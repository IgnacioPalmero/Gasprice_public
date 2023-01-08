import streamlit as st
import pandas as pd
import folium
import requests
import json
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import googlemaps
from time import sleep
from streamlit_folium import st_folium
import funciones


#Fecha
t = datetime.datetime.now()
fecha = t.strftime('%d/%m/%Y')

st.set_page_config(page_title="Mapa filtrado", page_icon="⛽")

tab_mapa, tab_competencia = st.tabs(["Mapa filtrado","Distribución de precios"])


# Primera pestaña 
                                                                                     
with tab_mapa:

    st.title('Mapa gasolineras')

    #response = requests.get('https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres')
    #js = json.loads(response.text)

    #df= pd.DataFrame(js['ListaEESSPrecio'])
   

    df = pd.read_csv("Gasolineras.csv")

    # Cambiar elementos vacíos por NaN

    df.replace("",np.nan, inplace=True)

    # Cambiar comas por puntos y castear a float 

    lista_gasolinas = list(df.columns[8:-11])
    lista_gasolinas.append("Latitud")
    lista_gasolinas.append("Longitud (WGS84)")

    for i in lista_gasolinas:
        funciones.comas_por_puntos(df, i)

    df.drop(["Margen", "Remisión"], axis = 1, inplace=True)

    option = st.selectbox('Selecciona una opción', options = ["Provincia", "Municipio", "C.P."])

    if option == "Provincia":

        provincia = st.selectbox('Selecciona una provincia', options = df["Provincia"].unique())

        df_mapa = df[df["Provincia"]==provincia]

        zoom = 9

        radio = 100

    elif option == "Municipio":

        municipio = st.selectbox('Selecciona un Municipio', options = df["Municipio"].unique(), help = ("Escribe las primeras letras del municipio para facilitar la búsqueda"))

        df_mapa = df[df["Municipio"]==municipio]

        zoom = 12

        radio = 15


    else:
        cp = st.selectbox('Escribe el C.P.', options = df["C.P."].unique())

        df_mapa = df[df['C.P.']==cp]

        zoom = 13

        radio = 5

    col_1, col_2, col_3 = st.columns(3)

    col_1.subheader("Proveedores\n")
    check_todas = col_1.checkbox("Todas las gasolineras",help="Seleccciona si quieres que aparezcan")
    check_repsol = col_1.checkbox("Repsol",help="Aparecerán las gasolineras Repsol con el icono naranja")
    check_cepsa = col_1.checkbox("Cepsa",help="Aparecerán las gasolineras Cepta con el icono rojo")
    check_bp = col_1.checkbox("BP",help="Aparecerán las gasolineras Cepta con el icono verde")

    col_2.subheader("Otras opciones")
    check_electro = col_2.checkbox("Electrolineras",help="Aparecerán los cargadores para vehiculos eléctricos")
    check_glp = col_2.checkbox("GLP",help="Aparecerán las gasolineras ue ofrecen gases licuados del petroleo (Icono negro)")
    check_gnl = col_2.checkbox("GNL",help="Aparecerán las gasolineras ue ofrecen gas natural licuado (Icono gris)")
    check_gnc = col_2.checkbox("GNC",help="Aparecerán las gasolineras ue ofrecen gas gas natural comprimido (Icono naranja)")

    col_3.subheader("Precio")
    check_cara = col_3.checkbox("Gasolinera más cara",help="Aparecerá la gasolinera más cara en rojo")
    check_barata = col_3.checkbox("Gasolinera más barata",help="Aparecerá la gasolinera más barata en verde")

    check_mapa = st.checkbox("Listo, muestrame el mapa!")


    lat = df_mapa["Latitud"].mean()
    long = df_mapa["Longitud (WGS84)"].mean()



    # Funciones

    def loc_gasolineras(data, color_p, color_s):
        for i, j, label, precio_gas, precio_diesel, horario, rot in zip(data["Latitud"], data["Longitud (WGS84)"], data["Dirección"], data["Precio Gasolina 95 E5"], data["Precio Gasoleo A"], data["Horario"], data["Rótulo"]): 
            
            gasolineras.add_child(folium.Marker(location     = [i, j],
                                                popup        = [f"Precio gasolina: {precio_gas}\n",
                                                                f"Precio diesel: {precio_diesel}\n",
                                                                f"Horario: {horario}\n",
                                                                rot,
                                                                label],
                                                icon         = folium.Icon(icon        = "fa-car",
                                                                        icon_color     = color_s,
                                                                        color          = color_p,
                                                                        prefix         = "fa")))


    def loc_min_max(serie, color_p , color_s):
    
        lat = serie["Latitud"]
        long = serie["Longitud (WGS84)"]
        precio_gas = serie["Precio Gasolina 95 E5"]
        precio_diesel = serie["Precio Gasoleo A"]
        horario = serie["Horario"]
        rot =serie["Rótulo"]
        label = serie["Dirección"]
        
        gasolineras.add_child(folium.Marker(location     = [lat, long],
                                            popup        = [f"Precio gasolina: {precio_gas}\n",
                                                            f"Precio diesel: {precio_diesel}\n",
                                                            f"Horario: {horario}\n",
                                                            rot,
                                                            label],
                                            icon         = folium.Icon(icon             = "fa-car",
                                                                    icon_color       = color_s,
                                                                    color            = color_p,
                                                                    prefix           = "fa")))


    #boton = st.button("Listo, muestrar el mapa")
    

    if check_mapa == True:


        #Obtenemos el mapa de la provincia
        mapa = folium.Map(location = [lat, long], zoom_start = zoom)

        # Inicializamos un FeatureGroup() para las gasolineras en el DataFrame
        gasolineras = folium.map.FeatureGroup()

        if check_todas == True:
            loc_gasolineras(df_mapa, "blue", "white")

        if check_repsol == True:

            df_repsol = funciones.filtro_proveedor(df_mapa, "REPSOL")

            loc_gasolineras(df_repsol, "blue", "orange")

        if check_cepsa == True:    

            df_cepsa = funciones.filtro_proveedor(df_mapa, "CEPSA")

            loc_gasolineras(df_cepsa, "blue", "red")

        if check_bp == True:

            df_bp = funciones.filtro_proveedor(df_mapa, "BP")

            loc_gasolineras(df_bp, "blue", "green")

        if check_barata == True:    

            df_min = df_mapa.sort_values('Precio Gasolina 95 E5').iloc[1]

            loc_min_max(df_min, "green", "white")

        if check_cara == True:

            df_max = df_mapa.sort_values('Precio Gasolina 95 E5', ascending=False).iloc[1]

            loc_min_max(df_max, "red", "white")

        if check_electro == True:

            df_places = funciones.extract_google_maps(lat, long, radio)

            for lat, lng, label, rating in zip(df_places["lat"], df_places["lng"], df_places["name"], df_places["rating"]):

                gasolineras.add_child(folium.Marker(location       = [lat, lng],
                                                    popup          = [label, f"Puntuación: {rating}"],
                                                    icon           = folium.Icon(icon = "fa-plug",
                                                    icon_color     = "white",
                                                    color          = "lightgreen",
                                                    prefix         = "fa")))

        if check_glp == True:

            df_glp = funciones.filtro_combustible(df_mapa, 'Precio Gases licuados del petróleo')

            for lat, lng,  precio, horario, label in zip(df_glp["Latitud"], df_glp["Longitud (WGS84)"], df_glp['Precio Gases licuados del petróleo'], df_glp["Horario"], df_glp["Dirección"]):

                gasolineras.add_child(folium.Marker(location       = [lat, lng],
                                                    popup          = [label, f"Precio GLP: {precio}"],
                                                    icon           = folium.Icon(icon = "fa-car",
                                                                    icon_color       = "white",
                                                                    color            = "black",
                                                                    prefix           = "fa")))       

        if check_gnl == True:

            df_gnl = funciones.filtro_combustible(df_mapa, 'Precio Gas Natural Licuado')

            for lat, lng,  precio, horario, label in zip(df_gnl["Latitud"], df_gnl["Longitud (WGS84)"], df_gnl['Precio Gas Natural Licuado'], df_gnl["Horario"], df_gnl["Dirección"]):

                gasolineras.add_child(folium.Marker(location       = [lat, lng],
                                                    popup          = [label, f"Precio GNL: {precio}"],
                                                    icon           = folium.Icon(icon = "fa-car",
                                                                    icon_color       = "white",
                                                                    color            = "lightgray",
                                                                    prefix           = "fa")))       
        
        if check_gnc == True:

            df_gnc = funciones.filtro_combustible(df_mapa, 'Precio Gas Natural Comprimido')

            for lat, lng,  precio, horario, label in zip(df_gnc["Latitud"], df_gnc["Longitud (WGS84)"], df_gnc['Precio Gas Natural Comprimido'], df_gnc["Horario"], df_gnc["Dirección"]):

                gasolineras.add_child(folium.Marker(location       = [lat, lng],
                                                    popup          = [label, f"Precio GNC: {precio}"],
                                                    icon           = folium.Icon(icon = "fa-car",
                                                                    icon_color       = "white",
                                                                    color            = "orange",
                                                                    prefix           = "fa")))   


        # Agrega gasolineras al mapa

        mapa.add_child(gasolineras)



        st_map = st_folium(mapa, width=900, height=550)
        st.text("* Haz click en los iconos para obtener la información de la gasolinera")

    df_historico = df_mapa[["Dirección", "Precio Gasoleo A", "Precio Gasoleo Premium", "Precio Gasolina 95 E5", "Precio Gasolina 98 E5"]]
    #df_historico.insert(0, 'Fecha', fecha)



with tab_competencia:

    st.title('Distribución de precios')

    col_tc_1, col_tc_2 = st.columns(2)

    col_tc_1.subheader("Distribución precios gasolina")
    col_tc_2.subheader("Distribución precios diesel")

    # distribucion precio gasolina

    fig = plt.figure(figsize = (5,3))

    sns.histplot(df_historico["Precio Gasolina 95 E5"],  kde = True)


    col_tc_1.pyplot(fig = fig)


    #Distribución precio diesel

    fig2 = plt.figure(figsize = (5,3))

    sns.histplot(df_historico["Precio Gasoleo A"],  kde = True)

    col_tc_2.pyplot(fig = fig2)


    # Preparamos el dato de los precios del día actual para el boxplot

    df_precios_localidad_hoy = df_historico.iloc[:,2:]


    # Cambiamos los NaN por la media de cada columna

    for i in df_precios_localidad_hoy.columns:
        
        df_precios_localidad_hoy[i].replace({np.nan : df_precios_localidad_hoy[i].mean()}, inplace = True)
        

    fig_box = plt.figure(figsize=(15,10))

    data = df_precios_localidad_hoy

    etiquetas = df_precios_localidad_hoy.columns

    fig = plt.boxplot(x = data, labels = etiquetas, meanline=True)

    st.pyplot(fig = fig_box)

    st.write(df_historico)





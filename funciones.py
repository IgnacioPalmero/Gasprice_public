import pandas as pd
import folium
import numpy as np
import googlemaps
from time import sleep


# Transformación

def comas_por_puntos(dataframe, columna):
    '''Cambia las comas por puntos y castea a float'''

    dataframe[columna] = dataframe[columna].apply(lambda x: float(x.replace(',', '.')) if pd.notnull(x) else x)


# Filtros

def filtro_proveedor(data, proveedor):
    return data[(data["Rótulo"]==proveedor)]

def filtro_provincia(data, provincia):
    provincia = provincia.upper()
    return data[(data["Provincia"]== provincia)]

def filtro_municipio(data, municipio):
    municipio = municipio.title()
    return data[(data["Municipio"]== municipio)]

def filtro_combustible(data, combustible):
    df_comb = data[(pd.isnull(data[combustible])==False)]
    return df_comb

# Mapas

def loc_gasolineras(data, color_p, color_s):
    for i, j, label, precio_gas, precio_diesel, horario, rot in zip(data["Latitud"], data["Longitud (WGS84)"], data["Dirección"], data["Precio Gasolina 95 E5"], data["Precio Gasoleo A"], data["Horario"], data["Rótulo"]): 
        
        gasolineras = folium.map.FeatureGroup()
        gasolineras.add_child(folium.Marker(location     = [i, j],
                                            popup        = [f"Precio gasolina: {precio_gas}\n",
                                                            f"Precio diesel: {precio_diesel}\n",
                                                            f"Horario: {horario}\n",
                                                            rot,
                                                            label],
                                            icon         = folium.Icon(icon           = "fa-car",
                                                                    icon_color     = color_s,
                                                                    color          = color_p,
                                                                    prefix         = "fa")))
            

def loc_min_max(serie, color_p , color_s):
    '''Dibuja en el mapa las gasolineras de la serie proporcionada
            serie: serie proporcionada
            color_p: color principal del icono
            color_s: color secundario del icono'''
    
    gasolineras = folium.map.FeatureGroup()
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





def extract_google_maps(lat, long, radio):
    
    '''Extrae un dataframe con los 60 principales cargadores de las coordenadas proporcionadas
            lat: latitud del punto que se quiere consultar
            long: longitud del punto que se quiere consultar
            radio: radio de aplicación'''
    
            
    # Se extraen las carácteristicas de los cargadores electricos de la api de google maps

    api_key = # Your google maps api_key

    gmaps = googlemaps.Client(key = api_key)


    params = {"query"     : "cargadores electricos",
            "location"   : [lat, long],
            "radius"     : radio,
            "page_token" : None}

    token = None

    places = gmaps.places(**params)

    stop = False

    data_places = list()

    while stop == False:
        
        sleep(3)
        
        params = {"query"     : "cargadores electricos",
                "location"   : [lat, long],
                "radius"     : 100,
                "page_token" : token}
        
        places = gmaps.places(**params)
        
        for p in places["results"]:
        
            formatted_address = p["formatted_address"]
            lat = p["geometry"]["location"]["lat"]
            lng = p["geometry"]["location"]["lng"]
            name = p["name"]
            place_id = p["place_id"]
            rating = p["rating"]
            types = "|".join(p["types"])
            user_ratings_total = p["user_ratings_total"]

            data_places.append([formatted_address, lat, lng, name, place_id, rating, types, user_ratings_total])
            
        try:
            token = places["next_page_token"]
            
        except:
            stop = True
            
            

    df_places = pd.DataFrame(data    = data_places,
                            columns = ["formatted_address", "lat", "lng", "name", "place_id",
                                        "rating", "types", "user_ratings_total"])

    return df_places
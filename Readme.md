# Getting started

This project is an automated data extraction and transformation process to obtain information about gasoline prices, the price of a barrel of oil in Spain and electric car chaging stations. 


A daily load of the data to airtable database is carried out in order to create a historical dataset of fuel prices.

Once the data is loaded, the application is ready to use the requests library to make requests to the Airtable API and obtain data on fuel prices and the price of a barrel of oil. It also uses the pandas library to process and treat the obtained data and the seaborn library to make graphs and visualizations. The numpy, matplotlib, folium, and plotly.express libraries have also been used to perform various tasks and visualizations.

An analysis of the correlation between fuel prices in Vigo and the price of crude oil is performed using a heatmap and a scatter plot. A linear regression model is also trained to predict the price of gasoline and diesel based on the price of crude oil.

Finally, various graphs and maps have been created to visualize the obtained information and comments and explanations have been included in the code to facilitate understanding.

In addition, it has been creted a webapp using streamlit that allows a user to view a map of a specific region in Spain and filter the information of the gas stations shown on the map. In addition, the user can view a chart with the distribution of gasoline prices at the selected gas stations.

The user can select the gas stations of the different providers (Repsol, Cepsa, BP) that they want to view on the map and can also choose to see electric vehicle chargers and gas stations that offer liquefied petroleum gas (GLP). In addition, the user can view a distribution of gasoline prices at the selected gas stations in a seaborn chart.

# Libraries used in Gasprice-extract-load.ipynb
import requests
import datetime
import json
import numpy as np
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
from time import sleep

# Libraries used in Gasprice-extract-load.ipynb
import requests
import datetime
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import plotly.express as px
from pprint import pprint
import googlemaps
from time import sleep

# Libraries used in streamlit_app.py
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

# Libraries used in funciones.py
import pandas as pd
import folium
import numpy as np
import googlemaps
from time import sleep

# Project API-keys

### The API-Keys used are private, so if you want to interact with a database to test the software, you need to create a creds.py file yourself with the following code:

API_KEY = #Your airtable api_key
api_key = #Your Google Maps API_KEY

# Tecnologies

folium==0.13.0
googlemaps==4.7.3
matplotlib==3.5.1
numpy==1.21.5
pandas==1.4.2
plotly==5.6.0
requests==2.27.1
seaborn==0.11.2
streamlit==1.16.0
streamlit_folium==0.7.0

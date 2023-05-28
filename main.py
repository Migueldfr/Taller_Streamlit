import streamlit as st
import pandas as pd
from PIL import Image # !pip install Pillow
import streamlit.components.v1 as components
import plotly.express as px
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import datetime


# Ajustamos la pagina con un icono en el buscador y el titulo
st.set_page_config(page_title="Pistas de Esqui", page_icon=":snowboarder:", layout="wide")

# Cargamos el Dataset con el que vamos a trabajar
pistas = pd.read_csv('data/pistas.csv')
pistas.rename(columns={"latitude":"lat", "longitude":"lon"}, inplace=True)

#Ponemos un titulo a nuestra aplicación
st.title("Pistas de esquí del mundo")


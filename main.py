import streamlit as st
import pandas as pd
from PIL import Image # !pip install Pillow
import streamlit.components.v1 as components
import plotly.express as px
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt


# Ajustamos la pagina con un icono en el buscador y el titulo
st.set_page_config(page_title="Pistas de Esqui", page_icon=":snowboarder:", layout="wide")

# Cargamos el Dataset con el que vamos a trabajar
pistas = pd.read_csv('data/pistas.csv')
pistas.rename(columns={"latitude":"lat", "longitude":"lon"}, inplace=True)

#Ponemos un titulo a nuestra aplicación
st.title("Pistas de esquí del mundo")

# Vamos a subir una foto desde url de internet
st.image("https://cdn.shopify.com/s/files/1/0012/8647/1793/articles/portada-definitiva-freeride.jpg?v=1622620556", width=800 )


# Creamos una caja con opciones para poder dirigirnos 
menu = st.sidebar.selectbox("Selecciona la página", ['Home','Filtros', 'Datasets'])

# Creamos contenido dentro de cada pestaña
if menu == "Home":

    # Ponemos un encabezado al nuestro dataset
    st.header("Datos con los que trabajamos")

    # Vamos a hacer una caja para marcar si queremos mostrarlo o no 
    if st.checkbox("Show"):
        pistas
    else:
        st.markdown('El Dataset esta oculto')

    # Vamos a crear pestañas y en cada una, vamos a meter un grafico 
    tab1, tab2, tab3, tab4 = st.tabs(["Localización", "Altura","Freeride","Distribución precios"])

    with tab1:

         # Ponemos un subencabezado de nuestro mapa
        st.subheader("Localización las pistas de esquí")
        st.map(pistas)

    with tab2:

        st.subheader("Altitud de las montañas")
        n = st.slider("Cuantas montañas quieres visualizar?",0,20)
        if n > 0:
            # Elaboramos un grafico de barras para determinar que Montaña es la mas alta
            altitud = pistas[['Nombre del Resort','Continente','Altitud','Km de Freeride']].sort_values(ascending=False,by='Altitud').head(n)
            altitud['Orden'] = range(len(altitud))
            resort_order = altitud.sort_values(by='Orden')['Nombre del Resort'].unique()

            fig = px.bar(altitud, y='Nombre del Resort', x='Altitud', color='Continente',
                     category_orders={'Nombre del Resort': resort_order},
                     labels={'Nombre del Resort': 'Resort', 'Altitud': 'Altitud'},
                     hover_data=['Continente'], text='Altitud',orientation='h')
            fig.update_layout(xaxis_tickangle=85, width=1000, height=800)
            fig.update_xaxes(title='Resorts')
            fig.update_yaxes(title='Altitud')
            st.plotly_chart(fig,use_container_width=True)
    
    with tab3:

        st.subheader("KM freeride")

        freeride = pistas[['Nombre del Resort','Continente','Km de Freeride','Esqui de fondo y senderos']].sort_values(ascending=False,by='Km de Freeride')
        freeride.dropna(inplace=True)
        n = st.slider("Cuantas montañas quieres visualizar?",0,50)

        if n > 0:
            fig = px.bar(freeride.head(n), x='Nombre del Resort', y='Km de Freeride', color='Continente',
                 #category_orders={'Nombre del Resort': resort_order},
                 labels={'Nombre del Resort': 'Resort', 'Km de Freeride': 'Km de Freeride'},
                 hover_data=['Continente'], text='Esqui de fondo y senderos')
            fig.update_layout(xaxis_tickangle=85, width=1000, height=800)
            y_ticks = np.arange(0, 201, 20)
            fig.update_yaxes(title = 'Altitud', tickvals=y_ticks)
            fig.update_xaxes(title = 'Resorts')

            st.plotly_chart(fig,use_container_width=True)
    
    with tab4:

        st.subheader("Distribución precios")

        # Box Plot con los precios por contienete 

    # Con esto ordenamos los continentes para que se vean ordenados, tan solo los continentes y esto lo sacamos con index.
    pistas_orden = pistas.groupby('Continente')[['Precio']].mean().sort_values(ascending=False, by='Precio').index
    
    plt.figure(figsize=(12,6))
    sns.boxplot(x = pistas['Continente'],y = pistas['Precio'], order=pistas_orden)


elif menu == 'Filtros':

    #Creamos un barra a deslizar con las diferentes opciones que vamos a poner a continuacion.
    st.sidebar.header('Opciones a filtrar: ')

    # Obtenemos los valores unicos de las columnas a filtrar
     
    continente = st.sidebar.multiselect("Seleccionamos el Continente: ",
                options = pistas['Continente'].unique(),
                default= pistas['Continente'].unique())
    
    pais = st.sidebar.multiselect("Selecciona el País: ",
                options = pistas['Pais'].unique(),
                default= pistas['Pais'].unique())
    
    rate = st.sidebar.slider("Selecciona la valoración: ", min(pistas['Rate']), max(pistas['Rate']), (min(pistas['Rate']), max(pistas['Rate'])))    

    precio = st.sidebar.slider("Selecciona el precio: ", min(pistas['Precio']), max(pistas['Precio']), (min(pistas['Precio']), max(pistas['Precio'])))

    # Unimos todas las cajas que hemos creado a nuestro dataset para visualizar
    df_seleccion = pistas.query('Continente == @continente & Pais == @pais & Rate >= @rate[0] & Rate <= @rate[1] & Precio >= @precio[0] & Precio <= @precio[1]')
    
    st.markdown('-----')

    # Creamos un grafico de barras para visualizar Rates
    rate = df_seleccion[['Nombre del Resort','Continente','Pais','Rate']].sort_values(by='Rate', ascending=False)

    rate['Orden'] = range(len(rate))

    resort_order = rate.sort_values(by='Orden')['Nombre del Resort'].unique()

    fig = px.bar(rate.head(20), x='Nombre del Resort', y='Rate', color='Continente',
                    category_orders={'Nombre del Resort': resort_order},
                 labels={'Nombre del Resort': 'Resorts', 'Rate': 'Rate'},
                 hover_data=['Continente'], text='Rate')

    fig.update_layout(title_text='Valoración', xaxis_tickangle=85, width=1000, height=800)
    fig.update_xaxes(title = 'Resorts')
    fig.update_yaxes(title = 'Rate')

    st.plotly_chart(fig,use_container_width=True)

    st.markdown('-----')

    # Creamos un grafico de barras para visualizar Precios
    precio = df_seleccion[['Nombre del Resort','Continente','Precio']].sort_values(by='Precio', ascending=False).head(20)

    fig = px.bar(precio, x='Nombre del Resort', y='Precio', color='Continente',
                 hover_data=['Continente'], text='Precio')
    fig.update_layout(title_text='Precio', xaxis_tickangle=85, width=1000, height=800)
    fig.update_xaxes(title = 'Resorts')
    fig.update_yaxes(title = 'Precio')

    st.plotly_chart(fig,use_container_width=True)
#
#-------------------
    #apres = st.sidebar.multiselect("Selecciona el precio: ",
    #            options = pistas['Precio'].unique(),
    #            default= pistas['Precio'].unique())

elif menu == 'Datasets':

    st.markdown('HOLA')


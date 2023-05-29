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

st.image('https://bextremeboards.com/blog/wp-content/uploads/2019/08/Screen-Shot-2019-02-11-at-20.24.42.jpg', width=800)
# o
#descarga = st.file_uploader('Subir imagen', accept_multiple_files=True)
#st.image(descarga)

menu = st.sidebar.selectbox("Seleccionamos la página", ['Home','Filtros', 'Dataset'])

if menu == 'Home':

    st.header('Datos con los que trabajamos')

    if st.checkbox('Mostrar'):
        pistas
    else:
        st.markdown('El dataset esta oculto')

    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Localizacion','Freeride','Altura','Distribucion de los precios','Distribucion de las pistas'])

    with tab1:

        st.subheader('Localizacion de pistas de esqui')
        st.map(pistas)

    with tab2:

        st.subheader('Km freeride')
        n = st.slider('Cuantas montañas quieres visualizar?', 0, 20)

        freeride = pistas[['Nombre del Resort','Continente','Km de Freeride','Esqui de fondo y senderos']].sort_values(ascending=False,by='Km de Freeride')
        freeride.dropna(inplace=True)

        fig = px.bar(freeride.head(n), x='Nombre del Resort', y='Km de Freeride', color='Continente',
                     #category_orders={'Nombre del Resort': resort_order},
                     labels={'Nombre del Resort': 'Resort', 'Km de Freeride': 'Km de Freeride'},
                     hover_data=['Continente'], text='Esqui de fondo y senderos')
        fig.update_layout(title_text='KM freeride', xaxis_tickangle=85, width=1000, height=800)
        fig.update_xaxes(title = 'Resorts')
        y_ticks = np.arange(0, 201, 20)
        fig.update_yaxes(title = 'Altitud', tickvals=y_ticks)


        st.plotly_chart(fig ,use_container_width=True)

    with tab3:

        st.subheader('Altitud de las montañas')

        altitud = pistas[['Nombre del Resort','Continente','Altitud','Km de Freeride']].sort_values(ascending=False,by='Altitud')
        n = st.slider('Cuantas montañas quieres visualizar?', 0, 20, key = 'tab3')
        # Alturas de la montañas
        altitud['Orden'] = range(len(altitud))

        resort_order = altitud.sort_values(by='Orden')['Nombre del Resort'].unique()

        if n > 0:
            # Crear el gráfico de barras
            fig = px.bar(altitud.head(n), x='Nombre del Resort', y='Altitud', color='Continente',
                         category_orders={'Nombre del Resort': resort_order},
                         labels={'Nombre del Resort': 'Resort', 'Altitud': 'Altitud'},
                         hover_data=['Continente'], text='Altitud')

            fig.update_layout(title_text='Resorts Esquiables', xaxis_tickangle=85, width=1000, height=800)
            fig.update_xaxes(title='Resorts')
            fig.update_yaxes(title='Altitud')

            st.plotly_chart(fig, use_container_width=True)
     
    with tab4:

        st.subheader('Distribucion de los precios')

        pistas_orden = pistas.groupby('Continente')[['Precio']].mean().sort_values(ascending=False, by='Precio').index
 
        plt.figure(figsize=(12,6))
        sns.boxplot(x = pistas['Continente'],y = pistas['Precio'], order=pistas_orden)
    
        st.pyplot(plt)

    with tab5:

        pistas_pais = pistas.groupby(['Pais','Continente','ISO Code'])['Nombre del Resort'].count().sort_values(ascending=False)
        pistas_pais = pd.DataFrame(pistas_pais).reset_index()

        fig = px.scatter_geo(pistas_pais, locations=pistas_pais['ISO Code'], color=pistas_pais.Continente,
                     hover_name=pistas_pais.Pais, size=pistas_pais['Nombre del Resort'],
                     projection="natural earth")

        st.plotly_chart(fig, use_container_width=True)

elif menu == 'Filtros':

    st.sidebar.header('Opciones a filtrar: ')


    continente = st.sidebar.multiselect('Seleccionamos Continente: ',
                        options = pistas['Continente'].unique(),
                        default= pistas['Continente'].unique())
    
    pais = st.sidebar.multiselect('Seleccionamos Pais: ',
                        options = pistas['Pais'].unique(),
                        default= pistas['Pais'].unique())
    
    rate = st.sidebar.slider('Selecionar valoracion: ', min(pistas['Rate']), max(pistas['Rate']), (min(pistas['Rate']), max(pistas['Rate'])))


    precio = st.sidebar.slider('Selecionar precio: ', min(pistas['Precio']), max(pistas['Precio']), (min(pistas['Precio']), max(pistas['Precio'])))

    df_seleccion = pistas.query('Continente == @continente & Pais == @pais & Rate >= @rate[0] & Rate <= @rate[1] & Precio >= @precio[0] & Precio <= @precio[1]')

    st.markdown('------')

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

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('----')

    precio = df_seleccion[['Nombre del Resort','Continente','Precio']].sort_values(by='Precio', ascending=False)

    precio['Orden'] = range(len(rate))

    resort_order = precio.sort_values(by='Orden')['Nombre del Resort'].unique()

    fig = px.bar(precio.head(20), x='Nombre del Resort', y='Precio', color='Continente',
                    category_orders={'Nombre del Resort': resort_order},
                 labels={'Nombre del Resort': 'Resorts', 'Rate': 'Rate'},
                 hover_data=['Continente'], text='Precio')

    fig.update_layout(title_text='Precio', xaxis_tickangle=85, width=1000, height=800)
    fig.update_xaxes(title = 'Resorts')
    fig.update_yaxes(title = 'Precio')

    st.plotly_chart(fig, use_container_width=True)

elif menu == 'Dataset':

    nombre = st.text_input('Nombre del resort', "")
    continente = st.selectbox('Continente', pistas['Continente'].unique())
    rate = st.slider('Cual es la valoracion?', 1,5)
    review = st.text_area('Comentario',"")
    precio = st.text_input('Que precio es el forfait?', "")
    dia = st.date_input(f"Hoy es... ", datetime.datetime.now())

    nueva_data = []

    nueva_data.append({
        'Nombre del Resort': nombre ,
        'Continente':continente,
        'Rate' : rate,
        'Comentario' : review,
        'Precio' : precio,
        'Dia' : dia
    })

    if st.button('Submit'):
        nueva_data.append({
        'Nombre del Resort': nombre ,
        'Continente':continente,
        'Rate' : rate,
        'Comentario' : review,
        'Precio' : precio,
        'Dia' : dia
    })
    
    df = pd.DataFrame(nueva_data)
    st.dataframe(df)

    if st.button('Export to CSV'):
        df.to_csv('data.csv')
        st.success('CSV exportado correctamente')

        


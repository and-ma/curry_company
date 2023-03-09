#Bibliotecas
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Site 1", page_icon=';)', layout='wide')

#Dados
df = pd.read_csv('train.csv')

#Limpeza
linhas = df['Delivery_person_ID']!='NaN '
df = df.loc[linhas,:]

linhas = df['Weatherconditions']!='NaN '
df = df.loc[linhas,:]

linhas = df['Road_traffic_density']!='NaN '
df = df.loc[linhas,:]

linhas = df['Type_of_order']!='NaN '
df = df.loc[linhas,:]

linhas = df['Type_of_vehicle']!='NaN '
df = df.loc[linhas,:]

linhas = df['City']!='NaN '
df = df.loc[linhas,:]

#Conversão
df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

#Site
st.header("Marketplace - Visão Cliente")

im_path = 'im.jpg'
image = Image.open(im_path)
st.sidebar.image(image, width=250)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""___""")

st.sidebar.markdown("## Selecione uma data limite")

date_slider = st.sidebar.slider("Até qual valor?",
                  value=pd.datetime(2022,4,13),
                  min_value=pd.datetime(2022,2,11),
                  max_value=pd.datetime(2022,4,6),
                  format="DD-MM-YYYY")

st.sidebar.markdown("""___""")

traffic = st.sidebar.multiselect("Quais as condições de trânsito?",
                       ["Low ","Medium ","High ","Jam "],
                       default="Low ")

st.sidebar.markdown("""___""")

#Filtro de data
linhas = df['Order_Date']<date_slider
df = df.loc[linhas,:]

#Filtro de tráfego
linhas = df['Road_traffic_density'].isin(traffic)
df = df.loc[linhas,:]
st.dataframe(df)
############################################################################################################
tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])

with tab1:
    with st.container():
        st.markdown("# Orders by day")
        df_aux = df.loc[:,['ID','Order_Date']].groupby('Order_Date').count().reset_index()
        fig = px.bar(df_aux, x='Order_Date', y='ID')
        st.plotly_chart(fig,use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("# Traffic Order Share")
            df_aux = df.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['perc'] = df_aux['ID']/df_aux['ID'].sum()
            fig = px.pie(df_aux, values='perc', names='Road_traffic_density')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("# Traffic Order City")
            df_aux = df.loc[:,['ID','Road_traffic_density','City']].groupby(['City','Road_traffic_density']).count().reset_index()
            fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID')
            st.plotly_chart(fig,use_container_width=True)
            
with tab2:
    with st.container():
        df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )
        df_aux = df.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
        fig = px.line(df_aux, x='week_of_year', y='ID')
        st.plotly_chart(fig,use_container_width=True)
        
    with st.container():
        df_aux1 = df.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux2 = df.loc[:,['Delivery_person_ID','week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner')
        df_aux['order'] = df_aux['ID']/df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x='week_of_year', y='order')
        st.plotly_chart(fig,use_container_width=True)
        
with tab3:
    with st.container():
        df_aux = df.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
        map = folium.Map(zoom_start=11)
        for index, location in df_aux.iterrows():
            folium.Marker([location['Delivery_location_latitude'],
                          location['Delivery_location_longitude']],
                         popup=location[['City','Road_traffic_density']]).add_to(map)
        folium_static(map,1024,600)
    

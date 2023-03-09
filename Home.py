import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=":)"
)

image_path = 'im.jpg'
image = Image.open(image_path)
st.sidebar.image(image,width=120)
st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard")
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento
    dos Entregadores e Restaurantes.
    ### Como utilizar?
    - Visão Gerencial: Métricas gerais de comportamento.
    - Visão Tática: Indicadores semanais de crescimento.
    - Visão Geográfica: Insights de geolocalização.
    """)

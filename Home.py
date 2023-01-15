import pandas as pd
import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth 
import yaml
from PIL import Image

st.set_page_config(page_title="Home Page", page_icon=":soccer:", layout="wide")

@st.cache
def read_info(path):
    return Path(path).read_text(encoding='utf8')


st.title("Best Scouters find Best Players ")
image1 = Image.open('loginn.jpeg')
st.image(image1,channels="RGB", output_format="auto")
st.markdown(read_info('scouters.md'), unsafe_allow_html=True)
st.sidebar.header("Menu")
image = Image.open('scouterr.jpeg')
image2= Image.open('sid.jpeg')
st.sidebar.image(image2,channels="RGB", output_format="auto")
st.sidebar.image(image,channels="RGB", output_format="auto",width=336)
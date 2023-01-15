import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from PIL import Image



st.set_page_config(page_title="Login Page", page_icon=":bar_chart:", layout="wide")

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

st.title(":soccer: Welcome to Best Scouting Tool :soccer: ")
username = st.text_input("User Name")
password = st.text_input("Password",type='password')

create_usertable()
hashed_pswd = make_hashes(password)
result = login_user(username,check_hashes(password,hashed_pswd))
if st.button("Login"):
 if result:
    st.success("Logged In as {}".format(username))
 else:
    st.warning("Incorrect Login Attempt. Can you try again?")
image = Image.open('s.jpeg')
col1, col2, col3 = st.columns([1,6,1])




with col1:
 st.write("")

with col2:
 st.image(image,channels="RGB", output_format="auto")

with col3:
 st.write("")

st.sidebar.header("Menu")
image = Image.open('scouterr.jpeg')
image1= Image.open('sid2.jpeg')
st.sidebar.image(image1,channels="RGB", output_format="auto")
st.sidebar.image(image,channels="RGB", output_format="auto",width=336)
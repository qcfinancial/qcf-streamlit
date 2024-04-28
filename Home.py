import streamlit as st
from PIL import Image
import requests
import sqlite3 as sql

st.set_page_config(
    page_title="Inicio",
    page_icon=Image.open('assets/favicon-32x32.png'),
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.image('./assets/econsult.png', width=250)

st.sidebar.title("Derivatives Platform")


def login(username: str, password: str) -> str | int:
    URL = "http://127.0.0.1:8000/user/token"
    response = requests.post(URL, data={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state.username = username
        st.session_state.token = response.json()["access_token"]
    return response.status_code


if "token" not in st.session_state:
    st.title("Login")
    with st.form("Login"):
        username = st.text_input("Enter your email")
        password = st.text_input("Enter your password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            status_code = login(username, password)
            if status_code == 200:
                URL = f"http://127.0.0.1:8000/user/{username}"
                response = requests.get(URL, headers={'Authorization': f"Bearer {st.session_state.token}"})
                st.session_state.full_name = response.json()["full_name"]
                st.session_state.client = response.json()["client"]
                st.success(f"Welcome {st.session_state.full_name}")
            else:
                st.error("Login failed")

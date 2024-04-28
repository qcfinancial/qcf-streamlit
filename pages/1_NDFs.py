import pandas as pd
import streamlit as st
from PIL import Image
import requests

from models.data_types import (
    Product,
    TypeLeg,
    Bank
)
from models.operations import OperationDaily

st.set_page_config(
    page_title="NDFs",
    page_icon=Image.open('./assets/favicon-32x32.png'),
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("NDFs")

if "token" not in st.session_state:
    st.error("You need to login first.")
else:
    action = st.sidebar.selectbox("Select Action", options=["New Operation", "Delete Operation"])
    st.text_input("Client", value=st.session_state.client, disabled=True)
    if action == "New Operation":
        col1, col2 = st.columns(2)
        with col1:
            fx_rate = st.selectbox(
                "Enter FX Rate",
                options=["USDCLP", "CLFCLP"],
            )
            counterparty = st.selectbox("Enter Counterparty", options=["SANTANDER", "BCI", ])
            amount = st.number_input(
                f"Enter Amount in {fx_rate[0:3]}",
                min_value=0.0,
                max_value=100_000_000.0,
                step=100.0,
                format="%.2f"
            )
            forward_price = st.number_input(
                f"Enter Forward Price",
                min_value=0.0,
                max_value=2_000.0 if fx_rate == "USDCLP" else 50_000.0,
                step=100.0,
                format="%.2f"
            )
        with col2:
            weak_amount = st.text_input(
                f"Amount in {fx_rate[3:]}",
                value=f"{amount * forward_price:,.2f}",
                disabled=True,
            )
            fx_fixing_date = st.date_input("Enter FX Fixing Date")
            settlement_date = st.date_input(
                "Enter Settlement Date",
                min_value=fx_fixing_date,
                value=fx_fixing_date
            )
            fx_rate_index_dict = {
                "USDCLP": "USDOBS",
                "CLFCLP": "UF",
            }
            fx_rate_index = st.text_input(
                f"FX Rate Index",
                value=f"{fx_rate_index_dict[fx_rate]}",
                disabled=True,
            )

        submit = st.button("Insert Operation")
        if submit:
            st.success("Operation submitted!")

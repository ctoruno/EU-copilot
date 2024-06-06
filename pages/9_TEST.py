import streamlit as st
from io import BytesIO
from inputs.paragraph import paragraph
import os
import dropbox
import dropbox.files
import requests
import json
# from dotenv import load_dotenv
from tools import passcheck

if passcheck.check_password():

    # Page config
    st.set_page_config(
        page_title = "GPP Country Validation",
        page_icon  = "🇪🇺"
    )
    # Reading CSS styles
    with open("styles.css") as stl:
        st.markdown(f"<style>{stl.read()}</style>", 
                    unsafe_allow_html=True)

    # Defining auth secrets (when app is already deployed)
    dbtoken  = st.secrets["dbtoken"]
    dbkey    = st.secrets["app_key"]
    dbsecret = st.secrets["app_secret"]

    atoken = passcheck.retrieve_DBtoken(dbkey, dbsecret, dbtoken)
    st.write(atoken)
"""
Module Name:    Password Check
Author:         Carlos Alberto Toruño Paniagua
Date:           May 20th, 2024
Description:    This module contains all the functions and classes to be used by the EU Copilot 
                Dashboard for visualizing GPP data.
This version:   May 20th, 2024
"""
import streamlit as st
import requests
import json

# Defining a function to check for password
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True
    
def retrieve_DBtoken(key, secret, refresh_token):
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': key,
        'client_secret': secret,
    }
    response = requests.post('https://api.dropbox.com/oauth2/token', data = data)
    response_data = json.loads(response.text)
    access_token  = response_data["access_token"]
    return access_token
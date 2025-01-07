"""
Project:        EU Copilot App
Module Name:    Media Reports Page
Author:         Carlos Alberto Toruño Paniagua
Date:           March 22nd, 2024
Description:    This module contains the code of the Media Repos tab for the EU Copilot App
This version:   March 24h, 2024
"""

import json
import re
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
from tools import sidemenu

if "country_track" not in st.session_state:
    st.session_state["country_track"] = False
if "search_track" not in st.session_state:
    st.session_state["search_track"] = False

def update_tracking(button_name):
    st.session_state[button_name] = True

# Page config
st.set_page_config(
    page_title = "Codebooks",
    # page_icon  = "📰"
    page_icon  = "🗞️"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)
    
# Sidebar menu
sidemenu.insert_smenu()

# Header and explanation
# st.markdown("<h1 style='text-align: center;'>Media Reports</h1>", 
#             unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    The Media Reports tab is no longer an available feature of the EU-S Copilot. If you wish to search and view the results of the World Justice Project's 
    massive webscraping exercise of Rule of Law related articles for each of the 27 active members of the European Union, as well as detailed summaries, classification results, 
    frequency analyses and topic modelling, please visit the following link: <a href='https://eu-rol-tracker.streamlit.app/Media_Reports' target='_blank'><b><i>https://eu-rol-tracker.streamlit.app/Media_Reports</i></b></a>.
    </p>
    """,
    unsafe_allow_html=True
)
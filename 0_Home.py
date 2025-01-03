"""
Project:        EU Copilot App
Module Name:    Master app script
Author:         Carlos Alberto Toruño Paniagua
Date:           October 19th, 2023
Description:    This module contains the home page code for the EU Copilot App
This version:   October 23rd, 2023
"""

import streamlit as st
import pandas as pd
from tools import sidemenu

# Page config
st.set_page_config(
    page_title = "Home",
    page_icon  = "house"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Sidebar menu
sidemenu.insert_smenu()
    
# Reading Codebook & DataMap
@st.cache_data
def load_datamap():
    datamap = pd.read_excel("inputs/EU2 GPP 2023 Full Datamap.xlsx", 
                            sheet_name = "Data Map")
    return datamap

@st.cache_data
def load_codebook():
    datamap = pd.read_excel("inputs/EU2 GPP 2023 Codebook.xlsx", 
                            sheet_name = "Codebook")
    return datamap

datamap  = load_datamap()
codebook = load_codebook() 

# st.markdown("<h1 style='text-align: center;'>EU-S Copilot</h1>", 
#             unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    The <strong style="color:#003249">EU-S Copilot</strong> is a web app designed to assist Data Analysts 
    in their data-cleaning, harmonizing, and validation tasks for data collected from public opinion polls 
    and expert-coded questionnaires.
    </p>
    
    <p class='jtext'>
    In the <strong style="color:#003249">GPP Tools tab</strong>, you'll discover a versatile toolkit that's 
    your trusty sidekick for tackling common challenges when cleaning public opinion poll data.
    </p>

    <p class='jtext'>
    Check out the <strong style="color:#003249">Codebooks tab</strong> for an interactive tool that helps 
    you easily access essential dataset information related to variables in the most recent EU GPP and 
    QRQ questionnaires.
    </p>

    <p class='jtext'>
    In the <strong style="color:#003249">Media Reports tab</strong> you'll encounter the results of a massive
    webscrapping exercise of news articles related to the Rule of Law, summarized and classify through AI. 
    The results are presented by country and thematic pillar.
    </p>

    <p class='jtext'>
    If you wish to preview the data in real time, you can take a look at the 
    <strong style="color:#003249">Dashboard tab</strong>, where you can find interactive maps showing you the
    latest results obtained from the GPP and QRQ data.
    </p>

    <p class='jtext'>
    If you're curious for more details about the app or if you have questions, suggestions or you want to report 
    a bug,  hop on over to the <strong style="color:#003249">Info tab</strong> in the left side bar panel.
    </p>

    <p class='jtext'>
    Galingan!
    </p>
    """,
    unsafe_allow_html = True
)
"""
Project:        EU Copilot App
Module Name:    Dashboard
Author:         Carlos Alberto Toruño Paniagua
Date:           April 29th, 2024
Description:    This module contains the code of the Dashboard tab for the EU Copilot App
This version:   April 29th, 2024
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px

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

if check_password():

    # Page config
    st.set_page_config(
        page_title = "Dashboard",
        page_icon  = "📶"
    )

    # Reading CSS styles
    with open("styles.css") as stl:
        st.markdown(f"<style>{stl.read()}</style>", 
                    unsafe_allow_html=True)
        
    # Reading data
    @st.cache_data
    def load_data_points():
        df = pd.read_csv("https://github.com/WJP-DAU/eu-gpp-report/raw/main/data-viz/data_points.csv")
        return df

    @st.cache_data
    def load_rlabels():
        df = pd.read_excel("https://github.com/WJP-DAU/eu-gpp-report/raw/main/data-viz/inputs/region_labels.xlsx")
        return df

    @st.cache_data
    def load_outline():
        df = pd.read_excel("https://github.com/WJP-DAU/eu-gpp-report/raw/main/data-viz/inputs/report_outline_1.xlsx")
        return df

    @st.cache_data
    def load_mlayer():
        df = gpd.read_file("https://raw.githubusercontent.com/ctoruno/ROLI-Map-App/main/Data/EU_base_map.geojson").to_crs(epsg=4326)
        return df
        
    data_points   = load_data_points()
    region_labels = load_rlabels()
    outline       = load_outline()
    eu_nuts       = load_mlayer()

    # Header and explanation
    st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", 
                unsafe_allow_html=True)
    st.markdown(
        """
        <p class='jtext'>
        Welcome to the <strong style="color:#003249">GPP Dashboard</strong>. In this page you can preview the GPP data
        as soon as it is cleaned and harmonized into our clouds. The data presented here is just a preview and 
        <b><i>BY NO MEANS should be considered final or official</i></b>. Please use the filters below to navigate through
        the questions of our data.

        Galingan!
        </p>
        """,
        unsafe_allow_html = True
    )

    # Filters
    chapter = st.selectbox(
        "Please select a thematic chapter from the list below",
        (outline
        .drop_duplicates(subset = "chapter")
        .chapter.to_list())
    )
    section = st.selectbox(
        "Please select a thematic section from the list below",
        (outline
        .loc[outline["chapter"] == chapter]
        .drop_duplicates(subset = "section")
        .section.to_list())
    )
    chart = st.selectbox(
        "Please select a graph from the list below",
        (outline
        .loc[outline["section"] == section]
        .drop_duplicates(subset = "title")
        .title.to_list())
    )

    st.markdown("-----")

    # Subsetting and preparing data
    chart_n = outline.loc[outline["title"] == chart, "n"].iloc[0]
    target_data_points = (
        data_points.copy()
        .loc[data_points["chart"] == chart_n]
    )
    data4map = pd.merge(
        target_data_points,
        region_labels[["nuts_id", "nameSHORT"]],
        how = "left",
        on  = "nuts_id"
    )
    data4map["value2plot"] = data4map["value2plot"]*100

    # Defining Annotations
    title    = outline.loc[outline["n"] == chart_n].title.iloc[0]
    subtitle = outline.loc[outline["n"] == chart_n].subtitle.iloc[0]

    st.markdown(
        f"""
        <h4 style='text-align: left;'>{title}</h4>
        <h6 style='text-align: left;'><i>{subtitle}</i></h6>
        <br>
        """, 
        unsafe_allow_html=True
    )

    # drawing map
    direction   = outline.loc[outline["n"] == chart_n].direction.iloc[0]
    color_codes = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
    if direction == "Negative":
        color_palette = color_codes[::-1]
    else:
        color_palette = color_codes
    
    fig = px.choropleth_mapbox(
        data4map,
        geojson      = eu_nuts,
        locations    = "nuts_id",
        featureidkey = "properties.polID",
        mapbox_style = "carto-positron",
        center       = {"lat": 52.250, "lon": 13.025},
        custom_data  = ["nameSHORT", "value2plot"],
        zoom         = 3,
        color        = "value2plot",
        color_continuous_scale = color_palette
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]}<br>Value: %{customdata[1]:.1f}%",
        # marker = dict(
        #     opacity = 0.5
        # )
    )
    fig.update_layout(
        margin = {"r":0,"t":0,"l":0,"b":0},
        height = 800,
        coloraxis_colorbar = dict(
            title   = "Percentage(%)",
            x       = 0,
            xanchor ="left",
            y       = -0.1,
            yanchor = "bottom", 
            orientation = "h", 
        )
    )
    st.plotly_chart(fig)
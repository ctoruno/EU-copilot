"""
Module Name:    Viz Tools
Author:         Carlos Alberto Toruño Paniagua
Date:           May 20th, 2024
Description:    This module contains all the functions and classes to be used by the EU Copilot 
                Dashboard for visualizing GPP data.
This version:   May 20th, 2024
"""
import plotly.express as px
import streamlit as st

def genBars(data, cpal):
    fig = px.bar(
        data, 
        x = "value_realign", 
        y = "title",
        color = "value_realign", 
        orientation  = "h",
        range_color  = [0,100],
        custom_data  = ["title", "value_realign", "direction"],
        color_continuous_scale = cpal,
        color_continuous_midpoint = 50
    )
    fig.update_traces(
        hovertemplate = "%{customdata[0]}<br>Value: %{customdata[1]:.1f}%<br>Direction: %{customdata[2]}",
        marker = dict(showscale = False)
    )
    fig.update(
        layout_coloraxis_showscale=False
    )
    fig.update_layout(
        xaxis_title = "Percentage (%)",
        yaxis_title = None,
        showlegend  = False,
        margin = {"r":0,"t":0,"l":0,"b":0},
        xaxis  = dict(
            range = [0, 100],
            dtick = 20
        ),
        yaxis = dict(
            tickmode = "linear"
        )
    )
    return fig

def genMetrics(n, df, d = ""):
    subsection = df.iloc[n]["subsection"]
    avg_value  = round(df.iloc[n]["average_value"], 1)
    card = st.metric(f":{d}[{subsection}]", f"Avg: {avg_value}")
    return card

# def genBees
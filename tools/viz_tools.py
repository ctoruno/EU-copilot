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

def genBees(country_data, country_select):
    fig = px.strip(
        country_data, 
        y = "subsection", 
        x = "value_realign", 
        stripmode   = "group",
        color       = "country_name_ltn", 
        custom_data = ["title", "value_realign", "country_name_ltn"]
    )
    fig.update_traces(
        hovertemplate="%{customdata[2]}<br>%{customdata[0]}<br>Value: %{customdata[1]:.1f}%",
    )
    for trace in fig.data:
        trace.update(opacity = 0.05)
    fig.for_each_trace(
        lambda trace: trace.update(opacity=1.0) if trace.name in country_select else None
    )
    fig.update_layout(
        height = 1100,
        xaxis_title = None,
        yaxis_title = None,
        template    = "plotly_white",
        showlegend  = False,
    )
    return fig

def genDots(data, topic, groupings, stat):
    if stat == "Data Points":
        xaxis = "value2plot"
    if stat == "Deviations from National Average":
        xaxis = "dev"
    
    grouping_pattern = "|".join(groupings)

    subset4charts = (
        data.copy()
        .loc[(data["topic"] == topic) & (data["region"].str.contains(grouping_pattern))]
    )
    fig = px.scatter(
        subset4charts,
        x = xaxis,
        y = "title",
        title = topic,
        color = "region",
        color_discrete_sequence=px.colors.qualitative.G10,
        facet_col="grouping",
        facet_col_spacing = 0.04,
        category_orders={"grouping": groupings}
    )
    fig.update_layout(
        height = 400,
        xaxis_title = None,
        yaxis_title = None,
        template    = "plotly_white",
        showlegend  = False,
    )

    return fig
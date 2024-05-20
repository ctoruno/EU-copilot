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
        # layout="wide"
    )

    # Reading CSS styles
    with open("styles.css") as stl:
        st.markdown(f"<style>{stl.read()}</style>", 
                    unsafe_allow_html=True)
        
    # Reading data
    @st.cache_data
    def load_data_points():
        df = pd.read_csv("https://github.com/WJP-DAU/eu-gpp-report/raw/main/data-viz/data_points.csv")
        df["value2plot"] = df["value2plot"]*100

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

    def realign_data(value, direction):
        if direction == "Positive":
            return value
        if direction == "Negative":
            return 100-value
        
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
        <b><i>BY NO MEANS should be considered final or official</i></b>.
        </p>
        <p class='jtext'>
        You have three options available:
            <ol>
                <li>
                    <b>Regional Overview</b>: Where you can view the overall performance of the 27 active members of the 
                    European Union
                </li>
                <li>
                    <b>Country Profile</b>: Where you can view the overall performance of a specific country across all
                    of our indicators
                </li>
                <li>
                    <b>Indicator Level</b>: Where you can search for specific indicators and explore the regional and national
                    performance of countries for that specific indicator.
                </li>
            </ol>
        </p>

        <p class='jtext'>
        Galingan!
        </p>
        """,
        unsafe_allow_html = True
    )

    # Defining tabs (Indicator Level)
    eutab, countrytab, vartab = st.tabs(["EU Overview", "Country Profile", "Indicator Level"])

    with eutab:

        # Subsetting and preparing data
        eu_data = pd.merge(
            (
                data_points.copy()
                .loc[data_points["level"] == "eu"]
            ),
            (
                outline[["chapter", "section", "subsection", "n", "reportValues", "direction", "title", "subtitle"]]
            ),
            how = "left",
            left_on  = "chart",
            right_on = "n"
        )
        eu_data["title"] = eu_data["title"].str.replace(r"^Graph \d+\. ", "", regex=True)
        eu_data["value_realign"] = eu_data.apply(lambda row: pd.Series(realign_data(
                    row["value2plot"], 
                    row["direction"], 
                )), axis = 1)
        eu_data = (
            eu_data
            .sort_values(by = "value_realign", ascending = False)
            .reset_index(drop = True)
        )
        subsection_summary = (
            eu_data.copy()
            .groupby("subsection")
            .agg(average_value = ("value_realign", "mean"))
            .sort_values(by = "average_value", ascending = False)
            .reset_index()
        )

        # Drawing Bar Charts
        color_codes   = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
        value_breaks  = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        color_palette = [[color, value] for color, value in zip(value_breaks, color_codes)]
        def genBars(data):
            fig = px.bar(
                data, 
                x = "value_realign", 
                y = "title",
                color = "value_realign", 
                orientation  = "h",
                range_color  = [0,100],
                custom_data  = ["title", "value_realign", "direction"],
                color_continuous_scale = color_palette,
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
        
        def genMetrics(n, d = ""):
            subsection = subsection_summary.iloc[n]["subsection"]
            avg_value  = round(subsection_summary.iloc[n]["average_value"], 1)
            card = st.metric(f":{d}[{subsection}]", f"Avg: {avg_value}")
            return card
        
        st.markdown(
            f"""
            <p class='jtext'>
                In general terms, the data collected in the European Union indicates that the region is 
                performing quite well in the following three sub-topics:
            </p>
            """, 
            unsafe_allow_html=True
        )
        col = st.columns(3)
        for metric in [0, 1, 2]:
            with col[metric]:
                genMetrics(metric, d = "green")
        st.markdown(
            f"""
            <p class='jtext'>
                On the other hand, the data also indicates that the region is performing quite low in 
                the following three sub-topics: 
            </p>
            """, 
            unsafe_allow_html=True
        )
        col = st.columns(3)
        for metric in [-1, -2, -3]:
            with col[abs(metric)-1]:
                genMetrics(metric, d = "red")
        st.markdown(
            f"""
            <p class='jtext'>
                To arrive to the values shown above, the following steps were taken:
                <ol>
                    <li>
                        The responses for individual respondents were aggregated using simple averages to
                        get a sub-national average for individual indicators.
                    </li>
                    <li>
                        Sub-national values were aggregated to get a national average. The total population of
                        each region was used as a weight during this step.
                    </li>
                    <li>
                        National values were aggregated to get a regional (EU) average using a simple mean.
                    </li>
                    <li>
                        Regional (EU) values were grouped into thematic groups and the average percentages
                        within each groups are the ones shown above.
                    </li>
                </ol>
            </p>
            <p class='jtext'>
                Additionally, the indicators were re-aligned so higher values have a positive impact in the 
                Rule of Law, while lower values reflect negative impacts on the Rule of Law.
            </p>
            <p class='jtext'>
                You can take a look at the complete list of topics and their respective average percentages
                in the table below:
            </p>
            """, 
            unsafe_allow_html=True
        )
        with st.expander("Click here to see table of results"):
            st.dataframe(subsection_summary.to_records(index=False))
        st.markdown(
            f"""
            <p class='jtext'>
                We also present a list of the top/bottom 15 indicators for the region, regardless of 
                their thematic grouping:
            </p>
            <br>
            """, 
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <h4 style='text-align: left;'>Top 15 Indicators in the Region</h4>
            <h6 style='text-align: left;'><i>Percentages</i></h6>
            """, 
            unsafe_allow_html=True
        )
        top_15 = genBars(eu_data.head(15).sort_values(by = "value_realign", ascending = True))
        st.plotly_chart(top_15, config = {"displayModeBar": False})
        st.markdown("---")
        st.markdown(
            f"""
            <h6 style='text-align: left;'><i>Important Notes:</i></h6>
            <p class='footnote'>
                <i>
                    Values were re-aligned so higher values have a positive impact in the Rule of Law,
                    while lower values have a negative impact on the Rule of Law. Indicators corresponding 
                    to the European Union were calculated as simple averages of the country indicators. 
                    Country indicators were estimated as weighted averages of the subnational regions.
                    For more information on what do the percentages represent for each indicator, please 
                    consult the report outline or the <b>Indicator Level</b> tab in this dashboard.
                </i>
            </p>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown(
            f"""
            <h4 style='text-align: left;'>Bottom 15 Indicators in the Region</h4>
            <h6 style='text-align: left;'><i>Percentages</i></h6>
            """, 
            unsafe_allow_html=True
        )
        bot_15 = genBars(eu_data.tail(15).sort_values(by = "value_realign", ascending = True))
        st.plotly_chart(bot_15, config = {"displayModeBar": False})
        st.markdown("---")
        st.markdown(
            f"""
            <h6 style='text-align: left;'><i>Important Notes:</i></h6>
            <p class='footnote'>
                <i>
                    Values were re-aligned so higher values have a positive impact in the Rule of Law,
                    while lower values have a negative impact on the Rule of Law. Indicators corresponding 
                    to the European Union were calculated as simple averages of the country indicators. 
                    Country indicators were estimated as weighted averages of the subnational regions.
                    For more information on what do the percentages represent for each indicator, please 
                    consult the report outline or the <b>Indicator Level</b> tab in this dashboard.
                </i>
            </p>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.dataframe(
            eu_data[["country_name_ltn", "subsection", "title", "value2plot", "direction", "value_realign", "reportValues"]]
            .sort_values("value_realign")
            .to_records(index=False)
        )
    with countrytab:
        st.markdown("COMING SOON. Bridgerton - Season 3 - is delaying the code for this tab")

    with vartab:

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
        country_focused = st.toggle(
            "Would you like to focus on a single country?",
            value = True
        )
        if country_focused == True:
            country_select = st.multiselect(
                "(Optional) Please select a country from the list below:",
                (data_points
                .drop_duplicates(subset = "country_name_ltn")
                .country_name_ltn.to_list())
            )

        st.markdown("<br>", unsafe_allow_html = True)

        # Subsetting and preparing data
        chart_n = outline.loc[outline["title"] == chart, "n"].iloc[0]

        data4map = (
            data_points.copy()
            .loc[(data_points["chart"] == chart_n) & (data_points["level"] == "regional")]
        )

        country_avgs = (
            data_points.copy()
            .loc[(data_points["chart"] == chart_n) & (data_points["level"] == "national")]
            .reset_index()
        )
        eu_avg = (
            data_points.copy()
            .loc[(data_points["chart"] == chart_n) & (data_points["level"] == "eu")]
            .reset_index()
        )

        if country_focused == True and len(country_select) > 0:
            data4map = (
                data4map.copy()
                .loc[data4map["country_name_ltn"].isin(country_select)]
                .reset_index()
            )
            country_avgs = (
                country_avgs.copy()
                .loc[country_avgs["country_name_ltn"].isin(country_select)]
                .reset_index()
            )
        data4bars =(
            pd.concat([country_avgs, eu_avg], ignore_index = True)
            .sort_values(by = "value2plot", ascending = True)
        )

        # Defining Annotations
        title    = outline.loc[outline["n"] == chart_n].title.iloc[0]
        subtitle = outline.loc[outline["n"] == chart_n].subtitle.iloc[0]
        reportV  = outline.loc[outline["n"] == chart_n].reportValues.iloc[0]

        # Defining tabs (Indicator Level)
        tab1, tab2, tab3 = st.tabs(["Sub-national Summary", "National Synopsis", "Detail"])

        direction    = outline.loc[outline["n"] == chart_n].direction.iloc[0]
        color_codes  = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
        value_breaks = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        if direction == "Negative":
            ordered_colors = color_codes[::-1]
        else:
            ordered_colors = color_codes
        color_palette = [[color, value] for color, value in zip(value_breaks, ordered_colors)]

        # Map Oberview
        with tab1:

            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title} (Regional level)</h4>
                <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                <br>
                """, 
                unsafe_allow_html=True
            )

            # Drawing map
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
                range_color  = [0,100],
                color_continuous_scale    = color_palette,
                color_continuous_midpoint = 50
            )
            fig.update_traces(
                hovertemplate="%{customdata[0]}<br>Value: %{customdata[1]:.1f}%",
                # marker = dict(
                #     opacity = 0.5
                # )
            )
            fig.update_layout(
                # margin = {"r":0,"t":0,"l":0,"b":0},
                height = 800,
                coloraxis_colorbar = dict(
                    title   = "Percentage(%)",
                    x       = 0,
                    xanchor ="left",
                    y       = 1.1,
                    yanchor = "top", 
                    orientation = "h", 
                    tickvals = [0, 20, 40, 60, 80, 100],
                    ticktext = ["0%", "20%", "40%", "60%", "80%", "100%"]
                )
            )
            st.plotly_chart(fig)
            st.markdown("---")
            st.markdown(
                f"""
                <p class='footnote'>
                    If the map looks suspiciously small, please locate the <i>mode bar</i>
                    on the top-right corner of the map and click on the <b>RESET VIEW</b>
                    button. I haven't figured out what's wrong.
                </p>
                """, 
                unsafe_allow_html=True
            )
            st.markdown("---")

        with tab2:
            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title} (Country level)</h4>
                <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                """, 
                unsafe_allow_html=True
            )

            # Drawing Bar Chart
            bars = px.bar(
                data4bars, 
                x = "value2plot", 
                y = "country_name_ltn",
                color = "value2plot", 
                orientation  = "h",
                range_color  = [0,100],
                custom_data  = ["country_name_ltn", "value2plot"],
                color_continuous_scale = color_palette,
                color_continuous_midpoint = 50
            )
            bars.update_traces(
                hovertemplate="%{customdata[0]}<br>Value: %{customdata[1]:.1f}%"
            )
            bars.update_layout(
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
                ),
                coloraxis_colorbar = dict(
                    title   = "Percentage(%)",
                    # x       = 0,
                    # xanchor = "left",
                    y       = 1.2,
                    yanchor = "top", 
                    orientation = "h",
                    tickvals = [0, 20, 40, 60, 80, 100],
                    ticktext = ["0%", "20%", "40%", "60%", "80%", "100%"]
                )
            )
            st.plotly_chart(bars, config = {"displayModeBar": False})

        with tab3:
            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title} (Regional level)</h4>
                <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                <br>
                """, 
                unsafe_allow_html=True
            )
            sorting = st.selectbox(
                "Sort table values based on:",
                ["Country/Region", "Percentage (Descending)", "Percentage (Ascending)"]
            )
            if sorting == "Country/Region":
                svar = ["country_name_ltn", "nuts_id"]
                asc  = True
            if sorting == "Percentage (Descending)":
                svar = ["value2plot"]
                asc  = False
            if sorting == "Percentage (Ascending)":
                svar = ["value2plot"]
                asc  = True
            data4table = (
                data4map
                .loc[:,["country_name_ltn", "nameSHORT", "nuts_id", "value2plot"]]
                .sort_values(svar, ascending = asc)
                .reset_index(drop = True)
            )
            data4table.index += 1
            st.markdown(
                """
                <style>
                .stDataFrame {
                    width: 100%;
                }
                </style>
                """,
                unsafe_allow_html = True
            )
            st.dataframe(
                data4table,
                column_config={
                    "value2plot": st.column_config.ProgressColumn(
                        "Percentage (%)",
                        format    = "%1.1f",
                        min_value = 0,
                        max_value = 100,
                    ),
                },
            )
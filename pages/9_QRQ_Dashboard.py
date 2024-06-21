"""
Project:            EU Copilot App
Module Name:        QRQ Dashboard
Author:             Isabella Coddington
Date:               June 13, 2024
Description:        This module contains the code of the QRQ Dashboard tab for the EU Copilot App
This version:       June 21st, 2024
"""

# importing libraries
import re
import pandas as pd
import numpy as np
import geopandas as gpd
import streamlit as st
import plotly.express as px
from tools import viz_tools as viz
from tools import passcheck, sidemenu

# page configuration
st.set_page_config(
    page_title= "QRQ Dashboard",
    page_icon = "📶",

)

# reading css styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>",
                unsafe_allow_html=True)
    
# sidebar menu
sidemenu.insert_smenu()

if passcheck.check_password():
    # read data
    @st.cache_data
    def load_data():
        df = pd.read_csv("https://github.com/WJP-DAU/eu-thematic-reports/raw/main/data-viz/data_points.csv")
        df['n'] = df['chart']
        return df
    
    
    @st.cache_data
    def load_rlabels():
        df = pd.read_excel("https://github.com/WJP-DAU/eu-thematic-reports/raw/main/data-viz/inputs/region_labels.xlsx")
        return df
    
    # loading outline
    @st.cache_data
    def load_outline():
        df = pd.read_excel("https://github.com/WJP-DAU/eu-thematic-reports/raw/main/data-viz/inputs/report_outline.xlsx")
        print("columns: ")
        print(df.info())
        return df
    
    # load mlayer for map
    @st.cache_data
    def load_mlayer():
        df = gpd.read_file("https://raw.githubusercontent.com/ctoruno/ROLI-Map-App/main/Data/EU_base_map.geojson").to_crs(epsg=4326)
        return df
 
    
    def realign_data(value, direction):
        if direction == "positive":
            return value
        if direction == "negative":
            return 1-value
        
    data_points = load_data()
    region_labels = load_rlabels()
    outline = load_outline()
    # remove access to justice from outline for now
    outline = outline.loc[outline['chapter'] != 'Access to Justice']
    eu_nuts = load_mlayer()
    # get combined data with stuff we want from outline
    combined = pd.merge(
            (
                data_points.copy()
            ),
            (
                outline[["report", "chapter", "section", "title", "reportValue", "direction", "subtitle", "n" ]]
            ),
            how = 'left',
            left_on = 'chart',
            right_on = 'n'
        )
        
    # define qrq or gpp - qrq has section = title
    combined['description'] = np.where(combined['section'] == combined['title'], 'qrq', 'gpp')
    # convert to percentage for gpp
    combined['value2plot'] = np.where(combined["description"] == 'gpp', combined['value2plot']*100, combined['value2plot'])
    # dataframe with qrq data only
    data_qrq = combined.loc[combined['description'] == 'qrq']


    st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">QRQ Dashboard</strong>! In this page you can preview and explore the QRQ
    data as it becomes available and is integrated into our clouds. Please note that the data here is just a preview and should not be considered
    final or official. 
    </p>
    <p class='jtext'>
    You have two options available:
       <ol>
          <li>
             <b>Indicator level</b>: Where you can search for specific subpillar scores and explore regional and national
                differences. You can also visualize the relationship between a given subpillar QRQ score and relevant GPP indicators
                at the regional level.
          </li> 
          <li>
            <b>Country Profile</b>: Where you can view the overall performance of a specific country across all pillars and subpillars.
            You can also check the EU rankings of QRQ scores.
          </li>
        </ol>
    </p>
    """,
    unsafe_allow_html=True
    )


    # defining tabs
    qrq_vartab, qrq_countrytab = st.tabs(["Indicator Level", "Country Profile"])

    with qrq_vartab:

    # get the report in the outline
        theme = st.selectbox(
        "Please select a report from the list below: ",
        (outline.drop_duplicates(subset = "report").report.to_list()), 
        key = 'indicator_level_theme'
        )

        # chapter
        chapter = st.selectbox(
        "Please select a chapter from the list below: ",
        (outline.loc[outline["report"] == theme]
         .drop_duplicates(subset = "chapter").chapter.to_list()), 
         key = 'indicator_level_chapter'
        )

        # get the pillar
        section = st.selectbox(
        "Please select an indicator from the list below:",
        (outline.loc[outline["chapter"] == chapter]
         .drop_duplicates(subset = "section")
         .section.to_list()),
         key = 'indicator_level_section'
        )

        country_focused = st.toggle(
        "Would you like to focus on a single country? ",
        value = True
        )

        if country_focused == True:
            country_select = st.multiselect(
            "(Optional) Select a country: ",
            (data_qrq
             .drop_duplicates(subset = 'country_name_ltn')
             .country_name_ltn.to_list())
            )



    # get the chart number
        chart_n = outline.loc[((outline['chapter'] == chapter) & (outline['title'] == section) &
                (outline['description'] == 'QRQ')), 'n'].iloc[0]
    

        mapData = (
            data_qrq.copy()
            .loc[(data_qrq["chart"] == chart_n) & (data_qrq["level"] == "regional")]
        )



        country_avgs = (
            data_qrq.copy()
            .loc[(data_qrq["chart"] == chart_n) & (data_qrq["level"] == "national")]
            .reset_index()
        )


        eu_avg = (
            data_qrq.copy()
            .loc[(data_qrq["chart"] == chart_n) & (data_qrq['level'] == "eu")]
            .reset_index()
        )


        if country_focused == True and len(country_select) > 0:
            mapData = (
                mapData.copy()
                .loc[mapData['country_name_ltn'].isin(country_select)]
                .reset_index()
            )
            country_avgs = (
                country_avgs.copy()
                .loc[country_avgs['country_name_ltn'].isin(country_select)]
                .reset_index()
            )
    
    
        data4bars = (
            pd.concat([country_avgs, eu_avg], ignore_index=True)
            .sort_values(by = 'value2plot', ascending = True)
        )


        print("Checking data4bars: ")
        print(data4bars.head())

        # Defining Annotations
        title    = outline.loc[outline["n"] == chart_n].title.iloc[0]
        subtitle = outline.loc[outline["n"] == chart_n].subtitle.iloc[0]
        reportV  = outline.loc[outline["n"] == chart_n].reportValue.iloc[0]

        # defining tabs for indicator level
        map_tab, bars_tab, table_tab, compare_tab = st.tabs(["Sub-national Summary","National Synopsis","Detail", "GPP Contextualization"])


        direction   =   outline.loc[outline["n"] == chart_n].direction.iloc[0]
        color_codes  = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
        value_breaks = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        if direction == "Negative":
            ordered_colors = color_codes[::-1]
        else:
            ordered_colors = color_codes
        color_palette = [[color, value] for color, value in zip(value_breaks, ordered_colors)]


        with map_tab:
            st.markdown(
                    f"""
                    <h4 style='text-align: left;'>{title} (Regional level)</h4>
                    <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                    <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                    <br>
                    """, 
                    unsafe_allow_html=True
            )
            map = viz.genQRQMap(data4map = mapData, eu_nuts = eu_nuts, color_palette = color_palette)
            st.plotly_chart(map, use_container_width = True)

        with bars_tab:
            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title} (Country level)</h4>
                <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                """, 
                unsafe_allow_html=True
            )
            bars = viz.genQRQBars(data = data4bars, cpal = color_palette, level = "indicator")
            st.plotly_chart(bars, use_container_width = True)

        with table_tab:
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
                    ["Country/Region", "Score (Descending)", "Score (Ascending)"]
                )
                if sorting == "Country/Region":
                    svar = ["country_name_ltn", "nuts_id"]
                    asc  = True
                if sorting == "Score (Descending)":
                    svar = ["value2plot"]
                    asc  = False
                if sorting == "Score (Ascending)":
                    svar = ["value2plot"]
                    asc  = True
                data4table = (
                    mapData
                    .loc[:,["country_name_ltn", "nameSHORT", "nuts_id", "value2plot"]]
                    .sort_values(svar, ascending = asc)
                    .reset_index(drop = True)
                )
                data4table.rename(columns={
                'country_name_ltn':'Country',
                'nameSHORT':'Region',
                'nuts_id': 'NUTS ID'
                }, inplace=True)
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
                            "QRQ Score",
                            format    = "%1.3f",
                            min_value = 0,
                            max_value = 1,
                        ),
                    }
                )   


        with compare_tab:
            st.markdown(
                """
                The purpose of this tab is to explore the relationships between QRQ subpillar scores 
                and relevant GPP indicators. Once you have selected a subpillar, you will see that indicator
                plotted against related GPP predictors (for the combined GPP/ QRQ data we currently have in our report
                workflow). Please note that the values here are <i>regional values</i>. For more context on regional breakdowns
                of QRQ scores for a specific indicator, please check the map tab on this page or the country profile tab. Also,
                click on autoscale in the top right corner to auto-adjust the x and y axes to the data!
                """,
                unsafe_allow_html=True
            )

            # subset to send to viz function
            regional = combined.loc[combined['level'] == 'regional']

        
            # filter for section
            compare_subset = regional.loc[regional['section'] == section]
            if len(compare_subset['title'].unique()) > 1:
                gpp_indicator = st.selectbox(
                    "Related GPP indicators: ",
                    (compare_subset.loc[compare_subset['description'] == 'gpp']
                    .drop_duplicates(subset = 'title')
                    .title.to_list())
                )

                compare_scatter = viz.gen_compare_scatter(compare_subset, section, gpp_indicator)
                st.plotly_chart(compare_scatter)
                st.markdown(
                f"""
                <p class='footnote'>
                Note: QRQ Score results reflect the evaluation of experts across the 27 EU Member States at the subnational level. 
                The expert scorecard ranges from 0 to 1, where 1 signifies the highest possible score and 0 signifies the lowest 
                possible score. The R-squared value represents the percentage of variation in population opinions that can be explained 
                by a linear association with expert scores. 
                </p>
                """,
                    unsafe_allow_html=True
                )
            else: 
                st.markdown("""
                        We don't currently have GPP data for the subpillar you have chosen integrated into this page of the Copilot. 
                        Feel free to explore a different subpillar, or reference the GPP Dashboard for full GPP data.
                        """,
                        unsafe_allow_html=True
                    )


    with qrq_countrytab:
        
        country = st.selectbox(
            "Please select a country from the list below: ",
            (
                data_qrq.drop_duplicates(subset = "country_name_ltn")
                .country_name_ltn.to_list()), key = 'country_profile_country'
            )

        
        theme = st.selectbox(
        "Please select a report from the list below: ",
        (outline.copy().drop_duplicates(subset = "report").report.to_list()),
        key = 'country_profile_theme'
        )

        
        chapter = st.selectbox(
        "Please select a chapter from the list below: ",
        (outline.loc[outline["report"] == theme]
        .drop_duplicates(subset = "chapter").chapter.to_list()),
        key = 'country_profile_chapter'
        )

        country_level, eu_dist = st.tabs(['Country Level Data', 'EU Distribution'])

    
        with country_level:
                st.markdown("""
                This plot shows regional QRQ scores as well as the national average 
                for the chosen country. Please note that the x axis scale is potentially 
                misleading here - utilize the zoom out option at the top right to get a better 
                idea of the deviations between regional scores.""", 
                unsafe_allow_html=True)
            
                country_qrq_df = data_qrq.loc[(data_qrq['level'] == 'national') | (data_qrq['level'] == 'regional')]

            # subset by country
                scatter = viz.QRQ_country_scatter(df = country_qrq_df, country = country, chapter = chapter)
                st.plotly_chart(scatter)


        with eu_dist:
                # generate rankings based on qrq scores
                national = data_qrq.loc[data_qrq['level'] == "national"]


                filtered_data = national.loc[(national['report'] == theme) & (
                    national['chapter'] == chapter)]

                subpillars = filtered_data['title'].unique()

                # generate rankings in filtered dataframe
                for subpillar in subpillars:
                    if filtered_data.loc[filtered_data['title'] == subpillar, 'direction'].iloc[0] == 'positive':
                        filtered_data.loc[filtered_data['title'] == subpillar, 'ranking'] = filtered_data.loc[
                            filtered_data['title'] == subpillar].groupby(
                                ['chapter', 'section','chart'])['value2plot'].rank(method = 'first', ascending = False).astype(int)    
                    else:
                        filtered_data.loc[filtered_data['title'] == subpillar, 'ranking'] = filtered_data.loc[
                            filtered_data['title'] == subpillar].groupby(
                                ['chapter', 'section','chart'])['value2plot'].rank(method = 'first', ascending = True).astype(int)  
                    
                rankings = viz.gen_qrq_rankins(filtered_data, country)
                st.plotly_chart(rankings)
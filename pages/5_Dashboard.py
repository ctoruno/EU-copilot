"""
Project:        EU Copilot App
Module Name:    Dashboard
Author:         Carlos Alberto Toruño Paniagua
Date:           April 29th, 2024
Description:    This module contains the code of the Dashboard tab for the EU Copilot App
This version:   May 24th, 2024
"""

import re
import pandas as pd
import numpy as np
import geopandas as gpd
import streamlit as st
import plotly.express as px
from tools import viz_tools as viz
from tools import passcheck, sidemenu
import dropbox
import dropbox.files
from io import BytesIO

# Page config
st.set_page_config(
    page_title = "Dashboard",
    page_icon  = "📶",
    # layout   = "wide"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Sidebar menu
sidemenu.insert_smenu()

if passcheck.check_password():
    #Defining auth secrets (when app is already deployed)
    dbtoken  = st.secrets["dbtoken"]
    dbkey    = st.secrets["app_key"]
    dbsecret = st.secrets["app_secret"]

    atoken = passcheck.retrieve_DBtoken(dbkey, dbsecret, dbtoken)

    # Accessing Dropbox
    dbx = dropbox.Dropbox(atoken)

    # Defining a loading function
    @st.cache_data
    def load_DBfile(file, format):

        # Accessing Dropbox files
        _, res = dbx.files_download(f"/{file}")
        data = res.content

        # Reading data frames
        with BytesIO(data) as file:
            if format == 'excel':
                df = pd.read_excel(file)
            if format == 'csv':
                df = pd.read_csv(file)

        return df

    @st.cache_data
    def load_rlabels():
        df = pd.read_excel("https://github.com/WJP-DAU/eu-gpp-report/raw/main/data-viz/inputs/region_labels.xlsx")
        return df

    @st.cache_data
    def load_mlayer():
        df = gpd.read_file("inputs/EU_base_map.geojson").to_crs(epsg=4326)
        return df
    # def load_mlayer():
    #     df = gpd.read_file("https://raw.githubusercontent.com/ctoruno/ROLI-Map-App/main/Data/EU_base_map.geojson").to_crs(epsg=4326)
    #     return df

    def realign_data(value, direction):
        if direction == "positive":
            return value
        if direction == "negative":
            return 100-value
        else:
            return value
        
    data_points   = load_DBfile("data4web_gpp.csv", format = 'csv')
    # data_points   = pd.read_csv("inputs/data4web_gpp.csv")
    region_labels = load_rlabels()
    outline       = load_DBfile("report_outline.xlsx", format = 'excel')
    eu_nuts       = load_mlayer()
    data_points.rename(columns = {
        'chapter': 'report',
        'section': 'chapter',
        'subsection': 'section',
        'value': 'value2plot'
    }, inplace = True)
    
    # Retrieving Data Points + Disaggregations
    data_points = pd.merge(data_points, outline[['title','direction', 'reportValue']], on = 'title', how = 'left')
    data_points_disag = data_points.copy()
    full_gpp = data_points.copy()
    full_gpp = full_gpp.drop_duplicates()
    data_points['value2plot'] = data_points['value2plot'] * 100
    data_points = data_points.drop_duplicates()
    data_points = data_points[data_points['demographic'] == "Total Sample"]
    data_points_disag['value2plot'] = data_points_disag['value2plot'] * 100
    data_points_disag = data_points_disag.drop_duplicates()

    eu_data = (
        data_points.copy()
        .loc[(data_points['level'] == "eu")]
        .reset_index()
    )

    eu_data["value_realign"] = (
        eu_data.apply(lambda row: pd.Series(realign_data(
                row["value2plot"], 
                row["direction"], 
            )), axis = 1)
    )

    eu_data = (
        eu_data
        .sort_values(by = "value_realign", ascending = False)
        .reset_index(drop = True)
    )

    country_data = (
        data_points.copy()
        .loc[(data_points["level"] == "national")]
        .reset_index()
    )

    country_data["value_realign"] = country_data.apply(lambda row: pd.Series(realign_data(
                    row["value2plot"], 
                    row["direction"], 
                )), axis = 1)

    # Header and explanation
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
    countrytab, vartab = st.tabs(["Country Profile", "Indicator Level"])

    with countrytab:

        st.markdown(
            f"""
            <h3 style='text-align: left;'> How are individual member states performing across WJP indicators? </h3>
            <p class='jtext'>
                This tab is meant to provide additional insight into the performance of individual countries, either relative to 
                EU averages or to other member states. Each plot here represents a  WJP subsection, and
                each line on the y-axis represents an individual indicator. For context on what reported values represent, hover
                over an individual data point. 
            """, 
            unsafe_allow_html=True
        )
        
        rankings_or_score = st.selectbox(
            "Would you like to focus on member-state rankings or the deviation from EU averages?",
            ["Rankings", "Averages"],
            index = 1
            )

        country = st.selectbox(
            "Please select a country from the list below:",
            (data_points
            .drop_duplicates(subset = "country")
            .country.to_list())
        )
        
        theme = st.selectbox(
            "Please select a report from the list below: ",
            (data_points.drop_duplicates(subset = "report").report.to_list()), 
            index = 0,
            key = 'country_profile_theme_gpp'
        )
        
        chapter = st.selectbox(
            "Please select a chapter from the list below: ",
            (data_points.loc[data_points["report"] == theme]
            .drop_duplicates(subset = "chapter").chapter.to_list()), 
            index = 0,
            key = 'country_profile_chapter_gpp'
        )
        
        if rankings_or_score == "Averages":
            eu_and_country = pd.concat([eu_data, country_data])
            subset_df = eu_and_country.loc[((eu_and_country['country'] == country) | (eu_and_country['country'] == 'European Union'))
                                          & (eu_and_country['chapter'] == chapter) & (eu_and_country['report'] == theme)]

            legend_entries = [
                {"color": "red", "label": country},
                {"color": "blue", "label": "European Union"}
            ]

            legend_html = "<div style='text-align: center;'>"

            for entry in legend_entries:
                legend_html += f"<div style='display: inline-block; margin-right: 10px;'>"
                legend_html += f"<div style='width: 10px; height: 10px; background-color: {entry['color']}; display: inline-block; margin-right: 5px;'></div>"
                legend_html += f"<span>{entry['label']}</span></div>"

            legend_html += "</div>"

            # display legend
            st.markdown(legend_html, unsafe_allow_html=True)

            pivot_df = subset_df.pivot_table(
            index=['section','title', 'subtitle'],
            columns= 'country',
            values= 'value2plot'
            ).reset_index()
            # make a pivot to get EU and country data in seperate columns
            eu_col = 'European Union'
            country_col = [col for col in pivot_df.columns if col not in ['title', 'subtitle', eu_col]][0]

            # Renaming columns appropriately
            pivot_df.columns = ['section','title', 'subtitle', 'eu_value', 'country_value']

            # Calculate the difference
            pivot_df['difference'] = pivot_df['country_value'] - pivot_df['eu_value']
            pivot_df['country'] = country
            pivot_df = pivot_df.drop_duplicates(subset=['country', 'title'])
            
            # get unique subsections
            subsections = subset_df["section"].unique()

            # make a plot for each section
            # the df sent to viz function should have indicators for ONLY the chosen section
            for subsection in subsections:
                subsection_data = pivot_df[pivot_df['section'] == subsection]
                country_dumbbell = viz.genDumbbell(subsection_data, subsection)
                st.plotly_chart(country_dumbbell)
        
        else:
        
            # filter by report and chapter
            filtered_data = country_data.loc[(country_data['report'] == theme)
                                             & (country_data['chapter'] == chapter)]
            
            filtered_data['value_realigned'] = filtered_data.apply(lambda row: pd.Series(realign_data(
                  row["value2plot"], 
                 row["direction"], 
              )), axis = 1)
            
            
            # collection of sections to iterate through
            subsections = filtered_data['section'].unique()

            # make a plot for each subsection
            for subsection in subsections:
                # being extra careful with filtering for report, chapter, section
                subsection_data = filtered_data[(filtered_data['report'] == theme)&(filtered_data['chapter'] == chapter)
                                                &(filtered_data['section'] == subsection)]
                direction = subsection_data['direction'].iloc[0]

                # rank in ascending order if direction is negative else rank in descending order
                # ascending = True if direction != "positive" else False
                if direction == 'negative':
                    ascending = False 
                else:
                    ascending = True

                # calculate ranking
                subsection_data['ranking'] = (
                    subsection_data
                    .groupby(['section', 'title'])['value_realigned']
                    .rank(method = 'first', ascending = ascending)
                    .astype(int)
                )
        
                rankings_viz = viz.genRankingsViz(subsection_data, subsection, country)
                st.plotly_chart(rankings_viz)
            
    with vartab:

        theme = st.selectbox(
            "Please select a report from the list below: ",
            (data_points.drop_duplicates(subset = "report").report.to_list()), 
            index = 0,
            key = 'indicator_level_theme_gpp'
        )

        chapter = st.selectbox(
            "Please select a chapter from the list below: ",
            (data_points.loc[data_points["report"] == theme]
            .drop_duplicates(subset = "chapter").chapter.to_list()), 
            index = 0,
            key = 'indicator_level_chapter_gpp'
        )

        # get the pillar
        section = st.selectbox(
            "Please select a section from the list below:",
            (data_points.loc[data_points["chapter"] == chapter]
            .drop_duplicates(subset = "section")
            .section.to_list()),
            key = 'section_gpp'
        )

        # get the chart
        chart = st.selectbox(
            "Please select an indicator from the list below: ",
            sorted((data_points.loc[data_points["section"] == section]
             .drop_duplicates(subset = "title")
             .title.to_list())),
             key = 'chart_vartab'
        )

        country_focused = st.toggle(
            "Would you like to focus on a single country? ",
            value = True
        )

        if country_focused == True:
            country_select = st.multiselect(
                "(Optional) Please select a country from the list below:",
                (data_points
                .drop_duplicates(subset = "country")
                .country.to_list())
            )

        st.markdown("<br>", unsafe_allow_html = True)

        dem_differences = st.checkbox("Would you like to view regional demographic differences in the reported value for this indicator?", value = False)
        if dem_differences:
                chosen_dem = st.selectbox("Please select a demographic dimension: ", ['Income', 'Gender'], key = 'chosen_dem')
                data_points_disag = data_points_disag[data_points_disag['demographic']!= 'Total Sample']


        # Subsetting and preparing data
        chart_n = (data_points.copy()
                   .loc[((data_points['report'] == theme) &
                (data_points['chapter'] == chapter) &
                (data_points['section'] == section) & (data_points["title"] == chart)), 'title'].iloc[0])

        data4map = (
            data_points.copy()
            .loc[
                (data_points['report'] == theme) &
                (data_points['chapter'] == chapter) &
                (data_points['section'] == section) & 
                (data_points["title"] == chart_n) & (data_points["level"] == "regional")]
        )


        country_avgs = (
            data_points.copy()
            .loc[
                (data_points['report'] == theme) &
                (data_points['chapter'] == chapter) &
                (data_points['section'] == section) & (data_points["title"] == chart_n) & 
                (data_points["level"] == "national")]
            .reset_index()
        )

        eu_avg = (
            data_points.copy()
            .loc[
                (data_points['report'] == theme) &
                (data_points['chapter'] == chapter) &
                (data_points['section'] == section) & (data_points["title"] == chart_n) & 
                (data_points["level"] == "eu")]
            .reset_index()
        )

        if country_focused == True and len(country_select) > 0:
            data4map = (
                data4map.copy()
                .loc[data4map["country"].isin(country_select)]
                .reset_index()
            )
            country_avgs = (
                country_avgs.copy()
                .loc[country_avgs["country"].isin(country_select)]
                .reset_index()
            )
        data4bars =(
            pd.concat([country_avgs, eu_avg], ignore_index = True)
            .sort_values(by = "value2plot", ascending = True)
        )

        data4bars = data4bars.drop_duplicates()

        # Defining Annotations
        title    = data_points.loc[data_points["title"] == chart_n].title.iloc[0]
        subtitle = data_points.loc[data_points["title"] == chart_n].subtitle.iloc[0]
        reportV  = data_points.loc[data_points["title"] == chart_n].reportValue.iloc[0]

        # Defining tabs (Indicator Level)
        map_tab, bars_tab, table_tab, lab_tab = st.tabs(["Sub-national Summary", "National Synopsis", "Detail", "Cross Lab"])

        direction    = data_points.loc[data_points["title"] == chart_n].direction.iloc[0]
        color_codes  = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
        value_breaks = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        if direction == "negative":
            ordered_colors = color_codes[::-1]
        else:
            ordered_colors = color_codes
        color_palette = [[color, value] for color, value in zip(value_breaks, ordered_colors)]

        with map_tab:
            # set dem differences to false for now
            if dem_differences:
                st.markdown(
                    """The values in the map below indicate the absolute difference in the average reported values among demographic groups for the chosen indicator
                    at the regional level. For income, the absolute difference is between the 1st and 5th income quintiles. """
                )

                demographic_data  = (
                    data_points_disag.copy()
                    .loc[ (data_points_disag['report'] == theme) & 
                         (data_points_disag['chapter'] == chapter) & 
                         (data_points_disag['level'] == 'regional') &
                        (data_points_disag['section'] == section) & 
                        (data_points_disag['title'] == chart) ]
                )

                if country_focused == True and len(country_select) > 0:
                    demographic_data = (
                        demographic_data.copy()
                        .loc[demographic_data['country'].isin(country_select)]
                    )

                # specify color palette
                color_codes   = ["#E03849", "#FF7900", "#FFC818"]
                value_breaks  = [0.00, .25, .5]
                color_palette_dem = [[color, value] for color, value in zip(value_breaks, color_codes)]
                
                # filter down to chosen_dem
                if chosen_dem == 'Income':
                    demographic_data = demographic_data.loc[(demographic_data['demographic'].isin(['Income Quintile 1', 'Income Quintile 5'])) & (demographic_data['level'] == 'regional')]
                    demographic_data  = demographic_data.pivot(
                    index   = ["country", "nuts_id", "nuts_ltn", "title", "subtitle"],
                    columns = "demographic",
                    values  = "value2plot"
                    ).reset_index()
                    demographic_data['difference'] = abs(demographic_data['Income Quintile 5'] - demographic_data['Income Quintile 1'])
                    print("demographic pivot: ")
                    print(demographic_data)
                    quintile_map = viz.gen_dem_Map(data4map = demographic_data, eu_nuts=eu_nuts, color_palette=color_palette_dem, demographic_vars=['Income Quintile 1', 'Income Quintile 5'])
                    st.plotly_chart(quintile_map, use_container_width=True)

                    

                else:
                    demographic_data = demographic_data.loc[demographic_data['demographic'].isin(['Male', 'Female'])]
                    demographic_data  = demographic_data.pivot(
                    index   = ["country", "nuts_id", "nuts_ltn", "title", "subtitle"],
                    columns = "demographic",
                    values  = "value2plot"
                    ).reset_index()
                    demographic_data['difference'] = abs(demographic_data['Male'] - demographic_data['Female'])
                    print("Demographic pivot for gender: ")
                    print(demographic_data)
                    gender_map = viz.gen_dem_Map(data4map=demographic_data, eu_nuts=eu_nuts, color_palette=color_palette_dem, demographic_vars = ['Male', 'Female'])
                    st.plotly_chart(gender_map, use_container_width=True)
            

            else:
                st.markdown(
                    f"""
                    <h4 style='text-align: left;'>{title} (Regional level)</h4>
                    <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                    <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                    <br>
                    """, 
                    unsafe_allow_html=True
                   )
                map = viz.genMap(data4map = data4map, eu_nuts  = eu_nuts, color_palette = color_palette)
                st.plotly_chart(map, use_container_width = True)

            st.markdown("---")
            st.markdown(
                f"""
                <p class='footnote'>
                Please note: we have cut off the color legend to display a maximum of 30 percentage points in difference
                in reported values between the demographic groups. However, there are some cases where the difference exceeds 
                30 percentage points. Please check the hover information for exact demographic differences.
                </p>
                <p class='footnote'>
                If the map looks suspiciously small, please locate the <i>mode bar</i>
                on the top-right corner of the map and click on the <b>RESET VIEW</b>
                button. I haven't figured out what's wrong.
                </p>
                <p class='footnote'>
                If a region is not shown on the map, it is because there were not enough observations to form a representative sample.
                </p>
                """, 
                unsafe_allow_html=True
            )
            st.markdown("---")

        with bars_tab:

            if dem_differences:
                if chosen_dem == 'Income':
                    demographics = 'Disaggregated by Income'
                if chosen_dem == "Gender":
                    demographics = 'Disaggregated by Gender'
                demographic_data = data_points_disag.loc[(data_points_disag['level'] == 'national')
                                                        &(data_points_disag['report'] == theme) & (data_points_disag['chapter'] == chapter) & 
                                                        (data_points_disag['section'] == section) & (data_points_disag['title'] == chart) ]
                
                if country_focused == True and len(country_select) > 0:
                    demographic_data = (
                        demographic_data.copy()
                        .loc[demographic_data['country'].isin(country_select)]
                    )


                dem_groups = {
                    'Disaggregated by Income': ['Income Quintile 1', 'Income Quintile 2', 'Income Quintile 3', 'Income Quintile 4', 'Income Quintile 5'],
                    'Disaggregated by Gender': ['Female', 'Male']
                }
                
                def make_dem_subsets(data):
                    return data.groupby(['country', 'title','subtitle', 'demographic'])['value2plot'].mean().reset_index()
                
                if demographics in dem_groups:
                    data4dots_subset = demographic_data.loc[(demographic_data['demographic'].isin(dem_groups[demographics])) & (demographic_data['demographic'] != 'Total Sample')]
                    demographic_dots = make_dem_subsets(data4dots_subset)
                    dem_chart = viz.genDem_Dots(data=demographic_dots, dem = demographics)
                    st.plotly_chart(dem_chart)
            else:
                st.markdown(
                    f"""
                    <h4 style='text-align: left;'>{title} (Country level)</h4>
                    <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                    <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                    """, 
                    unsafe_allow_html=True
                )

                data4bars = data4bars.drop_duplicates()
                bars = viz.genBars(data = data4bars, cpal = color_palette, level = "indicator")
                st.plotly_chart(bars, use_container_width = True)

                dtatab = (
                    data4bars
                    .reset_index(drop = True)
                    .loc[:,["country", "nuts_id", "value2plot"]]
                )
                dtatab.index += 1
                st.dataframe(dtatab)

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
                ["Country/Region", "Percentage (Descending)", "Percentage (Ascending)"]
            )
            if sorting == "Country/Region":
                svar = ["country", "nuts_id"]
                asc  = True
            if sorting == "Percentage (Descending)":
                svar = ["value2plot"]
                asc  = False
            if sorting == "Percentage (Ascending)":
                svar = ["value2plot"]
                asc  = True
            
            if dem_differences:
                data4table = (
                    demographic_data
                    .loc[
                        (demographic_data['demographic'].isin(dem_groups[demographics])), 
                        ["country", "nuts_ltn", "nuts_id", "value2plot", "demographic"] 
                        
                    ].sort_values(svar, ascending = asc)
                        .reset_index(drop = True)
                )
                data4table.index += 1
                
            else:
                data4table = (
                    data4map
                    .loc[:,["country", "nuts_ltn", "nuts_id", "value2plot", "demographic"]]
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

    with lab_tab:
        if dem_differences:
            st.markdown(
                "This feature is not available with demographic differences. "
            )
        else:
            title_xaxis  = re.sub("Graph \d+\. ", "", title)
            st.markdown(
                    f"""
                    <h3 style='text-align: center;'>
                        Cross Lab
                    </h3>
                    <p class='jtext'>
                        In this tab you can cross two variables into a single plot to see how correlated the variables are. The correlations are
                        visualized using scatter plots. Right now, you are working with data related to: 
                        <strong style="color:#003249">{title_xaxis}</strong>. This is your <b>target variable</b> and its values are going to be 
                        displayed in the <b>X-Axis</b> of the plot. However, you still need to select a comparison variable to display in the plot. 
                        For this, please use the menus below:
                    </p>
                    """, 
                    unsafe_allow_html=True
                )

            # Filters
            theme_lab = st.selectbox(
                "Please select a report from the list below: ",
                (data_points.drop_duplicates(subset = "report").report.to_list()), 
                index = 0,
                key = 'theme_lab'
                )
            

            chapter_lab = st.selectbox(
                "Please select a thematic chapter from the list below",
                (data_points
                .loc[data_points["report"] == theme_lab]
                .drop_duplicates(subset = "chapter")
                .chapter.to_list()),
                key = "chapter_lab"
            )
            section_lab = st.selectbox(
                "Please select a thematic section from the list below",
                (data_points
                .loc[data_points["chapter"] == chapter_lab]
                .drop_duplicates(subset = "section")
                .section.to_list()),
                key = "section_lab"
            )
            
            chart_lab = st.selectbox(
                "Please select a graph from the list below",
                (data_points
                .loc[(data_points["section"] == section_lab) & (data_points["title"] != chart_n)]
                .drop_duplicates(subset = "title")
                .title.to_list()),
                index=0,
                key = "chart_lab"
            )

            # Subsetting and preparing 
            chart_n_lab = (
                data_points
                .loc[(
                    (data_points['report'] == theme_lab) &
                    (data_points['chapter'] == chapter_lab) &
                    (data_points['section'] == section_lab) & 
                    (data_points["title"] == chart_lab)
                ), 'title'].iloc[0]
            )
            
            n4lab = [chart_n, chart_n_lab]
            data4lab = (
                data_points.copy()
                .loc[(data_points["title"].isin(n4lab)) & (data_points["level"] == "regional")]
            )

            data4lab["title"] = data4lab["title"].map({chart_n: "xaxis", chart_n_lab: "yaxis"})
            data4lab = data4lab.drop_duplicates(subset=["country", "nuts_id", "nuts_ltn", "title"])

            data4lab  = data4lab.pivot(
                    index   = ["country", "nuts_id", "nuts_ltn", "demographic"],
                    columns = "title",
                    values  = "value2plot"
                ).reset_index()
            
            # Defining Annotations
            title_lab    = data_points.loc[data_points["title"] == chart_n_lab].title.str.replace(r"Graph \d+\. ", "", regex=True).iloc[0]
            subtitle_lab = data_points.loc[data_points["title"] == chart_n_lab].subtitle.iloc[0]
            reportV_lab  = data_points.loc[data_points["title"] == chart_n_lab].reportValue.iloc[0]
            demo_lab     = data_points.loc[data_points["title"] == chart_lab].demographic.iloc[0]

            st.markdown(
                f"""
                <p class='jtext'>
                    You have successfully selected <strong style="color:#003249">{title_lab}</strong> to be 
                    your comparison variable. Data related to this indicator will be displayed in the 
                    <b>Y-Axis</b> of the plot.
                </p>
                <p class='jtext'>
                    A RED regression line will be draw in your plot. This line will be signaling the correlation level between 
                    the selected variables.
                </p>
                <ul>
                    <li>
                        If the line is either fully vertical or fully horizontal, there is no correlation between the variables. 
                    </li>
                    <li>
                        If the line shows a degree of steepness, that means your variables are correlated:
                        <ul>
                            <li>
                                A 45 degrees steepness shows a positive correlation between your variables. In other words, 
                                if your target variable increases, then your comparison variable will increase.
                            </li>
                            <li>
                                A 315 degrees steepness shows a negative correlation between your variables. In other words, 
                                if your target variable increases, then your comparison variable will decrease.
                            </li>
                        </ul>
                    </li>
                </ul>
                """, 
                unsafe_allow_html=True
            )
            
            scplot = viz.genScatter(data4lab, title_xaxis, title_lab, color_palette)
            st.plotly_chart(scplot, use_container_width = True)

            with st.expander("Click here for more information on your TARGET variable"):
                st.markdown(
                    f"""
                    <h4 style='text-align: left;'>{title_xaxis} (Regional level)</h4>
                    <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                    """, 
                    unsafe_allow_html=True
                )
            with st.expander("Click here for more information on your COMPARISON variable"):
                st.markdown(
                    f"""
                    <h4 style='text-align: left;'>{title_lab} (Regional level)</h4>
                    <h6 style='text-align: left;'><i>{subtitle_lab}</i></h6>
                    """, 
                    unsafe_allow_html=True
                ) 

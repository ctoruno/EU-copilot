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
import dropbox
import dropbox.files
from io import BytesIO

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

# if passcheck.check_password():
# Defining auth secrets (when app is already deployed)
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


# load mlayer for map
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
        return 1-value
data_points   = load_DBfile("data4web_qrq.csv", format = 'csv')
outline       = load_DBfile("report_outline.xlsx", format = 'excel')
data_points_gpp = load_DBfile("data4web_gpp.csv", format = 'csv')
data_points_gpp = (
    data_points_gpp
    .loc[data_points_gpp["demographic"] == "Total Sample"]
)
region_labels = load_rlabels()
# omit A2J for now
# outline = outline.loc[outline['chapter'] != 'Access to Justice']
eu_nuts       = load_mlayer()
data_points.rename(columns = {
    'theme': 'report',
    'pillar_name': 'chapter',
    'subpillar_name': 'title',
    'score': 'value2plot'
}, inplace = True)

data_points['section'] = data_points['title']

print("data_points.info():")
print(data_points.info())

data_points_gpp.rename(columns = {
    'chapter': 'report',
    'section': 'chapter',
    'subsection': 'section',
    'value': 'value2plot'
}, inplace = True)

#
# get the direction from the outline
data_points = pd.merge(data_points, outline[['title','subtitle', 'direction', 'reportValue']], on = 'title', how = 'left')

data_points_gpp = pd.merge(data_points_gpp, outline[['title', 'direction', 'reportValue']], on = 'title', how = 'left' )
data_points_gpp['value2plot'] = data_points_gpp['value2plot']*100


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
    theme_indicator = st.selectbox(
    "Please select a report from the list below: ",
    (data_points.copy().drop_duplicates(subset = "report").report.to_list()), 
    index = 0,
    key = 'indicator_level_theme'
    )

    # chapter
    chapter_indicator = st.selectbox(
    "Please select a chapter from the list below: ",
    (data_points.copy().loc[data_points["report"] == theme_indicator]
        .drop_duplicates(subset = "chapter").chapter.to_list()), 
        index = 0,
        key = 'indicator_level_chapter'
    )

    # get the pillar
    section_indicator = st.selectbox(
    "Please select an indicator from the list below:",
    (data_points.copy().loc[data_points["chapter"] == chapter_indicator]
        .drop_duplicates(subset = "section")
        .section.to_list()),
        index = 0,
        key = 'indicator_level_section'
    )

    country_focused = st.toggle(
    "Would you like to focus on a single country? ",
    value = True
    )

    if country_focused == True:
        country_select = st.multiselect(
        "(Optional) Select a country: ",
        (data_points.copy()
            .drop_duplicates(subset = 'country')
            .country.to_list())
        )



# get the chart number
    # data_points = data_points.copy().loc[(data_points['report'] == theme_indicator) & (data_points['chapter'] == chapter_indicator)]
    # chart_n = data_points.copy().loc[data_points['title'] == section_indicator, 'title'].iloc[0]
    filtered_data_points_indicator = data_points.loc[
    (data_points['report'] == theme_indicator) & 
    (data_points['chapter'] == chapter_indicator)
]
    chart_n = filtered_data_points_indicator.loc[
    filtered_data_points_indicator['title'] == section_indicator, 'title'
].iloc[0]

    mapData = (
        filtered_data_points_indicator.copy()
        .loc[(filtered_data_points_indicator["title"] == chart_n) & (filtered_data_points_indicator["level"] == "regional")]
    )



    country_avgs = (
        filtered_data_points_indicator.copy()
        .loc[(filtered_data_points_indicator["title"] == chart_n) & (filtered_data_points_indicator["level"] == "national")]
        .reset_index()
    )


    eu_avg = (
        filtered_data_points_indicator.copy()
        .loc[(filtered_data_points_indicator["title"] == chart_n) & (filtered_data_points_indicator['level'] == "eu")]
        .reset_index()
    )


    if country_focused == True and len(country_select) > 0:
        mapData = (
            mapData.copy()
            .loc[mapData['country'].isin(country_select)]
            .reset_index()
        )
        country_avgs = (
            country_avgs.copy()
            .loc[country_avgs['country'].isin(country_select)]
            .reset_index()
        )


    data4bars = (
        pd.concat([country_avgs, eu_avg], ignore_index=True)
        .sort_values(by = 'value2plot', ascending = True)
    )

    # Defining Annotations
    title    = data_points.copy().loc[data_points["title"] == chart_n].title.iloc[0]
    subtitle = data_points.copy().loc[data_points["title"] == chart_n].subtitle.iloc[0]
    reportV  = data_points.copy().loc[data_points["title"] == chart_n].reportValue.iloc[0]

    # defining tabs for indicator level
    map_tab, bars_tab, table_tab, compare_tab = st.tabs(["Sub-national Summary","National Synopsis","Detail", "GPP Contextualization"])


    direction   =   data_points.copy().loc[data_points["title"] == chart_n].direction.iloc[0]
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
                svar = ["country", "nuts_id"]
                asc  = True
            if sorting == "Score (Descending)":
                svar = ["value2plot"]
                asc  = False
            if sorting == "Score (Ascending)":
                svar = ["value2plot"]
                asc  = True
            data4table = (
                mapData
                .loc[:,["country", "nuts_ltn", "nuts_id", "value2plot"]]
                .sort_values(svar, ascending = asc)
                .reset_index(drop = True)
            )
            data4table.rename(columns={
            'country':'Country',
            'nuts_ltn':'Region',
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
        # label each data source
        data_points_gpp['description'] = 'gpp'
        data_points['description'] = 'qrq'

        full = pd.concat([filtered_data_points_indicator.copy(), data_points_gpp])
        # filter for regional data
        regional = full.loc[full['level'] == 'regional']
        # filter for section
        compare_subset = regional.loc[regional['section'] == section_indicator]

        if len(compare_subset['title'].unique()) > 1:       
        # Creating dropdown options
            options = []
            title_mapping = {}  

            filtered_subset = compare_subset.drop_duplicates(subset='title')
            for _, row in filtered_subset.iterrows():
                    if pd.notna(row['value2plot']) & (row['title']!= section_indicator):
                        options.append(row['title'])
                        title_mapping[row['title']] = (row['title'], 'value2plot')
            #     if pd.notna(row['value2plot_id1']):
            #         trust_title = f"{row['title']} (Trust)"
            #         options.append(trust_title)
            #         title_mapping[trust_title] = (row['title'], 'value2plot_id1')
            #     if pd.notna(row['value2plot_id2']):
            #         corruption_title = f"{row['title']} (Corruption Perceptions)"
            #         options.append(corruption_title)
            #         title_mapping[corruption_title] = (row['title'], 'value2plot_id2')

            # selectbox for gpp
            gpp_indicator = st.selectbox("Related GPP indicators: ", options)
            original_title, value2plot_column = title_mapping[gpp_indicator]

            # modify compare subset to send to plotting function
            # new_rows = []
            # for _, row in compare_subset.iterrows():
            #     if row['title'] == original_title:
            #         new_row = row.copy()
            #         if value2plot_column == 'value2plot_id1':
            #             new_row['title'] = f"{row['title']} (Trust)"
            #             new_row['value2plot'] = row['value2plot_id1'] * 100
            #         elif value2plot_column == 'value2plot_id2':
            #             new_row['title'] = f"{row['title']} (Corruption Perceptions)"
            #             new_row['value2plot'] = row['value2plot_id2'] * 100
            #         new_rows.append(new_row)
            #     else:
            #         new_rows.append(row)

            #     compare_subset = pd.DataFrame(new_rows)
            
            # handle the case where we have missing data in value2plot for qrq
            initial_count = compare_subset.shape[0]
            # grab missing data info so I can print it later
            missing = compare_subset.loc[(compare_subset['description'] == 'qrq') & (compare_subset['value2plot'].isna())]
            compare_subset = compare_subset[~((compare_subset['description'] == 'qrq') & (compare_subset['value2plot'].isna()))]
            omitted_count = initial_count - compare_subset.shape[0]

            # store missing country name and region name
            missing_countries = missing['country'].tolist()
            missing_nuts = missing['nuts_id'].tolist()

            if omitted_count > 0 :
                st.markdown(
                    f"""Please note that this QRQ indicator has one or more missing values for country: {missing_countries} and 
                    region {missing_nuts}. {omitted_count} observations were omitted to employ linear regression in this visualization.
                        """,
                    unsafe_allow_html=True
                )

            compare_scatter = viz.gen_compare_scatter(compare_subset, section_indicator, gpp_indicator)
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
                    <hr>
                    <p><strong>No available data</strong>: <em>We don't currently have GPP data for the subpillar you have chosen integrated into this page of the Copilot. 
                    Feel free to explore a different subpillar, or reference the GPP Dashboard for full GPP data.</em></p>
                    <hr>
                    """,
                    unsafe_allow_html=True
                )


with qrq_countrytab:
    
    country = st.selectbox(
        "Please select a country from the list below: ",
        (
            data_points.copy().drop_duplicates(subset = "country")
            .country.to_list()), key = 'country_profile_country'
        )

    
    theme = st.selectbox(
    "Please select a report from the list below: ",
    (data_points.copy().drop_duplicates(subset = "report").report.to_list()),
    key = 'country_profile_theme'
    )

    
    chapter = st.selectbox(
    "Please select a chapter from the list below: ",
    (data_points.copy().loc[(data_points["report"] == theme) 
                        # & (data_points['chapter'] != 'Chapter III. Safety')
                        ]
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
        
            country_qrq_df = data_points.copy().loc[(data_points['level'] == 'national') | (data_points['level'] == 'regional')]

        # subset by country
            scatter = viz.QRQ_country_scatter(df = country_qrq_df, country = country, chapter = chapter)
            st.plotly_chart(scatter)


    with eu_dist:
            # generate rankings based on qrq scores
            national = data_points.copy().loc[data_points['level'] == "national"]


            filtered_data = national.copy().loc[(national['report'] == theme) & (
                national['chapter'] == chapter)]

            subpillars = filtered_data['title'].unique()

            # generate rankings in filtered dataframe
            # for subpillar in subpillars:
            #     if filtered_data.copy().loc[(filtered_data['report'] == theme) & (filtered_data['chapter'] == chapter )& (filtered_data['title'] == subpillar), 'direction'].iloc[0] == 'positive':
            #         filtered_data.loc[filtered_data['title'] == subpillar, 'ranking'] = filtered_data.loc[
            #             filtered_data[(filtered_data['report'] == theme) & (filtered_data['chapter'] == chapter )&  (filtered_data['title'] == subpillar)].groupby(
            #                 ['chapter', 'section','title'])['value2plot'].rank(method = 'first', ascending = False, na_option='bottom').astype(int)    
            #     else:
            #         filtered_data.loc[(filtered_data['report'] == theme) & (filtered_data['chapter'] == chapter )&  (filtered_data['title'] == subpillar), 'ranking'] = filtered_data.loc[
            #             filtered_data[(filtered_data['report'] == theme) & (filtered_data['chapter'] == chapter )&  (filtered_data['title'] == subpillar)].groupby(
            #                 ['chapter', 'section','title'])['value2plot'].rank(method = 'first', ascending = True, na_option='bottom').astype(int)  

            for subpillar in subpillars:
                filtered_data = filtered_data.drop_duplicates(subset = ['country', 'indicator'])
                condition = (filtered_data['report'] == theme) & (filtered_data['chapter'] == chapter) & (filtered_data['title'] == subpillar)
                if filtered_data.loc[condition, 'direction'].iloc[0] == 'positive':
                    filtered_data.loc[condition, 'ranking'] = filtered_data.loc[condition].groupby(
                        ['chapter', 'section', 'title'])['value2plot'].rank(method='first', ascending=False, na_option='bottom').astype(int)
                else:
                    filtered_data.loc[condition, 'ranking'] = filtered_data.loc[condition].groupby(
                        ['chapter', 'section', 'title'])['value2plot'].rank(method='first', ascending=True, na_option='bottom').astype(int)
                
            # filtered_data = filtered_data.drop_duplicates(subset = ['country', 'indicator'])
            rankings = viz.gen_qrq_rankins(filtered_data, country, theme, chapter)
            st.plotly_chart(rankings)

st.markdown("""
    <hr>
    <p><strong>Important</strong>: <em>QRQ data is still being validated, and as such we expect that 
            scores might change, especially for regions and topics where we have relatively low expert counts. 
            While we encourage the use of this dashboard as a tool to collect preliminary QRQ insights, please do 
            not assume that it is reflective of final data. Additionally, since we expect that Czechia's nuts regions will 
            merge for QRQ analysis in the near future, it has been omitted from the whole QRQ dashboard. We will add it back once 
            regions and scores are finalized.</em></p>
    <hr>""",
    unsafe_allow_html=True)
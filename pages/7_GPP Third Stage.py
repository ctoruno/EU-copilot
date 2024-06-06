"""
Project:        EU Copilot App
Module Name:    GPP Third Stage Page
Author:         Dalia Habiby
Date:           March 18th, 2024
Description:    This module contains the code of the GPP Third Stage tab for the EU Copilot App
This version:   June 4th, 2024
"""

import pandas as pd
import numpy as np
import re
import streamlit as st
import streamlit.components.v1 as stc
import altair as alt
import os
import dropbox
import dropbox.files
import requests
import json
from io import BytesIO
# from dotenv import load_dotenv
from tools import passcheck

if passcheck.check_password():

    # Page config
    st.set_page_config(
        page_title = "GPP Third Stage",
        page_icon  = "🇪🇺"
    )
    # Reading CSS styles
    with open("styles.css") as stl:
        st.markdown(f"<style>{stl.read()}</style>", 
                    unsafe_allow_html=True)

    # load_dotenv()
    # dbtoken  = os.getenv("dbtoken")
    # dbkey    = os.getenv("app_key")
    # dbsecret = os.getenv("app_secret")


    # Defining auth secrets (when app is already deployed)
    dbtoken  = st.secrets["dbtoken"]
    dbkey    = st.secrets["app_key"]
    dbsecret = st.secrets["app_secret"]

    # Retrieving access token 
    # Note: DROPBOX access token are short-lived (valid for 4 hours), that's why you need to retrieve one every time you start a new session in the app

    atoken = passcheck.retrieve_DBtoken(dbkey, dbsecret, dbtoken)

    # Accessing Dropbox
    dbx = dropbox.Dropbox(atoken)

    # Defining a loading function
    @st.cache_data
    def load_DBfile(file, sheet):

        # Accessing Dropbox files
        _, res = dbx.files_download(f"/Validation Inputs/{file}")
        data = res.content

        # Reading data frames
        with BytesIO(data) as file:
            df = pd.read_excel(file, sheet_name= sheet)

        return df

    flags = load_DBfile("GPP_flagging_system.xlsx", 0)
    rank = load_DBfile("GPP_external_ranking.xlsx", 0)
    outliers = load_DBfile("outliers.xlsx", 0)
    intr = load_DBfile("GPP_internal_ranking.xlsx", 0)

    st.markdown("<h1 style='text-align: center;'>GPP Third Stage Validation</h1>", 
                unsafe_allow_html=True)
    st.markdown(
        """
        <p class='jtext'>
        Welcome to the <strong style="color:#003249"> GPP Third Stage Validation page</strong>. In this page you can view the
        everything that goes into the final flagging choices in each country.
        </p>
        """,
        unsafe_allow_html = True
    )

    country = st.selectbox("Select a country",
                            ("Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", 
                            "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", 
                            "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"), 
                            )

    # Header and explanation


    def color_row(row):
        color = 'background-color: #B6F161' if row['Flag'] == 'Green' else 'background-color: #FC7661' if row['Flag'] == 'Red' else 'background-color: #FFD700'
        return [color] * len(row)

    tab0, tab1, tab2, tab3= st.tabs(["Overview", "External Ranking Analysis", "Internal Ranking Analysis", "EU Level"])

    with tab0:

        st.markdown(
        """
        <p class='jtext'>
        Below are all of the variables in {} and how they are flagged throughout our overall validation process, beginning with Red flags, then variables lacking comparative information, then Green flags. 
        The default view is to only show the final flag, however you may select more to visualize.""".format(country),
        unsafe_allow_html = True
    )
        st.markdown("<h4>Choose an Analysis:</h4>",
                        unsafe_allow_html = True)
        est  = st.multiselect("Select which analysis you would like to visualize:",
                                    ('Country Level', 'Expert TPS Rank',  'Population TPS Rank', 
                                        'Internal Rank'),
                                )


        cyflags = flags[flags["Country"].isin([country])].rename(columns={"Internal_ranking_flag": "Internal Rank", "HTML_flag": "Country Level", 
                                                                            "Population_ranking_flag" : "Population TPS Rank",
                                                                            "Expert_ranking_flag": "Expert TPS Rank",
                                                                            "Final_flag": "Flag",
                                                                            "GPP_Variable_Name" : "Indicator",
                                                                            "subpillar": "Sub-Pillar"})
        
        st.markdown("<h5>Overall Flags:</h5>",
                        unsafe_allow_html = True)
        
        with st.expander("Flagging System"):
            st.write("""The flagging system employed to create one final flag for each variable in each country gives more weight to the analyses we believe are more rigorous, and takes into account the qualitative trend of the data.
                    <br>
                    <br>
                    The Country Level analysis refers to the first round of analysis performed on the full fieldwork data, including a score comparison with TPS indicators and a t-test with our previous GPP.
                    The Population Ranking and the Expert Ranking both fall under the External Ranking Analysis in which we compare the position of a country's score for an indicator in the EU GPP with its position in the TPS.
                    Finally, the Internal Ranking is an analysis in which we compare the position of a country's score for an indicator in the EU GPP with its position in the previous GPP.
                    <br>
                    <br>
                    <b>Here is the general logic of our flags:</b>
                    <br>
                    If the Internal and Population rankings are both Red and have the same trends, our final flag is Red. However, if they have opposite trends, this means that our EU GPP data falls in between them and therefore the final flag is Green.
                    <br> If the Internal ranking is Red and the Population ranking is Green or vice versa, we turn to the Expert ranking and the Country Level analysis. If one of those is Green, then the final flag is Green and if they are not analyzed, then we turn to the trends; if the Internal and Population have the same trend, the final flag is Red and if not, it is Green.
                    <br> If we only have one of the Internal ranking or the Population ranking, this overrules any weaker analysis. 
                    <br> If we only have the Expert ranking and the Country Level analysis, if they are both Red then the final flag is Red but if one of them is Green, then the final flag is Green.""",
                    unsafe_allow_html=True)


        st.dataframe(cyflags[["Indicator", "Score", "Sub-Pillar"] + est + ["Flag"]].drop_duplicates().sort_values(by='Flag', ascending = False).style.format({"Sub-Pillar": "{:.1f}"}).apply(color_row, axis=1), 
                        hide_index=True,
                        use_container_width=True)
        #subset data
        c= flags[flags["Country"].isin([country])]

    with tab1:

        st.markdown(
        """
        <p class='jtext'>
        In this page, you can view the results of the External Ranking Analysis in {}. The Graphs tab will visualize one variable at a time, showing its position in the EU GPP data as well as its position in the matched TPS data.
        The Table tab will visualize the results of every variable in this analysis in one table.
        """.format(country),
        unsafe_allow_html = True
        )
        tabch, tabtb = st.tabs(["Graphs", "Table"])
        rank2 = rank[rank["country_name_ltn"].isin([country])][["question", "Rank_GPP", "Rank_TPS", "Diff_Rank", "upper_bound", "value", "tps_value", "tps_question", "Type_Survey", "Match",  "flagged_questions"]].drop_duplicates().rename(columns={"flagged_questions": "Flag",
                                        "upper_bound" : "Threshold",
                                        "question": "Question",
                                        "tps_question": "TPS Question",
                                        "tps_value": "TPS Value",
                                        "Type_Survey": "Type",
                                        "Rank_GPP": "GPP Rank",
                                        "Rank_TPS": "TPS Rank",
                                        "Diff_Rank": "Difference",
                                        "value": "GPP Value"
                                                                                })

        with tabch:
            
            vars = rank[rank["country_name_ltn"].isin([country])]["question"].drop_duplicates().to_list()
            var = st.selectbox("Select a Variable",
                (vars))

            # bar = st.bar_chart(rank[rank["question"].isin([var])].sort_values('Rank_GPP', ascending=True),
            #                 x = "country_name_ltn",
            #                 y = "Rank_GPP")
            
            rankdf = rank[rank["question"].isin([var])][["country_name_ltn", "question", "Rank_GPP", "Rank_TPS", "tps_question", "value", "tps_value"]].drop_duplicates().rename(columns={"country_name_ltn": "Country"})
            rankdf.groupby('Country')['Rank_GPP'].mean().reset_index().sort_values("Rank_GPP", ascending=True)
            r = rankdf[["Country", "question","Rank_GPP", "value"]].groupby('Country').agg({'Rank_GPP': 'mean', 'value': 'first'}).reset_index().sort_values("Rank_GPP", ascending=True).drop_duplicates()
            r['value']= round(r['value'],2).astype(str)
            r['Rank_GPP']= round(r['Rank_GPP'])
            #rankdf.insert(3, "Rank in GPP", range(1, len(rankdf)+1))

        
            st.dataframe(rank2[rank2["Question"].isin([var])].drop(["Question"], axis=1).style.format({"Difference": "{:.1f}", "Threshold": "{:.1f}", "TPS Rank": "{:.1f}", "GPP Value": "{:.3f}", "TPS Value": "{:.3f}",}).apply(color_row, axis=1),
                        hide_index=True)

            st.markdown("""<b>Rankings in Current EU GPP</b>""",
                        unsafe_allow_html=True)
            
            bars = alt.Chart(r).mark_bar().encode(
                    x=alt.X('Country').sort('y'),
                    y=alt.Y('Rank_GPP', title='Rank in GPP'),
                    color=alt.condition(
                        alt.datum.Country == country,  
                        alt.value('orange'),    
                        alt.value('#086cd0')  
                    )
                    
                ).properties(
                        width=680,
                    )
            
            text = bars.mark_text(
                    align='center',
                    baseline='bottom'
                ).encode(
                    text="value",
                    color = alt.condition(
                        alt.datum.value <=1,
                        alt.value('#141417'),
                        alt.value('#141417')
                    )
                )

            chart = (bars + text)
            st.write(chart)

            st.markdown("""<b>Rankings in TPS Data</b>""",
                        unsafe_allow_html=True)
            
            ## Create new dataframe to plot TPS ranks and prepare values for visualization
            
            r2=rankdf[["Country", "question","Rank_TPS", "tps_value"]].groupby('Country').agg({'Rank_TPS': 'mean', 'tps_value': 'mean'}).reset_index().sort_values("Rank_TPS", ascending=True).drop_duplicates()
            r2['tps_value']= round(r2['tps_value'],2).astype(str)
            
            ## Create Bar Chart base
            barstps = alt.Chart(r2).mark_bar().encode(
                    x=alt.X('Country').sort('y'),
                    y=alt.Y('Rank_TPS', title = "Rank in TPS"),
                    color=alt.condition(
                        alt.datum.Country == country,  
                        alt.value('orange'),    
                        alt.value('#086cd0')  
                    )
                    
                ).properties(
                        width=680,
                    )
            ## add label text to bar chart
            texttps = barstps.mark_text(
                    align='center',
                    baseline='bottom'
                ).encode(
                    text="tps_value",
                    color = alt.condition(
                        alt.datum.tps_value <=1,
                        alt.value('#141417'),
                        alt.value('#141417')
                    )
                )

            ## merge chart and text and print graph
            charttps = (barstps + texttps)
            st.write(charttps)
                
        with tabtb:

            st.markdown("""<b>External Ranking Analysis Summary:</b>""",
                        unsafe_allow_html=True)
            st.dataframe(rank2.sort_values(by='Flag', ascending = False).style.apply(color_row, axis=1).format({"Difference": "{:.1f}", "Threshold": "{:.3f}", "TPS Rank": "{:.1f}"}),
                    hide_index=True)
        
    with tab2:
        st.markdown(
        """
        <p class='jtext'>
        In this page, you can view the results of the Internal Ranking Analysis in {}. The Graphs tab will visualize one variable at a time, showing the position of {} in the EU GPP data as well as its position in the previous Global GPP data.
        The Table tab will visualize the results of every variable in this analysis in one table.
        """.format(country, country),
        unsafe_allow_html = True
        )

        tabch, tabtb = st.tabs(["Graphs", "Table"])
        intr2 = intr[intr["country_name_ltn"].isin([country])][["question", "value", "prev_value", "Rank_curr", "Rank_prev", "Diff_Rank", "flagged_questions"]].drop_duplicates().rename(columns={"flagged_questions": "Flag",
                                                                                "question":"Question",
                                                                                "value": "Current Value",
                                                                                "prev_value": "Previous Value",
                                                                                "Rank_curr": "Current Rank",
                                                                                "Rank_prev": "Previous Rank",
                                                                                "Diff_Rank": "Difference"
                                                                                }) 
        with tabch:
            
            vars = intr[intr["country_name_ltn"].isin([country])]["question"].drop_duplicates().to_list()
            var = st.selectbox("Select a Variable",
                (vars))

            # bar = st.bar_chart(rank[rank["question"].isin([var])].sort_values('Rank_GPP', ascending=True),
            #                 x = "country_name_ltn",
            #                 y = "Rank_GPP")
            
            intrdf = intr[intr["question"].isin([var])][["country_name_ltn",  "question",  "Rank_curr", "Rank_prev", "value", "prev_value"]].drop_duplicates().rename(columns={"country_name_ltn": "Country"})
            intrdf.groupby('Country')['Rank_curr'].mean().reset_index().sort_values("Rank_curr", ascending=True)
            intrdf['value']= round(intrdf['value'],2).astype(str)

            st.dataframe(intr2[intr2["Question"].isin([var])].style.apply(color_row, axis=1),
                        hide_index=True)

            st.markdown("""<b>Rankings in Current EU GPP</b>""",
                        unsafe_allow_html=True)

            bars = alt.Chart(intrdf).mark_bar().encode(
                    x=alt.X('Country').sort('y'),
                    y='Rank_curr',
                    color=alt.condition(
                        alt.datum.Country == country,  
                        alt.value('orange'),    
                        alt.value('#086cd0')  
                    )
                    
                ).properties(
                        width=680,
                    )
            
            text = bars.mark_text(
                    align='center',
                    baseline='bottom'
                ).encode(
                    text="value",
                    color = alt.condition(
                        alt.datum.value <=1,
                        alt.value('#141417'),
                        alt.value('#141417')
                    )
                )

            chart = (bars + text)
            st.write(chart)


            st.markdown("""<b>Rankings in Previous GPP</b>""",
                        unsafe_allow_html=True)
            
            r2= intrdf.sort_values("Rank_prev", ascending=True)
            r2['prev_value']= round(r2['prev_value'],2).astype(str)
            
            bars = alt.Chart(r2).mark_bar().encode(
                    x=alt.X('Country').sort('y'),
                    y='Rank_prev',
                    color=alt.condition(
                        alt.datum.Country == country,  
                        alt.value('orange'),    
                        alt.value('#086cd0')  
                    )
                    
                ).properties(
                        width=680,
                    )
            
            text = bars.mark_text(
                    align='center',
                    baseline='bottom'
                ).encode(
                    text="prev_value",
                    color = alt.condition(
                        alt.datum.prev_value <=1,
                        alt.value('#141417'),
                        alt.value('#141417')
                    )
                )

            chart = (bars + text)
            st.write(chart)

                
        with tabtb:
            st.markdown("""<b>Internal Ranking Analysis Summary:</b>""",
                        unsafe_allow_html=True)
            st.dataframe(intr2.sort_values(by='Flag', ascending = False).style.apply(color_row, axis=1),
                    hide_index=True)

    with tab3:

        st.markdown("""<b>All Final Red Flags:</b>""",
                        unsafe_allow_html=True)
        st.markdown(
        """
        <p class='jtext'>
        This table indicates all of the variables in each country that have been flagged red after every stage of validation. This does not mean that they will necessarily be removed, instead that they require further qualitative context for decision making.
        """,
        unsafe_allow_html = True
        )
        st.dataframe(flags[flags['Final_flag'].str.contains("Red")].rename(columns={"Internal_ranking_flag": "Internal Rank", "HTML_flag": "Country Level", 
                                                                            "Population_ranking_flag" : "Population TPS",
                                                                            "Expert_ranking_flag": "Expert TPS",
                                                                            "Final_flag": "Flag",
                                                                            "GPP_Variable_Name" : "Indicator",
                                                                            "subpillar": "Sub-Pillar"})[["Country", "Indicator", "Country Level", "Expert TPS", "Population TPS", "Internal Rank",  "Flag"]].drop_duplicates().style.apply(color_row, axis=1),
                                                                            hide_index=True, 
                                                                            use_container_width=True)
        # st.dataframe(outliers[outliers["Country"].isin([country])].style.apply(color_row, axis=1),
        #              hide_index=True,
        #              use_container_width=True)






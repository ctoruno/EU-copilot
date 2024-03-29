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
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc

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
    
# Header and explanation
st.markdown("<h1 style='text-align: center;'>Media Reports</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Media Reports tab</strong>. In this page you can search and
    visualize the results a massive webscrapping exercise of newspapers for each of the 27 active members of
    the European Union. To visualize the results, you need to first select a country in order to load the data.
    Once the data is loaded, you will have to search for specific keywords and/or pillars of interest. The
    search tool will list all of the articles that matched your search.
    </p>
    """,
    unsafe_allow_html = True
)

# Country selection
country_selec = st.form("country_selection")
with country_selec:
    country = st.selectbox(
        "Select a country from the list below:",
        [
            # "Austria",
            # "Belgium",
            "Bulgaria",
            # "Croatia",
            # "Cyprus",
            # "Czech Republic",
            # "Denmark",
            # "Estonia",
            # "Finland",
            # "France",
            # "Germany",
            # "Greece",
            "Hungary",
            # "Ireland",
            # "Italy",
            # "Latvia",
            # "Lithuania",
            "Luxembourg",
            # "Malta",
            # "Netherlands",
            # "Poland",
            # "Portugal",
            # "Romania",
            # "Slovakia",
            # "Slovenia",
            # "Spain",
            # "Sweden"
        ]
    )
    submitted = st.form_submit_button("Load the data!!")
    if submitted:
        update_tracking("country_track")

if st.session_state["country_track"]:

    st.markdown(f"<h2>{country}</h2>", unsafe_allow_html = True)

    # Loading data for country
    country_data = pd.read_parquet(f"data/{country}_master.parquet.gzip")
    with open(f"summaries/{country}_overviewSummaries.json", "r") as file:
        summary_data = json.load(file)

    # Creating tabs
    overview, search = st.tabs(["Overview", "Search Engine"])
    with overview:
        sources =  "".join([f"\n\n- <a href='https://{link}' target='_blank'>{link}</a>" for link in country_data["domain_url"].drop_duplicates().to_list()])
        country_data["published_date"] = pd.to_datetime(country_data['published_date'])
        min_date  = min(country_data["published_date"]).strftime("%B %d, %Y")
        max_date  = max(country_data["published_date"]).strftime("%B %d, %Y")
        nrows     = len(country_data.drop_duplicates(subset='id'))
        nrows_fmt = "{:,}".format(nrows)
        st.markdown(
            f"""
            <p class='jtext'>
            Data for <strong style="color:#003249">{country}</strong> was extracted from the following sources:
            {sources}
            </p>
            """,
            unsafe_allow_html = True
        )
        st.markdown(
            f"""
            <p class='jtext'>
            The data for this country spans from <b>{min_date}</b> to <b>{max_date}</b>. For a total of {nrows_fmt} articles.
            </p>

            <p class='jtext'>
            Bellow, you can find a brief summary of the main issues and events related to each one of the 8 pillars of the Rule of Law. <b>The
            summaries were produced using AI</b>, after the model was presented with the project's theoretical framework. Therefore, 
            please read them carefully.
            </p>
            """,
            unsafe_allow_html = True
        )

        counter = 1
        for tab in st.tabs(["Pillar "+str(n) for n in range(1,9)]):
            with tab:
                tab_name = f"Pillar {counter}"
                st.markdown(
                    f"""
                    <p class='jtext'>
                    Below, you will find the most important issues that the Language Model identified as worth to be highlighted 
                    regarding the news articles extracted for <strong style="color:#003249">{country}, {tab_name}</strong>.
                    The model was told to keep a maximum of 10 events/issues for every 100,0000 words. Therefore, the 
                    summaries displayed below might vary in extention <i>depending on the extent of information extracted for each country</i>.
                    </p>
                    """,
                    unsafe_allow_html = True
                )
                pillar_bullets = "- " + summary_data[tab_name].replace("-", "").replace("/n", "\n- ")
                st.write(pillar_bullets)
            counter = counter + 1

    with search:
        search_engine = st.container()
        with search_engine:
            st.markdown(
                "<h4>Search articles based on:</h4>", 
                unsafe_allow_html = True
            )
            keywords  = st.text_input("The following keywords:")
            # target_options = {
            #     "Headline"    : "title_trans",
            #     "Description" : "description_trans",
            #     "Content"     : "content_trans" 
            # }
            # target_selection = st.selectbox(
            #     "Search for these keywords in..",
            #     target_options.keys
            # )
            assoc_pillar = st.selectbox(
                "Limit the search to a specific pillar",
                ["Pillar "+str(n) for n in range(1,9)]
            )
            search_button = st.button("Search")
            # if search_button:
            #     update_tracking("search_track")

        if search_button:

            session_state = True

            # Transforming keywords
            keys = []
            keywords = re.sub(" OR ", "|", keywords)
            for key in keywords.split():
                regexkey = f"(?=.*{key})"
                keys.append(regexkey)
            keys = "^" + "".join(keys)
            
            # Filtering results
            filtered_data = country_data.copy().loc[country_data["associated_pillar"] == assoc_pillar]
            results = filtered_data[filtered_data["summary"].str.contains(keys, case = False)]

            # Success Box
            nresults = len(results.index)
            st.success(f"Your search returned {nresults} results.")

            for index, row in results.iterrows():

                with st.container():
                    title   = row["title_trans"]
                    sumdesc = row["summary"]
                    body    = row["content_trans"]
                    score   = row["impact_score"]
                    date    = row["published_date"].strftime("%B %d, %Y")
                    source  = row["domain_url"]
                    link    = row["link"]

                    variable_html_layout = f"""
                                        <div>
                                            <h4>{title}</h4>
                                            <p class='jtext'><strong>Summary:</strong></p>
                                            <p class='vdesc'>{sumdesc}</h4>
                                            <br>
                                            <div class="row">
                                                <div class="column">
                                                    <p class='jtext'><strong>Source:</strong> {source}</p>
                                                </div>
                                                <div class="column">
                                                    <p class='jtext'><strong>Publishing date:</strong> {date}</p>
                                                </div> 
                                            </div>
                                            <div class="row">
                                                <div class="column">
                                                    <p class='jtext'><strong>Impact score:</strong> {score}</p>
                                                </div>
                                                <div class="column">
                                                    <p class='jtext'><strong>URL:</strong>
                                                        <a href='{link}' target='_blank'>Click here to open in a new tab</a>
                                                    </p>
                                                </div> 
                                            </div>
                                        </div>
                                        """
                
                    st.markdown(variable_html_layout, unsafe_allow_html = True)
                    with st.expander("Full content"):
                        stc.html(body, scrolling = True)
                    
                    st.markdown("---")


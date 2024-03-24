"""
Project:        EU Copilot App
Module Name:    Datamap Page
Author:         Carlos Alberto Toruño Paniagua
Date:           October 23rd, 2023
Description:    This module contains the code of the Data Maps tab for the EU Copilot App
This version:   October 23rd, 2023
"""

import pandas as pd
import numpy as np
import re
import streamlit as st
import streamlit.components.v1 as stc

# Page config
st.set_page_config(
    page_title = "Codebooks",
    page_icon  = "🧭"
)
# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Reading Codebook & DataMap
@st.cache_data
def load_datamap():
    datamap = pd.read_excel("inputs/EU2 GPP 2023 Full Datamap.xlsx", 
                            sheet_name = "Data Map")
    return datamap

@st.cache_data
def load_codebook_gpp():
    datamap = pd.read_excel("inputs/EU2 GPP 2023 Codebook.xlsx", 
                            sheet_name = "Codebook")
    return datamap

@st.cache_data
def load_codebook_qrq():
    datamap = pd.read_excel("inputs/EU2 QRQ 2023 Codebook.xlsx", 
                            sheet_name = "Codebook")
    return datamap

datamap  = load_datamap()

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Codebook Explorer</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">Codebook Explorer tool</strong>. In this page you can search 
    questions in the data codebook based on keywords and/or thematic group. It is not necessary to fill the 
    filters in order to get results. However, they will narrow your search.
    </p>
    """,
    unsafe_allow_html = True
)

# Writing helpers
keywords_hlp = """
The app will search questions (either by their name or their description) based in the keywords defined in this 
text box.
"""

chkbox_hlp = """
By default, the app will search for questions whose description contains the provided keywords. However, if you 
would like your search to be based on variable names instead of variable descriptions, then make sure to untick 
this box.
"""

# Choosing codebook
st.markdown("<h4>Choose a Codebook:</h4>",
            unsafe_allow_html = True)
cb  = st.selectbox(
    "Select which codebook you would like to search:",
    ('GPP', 'QRQ')                        
)

# Search Box Inputs
if 'GPP' in cb:
    codebook = load_codebook_gpp() 
    st.markdown("<h4>Search questions based on:</h4>",
            unsafe_allow_html = True)
    keywords = st.text_input("The following keywords:",
                            help = keywords_hlp)
    target   = st.checkbox("Search variables by description",
                        help  = chkbox_hlp,
                        value = True)
    modules_list = sorted(codebook["Survey Module"].astype(str).unique())
    modules  = st.multiselect("Select a thematic module from the following list:",
                            modules_list,
                            default = None)
    topics_list = (codebook[codebook["Survey Module"]
                        .isin(modules)]["Topic"]
                        .unique()
                        .tolist())

    topics   = st.multiselect("Select a question topic based on the selected modules:",
                            topics_list,
                            default = None)   
    submit_button = st.button(label = "Search!")

    if submit_button:

        # Transforming keywords
        keys = []
        keywords = re.sub(" OR ", "|", keywords)
        for key in keywords.split():
            regexkey = f"(?=.*{key})"
            keys.append(regexkey)
        keys = "^" + "".join(keys)

        # Filtering results
        if target == False:
            targetCol = "Variable"
        else: 
            targetCol = "Description"

        results = codebook[codebook[targetCol].str.contains(keys, case = False)]

        if modules != []:
            resultmd = codebook[codebook["Survey Module"].astype(str).isin(modules)]
            results = resultmd[resultmd[targetCol].str.contains(keys, case = False)]
        if topics != []:
            resulttp = codebook[codebook["Topic"].isin(topics)]
            results = resulttp[resulttp[targetCol].str.contains(keys, case = False)]

        # Success Box
        nresults = len(results.index)
        st.success(f"Your search returned {nresults} results.")

        for index, row in results.iterrows():

            with st.container():
                vtopic = row["Topic"]
                vname  = row["Variable"]
                vanswers = row["Values"]
                vmodule  = row["Survey Module"]
                global_name = row["Global GPP"]
                description = row["Description"]
                q2023_name  = row["2023  EU Questionnaire"]

                variable_html_layout = f"""
                                    <div>
                                        <h4>{vname}</h4>
                                        <p class='jtext'><strong>Description:</strong></p>
                                        <p class='vdesc'>{description}</h4>
                                        <br>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Survey Module:</strong> {vmodule}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>Topic:</strong> {vtopic}</p>
                                            </div> 
                                        </div>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Name in Global GPP:</strong> {global_name}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>Name in EU GPP Questionnaire:</strong> {q2023_name}</p>
                                            </div> 
                                        </div>
                                    </div>
                                    """
            
                st.markdown(variable_html_layout,
                        unsafe_allow_html = True)
            
                with st.expander("Coded Answers"):
                    stc.html(vanswers, 
                         scrolling = True)
                
                st.markdown("---")

if 'QRQ' in cb:
    codebook = load_codebook_qrq() 
    st.markdown("<h4>Search questions based on:</h4>",
            unsafe_allow_html = True)
    
    questionnaire  = st.multiselect("Select one or more questionnaires from the following list:",
                            ('CJ', 'CCA', 'CCB', 'GOV'),
                            default = None)

    keywords = st.text_input("The following keywords:",
                            help = keywords_hlp)
    target   = st.checkbox("Search variables by description",
                        help  = chkbox_hlp,
                        value = True)
    modules_list = sorted(codebook["Module"].astype(str).unique())
    if questionnaire != []:
            modsq = codebook[codebook["Questionnaire"].astype(str).isin(questionnaire)]
            modules_list = sorted(modsq["Module"].astype(str).unique())
    modules  = st.multiselect("Select a thematic module from the following list:",
                            modules_list,
                            default = None)
    #topics_list = (codebook[codebook["Module"]
                        #.isin(modules)]["Topic"]
                        #.unique()
                        #.tolist())

    #topics   = st.multiselect("Select a question topic based on the selected modules:",
     #                       topics_list,
      #                      default = None)   
    submit_button = st.button(label = "Search!")

    if submit_button:

        # Transforming keywords
        keys = []
        keywords = re.sub(" OR ", "|", keywords)
        for key in keywords.split():
            regexkey = f"(?=.*{key})"
            keys.append(regexkey)
        keys = "^" + "".join(keys)

        # Filtering results
        if target == False:
            targetCol = "Keywords"
        else: 
            targetCol = "Description"

        results = codebook[codebook[targetCol].str.contains(keys, case = False)]

        if questionnaire != []:
            resultq = codebook[codebook["Questionnaire"].astype(str).isin(questionnaire)]
            results = resultq[resultq[targetCol].str.contains(keys, case = False)]
        if modules != []:
            resultm = codebook[codebook["Module"].astype(str).isin(modules)]
            results = resultm[resultm[targetCol].str.contains(keys, case = False)]
        
        # Success Box
        nresults = len(results.index)
        st.success(f"Your search returned {nresults} results.")

        for index, row in results.iterrows():

            with st.container():
                vname  = row["Keywords"]
                vanswers = row["Values"]
                vmodule  = row["Module"]
                vquest = row["Questionnaire"]
                global_name = row["Global GPP Equivalent"]
                description = row["Description"]
                q2023_name  = row["Names"]

                variable_html_layout = f"""
                                    <div>
                                        <h4>{vname}</h4>
                                        <p class='jtext'><strong>Description:</strong></p>
                                        <p class='vdesc'>{description}</h4>
                                        <br>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Questionnaire:</strong> {vquest}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>Module:</strong> {vmodule}</p>
                                            </div> 
                                        </div>
                                        <div class="row">
                                            <div class="column">
                                                <p class='jtext'><strong>Name in Global GPP:</strong> {global_name}</p>
                                            </div>
                                            <div class="column">
                                                <p class='jtext'><strong>Name in EU QRQ Questionnaire:</strong> {q2023_name}</p>
                                            </div> 
                                        </div>
                                    </div>
                                    """
            
                st.markdown(variable_html_layout,
                        unsafe_allow_html = True)
            
                with st.expander("Coded Answers"):
                    stc.html(vanswers, 
                         scrolling = True)
                
                st.markdown("---")

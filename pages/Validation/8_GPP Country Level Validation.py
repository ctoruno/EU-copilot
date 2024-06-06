"""
Project:        EU Validator App
Module Name:    GPP Country Level Validation Page
Author:         Dalia Habiby
Date:           March 18th, 2024
Description:    This module contains the code of the GPP Country Level Validation tab for the EU Validator App
This version:   March 18th, 2024
"""

import pandas as pd
import numpy as np
import re
import streamlit as st
import streamlit.components.v1 as stc
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from inputs.paragraph import paragraph
import os
import dropbox
import dropbox.files
import requests
import json
# from dotenv import load_dotenv
from tools import passcheck

if passcheck.check_password():

    # Page config
    st.set_page_config(
        page_title = "GPP Country Validation",
        page_icon  = "🇪🇺"
    )
    # Reading CSS styles
    with open("styles.css") as stl:
        st.markdown(f"<style>{stl.read()}</style>", 
                    unsafe_allow_html=True)

    #load_dotenv()
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


    # Header and explanation
    st.markdown("<h1 style='text-align: center;'>GPP Country Level Validation</h1>", 
                unsafe_allow_html=True)
    st.markdown(
        """
        <p class='jtext'>
        Welcome to the <strong style="color:#003249"> GPP Country Level Validation page</strong>. In this page you can view the
        scores and country-level validation results of the full fieldwork analysis in the country of your choice.
        </p>
        """,
        unsafe_allow_html = True
    )

    country = st.selectbox("Select a country",
                            ("Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", 
                            "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", 
                            "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"),
                            
                            )


    flags = load_DBfile("GPP_flagging_system.xlsx", 0)
    xl = load_DBfile("report_tables.xlsx", None)

    time_output = xl[country + "_time_output"]
    time_output_sub = xl[country + "_time_output_sub"]
    tm = xl[country + "_tm"]
    tmnuts = xl[country + "_tmnuts"]
    expt = xl[country + "_expt"]
    exptnuts = xl[country + "_exptnuts"]
    expt_output = xl[country + "_exp_output"]
    expt_output_sub = xl[country + "_exp_output_sub"]
    pop = xl[country + "_pop"]
    popnuts = xl[country + "_popnuts"]
    pop_output = xl[country +"_pop_output"]
    pop_output_sub = xl[country + "_pop_output_sub"]
    tps = xl[country + "_tps"]


    st.markdown(
        """
        <p class='jtext'>
        Below are the concerning subpillars in {} identified by red flags throughout our country-level validation process as well as subpillars that require further qualitative research due to lack of quantitative information.
        This table serves to standardize the validation process by formatting an excel sheet that can be easily compared across countries.

        """.format(country),
        unsafe_allow_html = True
    )
    # with st.expander("Red Flags", expanded=False):
    #     c= flags[flags["Country"].isin([country]) & flags["Final_flag"].str.contains("Red")]
    #     st.dataframe(c[["GPP_Variable_Name", "Score", "Sub_Pillar"]].sort_values(by="Sub_Pillar"),
    #              use_container_width=True,
    #              hide_index= True)
        

    c= flags[flags["Country"].isin([country]) & flags["HTML_flag"].str.contains("Red")]
    subid = c["subpillar"].drop_duplicates().tolist()
    subp = subid + [1.02, 1.08, 1.06, 4.3, 8.6, 7.2]

    df = pd.DataFrame({'Sub Pillar': list(set(subp))})
    df = df.sort_values(by="Sub Pillar")
    empty_strings = [""] * len(df)
    df.insert(1, "Notes", empty_strings, True)
    df.insert(2, "Sentiment", empty_strings, True)
    df.insert(3, "Justified", empty_strings, True)
    df.insert(4, "QCC_rating", empty_strings, True)
    df.insert(5, "News_rating", empty_strings, True)
    edited_df = st.data_editor(
        df,
        column_config={
            
            "Notes": st.column_config.TextColumn(
                "Notes",
                help = "Input any relevant notes about the research",
                width = 150,

            ),

            "QCC_rating": st.column_config.SelectboxColumn(
                "QCC rating",
                help="How helpful was the QCC? (1 least - 5 most)?",
                options=[
                    1,
                    2,
                    3,
                    4,
                    5,
                ],
            ),
            "News_rating": st.column_config.SelectboxColumn(
                "News rating",
                help="How helpful was the News Report? (1 least - 5 most)?",
                options=[
                    1,
                    2,
                    3,
                    4,
                    5,
                ],
            ),
            "Sentiment": st.column_config.SelectboxColumn(
                "Trend",
                help="Is the subpillar trending Positively, Negatively, or Neutral?",
                options=[
                    "Positive",
                    "Negative",
                    "Neutral",
                ],
            ),
            "Justified": st.column_config.SelectboxColumn(
                "Validity",
                help="Is the data Justified, Inconsistent, or Unjustified?",
                options=[
                    "Justified",
                    "Inconsistent",
                    "Unjustified",
                ],
            ),
        },
        hide_index=True,
        num_rows="dynamic", 
        height = 300,
        use_container_width= False)

    #st.column_config.SelectboxColumn

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.close()
        processed_data = output.getvalue()
        return processed_data
    df_xlsx = to_excel(edited_df)
    st.download_button(label='📥 Download {} Notes'.format(country),
                                    data=df_xlsx ,
                                    file_name= "{} Notes.xlsx".format(country))


    tab0, tab1, tab2, tab3, tab4 = st.tabs(["Guidelines", "Summary of Findings", "Country Level", "Appendix", "Search"])


    def color_row(row):
        color = 'background-color: #B6F161' if row['Flag'] == 'Green' else 'background-color: #FC7661'
        return [color] * len(row)


    def insert_bold_before_pattern(text, pattern):
        # Define the regex pattern
        regex = re.compile(pattern, re.IGNORECASE)

        # Replace the matched pattern with <b> + pattern
        return regex.sub(r'<b>\g<0></b>', text)

    with tab0:

        st.markdown("""**Overview**

    The goal of this page is to facilitate the evaluation of concern for extreme issues in the GPP.

    We want to preserve the validation review process that has been implemented in the past by the GPP team, while also providing more structure and a quicker way to identify potential issues. Instead of keeping track of multiple files and documents on your device, all of the relevant information lives in one dynamic platform. 

    Our analyses are built to only identify cases of highly significant differences from our previous data as well as third party source data. We also acknowledge that many indicators are expected to change over time, or change when asked in a different way in another survey. Furthermore, our data is limited by the number of matches that can successfully be drawn from the EU GPP questionnaire to the Global GPP or to a Third Party Source. Ultimately, given these circumstances, it will still be up to the discretion of the GPP team about what and how they would like to communicate anything that might not be justified.

    For the full fieldwork, our mindset is to provide the recommendations for which comparisons need more context, and the EU GPP team may dig deeper into the question level if more information is needed.

    **Analyses**

    Each country is evaluated based on two analyses, internal and external, disaggregated by pillar and sub-pillar. 

    The internal and external analyses are based on a flagging system which is explained below. This has changed slightly from the pretest flagging system by removing yellow flags and making the thresholds more strict to avoid flagging too many questions. 

    The first analysis is a t-test between a subset of EU GPP indicators and their counterparts from the latest Global GPP per country. 

    We define a pillar as "significantly different" in the t-test analysis if:

    - 50% or more of the indicators have a statistically significant difference from our last GPP with a p-value below 0.01 (red flag)

    The second is a threshold difference between a few EU GPP indicators and their matched third party source indicators for each sub-pillar.

    We define a pillar as "significantly different" in the threshold analysis if:

    - If 50% or more of the indicators have a threshold difference above 0.35 (red flag)

    Although the analysis provides summaries at both the sub-pillar and pillar levels, the unit of analysis remains the same: the indicators. Therefore, to avoid misleading results or bias given the different sizes of sub-pillars, the number of flagged sub-pillars does not affect the number of flagged pillars. 

    Furthermore, the analysis classifies pillars and sub pillars differently, where pillar summaries concern whether or not they are significantly different while sub pillar summaries concern the presence and direction of underlying trends. 

    In both of these tests, we implemented a more qualitative labeling system to incorporate general trends and direction of difference for each sub pillar. We believe that the sub pillars represent political topic areas that are tied together, and if multiple question level comparisons follow the same pattern, this may indicate a political trend that can be validated. 

    - If 75% or more of the indicators in a sub pillar are red flags (as indicated above), we identify a trend 
    - If all of the indicators share the same direction of difference, this is indicated as "Potential Negative trend" or "Potential Positive trend"
    - If these indicators do not share the same direction, this is indicated as "Potential Mixed trend"
    - Otherwise, the sub pillar is indicated as "No change"


    **Process**

    In order to utilize this document to the fullest, we suggest navigating to the "Country Level Findings" tab to view a summary of which Sub pillars or questions are concerning. The tables in each of the sub-tabs will give you an overview of all the pillars and sub pillars. From there, if any of the Pillars are significantly different, you can investigate further in the "Appendix" tab. Under the Appendix, you can select the Pillar of interest and view the analysis results as well as contextual information for each indicator that we tested. Based on the flags in the tables, it may be necessary to proceed with qualitative research to determine if the significant changes are unexpected, and therefore troublesome. 

    Overall, this platform is a tool to help accelerate the process of identifying possible issues that should be further investigated.

    As a note, scores are re-oriented, normalized, and aggregated. The scores presented in the analyses are created by re-orienting indicators if necessary to ensure that higher numbers are better for the rule of law. Then, they are normalized to fit between 0 and 1 and finally, the individual scores are aggregated by mean.

    We will offer guidelines regarding which sub-pillars require further context and research to elucidate inconsistencies identified during the quantitative data validation process. We employ a systematic analysis approach using the flagging system to achieve this. Initially, we review all sub-pillars exhibiting potential trends in both the GPP over time analysis and the TPS Public Opinion Polls.

    If we determine an explanation for the trends observed in the GPP over time within the TPS Public Opinion Polls, we refrain from flagging the sub-pillars. However, in instances where we cannot find an explanation for the observed trends through the intersection of both analyses, we will flag the sub-pillars in the insights summary. A summary of this selection process is presented in the following flowchart.
    """, 
        unsafe_allow_html=True)
            

        def mermaid(code: str) -> None:
            stc.html(
                f"""
                <pre class="mermaid">
                    {code}
                </pre>

                <script type="module">
                    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                    mermaid.initialize({{ startOnLoad: true }});
                </script>
                """,
                height= 170
            )

        mermaid("""graph LR
            A[Subpillars flagged] --> B[Findings in GPP over time]
            A[Subpillars flagged] --> C[Findings in TPS analysis]
            B[Findings in GPP over time] -- Appendix --> D(Indicators flagged in both analyses)
            C[Findings in TPS analysis] -- Appendix --> D(Indicators flagged in both analyses)
            D(Indicators flagged in both analyses) --> E(Match level)
            D(Indicators flagged in both analyses) --> F(Time difference)
            D(Indicators flagged in both analyses) --> G(GPP time change)
        """
        )


        st.markdown("""
        In this context, we advice to be critical about the comparisons when you are making your notes. We will provide recommendations about which comparisons need more context, however keep in mind:

        - **Match level**: The comparisons with third-party sources include a column indicating the match level between the GPP and TPS questions. Comparisons with high match level should be weighted more in the overall validation.
        - **Time difference**: Many relevant third party sources are from 2020 or earlier, which can cause discrepancies in the scores simply due to change over time. Comparisons with large year gaps should be weighted less in the overall validation.
        - **GPP time change**: In many cases, the latest global GPP data we have is from as early as 2017, which will likely result in many flags. Comparisons with large year gaps should be weighted less in the overall validation.
        """)

    with tab1:

        st.markdown(paragraph(country), unsafe_allow_html=True)

        flags1 = flags[flags["Country"].isin([country])]

        spmatches = re.findall(r'\d\.\d{1,2}:', paragraph(country))

        #popsum = pop[pop['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)]

        # Select all columns except 'Pillar'

        tabx, taby = st.tabs(["National Level", "NUTS Level"])

        tmout   = tm[tm['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar'])
        popout  = pop[pop['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar'])
        exptout = expt[expt['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar'])
        with tabx:
            if len(spmatches)>0:
                if len(tmout) > 0:
                    st.dataframe(tm[tm['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)
                if len(popout) > 0:    
                    st.dataframe(pop[pop['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)
                    
                if len(exptout) > 0:    
                    st.dataframe(expt[expt['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)
        with taby:
            if len(spmatches)>0:
                if len(tmout) > 0:
                    st.dataframe(tmnuts[tmnuts['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)
                if len(popout) > 0:    
                    st.dataframe(popnuts[popnuts['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)
                if len(exptout) > 0:
                    st.dataframe(exptnuts[exptnuts['Sub Pillar'].str.contains('|'.join(spmatches), regex=True)].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height = 300)


    with tab2:

        def color_label(val):
            color = '#B6F161' if val=="Consistent" else '#FC7661'
            return f'background-color: {color}'
        
        def color_label_sub(val):
            color = '#FC7661' if val == "No Change" else '#FFFD69' if val=="Potential Mixed Trends" else '#B6F161'
            return f'background-color: {color}'
        
        st.markdown("""Below are three tabs summarizing each of the validation analyses to provide further details about the issues 
                    we have flagged. If you are interested in exploring which specific variables are flagged, please see the Appendix.""")

        taba, tabb, tabc = st.tabs(["GPP Over Time", "TPS Population Polls", "TPS Expert Survey"])

        with taba:

            st.markdown("""Since the t-test analysis this year is comparing to the previous Global GPP, there are some indicators that 
                        are new this year and do not match with the Global indicators. Therefore, there are less indicators evaluated in 
                        this analysis than the threshold analysis. Additionally, we expect many of our indicators to change in significant 
                        ways as the world changes. Therefore, it is up to the discretion of the EU GPP team whether or not the t-test 
                        results are concerning.""")
            st.dataframe(time_output.style.map(color_label, subset=['Label']),
                        column_config={
                            "Pillar": st.column_config.TextColumn(
                            width=280,
                            ), },
                        use_container_width=False, 
                        hide_index=True)
            
            st.dataframe(time_output_sub.style.map(color_label_sub, subset=['Label']), 
                        use_container_width=True, 
                        hide_index=True)
        with tabb: 

            st.dataframe(pop_output.style.map(color_label, subset=['Label']),
                        column_config={
                            "Pillar": st.column_config.TextColumn(
                            width=280,
                            ), },
                        use_container_width=False, 
                        hide_index=True)
            
            st.dataframe(pop_output_sub.style.map(color_label_sub, subset=['Label']), 
                        use_container_width=True, 
                        hide_index=True)
        with tabc: 

            st.dataframe(expt_output.style.map(color_label, subset=['Label']),
                        column_config={
                            "Pillar": st.column_config.TextColumn(
                            width=280,
                            ), },
                        use_container_width=False, 
                        hide_index=True)
            
            st.dataframe(expt_output_sub.style.map(color_label_sub, subset=['Label']), 
                        use_container_width=True, 
                        hide_index=True)
        

    with tab3: 

        st.markdown("""Each tab below holds the full information for each analysis for each pillar in order to facilitate the evaluation of the results. 
                    At the moment, we do not have any matches in Pillar 6, and therefore there are no analysis tables for Pillar 6.""")

        tabp1, tabp2, tabp3, tabp4, tabp5, tabp6, tabp7, tabp8 = st.tabs(["Pillar 1", "Pillar 2", "Pillar 3", "Pillar 4", "Pillar 5", "Pillar 6", "Pillar 7", "Pillar 8"])
        
        tablist = [tabp1, tabp2, tabp3, tabp4, tabp5, tabp6, tabp7, tabp8]
        for i in range(0,8):

            with tablist[i]:

                tabx, taby, tabz = st.tabs(["GPP Over Time", "TPS Population Polls", "TPS Expert Survey"])


                with tabx:
                    st.markdown("""In the T-test, a red flag indicates statistical significance with a p-value of 0.01. 
                                A green flag indicates statistical significance only with a p-value greater than 0.01, or no statistical significance.""")
                    
                    st.dataframe(tm[tm['Pillar'].astype(str).str.contains(str(i+1))].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height=300)
                    
                with taby: 
                    st.markdown("""In the threshold difference, a red flag indicates a difference of 0.35 or more. 
                                DISCLAIMER: some large differences may be caused by low matches between the content of the GPP and TPS questions. 
                                Make sure to account for how similar (or dissimilar) each pair is when performing qualitative checks.""")
                    
                    st.dataframe(pop[pop['Pillar'].astype(str).str.contains(str(i+1))].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height=300)
                    
                with tabz: 
                    st.markdown("""In the threshold difference, a red flag indicates a difference of 0.35 or more. 
                                DISCLAIMER: some large differences may be caused by low matches between the content of the GPP and TPS questions. 
                                Make sure to account for how similar (or dissimilar) each pair is when performing qualitative checks.""")
                    
                    st.dataframe(expt[expt['Pillar'].astype(str).str.contains(str(i+1))].drop(columns=['Pillar']).style.apply(color_row, axis=1),
                                hide_index=True,
                                height=300)




    with tab4:
        
        
        #st.markdown("""<b>Summary</b> <br> <b>Pillar 1: </b> In 2023, Luxembourg maintains strong public trust in its judicial independence, with majorities of both the general public and businesses expressing confidence in the courts and judges (but there is a slight decline in business confidence). Positive developments include a constitutional reform that established the National Council for Justice (NCJ) and strengthened the independence of the Prosecutor's Office, aligning Luxembourg with European standards and fulfilling EU recommendations. The expansion of the EU Whistleblower Directive and the implementation of a transparency register for Members of Parliament mark further progress towards transparency and accountability. However, there are areas of concern, such as criticism of the transparency register's limited scope, and the absence of a comprehensive anti-corruption strategy or body. Also, the Corruption Prevention Committee's lack of transparency and engagement with civil society points to a need for more robust anti-corruption measures. <br> <br> <b>Pillar 2: </b> Luxembourg’s anti-corruption framework, led by the Ministry of Justice and supported by various institutions, ranks highly globally and within the EU. The country has experienced a slight increase in reported corruption cases and convictions, indicating both a challenge in combating corruption and an effective response to it. In line with the 2022 EU Rule of Law Report’s recommendations, Luxembourg has boosted resources for tackling economic and financial crime, with a focus on enhancing prosecution services and law enforcement capabilities. New laws aim to improve the management of seized assets and foster collaboration against financial crimes. Despite these efforts, the Special Eurobarometer on Corruption indicates mixed perceptions among the public and businesses regarding corruption's prevalence and the effectiveness of punitive measures. GRECO acknowledges Luxembourg's satisfactory implementation of reforms to ensure judiciary transparency and objectivity but notes shortcomings in verifying the accuracy of financial declarations by members of parliament, underscoring the need for further improvements in oversight and transparency. <br> <br> <b>Pillar 3: </b> The government has introduced “BEE SECURE”, an initiative aimed at bolstering online support for civil society organizations (CSOs) and preserving open civic space, without changing the legislative framework for CSOs since the 2022 EU Rule of Law Report. This reflects a positive development, indicating a supportive environment for CSOs with an emphasis on enhancing online safety and responsible digital behavior. Additionally, a constitutional reform adopted on 21 December 2022 has advanced citizen engagement by allowing legislative proposals from citizens to be considered by Parliament, a move towards direct democracy. However, the area of public consultations shows no progress; despite the EU’s recommendations for increased stakeholder participation, Luxembourg has not improved the inclusivity of its consultation processes. Regular and meaningful consultations, particularly in non-legislative areas, remain an unmet goal, highlighting a significant gap in stakeholder engagement and transparency in the legislative process. Pillar 4: In terms of the right to information and access to justice, Luxembourg is actively addressing the need for better court statistics and data collection, acknowledging the inadequacy of current systems for detailed analysis. The country is tackling access to justice issues, facing challenges with a limited number of authoritative bodies equipped to handle discrimination and human rights violations, alongside underused existing support mechanisms, hindered by several factors such as fear of retaliation. Transparency issues persist, especially with non-disclosure of government positions on key directives and insufficient communication with non-governmental stakeholders. However, legislative steps towards recognizing hate crimes and combating racism, including the publication of a national study and the drafting of a National Action Plan on anti-racism, mark positive developments. The government has also addressed the challenge of affordable housing with financial support and strategic plans, alongside targeted subsidies to mitigate rising energy costs due to geopolitical tensions. Also, efforts to reform youth protection and the implementation of the National Action Plan for Children’s Rights demonstrate Luxembourg’s commitment to child welfare and rights. Pillar 5: Luxembourg provides its citizens with a high level of physical security, maintaining adequate prison conditions and strong protections against excessive force. The country records a low rate of violent crime, with an impressive 87% of people feeling safe walking alone at night, well above the OECD average. Furthermore, its homicide rate of 0.2 per 100,000 inhabitants significantly undercuts the OECD average, highlighting Luxembourg’s status as a safe and secure nation. The country also enjoys a reputation for political stability, experiencing no serious incidents of politically motivated damage recently. Demonstrations, though rare, typically focus on European entities located within Luxembourg, such as the European Court of Justice, rather than the country itself, showing little political unrest and no threats from insurrections or hostile neighbors. Pillar 6: Luxembourg has shown commendable compliance with European Court of Human Rights (ECtHR) judgments, effectively implementing nearly all decisions over the past decade, with an exceptional case remaining pending as of January 2023. This case, related to a fair trial violation by the Court of Cassation, underscores a minor setback in an otherwise strong record of adhering to ECtHR judgments. The country has addressed various ECtHR concerns, including judicial review for parole revocations and enhancing criminal suspects’ rights. Luxembourg maintains effective mechanisms for enforcing administrative judgments, ensuring compliance and accountability. On the economic front, despite facing challenges from inflation and global disruptions, Luxembourg has maintained stable public finances and economic growth, supported by government measures to protect households and firms. The country continues to implement regulatory reforms to address money laundering, terrorist financing, and tax evasion, underscoring its commitment to openness, transparency, and competitiveness. Pillar 7:  In 2022, Luxembourg initiated its first pilot project for digitalizing administrative justice, aiming for a “paperless justice” system by 2026, yet the complete transition faces challenges due to restrictive procedural rules and a scarcity of digital tools for case management. The reform to expand legal aid, suggested in the 2022 EU Rule of Law Report, remains in review, with concerns over delays in providing legal representation to children in criminal proceedings. Courts have improved their efficiency, showing better clearance rates and stable case resolution times. However, the Luxembourg Bar Association raises concerns over the potential effects of anti-money laundering regulations on lawyers’ independence, urging for legislative clarity to protect professional secrecy and uphold the rule of law. Pillar 8: The 2023 Law amending the Code of Criminal Procedure and the Law on court organization has advanced the objectivity of justice administration in Luxembourg by empowering the Minister of Justice to issue criminal policy guidelines, effectively standardizing prosecution processes. This measure, coupled with the strengthened independence of the Public Prosecution Service and an autonomous National Judicial Council, earns praise from GRECO for promoting prosecutorial independence and streamlining law enforcement without infringing on individual case integrity. Luxembourg consistently ensures due process, guaranteeing fair public trials and protection against arbitrary detention. Progress towards enhancing minors' rights in criminal proceedings reflects a commitment to safeguarding vulnerable individuals, complemented by extensive victim support services. However, the country faces challenges, such as the deterrent effect of high legal costs and unclear access to justice for human rights violations linked to Luxembourg-based businesses.""", unsafe_allow_html= True)
        # Combine unique GPP Indicators
        varslist = pd.unique(pd.concat([pop['GPP Indicator'], expt['GPP Indicator'], tm['GPP Indicator']]))
        z = pd.DataFrame({"GPP Indicator": varslist})

        # Remove Pillar column if it exists
        tm2 = tm.drop(columns=['Pillar'], errors='ignore')
        tps2 = tps.drop(columns=['Pillar'], errors='ignore')

        # Sidebar filter selection
        selected_indicator = st.selectbox("Select GPP Indicator", z['GPP Indicator'])

        # Filter data based on selection
        filtered_tm = tm2[tm2['GPP Indicator'] == selected_indicator]
        filtered_tps = tps2[tps2['GPP Indicator'] == selected_indicator]

        # Display the data tables
        st.write("### GPP Over Time")
        st.dataframe(filtered_tm.style.format({"Current Score": "{:.3f}", "Previous Score": "{:.3f}", "P value": "{:.3f}"}).apply(color_row, axis=1),
                    hide_index=True,
                    height= (len(filtered_tm) +1)*50)

        st.write("### Third Party Source")
        st.dataframe(filtered_tps.style.format({"GPP Score": "{:.3f}", "TPS Score": "{:.3f}", "Difference": "{:.3f}"}).apply(color_row, axis=1),
                    hide_index=True,
                    height= (len(filtered_tps) +1)*50)
        

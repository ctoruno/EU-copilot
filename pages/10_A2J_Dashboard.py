"""
Project:            EU Copilot App
Module Name:        Access to Justice Dashboard
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
from plotly.subplots import make_subplots

# page configuration
st.set_page_config(
    page_title= "Access to Justice Journey",
    page_icon = "📶",
)

# reading css styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>",
                unsafe_allow_html=True)
    
# sidebar menu
sidemenu.insert_smenu()

if passcheck.check_password():
    dbtoken  = st.secrets["dbtoken"]
    dbkey    = st.secrets["app_key"]
    dbsecret = st.secrets["app_secret"]

    atoken = passcheck.retrieve_DBtoken(dbkey, dbsecret, dbtoken)

    #####################################################################################################################
    #                                                        LOADING DATA                                               #
    #####################################################################################################################
    # Accessing Dropbox
    dbx = dropbox.Dropbox(atoken)

    # loading function
    @st.cache_data
    def load_DBfile(file, format, sheet=None):

        # accessing dropbox files
        __, res = dbx.files_download(f"/{file}")
        data = res.content

    # reading data frames
        with BytesIO(data) as file:
            if format == 'excel':
                df = pd.read_excel(file, sheet_name = sheet)
            if format == 'csv':
                df = pd.read_csv(file)
        return df





    gpp_datapoints = load_DBfile("data4web_gpp.csv", format = 'csv')

    # load wrangled A2J data
    sections = [f"Section{i}" for i in range(1,7)]
    data = {section: load_DBfile("A2J_justicejourney_wrangled.xlsx", format = 'excel', sheet = section) for section in sections}

    # load sheets
    section1 = data["Section1"].mask(data["Section1"]['total_count'] < 30)
    section2 = data["Section2"]
    section3 = data["Section3"].mask(data["Section3"]['total_sources'] < 30)
    section4 = data["Section4"]
    section5 = data["Section5"]
    section6 = data["Section6"]

    # impute values with observation count <= 30
    count_sections = ['Section2', 'Section4', 'Section5',  'Section6']
    for section in count_sections:
        data[section] = data[section].mask(data[section]['count'] < 30)


    # header and explanation
    st.markdown(
        """
        <p class='jtext'>
        Welcome to the <strong style="color:#003249">Justice Journey Dashboard</strong>. In this page you can view Access to Justice
        data. The data presented here is just a preview and 
        <b><i>BY NO MEANS should be considered final or official</i></b>.
        </p>
        <p class='jtext'>
        Galingan!
        </p>
        """,
        unsafe_allow_html = True
    )

    eu_or_country = st.selectbox(
        "Would you like to focus on all EU member states or a specific country? ",
        ["EU", "Country"],
        index = 0
    )

    demographic = st.selectbox(
        "Total sample or a disaggregation? ",
        ["Total sample", "Disagreggated by Gender", "Disagreggated by Income"]
    )

    #####################################################################################################################
    #                                               FILTERING - NATIONAL LEVEL                                          #
    #####################################################################################################################

    if eu_or_country == "Country":
        country = st.selectbox(
            "Please select a country from the list below: ",
            gpp_datapoints.loc[gpp_datapoints['country'] != 'Ireland']
            .drop_duplicates(subset="country")
            .country.to_list()
        )

        level = 'national' # for later filtering

        if demographic == 'Total sample':
            section1 = section1.loc[(section1['country_name_ltn'] == country) & (section1['demographic'] == 'Total sample')]
            section2 = section2.loc[(section2['country_name_ltn'] == country) & (section2['demographic'] == "Total Sample")]
            section3 = section3.loc[(section3['country_name_ltn'] == country) & (section3['demographic'] == 'Total sample')]
            section4 = section4.loc[(section4['country_name_ltn'] == country) & (section4['demographic'] == "Total Sample")]
            section5 = section5.loc[(section5['country_name_ltn'] == country) & (section5['demographic'] == 'Total Sample')]
            section6 = section6.loc[(section6['country_name_ltn'] == country) & (section6['demographic'] == 'Total sample')]

        if demographic == 'Disagreggated by Gender':
            section1 = section1.loc[(section1['country_name_ltn'] == country) & ((section1['demographic'] == 'Male') | (section1['demographic'] == 'Female'))]
            section2 = section2.loc[(section2['country_name_ltn'] == country) & ((section2['demographic'] == 'Male') | (section2['demographic'] == 'Female'))]
            section3 = section3.loc[(section3['country_name_ltn'] == country) & ((section3['demographic'] == 'Male') | (section3['demographic'] == 'Female') )]
            section4 = section4.loc[(section4['country_name_ltn'] == country) & ((section4['demographic'] == 'Male') | (section4['demographic'] == 'Female'))]
            section5 = section5.loc[(section5['country_name_ltn'] == country) & ((section5['demographic'] == 'Male') | (section5['demographic'] == 'Female'))]
            section6 = section6.loc[(section6['country_name_ltn'] == country) & ((section6['demographic'] == 'Male') | (section6['demographic'] == 'Female'))]

        if demographic == 'Disagreggated by Income':
            section1 = section1.loc[(section1['country_name_ltn'] == country) & ((section1['demographic'] == 'Financially Tight') | (section1['demographic'] == 'Financially Stable'))]
            section2 = section2.loc[(section2['country_name_ltn'] == country) & ((section2['demographic'] == 'Financially Tight') | (section2['demographic'] == 'Financially Stable'))]
            section3 = section3.loc[(section3['country_name_ltn'] == country) & ((section3['demographic'] == 'Financially Tight') | (section3['demographic'] == 'Financially Stable') )]
            section4 = section4.loc[(section4['country_name_ltn'] == country) & ((section4['demographic'] == 'Financially Tight') | (section4['demographic'] == 'Financially Stable'))]
            section5 = section5.loc[(section5['country_name_ltn'] == country) & ((section5['demographic'] == 'Financially Tight') | (section5['demographic'] == 'Financially Stable'))]
            section6 = section6.loc[(section6['country_name_ltn'] == country) & ((section6['demographic'] == 'Financially Tight') | (section6['demographic'] == 'Financially Stable'))]


    ######################################################################################################################
    #                                                   FILTERING - EU LEVEL                                             #
    ######################################################################################################################
    if eu_or_country == "EU":
        country = 'European Union' # for filtering gpp datapoints
        level = 'eu'
        # gather dataset for eu
        if demographic == "Total sample" :
            section1 = pd.DataFrame({
                'country_name_ltn': "European Union",
                'demographic': "Total sample",
                'category': section1.loc[section1['demographic'] == "Total sample"].groupby('category')['value2plot'].mean().index,
                'value2plot': section1.loc[section1['demographic'] == "Total sample"].groupby('category')['value2plot'].mean().values
            })

            section2 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : 'Total sample',
                'advice' : [
                    section2.loc[section2['demographic'] == 'Total Sample', 'advice'].mean()
                ],
                'get_information': [
                        section2.loc[section2['demographic'] == 'Total Sample', 'get_information'].mean()
                    ],
                    'get_expert': [
                        section2.loc[section2['demographic'] == 'Total Sample', 'get_expert'].mean()
                    ],
                    'confidence': [
                        section2.loc[section2['demographic'] == 'Total Sample', 'confidence'].mean()
                    ]
            })

            section3 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : 'Total sample',
                'adviser' : section3.loc[section3['demographic'] == 'Total sample'].groupby('adviser')['value2plot'].mean().index,
                'value2plot' : section3.loc[section3['demographic'] == 'Total sample'].groupby('adviser')['value2plot'].mean().values
            })

            section4 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : 'Total sample',
                'fully_resolved': [
                        section4.loc[section4['demographic'] == 'Total Sample', 'fully_resolved'].mean()
                    ],
                'problem_persists': [
                        section4.loc[section4['demographic'] == 'Total Sample', 'problem_persists'].mean()
                    ],
                'satisfaction' : [
                        section4.loc[section4['demographic'] == 'Total Sample', 'satisfaction'].mean()
                ]
            })

            section5 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : 'Total sample',
                'fair' : [section5.loc[section5['demographic'] == 'Total Sample', 'fair'].mean()],
                'time' : [section5.loc[section5['demographic'] == 'Total Sample', 'time'].mean()],
                'financial_diff' : [section5.loc[section5['demographic'] == 'Total Sample', 'financial_diff'].mean()],
                'slow' : [section5.loc[section5['demographic'] == 'Total Sample', 'slow'].mean()],
                'expensive' : [section5.loc[section5['demographic'] == 'Total Sample', 'expensive'].mean()]
            })

            section6 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : 'Total sample',
                'any_hardship' : [section6.loc[section6['demographic'] == 'Total sample', 'any_hardship'].mean()],
                'health' : [section6.loc[section6['demographic'] == "Total sample", 'health'].mean()] ,
                'interpersonal' :[section6.loc[section6['demographic'] == 'Total sample', 'interpersonal'].mean()] ,
                'economic' : [section6.loc[section6['demographic'] == 'Total sample', 'interpersonal'].mean()], 
                'drugs' : [section6.loc[section6['demographic'] == 'Total sample', 'drugs'].mean()]
            })


        if demographic == "Disagreggated by Gender" :
            section1 = section1.loc[
                (section1['demographic'] == 'Male') | (section1['demographic'] == 'Female')
            ].groupby(['demographic', 'category'])['value2plot'].mean().reset_index()
            section1 = pd.DataFrame({
                'country_name_ltn': 'European Union',
                'demographic': section1['demographic'],  
                'category': section1['category'],        
                'value2plot': section1['value2plot']    
            })


            section2 = section2.loc[
                (section2['demographic'] == 'Male') | (section2['demographic'] == 'Female')
                ].groupby('demographic')[['get_expert', 'get_information', 'confidence', 'advice' ]].mean().reset_index()
            section2 = pd.DataFrame({
                'country_name_ltn': 'European Union',
                'demographic': section2['demographic'],  # Filtered demographics
                'get_information': pd.to_numeric(section2['get_information'], errors = 'coerce'),  
                'get_expert': pd.to_numeric(section2['get_expert'], errors = 'coerce'),            
                'confidence': pd.to_numeric(section2['confidence'], errors = 'coerce'),
                'advice' : pd.to_numeric(section2['advice'], errors = 'coerce')            
            })

            section3 = section3.loc[(section3['demographic'] == 'Male') | (section3['demographic'] == 'Female')].groupby(['demographic', 'adviser'])['value2plot'].mean().reset_index()
            section3 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section3['demographic'],
                'adviser' : section3['adviser'],
                'value2plot' : section3['value2plot']
            })

            section4 = section4.loc[(section4['demographic'] == 'Male') | (section4['demographic'] == 'Female')].groupby('demographic')[['fully_resolved', 'problem_persists', 'satisfaction']].mean().reset_index()
            section4 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section4['demographic'],
                'fully_resolved' : section4['fully_resolved'],
                'problem_persists' : section4['problem_persists'],
                'satisfaction' : section4['satisfaction']
            })

            section5 = section5.loc[(section5['demographic'] == 'Male') | (section5['demographic'] == 'Female')].groupby('demographic')[['fair', 'time', 'financial_diff', 'slow', 'expensive']].mean().reset_index()
            section5 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section5['demographic'],
                'fair' : section5['fair'],
                'time' : section5['time'],
                'financial_diff' : section5['financial_diff'],
                'slow' : section5['slow'],
                'expensive' : section5['expensive']
            })

            section6 = section6.loc[(section6['demographic'] == 'Male') | (section6['demographic'] == 'Female')].groupby('demographic')[['any_hardship', 'health', 'interpersonal', 'economic', 'drugs']].mean().reset_index()
            section6 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section6['demographic'],
                'any_hardship' : section6['any_hardship'],
                'health' : section6['health'],
                'interpersonal' : section6['interpersonal'],
                'economic' : section6['economic'],
                'drugs' : section6['drugs']
            })
            
        if demographic == "Disagreggated by Income" :
            section1 = section1.loc[(section1['demographic'] == 'Financially Tight') | (section1['demographic'] == 'Financially Stable')].groupby(['demographic', 'category'])[['total_count', 'value2plot', 'total_incidents']].mean().reset_index()
            section1 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section1['demographic'],
                'category' : section1['category'],
                'value2plot' : section1['value2plot'],
                'total_count' : section1['total_count'],
                'total_incidents' : section1['total_incidents']
                })

            section2 = section2.loc[(section2['demographic'] == 'Financially Tight') | (section2['demographic'] == 'Financially Stable')].groupby('demographic')[['get_information', 'get_expert', 'confidence', 'advice']].mean().reset_index()
            section2= pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section2['demographic'],
                'get_expert' : section2['get_expert'],
                'get_information' : section2['get_information'],
                'confidence' : section2['confidence'],
                'advice' : section2['advice']         
            })
    
            section3 = section3.loc[(section3['demographic'] == 'Financially Tight') | (section3['demographic'] == 'Financially Stable')].groupby(['demographic', 'adviser'])['value2plot'].mean().reset_index()
            section3 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section3['demographic'],
                'adviser' : section3['adviser'],
                'value2plot' : section3['value2plot']
            })

            section4 = section4.loc[(section4['demographic'] == 'Financially Tight') | (section4['demographic'] == 'Financially Stable')].groupby('demographic')[['fully_resolved', 'problem_persists', 'satisfaction']].mean().reset_index()
            section4 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section4['demographic'],
                'fully_resolved' : section4['fully_resolved'],
                'problem_persists' : section4['problem_persists'],
                'satisfaction' : section4['satisfaction']
            })
            section5 = section5.loc[(section5['demographic'] == 'Financially Tight') | (section5['demographic'] == 'Financially Stable')].groupby('demographic')[['fair', 'time', 'financial_diff', 'slow', 'expensive']].mean().reset_index()
            section5 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section5['demographic'],
                'fair' : section5['fair'],
                'time' : section5['time'],
                'financial_diff' : section5['financial_diff'],
                'slow' : section5['slow'],
                'expensive' : section5['expensive']
            })

            section6 = section6.loc[(section6['demographic'] == 'Financially Tight') | (section6['demographic'] == 'Financially Stable')].groupby('demographic')[['any_hardship', 'health', 'interpersonal', 'economic', 'drugs']].mean().reset_index()
            section6 = pd.DataFrame({
                'country_name_ltn' : 'European Union',
                'demographic' : section6['demographic'],
                'any_hardship' : section6['any_hardship'],
                'health' : section6['health'],
                'interpersonal' : section6['interpersonal'],
                'economic' : section6['economic'],
                'drugs' : section6['drugs']
            })



    # viz
    # part 1. percentage who experience legal problems
    import plotly.graph_objects as go

    #####################################################################################################################
    #                                           DASHBOARD - TOTAL SAMPLE                                                #
    #####################################################################################################################

    if demographic == "Total sample": 
        # 1. LEGAL PROCESS
        prevalence = gpp_datapoints.loc[(gpp_datapoints['country'] == country) & (gpp_datapoints['level'] == level) & 
                                        (gpp_datapoints['id'] == 'prevalence2') & (gpp_datapoints['demographic'] == 'Total Sample')]['value'].iloc[0] * 100
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                1. Legal Process
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            In {country}, <strong>{prevalence: .2f}%</strong> experienced a non-trivial problem in the last two years.  
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        fig1 = px.scatter(
            section1,
            x='value2plot',
            y='category',
            color='category',
        )
        category_colors = {trace.name: trace.marker.color for trace in fig1.data}


        for index, row in section1.iterrows():
            fig1.add_trace(
                go.Scatter(
                    x=[0, row['value2plot']],  
                    y=[row['category'], row['category']],  
                    mode='lines',
                    line=dict(color=category_colors[row['category']], width=2),  
                    showlegend=False 
                )
            )
        fig1.update_traces(
            hovertemplate = 'Category: %{y} <br> Prevalence: %{x:.2f}%'

        )

        fig1.update_layout(
            title="Legal Process",
            xaxis_title="Percentage of Respondents who Experienced that Type of Problem",
            yaxis_title=" ",
            template="plotly_white",
            showlegend = False,
            xaxis = dict(range = (0,100)),
        )

        st.plotly_chart(fig1)

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 2. LEGAL CAPABILITY
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
            2.  Legal Capability
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section2['get_information'].iloc[0] *100: .2f}%</strong> knew where to get advice and information. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section2['get_expert'].iloc[0] * 100: .2f}</strong>% felt that they could get all of the expert help they wanted. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section2['confidence'].iloc[0] * 100: .2f}</strong>% were confident that they could achieve a fair outcome. 
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>
            """,
        unsafe_allow_html=True
        )

        # 3. SOURCES OF HELP
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                3. Sources of Help
            </h3>
            """,
            unsafe_allow_html=True
        )

        # advisers - total sample
        adviser_mapping = {
        'AJD_adviser_1': 'Relatives and friends',
        'AJD_adviser_2': 'Lawyer or professional adviser',
        'AJD_adviser_3': 'Government legal aid',
        'AJD_adviser_4': 'Court, govt, police',
        'AJD_adviser_5': 'Health or welfare adviser',
        'AJD_adviser_6': 'Trade union or employer',
        'AJD_adviser_7': 'Religious or community advisor',
        'AJD_adviser_8': 'Civil society or charity',
        'AJD_adviser_9': 'Other organization advisor',
    }

        section3['advisor_name'] = section3['adviser'].map(adviser_mapping)

        fig3 = go.Figure(
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color='black', width=0.5),
                    label=section3['advisor_name'].tolist() + ['Total']
                ),
                link=dict(
                    source=list(range(len(section3))),
                    target=[len(section3)] * len(section3),
                    value=section3['value2plot']*100,
                    customdata=section3['advisor_name'],
                    hovertemplate='Advisor: %{customdata}<br>Value: %{value:.2f} % <extra></extra>'
                )
            )
        )

        fig3.update_layout(
            title_text="Distribution of Advisors",
            font_size=12,
            template="plotly_white"
        )

        st.plotly_chart(fig3)

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 4. STATUS
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                4. Status
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section4['fully_resolved'].iloc[0]*100: .2f}%</strong> were able to fully resolve their issue. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section4['problem_persists'].iloc[0] * 100: .2f}</strong>% gave up any action to resolve the problem further. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section4['satisfaction'].iloc[0]*100: .2f}%</strong> were satisfied with the outcome of the resolution.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 5. PROCESS
        st.markdown(
            f"""
            <h3 style='text-align: center;'>5. Process</h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section5['fair'].iloc[0]*100:.2f}%</strong> said that the process was fair.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            On average, it took <strong>{section5['time'].iloc[0]:.1f}</strong> months for respondents to solve the problem.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section5['financial_diff'].iloc[0]*100:.2f}%</strong> said that the process was financially difficult.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section5['expensive'].iloc[0]*100:.2f}%</strong> said that the process was expensive.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{section5['slow'].iloc[0]*100:.2f}%</strong> said that the process was slow.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 6. HARDSHIP
        st.markdown(
            """
            <h3 style='text-align: center;'>
                6. Hardship
            </h3>""",
            unsafe_allow_html=True)
        
        hardship = pd.melt(
            section6,
            id_vars=['country_name_ltn', 'demographic'],
            value_vars = ['any_hardship', 'health', 'interpersonal', 'economic', 'drugs'],
            var_name='Type of Hardship',
            value_name = 'value2plot'
        )
        fig4 = px.bar(
                x = hardship['Type of Hardship'],
                y = hardship['value2plot']*100,
                color = hardship['Type of Hardship'],
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
        fig4.update_traces(
            hovertemplate = '%{y:.2f}%'
        )

        fig4.update_layout(
        title=" ",
        xaxis_title="Type of Hardship",
        yaxis_title="Proportion of Respondents (%)",
        template="plotly_white",
        font=dict(size=14),
        showlegend = False,
        yaxis = dict(range=(0,100)))

        st.plotly_chart(fig4)

    #####################################################################################################################
    #                                           DASHBOARD - GENDER DISAGREGGATION                                       #
    #####################################################################################################################


    if demographic == 'Disagreggated by Gender':
        prevalence_male = gpp_datapoints.loc[(gpp_datapoints['country'] == country) & (gpp_datapoints['level'] == level) & 
                                        (gpp_datapoints['id'] == 'prevalence2') & (gpp_datapoints['demographic'] == 'Male')]['value'].iloc[0] * 100
        
        prevalence_female = gpp_datapoints.loc[(gpp_datapoints['country'] == country) & (gpp_datapoints['level'] == level) & 
                                        (gpp_datapoints['id'] == 'prevalence2') & (gpp_datapoints['demographic'] == 'Female')]['value'].iloc[0] * 100
        
        import streamlit as st

        # Display the title
        st.markdown("<h3 style='text-align: center;'>1. Legal Process</h3>", unsafe_allow_html=True)

        # Markdown table
        st.markdown(
            f"""
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Men in {country}</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Women in {country}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{prevalence_male:.2f}</strong>% of men experienced a non-trivial legal problem in the last two years.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{prevalence_female:.2f}</strong>% of women experienced a non-trivial legal problem in the last two years.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)



        male_1 = section1[section1['demographic'] == 'Male']
        female_1 = section1[section1['demographic'] == 'Female']

        # Create subplots with two panels
        fig = make_subplots(
            rows=1, cols=2,  # One row, two columns
            subplot_titles=("Male", "Female"),
            shared_yaxes=True,  # Share the y-axis for better comparison
        )

        # Scatter plot for Male
        fig.add_trace(
            go.Scatter(
                x=male_1['value2plot'],
                y=male_1['category'],
                mode='markers',
                marker=dict(color='blue'),
                name='Male',
            ),
            row=1, col=1  # First panel
        )

        # Add horizontal lines for Male
        for _, row in male_1.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[0, row['value2plot']],
                    y=[row['category'], row['category']],
                    mode='lines',
                    line=dict(color='blue', width=2),
                    showlegend=False,
                ),
                row=1, col=1,
            )

        # Scatter plot for Female
        fig.add_trace(
            go.Scatter(
                x=female_1['value2plot'],
                y=female_1['category'],
                mode='markers',
                marker=dict(color='pink'),
                name='Female',
            ),
            row=1, col=2  # Second panel
        )
        fig.update_traces(
            hovertemplate = 'Category: %{y} <br> Value: %{x:.2f}% '
        )

        # Add horizontal lines for Female
        for _, row in female_1.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[0, row['value2plot']],
                    y=[row['category'], row['category']],
                    mode='lines',
                    line=dict(color='pink', width=2),
                    showlegend=False,
                ),
                row=1, col=2,
            )

        fig.update_layout(
            title="Legal Process by Gender",
            xaxis_title="Percentage of Respondents",
            yaxis_title="Type of Problem",
            template="plotly_white",
            height=600,
            width=800,
            showlegend=False,
            xaxis = dict(range = (0,100)),
            xaxis2 = dict(range = (0,100))
        )


        fig.update_xaxes(title_text="Percentage of Respondents", row=1, col=1)
        fig.update_xaxes(title_text="Percentage of Respondents", row=1, col=2)
        fig.update_yaxes(title_text="Type of Problem", row=1, col=1)

        st.plotly_chart(fig)

        male_2 = section2[section2['demographic'] == 'Male']
        female_2 = section2[section2['demographic'] == 'Female']

        get_info_male = male_2['get_information'].iloc[0]*100
        get_info_female = female_2['get_information'].iloc[0]*100
        get_expert_male = male_2['get_expert'].iloc[0]*100
        get_expert_female = female_2['get_expert'].iloc[0]*100
        confidence_male = male_2['confidence'].iloc[0]*100
        confidence_female = female_2['confidence'].iloc[0]*100

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)

        # 2. LEGAL CAPABILITY
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                2. Legal Capability
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Men in {country}</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Women in {country}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{get_info_male:.2f}</strong>% knew where to get advice and information.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_info_female:.2f}</strong>% knew where to get advice and information.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_expert_male:.2f}</strong>% felt that they could get all of the expert help they needed.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_expert_female:.2f}</strong>% felt that they could get all of the expert help they needed.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{confidence_male:.2f}</strong>% were confident that they could achieve a fair outcome. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{confidence_female:.2f}</strong>% were confident that they could achieve a fair outcome. 
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )


        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)


        # 3. SOURCES OF HELP
        male_3 = section3[section3['demographic'] == 'Male']
        female_3 = section3[section3['demographic'] == 'Female']


        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                3. Sources of Help
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Men in {country}</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Women in {country}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_2['advice'].iloc[0]*100:.2f}</strong>% were able to access help for their issue.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_2['advice'].iloc[0]*100:.2f}</strong>% were able to access help for their issue.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        adviser_mapping = {
        'AJD_adviser_1': 'Relatives and friends',
        'AJD_adviser_2': 'Lawyer or professional adviser',
        'AJD_adviser_3': 'Government legal aid',
        'AJD_adviser_4': 'Court, govt, police',
        'AJD_adviser_5': 'Health or welfare adviser',
        'AJD_adviser_6': 'Trade union or employer',
        'AJD_adviser_7': 'Religious or community advisor',
        'AJD_adviser_8': 'Civil society or charity',
        'AJD_adviser_9': 'Other organization advisor',
    }
        section3['adviser_name'] = section3['adviser'].map(adviser_mapping)
        male_3['adviser_name'] = male_3['adviser'].map(adviser_mapping)
        female_3['adviser_name'] = female_3['adviser'].map(adviser_mapping)

        link_colors = section3['demographic'].map({'Male': 'sky-blue', 'Female': 'pink'})
        
        fig_3a = make_subplots(
        rows=1, cols=2,  # Two horizontal panels
        subplot_titles=("Men", "Women"),
        specs=[[{"type": "sankey"}, {"type": "sankey"}]]
        )
        fig_3a.add_trace(
            go.Sankey(
                node=dict(
                    pad=15, thickness=20, line=dict(color="black", width=0.5),
                    label=male_3['adviser_name'].tolist() + ["Total"]
                ),
                link=dict(
                    source=list(range(len(male_3))),
                    target=[len(male_3)] * len(male_3),
                    value=(male_3["value2plot"]*100).tolist(),
                    color=["#87CEEB"] * len(male_3),
                    customdata = male_3['adviser_name'],
                    hovertemplate='Advisor: %{customdata}<br>Value: %{value:.2f}%<extra></extra>'
                )
            ),
            row=1, col=1
        )

        # Add Female Sankey (flows downward)
        fig_3a.add_trace(
            go.Sankey(
                node=dict(
                    pad=15, thickness=20, line=dict(color="black", width=0.5),
                    label=female_3['adviser_name'].tolist() + ["Total"]
                ),
                link=dict(
                    source=list(range(len(female_3))),
                    target=[len(female_3)] * len(female_3),
                    value=(female_3["value2plot"]*100).tolist(),
                    color=["pink"] * len(female_3),
                    customdata = female_3['adviser_name'],
                    hovertemplate='Advisor: %{customdata}<br>Value: %{value:.2f}%<extra></extra>'
                )
            ),
            row=1, col=2
        )

        # Update layout
        fig_3a.update_layout(
            title_text="Advisor Distribution by Gender",
            font_size=12,
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig_3a)


        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )
        # 4. STATUS
        male_4 = section4[section4['demographic'] == 'Male']
        female_4 = section4[section4['demographic'] == 'Female']
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                4. Status
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Men in {country}</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Women in {country}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_4['fully_resolved'].iloc[0]*100:.2f}</strong>% were able to fully resolve the issue. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_4['fully_resolved'].iloc[0]*100:.2f}</strong>% were able to fully resolve the issue. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{male_4['problem_persists'].iloc[0]*100:.2f}</strong>% gave up any action to solve the problem further.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_4['problem_persists'].iloc[0]*100:.2f}</strong>% gave up any action to solve the problem further.
                        </td>
                    </tr>'
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_4['satisfaction'].iloc[0]*100:.2f}</strong>% were satisfied with the outcome of the resolution. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_4['satisfaction'].iloc[0]*100:.2f}</strong>% were satisfied with the outcome of the resolution.  
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )




        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)

        # 5. PROCESS
        male_5 = section5[section5['demographic'] == 'Male']
        female_5 = section5[section5['demographic'] == 'Female']
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
            5.  Process
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Men in {country}</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Women in {country}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_5['fair'].iloc[0]*100:.2f}</strong>% said that the process was fair. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_5['fair'].iloc[0]*100:.2f}</strong>% said that the process was fair. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            On average, it took <strong>{male_5['time'].iloc[0]:.1f}</strong> months to solve the problem. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            On average, it took <strong>{female_5['time'].iloc[0]:.1f}</strong> months to solve the problem. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_5['financial_diff'].iloc[0]*100:.2f}</strong>% said that it was difficult or nearly impossible to find the money required to solve the problem. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_5['financial_diff'].iloc[0]*100:.2f}</strong>% said that it was difficult or nearly impossible to find the money required to solve the problem. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_5['slow'].iloc[0]*100:.2f}</strong>% said that the process was slow. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_5['slow'].iloc[0]*100:.2f}</strong>% said that the process was slow. 
                        </td>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{male_5['expensive'].iloc[0]*100:.2f}</strong>% said that the process was expensive. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{female_5['expensive'].iloc[0]*100:.2f}</strong>% said that the process was expensive. 
                        </td>
                    </tr>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 6. HARDSHIP
        st.markdown(
            """
            <h3 style='text-align: center;'>
                6. Hardship
            </h3>""",
            unsafe_allow_html=True)
        
        hardship = pd.melt(
            section6,
            id_vars=['country_name_ltn', 'demographic'],
            value_vars = ['any_hardship', 'health', 'interpersonal', 'economic', 'drugs'],
            var_name='Type of Hardship',
            value_name = 'value2plot'
        )
        female_6 = hardship[hardship['demographic'] == 'Female']
        male_6 = hardship[hardship['demographic'] == 'Male']

        fig5 = make_subplots(
            rows = 1, cols = 2,
            subplot_titles = ("Male Respondents", "Female Respondents"),
            shared_yaxes = True
        )

        fig5.add_trace(
            go.Bar(
                x = male_6['Type of Hardship'],
                y = male_6['value2plot']*100,
                marker_color = px.colors.qualitative.Plotly,
                showlegend = False,
                name = 'Male'
            ),
            row = 1, col = 1
        )
        

        fig5.add_trace(
            go.Bar(
                x = female_6['Type of Hardship'],
                y = female_6['value2plot']*100,
                marker_color = px.colors.qualitative.Plotly,
                showlegend = False,
                name = 'Female'
            ),
            row = 1, col = 2
        )

        fig5.update_traces(
            hovertemplate = '%{y:.2f}%'
        )

        fig5.update_layout(
        title=" ",
        xaxis_title="Type of Hardship",
        yaxis_title="Proportion of Respondents",
        template="plotly_white",
        font=dict(size=14),
        yaxis=dict(range=(0, 100))  # Fix y-axis range
        )

        # Update axis titles for each panel
        fig5.update_xaxes(title_text="Type of Hardship", row=1, col=1)
        fig5.update_xaxes(title_text="Type of Hardship", row=1, col=2)
        fig5.update_yaxes(title_text="Proportion of Respondents", row=1, col=1)

        st.plotly_chart(fig5)


    #####################################################################################################################
    #                                           DASHBOARD - INCOME DISAGGREGATION                                       #
    #####################################################################################################################

    if demographic == 'Disagreggated by Income':
        if country != 'European Union':
            prevalence_lowes = (section1.loc[(section1['country_name_ltn'] == country) & (section1['demographic'] == 'Financially Tight')]['total_count'].sum()) / (section1.loc[(section1['country_name_ltn'] == country) & (section1['demographic'] == 'Financially Tight')]['total_incidents'].mean())
            prevalence_highes = (section1.loc[(section1['country_name_ltn'] == country) & (section1['demographic'] == 'Financially Stable')]['total_count'].sum()) / (section1.loc[(section1['country_name_ltn'] == country) & (section1['demographic'] == 'Financially Stable')]['total_incidents'].mean())

        if country == 'European Union':
            prevalence_lowes = ((section1.loc[section1['demographic'] == 'Financially Tight']['total_count'].sum()) / (section1.loc[section1['demographic'] == 'Financially Tight']['total_incidents'].mean())).mean()
            prevalence_highes = ((section1.loc[section1['demographic'] == 'Financially Stable']['total_count'].sum()) / (section1.loc[section1['demographic'] == 'Financially Stable']['total_incidents'].mean())).mean()

        # 1. LEGAL PROCESS
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                1. Legal Process
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Tight</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Stable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{prevalence_lowes*100:.2f}</strong>% experienced a non-trivial legal problem in the last two years.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{prevalence_highes*100:.2f}</strong>% experienced a non-trivial legal problem in the last two years.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        lowes_1 = section1[section1['demographic'] == 'Financially Tight']
        highes_1 = section1[section1['demographic'] == 'Financially Stable']

        fig = make_subplots(
            rows=1, cols=2,  # One row, two columns
            subplot_titles=("Financially Tight", "Financially Stable"),
            shared_yaxes=True,  # Share the y-axis for better comparison
        )

        fig.add_trace(
            go.Scatter(
                x=lowes_1['value2plot'],
                y=lowes_1['category'],
                mode='markers',
                marker=dict(color='#B33C86'),
                name='Tight',
            ),
            row=1, col=1  # First panel
        )

        for _, row in lowes_1.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[0, row['value2plot']],
                    y=[row['category'], row['category']],
                    mode='lines',
                    line=dict(color='#B33C86', width=2),
                    showlegend=False,
                ),
                row=1, col=1,
            )

        fig.add_trace(
            go.Scatter(
                x=highes_1['value2plot'],
                y=highes_1['category'],
                mode='markers',
                marker=dict(color='#1C7C54'),
                name='Stable'
            ),
            row=1, col=2  # Second panel
        )

        fig.update_layout(xaxis = dict(range = (0,100)))

        for _, row in highes_1.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[0, row['value2plot']],
                    y=[row['category'], row['category']],
                    mode='lines',
                    line=dict(color='#1C7C54', width=2),
                    showlegend=False
                ),
                row=1, col=2,
            )
        fig.update_traces(
            hovertemplate = 'Category: %{y} <br> Value: %{x:.2f}%'
        )
        fig.update_layout(xaxis = dict(range = (0,100)),
                        xaxis2 = dict(range = (0,100)))

        fig.update_layout(
            title="Legal Process by Economic Status",
            xaxis_title="Percentage of Respondents",
            yaxis_title="Type of Problem",
            template="plotly_white",
            height=600,
            width=800,
            showlegend=False,
            xaxis = dict(range = (0,100))
        )


        fig.update_xaxes(title_text="Percentage of Respondents", row=1, col=1)
        fig.update_xaxes(title_text="Percentage of Respondents", row=1, col=2)
        fig.update_yaxes(title_text="Type of Problem", row=1, col=1)

        st.plotly_chart(fig)

        lowes_2 = section2[section2['demographic'] == 'Financially Tight']
        highes_2 = section2[section2['demographic'] == 'Financially Stable']

        get_info_lowes = lowes_2['get_information'].iloc[0]*100
        get_info_highes = highes_2['get_information'].iloc[0]*100
        get_expert_lowes = lowes_2['get_expert'].iloc[0]*100
        get_expert_highes = highes_2['get_expert'].iloc[0]*100
        confidence_lowes = lowes_2['confidence'].iloc[0]*100
        confidence_highes = highes_2['confidence'].iloc[0]*100

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)
        
        # 2. LEGAL CAPABILITY
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                2. Legal Capability
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Tight</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Stable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{get_info_lowes:.2f}</strong>% knew where to get advice and information.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_info_highes:.2f}</strong>% knew where to get advice and information.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_expert_lowes:.2f}</strong>% felt that they could get all of the expert help they needed.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{get_expert_highes:.2f}</strong>% felt that they could get all of the expert help they needed.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{confidence_lowes:.2f}</strong>% were confident that they could achieve a fair outcome. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{confidence_highes:.2f}</strong>% were confident that they could achieve a fair outcome. 
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)

        # 3. SOURCES OF HELP
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                3. Sources of Help
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Tight</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Stable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_2['advice'].iloc[0]*100:.2f}</strong>% were able to access help for their issue.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_2['advice'].iloc[0]*100:.2f}</strong>% were able to access help for their issue.
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        # advisors - gender
        lowes_3 = section3[section3['demographic'] == 'Financially Tight']
        highes_3 = section3[section3['demographic'] == 'Financially Stable']

        adviser_mapping = {
        'AJD_adviser_1': 'Relatives and friends',
        'AJD_adviser_2': 'Lawyer or professional adviser',
        'AJD_adviser_3': 'Government legal aid',
        'AJD_adviser_4': 'Court, govt, police',
        'AJD_adviser_5': 'Health or welfare adviser',
        'AJD_adviser_6': 'Trade union or employer',
        'AJD_adviser_7': 'Religious or community advisor',
        'AJD_adviser_8': 'Civil society or charity',
        'AJD_adviser_9': 'Other organization advisor',
    }
        lowes_3['adviser_name'] = lowes_3['adviser'].map(adviser_mapping)
        highes_3['adviser_name'] = highes_3['adviser'].map(adviser_mapping)

        section3['adviser_name'] = section3['adviser'].map(adviser_mapping)

        link_colors = section3['demographic'].map({'Financially Tight': 'orange', 'Financially Stable': 'blue'})
        
        fig_3b = make_subplots(
        rows=1, cols=2,  # Two horizontal panels
        subplot_titles=("Financially Tight", "Financially Stable"),
        specs=[[{"type": "sankey"}, {"type": "sankey"}]]
        )
        fig_3b.add_trace(
            go.Sankey(
                node=dict(
                    pad=15, thickness=20, line=dict(color="black", width=0.5),
                    label=lowes_3['adviser_name'].tolist() + ["Total"]
                ),
                link=dict(
                    source=list(range(len(lowes_3))),
                    target=[len(lowes_3)] * len(lowes_3),
                    value=(lowes_3["value2plot"]*100).tolist(),
                    color=["#CBC3E3"] * len(lowes_3),
                    customdata = lowes_3['adviser_name'],
                    hovertemplate='Advisor: %{customdata}<br>Value: %{value:.2f}%<extra></extra>'
                )
            ),
            row=1, col=1
        )

        fig_3b.add_trace(
            go.Sankey(
                node=dict(
                    pad=15, thickness=20, line=dict(color="black", width=0.5),
                    label=highes_3['adviser_name'].tolist() + ["Total"]
                ),
                link=dict(
                    source=list(range(len(highes_3))),
                    target=[len(highes_3)] * len(highes_3),
                    value=(highes_3["value2plot"]*100).tolist(),
                    color=["#90EE90"] * len(highes_3),
                    customdata = highes_3['adviser_name'],
                    hovertemplate='Advisor: %{customdata}<br>Value: %{value:.2f}%<extra></extra>'
                )
            ),
            row=1, col=2
        )

        # Update layout
        fig_3b.update_layout(
            title_text="Advisor Distribution by Economic Status",
            font_size=12,
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig_3b)


        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        # 4. STATUS
        lowes_4 = section4[section4['demographic'] == 'Financially Tight']
        highes_4 = section4[section4['demographic'] == 'Financially Stable']

        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                4. Status
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Tight</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Stable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_4['fully_resolved'].iloc[0]*100:.2f}</strong>% were able to fully resolve the issue. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_4['fully_resolved'].iloc[0]*100:.2f}</strong>% were able to fully resolve the issue. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{lowes_4['problem_persists'].iloc[0]*100:.2f}</strong>% gave up any action to solve the problem further.
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_4['problem_persists'].iloc[0]*100:.2f}</strong>% gave up any action to solve the problem further.
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{lowes_4['satisfaction'].iloc[0]*100:.2f}</strong>% were satisfied with the outcome of the resolution. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_4['satisfaction'].iloc[0]*100:.2f}</strong>% were satisfied with the outcome of the resolution. 
                        </td>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True)

    # PROCESS
        lowes_5 = section5[section5['demographic'] == 'Financially Tight']
        highes_5 = section5[section5['demographic'] == 'Financially Stable']
        st.markdown(
            f"""
            <h3 style='text-align: center;'>
                5. Process
            </h3>
            <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Tight</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Financially Stable</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_5['fair'].iloc[0]*100:.2f}</strong>% said that the process was fair. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_5['fair'].iloc[0]*100:.2f}</strong>% said that the process was fair. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            On average, it took <strong>{lowes_5['time'].iloc[0]:.1f}</strong> months to solve the problem. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            On average, it took <strong>{highes_5['time'].iloc[0]:.1f}</strong> months to solve the problem. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_5['financial_diff'].iloc[0]*100:.2f}</strong>% said that it was difficult or nearly impossible to find the money required to solve the problem. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_5['financial_diff'].iloc[0]*100:.2f}</strong>% said that it was difficult or nearly impossible to find the money required to solve the problem. 
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_5['slow'].iloc[0]*100:.2f}</strong>% said that the process was slow. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_5['slow'].iloc[0]*100:.2f}</strong>% said that the process was slow. 
                        </td>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;"> 
                            <strong>{lowes_5['expensive'].iloc[0]*100:.2f}</strong>% said that the process was expensive. 
                        </td>
                        <td style="border: 1px solid #ddd; padding: 8px; color:#003249;">
                            <strong>{highes_5['expensive'].iloc[0]*100:.2f}</strong>% said that the process was expensive. 
                        </td>
                    </tr>
                    </tr>
                </tbody>
            </table>
            """,
            unsafe_allow_html=True
        )
        # hardship - gender
        st.markdown(
            """
            <div style="font-size: 40px; color: #003249; text-align: center">&#x2193;</div> <!-- Downward arrow -->
            </div>""",
        unsafe_allow_html=True
        )

        st.markdown(
            """
            <h3 style='text-align: center;'>
                6. Hardship
            </h3>""",
            unsafe_allow_html=True)
        
        hardship = pd.melt(
            section6,
            id_vars=['country_name_ltn', 'demographic'],
            value_vars = ['any_hardship', 'health', 'interpersonal', 'economic', 'drugs'],
            var_name='Type of Hardship',
            value_name = 'value2plot'
        )
        lowes_6 = hardship[hardship['demographic'] == 'Financially Tight']
        highes_6 = hardship[hardship['demographic'] == 'Financially Stable']

        fig5 = make_subplots(
            rows = 1, cols = 2,
            subplot_titles = ("Financially Tight Respondents", "Financially Stable Respondents"),
            shared_yaxes = True
        )

        fig5.add_trace(
            go.Bar(
                x = lowes_6['Type of Hardship'],
                y = lowes_6['value2plot']*100,
                marker_color = px.colors.qualitative.Plotly,
                showlegend = False,
                name = 'Tight'
            ),
            row = 1, col = 1
        )
        

        fig5.add_trace(
            go.Bar(
                x = highes_6['Type of Hardship'],
                y = highes_6['value2plot']*100,
                marker_color = px.colors.qualitative.Plotly,
                showlegend = False,
                name = 'Stable'
            ),
            row = 1, col = 2
        )

        fig5.update_traces(
            hovertemplate = '%{y:.2f}%'
        )

        fig5.update_layout(
        title=" ",
        xaxis_title="Type of Hardship",
        yaxis_title="Proportion of Respondents",
        template="plotly_white",
        font=dict(size=14),
        yaxis=dict(range=(0, 100))  # Fix y-axis range
        )

        # Update axis titles for each panel
        fig5.update_xaxes(title_text="Type of Hardship", row=1, col=1)
        fig5.update_xaxes(title_text="Type of Hardship", row=1, col=2)
        fig5.update_yaxes(title_text="Proportion of Respondents", row=1, col=1)

        st.plotly_chart(fig5)
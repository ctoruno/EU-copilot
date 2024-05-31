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
import geopandas as gpd
import streamlit as st
import plotly.express as px
from tools import viz_tools as viz
from tools import passcheck

if passcheck.check_password():

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
    eutab, countrytab, vartab, czechia_tab = st.tabs(["EU Overview", "Country Profile", "Indicator Level", "Czechia"])

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

        country_data = pd.merge(
            (
                data_points.copy()
                .loc[data_points["level"] == "national"]
            ),
            (
                outline[["chapter", "section", "subsection", "n", "reportValues", "direction", "title", "subtitle"]]
            ),
            how = "left",
            left_on  = "chart",
            right_on = "n"
        )
        country_data["value_realign"] = country_data.apply(lambda row: pd.Series(realign_data(
                    row["value2plot"], 
                    row["direction"], 
                )), axis = 1)

        # Content
        color_codes   = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
        value_breaks  = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        color_palette = [[color, value] for color, value in zip(value_breaks, color_codes)]
        
        st.markdown(
            f"""
            <h4>How's the region performing?</h4>
            <p class='jtext'>
                In a nutshell, the data collected in the European Union indicates that the region is 
                performing quite well in the following four thematic topics (sub-sections):
            </p>
            """, 
            unsafe_allow_html=True
        )
        col = st.columns(2)
        for metric in [0, 1]:
            with col[metric]:
                viz.genMetrics(metric, df = subsection_summary, d = "green")
        col = st.columns(2)
        for metric in [2, 3]:
            with col[metric-2]:
                viz.genMetrics(metric, df = subsection_summary, d = "green")
        st.markdown(
            f"""
            <p class='jtext'>
                On the other hand, the data also indicates that the region is performing quite low in 
                the following four topics (sub-sections): 
            </p>
            """, 
            unsafe_allow_html=True
        )
        col = st.columns(2)
        for metric in [-1, -2]:
            with col[abs(metric)-1]:
                viz.genMetrics(metric, df = subsection_summary, d = "red")
        col = st.columns(2)
        for metric in [-3, -4]:
            with col[abs(metric)-3]:
                viz.genMetrics(metric, df = subsection_summary, d = "red")
        with st.expander("Technical note here"):
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
                            Regional (EU) values were grouped into thematic groups (topics) and the average percentages
                            within each groups are the ones shown above.
                        </li>
                    </ol>
                </p>
                <p class='jtext'>
                    Additionally, the indicators were re-aligned so higher values have a positive impact in the 
                    Rule of Law, while lower values reflect negative impacts on the Rule of Law. You can take a 
                    look at the full list of results in the table below:
                </p>
                """, 
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
            <p class='jtext'>
                You can take a look at the full list of results in the table below:
            </p>
            """, 
            unsafe_allow_html=True
        )
        with st.expander("Click here to see table of results"):
            st.dataframe(subsection_summary.to_records(index=False))
        st.markdown(
            f"""
            <h4>What about specific indicators?</h4>
            <p class='jtext'>
                Regardless of their associated topic, there is a handful of indicators in which the region, 
                on average, is showing a top performance:
            </p>
            <h4 style='text-align: left;'>Top 15 Indicators in the Region</h4>
            """, 
            unsafe_allow_html=True
        )
        top_15 = viz.genBars(
            data  = eu_data.head(15).sort_values(by = "value_realign", ascending = True), 
            cpal  = color_palette,
            level = "EU"
        )
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
            <p class='jtext'>
                Similarly, there is a set of indicators in which the region shows very low averages, most of 
                them related to the topics highlighted above:
            </p>
            <h4 style='text-align: left;'>Bottom 15 Indicators in the Region</h4>
            """, 
            unsafe_allow_html=True
        )
        bot_15 = viz.genBars(
            data  = eu_data.tail(15).sort_values(by = "value_realign", ascending = True),  
            cpal  = color_palette,
            level = "EU"
        )
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
        st.markdown(
            f"""
            <p class='jtext'>
                You can take a look at the complete list of topics and their respective average percentages
                in the table below:
            </p>
            """, 
            unsafe_allow_html=True
        )
        st.dataframe(
            eu_data[["country_name_ltn", "subsection", "title", "value2plot", "direction", "value_realign", "reportValues"]]
            .sort_values("value_realign")
            .to_records(index=False)
        )
        st.markdown(
            f"""
            <h4>Do specific results deviate a lot from these averages?</h4>
            <p class='jtext'>
                Yes, they do. To be more specific, looking at the average performance of the region is not recommended because 
                indicators present some important variation across countries and, more importantly, even across
                indicators associated to the same topics (sub-section).
            </p>
            <p class='jtext'>
                Below, I'm presenting the comparison between Denmark and Hungary across all topics covered in
                our Report. There is a clear difference between the performance of both countries in topics such as Freedom of 
                Expression and Judicial Independence. However, if we take a look at the indicators within the 
                Perceptions on the Accesibility of Civil Justice, Denmark alone has some quite variation. From only a 27% of
                the sample agreeing that there is access to affordable DRM to more than 60% agreeing that the Danish Civil Justice
                provides an equal and fair treatment.
            </p>
            <p class='jtext'>
                Feel free to play with the data below. Don't forget that individual indicators have been re-aligned to higher
                values are positive outcomes for the Rule of Law in a country, while lower values are associated to negative
                perceptions of the Rule of Law.
            </p>
            """, 
            unsafe_allow_html=True
        )
        country_select = st.multiselect(
            "Please select a country(-ies) from the list below:",
            (
                data_points
                .loc[data_points["level"] == "national"]
                .drop_duplicates(subset = "country_name_ltn")
                .country_name_ltn.to_list()
            ),
            default = ["Denmark", "Hungary"]
        )
        topic_focused = st.multiselect(
            "(Optional) Let's narrow the data to the following topics:",
            (
                country_data
                .loc[country_data["level"] == "national"]
                .drop_duplicates(subset = "subsection")
                .subsection.to_list()
            )
        )
        if len(topic_focused) > 0:
            country_data = (
                country_data.loc[country_data["subsection"].isin(topic_focused)]
            ) 
        bees = viz.genBees(country_data = country_data, country_select = country_select)
        st.plotly_chart(bees, config = {"displayModeBar": False})

    with countrytab:
        st.markdown("COMING SOON")

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
        map_tab, bars_tab, table_tab, lab_tab = st.tabs(["Sub-national Summary", "National Synopsis", "Detail", "Cross Lab"])

        direction    = outline.loc[outline["n"] == chart_n].direction.iloc[0]
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
            map = viz.genMap(data4map = data4map, eu_nuts  = eu_nuts, color_palette = color_palette)
            st.plotly_chart(map, use_container_width = True)
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

        with bars_tab:
            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title} (Country level)</h4>
                <h6 style='text-align: left;'><i>{subtitle}</i></h6>
                <p style='text-align: right;'><i>Reported values: {reportV}</i></p>
                """, 
                unsafe_allow_html=True
            )
            bars = viz.genBars(data = data4bars, cpal = color_palette, level = "indicator")
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

    with lab_tab:
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
        chapter_lab = st.selectbox(
            "Please select a thematic chapter from the list below",
            (outline
            .drop_duplicates(subset = "chapter")
            .chapter.to_list()),
            key = "chapter_lab"
        )
        section_lab = st.selectbox(
            "Please select a thematic section from the list below",
            (outline
            .loc[outline["chapter"] == chapter_lab]
            .drop_duplicates(subset = "section")
            .section.to_list()),
            key = "section_lab"
        )
        chart_lab = st.selectbox(
            "Please select a graph from the list below",
            (outline
            .loc[(outline["section"] == section_lab) & (outline["n"] != chart_n)]
            .drop_duplicates(subset = "title")
            .title.to_list()),
            key = "chart_lab"
        )

        # Subsetting and preparing data
        chart_n_lab = outline.loc[outline["title"] == chart_lab, "n"].iloc[0]
        n4lab = [chart_n, chart_n_lab]
        data4lab = (
            data_points.copy()
            .loc[(data_points["chart"].isin(n4lab)) & (data_points["level"] == "regional")]
        )
        data4lab["chart"] = data4lab["chart"].map({chart_n: "xaxis", chart_n_lab: "yaxis"})
        data4lab  = data4lab.pivot(
                index   = ["country_name_ltn", "nuts_id", "nameSHORT"],
                columns = "chart",
                values  = "value2plot"
            ).reset_index()

        # Defining Annotations
        title_lab    = outline.loc[outline["n"] == chart_n_lab].title.str.replace(r"Graph \d+\. ", "", regex=True).iloc[0]
        subtitle_lab = outline.loc[outline["n"] == chart_n_lab].subtitle.iloc[0]
        reportV_lab  = outline.loc[outline["n"] == chart_n_lab].reportValues.iloc[0]

        st.markdown(
            f"""
            <p class='jtext'>
                You have successfully selected <strong style="color:#003249">{title_xaxis}</strong> to be 
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
                <p style='text-align: left;'><i>Reported values: {reportV}</i></p>
                """, 
                unsafe_allow_html=True
            )
        with st.expander("Click here for more information on your COMPARISON variable"):
            st.markdown(
                f"""
                <h4 style='text-align: left;'>{title_lab} (Regional level)</h4>
                <h6 style='text-align: left;'><i>{subtitle_lab}</i></h6>
                <p style='text-align: left;'><i>Reported values: {reportV_lab}</i></p>
                """, 
                unsafe_allow_html=True
            )

    with czechia_tab:
        st.markdown(
            f"""
            <h3 style='text-align: left;'>
                Does the regional grouping in Czechia affect the main findings?
            </h3>
            <p class='jtext'>
                This tab is specially dedicated to answer that question. Here you can compare the data points for 
                different grouping options and see how much do the resulting data points change. Take into account that
                the resulng regions are not comparable across grouping options. Therefore, you need to focus on how much
                do the distribution of data points change between options. 
            </p>
            <p class='jtext'>
                You can also visualize the deviations from the national average. Given that the national average is fixed,
                no matter which grouping option are you working, the deviations will give a different approach to answer
                the question by using a fixed benchmark.
            </p>
            <h5 style='text-align: left;'>
                Summary
            </h5>
            <ul>
                <li>
                    <p class='jtext'>
                    Option 2 is slightly more efficient in reducing heterogeneity across regions. In other words, it reduces 
                    the regional differences across topics. Option 1 is also a good alternative if we do not want to inflate 
                    the regional differences. The "reduced" differences across regions seems to be common in the options where 
                    all regions have at least 500 observations.
                </p>
                </li>
                <li>
                    <p class='jtext'>
                        Option 5 is the option that produces the highest differences across regions. However, as mentioned above, 
                        these differences would not affect the overall findings across thematic topics. Leaving Prague as a sole 
                        region shows higher values for trust of authority figures, perception of corruption in institutions, and 
                        other variables. This "amplified" differences could be due to higher SES and Urban levels, but also because 
                        of the reduced sample for Prague (only 250 people).
                    </p>
                </li>
                <li>
                    <p class='jtext'>
                        Option 3 and 4 show very marginal differences in the results.
                    </p>
                </li>
            </ul>
            <p class='jtext'>
                Finally, we would like to warn about the potential sampling issues for choosing a grouping option in which a region is left alone. In this specific scenario, we would be dealing with a total sample size of 250 respondents for that region, which is even lower than the total samples that we have for some Caribbean countries. This would be a total sample of only 125 respondents for questions in which the questionnaire is split into two sub-groups: Civic Participation and Institutional Performance modules.
            </p>
            <p class='jtext'>
                <b>At this point, our preference would be using Option 1 for grouping sub-national regions.</b>
            </p>
            """, 
            unsafe_allow_html=True
        )

        with st.expander("Click here to see the detail of current options"):
            st.markdown(
                f"""
                <p class='jtext'>
                    Available options:
                </p>
                <ul>
                    <li>
                        <b>T1</b>: Based on geography/population:
                        <ul>
                            <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
                            <li>CZ03 (Southwest) + CZ04 (Northwest)</li>
                            <li>CZ05 (Northeast) + CZ06 (Southeast)</li>
                            <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
                        </ul>
                    </li>
                    <br>
                    <li>
                        <b>T2</b>: Based on geography/population:
                        <ul>
                            <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
                            <li>CZ03 (Southwest) + CZ06 (Southeast)</li>
                            <li>CZ04 (Northwest) + CZ05 (Northeast)</li>
                            <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
                        </ul>
                    </li>
                    <br>
                    <li>
                        <b>T3</b>: Based on cultural divisions:
                        <ul>
                            <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
                            <li>CZ03 (Southwest) + CZ04 (Northwest) + CZ05 (Northeast)</li>
                            <li>CZ06 (Southeast) + CZ07 (Central Moravia)</li>
                            <li>CZ08 (Moravian-Silesian)</li>
                        </ul>
                    </li>
                    <br>
                    <li>
                        <b>T4</b>: Based on cultural divisions:
                        <ul>
                            <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
                            <li>CZ03 (Southwest) + CZ04 (Northwest) + CZ05 (Northeast)</li>
                            <li>CZ06 (Southeast)</li>
                            <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
                        </ul>
                    </li>
                    <br>
                    <li>
                        <b>T5</b>: Based on both geographic and cultural features:
                        <ul>
                            <li>CZ01 (Prague)</li>
                            <li>CZ02 (Central Bohemia) + CZ03 (Southwest) + CZ04 (Northwest)</li>
                            <li>CZ05 (Northeast) + CZ06 (Southeast)</li>
                            <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
                        </ul>
                    </li>
                </ul>
                <br>
                """, 
                unsafe_allow_html=True
            )

        topics = [
            "Trust", "Corruption Perceptions", "Justice System Evaluation", "Law Enforcement Performance",
            "Criminal Justice Performance", "Perceptions on Authoritarian Behavior", "Civic Participation A", 
            "Civic Participation B", "Corruption Perceptions"
        ]

        groupings = st.multiselect(
            "Which grouping options do you want to visualize and compare",
            ["T1", "T2", "T3", "T4", "T5"],
            default = ["T1", "T5"],
            max_selections = 2
        )
        stat = st.selectbox(
            "What statistic would you like to visualize?",
            ["Data Points", "Deviations from National Average"],
            index = 0
        )

        czechia_data = pd.merge(
            pd.read_csv("inputs/cpoints.csv"),
            outline[["n", "topic", "reportValues", "title", "subtitle", "direction"]],
            how      = "left",
            left_on  = "chart",
            right_on = "n"
        )
        czechia_data = czechia_data[czechia_data["topic"].isin(topics)]
        czechia_data["title"] = czechia_data["title"].str.replace(r"^Graph \d+\. ", "", regex=True)
        czechia_data["grouping"] = czechia_data["region"].str[:2]

        for topic in topics:
            with st.empty():
                st.markdown(
                    f"""
                    <h3 style='text-align: left;'>{topic}</h3>
                    """, 
                    unsafe_allow_html=True
                )
                dotties = viz.genDotties(
                    data = czechia_data, 
                    topic = topic, 
                    groupings = groupings, 
                    stat = stat
                )
                st.plotly_chart(dotties, use_container_width = True)

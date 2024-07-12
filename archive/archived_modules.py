# Content EU TAB
    # color_codes   = ["#E03849", "#FF7900", "#FFC818", "#46B5FF", "#0C75B6", "#18538E"]
    # value_breaks  = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
    # color_palette = [[color, value] for color, value in zip(value_breaks, color_codes)]
    
    # st.markdown(
    #     f"""
    #     <h4>How's the region performing?</h4>
    #     <p class='jtext'>
    #         In a nutshell, the data collected in the European Union indicates that the region is 
    #         performing quite well in the following four thematic topics (sub-sections):
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # col = st.columns(2)
    # for metric in [0, 1]:
    #     with col[metric]:
    #         viz.genMetrics(metric, df = subsection_summary, d = "green")
    # col = st.columns(2)
    # for metric in [2, 3]:
    #     with col[metric-2]:
    #         viz.genMetrics(metric, df = subsection_summary, d = "green")
    # st.markdown(
    #     f"""
    #     <p class='jtext'>
    #         On the other hand, the data also indicates that the region is performing quite low in 
    #         the following four topics (sub-sections): 
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # col = st.columns(2)
    # for metric in [-1, -2]:
    #     with col[abs(metric)-1]:
    #         viz.genMetrics(metric, df = subsection_summary, d = "red")
    # col = st.columns(2)
    # for metric in [-3, -4]:
    #     with col[abs(metric)-3]:
    #         viz.genMetrics(metric, df = subsection_summary, d = "red")
    # with st.expander("Technical note here"):
    #     st.markdown(
    #         f"""
    #         <p class='jtext'>
    #             To arrive to the values shown above, the following steps were taken:
    #             <ol>
    #                 <li>
    #                     The responses for individual respondents were aggregated using simple averages to
    #                     get a sub-national average for individual indicators.
    #                 </li>
    #                 <li>
    #                     Sub-national values were aggregated to get a national average. The total population of
    #                     each region was used as a weight during this step.
    #                 </li>
    #                 <li>
    #                     National values were aggregated to get a regional (EU) average using a simple mean.
    #                 </li>
    #                 <li>
    #                     Regional (EU) values were grouped into thematic groups (topics) and the average percentages
    #                     within each groups are the ones shown above.
    #                 </li>
    #             </ol>
    #         </p>
    #         <p class='jtext'>
    #             Additionally, the indicators were re-aligned so higher values have a positive impact in the 
    #             Rule of Law, while lower values reflect negative impacts on the Rule of Law. You can take a 
    #             look at the full list of results in the table below:
    #         </p>
    #         """, 
    #         unsafe_allow_html=True
    #     )
    # st.markdown(
    #     f"""
    #     <p class='jtext'>
    #         You can take a look at the full list of results in the table below:
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # with st.expander("Click here to see table of results"):
    #     st.dataframe(subsection_summary.to_records(index=False))
    # st.markdown(
    #     f"""
    #     <h4>What about specific indicators?</h4>
    #     <p class='jtext'>
    #         Regardless of their associated topic, there is a handful of indicators in which the region, 
    #         on average, is showing a top performance:
    #     </p>
    #     <h4 style='text-align: left;'>Top 15 Indicators in the Region</h4>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # top_15 = viz.genBars(
    #     data  = eu_data.head(15).sort_values(by = "value_realign", ascending = True), 
    #     cpal  = color_palette,
    #     level = "EU"
    # )
    # st.plotly_chart(top_15, config = {"displayModeBar": False})
    # st.markdown("---")
    # st.markdown(
    #     f"""
    #     <h6 style='text-align: left;'><i>Important Notes:</i></h6>
    #     <p class='footnote'>
    #         <i>
    #             Values were re-aligned so higher values have a positive impact in the Rule of Law,
    #             while lower values have a negative impact on the Rule of Law. Indicators corresponding 
    #             to the European Union were calculated as simple averages of the country indicators. 
    #             Country indicators were estimated as weighted averages of the subnational regions.
    #             For more information on what do the percentages represent for each indicator, please 
    #             consult the report outline or the <b>Indicator Level</b> tab in this dashboard.
    #         </i>
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # st.markdown("---")
    # st.markdown(
    #     f"""
    #     <p class='jtext'>
    #         Similarly, there is a set of indicators in which the region shows very low averages, most of 
    #         them related to the topics highlighted above:
    #     </p>
    #     <h4 style='text-align: left;'>Bottom 15 Indicators in the Region</h4>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # bot_15 = viz.genBars(
    #     data  = eu_data.tail(15).sort_values(by = "value_realign", ascending = True),  
    #     cpal  = color_palette,
    #     level = "EU"
    # )
    # st.plotly_chart(bot_15, config = {"displayModeBar": False})
    # st.markdown("---")
    # st.markdown(
    #     f"""
    #     <h6 style='text-align: left;'><i>Important Notes:</i></h6>
    #     <p class='footnote'>
    #         <i>
    #             Values were re-aligned so higher values have a positive impact in the Rule of Law,
    #             while lower values have a negative impact on the Rule of Law. Indicators corresponding 
    #             to the European Union were calculated as simple averages of the country indicators. 
    #             Country indicators were estimated as weighted averages of the subnational regions.
    #             For more information on what do the percentages represent for each indicator, please 
    #             consult the report outline or the <b>Indicator Level</b> tab in this dashboard.
    #         </i>
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # st.markdown("---")
    # st.markdown(
    #     f"""
    #     <p class='jtext'>
    #         You can take a look at the complete list of topics and their respective average percentages
    #         in the table below:
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # st.dataframe(
    #     eu_data[["country","nuts_id", "chapter", "section", "title", "value2plot", "direction", "value_realign", "reportValue"]]
    #     .sort_values("value_realign")
    #     .to_records(index=False)
    # )
    # st.markdown(
    #     f"""
    #     <h4>Do specific results deviate a lot from these averages?</h4>
    #     <p class='jtext'>
    #         Yes, they do. To be more specific, looking at the average performance of the region is not recommended because 
    #         indicators present some important variation across countries and, more importantly, even across
    #         indicators associated to the same topics (sub-section).
    #     </p>
    #     <p class='jtext'>
    #         Below, I'm presenting the comparison between Denmark and Hungary across all topics covered in
    #         our Report. There is a clear difference between the performance of both countries in topics such as Freedom of 
    #         Expression and Judicial Independence. However, if we take a look at the indicators within the 
    #         Perceptions on the Accesibility of Civil Justice, Denmark alone has some quite variation. From only a 27% of
    #         the sample agreeing that there is access to affordable DRM to more than 60% agreeing that the Danish Civil Justice
    #         provides an equal and fair treatment.
    #     </p>
    #     <p class='jtext'>
    #         Feel free to play with the data below. Don't forget that individual indicators have been re-aligned to higher
    #         values are positive outcomes for the Rule of Law in a country, while lower values are associated to negative
    #         perceptions of the Rule of Law.
    #     </p>
    #     """, 
    #     unsafe_allow_html=True
    # )
    # country_select = st.multiselect(
    #     "Please select a country(-ies) from the list below:",
    #     (
    #         data_points
    #         .loc[data_points["level"] == "national"]
    #         .drop_duplicates(subset = "country")
    #         .country.to_list()            ),
    #     default = ["Denmark", "Hungary"]
    # )
    # topic_focused = st.multiselect(
    #     "(Optional) Let's narrow the data to the following topics:",
    #     (
    #         country_data
    #         .loc[country_data["level"] == "national"]
    #         .drop_duplicates(subset = "section")
    #         .section.to_list()
    #     )
    # )
    # if len(topic_focused) > 0:
    #     country_data = (
    #         country_data.loc[country_data["section"].isin(topic_focused)]
    #     ) 
    # bees = viz.genBees(country_data = country_data, country_select = country_select)
    # st.plotly_chart(bees, config = {"displayModeBar": False})

# with czechia_tab:
    #     st.markdown(
    #         f"""
    #         <h3 style='text-align: left;'>
    #             Does the regional grouping in Czechia affect the main findings?
    #         </h3>
    #         <p class='jtext'>
    #             This tab is specially dedicated to answer that question. Here you can compare the data points for 
    #             different grouping options and see how much do the resulting data points change. Take into account that
    #             the resulng regions are not comparable across grouping options. Therefore, you need to focus on how much
    #             do the distribution of data points change between options. 
    #         </p>
    #         <p class='jtext'>
    #             You can also visualize the deviations from the national average. Given that the national average is fixed,
    #             no matter which grouping option are you working, the deviations will give a different approach to answer
    #             the question by using a fixed benchmark.
    #         </p>
    #         <h5 style='text-align: left;'>
    #             Summary
    #         </h5>
    #         <ul>
    #             <li>
    #                 <p class='jtext'>
    #                 Option 2 is slightly more efficient in reducing heterogeneity across regions. In other words, it reduces 
    #                 the regional differences across topics. Option 1 is also a good alternative if we do not want to inflate 
    #                 the regional differences. The "reduced" differences across regions seems to be common in the options where 
    #                 all regions have at least 500 observations.
    #             </p>
    #             </li>
    #             <li>
    #                 <p class='jtext'>
    #                     Option 5 is the option that produces the highest differences across regions. However, as mentioned above, 
    #                     these differences would not affect the overall findings across thematic topics. Leaving Prague as a sole 
    #                     region shows higher values for trust of authority figures, perception of corruption in institutions, and 
    #                     other variables. This "amplified" differences could be due to higher SES and Urban levels, but also because 
    #                     of the reduced sample for Prague (only 250 people).
    #                 </p>
    #             </li>
    #             <li>
    #                 <p class='jtext'>
    #                     Option 3 and 4 show very marginal differences in the results.
    #                 </p>
    #             </li>
    #         </ul>
    #         <p class='jtext'>
    #             Finally, we would like to warn about the potential sampling issues for choosing a grouping option in which a region is left alone. In this specific scenario, we would be dealing with a total sample size of 250 respondents for that region, which is even lower than the total samples that we have for some Caribbean countries. This would be a total sample of only 125 respondents for questions in which the questionnaire is split into two sub-groups: Civic Participation and Institutional Performance modules.
    #         </p>
    #         <p class='jtext'>
    #             <b>At this point, our preference would be using Option 1 for grouping sub-national regions.</b>
    #         </p>
    #         """, 
    #         unsafe_allow_html=True
    #     )

    #     with st.expander("Click here to see the detail of current options"):
    #         st.markdown(
    #             f"""
    #             <p class='jtext'>
    #                 Available options:
    #             </p>
    #             <ul>
    #                 <li>
    #                     <b>T1</b>: Based on geography/population:
    #                     <ul>
    #                         <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
    #                         <li>CZ03 (Southwest) + CZ04 (Northwest)</li>
    #                         <li>CZ05 (Northeast) + CZ06 (Southeast)</li>
    #                         <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
    #                     </ul>
    #                 </li>
    #                 <br>
    #                 <li>
    #                     <b>T2</b>: Based on geography/population:
    #                     <ul>
    #                         <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
    #                         <li>CZ03 (Southwest) + CZ06 (Southeast)</li>
    #                         <li>CZ04 (Northwest) + CZ05 (Northeast)</li>
    #                         <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
    #                     </ul>
    #                 </li>
    #                 <br>
    #                 <li>
    #                     <b>T3</b>: Based on cultural divisions:
    #                     <ul>
    #                         <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
    #                         <li>CZ03 (Southwest) + CZ04 (Northwest) + CZ05 (Northeast)</li>
    #                         <li>CZ06 (Southeast) + CZ07 (Central Moravia)</li>
    #                         <li>CZ08 (Moravian-Silesian)</li>
    #                     </ul>
    #                 </li>
    #                 <br>
    #                 <li>
    #                     <b>T4</b>: Based on cultural divisions:
    #                     <ul>
    #                         <li>CZ01 (Prague) + CZ02 (Central Bohemia)</li>
    #                         <li>CZ03 (Southwest) + CZ04 (Northwest) + CZ05 (Northeast)</li>
    #                         <li>CZ06 (Southeast)</li>
    #                         <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
    #                     </ul>
    #                 </li>
    #                 <br>
    #                 <li>
    #                     <b>T5</b>: Based on both geographic and cultural features:
    #                     <ul>
    #                         <li>CZ01 (Prague)</li>
    #                         <li>CZ02 (Central Bohemia) + CZ03 (Southwest) + CZ04 (Northwest)</li>
    #                         <li>CZ05 (Northeast) + CZ06 (Southeast)</li>
    #                         <li>CZ07 (Central Moravia) + CZ08 (Moravian-Silesian)</li>
    #                     </ul>
    #                 </li>
    #             </ul>
    #             <br>
    #             """, 
    #             unsafe_allow_html=True
    #         )

    #     topics = [
    #         "Trust", "Corruption Perceptions", "Justice System Evaluation", "Law Enforcement Performance",
    #         "Criminal Justice Performance", "Perceptions on Authoritarian Behavior", "Civic Participation A", 
    #         "Civic Participation B", "Corruption Perceptions"
    #     ]

    #     groupings = st.multiselect(
    #         "Which grouping options do you want to visualize and compare",
    #         ["T1", "T2", "T3", "T4", "T5"],
    #         default = ["T1", "T5"],
    #         max_selections = 2
    #     )
    #     stat = st.selectbox(
    #         "What statistic would you like to visualize?",
    #         ["Data Points", "Deviations from National Average"],
    #         index = 0
    #     )

    #     czechia_data = pd.merge(
    #         pd.read_csv("inputs/cpoints.csv"),
    #         outline[["n", "topic", "reportValues", "title", "subtitle", "direction"]],
    #         how      = "left",
    #         left_on  = "chart",
    #         right_on = "n"
    #     )
    #     czechia_data = czechia_data[czechia_data["topic"].isin(topics)]
    #     czechia_data["title"] = czechia_data["title"].str.replace(r"^Graph \d+\. ", "", regex=True)
    #     czechia_data["grouping"] = czechia_data["region"].str[:2]

    #     for topic in topics:
    #         with st.empty():
    #             st.markdown(
    #                 f"""
    #                 <h3 style='text-align: left;'>{topic}</h3>
    #                 """, 
    #                 unsafe_allow_html=True
    #             )
    #             dotties = viz.genDotties(
    #                 data = czechia_data, 
    #                 topic = topic, 
    #                 groupings = groupings, 
    #                 stat = stat
    #             )
    #             st.plotly_chart(dotties, use_container_width = True)

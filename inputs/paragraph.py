## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
##  Paragraph                                                                                      ----
##
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def paragraph(country):
  
  if country == "Austria":
    
    ## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Austria                                                                                        ----
    ## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    p=  """ 
      <b>Insights summary</b>
      <br>
      We are seeing that across time, a lot of pillars and subpillars are flagged. However, our previous data is from 2017, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we don't have any red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. 
      <br>
      <br>
      Given that we expect to see large changes from our previous data in Austria, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Austria. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis. In the case of Austria, all the changes over the time are supported by the TPS.
      <br>
      <br>
      <b> Sub Pillars to Research </b>
      <br>

      <li> We don't find any subpillar that needs extra research.
      </li>
      <br>
        """
  
  elif country == "Belgium":
    
    ## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ## Belgium                                                                                        ----
    ## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    p = """
            <b>Insights summary</b>
              <br>
              We are seeing that across time, a few pillars and subpillars are flagged. However, our previous data is from 2019, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have one red flag. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses.
            <br>
              <br>
              Given that we expect to see large changes from our previous data in Belgium, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Belgium. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
              <br>
              <b> Sub Pillars to Research </b>
              <br>
              <ul>
              <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.1: Legal Security</li>
              <ul>
              <li> When we asked if people know their rights when facing a legal problem, we found a score of 0.364, while the Fundamental Rights Survey gave a score of 0.737. Although these questions are not matched very well, it is still important to supplement the comparison with research on the accessibility to justice and legal information in Belgium. This differences are consistent across all the NUTS.           
              </li>
            </ul>
              </ul>
              </li>
              </li>
              <ul>
              <li>
              Negative trend in 7.2: People can acces quality legal assistance and representation
              </li>
              <ul>
              <li>
              When we asked if people  have access to affordable legal assistance and representation when they face a legal problem, we found a score of 0.473, while VDEM gave a score of 0.858. Although these questions are not matched very well, and VDEM is an expert survey, it is still important to supplement the comparison with research on the accessibility to justice and legal assistance in Belgium. This differences are consistent across all the NUTS.           
              </li>
              </ul>
              </ul>
              </ul>
              <ul>
              <li> Pillar 8. Criminal Justice
             <ul>
              <li> Negative trend in 8.7: Prisons </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.547, while Varieties of Democracy found a score of 0.909 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. </li>
            </ul>
            </ul>
            </li>
            </ul>
              </li>
              </ul>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """
  elif country == "Bulgaria":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, a few pillars are indicating changes. Most only have one or two indicators, however pillar 2 has 16 comparisons. Although many of these have red flags, some are positive changes while others are negative changes and overall encompass experience and opinion questions. In comparison to the TPS public opinion polls, we only have 2 red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, there are a few pillars flagged, however we are conscious that we trust these scores less. 
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Bulgaria, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Bulgaria Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.1: People feel safe</li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.664 when our previous score was 0.52. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. 
            </li>
            </ul>
            <li> Positive trend in 5.2: Absence of crime and violence </li>
            <ul>
            <li> When we asked if people were aware of organized crime occuring in their neighborhoods, we found a score of 0.935, while the average criminality score in the Organized Crime Index was 0.483. Although the comparison is from a low match, the concepts are still related and therefore we should give context about organized crime rates. </li>
            </ul>
            </ul>
            </li>
            </ul>
            All these discrepancies between the data are also consistent at the NUTS level; we observe that the significant differences persist across all NUTS regions for all sub-pillars flagged.
            <br>
            <br>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """
  elif country == "Croatia":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, a few pillars are indicating changes. Although many of these have red flags, some are positive changes while others are negative changes and overall encompass opinion questions. In comparison to the TPS public opinion polls, we have 0 red flags! This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, there are a few pillars flagged, however we are conscious that we trust these scores less. 
            <br>
            <br>
            Given that we do not expect to see large changes from our previous data in Croatia, we are noting sub pillars that are flagged in either the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Croatia. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 1. Constraints on Government Powers
            <ul>
            <li> Negative trend in 1.06:  Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism) </li>
            <ul>
            <li> When we asked if people agreed that emergency powers are utilized to circumvent institutional checks and balances, we found a score of 0.365 while Freedom in the World provided a score of 1 when asking if members of the executive respect the constitution. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match with an expert TPS, we recommend to give context about respect for checks and balances. 
            </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 5. Security
            <ul>
            <li> Negative trend in 5.1: People feel safe </li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.699 when our previous score was 0.734. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more negatively than before. This inconsistency is especially high in HR05:Grad Zagreb, so it would be ideal to proportionate some additional information about this region regarding security.</li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """
  elif country == "Cyprus":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, a few pillars are indicating changes. Most only have a few indicators, however pillar 2 has 16 comparisons. Although many of these have red flags, some are positive changes while others are negative changes and overall encompass experience and opinion questions. In comparison to the TPS public opinion polls, we only have 3 red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are mostly highlighting Pillar 8, however we are conscious that we trust these scores less.  Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we do not expect to see large changes from our previous data in Cyprus, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Cyprus. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 8. Criminal Justice
            <ul>
            <li> Negative trend in 8.6: Due process of law </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees a fair trial of all accused people, we found a score of 0.434, while Freedom in the World found a score of 1 when they asked if due process prevails in civil and criminal matters. Furthermore, when we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.481 while Freedom in the World assigned a score of 1 for the question regarding if due process prevails in civil and criminal matters. Although these questions have low matches, they are still related and should be complemented with research about the rights of the accused and due process.</li>
            </ul>
            <li> Negative trend in 8.7: Prisons</li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.45, while V-Dem found a score of 0.838 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. 
            </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Czechia":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, only Pillars 2 and 3 are flagged. However, our previous data is from 2017, and thus we do not expect nothing to have changed. Furthermore, in comparison to the TPS public opinion polls, we only have one indicator level red flag, and none of the Pillars or Sub-pillars are flagged. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging Sub-pillar 4.6 and all of the Sub-pillars in Pillars 7 and 8, however we are conscious that we trust these scores less. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Czechia, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Czechia, and all Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.2: People can access quality legal assistance and representation</li>
            <ul>
            <li> When we asked if individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we found a score of 0.445, while V-Dem found a score of 0.888 when they asked if women enjoy equal, secure, and effective access to justice and a score of 0.918 when they asked if men enjoy equal, secure, and effective access to justice. Although the questions have a low match, they are still related and should be complemented with research about effective access to justice. 
            </li>
            </ul>
            </ul>
            <li> Pillar 8. Criminal Justice
            <ul>
            <li> Negative trend in 8.7: Prisons</li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.515, while V-Dem found a score of 0.942 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. 
            </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """

  elif country == "Denmark":
    p = """<b>Insights summary</b>
              <br>
              We are seeing that across time, a lot pillars and subpillars are flagged. However, our previous data is from 2017, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have on red flag. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. 
            <br>
              <br>
              Given that we expect to see large changes from our previous data in Denmark, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Denmark. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <br>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.1: People feel safe</li>
              <ul>
              <li> When we asked if people feel safe walking in their neighborhood at night, we found an score of 0.754 which is higher than the previous score of 0.713. In this case the difference is not very big, so we propose to give some context about the security in Denmark.
            </li>
            </ul>
            </ul>
              <li> Pillar 7. Civil justice
              <ul>
              <li>
              Negative trend in 7.2: People can acces quality legal assistance and representation
              </li>
              <ul>
              <li>
              When we asked if people  have access to affordable legal assistance and representation when they face a legal problem, we found a score of 0.554, while VDEM gave a score of 1. Although these questions are not matched very well, and VDEM is an expert survey, it is still important to supplement the comparison with research on the accessibility to justice and legal assistance in Denmark. This differences are consistent across all the NUTS.           
              </li>
              </ul>
              </ul>
              </li>
              </ul>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
              """

  elif country == "Estonia":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, only Pillars 5 and 7 are flagged. However, our previous data is from 2017, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, have zero red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging Sub-pillars 4.5, 4.6, 7.2. 7.4, 8.3, and 8.6, however we are conscious that we trust these scores less and that all of these besides 7.2 have green flags in other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Estonia, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Estonia, and all Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.1: People feel safe</li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.685 when our previous score was 0.579. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. 
            </li>
            </ul>
            </ul>
            <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.2: People can access quality legal assistance and representation</li>
            <ul>
            <li> When we asked if individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we found a score of 0.362, while V-Dem found a score of 0.729 when they asked if women enjoy equal, secure, and effective access to justice and a score of 0.740 when they asked if men enjoy equal, secure, and effective access to justice. Although the questions have a low match, they are still related and should be complemented with research about effective access to justice. 
            </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """

  elif country == "Finland":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, only Pillars 5 and 7 are flagged. However, our previous data is from 2017, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we have zero red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging Sub-pillars 4.6, 7.4, 8.3, and 8.6, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Finland, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Finland. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.1: People feel safe</li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.713 when our previous score was 0.662. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. This red flag is consistent in all the NUTS regions besides FI1B, Helsinki-Uusimaa.
            </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """

  elif country == "France":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, a few pillars and subpillars are flagged. However, our previous data is from 2018, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have two red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in France, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of France. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.2: Absence of crime and violence</li>
            <ul>
            <li> When we asked if people know or have heard if organized crime happens in their community or neighborhood, we found a score of 0.863 while the Organized Crime Index gave a Criminality Average Score of 0.464. Although these questions are not matched very well, it is still imporant to supplement the comparison with research on organized crime in France.
            </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.1: Legal security</li>
            <ul>
            <li> When we asked if people are informed about their legal rights when dealing with legal issues, we found a score of 0.332 while the Fundamental Rights Survey found a score of 0.683 regarding views on authorities providing information for people in a simple way. Although these questions are not matched very well, it is still imporant to supplement the comparison with research on access to legal information in France.</li>
            </ul>
            </ul>
            </li>
            </ul>
            These discrepancies between the data are <b>NOT</b> consistent at the NUTS level; we observe that the significant differences occuring in some NUTS regions are causing the indicators to be flagged at the national level. There is a lot of heterogeneity between regions, and in subpillar 5.2, FRM/Corse is exceptionally low compared to the others. In 7.1 however, the difference between the regions with red flags and the regions with green flags is very small, each sitting very close to the 0.35 score difference threshold we implemented.
            <br>
            <br>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """

  elif country == "Germany":
    p = """<b>Insights Summary</b>
      <br>
       We see that, across time, sub-pillars 3.1, 3.2, 4.2, and 4.4 are flagged. Given that the previous GPP data from Germany is from 2018, we expect there to be significant difference. However, when observing the TPS public opinion polls, we find no flagged sub-pillars. This indicates that our data are consistent with other population surveys, which is a key objective. In terms of TPS expert surveys, we find flags in sub-pillars 1.03, 1.06, 4.6, 7.2, 7.4, 8.3, and 8.6, however we are conscious that we trust these scores less and several of these sub-pillars have green flags in other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
      <br>
      <br>
      Given that we expect to see large changes from our previous data in Germany, we are noting sub-pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Germany. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
      <br>
      <br>
      <b>Sub Pillars to Research</b>
      <ul>
      <li>Pillar 1. Constraints on Government Powers
      <ul>
      <li>Negative trend in 1.06: Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism)</li>
      <ul>
      <li>When we asked respondents whether emergency powers are utilized to circumvent institutional checks and balances, we received an agreement rate of 0.552. When our TPS Extert polling source, Varieties of Democracy, asked whether members of the executive (the head of state, the head of government, and cabinet ministers) respect the constitution, they found an agreement rate of 0.969. These questions are a low match, and this sub-pillar was not tested in any other analysis, so while it is flagged, it is not an especially clear discrepancy.</li>
      </ul>
      </ul>
      </li>
      <li>Pillar 7. Civil Justice
      <ul>
      <li>Negative trend in 7.2: People can access quality legal assistance and representation</li>
      <ul>
      <li>When we asked respondents whether individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we received a score of 0.523. However, in the TPS Expert polls, our source Varieties of Democracies asked whether men and women each enjoy secure and effective access to justice, they returned a score of 0.970 for men and 0.926 for women. It is worth noting that our question specifies affordability as an issue, whereas the TPS Expert polling does not. Because of the low question match, this is not an especially clear discrepancy. This sub-pillar was not tested in any other analysis.</li>
      </ul>
      </ul>
      </li>
      </ul>
            
      """

  elif country == "Greece":
    p = """<b>Insights summary</b>
            <br> 
            We see that, across time, sub-pillars 1.11, 3.1, 4.4, 8.1, and 8.5 are flagged. Given that the previous GPP data from Greece is from 2017, we expect there to be significant difference. However, when observing the TPS public opinion polls, we only find flags in sub-pillars 5.2 and 8.2. This indicates that our data are relatively consistent with other population surveys, which is a key objective. In terms of TPS expert surveys, we find flags in sub-pillars 1.06, 4.5, and 7.2, however we are conscious that we trust these scores less and prefer to rely on population polling as a comparative metric. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Greece, we are noting sub-pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Greece. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis. For Greece, all sub-pillars highlighted are ones which are flagged in the TPS polling, but not addressed in our GPP over time analysis.
            <br>
            <br>
            <b>Sub Pillars to Research </b>
            <ul>
            <li>Pillar 1. Constraints on Government Powers
            <ul>
            <li>Negative trend in 1.06: Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism)</li>
            <ul>
            <li>When we asked respondents whether emergency powers are utilized to circumvent institutional checks and balances, we received an agreement rate of 0.371. When our TPS Extert polling source, Varieties of Democracy, asked whether members of the executive (the head of state, the head of government, and cabinet ministers) respect the constitution, they found an agreement rate of 0.9878. These questions are a low match, and this sub-pillar was not tested in any other analysis, so while it is flagged, it is not an especially clear discrepancy.</li>
            <ul>
            <li>At the NUTS level, we found red flags in sub-pillar 1.06 for EL3: Attiki (0.363), EL4: Nisian Aigaiou, Kriti (0.365), EL5: Voreia Ellada (0.358), and EL6: Kentriki Ellada (0.401)</li>
            </ul>
            </ul>
            </ul>
            </li>
            <li>Pillar 5. Security
            <ul>
            <li>Positive trend in 5.2: Absence of crime and violence</li>
            <ul>
            <li>When we asked if people know or have heard if organized crime happens in their community or neighborhood, we found a score of 0.896 while the Organized Crime Index gave a Criminality Average Score of 0.517. Although these questions are not matched very well, it is still imporant to supplement the comparison with research on organized crime in Greece.</li>
            <ul>
            <li>At the NUTS level, we found red flags in sub-pillar 5.2 for EL3: Attiki (0.881), EL5: Voreia Ellada (0.998), and EL 6: Kentriki Ellada (0.930). One NUTS region returned a green flag, EL4: Nisia Aigaiou, Kriti, with a score of 0.778.</li>
            </ul>
            </ul>
            </ul>
            </li>
            <li>Pillar 7. Civil Justice
            <ul>
            <li>Negative trend in 7.2: People can access quality legal assistance and representation</li>
            <ul>
            <li>When we asked respondents whether individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we received a score of 0.349. However, in the TPS Expert polls, our source Varieties of Democracies asked whether men and women each enjoy secure and effective access to justice, they returned a score of 0.827 for men and 0.708 for women. It is worth noting that our question specifies affordability as an issue, whereas the TPS Expert polling does not. Because of the low question match, this is not an especially clear discrepancy. This sub-pillar was not tested in any other analysis.</li>
            <ul>
            <li>In this sub-pillar, our TPS analysis relies on Varieties of Democracy's polling on whether men and women enjoy secure and effective access to justice. These questions were asked separately, so different scores are generated for men's and women's access. At the NUTS level, we found red flags for men's access in EL3, EL4, EL5, and EL6. We found red flags for women's access in EL4 and EL6, whereas EL3 and EL5 returned green flags.</li>
            </ul>
            </ul>
            </li>
            </ul>
            </ul>
            <br>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Hungary":
    p = """ <b>Insights summary</b>
            <br>
            We are seeing that across time, all of the pillars in the GPP are changing. For the most part, these changes indicate more negative opinions about the rule of law with some positive trends in select sub pillars. Nevertheless, the result of these trends in terms of our full fieldwork data are similar to what other sources are observing. Therefore, according to our data, people in Hungary have a decreased view of the rule of law, which is in accordance with the third party source data.
            <br>
            <br>
            Given that we expect to see changes from our previous data in Hungary, we are noting sub pillars that are flagged in the TPS analyses. In this regard, all the topics that are flagged in the time comparisson but supported by green flags in the TPS are considered as something normal in the context of Hungary. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported in the TPS.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 4. Fundamental Rights
            <ul>
            <li> Negative trend in 4.4: Solidarity </li>
            <ul>
            <li> When we asked if people thought that workers’ freedom to form labor unions and negotiate with employers is important, we found a score of 0.46 when our previous score was 0.61. Additionaly, when we asked if working conditions are favorable, we found a score of 0.36 while the European Social Survey found a score of 0.74 in 2021. These large discrepancies should be investigated through context about both unionization and working conditions. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.1: Legal Security </li>
            <ul>
            <li> When we asked if people are aware of their rights when they face a legal problem we found an score of 0.34, while the Fundamental Rights Survey shows a score of 0.758 when they asked about the views on authorities providing information for people in a simple way. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match, we recommend to give a context about the knowledge of people about their rights when they faced a legal problem. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 8. Criminal Justice 
            <ul>
            <li> Negative trend in 8.7: Prisons </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.47, while Varieties of Democracy found a score of 0.835 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. </li>
            </ul>
            </ul>
            </li>
            </ul>
            All these discrepancies between the data are also consistent at the NUTS level; we observe that the significant differences persist across all NUTS regions for all sub-pillars flagged.
            <br>
            <br>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Ireland":
    p = """<b>Insights summary</b>
            <br>
            We see that, across time, sub-pillars 1.11 and 5.1 are flagged. Given that the previous GPP data from Ireland is from 2021, we may or may not expect there to be significant difference. However, when observing the TPS public opinion polls, we find no flagged sub-pillars. This indicates that our data are relatively consistent with other population surveys, which is a key objective. In terms of TPS expert surveys, we find flags in sub-pillars 1.03, 1.06, 4.5, 4.6, 7.2, 7.4, 8.3, 8.6, and 8.7 however we are conscious that we trust these scores less and several of these sub-pillars have green flags in other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where low matches in questions lead certain variables to yield significantly high differences. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Understanding that we do not necessarily expect large changes in data from Ireland, we are noting sub-pillars which trigger red flags in our comparative polling but are not examined in the TPS polling data. Additionally, we note sub-pillars which receive red flags in the expert polling but are not addressed in other analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Ireland. Therefore, what we are highlighting are the areas of concern as identified by the GPP analysis which are supported by external TPS public opinion data, as well as red flags raised by TPS data which are not reviewed in any other analysis.
            <br>
            <br>
            <b>Sub pillars to research</b>
            <ul>
            <li>Pillar 1. Constraints on Government Powers
            <ul>
            <li>Negative trend in 1.06: Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism)</li>
            <ul>
            <li> When we asked if people agreed that emergency powers are utilized to circumvent institutional checks and balances, we found a score of 0.495 while Varieties of Democracy provided a score of 0.906 when asking if members of the executive respect the constitution in expert polling. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match with an expert TPS, we recommend to give context about respect for checks and balances.</li>
            </ul>
            </ul>
            </li>
            <li>Pillar 5. Security
            <ul>
            <li>Negative trend in 5.1: People feel safe</li>
            <ul>
            <li>When we asked respondeds how safe they feel walking int heir neighborhood at night, we found a score of 0.577. When we asked the same question in the 2021 polling, we found a score of 0.629. This is a key area for investigation, and we recommend further review of the contexts of crime and personal safety in Ireland, especially given the recency of our comparison score.</li>
            </ul>
            </ul>
            </li>
            <li>Pillar 7. Civil Justice
            <ul>
            <li>Negative trend in 7.2: People can access quality legal assistance and representation</li>
            <ul>
            <li>When we asked respondents whether individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we received a score of 0.468. However, in the TPS Expert polls, our source Varieties of Democracies asked whether men and women each enjoy secure and effective access to justice, they returned a score of 0.852 for men and 0.835 for women. It is worth noting that our question specifies affordability as an issue, whereas the TPS Expert polling does not.</li>
            </ul>
            </ul>
            </li>
            <li>Pillar 8. Criminal Justice
            <ul>
            <li>Negative trend in 8.7: Prisons</li>
            <ul>
            <li>When we asked respondents how confident they are that the criminal justice system as a whole guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.548. However, in Varieties of Democracy's expert polling, when they asked whether there is freedom from torture, they found a score of 0.899. This is a lowest match question, which may account for the disparity in score. </li>
            </ul>
            </ul>
            </li>
            </ul>
            """

  elif country == "Italy":
    p = """<b>Insights summary</b>
            <br>
            We see that, across time, sub-pillars 1.11, 4.4, and 8.5 are flagged. Given that the previous GPP data from Italy is from 2017, we expect there to be significant difference. However, when observing the TPS public opinion polls, we only find one flagged subpillar, 8.5. This indicates that our data are relatively consistent with other population surveys, which is a key objective. In terms of TPS expert surveys, we find flags in sub-pillars 1.03, 1.06, 1.10, 4.5, 7.2, 7.4, and 8.3, however we are conscious that we trust these scores less and these sub-pillars have green flags in other analyses. TPS expert surveys did not address sub-pillar 8.5, which signaled red flags in the two other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Italy, we are noting sub-pillars that are flagged in both TPS Public Opinion Polls and the GPP cross-analysis. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Italy. Therefore, what we are highlighting are the areas of concern as identified by the GPP analysis which are supported by external TPS public opinion data.
            <br>
            <br>
            <b>Sub Pillars to Research</b>
            <ul>
            <br>
            <li>Pillar 7. Civil Justice
            <ul>
            <li>Negative trend in 7.2: People can access quality legal assistance and representation</li>
            <ul>
            <li>When we asked respondents whether individuals have access to reasonably priced legal assistance and representation when dealing with legal matters, we received a score of 0.389. However, in the TPS Expert polls, our source Varieties of Democracies asked whether men and women each enjoy secure and effective access to justice, they returned a score of 0.865 for men and 0.837 for women. It is worth noting that our question specifies affordability as an issue, whereas the TPS Expert polling does not.</li>
            </ul>
            </ul>
            </li>
            <li>Pillar 8. Criminal Justice
            <ul>
            <li>Negative trend in 8.5: Victim's Rights</li>
            <ul>
            <li>When we asked how confident people are that the criminal justice system allows all victims of crime to seek justice regardless of who they are, we found a score of 0.498, when our previous score was 0.647. Furthermore, when we asked if people thought that the criminal justice system provides victims of crime with the service and support they need, we found a score of 0.566 when our previous score was .0.643. This inconsistency indicates a red flag in our GPP over time analysis. Furthermore, when our TPS source, the Fundamental Rights Survey, asked the public whether police generally treat people positively, they found an agreement rate of 0.830. Despite the disparity in the phrasing of the two surveys (the GPP pointing to the perception of the criminal justice system as a whole and the TPS polling asking about police specifically), we find a potential negative trend in the area of victim's rights.</li>
            </ul>
            </ul>
            </li>
            </ul>
            """

  elif country == "Latvia":
    p = """There is no paragraph"""

  elif country == "Lithuania":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, most pillars are indicating changes. Although, this seems to be a result of a few sub-pillars, and some of them have mixed trends. In comparison to the TPS public opinion polls, we only have 1 red flag. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, there are a few pillars flagged, however we are conscious that we trust these scores less. 
            <br>
            <br>
            Given that we do not expect to see large changes from our previous data in Lithuania, we are noting sub pillars that are flagged in either the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Lithuania Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 1. Constraints on Government Powers
            <ul>
            <li> Negative trend in 1.06:  Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism) </li>
            <ul>
            <li> When we asked if people agreed that emergency powers are utilized to circumvent institutional checks and balances, we found a score of 0.448 while Freedom in the World provided a score of 0.944 when asking if members of the executive respect the constitution. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match with an expert TPS, we recommend to give context about respect for checks and balances. 
            </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 5. Security
            <ul>
            <li> Positive trend in 5.1: People feel safe </li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.593 when our previous score was 0.546. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 8. Criminal Justice 
            <ul>
            <li> Positive trend in 8.6: Due process of law </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees a fair trial of all accused people, we found a score of 0.569, while our previous score was 0.400. Furthermore, when we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.579 while our previous score was 0.473. In this regard, the score of this question has increased significantly since 2021, so we recommend researching the explanation of this change. </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. These inconsistencies are observed across all NUTS regions. 
            """

  elif country == "Luxembourg":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, most of the pillars are not changing drastically over time or indicate discrepancies with the TPS Public Opinion Polls. Pillar 1 is flagged in the GPP Over Time, however there is only one indicator level analysis and it is an opinion question. Pillar 8 is flagged in the TPS Expert Surveys, however the analyses have medium to low matches. Therefore, according to our data, people in Luxembourg have a similar view of the rule of law as they did in 2021, which is in accordance with the third party source data. Certainly, the primary source disparity is with Freedom in the World, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we do not expect to see changes from our previous data in Luxembourg, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Luxembourg Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported in the TPS.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 1. Constraints on Government Powers
            <ul>
            <li> Positive trend in 1.11: Government officials who abuse their power are sanctioned for misconduct (accountability and sanctions for misconduct) </li>
            <ul>
            <li> When we asked if people a hypothetical situation about a government official taking money for personal benefit, we found a score of 0.738 when our previous score was 0.653. This indicates that people think it is more likely that the official is punished appropriately. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 4. Fundamental Rights
            <ul>
            <li> Negative trend in 4.6: Justice </li>
            <ul>
            <li> When we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.592 while Freedom in the World assigned a score of 1 for the question regarding if due process prevails in civil and criminal matters. The large discrepancy between these scores should be explained further. Since this source of comparison is includes a strict expert encoding, we recommend to give a context about the rights of the accused and due process. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.1: Legal Security </li>
            <ul>
            <li> When we asked if people are aware of their rights when they face a legal problem we found a score of 0.438, while the Fundamental Rights Survey shows a score of 0.825 when they asked about the views on authorities providing information for people in a simple way. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match, we recommend to give a context about the knowledge of people about their rights when they faced a legal problem. </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 8. Criminal Justice 
            <ul>
            <li> Negative trend in 8.6: Due process of law </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees a fair trial of all accused people, we found a score of 0.633, while Freedom in the World found a score of 1 when they asked if due process prevaisl in civil and criminal matters. In the same analysis identified in Sub Pillar 4.6, when we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.592 while Freedom in the World assigned a score of 1 for the question regarding if due process prevails in civil and criminal matters. Although these questions have low matches, they are still related and should be complemented with research about the rights of the accused and due process. </li>
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Malta":
    p = """<b>Insights summary</b>
              <br>
              We are seeing that across time, only one pillar and subpillar are flagged. Our previous data is from 2021, and thus we may not expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have one red flag. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses.
            <br>
              <br>
              Given that we do not expect to see large changes from our previous data in Malta, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Malta Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
              <br>
              <b> Sub Pillars to Research </b>
              <br>
              <ul>
              <li> Pillar 7. Civil Justice
            <ul>
            <li> Negative trend in 7.1: Legal Security</li>
              <ul>
              <li> When we asked if people know their rights when facing a legal problem, we found a score of 0.473, while the Fundamental Rights Survey gave a score of 0.840. Although these questions are not matched very well, it is still important to supplement the comparison with research on the accessibility to justice and legal information in Malta.          
              </li>
            </ul>
              </ul>
              </ul>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
              """

  elif country == "Netherlands":
    p = """<b>Insights summary</b>
              <br>
              We are seeing that across time, a lot pillars and subpillars are flagged. However, our previous data is from 2018, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we have only two flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. 
            <br>
              <br>
              Given that we expect to see large changes from our previous data in Netherlands, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Netherlands. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
              <br>
              <b> Sub Pillars to Research </b>
              <br>
              <ul>
              <li> Pillar 8. Criminal Justice
            <ul>
            <li> Negative trend in 8.6: Due process of law</li>
              <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees a fair trial of all accused people, we found a score of 0.591, while Freedom in the World found a score of 1 when they asked if due process prevails in civil and criminal matters. Furthermore, when we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.592 while Freedom in the World assigned a score of 1 for the question regarding if due process prevails in civil and criminal matters. In this regard, the score of this question has decreased significantly since 2018, so we recommend researching the explanation of this change. </li>            </li>
            </ul>
              <li> Negative trend in 8.7: Prisons</li>
              <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.567, while Varieties of Democracy found a score of 0.909 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. </li>
            </li>
              </ul>
              </ul>
              </ul>
              <br>
              These discrepancies between the data are <b>NOT</b> consistent at the NUTS level; we observe that the significant differences occuring in some NUTS regions are causing the indicators to be flagged at the national level. There is a lot of heterogeneity between regions, and in subpillar 8.6. NL1:Noord-Nederland and NL3:West-Nederland are especially lower compared to the others.
            <br>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
              """

  elif country == "Poland":
    p = """There is no paragraph"""

  elif country == "Portugal":
    p = """<b>Insights summary</b>
              <br>
              We are seeing that across time, a lot pillars and subpillars are flagged. However, our previous data is from 2017, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have two red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. 
            <br>
              <br>
              Given that we expect to see large changes from our previous data in Portugal, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Portugal. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
              <br>
              <b> Sub Pillars to Research </b>
              <br>
              <ul>
              <li> Pillar 5. Security
              <ul>
              <li> Positive trend in 5.1: People feel safe</li>
              <ul>
              <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.663 when our previous score was 0.628. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more positively than before. 
            </li>
              </ul>
              <li> Positive trend in 5.2: Absence of crime and violence</li>
              <ul>
              <li> When we asked if people know or have heard if organized crime happens in their community or neighborhood, we found a score of 0.939 while the Organized Crime Index gave a Criminality Average Score of 0.57. Although these questions are not matched very well, it is still imporant to supplement the comparison with research on organized crime in Portugal.
            </li>
              </ul>
              </ul>
              </ul>
              <ul>
              <li> Pillar 8. Criminal justice
              <ul>
              <li>
              Positive trend in 8.2: Prosecution and pre-trial process
              </li>
              <ul>
              <li>
              When we asked if prosecutors prosecute crimes commited in an independent manner and are not subject to any pressure, we found a score of 0.568, while Special Eurobarometer 489 gave a score of 0.124. These questions matched very well, so it is important to supplement the comparison with research about the way Portugal’s judicial system prosecutes crimes. This differences are consistent across all the NUTS.           
              </li>
              </ul>
              </ul>
              </li>
              </ul>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
            """

  elif country == "Romania":
    p = """There is no paragraph"""

  elif country == "Slovakia":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, a few pillars are indicating changes. Most only have one or two indicators, however pillar 3 has 25 comparisons. Although many of these have red flags, some are positive changes while others are negative changes and overall encompass opinion questions. In comparison to the TPS public opinion polls, we have 0 red flags! This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, there are a few pillars flagged, however we are conscious that we trust these scores less. 
            <br>
            <br>
            Given that we do not expect to see large changes from our previous data in Slovakia, we are noting sub pillars that are flagged in either the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Slovakia Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 1. Constraints on Government Powers
            <ul>
            <li> Negative trend in 1.06:  Respect for the legitimacy of the constitutional order, the law making process, and political opponents (absence of authoritarianism) </li>
            <ul>
            <li> When we asked if people agreed that emergency powers are utilized to circumvent institutional checks and balances, we found a score of 0.318 while Freedom in the World provided a score of 0.822 when asking if members of the executive respect the constitution. The large discrepancy between these scores should be explained further. Since this source of comparison is a low match with an expert TPS, we recommend to give context about respect for checks and balances. 
            </li>
            </ul>
            </ul>
            </li>
            <li> Pillar 5. Security
            <ul>
            <li> Negative trend in 5.1: People feel safe </li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.52 when our previous score was 0.58. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more negatively than before. This inconsistency is observed across all NUTS regions.</li>
            </ul>
            </ul>
            </li>
            <li> Pillar 8. Criminal Justice 
            <ul>
            <li> Positive trend in 8.5: Victim's Rights </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system allows all victims of crime to seek justice regardless of who they are, we found a score of 0.618, when our previous score was 0.550. Furthermore, when we asked if people thought that the criminal justice system provides victims of crime with the service and support they need, we found a score of 0.618 when our previous score was .579. Although this subpillar has a green flag in the TPS public opinion poll analysis, we are still flagging it because that green flag is the result of a low matched comparison and the previous GPP data is most updated. </li>
            <li> At the NUTS level, discrepancies are evident in the regions 'SK01: Bratislavský kraj' and 'SK03: Stredné Slovensko', where the scores are significantly higher than the rest of the country. Finding further explanations for the improvements in these regions' criminal justice systems would better clarify the overall explanation.</li>              
            </ul>
            </ul>
            </li>
            </ul>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Slovenia":
    p = """<b>Insights summary</b>
            <br>
            We are seeing that across time, most of the pillars in the GPP are changing. For the most part, these changes indicate a mix of trends across and within sub pillars. Furthermore, since our previous data from Slovenia is from 2017, these changes are expected. Nevertheless, the result of these trends in terms of our full fieldwork data are similar to what other sources are observing. In comparison to the TPS public opinion polls, we only have one red flag. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. A few sub-pillars are flagged in the TPS expert comparisons, which is also to be expected.
            <br>
            <br>
            Given that we expect to see changes from our previous data in Slovenia, we are noting sub pillars that are flagged in the TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Slovenia. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported in the TPS.
            <br>
            <br>
            <b> Sub Pillars to Research </b>
            <ul>
            <li> Pillar 5. Security
            <ul>
            <li> Negative trend in 5.1: People feel safe </li>
            <ul>
            <li> When we asked how safe people feel walking in their neighborhood at night, we found a score of 0.667 when our previous score was 0.722. Although the difference between scores is not very large, the t-test indicates that overall, individuals are answering more negatively than before. </li>
            </ul>
            </ul>
            </li>
            </li>
            <li> Pillar 8. Criminal Justice 
            <ul>
            <li> Mixed trends in 8.5: Victim’s Rights </li> 
            <ul>
            <li> The GPP Over Time analysis indicates a positive trend. When we asked how confident people are that the criminal justice system allows all victims of crime to seek justice regardless of who they are, we found a score of 0.580, when our previous score was 0.486. Furthermore, when we asked if people thought that the criminal justice system provides victims of crime with the service and support they need, we found a score of 0.613 when our previous score was 0.504. </li>
            <li> The TPS Public Opinion Poll comparison indicates a negative trend. When we asked how confident people are that the criminal justice system as a whole respects the rights of victims, we found a score of 0.404 while the Fundamental Rights Survey found a score of 0.793 when they measured the perception of the way the police generally treats people. Although these questions have a low match, it is still important to highlight the disparity. </li>
            <li> Given the different trends indicated in each analysis, we can surmise that overall, our data on victim's rights is trending in a positive direction, yet is still lower than other third party sources.
            </ul>
            <li> Negative trend in 8.6: Due process of law </li>
            <ul>
            <li> The TPS Public Opinion Poll comparison indicates a negative trend. When we asked how confident people are that the criminal justice system guarantees a fair trial of all accused people, we found a score of 0.371, while our previous score was 0.456 and Freedom in the World found a score of 1 when they asked if due process prevails in civil and criminal matters. Furthermore, when we asked if people thought that the criminal justice system treats those accused as innocent until proven guilty, we found a score of 0.472 while our previous score was 0.586 and Freedom in the World assigned a score of 1 for the question regarding if due process prevails in civil and criminal matters.</li>
            </ul>
            <li> Negative trend in 8.7: Prisons </li>
            <ul>
            <li> When we asked how confident people are that the criminal justice system guarantees the safety and human rights of people deprived of their liberty, we found a score of 0.467, while Varieties of Democracy found a score of 0.859 when they asked if there was freedom from torture. Although the questions have a low match, they are still related and should be complemented with research about safety and human rights in the criminal justice system. </li>
            </ul>
            </ul>
            </li>
            </ul>
            All these discrepancies between the data are also consistent at the NUTS level; we observe that the significant differences persist across all NUTS regions for all sub-pillars flagged.
            <br>
            <br>
            The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly. 
            """

  elif country == "Spain":
    p = """<b>Insights summary</b>
              <br>
              We are seeing that across time, a few pillars and subpillars are flagged. However, our previous data is from 2018, and thus we expect there to be changes. Furthermore, in comparison to the TPS public opinion polls, we only have two red flags. This indicates that our data is in accordance with other population surveys, which is one of the most important goals. In terms of the TPS expert surveys, we are flagging a few subpillars, however we are conscious that we trust these scores less and that all of these have green flags in other analyses. Given the subpillars we are highlighting, we recommend providing information about the current status of security in Spain and the changes across time given that we are finding mixed trends in this regard.
            <br>
              <br>
              Given that we expect to see large changes from our previous data in Spain, we are noting sub pillars that are flagged in both the GPP and TPS analyses. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Spain. Therefore, what we are highlighting are the discrepancies found in the data in two aspects: the ones that are consistent in both analyses, and also the ones that are not supported by another analysis.
            <br>
              <br>
              <b> Sub Pillars to Research </b>
              <br>
              <ul>
              <li> Pillar 5. Security
            <ul>
            <li> Negative trend in 5.1: People feel safe</li>
              <ul>
              <li> When we asked if people feel safe walking in their neighborhood at night, we found an score of 0.61 which is lower than the previous score of 0.653. In this case the difference is not very big, so we propose to give some context about the security in Spain.
            </li>
            </ul>
              <li> Positive trend in 5.2: Absence of crime and violence</li>
              <ul>
              <li> When we asked if people know or have heard if organized crime happens in their community or neighborhood, we found a score of 0.873 while the Organized Crime Index gave a Criminality Average Score of 0.464. Although these questions are not matched very well, it is still imporant to supplement the comparison with research on organized crime in Spain.
            </li>
              </ul>
              </ul>
              </ul>
              <ul>
              <li> Pillar 7. Civil justice
              <ul>
              <li>
              Negative trend in 7.2: People can acces quality legal assistance and representation
              </li>
              <ul>
              <li>
              When we asked if people  have access to affordable legal assistance and representation when they face a legal problem, we found a score of 0.473, while VDEM gave a score of 0.858. Although these questions are not matched very well, and VDEM is an expert survey, it is still important to supplement the comparison with research on the accessibility to justice and legal assistance in Spain. This differences are consistent across all the NUTS.           
              </li>
              </ul>
              </ul>
              </li>
              </ul>
              <br>
              These discrepancies between the data are <b>NOT</b> consistent at the NUTS level; we observe that the significant differences occuring in some NUTS regions are causing the indicators to be flagged at the national level. There is a lot of heterogeneity between regions, and in subpillars 5.1 and 5.2, ES5:Este and ES6: Sur are especially lower compared to the others.
            <br>
            <br>
              The topic areas highlighted above are what our data is telling us through the given analyses. However, it is still important to take into account the media reports and other qualitative background research to potentially identify any other sub-pillar that should be researched more thoroughly.
              """

  elif country == "Sweden":
    p = """<b>Insights summary</b>
            <br>
            We see that, across time, sub-pillars 1.11 and 5.1 are flagged. Given that the previous GPP data from Sweden is from 2018, we expect there to be significant difference. However, when observing the TPS public opinion polls, we only find one flagged subpillar, 8.5. This indicates that our data are relatively consistent with other population surveys, which is a key objective. In terms of TPS expert surveys, we find flags in sub-pillars 1.03, 4.5, 4.6, 7.4, 8.3, 8.6, and 8.7, however we are conscious that we trust these scores less and these sub-pillars have green flags in other analyses. Certainly, the primary source disparity is with Experts sources like Freedom in the World and V-Dem, where certain variables yield significantly high scores. In such instances, we advise prioritizing a discussion on the validity of our scores rather than clarifying disparities between the sources.
            <br>
            <br>
            Given that we expect to see large changes from our previous data in Sweden, we are noting sub-pillars that are flagged in TPS Public Opinion Polls. In this regard, all the topics that are flagged in the time comparison but supported by green flags in the TPS are considered as something normal in the context of Sweden. Therefore, what we are highlighting are the discrepancies found in the TPS polls, which serve as our most salient indicator, but do not trigger red flags in our own GPP analysis.
            <br>
            <br>
            <b>Sub Pillars to Research</b>
            <ul>
            <li>Pillar 8. Criminal Justice
            <ul>
            <li>Negative trend in 8.5: Victim's Rights</li>
            <ul>
            <li>When we asked how confident people are that the criminal justice system allows all victims of crime to seek justice regardless of who they are, we found a score of 0.527, when our previous score was 0.503. Furthermore, when we asked if people thought that the criminal justice system provides victims of crime with the service and support they need, we found a score of 0.561 when our previous score was .542. This consistency indicates a green flag in our GPP over time analysis, however when our TPS source, the Fundamental Rights Survey, asked the public whether police generally treat people positively, they found an agreement rate of 0.910. The primary cause of disparity likely stems from the phrasing of the two questions: the GPP pointing to the perception of the criminal justice system as a whole and the TPS polling asking about police specifically.</li>
            </ul>
            </ul>
            </li>
            </ul>"""

  return p
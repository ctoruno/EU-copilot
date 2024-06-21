"""
Module Name:    Password Check
Author:         Carlos Alberto Toruño Paniagua
Date:           June 7th, 2024
Description:    This module contains the code for inserting a grouped menu on side bar
This version:   June 7th, 2024
"""
from st_pages import Page, Section, show_pages, add_page_title
def insert_smenu():
    add_page_title()
    show_pages(
        [
            Page("0_Home.py", "EU-S Copilot"),
            Section("Tools"),
            Page("pages/1_GPP_tools.py", "GPP Tools", in_section=True),
            Page("pages/3_Codebooks.py", "Codebook Explorer", in_section=True),
            Section("Data Validation"),
            Page("pages/6_GPP_Country_Level_Validation.py", "GPP Country Validation", in_section=True),
            Page("pages/7_GPP_Third_Stage.py", "GPP Third Stage", in_section=True),
            Page("pages/4_Media_Reports.py", "Media Reports", in_section=True),
            Section("Dashboard"),
            Page("pages/5_Dashboard.py", "GPP Data", in_section=True),
            Page("pages/9_QRQ_Dashboard.py", "QRQ Data", in_section=True),
            Page("pages/8_Information.py", "Information", in_section=False)
        ]
    )
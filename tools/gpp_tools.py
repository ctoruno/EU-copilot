"""
Module Name:    EU-GPP Tools
Author:         Carlos Alberto Toruño Paniagua
Date:           October 19th, 2023
Description:    This module contains all the functions and classes to be used by the EU Copilot 
                app in the cleaning process for the GPP data.
This version:   October 23rd, 2023
"""

import math
import pandas as pd
import streamlit as st
import base64
import pyreadstat
import tempfile
import os

def dtaNames(df, datamap, ignore_case = False):
    """
    This function takes the pre-defined data map and a data frame as inputs and returns a 
    dictionary containg the names of the variables that are, either in the data but not listed in 
    the data map, or those variables that are listed in the data map but were not found in the 
    data.

    Parameters:
    df:             Data frame containg the data to be analyzed.
    datamap:        Object containg the data map as a pandas data frame.
    ignore_case:    Boolean. Should the match ignore lower/upper case in names?

    Returns:
    dict:       Dictionary with lists of variable names as values
    """

    # Defining inputs
    cnames    = df.columns
    dmap_vars = datamap["Variable"]

    if ignore_case == False:
        cnames    = [x.lower().strip() for x in cnames]
        dmap_vars = [x.lower().strip() for x in dmap_vars]
    else:
        cnames    = [x.strip() for x in cnames]
        dmap_vars = [x.strip() for x in dmap_vars]

    # Elements in data map but not in data
    dmap_missing = [item for item in dmap_vars if item not in cnames]
    
    # Elements in data but not in data map
    master_added = [item for item in cnames if item not in dmap_vars]

    return dmap_missing, master_added


def dtaValues(df, datamap, missing_vals):
    """
    This function takes the pre-defined data map, a target data frame, and a list containing the
    the names of the variables that are missing in the target data and returns a dictionary with
    two elements as values: (1) a count of the number of observations outside the expected range
    per variable, and (2) a list containing the expected values of that variable according to
    the datamap.

    Parameters:
    df:             Data frame containg the data to be analyzed.
    datamap:        Object containg the data map as a pandas data frame.
    missing_vals:   List containg the names of the variables that are not present in the data
                    but isted in the data map

    Returns:
    dict:       Dictionary with two elements as values: (1) a count of the number of observations 
                outside the expected range per variable, and (2) a list containing the expected 
                values of that variable according to the datamap.
    """

    # Defining columns to check
    cnames     = df.columns
    svars      = [
        "year", "age", 
        "q16_A1", "q16_A2", "q16_A3", "q16_B1", "q16_B2", "q16_B3", "q16_B4", "q16_C1", "q16_C2", 
        "q16_C3", "q16_C4", "q16_D1", "q16_D2", "q16_D3", "q16_D4", "q16_D5", "q16_D6", "q16_E1"
        "q16_E2", "q16_E3", "q16_F1", "q16_F2", "q16_G1", "q16_G2", "q16_G3", "q16_H1" ,"q16_H2", 
        "q16_H3", "q16_I1", "q16_J1", "q16_J2", "q16_J3", "q16_J4", "q16_K1", "q16_K2", "q16_K3", 
        "q16_L1", "q16_L2",
        "paff1", "A1", "COLOR"
    ]
    vars2check = [x.strip() for x in cnames if x not in missing_vals]
    vars2check = [x.lower() for x in vars2check if x not in svars]

    # Variables from data map
    datamap["Variable"] = datamap["Variable"].map(str.lower)
    dmap_vars  = datamap["Variable"]
    
    # Renaming variables to lowercase
    df.columns = [x.lower() for x in df.columns]

    # Create an empty dictionary to store results for each column
    results = {}

    # Looping through variables
    for target in vars2check:
        scale   = (datamap
                   .loc[datamap["Variable"] == target, "Scale"]
                   .to_string(index=False))
        
        if scale in ["Open", "Fix"]:
            choices = []
        elif scale in ["Scale 2 without DKNA"]:
            choices = [math.nan, 1, 2]
        elif scale in ["Scale 3 without DKNA"]:
            choices = [math.nan, 1, 2, 3]
        elif scale in ["Scale 5 without DKNA"]:
            choices = [math.nan, 1, 2, 3, 4, 5]
        elif scale in ["Scale 2"]:
            choices = [math.nan, 1, 2, 98, 99]
        elif scale in ["Scale 3"]:
            choices = [math.nan, 1, 2, 3, 98, 99]
        elif scale in ["Scale 4"]:
            choices = [math.nan, 1, 2, 3, 4, 98, 99]
        elif scale in ["Scale 5"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 98, 99]
        elif scale in ["Scale 7"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 98, 99]
        elif scale in ["Scale 8"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 8, 98, 99]
        elif scale in ["Scale 10"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 98, 99]
        elif scale in ["Scale 11"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 98, 99]
        elif scale in ["Range 0-4"]:
            choices = [math.nan, 0, 1, 2, 3, 4, 98, 99]
        elif scale in ["Range 0-10"]:
            choices = [math.nan, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 98, 99]
        elif scale in ["Range 1-10"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 98, 99]
        elif scale in ["Range 1-11"]:
            choices = [math.nan, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        else:
            choices = []

        if scale in["Open", "Fix"]:
            results[target] = (0, ["Open/Fix entry"])
        else:
            results[target] = ((~df[target].isin(choices)).sum(), choices)

    return results


def show_pdf(file_path):
    """
    This function takes a local path to a PDF document in the local files and generates an
    iframe to dissplay it.

    Parameters:
    file_path:  String. Path to PDF file in the local files.

    Returns:
    HTML:       HTML code with iframe to preview the PDF file.
    """
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, 
                unsafe_allow_html = True)

def read_dta(file):
    """
    This is a helper function to load a DTA file using pyreadstat instead of pandas. It takes a Uploader object from
    a Streamlit STATA Uploader Input widget and returns a Pandas Data Frame.
    """
    
    temp_dir  = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.name)
    with open(temp_path, 'wb') as f:
        f.write(file.read())

    df, meta = pyreadstat.read_dta(temp_path,
                                   apply_value_formats = True,
                                   formats_as_category = False)
    
    return df

# Defining a nested dictionary with all value labels in the data map
value_labs = {
    "replacements_common" : {
        "acc" : {
            1 : "Always Acceptable",
            2 : "Usually Acceptable",
            3 : "Sometimes Acceptable",
            4 : "Not Acceptable",
            98 : "Don't Know",
            99 : "No Answer"
        },
        "agree" : {
            1: "Strongly Agree",
            2: "Agree",
            3: "Disagree",
            4: "Strongly Disagree",
            98: "Don't know",
            99: "No answer"
        },
        "confid": {
            1: "Very Confident",
            2: "Fairly confident",
            3: "Not very confident",
            4: "Not at all confident",
            98: "Don't know",
            99: "No answer"
        },
        "contact": {
            1: "Myself (or someone on my behalf)",
            2: "The other party",
            3: "Someone else",
            98: "Don't know",
            99: "No answer"
        },
        "cor": {
            1: "None",
            2: "Some of them",
            3: "Most of them",
            4: "All of them",
            98: "Don't know",
            99: "No answer"
        },
        "done": {
            1: "Ongoing",
            2: "Too early to say",
            3: "Done with, but problem persists",
            4: "Done with, problem fully resolved",
            98: "Don't know",
            99: "No answer"
        },
        "imp": {
            1: "Essential",
            2: "Important",
            3: "Not so important",
            4: "Not important at all",
            98: "Don't know",
            99: "No answer"
        },
        "improv": {
            1: "Yes",
            2: "Maybe, somewhat",
            3: "No, it's already fine",
            98: "Don't know",
            99: "No answer"
        },
        "likely": {
            1: "Very likely",
            2: "Likely",
            3: "Unlikely",
            4: "Very unlikely",
            98: "Don't know",
            99: "No answer"
        },
        "psdesc": {
            1: "Not at all",
            2: "Little",
            3: "Somewhat",
            4: "Very much",
            98: "Don't know",
            99: "No answer"
        },
        "rate": {
            1: "Very Good",
            2: "Good",
            3: "Neither good nor bad (fair)",
            4: "Bad",
            5: "Very Bad",
            98: "Don't know",
            99: "No answer"
        },
        "safe": {
            1: "Very safe",
            2: "Safe",
            3: "Unsafe",
            4: "Very unsafe",
            98: "Don't know",
            99: "No answer"
        },
        "satis": {
            1: "Very satisfied",
            2: "Satisfied",
            3: "Dissatisfied",
            4: "Very dissatisfied",
            98: "Don't know",
            99: "No answer"
        },
        "trust": {
            1: "A lot",
            2: "Some",
            3: "A little",
            4: "No trust",
            98: "Don't know",
            99: "No answer"
        },
        "yn": {
            1: "Yes",
            2: "No",
            98: "Don't know",
            99: "No answer"
        },
        "account" : {
            1: "The accusation is completely ignored by the authorities",
            2: "An investigation is opened, but it never reaches any conclusions",
            3: "The high-ranking government officer is prosecuted and punished (through fines, or time in prison)",
            98: "Don't know",
            99: "No answer"
        }
    },
    "replacements_unique" : {
        "q5" : {
            1: "Significantly Increased",
            2: "Increased",
            3: "Remained the Same",
            4: "Decreased",
            5: "Significantly Decreased",
            98: "Don't know",
            99: "No answer"
        },
        "q23" : {
            1: "I thought the issue was not important or not difficult to resolve",
            2: "Thought the other side was right",
            3: "I did not think I needed advice",
            4: "I was concerned about the financial cost",
            5: "I had received help with a problem before and did not find it useful",
            6: "I did not know who to call or where to get advice",
            7: "I did not know I could get advice for this problem",
            8: "Was scared to get advice",
            9: "Advisers were too far away or it would take too much time",
            10: "Other",
            98: "Don't know",
            99: "No answer"
        },
        "q25" : {
            1: "I thought the problem was not important enough or easy to resolve",
            2: "I was confident I could resolve it by myself",
            3: "Resolving the problem would have taken a long time or a lot of bureaucratic procedures",
            4: "I did not have evidence or a strong case",
            5: "Scared of the consequences / The other party is much more powerful",
            6: "I did not know what to do, where to go, or how to do it",
            7: "Access problems (cost, distance, schedule, etc.)",
            8: "I did not trust the authorities",
            9: "It would create problems for my family or damage a relationship",
            10: "I caused the problem / It was up to the other party",
            11: "Other",
            98: "Don't know",
            99: "No answer"
        },
        "q27" : {
            1: "Agreement between you and the other party",
            2: "The other party independently doing what you wanted",
            3: "You independently doing what the other party wanted",
            4: "The problem sorting itself out",
            5: "You moving away from the problem (e.g. moving homes, changing jobs)",
            6: "You and/or all other parties giving up trying to resolve the problem",
            7: "None of these",
            98: "Don't know",
            99: "No answer"
        },
        "q31" : {
            1: "A decision or intervention by a court or a formal authority",
            2: "Mediation or arbitration",
            3: "Action by another third party",
            4: "Agreement between you and the other party",
            5: "The other party independently doing what you wanted",
            6: "You independently doing what the other party wanted",
            7: "The problem sorting itself out",
            8: "You moving away from the problem (e.g. moving homes, changing jobs)",
            9: "You and/or all other parties giving up trying to resolve the problem",
            10: "None of these",
            98: "Don't know",
            99: "No answer"
        },
        "q33a" : {
            1: "Mostly in my favor",
            2: "Somewhat in my favor",
            3: "Mostly not in my favor",
            98: "Don't know",
            99: "No answer"
        },
        "q33d" : {
            1: "Very easy",
            2: "Somewhat easy",
            3: "Difficult",
            4: "Nearly impossible",
            98: "Don't know",
            99: "No answer"
        },
        "nation" : {
            1: "National [Citizen]",
            2: "Foreigner",
            98: "Don't know",
            99: "No answer"
        },
        "fin" : {
            1: "Money is not enough even for basic necessities and buying clothes is difficult",
            2: "Can buy basic products but buying clothes is difficult",
            3: "Can buy basic products and clothes, but not long-term goods",
            4: "Can buy long-term goods, but cannot buy expensive goods",
            5: "Can afford sufficiently expensive goods",
            98: "Don't know",
            99: "No answer"
        },
        "edu" : {
            1: "None",
            2: "Elementary school diploma",
            3: "Middle school diploma",
            4: "High school diploma or equivalent",
            5: "Bachelor's degree",
            6: "Graduate degree (Masters, Ph.D.)",
            7: "Vocational",
            98: "Don't know",
            99: "No answer"
        },
        "emp" : {
            1: "Worked",
            2: "Had work, but did not work",
            3: "Looked for work",
            4: "Studied",
            5: "Dedicated yourself to household tasks",
            6: "Were retired",
            7: "Were permanently incapable of working",
            8: "Did not work",
            98: "Don't know",
            99: "No answer"
        },
        "work" : {
            1: "Government worker",
            2: "Private sector worker",
            3: "Independent professional",
            4: "Self-employed worker",
            5: "Day laborer",
            6: "Businessman or businesswomen",
            7: "Entrepreneur or business owner",
            8: "Unpaid worker",
            98: "Don't know",
            99: "No answer"
        },
         "wagreement": {
            1: "A written agreement",
            2: "An oral agreement",
            98: "Don't know",
            99: "No answer"
        },
        "marital": {
            1: "Single",
            2: "Domestic partnership/living as married",
            3: "Married",
            4: "Divorced",
            5: "Widowed",
            98: "Don't know",
            99: "No answer"
        },
        "disability2": {
            1: "Physical",
            2: "Mental",
            3: "Both",
            98: "Don't know",
            99: "No answer"
        },
        "politics": {
            1: "Very interested",
            2: "Interested",
            3: "A little interested",
            4: "Not at all interested",
            98: "Don't know",
            99: "No answer"
        },
        "A3": {
            1: "Daily",
            2: "Several times a week",
            3: "Several times a month",
            4: "Rarely",
            5: "Never",
            98: "Don't know",
            99: "No answer"
        },
        "A5c": {
            1: "A title, deed, or certificate of ownership",
            2: "A rental contract or lease",
            3: "Other",
            98: "Don't know",
            99: "No answer"
        },
        "Urban": {
            1: "Urban",
            2: "Rural"
        },
        "B1": {
            1: "Independent home",
            2: "Apartment Building",
            3: "Multi-family apartment/low-income housing unit",
            4: "Unfinished housing",
            5: "Structure not built for housing"
        },
        "B3": {
            1: "From the same home",
            2: "Neighbor",
            3: "A stranger monitoring responses",
            4: "Other representative from a polling company (i.e. supervisor)",
            5: "Other (a friend, salesperson, etc.)"
        },
        "qpi2a": {
            1: "Friendly",
            2: "In between",
            3: "Hostile"
        },
        "qpi2b": {
            1: "Interested",
            2: "In between",
            3: "Bored"
        },
        "qpi2c": {
            1: "Cooperative",
            2: "In between",
            3: "Uncooperative"
        },
        "qpi2d": {
            1: "Patient",
            2: "In between",
            3: "Impatient"
        },
        "qpi2e": {
            1: "At ease",
            2: "In between",
            3: "Suspicious"
        },
        "qpi2f": {
            1: "Honest",
            2: "In between",
            3: "Misleading"
        }
    }
}

def vals_checks(df_nums, df_labs, filtered_map, target, lab_class):

    if lab_class == "unique":
        repls = value_labs["replacements_unique"][target]
    else:
        repls = value_labs["replacements_common"][lab_class]

    df1 = df_nums[[target]].replace(repls)
    df2 = df_labs[[target]]

    try:
        df1[target] = (df1[target]
                    .str.lower()
                    .str.replace("’", "'")
                    .str.strip())
        df2[target] = (df2[target]
                    .str.lower()
                    .str.replace("’", "'")
                    .str.strip())
    except AttributeError:
        re1 = False
        re2 = "Attribute error"

    if df1[target].equals(df2[target]):
        re1 = True
        re2 = None
    else:
        re1 = False
        re2 = df1[df1[target] != df2[target]]
        re2 = re2.index

    return [target, re1, re2, repls]

    

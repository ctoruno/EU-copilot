"""
Module Name:    EU-GPP Tools
Author:         Carlos Alberto Toruño Paniagua
Date:           October 19th, 2023
Description:    This module contains all the functions and classes to be used by the EU Copilot 
                app in the cleaning process for the GPP data.
This version:   October 19th, 2023
"""

import math

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
    vars2check = [x for x in vars2check if x not in svars]
    
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
            results[target] = (0, choices)
        else:
            results[target] = ((~df[target].isin(choices)).sum(), choices)

    return results



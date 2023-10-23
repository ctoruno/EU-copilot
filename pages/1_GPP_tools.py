import re
import pandas as pd
import streamlit as st
# import tools.gpp_tools as gpp


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




st.title("GPP tools")

# Reading Codebook & DataMa
datamap = pd.read_excel("inputs/EU2 GPP 2023 Full Datamap.xlsx", 
                        sheet_name = "Data Map")

# Creating a container for Step 1
step1 = st.container()
with step1:

    # Container Title
    st.markdown("<h4>Step 1: File conversion and UTF-8 encoding",
                unsafe_allow_html = True)
    
    # Uploader widget
    uploaded_file = st.file_uploader("Upload a Stata DTA file", 
                                     type = ["dta"])
    
    
    # Read the uploaded file using Pandas
    if uploaded_file is not None:
        try:
            data = pd.read_stata(uploaded_file, 
                                convert_categoricals = False, 
                                convert_missing = False)
            data_preview = st.expander("Click here to preview your data file")
            with data_preview:
                st.write("Data from the uploaded file:")
                st.write(data)

        except pd.errors.ParserError as e:
            st.error("Error: Invalid DTA file. Please upload a valid Stata DTA file.")

# Creating a container for Step 2
step2 = st.container()
with step2:

    # Container Title
    st.markdown("<h4>Step 2: Data structure checks",
                unsafe_allow_html = True)

    if uploaded_file is not None:

        # Widget to (de)activate case sensitivity
        scase = st.toggle(
            "Case sensitivity?",
            value = False,
            help = "When mapping missing variables, should the mapping omit mismatches based on lower/upper caps?"
        )
    
        dmap_missing, master_added = gpp.dtaNames(data, datamap, ignore_case = scase)

        exp2_1 = st.expander("Are all the variables listed in the data map present in the data set?")
        with exp2_1:
            st.markdown(
                """
                <p class='jtext'><b>
                The following elements were not found in the uploaded data file:
                </b></p>
                """,
                unsafe_allow_html = True
            )
            st.write(dmap_missing)
            st.markdown(
                """
                <p class='jtext'><b>
                Use the following Stata command line(s) to generate empty values:
                </b></p>
                """,
                unsafe_allow_html = True
            )
            for v in dmap_missing:
                st.code("g " + v + " = .",
                        language     = "stata", 
                        line_numbers = False)

        exp2_2 = st.expander("The following elements are present in the data file but they are not listed in the data map:")
        with exp2_2:
            st.markdown(
                """
                <p class='jtext'><b>
                The following elements are present in the data file but they are not listed in the data map:
                </b></p>
                """,
                unsafe_allow_html = True
            )
            st.write(master_added)
            st.markdown(
                """
                <p class='jtext'><b>
                Use the following Stata command line(s) to drop these variables:
                </b></p>
                """,
                unsafe_allow_html = True
            )
            st.code("drop " + " ".join(master_added),
                    language     = "stata", 
                    line_numbers = False)
    
        exp2_3 = st.expander("Does any variable surpass the expected value range?")
        with exp2_3:

            range_checks = gpp.dtaValues(data, datamap, dmap_missing)
            counts       = [sublist[0] for sublist in list(range_checks.values())]

            if sum(counts) == 0:
                st.markdown(
                """
                <p class='jtext'><b>
                No variable found with values outside the expected range
                </b></p>
                """,
                unsafe_allow_html = True
            )
            else:
                for column, result in range_checks.items():
                    if result[0] > 0 and len(result[1]) > 0:
                        st.code(f"At least one value in {column} is outside the expected range.")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("Variable presents the following frequencies:")
                            st.write(data[column].value_counts().sort_index())
                        with col2:
                            st.write("Available choices:")
                            st.write(result[1])
    else:
        st.markdown("<p class='jtext'><b>Please upload a data file before continuing.</b></p>",
                    unsafe_allow_html = True
        )

                    
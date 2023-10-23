import streamlit as st

# Page config
st.set_page_config(
    page_title = "Home",
    page_icon  = "house"
)

# Reading CSS styles
with open("styles.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

st.title("EU-S Copilot")
st.markdown(
    """
    <p class='jtext'>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
    aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
    sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>
    
    <p class='jtext'>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
    aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 
    sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>

    <p class='jtext'>
    If you have questions, suggestions or you want to report a bug, make sure of checking the 
    <strong style="color:#003249">Info Tab</strong> in the left side bar panel.
    </p>

    <p class='jtext'>
    Galingan!
    </p>
    """,
    unsafe_allow_html = True
)
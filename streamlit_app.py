# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to hold the front-end logic using StreamLit

# IMPORTS
import streamlit as st

# Favicon
# May not work on Safari, but should work on Chrome
st.set_page_config(
    page_title="MetaReads",
    page_icon="🚀"
    #page_icon="assets/my_favicon.png", # Path to your file
    #layout="wide"
)

# Page setup
home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
alg_search = st.Page("pages/02_Algorithm.py", title="Algorithm Search", icon="🔍")
fil_search = st.Page("pages/03_Filter.py", title="Filter Search", icon="📊")
about = st.Page("pages/04_About.py", title="About", icon="ℹ️")

# Navigation 
pg = st.navigation([home, alg_search, fil_search, about], position="sidebar")

# Run selected page 
pg.run()
# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to hold the front-end logic using StreamLit

# IMPORTS
import streamlit as st

# Page setup
home = st.Page("pages/01_Home.py", title="Home", icon="🏠")
alg_search = st.Page("pages/02_Algorithm.py", title="Algorithm Search", icon="🔍")
fil_search = st.Page("pages/03_Filter.py", title="Filter Search", icon="📊")

# Navigation 
pg = st.navigation([home, alg_search, fil_search], position="sidebar")

# Run selected page 
pg.run()
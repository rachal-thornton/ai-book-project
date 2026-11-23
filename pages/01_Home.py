# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to hold the front-end logic using StreamLit

# IMPORTS
import streamlit as st

# Title
st.title("MetaReads")

# Main body
st.markdown(
    """
    *Welcome to **MetaReads**!* We are a book recommendation application that uses your 
    favorite books to suggest you something new to read. Click on the sidebar to try one
    of our search algorithms!
    """
)

# Divider and credits
st.divider()
st.write("Created by Rachal Thornton @ 2026 | For a full list of credits, check out our [GitHub](https://github.com/rachal-thornton/ai-book-project)")
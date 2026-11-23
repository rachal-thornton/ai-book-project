# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to hold the front-end logic using StreamLit

# IMPORTS
import streamlit as st

# Title
st.title("Book Recommender Using Algorithm")

# Main body
st.write("Don't see your favorite book listed? Try our filtered search to look for a new book instead!")
st.caption("Due to a limited number of books in the dataset, your favorite one might not be included. Sorry!")

# Search for book in database
# TODO: implement a way for users to search for multiple books,
#       see options as they search
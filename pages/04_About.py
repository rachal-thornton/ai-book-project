# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to hold the front-end logic using StreamLit

# IMPORTS
import streamlit as st

# Title
st.title("About")

# Main body
st.markdown(
    """
    **MetaReads** is a student-led final project developed for Winona State University's *CS445 Artificial Intelligence* class.
    It demonstrates concepts taught throughout the semester, focusing on a TF-IDF/embeddings hybrid recommendation model.\n

    Using book data from a *[Price Prediction Dataset](https://www.kaggle.com/competitions/book-prices-prediction/data?select=books_train.csv)* 
    on Kaggle, a cleaned CSV file of raw books data was created. From there, a weighted TF-IDF/embeddings recommender was built using Python libraries and machine learning concepts.
    Different factors, such as a book's liked percentage or number of five-star ratings, determine how closely a book aligns with a user's previously-read book.
    The recommender will return a list of books that have the cloest score, with the assumption that these books are ones that the user is most likely to enjoy from the dataset.

    Progress tracked and any changes to the model/software can be tracked on the author's [GitHub](https://github.com/rachal-thornton/ai-book-project).
    """
)

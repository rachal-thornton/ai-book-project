# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program test aspects of the code.

# IMPORTS
from data_processing import clean_books
from recommender import train_recommender, recommend_books
from pathlib import Path

# TESTS
"""Test all steps of cleaning and recommending."""
# Imput/output path
project_root = Path.cwd()
input_path = project_root / "data" / "books.csv"
output_path = project_root / "data" / "books_cleaned.csv"

# Clean books
books = clean_books(input_path, output_path)

# Train data
books, vectorizer, tfidf_matrix = train_recommender(books)

# Example of user titles
fav_titles = [
    ""
]

# Recommend new books
recommendations = recommend_books(
    fav_titles,
    books,
    tfidf_matrix,
    num_of_rec=10
)

# Print recommended books 
print("\nRecommended books:")
print(
    recommendations[["title", "author", "sim_score"]]
    .to_string(index=False)
)
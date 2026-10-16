# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to train and recommend a user books based on their entered favorite books.

# IMPORTS
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# FUNCTIONS
def train_recommender(books):
    """Train a model to vectorize book information."""

    # Copy books data to avoid altering original
    books = books.copy()

    # Convert genre lists into plain text
    books["genres"] = books["genres"].apply(
        lambda x: " ".join(x) if isinstance(x, list) else str(x)
    )

    # Combine metadata about each book into one field
    books["combined_meta"] = (
        books["title"].fillna("").astype(str) + " " +
        books["author"].fillna("").astype(str) + " " +
        books["description"].fillna("").astype(str) + " " +
        books["genres"].fillna("").astype(str)
    )

    # Convert book text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english",   # Remove common English words from being stored
        max_features=50000,     # Max number of words to store
        ngram_range=(1, 2),     # Store 1 or 2-word phrases
        min_df=2                # Only store words that appear in 2 or more books
    )

    # Fit model on book metadata
    tfidf_matrix = vectorizer.fit_transform(books["combined_meta"])

    return books, vectorizer, tfidf_matrix

def recommend_books(
    fav_titles,         # User-entered favorite books
    books,              # Books dataset
    tfidf_matrix,       # Model
    num_of_rec=10       # Max number of recommendations defaults to 10
):
    """Recommend books based on user-entered favorite books."""

    # Normalize the titles entered by the user
    cleaned_titles = []
    
    for title in fav_titles:
        if isinstance(title, str) and title.strip():
            cleaned_title = title.strip().casefold()
            cleaned_titles.append(cleaned_title)

    # Normalize the titles in dataset
    normalized_titles = books["title"].fillna("").str.casefold()

    # Find the positions of favorite books in the dataset
    fav_indices = np.flatnonzero(
        normalized_titles.isin(cleaned_titles).to_numpy()
    ).tolist()

    # Check if no favorite titles were found in dataset
    if not fav_indices:
        print("No matching favorite books found.")
        return books.iloc[0:0].copy()

    # Create a user profile by averaging the favorite book vectors
    # TODO: Currently, takes into account all favorite books equally,
    #       change to allow users to put weight to their favorite books
    user_profile = np.asarray(
        tfidf_matrix[fav_indices].mean(axis=0)
    )

    # TODO: Currently, just uses the similarity scoring to sort books,
    #       change to take into account other aspects, such as number of 5 stars, awards, and liked percent
    
    # Calculate similarity between the user profile and every book
    scores = linear_kernel(user_profile, tfidf_matrix).ravel()

    # Exclude books the user has already selected as favorites
    scores[fav_indices] = -1

    # Sort book positions from highest to lowest similarity
    ranked_indices = np.argsort(scores)[::-1]

    # Keep only books with positive similarity scores
    recommended_indices = []

    for idx in ranked_indices:
        if scores[idx] > 0:
            recommended_indices.append(idx)

        # Stop if number of recommendations has been met
        if len(recommended_indices) >= num_of_rec:
            break

    # Select the recommended books using their indices
    recommendations = books.iloc[recommended_indices].copy()

    # Include similarity score for each recommended book
    recommendations["sim_score"] = scores[recommended_indices]

    return recommendations
# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 11/30/26
# Desc: A program to train and recommend a user books based on their entered favorite books.

# IMPORTS
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# CONSTANTS
# Percentage of how important each attribute is to recommending a book
DEFAULT_WEIGHTS = {
    "bayesian": 0.4,     # Bayesian rating-- will prevent books with high-score reviews but low number of reviewers from dominating ranking 
    "liked": 0.3,        # Liked percentage
    "five_stars": 0.2,   # 5 star rating percentage
    "awards": 0.1       # Book awards percentage
}

# FUNCTIONS
def five_star_rate(ratingsbystars):
    """Calculates the percentage of 5 star ratings for a book
    based on the 'ratingsByStars' column in the dataset that holds
    ratings in the order of: [5, 4, 3, 2, 1]."""

    try:
        # Convert list of starts into NumPy array
        np_stars = np.asarray(ratingsbystars, dtype=float)

        if len(np_stars) == 5 and np_stars.sum() > 0:
            # Return number of 5 star ratings divided by total number of ratings
            return np_stars[0] / np_stars.sum()
        else: 
            # Return null if something is wrong with the stars array or number of ratings
            np.nan
    except (TypeError, ValueError):
        return np.nan

def book_quality(books, weights=None):
    """Determines the overall quality for each book in the dataset given the provided weights,
    or uses default weights if none are provided. Provides a score between 0-1 of how well each book is liked."""
    weights = weights or DEFAULT_WEIGHTS
    parts = {}  # Stores each quality measurement 

    # Bayesian rating
    if "rating" in books and "numratings" in books:
        rating = pd.to_numeric(books["ratings"], errors="coerce").astype("float64") # Average rating for the book
        num_ratings = pd.to_numeric(books["numratings"], errors="coerce").astype("float64").fillna(0) # Total number of ratings the book recieved
        avg_rating = rating.mean() # Average book rating across whole dataset
        median_ratings = max(float(num_ratings()), 1.0) # Median number of ratings across whole dataset

        # Bayesian calculation-- will prevent books with high-score reviews but low number of reviewers from dominating ranking 
        parts["bayesian"] = (num_ratings / (num_ratings + median_ratings)) * rating.fillna(avg_rating) + (median_ratings / (num_ratings + median_ratings)) * avg_rating 

    # Liked percentage-- Returns percentage of readers who liked the book
    if "likedpercent" in books:
        parts["liked"] = pd.to_numeric(books["likedpercent"], errors="coerce").astype("float64")

    # 5 star percentage-- Returns proportion of 5 star ratings
    if "ratingsbystars" in books:
        parts["five_stars"] = books["ratingsbystars"].apply(five_star_rate)

    # Awards-- Returns how many awards each book received
    if "awards" in books:
        # Checks awards is in a list format, uses natural log of 1 + award count to apply diminishing returns to books with large number of awards
        parts["awards"] = np.log1p(books["awards"].apply(lambda a: len(a) if isinstance(a, list) else 0))

    # Get rid of measurements without a defined weight
    parts = {key: value for key, value in parts.items() if key in weights}

    # If no quality measurements available, return an array of zeros 
    if not parts:
        return np.zeros(len(books))

    # Calculate total weight of available measurements
    total = sum(weights[key] for key in parts)

    # Combine measurements into an overall quality score between 0 and 1
    score = sum(weights[key].rank(pct=True).fillna(0.5) for key in parts) / total

    # Return the quality scores for each book as a NumPy array that cooresponds to the same row as the book
    return score.to_numpy(dtype=float)

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
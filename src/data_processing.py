# Author: Rachal Thornton
# Class: CS445-01 Artificial Intelligence
# Due: 
# Desc: A program to clean a csv file storing book information

# IMPORTS
import pandas as pd
from ast import literal_eval
from pathlib import Path

# FUNCTION
def clean_books(input: Path, output: Path):
    # Define data types in schema
    user_schema = {
        'id': 'int',
        'title': 'str',
        'series': 'str',
        'author': 'str',
        'rating': 'float64',
        'description': 'str',
        'language': 'str',
        'isbn': 'double',
        'bookFormat': 'str',
        'edition': 'str',
        'pages': 'str',
        'publisher': 'str',
        'publishDate': 'str',
        'firstPublishDate': 'str',
        'numRatings': 'Int64',
        'likedPercent': 'Int64',
        'bbeScore': 'Int64',
        'bbeVotes': 'Int64',
        'price': 'float64' 

    }

    # Define list data types, parses list string into actual list
    user_converters = {
        'genres': literal_eval,
        'characters': literal_eval,
        'awards': literal_eval,
        'ratingsByStars': literal_eval, # List of num of ratings recieved for each star [5, 4, 3, 2, 1]
        'setting': literal_eval
    }

    # Read raw books csv
    books = pd.read_csv(input, dtype=user_schema, converters=user_converters, low_memory=True)
    raw_books = len(books)

    # Standardize column names
    books.columns = (
        books.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    # Check for required columns
    required = ["title", "author", "description", "language"]
    missing = [c for c in required if c not in books.columns]

    # Raise error if missing columns
    if missing:
        raise ValueError(
            f"Dataset is missing columns: {missing}. "
            f"Available columns: {list(books.columns)}"
        )

    # Drop books without required information
    books = books.dropna(subset=["title", "author"])

    # Remove books with empty titles or authors
    books = books[
        (books["title"] != "") &
        (books["author"] != "")
    ].copy()

    # Remove non-English language books
    books["language"] = books["language"].str.strip().str.lower()
    books = books[
        books["language"].isin(["english", "eng", "en"])
    ].copy()

    # Clean descriptions and handle missing values
    books["description"] = books["description"].fillna("").str.strip()

    # Remove duplicate books that have same title and author
    books = books.drop_duplicates(subset=["title", "author"])

    # Reset row indexes after removing books
    books = books.reset_index(drop=True)

    # Saved cleaned output to new output CSV file
    books.to_csv(output, index=False)

    # Print out summary
    print("Data cleaning complete.")
    print(f"Number of raw books: {raw_books}")
    print(f"Number of cleaned books: {len(books)}")
    print(f"Saved cleaned data to: {output}")

    return books

# TESTING
if __name__ == "__main__":
    input_path = Path("ai-book-project/data/books.csv")
    output_path = Path("ai-book-project/data/books_cleaned.csv")
    books = clean_books(input_path, output_path)

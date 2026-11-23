# MetaReads
> MetaReads is a book recommendation software that uses your favorite books to suggest you something new to read.

## About
MetaReads is a student-led final project developed for Winona State University's *CS445 Artificial Intelligence* class. It demonstrates concepts taught throughout the semester, focusing on a TF-IDF/embeddings hybrid recommendation model.

Using book data from a *[Price Prediction Dataset](https://www.kaggle.com/competitions/book-prices-prediction/data?select=books_train.csv)* on Kaggle, a cleaned CSV file of raw books data was created. From there, a weighted TF-IDF/embeddings recommender was built using Python libraries and machine learning concepts. Different factors, such as a book's liked percentage or number of five-star ratings, determine how closely a book aligns with a user's previously-read book. The recommender will return a list of books that have the closest score, with the assumption that these books are ones that the user is most likely to enjoy from the dataset.

## Data Sources
- [Kaggle Books Dataset](https://www.kaggle.com/competitions/book-prices-prediction/data?select=books_train.csv)
- [OpenLibrary's Book Cover API](https://openlibrary.org/dev/docs/api/covers)

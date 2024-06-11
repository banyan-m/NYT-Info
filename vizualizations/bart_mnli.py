import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import sqlite3
from transformers import pipeline



# Establish a connection to the SQLite database
conn = sqlite3.connect('nyt_articles.db')

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch the data
cur.execute("SELECT snippet FROM articles WHERE snipembedding IS NOT NULL LIMIT 10")
rows = cur.fetchall()

# Close the database connection
cur.close()
conn.close()

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Specify the candidate labels
candidate_labels = ['happy', 'sad', 'angry']

# Classify the sequences
for row in rows:
    sequence_to_classify = row[0]
    result = classifier(sequence_to_classify, candidate_labels)
    print(result)

import sqlite3
import json
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open('config.json') as f:
    config = json.load(f)
Openapi_key = config['openAIKey']

# Connect to the SQLite database
conn = sqlite3.connect('nyt_articles.db')
c = conn.cursor()

# Query the data
c.execute('SELECT title, keywords FROM articles LIMIT 10')
rows = c.fetchall()

# Close the connection
conn.close()

# Define the OpenAI API endpoint and headers
url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
headers = {'Authorization': Openapi_key, 'Content-Type': 'application/json'}

# Get the embeddings for each entry
embeddings = []
for row in rows:
    data = {'prompt': ' '.join(row), 'max_tokens': 1}
    response = requests.post(url, headers=headers, json=data)
    embeddings.append(response.json()['choices'][0]['embeddings'])

# Convert the embeddings to a NumPy array
embeddings = np.array(embeddings)

# Perform a vector similarity search on a specific word
word = 'your_word'
word_embedding = ...  # Get the embedding for the word using the OpenAI API
word_embedding = np.array(word_embedding)
similarities = cosine_similarity(embeddings, word_embedding.reshape(1, -1))

# Print the entries with the highest similarity
top_indices = np.argsort(similarities, axis=0)[-5:]
for index in top_indices:
    print(rows[index])
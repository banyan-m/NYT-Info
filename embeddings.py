import sqlite3
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai


# Load API key
with open('config.json') as f:
    config = json.load(f)
OAIapi_key = config['openAIKey']

# Set the API key for the openai module
openai.api_key = OAIapi_key

# Connect to SQLite database
conn = sqlite3.connect('nyt_articles.db')  # replace with your database name
cursor = conn.cursor()

# Write your SQL query here
query = "SELECT snippet FROM articles LIMIT 5"  # replace with your query

# Execute the query and fetch all results
cursor.execute(query)
rows = cursor.fetchall()

# Loop through the rows and create embeddings
for row in rows:
    text = row[0]  # replace 0 with the index of the text in each row
    response = openai.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        encoding_format="float"
    )
    print(response.data[0].embedding)

# Close the connection
conn.close()
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

cursor.execute("PRAGMA table_info(articles)")
columns = [column[1] for column in cursor.fetchall()]
if "snipembedding" not in columns:
    cursor.execute("ALTER TABLE articles ADD COLUMN snipembedding TEXT")

# Write your SQL query here
query = "SELECT rowid, snippet FROM articles LIMIT 5"  # replace with your query

# Execute the query and fetch all results
cursor.execute(query)
rows = cursor.fetchall()

# Loop through the rows and create embeddings
for row in rows:
    rowid = row[0]
    text = row[1]
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float"
        )
        embedding = response.data[0].embedding

        cursor.execute("UPDATE articles SET snipembedding = ? WHERE rowid = ?", (json.dumps(embedding), rowid))
    except Exception as e:
        print(f"Failed to create embedding for row {rowid}: {e}")


# Close the connection
conn.commit()
conn.close()
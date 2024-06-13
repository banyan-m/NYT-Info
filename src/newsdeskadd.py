import sqlite3
import requests
import json 

# Load the API key from the config file
with open('config.json') as f:
    config = json.load(f)
api_key = config['nytApiKey']


# Connect to the database
conn = sqlite3.connect('nyt_articles.db')
c = conn.cursor()


# Define the base URL and your API key
base_url = 'https://api.nytimes.com/svc/archive/v1'


# Define the year and month you want to query
year = 2024

for month in range(1, 13):
    url = f'{base_url}/{year}/{month}.json?api-key={api_key}'

    # Make the request
    response = requests.get(url)

    # Check the status code of the response
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        docs = data['response']['docs']
        for doc in docs:
            # Extract the 'news_desk' value and the 'pub_date'
            news_desk = doc['news_desk']
            pub_date = doc['pub_date']

            # Check if the publication date exists in the database
            c.execute("SELECT 1 FROM articles WHERE pub_date = ?", (pub_date,))
            if c.fetchone() is not None:
                # If the publication date exists, update the corresponding row in the 'articles' table
                c.execute("UPDATE articles SET news_desk = ? WHERE pub_date = ?", (news_desk, pub_date))

# Commit the changes
conn.commit()

# Close the database connection
conn.close()
import requests
import json
import sqlite3
from pprint import pprint


# Load the API key from the config file
with open('config.json') as f:
    config = json.load(f)
api_key = config['nytApiKey']

# Define the base URL of the API
base_url = 'https://api.nytimes.com/svc/archive/v1'

conn = sqlite3.connect('nyt_articles.db')
c = conn.cursor()

# Create a table in the database
c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        pub_date TEXT,
        snippet TEXT,
        abstract TEXT,
        keywords TEXT,
        headline TEXT,
        lead_paragraph TEXT
    )
''')

# Define the year and month you want to query

for month in range(1, 13):
    year = 2024
    url = f'{base_url}/{year}/{month}.json?api-key={api_key}'

        # Make the request
    response = requests.get(url)

        # Check the status code of the response
    if response.status_code == 200:
            # Parse the response as JSON
        data = response.json()
        docs = data['response']['docs']
        for doc in docs:
                # Extract the fields
            pub_date = doc['pub_date']
            snippet = doc['snippet']
            abstract = doc['abstract']
            keywords = ', '.join([keyword['value'] for keyword in doc['keywords']])
            headline = doc['headline']['main']
            lead_paragraph = doc['lead_paragraph']

                # Insert the data into the database
            c.execute('''
                INSERT INTO articles (pub_date, snippet, abstract, keywords, headline, lead_paragraph)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (pub_date, snippet, abstract, keywords, headline, lead_paragraph))

            # Commit the changes
        conn.commit()

    else:
        print(f'Failed to fetch data for {month}/{year}: HTTP {response.status_code}')

# Close the connection
conn.close()


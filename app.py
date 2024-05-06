#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------
import requests
import json
from pprint import pprint


# Load the API key from the config file
with open('config.json') as f:
    config = json.load(f)
api_key = config['nytApiKey']

# Define the base URL of the API
base_url = 'https://api.nytimes.com/svc/archive/v1'

# Define the year and month you want to query
year = 2024
month = 1

# Construct the full URL
url = f'{base_url}/{year}/{month}.json?api-key={api_key}'

# Make the request
response = requests.get(url)

# Check the status code of the response
if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()
    pprint(list(data.items())[:100]) 
    # Now you can work with the data as needed
else:
    print(f'Failed to fetch data: HTTP {response.status_code}')


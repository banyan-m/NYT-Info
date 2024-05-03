#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------
import requests
import json
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# Please note: f-strings require Python 3.6+

# The URL of the Common Crawl Index server
CC_INDEX_SERVER = 'http://index.commoncrawl.org/'

# The Common Crawl index you want to query
INDEX_NAME = 'CC-MAIN-2023-40'      # Replace with the latest index name

# The URL you want to look up in the Common Crawl index
target_url = 'pitchfork.com'  # Replace with your target URL

# Function to search the Common Crawl Index
def search_cc_index(url):
    encoded_url = quote_plus(url)
    index_url = f'{CC_INDEX_SERVER}{INDEX_NAME}-index?url={encoded_url}&output=json'
    response = requests.get(index_url)
    print("Response from CCI:", response.text)  # Output the response from the server
    if response.status_code == 200:
        records = response.text.strip().split('\n')
        return [json.loads(record) for record in records]
    else:
        return None

# Function to fetch the content from Common Crawl
def fetch_page_from_cc(records):
    for record in records:
        offset, length = int(record['offset']), int(record['length'])
        prefix = record['filename'].split('/')[0]
        s3_url = f'https://data.commoncrawl.org/{record["filename"]}'
        response = requests.get(s3_url, headers={'Range': f'bytes={offset}-{offset+length-1}'})
        if response.status_code == 206:
            # Process the response content if necessary
            # For example, you can use warcio to parse the WARC record
            return response.content
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None

# Search the index for the target URL
records = search_cc_index(target_url)
if records:
    print(f"Found {len(records)} records for {target_url}")

    # Fetch the page content from the first record
    content = fetch_page_from_cc(records)
    if content:
        print(f"Successfully fetched content for {target_url}")
        # You can now process the 'content' variable as needed
else:
    print(f"No records found for {target_url}")





def fetch_content_from_common_crawl(filename, offset, length):
    """
    Fetches content from a Common Crawl WARC file given filename, offset, and length.
    
    Args:
        filename (str): The name of the WARC file.
        offset (int): The byte offset where the content starts in the WARC file.
        length (int): The length of the content in bytes.
    
    Returns:
        bytes: The content retrieved from the WARC file, or None if unsuccessful.
    """
    # Construct the full URL to access the Common Crawl data
    base_url = "https://data.commoncrawl.org/"
    full_url = f"{base_url}{filename}"

    # Calculate the range of bytes to fetch
    byte_range = f"bytes={offset}-{offset + length - 1}"

    # Make an HTTP GET request with the appropriate range header
    response = requests.get(full_url, headers={"Range": byte_range})

    if response.status_code == 206:  # HTTP status code 206 means "Partial Content"
        return response.content
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return None

# Example usage
filename = "crawl-data/CC-MAIN-2023-40/segments/1695233506329.15/warc/CC-MAIN-20230922034112-20230922064112-00893.warc.gz"
offset = 211129121
length = 7271

content = fetch_content_from_common_crawl(filename, offset, length)
if content:
    print("Successfully retrieved content.")
    # If the content is HTML or plain text, you might want to print it out
    print(content.decode('utf-8'))  # Uncomment this line to print the content
else:
    print("Content retrieval failed.")
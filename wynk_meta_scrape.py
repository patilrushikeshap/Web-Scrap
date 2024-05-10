import os
import re
import time
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langcodes import Language

# Read csv having urls
path = "C://Users//patil//Downloads//New folder//ab.csv"
df = pd.read_csv(f"{path}")
file_name = os.path.basename(f"{path}")
urls = df['Joined_URL'].tolist()
csv_rows = []


# Mapping short forms of language to long
def map_language(short_code):
    try:
        language = Language.get(short_code)
        return language.display_name()
    except ValueError:
        return short_code


count = 0

# Data fetching
for url in urls:
    count += 1
    print(count)

    response = None

    try:
        response = requests.get(url)
        if response.status_code == 404:
            pass
    except requests.ConnectionError as ce:
        print(f"Connection error for URL: {url} - {str(ce)}")
        retry_count = 0
        max_retries = 200
        while retry_count < max_retries:
            print(f"Retrying... (Attempt {retry_count + 1} of {max_retries})")
            time.sleep(5)  # Wait for 5 seconds before retrying
            try:
                response = requests.get(url)
                response.raise_for_status()
                break
            except requests.ConnectionError:
                retry_count += 1

    table_rows = {"url": url}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_element = soup.find('h1', class_='heading1')
        if h1_element:
            title = h1_element.text.strip()
            table_rows["title"] = title

        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                row_data = row.find_all('td')
                table_rows[row_data[0].text] = row_data[1].text
            match = re.search(r'ab_([^/]+)', url)

            if match:
                value = match.group(1)

                if '_' in value:
                    parts = value.split('_')
                    for part in parts:
                        if re.match(r'\b(?![0-9]+\b)[A-Za-z0-9]+\b', part):
                            table_rows["ISRC"] = part
                        elif re.match(r'^[0-9]*$', part):
                            table_rows["UPC"] = part
                        else:
                            print(f"Unknown Format: {part}")
                else:
                    if re.match(r'\b(?![0-9]+\b)[A-Za-z0-9]+\b', value):
                        table_rows["ISRC"] = value
                    elif re.match(r'^[0-9]*$', value):
                        table_rows["UPC"] = value
                    else:
                        print(f"Unknown Format: {value}")
            csv_rows.append(table_rows)
        else:
            print(f"Table not found on the page for URL: {url}")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code} for URL: {url}")

for d in csv_rows:
    print(d)
    try:
        d['Language'] = map_language(d['Language'])
    except Exception as e:
        print(e)
        pass

if csv_rows:
    csv_final = pd.DataFrame(csv_rows)  
    csv_final.to_csv(f"C:\study\Wynk\ab\Metadata{file_name}")
    csv_file = f'C:\study\Wynk\ab\Metadata{file_name}'
    df = pd.read_csv(f"C:\study\Wynk\ab\Metadata{file_name}")
    df = df.loc[:, df.columns.str.find('.') < 0]
    desired_sequence = ['url', 'title', 'Album/Movie', 'Singers', 'Producer', 'Lyricist', 'Language', 'Music Company',
                        'Duration', 'ISRC', 'UPC', 'Other']
    df = df[desired_sequence]
    df.to_csv(f"C:\study\Wynk\ab\Metadata{file_name}", index=False, encoding='utf-8-sig')
    print(f"Data saved to '{csv_file}'")
else:
    print("No data to save.")


import csv
import requests
import time

input_file = 'scripture.csv'      # Use your file name here
output_file = 'verses_with_text.csv'

def fetch_verse(reference):
    url = f'https://bible-api.com/{reference.replace(" ", "%20")}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('text', '').replace('\n', ' ').strip()
    else:
        return 'Not found'

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Text']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        verse_text = fetch_verse(row['Reference'])
        row['Text'] = verse_text
        writer.writerow(row)
        time.sleep(1)  # Be polite to the API!

print('Done! Check verses_with_text.csv')
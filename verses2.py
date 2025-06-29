import csv
import requests
from bs4 import BeautifulSoup
import time

def fetch_bible_gateway(reference, version='NIV'):
    # Format reference for URL
    ref_url = reference.replace(' ', '+')
    url = f"https://www.biblegateway.com/passage/?search={ref_url}&version={version}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Not found"
    soup = BeautifulSoup(response.text, 'html.parser')
    # Bible Gateway puts verse text in <div class="passage-text">
    passage_div = soup.find('div', class_='passage-text')
    if not passage_div:
        return "Not found"
    # Remove crossrefs and footnotes
    for tag in passage_div.find_all(['sup', 'span', 'div'], class_=['crossreference', 'footnote', 'chapternum', 'versenum']):
        tag.decompose()
    text = passage_div.get_text(separator=' ', strip=True)
    return text

input_file = 'scripture.csv'
output_file = 'verses.csv'

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Text']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        verse_text = fetch_bible_gateway(row['Reference'])
        row['Text'] = verse_text
        writer.writerow(row)
        print(f"Fetched: {row['Reference']}")
        time.sleep(2)  # Be polite to Bible Gateway!

print('Done! Check verses.csv')
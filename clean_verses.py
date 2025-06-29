import csv
import re

input_file = 'verses2.csv'
output_file = 'verses2_cleaned.csv'

def clean_text(text):
    # Remove everything from "Read" onward (case-insensitive)
    cleaned = re.split(r'\bRead\b', text, flags=re.IGNORECASE)[0].strip()
    # Ensure text is wrapped in double quotes and escape any existing quotes
    cleaned = '"' + cleaned.replace('"', '""') + '"'
    return cleaned

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for row in reader:
        if 'Text' in row and row['Text']:
            row['Text'] = clean_text(row['Text'])
        writer.writerow(row)

print('Done! Check verses2_cleaned.csv')
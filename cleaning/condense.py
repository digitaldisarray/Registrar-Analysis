import json
import csv
import os
import re

def extract_date(filename):
    base = os.path.basename(filename)
    date_str = base.split('-')[3] + '-' + base.split('-')[4] + '-' + base.split('-')[5].split('T')[0]
    return date_str

def process_json_file(fname, date, rows):
    with open(fname, 'r', encoding='utf-8') as json_file:
        content = json_file.read()
        if not content.strip():
            print(f"Error: The file {fname} is empty.")
            return
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {fname}: {e}")
            return
    
    for tld, tld_data in data.get('data', {}).items():
        registrars = tld_data.get('registrars', {})
        for registrar, registrar_data in registrars.items():
            prices = registrar_data.get('price', {})
            for price_type, price in prices.items():
                if price and price_type != "whois_privacy":
                    rows.append([tld, date, price_type, price, registrar])

def main():
    directory = '/data/tld-list-daily'
    json_pattern = re.compile(r'tld-list-full-\d{4}-\d{2}-\d{2}\.json')
    csv_filename = 'tld-list-daily-combined.csv'
    rows = []

    json_files = [f for f in os.listdir(directory) if json_pattern.match(f)]
    
    if not json_files:
        print("No files with name scheme 'tld-list-full-YYYY-MM-DD.json' found")
        return
    
    for json_file in json_files:
        fname = os.path.join(directory, json_file)
        date = extract_date(json_file)
        process_json_file(fname, date, rows)
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['tld', 'date', 'price-type', 'price', 'registrar'])
        writer.writerows(rows)
    
    print(f"Data has been written to {csv_filename}")

if __name__ == "__main__":
    main()


# make /data/all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names.json

import pandas as pd

bad_domains_path = '/data/all_types_domains_balanced_registered_domains_whois_parsed.json'
registar_domain_count_path = '/data/registrar_domain_count_flat.json'

# Bad_domains has incorrect registrar names
bad_domains = pd.read_json(bad_domains_path, lines=True)

# The json with domain counts has correct registrar names
registrar_domain_count = pd.read_json(registar_domain_count_path)

# Create a dictionary that maps registrar_id to registrar name
registrar_dict = registrar_domain_count.set_index('id')['name'].to_dict()

# Map the registrar_id from bad_domains to the correct registrar name using the dictionary
bad_domains['registrar'] = bad_domains['registrar_id'].map(registrar_dict)

# Optionally, save the updated bad_domains to a new JSON file
bad_domains.to_json('/data/all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names.json', orient='records', lines=True)

# Print the first few updated rows to verify
print(bad_domains[['domain', 'registrar']].head())


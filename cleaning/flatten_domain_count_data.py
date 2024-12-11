import json

# Step 1: Read the JSON data from the file
file_path = '/data/registrar_domain_count.json'
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Step 2: Extract the data under the "top" key and overwrite the root structure
json_data_flat = json_data["top"]

# Step 3: Save the flattened JSON to a new file
flattened_file_path = '/data/registrar_domain_count_flat.json'
with open(flattened_file_path, 'w') as file:
    json.dump(json_data_flat, file)
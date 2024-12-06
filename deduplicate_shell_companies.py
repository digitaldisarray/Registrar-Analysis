import pandas as pd
import json
import re

# Load the JSON data into a DataFrame
df = pd.read_json('/data/registrar_domain_count_flat.json')
print("Starting data:")
print(df)

# Normalize names by removing numbers and extra spaces
def clean_name(name):
    if pd.isnull(name):
        return name
    return re.sub(r'\d+', '', name).strip()

df['cleaned_name'] = df['name'].apply(clean_name)

# Identify duplicates and print them out
duplicates = df[df.duplicated(subset='cleaned_name', keep=False)]
print("Duplicates found:")
print(duplicates)

# Create a map of ID changes and merge data accordingly
# Group by cleaned name and aggregate data
grouped = df.groupby('cleaned_name').agg({
    'id': 'first',  # Choose the first ID as the new ID for this group
    'name': 'first',
    'domains': 'sum',
    'share': 'sum',
    'tlds': 'max',
    'signedZones': 'sum', # I think its correct to sum these?
    'upcomingDeletes': 'sum', # I think its correct to sum these?
}).reset_index()

grouped.to_json('grouped.json', index=False)

# Create a mapping of old IDs to new IDs
# Also (optionally) print changes for sanity check
id_map = {}
name_id_list = pd.DataFrame(columns=['new_name', 'new_id'])
for _, row in grouped.iterrows():
    new_id = row['id']
    old_ids = df[df['cleaned_name'] == row['cleaned_name']]['id'].tolist()
    for old_id in old_ids:
        if old_id != new_id:
            id_map[old_id] = new_id
            old_name = df[df['id'] == old_id]['name'].values[0]  # Get the original name of the old ID
            cleaned_name = row["cleaned_name"]
            new_name = row["name"]
            # debug print
            #print(f"ID {old_id} ({old_name}) with cleaned name '{cleaned_name}' becomes ID {new_id} ({new_name})")
            name_id_list.loc[len(name_id_list)] = [new_name, new_id]

name_id_list.drop_duplicates().to_csv('name_id_list.csv', index=False)
            

# Apply the id mappings to the reports
reports = pd.read_json("/data/all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names.json", lines=True)
reports = reports.dropna(subset=['registrar_id']) # drop null registrar ids
for index, row in reports.iterrows():
    if int(row["registrar_id"]) not in id_map:
        continue
    name = row["registrar"]
    old_id = row["registrar_id"]
    new_id = id_map[old_id]
    # debug print
    #print(f"Remapping {old_id} for {name} to {new_id}")
    reports.loc[index, "registrar_id"] = new_id
    reports.loc[index, "registrar"] = grouped[grouped["id"] == new_id]["name"].values[0] #get new name
reports.to_json("/data/all_types_domains_balanced_registered_domains_whois_parsed_correct_registrar_names_deduplicated_ids.json", orient='records', lines=True)

# Save the id mappings for use in correcting other datasets
with open("/data/id_mappings_for_deduplication.json", "w") as f:
    f.write(json.dumps(id_map))

# Save the grouped registrars
grouped.drop('cleaned_name', axis=1, inplace=True) # Drop cleaned name
#print("Grouped:")
#print(grouped)
grouped.to_json("/data/registrar_domain_count_flat_deduplicated.json", orient='records', lines=True)


print("wrote files to disk")



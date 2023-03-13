import json

# Load the JSON file
with open('./static/pokemon_data.json', 'r') as f:
    data = json.load(f)

# Loop through each Pokemon object
for pokemon in data:
    # Calculate the total base stats
    total_base_stats = sum(stat['base_stat'] for stat in pokemon['stats'])

    # Add the new attribute to the Pokemon object
    pokemon['total_base_stats'] = total_base_stats

# Save the updated data to a new JSON file
with open('./static/pokemon_data.json', 'w') as f:
    json.dump(data, f, indent=4)

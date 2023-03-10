import requests
import json

# Define the URL for the PokeAPI
url = "https://pokeapi.co/api/v2/pokemon/"

# Create an empty list to hold the Pokemon data
pokemon_data_list = []

# Loop over the first 151 Pokemon and grab their data
for i in range(1, 152):
    # Construct the URL for this Pokemon
    pokemon_url = url + str(i)

    # Make a GET request to the API
    response = requests.get(pokemon_url)

    # If the request was successful, extract the data we need
    if response.status_code == 200:
        pokemon_data = response.json()
        
        # Extract the name
        name = pokemon_data['name']
        
        # Extract the stats
        stats = pokemon_data['stats']
        
        # Extract the front sprite URL
        front_sprite_url = pokemon_data['sprites']['front_default']
        
        # Extract the types
        types = [t['type']['name'] for t in pokemon_data['types']]
        
        # Extract the moves
        moves = [m['move']['name'] for m in pokemon_data['moves']]
        
        # Extract the abilities
        abilities = [a['ability']['name'] for a in pokemon_data['abilities']]
        
        # Create a dictionary with the Pokemon data
        pokemon_dict = {
            "id": i,
            "name": name,
            "stats": stats,
            "front_sprite_url": front_sprite_url,
            "types": types,
            "moves": moves,
            "abilities": abilities
        }
        
        # Add the dictionary to the list of Pokemon data
        pokemon_data_list.append(pokemon_dict)

# Write the Pokemon data to a JSON file
with open("pokemon_data.json", "w") as f:
    json.dump(pokemon_data_list, f, indent=4)

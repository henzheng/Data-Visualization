import requests
import json

# URL for the PokeAPI
url = 'https://pokeapi.co/api/v2/'

# Get a list of all the types
types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon']

# Get a list of all the first generation Pokémon
pokemons_response = requests.get(url + 'pokemon', params={'limit': 151}).json()
pokemons = [pokemon['name'] for pokemon in pokemons_response['results']]

print(pokemons)
# Initialize the JSON data structure
data = {'name': 'flare', 'children': []}

# Loop through each type
for type in types:
    # Initialize the type data structure
    type_data = {'name': type.capitalize(), 'children': []}
    # Loop through each Pokemon of the current type
    for pokemon in pokemons:
        # Make a request for the current Pokemon's data
        pokemon_response = requests.get(url + 'pokemon/' + pokemon).json()
        # Get a list of all the type names for the current Pokemon
        pokemon_types = [type['type']['name'] for type in pokemon_response['types']]
        # print(pokemon_types)
        # Check if the current type is in the list of type names for the current Pokemon
        if type in pokemon_types:
            # Initialize the Pokemon data structure
            pokemon_data = {
                'name': pokemon_response['name'].capitalize(),
                'id': pokemon_response['id'],
                'api_url': url + 'pokemon/' + str(pokemon_response['id']),
                'front_sprite_url': pokemon_response['sprites']['front_default'],
                'abilities': [ability['ability']['name'].capitalize() for ability in pokemon_response['abilities']],
                'stats': pokemon_response['stats'],
                'total_base_stats': sum([stat['base_stat'] for stat in pokemon_response['stats']])
            }
            
            # Add the Pokemon data to the type data
            print(f"Done adding {pokemon_response['name']} to {type}")
            type_data['children'].append(pokemon_data)
    
    # Add the type data to the root data
    data['children'].append(type_data)

# Write the output to a JSON file
with open('pokeapi_data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
print('DONE')

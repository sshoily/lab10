import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Get user input for the Pokémon name
    pokemon_name = input("Enter the name or Pokedex number of the Pokémon: ").strip()
    
    # Test out the get_pokemon_info() function
    poke_info = get_pokemon_info(pokemon_name)

    if poke_info:
        # Display some key information about the Pokémon
        print_pokemon_info(poke_info)
    else:
        print("Could not retrieve Pokémon information.")

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokémon from the PokeAPI.

    Args:
        pokemon (str): Pokémon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokémon information, if successful. Otherwise None.
    """
    # Clean the Pokémon name parameter
    pokemon = str(pokemon).strip().lower()

    # Check if Pokémon name is an empty string or contains special characters
    if not pokemon.isalnum():
        print('Error: Pokémon name must contain only letters or numbers.')
        return None

    if pokemon == '':
        print('Error: No Pokémon name specified.')
        return None

    # Send GET request for Pokémon info
    try:
        print(f'Getting information for {pokemon.capitalize()}...', end='')
        url = POKE_API_URL + pokemon
        resp_msg = requests.get(url)

        # Check if request was successful
        if resp_msg.status_code == requests.codes.ok:
            print('success')
            # Return dictionary of Pokémon info
            return resp_msg.json()
        else:
            print('failure')
            print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error: Unable to retrieve data ({e})')
        return None

def print_pokemon_info(poke_info):
    """Displays key information about the Pokémon.

    Args:
        poke_info (dict): Dictionary of Pokémon information
    """
    # Example of some key information to display
    name = poke_info['name'].capitalize()
    height = poke_info['height']
    weight = poke_info['weight']
    types = ', '.join([t['type']['name'] for t in poke_info['types']])
    
    print(f"\nPokémon: {name}")
    print(f"Height: {height} decimetres")
    print(f"Weight: {weight} hectograms")
    print(f"Type(s): {types}")

if __name__ == '__main__':
    main()

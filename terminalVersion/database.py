from os.path import splitext
import csv
from Pokemon import Pokemon


class MalformedPokemonDataError(Exception):
    pass


class InvalidPokemonError(Exception):
    pass


class PokemonsPathNotFound(FileNotFoundError):
    pass

class PokemonPermissionDenied(PermissionError):
    pass


class Database:
    def __init__(self) -> None:
        pass

    def load_from_file(self, path):
        """
        Load pokemon data from file
        :path: path to the file
        """
        try:
            with open(path, 'r', encoding="utf-8") as file_handle:
                pokemons = read_from_csv(file_handle)
        except FileNotFoundError:
            raise PokemonsPathNotFound("Could not open database")
        except PermissionError:
            raise PokemonPermissionDenied("No permission to file")
        except IsADirectoryError:
            raise IsADirectoryError("It is not file, it is directory")
        return pokemons


def read_from_csv(file_handle):
    """
    Reads file from csv file
    :file_handle: handle of given file
    """
    pokemons = []
    reader = csv.DictReader(file_handle,
        [
            "abilities", 'against_bug', 'against_dark', 'against_dragon',
            'against_electric', 'against_fairy', 'against_fight',
            'against_fire', 'against_flying', 'against_ghost',
            'against_grass', 'against_ground', 'against_ice',
            'against_normal', 'against_poison', 'against_psychic',
            'against_rock', 'against_steel', 'against_water', 'attack',
            'base_egg_steps', 'base_happiness', 'base_total',
            'capture_rate', 'classfication', 'defense', 'experience_growth',
            'height_m', 'hp', 'japanese_name', 'name',
            'percentage_male', 'pokedex_number', 'sp_attack', 'sp_defense',
            'speed', 'type1', 'type2', 'weight_kg', 'generation',
            'is_legendary'
        ])
    pokemon_id = 1
    try:
        for row in reader:

            if(row['name'] == "name"):
                pass
            else:
                if None in row.values():
                    raise MalformedPokemonDataError("Missing column")
                try:
                    abilities_not_formatted = row['abilities'].strip()
                    normal_string = "".join(ch for ch in abilities_not_formatted if (ch.isalnum() or ch == ','))
                    abilities = normal_string.split(',')
                    weakness_against_types = {
                        'against_bug': row['against_bug'],
                        'against_dark': row['against_dark'],
                        'against_dragon': row['against_dragon'],
                        'against_electric': row['against_electric'],
                        'against_fairy': row['against_fairy'],
                        'against_fight': row['against_fight'],
                        'against_fire': row['against_fire'],
                        'against_flying': row['against_flying'],
                        'against_ghost': row['against_ghost'],
                        'against_grass': row['against_grass'],
                        'against_ground': row['against_ground'],
                        'against_ice': row['against_ice'],
                        'against_normal': row['against_normal'],
                        'against_poison': row['against_poison'],
                        'against_psychic': row['against_psychic'],
                        'against_rock': row['against_rock'],
                        'against_steel': row['against_steel'],
                        'against_water': row['against_water']
                    }
                    for weakness in weakness_against_types:
                        weakness_against_types[weakness] = float(weakness_against_types[weakness])
                    attack = int(row['attack'])
                    defense = int(row['defense'])
                    health = int(row['hp'])
                    name = row['name']
                    types = [row['type1'], row['type2']]
                    generation = int(row['generation'])
                    special_attack = int(row['sp_attack'])
                    special_defense = int(row['sp_defense'])
                    speed = int(row['speed'])
                    pokemon = Pokemon(
                        pokemon_id, abilities,
                        name, health, defense, attack, types, special_attack,
                        special_defense, weakness_against_types, speed,
                        generation
                    )
                except Exception as e:
                    raise InvalidPokemonError(row)
                pokemons.append(pokemon)
                pokemon_id += 1

    except Exception as e:
        raise e
    return pokemons

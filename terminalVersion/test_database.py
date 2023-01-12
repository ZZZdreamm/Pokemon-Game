from pytest import raises
from database import PokemonsPathNotFound, Database

def test_load_file_not_found_error():
    database = Database()
    with raises(PokemonsPathNotFound):
        database.load_from_file('d')

def test_load_file_no_error():
    database = Database()
    database.load_from_file('pokemon.csv')
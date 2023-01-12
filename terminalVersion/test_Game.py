from Game import Game
from database import Database

def test_creating_game_with_pokemons():
    database = Database()
    all_pokemons = database.load_from_file('pokemon.csv')
    game = Game(all_pokemons)
    assert game._all_pokemons[0]._name == 'Bulbasaur'


def test_creating_game_without_pokemons():
    game = Game()
    assert game._all_pokemons == None
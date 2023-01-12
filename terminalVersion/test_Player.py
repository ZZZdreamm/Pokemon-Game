from Pokemon import Pokemon
from io import StringIO
from database import read_from_csv
from pytest import raises
from Pokemon import NegativeParamError
from Player import Player, PokemonNotInListError

def test_create_player_without_pokemons():
    player = Player(1, 'Adam')
    assert player.current_fighter is None
    assert player._player_pokemons == []

def test_choosing_pokemon_to_team():
    player = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    bulbasaur_id = pokemons[0].id
    pokemon = player.choose_pokemon_to_your_team(bulbasaur_id, pokemons)
    assert player._player_pokemons == [pokemon]
    assert player._player_pokemons[0]._name == 'Bulbasaur'


def test_set_player_pokemons_add():
    player = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    player.set_player_pokemons(pokemons[0])
    assert player._player_pokemons == [pokemons[0]]


def test_set_player_pokemons_remove():
    player = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    player.set_player_pokemons(pokemons[0])
    assert player._player_pokemons == [pokemons[0]]
    player.set_player_pokemons(pokemons[0], add=False)
    assert player._player_pokemons == []


def test_set_player_pokemons_remove_error():
    player = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    with raises(PokemonNotInListError):
        player.set_player_pokemons(pokemons[0], add=False)


def test_choosing_fighter():
    player = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    player._player_pokemons = pokemons
    charmander_id =  player._player_pokemons[0].id
    player.choose_pokemon_to_fight(charmander_id)
    assert player.current_fighter._name == 'Charmander'

def test_choose_pokemon_move_defense():
    player1 = Player(1, 'Adam')
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    player1._player_pokemons = [pokemon]
    player1.current_fighter = pokemon
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    assert player1.current_fighter._defense == 49
    result = player1.choose_pokemon_move(1, player2)
    assert result == 'Bulbasaur raised his defense to 53.9'
    assert player1.current_fighter._defense == 53.9

def test_choose_pokemon_move_normal_attack(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = Player(1, 'Adam')
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,35,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    player1._player_pokemons = [pokemon]
    player1.current_fighter = pokemon
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    assert player2.current_fighter._health == 35
    result = player1.choose_pokemon_move(2, player2)
    assert result == 'Charmander took 2.05.\nHis current health is 32.95.'
    assert player2.current_fighter._health == 32.95

def test_choose_pokemon_move_normal_attack(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = Player(1, 'Adam')
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    player1._player_pokemons = [pokemon]
    player1.current_fighter = pokemon
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    assert player2.current_fighter._health == 39
    result = player1.choose_pokemon_move(2, player2)
    assert result == 'Bulbasaur used normal attack.\nCharmander took 2.05.\nHis current health is 36.95.'

def test_choose_pokemon_move_special_attack(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = Player(1, 'Adam')
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    player1._player_pokemons = [pokemon]
    player1.current_fighter = pokemon
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    assert player2.current_fighter._health == 39

    result = player1.choose_pokemon_move(3, player2, pokemon._types[1])
    assert result == 'Bulbasaur used poison attack.\nCharmander took 2.05.\nHis current health is 36.95.'
    assert player2.current_fighter._health == 36.95

def test_check_if_pokemon_died(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = Player(1, 'Adam')
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    player1._player_pokemons = [pokemon]
    player1.current_fighter = pokemon
    player1.current_fighter._health = 0
    assert player1.check_if_pokemon_died() == True

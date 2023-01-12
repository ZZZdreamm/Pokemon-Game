from Pokemon import Pokemon
from io import StringIO
from database import read_from_csv
from pytest import raises
from Pokemon import NegativeParamError

def test_create_pokemon():
    pokemon = Pokemon(1, ['p','f'], "Char", 1, 2 ,3, ['p'], 2, 3, [2,2,3], 2, 1)
    assert pokemon._health == 1

def test_creating_wrong_pokemon():
    with raises(NegativeParamError):
        Pokemon(1, ['p','f'], "Char", -1, 0 ,0, ['p'], 2, 3, [2,2,3], 2, 1)

def test_pokemon_defense():
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    assert pokemon._defense == 49
    assert pokemon.defense() == 53.9

def test_pokemon_normal_attack(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    damage_dealt, enemy_health = pokemon.attack('normal', enemy)
    assert damage_dealt == 2.05
    assert enemy_health == 36.95


def test_pokemon_normal_attack_weakness_multiplier(monkeypatch):
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    assert pokemon.weakness_multiplier('normal', enemy) == 1

def test_pokemon_special_attack_grass_type(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0')
    pokemons = read_from_csv(file)
    pokemon = pokemons[0]
    enemy = pokemons[1]
    damage_dealt, enemy_health = pokemon.attack("grass",enemy)
    assert damage_dealt == 1.03
    assert enemy_health == 37.97



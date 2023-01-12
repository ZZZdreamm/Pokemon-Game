from Player import Player
from Pokemon import Pokemon
from io import StringIO
from database import read_from_csv
from pytest import raises
from Pokemon import NegativeParamError
from ComputerPlayer import ComputerPlayer


def test_choose_best_fighter():
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [pokemon1, pokemon2]
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    pokemon1_potential = player1.calculate_pokemon_potential(pokemon1, enemy)
    pokemon2_potential = player1.calculate_pokemon_potential(pokemon2, enemy)
    assert pokemon1_potential == 1
    assert pokemon2_potential == 2
    assert pokemon2._name == 'Charmander'
    result = player1.choose_best_fighter(player2.current_fighter)
    assert player1.current_fighter._name == 'Charmander'


def test_choose_attack_normal():
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [pokemon1, pokemon2]
    player2._player_pokemons = [enemy]
    player1.current_fighter = pokemon1
    player2.current_fighter = enemy
    result = player1.choose_attack(player2.current_fighter)
    assert result == 'normal'



def test_choose_attack_special_fire():
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [pokemon1, pokemon2]
    player2._player_pokemons = [enemy]
    player1.current_fighter = pokemon2
    player2.current_fighter = enemy
    result = player1.choose_attack(player2.current_fighter)
    assert result == 'fire'


def test_choose_best_move_pokemon_not_being_countered(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [pokemon1, pokemon2]
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    player1.choose_best_fighter(player2.current_fighter)
    result = player1.do_best_move(player2)
    assert result == 'Charmander used fire attack.\nMetapod took 4.09.\nHis current health is 45.91.'



def test_choose_best_move_pokemon_being_countered(monkeypatch):
    def return_max(a, b):
        return 255
    monkeypatch.setattr('Pokemon.randint', return_max)
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [enemy, pokemon2]
    player2._player_pokemons = [pokemon1]
    player2.current_fighter = pokemon1
    player1.choose_best_fighter(player2.current_fighter)
    result = player1.do_best_move(player2)
    assert result == 'Charmander used fire attack.\nBulbasaur took 4.1.\nHis current health is 40.9.'


def test_calculate_pokemon_potential():
    computer = ComputerPlayer(1)
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    enemy = pokemons[1]
    potential = computer.calculate_pokemon_potential(pokemon1, enemy)
    assert potential == 0.5


def test_calculate_pokemon_attack_potential():
    computer = ComputerPlayer(1)
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    enemy = pokemons[1]
    attack_potential = computer.calculate_attack_potential(pokemon1, enemy)
    assert attack_potential == 1


def test_calculate_pokemon_attack_potential2():
    computer = ComputerPlayer(1)
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    enemy = pokemons[1]
    attack_potential = computer.calculate_attack_potential(enemy, pokemon1)
    assert attack_potential == 2


def test_calculate_if_there_is_better_pokemon():
    player1 = ComputerPlayer(1)
    player2 = Player(2, "Stasiek")
    file = StringIO('[Overgrow. Chlorophyll],1,1,1,0.5,0.5,0.5,2,2,1,0.25,1,2,1,1,2,1,1,0.5,49,5120,70,318,45,Seed PokĂ©mon,49,1059860,0.7,45,Fushigidan‚T,Bulbasaur,88.1,1,65,65,45,grass,poison,6.9,1,0\n[Blaze. Solar Power],0.5,1,1,1,0.5,1,0.5,1,1,0.5,2,0.5,1,1,1,2,0.5,2,52,5120,70,309,45,Lizard PokĂ©mon,43,1059860,0.6,39,Hitokage‚ZA‚M,Charmander,88.1,4,60,50,65,fire,,8.5,1,0\n[Shed Skin],1,1,1,1,1,0.5,2,2,1,0.5,0.5,1,1,1,1,2,1,1,20,3840,70,205,120,Cocoon PokĂ©mon,55,1000000,0.7,50,Transel‚polmzcx,Metapod,50,11,25,25,30,bug,,9.9,1,0')
    pokemons = read_from_csv(file)
    pokemon1 = pokemons[0]
    pokemon2 = pokemons[1]
    enemy = pokemons[2]
    player1._player_pokemons = [pokemon1, pokemon2]
    player2._player_pokemons = [enemy]
    player2.current_fighter = enemy
    pokemon1_potential = player1.calculate_pokemon_potential(pokemon1, enemy)
    pokemon2_potential = player1.calculate_pokemon_potential(pokemon2, enemy)
    assert pokemon1_potential == 1
    assert pokemon2_potential == 2
    fighter = player1.calculate_if_there_is_better_pokemon(player2.current_fighter)
    assert pokemon2 == fighter
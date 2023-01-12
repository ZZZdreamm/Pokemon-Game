from colorama import Fore, Style
from enum import Enum


class MoveNumbers(Enum):
    DEFENSE = 1
    NORMAL_ATTACK = 2
    SPECIAL_ATTACK = 3
    GO_BACK = 4

class NoPokemonsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PokemonNotInListError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SpecialAttackDoesntExistError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Player:
    def __init__(self, id, name) -> None:
        """
        Constructor of Player
        """
        self.id = id
        self._player_pokemons = []
        self.current_fighter = None
        self.name = name

    def set_player_pokemons(self, pokemon, add=True):
        """
        Adds or remove pokemon from _player_pokemons depending on "add"
        parameter
        :pokemon: pokemon to add or remove to list
        :add: if add is True append pokemon otherwise remove from list
        """
        if (add):
            self._player_pokemons.append(pokemon)
        else:
            if (pokemon not in self._player_pokemons):
                raise PokemonNotInListError("This pokemon is not in list")
            self._player_pokemons.remove(pokemon)

    def choose_pokemon_to_your_team(self, pokemon_id, all_pokemons):
        """
        Player chooses which pokemon from list of all pokemons he wants
        to add to his team
        :pokemon_name: name of pokemon he choosed
        :all_pokemons: list of all pokemons available in game
        """
        choosen_pokemon = None
        for pokemon in all_pokemons:
            if (pokemon.id == pokemon_id):
                choosen_pokemon = pokemon
                break
        all_pokemons.remove(choosen_pokemon)
        self.set_player_pokemons(choosen_pokemon, add=True)
        return choosen_pokemon

    def choose_pokemon_to_fight(self, pokemon_id):
        """
        Player chooses his current fighter from his alive pokemons
        :pokemon_name: name of pokemon he choosed
        """
        self.current_fighter = self._player_pokemons[pokemon_id]
        self.set_player_pokemons(self.current_fighter, add=False)
        return f'Player {self.id} have chosen {self.current_fighter._name}!'

    def choose_pokemon_move(self, move_number, another_player=None, chosen_special=None, chosen_pokemon_num=None):
        """
        Player chooses 1 from 4 moves to do during his turn in game
        :move_number: number of move pokemon will do
        :another_player: enemy player
        """
        enemy_name = another_player.current_fighter._name
        if (move_number == MoveNumbers.DEFENSE.value):
            defense = self.current_fighter.defense()
            return f'{self.current_fighter._name} raised his defense to {defense}'
        elif (move_number == MoveNumbers.NORMAL_ATTACK.value):
            damage, enemy_health = self.current_fighter.attack(
                'normal', another_player.current_fighter)
            result = f'{self.current_fighter._name} used normal attack.\n{enemy_name} took {damage}.\nHis current health is {enemy_health}.'
            enemy_dead = another_player.check_if_pokemon_died()
            if (enemy_dead):
                result += f'\n{enemy_name} has died.'
            return result
        elif (move_number == MoveNumbers.SPECIAL_ATTACK.value):
            damage, enemy_health = self.current_fighter.attack(chosen_special, another_player.current_fighter)
            result = f'{self.current_fighter._name} used {chosen_special} attack.\n{enemy_name} took {damage}.\nHis current health is {enemy_health}.'
            enemy_dead = another_player.check_if_pokemon_died()
            if (enemy_dead):
                result += f'\n{enemy_name} has died.'
            return result
        elif (move_number == MoveNumbers.GO_BACK.value):
            if (len(self._player_pokemons) == 0):
                raise NoPokemonsError()
            old_fighter = self.current_fighter
            self.choose_pokemon_to_fight(chosen_pokemon_num)
            self.set_player_pokemons(old_fighter, add=True)
            return f"{old_fighter._name} has back.\n{self.current_fighter._name} has been chosen."

    def check_if_pokemon_died(self):
        """
        Checks if current fighter have died
        """
        if (self.current_fighter._health <= 0):
            self.current_fighter = None
            return True
        return False





from Player import Player
from Pokemon import Pokemon
from random import choice

class ComputerPlayer(Player):
    def __init__(self, id, name='Computer') -> None:
        super().__init__(id, name)


    def choose_best_fighter(self, enemy_fighter:Pokemon):
        """
        Computer chooses best possible fighter from his pokemons to fight enemy
        depending on pokemon potential
        :enemy_fighter: current enemy fighter
        """
        if (self.current_fighter):
            self.set_player_pokemons(self.current_fighter, add=True)
        self.current_fighter = self.calculate_if_there_is_better_pokemon(enemy_fighter)
        self.set_player_pokemons(self.current_fighter, add=False)
        return f'{self.name} have chosen {self.current_fighter._name}!'

    def choose_attack(self, enemy_fighter:Pokemon):
        """
        Choose best type of attack fighter should use
        :enemy_fighter: enemy player fighter
        """
        attack_potential = self.current_fighter.weakness_multiplier('normal', enemy_fighter)
        chosen_attack = 'normal'
        for attack_type in self.current_fighter._types:
            potential = self.current_fighter.weakness_multiplier(attack_type, enemy_fighter)
            if (potential > attack_potential):
                attack_potential = potential
                chosen_attack = attack_type
        return chosen_attack


    def do_best_move(self, enemy:Player):
        """
        Chooses best possible move in current situation depending on
        pokemon potential
        :enemy: enemy Player
        """
        result = ''
        potential = self.calculate_pokemon_potential(self.current_fighter, enemy.current_fighter)
        best_pokemon = self.calculate_if_there_is_better_pokemon(enemy.current_fighter)
        if (potential <= 0.75 and len(self._player_pokemons) != 0 and best_pokemon != self.current_fighter):
            result = self.choose_best_fighter(enemy.current_fighter)
        else:
            chosen_attack = self.choose_attack(enemy.current_fighter)
            if (chosen_attack == 'normal'):
                result = self.choose_pokemon_move(2, enemy)
            else:
                result = self.choose_pokemon_move(3, enemy, chosen_attack)
        return result

    def choose_random_pokemons_to_your_team(self, number_of_pokemons, all_pokemons):
        """
        Adds certain amount of random pokemons from all pokemons
        :number_of_pokemons: number of pokemons choosen in game
        :all_pokemons: list of all available pokemons
        """
        for _ in range(0, number_of_pokemons):
            pokemon = choice(all_pokemons)
            self.set_player_pokemons(pokemon, add=True)
            all_pokemons.remove(pokemon)

    def calculate_pokemon_potential(self, my_pokemon, enemy_pokemon):
        """
        Calculates pokemon potential depending on pokemon and enemy pokemon types
        :my_pokemon: player current fighter
        :enemy_pokemon: enemy current fighter
        """
        my_attack_potential = self.calculate_attack_potential(
            my_pokemon, enemy_pokemon)
        enemy_attack_potential = self.calculate_attack_potential(
            enemy_pokemon, my_pokemon)
        pokemon_potential = my_attack_potential/enemy_attack_potential
        return pokemon_potential

    def calculate_attack_potential(self, pokemon, enemy):
        """
        Calculate pokemon attack potential
        :pokemon: player current fighter
        :enemy: enemy current fighter
        """
        my_attack_potential = pokemon.weakness_multiplier('normal', enemy)
        for attack_type in pokemon._types:
            potential = pokemon.weakness_multiplier(attack_type, enemy)
            if (potential > my_attack_potential):
                my_attack_potential = potential
                break
        return my_attack_potential

    def calculate_if_there_is_better_pokemon(self, enemy_pokemon):
        """
        Calculates if there is a better possible fighter then current one against
        enemy pokemon
        :enemy_pokemon: enemy current fighter
        """
        fighter = self.current_fighter
        if(self.current_fighter):
            multiplier = self.calculate_pokemon_potential(self.current_fighter, enemy_pokemon)
        else:
            multiplier = 0
        for pokemon in self._player_pokemons:
            pokemon_potential = self.calculate_pokemon_potential(pokemon, enemy_pokemon)
            if(pokemon_potential > multiplier):
                multiplier = pokemon_potential
                fighter = pokemon
        return fighter


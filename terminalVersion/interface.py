from Player import Player
from ComputerPlayer import ComputerPlayer
from colorama import Fore, Style
from Player import MoveNumbers
from Game import Game
import os


class SpecialAttackDoesntExistError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GameInterface:
    def __init__(self) -> None:
        pass

    def play_game(self):
        """
        Begin game between 2 players
        """
        self.setup_game()
        game = self.game
        self.fight()
        game.determine_winner()
        self.print_who_is_winner()
        do_reset = input('If you want to play again click Y\n')
        game.reset_game(do_reset)
        if (do_reset == 'Y'):
            self.play_game()


    def setup_game(self):
        """
        Setups game statistics before fight
        """
        os.system('cls')
        game = Game()
        self.game = game
        game.load_all_pokemons()
        print(Style.RESET_ALL)

        mode_number = self.input_value_and_check_it(
            1, 2, "Choose mode:\n1.Player vs Player\n2.Player vs Computer\n")

        game.set_mode(mode_number)

        players = []
        players.append(Player(1, input('Choose player 1 name: ')))
        if (game._mode == 1):
            players.append(Player(2, input('Choose player 2 name: ')))
        else:
            players.append(ComputerPlayer(2))

        number_of_pokemons = self.input_value_and_check_it(
            1, 6, 'Choose number of pokemons from 1 to 6\n')

        game.set_players(players)
        game.set_number_of_pokemons(number_of_pokemons)

        self.players_choose_pokemons()

        player1 = game.players[0]
        player2 = game.players[1]

        self.print_player_pokemons(player1)
        pokemon_number = self.input_value_and_check_it(0, len(player1._player_pokemons)-1, "Player 1 choose pokemon number: ")
        result = player1.choose_pokemon_to_fight(pokemon_number)
        print(result)
        if (game._mode == 1):
            self.print_player_pokemons(player2)
            pokemon_number = self.input_value_and_check_it(0, len(player2._player_pokemons)-1, "Player 2 choose pokemon number: ")
            result = player2.choose_pokemon_to_fight(pokemon_number)
            print(result)
        else:
            result = player2.choose_best_fighter(player1.current_fighter)
            print(result)


    def fight(self):
        """
        Does fight system
        """
        game = self.game
        player1 = game.players[0]
        player2 = game.players[1]
        while (game._game_state == 0):
            if (not player1.current_fighter):
                self.player_choose_new_fighter(player1)
            print(Fore.RED + f'Player 1 fighter: {player1.current_fighter._name}, Health: {player1.current_fighter._health},  Attack: {player1.current_fighter._normal_attack}')
            players1_move_result = self.player_chooses_move(0)
            print(Style.RESET_ALL)
            print(players1_move_result)
            if (not player2.current_fighter and len(player2._player_pokemons) != 0):
                if (game._mode == 1):
                    self.player_choose_new_fighter(player2)
                else:
                    result = player2.choose_best_fighter(
                        player1.current_fighter)
                    print(result)
            if (player2.current_fighter):
                print(Fore.RED + f'Player 2 fighter: {player2.current_fighter._name}, Health: {player2.current_fighter._health}, Attack: {player2.current_fighter._normal_attack}')
                if (game._mode == 1):
                    players2_move_result = self.player_chooses_move(1)
                else:
                    print('Computer move: ')
                    players2_move_result = player2.do_best_move(player1)
                print(Style.RESET_ALL)
                print(players2_move_result)
            game.check_if_game_ended()

    def player_choose_new_fighter(self, player):
        self.print_player_pokemons(player)
        pokemon_number = self.input_value_and_check_it(
            0, len(player._player_pokemons)-1, "Player 1 choose pokemon number: ")
        result = player.choose_pokemon_to_fight(pokemon_number)
        print(result)

    def player_chooses_move(self, player_number):
        """
        Player inputs move numbers
        :player_number: number of player currently doing move
        """
        self.print_possible_moves()
        print(Fore.RED)

        player = self.game.players[player_number]
        if (player_number == 1):
            enemy = self.game.players[0]
        else:
            enemy = self.game.players[1]

        move_number = self.input_value_and_check_it(1, 4, f"Player {player_number+1} chooses move: ")
        chosen_special = None
        chosen_pokemon = None

        if (move_number == MoveNumbers.SPECIAL_ATTACK.value):
            chosen_special = self.return_pokemon_special_attack_types(player.current_fighter)
        elif (move_number == MoveNumbers.GO_BACK.value):
            self.print_player_pokemons(player)
            chosen_pokemon = self.input_value_and_check_it(0, len(player._player_pokemons)-1, "Choose new fighter: ")

        players_move_result = player.choose_pokemon_move(
            move_number, enemy, chosen_special, chosen_pokemon)
        return players_move_result

    def players_choose_pokemons(self):
        """
        Player chooses certain amount of pokemons to his team
        :player_number: number of player in game
        """
        for _ in range(0, self.game._number_of_pokemons):
            self.print_all_pokemons()
            while True:
                try:
                    pokemon_number = int(input(f"Player 1 chooses pokemon: "))
                    # self.game.player_adds_pokemon_to_team(0, pokemon_number)
                    self.game.players[0].choose_pokemon_to_your_team(pokemon_number, self.game._all_pokemons)
                    break
                except ValueError:
                    print('Wrong value\nInput again')


        self.print_player_pokemons(self.game.players[0])
        if (self.game._mode == 1):
            for _ in range(0, self.game._number_of_pokemons):
                self.print_all_pokemons()
                while True:
                    try:
                        pokemon_number = int(input(f"Player 2 chooses pokemon: "))
                        self.game.players[1].choose_pokemon_to_your_team(pokemon_number, self.game._all_pokemons)
                        break
                    except ValueError:
                        print('Wrong value\nInput again')
        else:
            self.game.players[1].choose_random_pokemons_to_your_team(
                self.game._number_of_pokemons, self.game._all_pokemons)
        self.print_player_pokemons(self.game.players[1])


    def input_value_and_check_it(self, minimum_value, maximum_value, message):
        """
        Checks if value inputted by player is not string and between
        certain values
        :minimum_value: minimum integer of input
        :maximum_value: maximum integer of input
        :message: message for user
        """
        if (maximum_value <= 1):
            minimum_value = 0
        while True:
            try:
                input_number = int(input(message))
                if (input_number > maximum_value or input_number < minimum_value):
                    raise ValueError
                break
            except ValueError:
                print('Wrong value\nInput again')
        return input_number


    def print_all_pokemons(self):
        """
        Prints in terminal list of all pokemons in game
        """
        for pokemon in self.game._all_pokemons:
            result = f'Id: {pokemon.id}. Name: {pokemon._name}, Health: {pokemon._health}, Attack: {pokemon._normal_attack}, Type 1: {pokemon._types[0]}'
            if (pokemon._types[1]):
                result += f', Type 2: {pokemon._types[0]}'
            print(result)

    def print_player_pokemons(self, player):
        """
        Prints in terminal list of player pokemons
        :player: player class
        """
        print(Fore.RED)
        print(f"Player {player.id} pokemons:")
        for index, pokemon in enumerate(player._player_pokemons):
            result = f'Number: {index}. Name: {pokemon._name}, Health: {pokemon._health}, Attack: {pokemon._normal_attack}, Type 1: {pokemon._types[0]}'
            if (pokemon._types[1]):
                result += f', Type 2: {pokemon._types[1]}'
            print(result)
        print(Style.RESET_ALL)

    def print_possible_moves(self):
        """
        Prints in terminal player moves
        """
        print(Fore.BLUE + '1. Defense')
        print('2. Attack')
        print('3. Special attack')
        print('4. Go back')

    def print_who_is_winner(self):
        """
        Prints in terminal who is winner of game
        """
        os.system('cls')
        print(f'The winner is {self.game.winner.name}!!!')


    def return_pokemon_special_attack_types(self, pokemon):
        """
        Printing possible special attacks then choose one of them
        """
        for index, type in enumerate(pokemon._types):
            if (type != ''):
                print(f'{index}. {type} attack')
        try:
            chosen_special_index = int(input('Choose special attack type: '))
            if (chosen_special_index > len(pokemon._types)-1):
                raise SpecialAttackDoesntExistError
            chosen_special = pokemon._types[chosen_special_index]
            if (chosen_special == ''):
                raise SpecialAttackDoesntExistError
        except SpecialAttackDoesntExistError:
            print('Wrong number')
            chosen_special = self.return_pokemon_special_attack_types(pokemon)
        except ValueError:
            print('Wrong value')
            chosen_special = self.return_pokemon_special_attack_types(pokemon)
        return chosen_special

if __name__ == "__main__":
    interface = GameInterface()
    interface.play_game()
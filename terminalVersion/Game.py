from database import Database


FILE_TO_READ_POKEMONS = 'pokemon.csv'


class Game:
    def __init__(self, all_pokemons=None) -> None:
        """
        Constructor of game class
        :all_pokemons: list of pokemons available in game
        """
        self.players = []
        self._mode = 0
        self._game_state = 0
        self.winner = None
        self._all_pokemons = all_pokemons
        self._number_of_pokemons = 3

    def get_all_pokemons(self):
        """
        Returns list of all available pokemons in game
        """
        return self._all_pokemons

    def set_players(self, players):
        """
        Set players participating in game
        :players: players playing game
        """
        self.players = players

    def set_mode(self, mode_number):
        """
        Set mode of game
        :mode_number: 1 for Player vs Player, 2 for Player vs Computer
        """
        self._mode = mode_number

    def set_number_of_pokemons(self, pokemons_number):
        """
        Set number of pokemons each player will have
        :pokemon_number: amount of pokemons
        """
        self._number_of_pokemons = pokemons_number

    def load_all_pokemons(self):
        """
        Setup data to start a game
        """
        database = Database()
        self._all_pokemons = database.load_from_file(FILE_TO_READ_POKEMONS)

    def determine_winner(self):
        """
        Returns the winner of game
        """
        if (self._game_state == 1):
            self.winner = self.players[0]
        elif (self._game_state == 2):
            self.winner = self.players[1]

    def check_if_game_ended(self):
        """
        Checks if game has come to end
        """
        if (not self.players[0]._player_pokemons and not self.players[0].current_fighter):
            self._game_state = 2
        if (not self.players[1]._player_pokemons and not self.players[1].current_fighter):
            self._game_state = 1

    def reset_game(self, do_reset):
        """
        Reset data of game class instance and starts game again
        """
        if (do_reset == 'Y'):
            self.players = []
            self._mode = 0
            self._game_state = 0
            self._all_pokemons = []
            self._number_of_pokemons = 3
            self.winner = None
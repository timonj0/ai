"""
Game Hi-Low
Version: 0.02
"""

from random import randint, choice
from colorama import Back


class beautiful_hilo:
    """Pint beatiful and clearly arranged views of hilo"""

    colors = [["red", Back.RED],
              ["orange", Back.LIGHTRED_EX],
              ["green", Back.GREEN],
              ["lime", Back.LIGHTGREEN_EX],
              ["yellow", Back.YELLOW],
              ["blue", Back.BLUE],
              ["cyan", Back.LIGHTBLUE_EX],
              ["pink", Back.LIGHTMAGENTA_EX]]

    def __init__(self):
        pass

    def get_color_code(self, card):
        if not card.revealed:
            return Back.BLACK
        for code in self.colors:
            if card.color == code[0]:
                return code[1]

    def get_value_code(self, card):
        if not card.revealed:
            return "##"
        if len(str(card.value)) == 1:
            return " " + str(card.value)
        else:
            return str(card.value)

    def print_card_grid(self, card_grid: list):
        """Print an arranged, colored card grid"""
        rows = len(card_grid)
        columns = len(card_grid[0])

        for row in card_grid:
            print(columns * "+-----" + "+")
            for c in row:
                print(f"|{self.get_color_code(c)}     {Back.RESET}", end="")
            print("|")
            for c in row:
                print(f"|{self.get_color_code(c)} {self.get_value_code(c)}  {Back.RESET}", end="")
            print("|")
            for c in row:
                print(f"|{self.get_color_code(c)}     {Back.RESET}", end="")
            print("|")

        print(columns * "+-----" + "+")

    def print_card(self, card):
        print("+-----+")
        print(f"|{self.get_color_code(card)}     {Back.RESET}|")
        print(f"|{self.get_color_code(card)} {self.get_value_code(card)}  {Back.RESET}|")
        print(f"|{self.get_color_code(card)}     {Back.RESET}|")
        print("+-----+")


class card:
    color = ""
    value = ""
    revealed = False

    def __init__(self, color, value, revealed):
        self.color = color
        self.value = value
        self.revealed = revealed

    def reveal(self):
        self.revealed = True

    def as_list(self):
        if self.revealed:
            return [self.color, self.value]
        else:
            return ["##", "##"]


class player:
    card_grid = []
    points = 0

    def __init__(self, points):
        self.points = points

    def print_card_grid(self):
        for row in self.card_grid:
            for c in row:
                print(c.as_list(), end='   ')
            print("\n")


class game:
    """
    Game Variables
    """
    players = []
    colors = ["red", "orange", "green", "lime", "yellow", "blue", "cyan", "pink"]
    values = list(range(-1, 12, 1))
    card_grid_width = 3
    card_grid_height = 3

    open_stack_card = ""  # Top card from the revealed stack
    closed_stack_card = ""  # Top card from the unrevealed stack

    game_on = True
    round_on = True

    """
    General Functions
    """

    def __init__(self, no_players=4):
        self.start_game(no_players)

    def random_card(self, revealed=True):
        """Return a random card"""
        return card(choice(self.colors), choice(self.values), revealed)

    """
    Game Functions
    """

    def start_game(self, no_players):
        """Initate Players and points"""
        for i in range(no_players):
            self.players.append(player(0))

        self.gameloop()  # Start game

    def check_game_on(self):
        """Check if game is over"""
        for p in self.players:
            if p.points >= 100:
                return True
        return False

    def gameloop(self):
        """Gameloop"""
        while self.game_on:
            self.start_round()
            self. game_on = self.check_game_on()

    """
    Round Functions
    """

    def start_round(self):
        """Initiate cards and players at the start of a round"""
        for current_player in self.players:  # Initiate each players cardgrid with random cards
            for h in range(self.card_grid_height):
                current_row = []
                for w in range(self.card_grid_width):
                    current_row.append(self.random_card())
                current_player.card_grid.append(current_row)

        self.roundloop()

    def check_round_on(self):
        """Check if round is over"""
        pass

    def turn(self, player: player):
        pass

    def roundloop(self):
        """Roundloop"""
        while self.round_on:
            for current_player in self.players:
                self.closed_stack_card = self.random_card(False)
                self.turn(current_player)


"""
mygame = game()

# DEBUG
for p in game.players:
    p.print_card_grid()
"""

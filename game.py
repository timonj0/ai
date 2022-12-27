"""
Game Hi-Low
Version: 0.03
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

        string_grid = ""

        for row in card_grid:
            string_grid = string_grid + columns * "+-----" + "+\n"
            for c in row:
                string_grid = string_grid + f"|{self.get_color_code(c)}     {Back.RESET}"
            string_grid = string_grid + "|\n"
            for c in row:
                string_grid = string_grid + f"|{self.get_color_code(c)} {self.get_value_code(c)}  {Back.RESET}"
            string_grid = string_grid + "|\n"
            for c in row:
                string_grid = string_grid + f"|{self.get_color_code(c)}     {Back.RESET}"
            string_grid = string_grid + "|\n"

        string_grid = string_grid + columns * "+-----" + "+"

        print(string_grid)

    def print_grids(self, card_grids: list):
        "Print three arranged, colored card grids in one line"

        string_grids = []
        for card_grid in card_grids:
            rows = len(card_grid)
            columns = len(card_grid[0])
            string_grid = ""
            for row in card_grid:
                string_grid = string_grid + columns * "+-----" + "+\n"
                for c in row:
                    string_grid = string_grid + f"|{self.get_color_code(c)}     {Back.RESET}"
                string_grid = string_grid + "|\n"
                for c in row:
                    string_grid = string_grid + f"|{self.get_color_code(c)} {self.get_value_code(c)}  {Back.RESET}"
                string_grid = string_grid + "|\n"
                for c in row:
                    string_grid = string_grid + f"|{self.get_color_code(c)}     {Back.RESET}"
                string_grid = string_grid + "|\n"
            string_grid = string_grid + columns * "+-----" + "+"
            string_grids.append(string_grid)

        player = [0, 1, 2]
        lines = [string_grids[i].splitlines() for i in player]
        for l in zip(*lines):
            print(*l, sep='     ')

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
    name = ""

    def __init__(self, points, name):
        self.points = points
        self.name = name

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

    gameprint = beautiful_hilo()

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
            self.players.append(player(0, str(i)))

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
            current_card_grid = []
            for h in range(self.card_grid_height):
                current_row = []
                for w in range(self.card_grid_width):
                    current_row.append(self.random_card(False))
                current_card_grid.append(current_row)
            current_player.card_grid = current_card_grid

        self.open_stack_card = self.random_card(True)
        self.roundloop()

    def turn(self, player: player):
        """Player Interaction"""

        """STAGE 0: Output"""
        print("Cards of your opponents:")
        self.print_other_player_grids(player)
        print(f"Cards of Player: {player.name}")
        self.gameprint.print_card_grid(player.card_grid)
        print("Open card stack:")
        self.gameprint.print_card(self.open_stack_card)

        """STAGE 1: Take open card or draw random card"""
        valid = False  # Input validation
        while not valid:  # ^^^
            action = input("Do you want to take the open card (o) or draw a new one (d)? >")
            if action == "o":
                self.switch_cards()
                valid = True
            elif action == "d":
                self.draw()
                valid = True
            else:
                print(f"Invalid input: <{action}>. Use <o> or <d>")
                valid == False

    def print_other_player_grids(self, current_player):
        """Print grids of other all players"""
        other_players = []
        for p in self.players:
            if not p.name == current_player.name:
                other_players.append(p)

        other_player_grids = []
        for p in other_players:
            other_player_grids.append(p.card_grid)

        self.gameprint.print_grids(other_player_grids)

    def roundloop(self):
        """Roundloop"""
        while self.round_on:
            for current_player in self.players:
                self.closed_stack_card = self.random_card(False)
                self.turn(current_player)


mygame = game()

"""
Game Hi-Low
Version: 0.03
"""

from random import randint, choice
from colorama import Back


class beautiful_hilo:
    """Pint beatiful and clearly arranged views of hilo"""

    SUPER_VISION = True  # Shows all cards, even if not revealed

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
        if not card.revealed and not self.SUPER_VISION:
            return Back.BLACK
        for code in self.colors:
            if card.color == code[0]:
                return code[1]

    def get_value_code(self, card):
        if not card.revealed and not self.SUPER_VISION:
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

    def print_grids(self, card_grids: list, titles: list):
        "Print three arranged, colored card grids with titles in one line"

        string_grids = []
        for card_grid in card_grids:
            rows = len(card_grid)
            columns = len(card_grid[0])
            grid_length = columns * 6 + 1
            title = titles[card_grids.index(card_grid)]
            title_line = title + " " * (grid_length - len(title)) + "\n"

            string_grid = ""
            string_grid = string_grid + title_line
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

    def __init__(self, color, value, revealed=True):
        self.color = color
        self.value = value
        self.revealed = revealed

    def __str__(self) -> str:
        return self.color + self.value

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

    NAME_MAX_LEN = 10

    def __init__(self, points, name):
        self.points = points
        if len(name) <= self.NAME_MAX_LEN:  # Validate Playername
            self.name = name
        else:
            raise Exception(f"Playername is too long! (Max length: {self.NAME_MAX_LEN})")

    def __str__(self) -> str:
        return self.name + self.points


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

    def print_other_player_grids(self, current_player):
        """Print grids of other all players"""
        other_players = []
        for p in self.players:
            if not p.name == current_player.name:
                other_players.append(p)
        other_player_grids = []
        other_player_names = []
        for p in other_players:
            other_player_grids.append(p.card_grid)
            other_player_names.append((p.name))
        self.gameprint.print_grids(other_player_grids, other_player_names)

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
                nr_valid = False
                while not nr_valid:
                    card_nr = input(
                        f"Which card do you want to switch with? (Cards are numbered left to right, top to bottom) >")
                    try:
                        card_nr = int(card_nr)
                        nr_valid = True
                    except:
                        print("Input must be a number. Cards are numbered left to right, top to bottom")
                self.switch_cards(player.card_grid, card_nr, self.open_stack_card)
                valid = True
            elif action == "d":
                self.draw()  # TODO
                valid = True
            else:
                print(f"Invalid input: <{action}>. Use <o> or <d>")
                valid == False

    def switch_cards(self, cardgrid: list, card_nr: int, card_1: card):
        """Switch value and color of a card from a cardgrid with another card"""
        """Cards are numbered left to right, top to bottom"""
        counter = 1
        card_2 = -1
        for row in cardgrid:  # Get card to switch with from cardgrid
            for c in row:
                if counter == card_nr:
                    card_2 = c
                counter = counter + 1

        if card_2 == -1:  # Validate card exists
            raise Exception(f"Card: {card_nr} is not in cardgrid")

        c1_c = card_1.color
        c1_v = card_1.value
        card_1.color = card_2.color
        card_1.value = card_2.value
        card_1.reveal()
        card_2.color = c1_c
        card_2.value = c1_v
        card_2.reveal()

    def draw(self):
        pass

    def roundloop(self):
        """Roundloop"""
        while self.round_on:
            for current_player in self.players:
                self.closed_stack_card = self.random_card(False)
                self.turn(current_player)


mygame = game()

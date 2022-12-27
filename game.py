"""
Game Hi-Low
Version: 0.01
"""

from random import randint, choice


class card:
    color = ""
    value = ""
    revealed = False

    def __init__(self, color, value, revealed):
        self.color = color
        self.value = value
        self.revealed = revealed


class player:
    card_grid = []

    def __init__(self):
        pass

    def print_card_grid(self):
        for row in self.card_grid:
            for c in row:
                print([c.color, c.value], end='   ')
            print("\n")


class game:
    players = []
    colors = ["red", "orange", "green", "lime", "yellow", "blue", "cyan", "pink"]
    values = list(range(-1, 12, 1))
    card_grid_width = 3
    card_grid_height = 3

    open_stack_card = ""  # Top card from the revealed stack
    closed_stack_card = ""  # Top card from the unrevealed stack

    def __init__(self, no_players=4):
        self.start_game(no_players)

    def random_card(self, revealed=True):
        return card(choice(self.colors), choice(self.values), revealed)

    def start_game(self, no_players):
        for i in range(no_players):
            current_player = player()

            # Give Cards to players
            for h in range(self.card_grid_height):
                current_row = []
                for w in range(self.card_grid_width):
                    current_row.append(self.__random_card__())
                current_player.card_grid.append(current_row)
            self.players.append(current_player)


mygame = game()

# DEBUG
for p in game.players:
    p.print_card_grid()

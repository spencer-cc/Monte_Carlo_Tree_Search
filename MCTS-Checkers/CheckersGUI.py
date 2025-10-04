import tkinter as tk
from math import floor
from random import choice
import MonteCarloTreeSearch
import AmericanCheckers_optimized as AmericanCheckers
#import AmericanCheckers
from time import time, sleep

window_size = 600
tile_width = window_size / 8

star_offset_percents = [[0.0, -0.35], [0.07, -0.1], [0.34, -0.1], [0.12, 0.04], [0.21, 0.29],
                        [0.0, 0.14], [-0.21, 0.29], [-0.12, 0.04], [-0.34, -0.1], [-0.07, -0.1]]
star_offsets = []
for point in star_offset_percents:
    star_offsets.append((point[0] * (tile_width / 2), point[1] * (tile_width / 2)))
star_offsets = tuple(star_offsets)

circle_offset_percent = 0.75
circle_offset = (tile_width / 2) * 0.75

line_color = "black"
dark_tile_color = "gray65"
light_tile_color = "white"
highlight_color = "yellow2"
red_piece_colors = ["red2", "red4"]
black_piece_colors = ["black", "gray20"]


class GUI:
    def __init__(self, root, game_controller):
        self.root = root
        self.root.title("Checkers")
        self.canvas = tk.Canvas(self.root, width=window_size, height=window_size, background='white')
        self.canvas.pack()
        self.game_controller = game_controller
        self.player_color = game_controller.player_color
        self.do_loop = True

        if self.player_color == "b":
            self.y_list = list("87654321")
            self.x_list = list("abcdefgh")
        else:
            self.y_list = list("12345678")
            self.x_list = list("hgfedcba")

        for x in range(8):
            for y in range(8):
                if x % 2 == 0:
                    if y % 2 == 1:
                        self.canvas.create_rectangle(x * tile_width, y * tile_width, (x + 1) * tile_width,
                                                     (y + 1) * tile_width, fill=dark_tile_color)
                    else:
                        self.canvas.create_rectangle(x * tile_width, y * tile_width, (x + 1) * tile_width,
                                                     (y + 1) * tile_width, fill=light_tile_color)
                else:
                    if y % 2 == 0:
                        self.canvas.create_rectangle(x * tile_width, y * tile_width, (x + 1) * tile_width,
                                                     (y + 1) * tile_width, fill=dark_tile_color)
                    else:
                        self.canvas.create_rectangle(x * tile_width, y * tile_width, (x + 1) * tile_width,
                                                     (y + 1) * tile_width, fill=light_tile_color)

        for x in range(8):
            self.canvas.create_line(x * tile_width, 0, x * tile_width, 600, fill=line_color, width=2)

        for y in range(8):
            self.canvas.create_line(0, y * tile_width, 600, y * tile_width, fill=line_color, width=2)

        self.canvas_objects = []

        self.canvas.bind("<Button-1>", self.on_click)

    def cord_to_loc(self, event) -> str:
        x, y = event.x, event.y
        return self.x_list[floor(x/tile_width)] + self.y_list[floor(y/tile_width)]

    def on_click(self, event):
        self.game_controller.handle_click(self.cord_to_loc(event))

    def place_piece(self, location: str,  piece: str):
        if piece == " ":
            return

        x = tile_width/2 + self.x_list.index(location[0]) * tile_width
        y = tile_width/2 + self.y_list.index(location[1]) * tile_width

        if piece[0] == "r":
            colors = red_piece_colors
        else:
            colors = black_piece_colors
        self.canvas_objects.append(
            self.canvas.create_oval(
                x-circle_offset, y-circle_offset, x+circle_offset, y+circle_offset, fill=colors[0], outline=''))

        if piece[2:] == "king":
            star_points = []
            for point in star_offsets:
                star_points.append((point[0]+x, point[1]+y))
            self.canvas_objects.append(self.canvas.create_polygon(tuple(star_points), fill=colors[1], outline=''))

    def update_board(self):
        board, turn, highlight = self.game_controller.get_board_info()
        if turn == "b":
            self.root.title("Checkers: Black's Turn")
        else:
            self.root.title("Checkers: Red's Turn")

        for element in self.canvas_objects:
            self.canvas.delete(element)

        if highlight is not None:
            x1 = self.x_list.index(highlight[0]) * tile_width
            x2 = (self.x_list.index(highlight[0]) + 1) * tile_width
            y1 = self.y_list.index(highlight[1]) * tile_width
            y2 = (self.y_list.index(highlight[1]) + 1) * tile_width
            self.canvas_objects.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill=highlight_color, width=2))

        for key in board.keys():
            self.place_piece(key, board[key])

        self.root.update()

    def end_game(self, result):
        if result == "win":
            title = "Game Over: Win"
            text = "You Won!"
            color = "green"
        elif result == "loss":
            title = "Game Over: Loss"
            text = "You Lost!"
            color = "red"
        elif result == "draw":
            title = "Game Over: Draw"
            text = "Draw"
            color = "gray"
        else:
            raise ValueError("Incorrect result")

        self.do_loop = False
        self.root.title(title)
        self.canvas.create_text(window_size/2, window_size/2,
                                anchor='s', text=text, fill=color,
                                font=('Comic Sans', -int(tile_width*.8), 'bold'))

    def game_loop(self):
        self.update_board()
        status = self.game_controller.game.get_status()
        if status == "draw":
            self.end_game("draw")
        if status == "win":
            if self.game_controller.player_turn():
                self.end_game("win")
            else:
                self.end_game("loss")

        sleep(.1)
        if not self.game_controller.player_turn():
            self.game_controller.do_playout()
            self.update_board()

        if self.do_loop:
            self.root.after(100, self.game_loop)


class GameController:
    def __init__(self, time_limit: float):
        self.game = AmericanCheckers.game()
        self.tree = MonteCarloTreeSearch.MCTS(time_limit, AmericanCheckers, heuristic=AmericanCheckers.heuristic, show_progress=True)
        self.selected_tile = None
        self.player_color = choice(["r", "b"])

    def handle_click(self, location: str):
        if not self.player_turn() or self.game.get_status() != "playing":
            return

        if self.selected_tile is None:
            if self.game.board[location][0] == self.game.turn:
                self.selected_tile = location
        elif self.selected_tile == location:
            self.selected_tile = None
        else:

            temp = f"{self.selected_tile}:{location}"
            if temp in self.game.get_legal_moves():
                self.game.make_move(temp)
                self.selected_tile = None

    def get_board_info(self):
        return self.game.get_dict(), self.game.turn, self.selected_tile

    def do_playout(self):
        start = time()
        move = self.tree.playout(self.game)
        while time() - start < 0.5:
            pass
        self.game.make_move(move)

    def player_turn(self):
        if self.game.turn == self.player_color:
            return True
        return False


def run_game(time_limit, dev_mode=(False, [])):
    root = tk.Tk()
    controller = GameController(time_limit=time_limit)
    gui = GUI(root, controller)
    if dev_mode[0]:
        for letter in list("abcdefgh"):
            for num in list("12345678"):
                controller.game.board[letter+num] = " "

        for element in dev_mode[1]:
            controller.game.board[element[0]] = element[1]

    gui.game_loop()
    root.mainloop()


if __name__ == '__main__':
    run_game(3)


# TODO: make multi-jumps manual not automatic for player
# TODO: multi-jumps break user input
# TODO: hinge input on player_turn on accept_input

from game_env import game_env


def heuristic(game_dict):
    return None

# TODO: instead of index use a dict?

# TODO: Would it be faster calculate available moves with a c program?

# TODO: optmimize this 3rd
def jump(start, end):
    columns = list("abcdefgh")
    rows = list("12345678")
    start_col = columns.index(start[0])
    start_row = rows.index(start[1])
    end_col = columns.index(end[0])
    end_row = rows.index(end[1])

    if start_col == end_col + 2 and start_row == end_row + 2:
        return True, columns[start_col - 1] + rows[start_row - 1]

    elif start_col == end_col - 2 and start_row == end_row - 2:
        return True, columns[start_col + 1] + rows[start_row + 1]

    elif start_col == end_col + 2 and start_row == end_row - 2:
        return True, columns[start_col - 1] + rows[start_row + 1]

    elif start_col == end_col - 2 and start_row == end_row + 2:
        return True, columns[start_col + 1] + rows[start_row - 1]

    return False, None

# TODO: optimize this 2nd
def get_directions(location: str, piece: str):
    columns = list("abcdefgh")
    rows = list("12345678")
    col = location[0]
    row = location[1]
    col_ind = columns.index(col)
    row_ind = rows.index(row)
    upper_left = [columns[col_ind - 1] + rows[(row_ind + 1) % 8], columns[col_ind - 2] + rows[(row_ind + 2) % 8]]
    upper_right = [columns[(col_ind + 1) % 8] + rows[(row_ind + 1) % 8],
                   columns[(col_ind + 2) % 8] + rows[(row_ind + 2) % 8]]
    lower_left = [columns[col_ind - 1] + rows[row_ind - 1], columns[col_ind - 2] + rows[row_ind - 2]]
    lower_right = [columns[(col_ind + 1) % 8] + rows[row_ind - 1], columns[(col_ind + 2) % 8] + rows[row_ind - 2]]

    if col == "a":
        upper_left = []
        lower_left = []
    elif col == "b":
        upper_left = [upper_left[0]]
        lower_left = [lower_left[0]]

    if col == "h":
        upper_right = []
        lower_right = []
    elif col == "g":
        upper_right = [upper_right[0]]
        lower_right = [lower_right[0]]

    if row == "1":
        lower_left = []
        lower_right = []
    elif row == "2":
        if lower_left:
            lower_left = [lower_left[0]]
        if lower_right:
            lower_right = [lower_right[0]]

    if row == "8":
        upper_right = []
        upper_left = []
    elif row == "7":
        if upper_left:
            upper_left = [upper_left[0]]
        if upper_right:
            upper_right = [upper_right[0]]

    if piece[2:] == "king":
        out = [upper_left, upper_right, lower_left, lower_right]
    elif piece[0] == "r":
        out = [lower_left, lower_right]
    elif piece[0] == "b":
        out = [upper_left, upper_right]
    else:
        raise ValueError("Invalid piece type")

    return out


class game(game_env):

    # location syntax: a1, b2, c3 etc.
    #   columns use locations a-h
    #   rows use 1-8
    #
    # 0, 1 are red pawn and king
    # 2, 3 are black pawn and king

    def __init__(self):
        super().__init__()
        self.board = {}
        for row in list("87654321"):
            for column in list("abcdefgh"):
                if row in list("13") and column in list("aceg"):
                    self.board[column + row] = "b_pawn"
                elif row == "2" and column in list("bdfh"):
                    self.board[column + row] = "b_pawn"
                elif row in list("68") and column in list("bdfh"):
                    self.board[column + row] = "r_pawn"
                elif row == "7" and column in list("aceg"):
                    self.board[column + row] = "r_pawn"
                else:
                    self.board[column + row] = " "

        self.chips = {"b_pawn": "\033[90m\u25CF\033[0m", "b_king": "\033[90m\u25CE\033[0m",
                      "r_pawn": "\033[31m\u25CF\033[0m", "r_king": "\033[31m\u25CE\033[0m"}

        self.state = []
        self.state_history = [[]]
        self.turn = "b"
        self.last_move = None
        self.legal_moves = []
        self.update_legal_moves()
        self.status = "playing"
        self.black_pieces = 12
        self.red_pieces = 12

    def get_string(self, turn="default") -> str:
        string = ""
        if turn == "default":
            if self.turn == "r":
                rows = list("12345678")
                columns = list("hgfedcba")
            else:
                rows = list("87654321")
                columns = list("abcdefgh")
        elif turn == "r":
            rows = list("12345678")
            columns = list("hgfedcba")
        elif turn == "b":
            rows = list("87654321")
            columns = list("abcdefgh")
        else:
            raise ValueError("Invalid turn option. Please use 'r' or 'b'")

        for row in rows:
            if self.last_move is not None and self.last_move[1] == row:
                string += "\033[36m" + row + "\033[0m |"
            else:
                string += row + " |"
            for col in columns:
                temp = self.board[col + row]
                if temp == " ":
                    string += " |"
                else:
                    string += self.chips[temp] + "|"
            string += "\n"
        string += "  "
        for col in columns:
            if self.last_move is not None and self.last_move[0] == col:
                string += " \033[36m" + col + "\033[0m"
            else:
                string += " " + col
        return string

    def get_state_history(self) -> tuple:
        return tuple(self.state_history)

    def get_dict(self) -> dict:
        return self.board

    def get_state(self) -> list:
        return self.state

    def get_legal_moves(self) -> list:
        return self.legal_moves

    def get_status(self) -> str:
        return self.status

    # TODO: optimize this 1st
    def update_legal_moves(self):
        out = []
        for key in self.board.keys():
            tile = self.board[key]
            if tile != " " and tile[0] == self.turn:
                directions = get_directions(key, tile)
                for direction in directions:
                    direction_len = len(direction)
                    if direction_len > 0 and self.board[direction[0]] == " ":
                        out.append(f"{key}:{direction[0]}")
                    elif (direction_len > 1 and self.board[direction[0]][0] != tile[0]
                          and self.board[direction[1]] == " "):
                        out.append(f"{key}:{direction[1]}")
        jump_present = False
        jump_list = []
        for move in out:
            temp, NA = jump(move[:2], move[3:])
            if temp:
                jump_present = True
                jump_list.append(move)
        if jump_present:
            out = jump_list

        self.legal_moves = out

    # TODO: optimize this?
    def update_status(self):
        if self.black_pieces == 0 or self.red_pieces == 0:
            self.status = "win"
        elif not self.legal_moves:
            if self.turn == "r":
                self.turn = "b"
            elif self.turn == "b":
                self.turn = "r"
            self.update_legal_moves()
            if not self.legal_moves:
                self.status = "draw"
            else:
                self.status = "win"

    def make_move(self, move, do_update=True) -> None:
        if move not in self.legal_moves:
            raise ValueError(f"Invalid move: {move}")
        else:
            self.state.append(move)
            self.state_history.append(tuple(self.state))
            origin = move[:2]
            end = move[3:]
            self.board[end] = self.board[origin]
            self.board[origin] = " "
            self.last_move = end

            if end[1] == "1" and self.board[end][0] == "r":
                self.board[end] = self.board[end][0] + "_king"
            if end[1] == "8" and self.board[end][0] == "b":
                self.board[end] = self.board[end][0] + "_king"

            is_jump, remove = jump(origin, end)
            if is_jump:
                temp_c = self.board[remove][0]
                if temp_c == "r":
                    self.red_pieces -= 1
                else:
                    self.black_pieces -= 1
                self.board[remove] = " "

            jump_available = False
            if is_jump and len(self.legal_moves) > 0:
                for move in self.legal_moves:
                    if move[:2] == end:
                        jump_available, NA = jump(self.legal_moves[0][:2], self.legal_moves[0][3:])
                        if jump_available:
                            break

            if not jump_available and self.get_status() == "playing":
                if self.turn == "r":
                    self.turn = "b"
                elif self.turn == "b":
                    self.turn = "r"
            if do_update:
                self.update_legal_moves()
                self.update_status()

    def set_board(self, state) -> None:
        for move in state:
            self.make_move(move, do_update=False)
        self.update_legal_moves()
        self.update_status()


def dev_game(game, display_direction="b", custom_board=(False, []), custom_moves=(False, []), random_moves=False):
    from random import choice
    from time import sleep

    print(custom_board)
    if custom_board[0]:
        for row in list("12345678"):
            for col in list("abcdefgh"):
                game.board[col + row] = " "
        for piece in custom_board[1]:
            game.board[piece[0]] = piece[1]
        game.update_legal_moves()
        game.update_status()

    if custom_moves[0]:
        game.set_board(custom_moves[1])

    while game.get_status() == "playing":
        print(game.get_string(turn=display_direction))
        if game.turn == "r":
            print("\033[31mRed\033[0m moves: ", end='')
        else:
            print("\033[90mBlack\033[0m moves: ", end='')
        for move in game.get_legal_moves():
            print(move + ", ", end='')
        print()
        if random_moves:
            game.make_move(choice(game.get_legal_moves()))
            sleep(0.2)
        else:
            move = input("Enter move: ")
            while move not in game.get_legal_moves():
                move = input("Invalid move. Enter move: ")
            game.make_move(move)
        print()

    if game.get_status() == "draw":
        print("Game Over: Draw")
    else:
        if game.turn == "r":
            print("Game Over: \033[31mRed\033[0m wins!")
        else:
            print("Game Over: \033[90mBlack\033[0m wins!")
    print(game.get_string(turn=display_direction))
    print(game.get_state_history())


if __name__ == '__main__':
    #dev_game(game())
    dev_game(game(), custom_board=[True, [["a1", "r_pawn"], ["b2", "b_pawn"]]])

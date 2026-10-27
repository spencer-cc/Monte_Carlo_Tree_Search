from game_env import game_env


def heuristic(game_dict):
    for win_state in (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ):
        temp = 0
        empty = None
        for loc in win_state:
            if game_dict[loc] == "X":
                temp += 1
            if game_dict[loc] == "O":
                temp -= 1
            if game_dict[loc] == " ":
                empty = loc
        if temp in [-2, 2]:
            return empty
    return None


class game(game_env):
    def __init__(self):
        super().__init__()
        self.board = {
            1: " ",
            2: " ",
            3: " ",
            4: " ",
            5: " ",
            6: " ",
            7: " ",
            8: " ",
            9: " ",
        }
        self.empty_spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.state = []
        self.mark = "X"
        self.state_history = [[]]
        self.last_move = None

    def set_board(self, state):
        for move in state:
            self.make_move(move)

    def make_move(self, move):
        if move in self.empty_spaces:
            self.board[move] = self.mark
            self.empty_spaces.remove(move)
            self.state.append(move)
            self.state_history.append(list(self.state))
            self.last_move = move

            if self.mark == "O":
                self.mark = "X"
            elif self.mark == "X":
                self.mark = "O"
        else:
            raise ValueError(f"'{move}' not a legal move.")

    def get_string(self):
        board_lst = [
            self.board[1],
            self.board[2],
            self.board[3],
            self.board[4],
            self.board[5],
            self.board[6],
            self.board[7],
            self.board[8],
            self.board[9],
        ]

        if self.last_move is not None:
            board_lst[self.last_move - 1] = (
                "\033[36m" + board_lst[self.last_move - 1] + "\033[0m"
            )

        for i, cell in enumerate(board_lst):
            if cell == " ":
                board_lst[i] = f"\033[2m{i + 1}\033[0m"

        str_out = (
            f" {board_lst[0]} │ {board_lst[1]} │ {board_lst[2]}\n"
            f"───┼───┼───\n"
            f" {board_lst[3]} │ {board_lst[4]} │ {board_lst[5]}\n"
            f"───┼───┼───\n"
            f" {board_lst[6]} │ {board_lst[7]} │ {board_lst[8]}"
        )
        return str_out

    def get_status(self):
        for line in (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7),
        ):
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                return "win"

        if len(self.empty_spaces) == 0:
            return "draw"

        return "playing"

    def get_legal_moves(self):
        return self.empty_spaces

    def get_state(self):
        return self.state

    def get_dict(self):
        return self.board

    def get_state_history(self):
        return self.state_history

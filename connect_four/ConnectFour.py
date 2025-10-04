from game_env import game_env


# TODO: make a heuristic
def heuristic(game_dict):
    return None


class game(game_env):

    # structure: [column, row]
    #
    # columns: 7
    # rows: 6

    def __init__(self):
        super().__init__()
        self.board = {}
        for col in range(7):
            for row in range(6):
                self.board[(col, row)] = " "
        self.column_heads = [0, 0, 0, 0, 0, 0, 0]

        self.active_player = "0"
        self.state = []
        self.state_history = [[]]
        self.last_move = None

        rChip = '\033[91m\u25CF\033[0m'
        yChip = '\033[93m\u25CF\033[0m'
        self.chips = {" ": " ", "0": rChip, "1": yChip}

    def set_board(self, state):
        for move in state:
            self.make_move(move)

    def make_move(self, move):
        if self.column_heads[move] > 5:
            raise ValueError(f"Illegal move: {move}")
        else:
            self.board[(move, self.column_heads[move])] = self.active_player

            self.column_heads[move] += 1
            self.state.append(move)
            self.state_history.append(tuple(self.state))
            self.last_move = move

            if self.active_player == "1":
                self.active_player = "0"
            else:
                self.active_player = "1"

    def get_status(self):
        # check for draw
        if len(self.get_legal_moves()) == 0:
            return "draw"

        if len(self.state) == 0:
            return "playing"

        # define variables
        col = self.state[-1]
        row = self.column_heads[col] - 1
        last_val = self.board[(col, row)]
        checklists = []

        # get horizontal
        temp = []
        for i in range(7):
            temp.append(self.board[(i, row)])
        checklists.append(temp)

        # get vertical
        temp = []
        for i in range(6):
            temp.append(self.board[(col, i)])
        checklists.append(temp)

        # get diagonals
        diagonal_1_loc = ((col - 3, row + 3), (col - 2, row + 2), (col - 1, row + 1),
                          (col, row),
                          (col + 1, row - 1), (col + 2, row - 2), (col + 3, row - 3))

        diagonal_2_loc = ((col - 3, row - 3), (col - 2, row - 2), (col - 1, row - 1),
                          (col, row),
                          (col + 1, row + 1), (col + 2, row + 2), (col + 3, row + 3))

        for diagonal in [diagonal_1_loc, diagonal_2_loc]:
            temp = []
            for loc in diagonal:
                if (-1 < loc[0] < 7) and (-1 < loc[1] < 6):
                    temp.append(self.board[loc])
            checklists.append(temp)

        # check for win
        for line in checklists:
            consecutive = 0
            for move in line:
                if move == last_val:
                    consecutive += 1
                else:
                    consecutive = 0
                if consecutive == 4:
                    return "win"
        return "playing"

    def get_legal_moves(self):
        out = []
        for i in range(7):
            if self.column_heads[i] < 6:
                out.append(i)
        return out

    def get_state(self):
        return self.state

    def get_dict(self):
        return self.board

    def get_state_history(self):
        return self.state_history

    def get_string(self):
        out = ""
        for row in reversed(range(6)):
            out += "|"
            for col in range(7):
                out += self.chips[self.board[(col, row)]] + "|"
            out += "\n"
        num_row = "|0|1|2|3|4|5|6|"
        if self.last_move is not None:
            num_row = (num_row[:(self.last_move*2+1)] +
                       '\033[36m' + num_row[self.last_move*2+1]
                       + '\033[0m' + num_row[self.last_move*2+2:])
        return out + num_row

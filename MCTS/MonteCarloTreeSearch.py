from math import log as ln
from math import sqrt
from functools import cmp_to_key as custom_sort
from ProgressBar import TimeBar as ProgressBar
from time import time
import game_env
from random import choice


def compare_lists(list1, list2):
    for a, b in zip(list1, list2):
        if a < b:
            return -1
        elif a > b:
            return 1

    return len(list1) - len(list2)


class MCTS:

    # node structure:
    # [wins, visits]

    def __init__(self, time_limit: float, game: game_env, explore_param: float = sqrt(2),
                 heuristic: callable = lambda x: None, show_progress: bool = False, dev_mode: bool = False):

        self.search_tree = {tuple([]): [0, 0]}
        self.exploration_parameter = explore_param
        self.time_limit = time_limit
        self.heuristic = heuristic
        self.game_env = game
        self.dev_mode = dev_mode
        self.playout_stats = []

        self.show_progress = show_progress
        if show_progress:
            self.progress_bar = ProgressBar(20, "playout")
        else:
            self.progress_bar = None

    def get_string(self, depth=None):
        output = ""
        keys = sorted(self.search_tree.keys(), key=len)
        output += f"Playouts: {self.search_tree[keys[0]][1]}\n"
        if self.dev_mode:
            output += f"Playout history: {self.playout_stats}\n"

        keys.sort(key=custom_sort(compare_lists))

        if depth is not None:
            new_keys = []
            for key in keys:
                if len(key) <= depth:
                    new_keys.append(key)
            keys = new_keys

        longest_key_len = 0
        for key in keys:
            key_len = len(str(key))
            if key_len > longest_key_len:
                longest_key_len = key_len

        for key in keys:
            output += f"{str(key):<{longest_key_len}}: {self.search_tree[key]}\n"
        return output

    def UCT(self, parent_state: tuple, child_state: tuple):
        na, parent_visits = self.get_node(parent_state)
        child_wins, child_visits = self.get_node(child_state)
        return (child_wins / child_visits) + (self.exploration_parameter * sqrt(ln(parent_visits) / child_visits))

    def get_node(self, state: tuple):
        return self.search_tree[tuple(state)]

    def create_node(self, state: tuple):
        self.search_tree[state] = [0, 0]

    def update_node(self, state: tuple, delta):
        if state not in self.search_tree.keys():
            pass
        else:
            n, d = self.search_tree[state]
            self.search_tree[state] = [n + delta, d + 1]

    def playout(self, root: game_env):
        root_state = root.get_state()
        moves_from_root = root.get_legal_moves()

        if self.show_progress:
            self.progress_bar.start(self.time_limit)

        if tuple(root_state) not in self.search_tree.keys():
            self.create_node(tuple(root_state))

        if len(moves_from_root) == 1:
            if self.show_progress:
                self.progress_bar.end()
            if self.dev_mode:
                self.playout_stats.append(0)
            return moves_from_root[0]

        start_time = time()
        playouts = 0
        # repeat while time allows
        while (time() - start_time) < self.time_limit:  # start of a game

            playouts += 1

            if self.show_progress:
                self.progress_bar.iterate()

            game = self.game_env.game()
            game.set_board(root_state)
            selection = True

            # selection
            while selection:
                current_state = game.get_state()
                legal_moves = game.get_legal_moves()
                # check if this is a leaf node
                if game.get_status() != "playing":
                    selection = False
                else:
                    for move in legal_moves:
                        if tuple(current_state + [move]) not in self.search_tree.keys():
                            selection = False
                            game.make_move(move)
                            break
                # use UCT to find descent path
                if selection:
                    max_score = float('-inf')
                    best_move = None
                    for move in legal_moves:
                        score = self.UCT(tuple(current_state), tuple(current_state + [move]))
                        if score > max_score:
                            max_score = score
                            best_move = move
                    game.make_move(best_move)

            # expansion
            game_status = game.get_status()
            if tuple(game.get_state()) not in self.search_tree.keys():
                self.create_node(tuple(game.get_state()))
            if game_status == "playing":
                simulation = True
            else:
                simulation = False

            # simulation
            while simulation:
                h = self.heuristic(game.get_dict())
                if h is None:
                    game.make_move(choice(game.get_legal_moves()))
                else:
                    game.make_move(h)
                game_status = game.get_status()
                if game_status != "playing":
                    simulation = False

            # backpropagation
            if game_status == "draw":
                deltas = [0.5, 0.5]
            elif game_status == "win":
                deltas = [1, 0]
            else:
                raise ValueError(f"Game status: {game_status} not allowed")

            for i, state in enumerate(reversed(game.get_state_history())):
                self.update_node(tuple(state), deltas[i % 2])

        if self.dev_mode:
            self.playout_stats.append(playouts)
        if self.show_progress:
            self.progress_bar.end()
            print(f"Playouts: {playouts}")

        # choose move with the highest visits
        max_visits = float('-inf')
        best_move = None
        for move in moves_from_root:
            na, visits = self.search_tree[tuple(root_state + [move])]
            if visits > max_visits:
                max_visits = visits
                best_move = move

        return best_move

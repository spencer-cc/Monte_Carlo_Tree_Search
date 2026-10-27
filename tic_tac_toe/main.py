import TicTacToe
from random import choice
from MonteCarloTreeSearch import MCTS

MCTS_TIME_LIMIT = 2.0


def human_vs_comp(time_limit: float):
    tree = MCTS(time_limit, TicTacToe, heuristic=TicTacToe.heuristic, show_progress=True)

    print("Now playing against MCTS agent, enter moves as 1-9, enter 'k' to exit.")
    i = choice([0, 1])
    game = TicTacToe.game()
    result = None
    if i % 2 == 0:
        print("You are \033[91mX\033[0m")
    else:
        print("You are \033[93mO\033[0m")

    while game.get_status() == "playing":
        print("\n" + game.get_string())

        if i % 2 == 0:
            move = input("Enter move: ")
            while True:
                if move == "k":
                    exit()
                try:
                    if int(move) in game.get_legal_moves():
                        break
                except ValueError:
                    pass
                move = input("Invalid move. Enter move: ")
            game.make_move(int(move))

            if game.get_status() == "win":
                result = "win"
        if i % 2 == 1:
            move = tree.playout(game)
            game.make_move(move)
            if game.get_status() == "win":
                result = "loss"

        i += 1
        print()
    if game.get_status() == "draw":
        result = "draw"

    print(f"game over: {result}")
    print(game.get_string() + "\n")


if __name__ == '__main__':
    human_vs_comp(MCTS_TIME_LIMIT)

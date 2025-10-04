import TicTacToe
from random import choice
from MonteCarloTreeSearch import MCTS


def human_vs_comp(time_limit: float):
    tree = MCTS(time_limit, TicTacToe, heuristic=TicTacToe.heuristic, show_progress=True)

    print("Now playing against MCTS agent, enter moves as 1-9, enter 'k' to exit.")
    i = choice([0, 1])
    while True:
        game = TicTacToe.game()
        result = None

        while game.get_status() == "playing":
            print(game.get_string())

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
            i = choice([1, 0])

        print(f"game over: {result}")
        print(game.get_string() + "\n")


def rand_vs_comp(time_limit: float, number_of_games: int):
    from ProgressBar import IterationBar as ProgressBar
    bar = ProgressBar(50, "testing")

    tree = MCTS(time_limit, TicTacToe, heuristic=TicTacToe.heuristic, show_progress=False)

    wins = 0
    losses = 0
    draws = 0

    bar.start(number_of_games)
    for i in range(number_of_games):
        bar.iterate()
        game = TicTacToe.game()

        i = choice([0, 1])
        while game.get_status() == "playing":

            if i % 2 == 0:
                game.make_move(choice(game.get_legal_moves()))
                if game.get_status() == "win":
                    losses += 1
            if i % 2 == 1:
                game.make_move(tree.playout(game))
                if game.get_status() == "win":
                    wins += 1

            if game.get_status() == "draw":
                draws += 1

            i += 1
    bar.end()

    print(f"Wins: {wins}\nLosses: {losses}\nDraws: {draws}")
    print(f"Raw win ratio: {wins / number_of_games}\nAdjusted win ratio: {(wins + 0.5 * draws) / number_of_games}")


if __name__ == '__main__':
    inp = input("1. Play against MCTS agent\n2. Play MCTS agent against random agent\nEnter choice: ")
    while inp not in ["1", "2"]:
        inp = input("Invalid choice. Enter choice: ")

    if inp == "1":
        limit = float(input("Enter time limit for MCTS agent: "))
        human_vs_comp(limit)

    if inp == "2":
        limit = float(input("Enter time limit for MCTS agent: "))
        num_games = int(input("Enter number of games: "))
        rand_vs_comp(limit, num_games)

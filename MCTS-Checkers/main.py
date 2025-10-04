#import AmericanCheckers_optimized as AmericanCheckers
import AmericanCheckers
from MonteCarloTreeSearch import MCTS
from random import choice
from random import shuffle
from ProgressBar import IterationBar
from time import time


def comp_vs_rand(time_limit: float, iterations: int):
    bar = IterationBar(50, f"{iterations} MCTS vs random games")
    comp_wins = 0
    rand_wins = 0
    draws = 0
    game_durations = []

    bar.start(iterations)
    for i in range(iterations):
        game_start = time()
        game = AmericanCheckers.game()
        tree = MCTS(time_limit, AmericanCheckers, heuristic=AmericanCheckers.heuristic)

        l = ["r", "b"]
        shuffle(l)
        random = l.pop()
        comp = l.pop()

        while game.get_status() == "playing":
            if game.turn == comp:
                game.make_move(tree.playout(game))

            elif game.turn == random:
                game.make_move(choice(game.get_legal_moves()))

        result = game.get_status()
        if result == "win":
            if game.turn == comp:
                comp_wins += 1
            else:
                rand_wins += 1
        elif result == "draw":
            draws += 1
        else:
            raise ValueError(f"Game status: {result} not 'draw' or 'win'")

        game_durations.append(time() - game_start)
        bar.iterate()

    bar.end()
    print(f"MCTS wins: {comp_wins}\nrand wins: {rand_wins}\ndraws: {draws}")
    print(f"MCTS win ratio: {(comp_wins + 0.5*draws) / iterations}\n")
    print(f"Mean game duration: {sum(game_durations) / len(game_durations)}")


def human_vs_comp(time_limit: float):
    game = AmericanCheckers.game()
    tree = MCTS(time_limit, AmericanCheckers, heuristic=AmericanCheckers.heuristic, show_progress=True)

    l = ["r", "b"]
    shuffle(l)
    human = l.pop()
    comp = l.pop()

    while game.get_status() == "playing":
        print(game.get_string(turn=human))
        if game.turn == comp:
            game.make_move(tree.playout(game))

        elif game.turn == human:
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
    print(game.get_string(turn=human))


def bench_MCTS(time_limit: float, iterations: int):
    bar = IterationBar(50, f"MCTS benchmark {iterations} playouts")
    game = AmericanCheckers.game()
    tree = MCTS(time_limit, AmericanCheckers, heuristic=AmericanCheckers.heuristic, dev_mode=True)
    bar.start(iterations)
    for i in range(iterations):
        game.make_move(tree.playout(game))
        bar.iterate()
    bar.end()
    print("\n" + game.get_string())
    print(f"Moves: {iterations}")
    print(tree.get_string(depth=-1))


if __name__ == '__main__':
    from CheckersGUI import run_game
    comp_vs_rand(3, int(input("Games: ")))
    #human_vs_comp(3)
    #bench_MCTS(3, 40)
    #run_game(3)

# TODO: event based game via GUI


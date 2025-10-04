from MonteCarloTreeSearch import MCTS
import ConnectFour
from random import choice


def human_vs_comp(time_limit:  float):
    tree = MCTS(time_limit, ConnectFour, heuristic=ConnectFour.heuristic, show_progress=True)
    i = choice([0, 1])

    print("Now playing against MCTS agent, enter moves as 0-6,  enter 'k' to exit.")
    if i == 0:
        header_string = "You are \033[91mRED\033[0m"
    else:
        header_string = "You are \033[93mYELLOW\033[0m"

    game = ConnectFour.game()
    result = None
    while game.get_status() == "playing":

        if i % 2 == 0:
            print(header_string)
            print(game.get_string())
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
            print(game.get_string(), end='')
            move = tree.playout(game)
            game.make_move(move)

            if game.get_status() == "win":
                result = "loss"

        i += 1
        print("\n")
    if game.get_status() == "draw":
        result = "draw"
        i = choice([1, 0])

    if result == "win":
        print("Game Over: \033[32mYou Win\033[0m")
    elif result == "loss":
        print("Game Over: \033[91mYou Lost!\033[0m")
    else:
        print("Game Over: \033[34mDraw!\033[0m")
    print(game.get_string())


if __name__ == '__main__':
    human_vs_comp(2.5)

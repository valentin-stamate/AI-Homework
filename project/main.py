from stockfish import Stockfish
import chess
import chess.pgn
from minimax import minimax
from util import print_white, print_black
import matplotlib.pyplot as plt

ENV_PATH = 'stockfish_14.1_win_x64_avx2.exe'
FILE = 'stats.txt'
DEPTH = 3


def get_best_move(agent: Stockfish):
    game = chess.Board(agent.get_fen_position())

    _eval = minimax(game, 0, True, -50000, 50000, DEPTH)
    return _eval['move']


def start():
    env_path = ENV_PATH
    # Stockfish is black, up, lowercase
    stockfish = Stockfish(env_path, parameters={'Threads': 1})
    stockfish.set_position([])

    # Agent is white, down, UPPERCASE
    agent = Stockfish(env_path, parameters={'Threads': 1})
    stockfish.set_position([])
    agent.set_depth(1)

    game = chess.Board(stockfish.get_fen_position())
    pgn_game = chess.pgn.Game()
    node = pgn_game

    ms = 500
    total_moves = 0

    while True:
        print("Move:", total_moves)
        # ---------------================== Agent | White ==================---------------
        print_white(game)
        # moves = to_list(game.legal_moves)

        agent_move = get_best_move(agent)

        print_white(f"Agent move : {agent_move}")
        # print_white(f"Possible moves: {moves}")

        stockfish.make_moves_from_current_position([agent_move])
        agent.make_moves_from_current_position([agent_move])
        game.push(chess.Move.from_uci(agent_move))

        node = node.add_variation(chess.Move.from_uci(agent_move))

        if game.is_checkmate():
            print("Agent wins.")
            break

        print('\n')

        # ---------------================== Stockfish | Black ==================---------------
        print_black(game)
        # moves = to_list(game.legal_moves)

        st_move = stockfish.get_best_move_time(ms)

        print_black(f"Stockfish move : {st_move}")
        # print_black(f"Possible moves: {moves}")

        stockfish.make_moves_from_current_position([st_move])
        agent.make_moves_from_current_position([st_move])
        game.push(chess.Move.from_uci(st_move))

        node = node.add_variation(chess.Move.from_uci(st_move))

        total_moves += 1

        if game.is_checkmate():
            print("Stockfish wins.")
            break

        print('\n')

    print("\n")
    pgn_game.headers["Result"] = game.result()
    pgn_game.headers["Moves"] = str(total_moves)
    print("Game PGN\n", pgn_game)

    with open(FILE, 'a') as f:
        f.write('PGN\n')
        f.write(pgn_game.__str__())

    return total_moves


def main():
    with open(FILE, 'a') as f:
        f.write(f'Game starts. Depth {DEPTH}\n')

    x = []
    for i in range(0, 30):
        with open(FILE, 'a') as f:
            f.write(f"Game {i}\n")

        try:
            moves = start()
            x.append(moves)
        except Exception as e:
            print('Something went wrong')
            print(e)

        plt.plot(x)
        plt.show()

        with open(FILE, 'a') as f:
            f.write(f"\n\n")

    plt.plot(x)
    plt.title(f'Agent(depth {DEPTH}) VS Stockfish')
    plt.xlabel('Game')
    plt.ylabel('Moves')
    plt.show()

    with open(FILE, 'a') as f:
        f.write('Evolution\n')
        f.write(x.__str__())


if __name__ == '__main__':
    main()

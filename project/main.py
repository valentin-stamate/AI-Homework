from stockfish import Stockfish
import chess
import chess.pgn
from minimax import minimax, INFINITY
from models import BestMove
from util import print_white, print_black

ENV_PATH = 'stockfish_14.1_win_x64_avx2.exe'


def get_best_move(agent: Stockfish):
    best_move = BestMove()

    game = chess.Board(agent.get_fen_position())
    minimax(game, 0, True, -INFINITY, +INFINITY, 3, best_move)

    if best_move.move == '':
        print("Something went wrong")

    return best_move.move


def start():
    env_path = ENV_PATH
    # Stockfish is black, up, lowercase
    stockfish = Stockfish(env_path, parameters={'Threads': 1})

    # Agent is white, down, UPPERCASE
    agent = Stockfish(env_path, parameters={'Threads': 1})
    agent.set_depth(1)

    game = chess.Board()
    pgn_game = chess.pgn.Game()
    node = pgn_game

    ms = 500
    total_moves = 0

    while True:
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

        total_moves += 1

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


def main():
    start()


if __name__ == '__main__':
    main()

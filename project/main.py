from stockfish import Stockfish
import chess


def colored(text, r, g, b, ):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def print_black(obj):
    print(colored(obj, 100, 100, 100))


def print_white(obj):
    print(colored(obj, 255, 255, 255))


def to_list(moves: [chess.Move]):
    str_moves = []

    for move in moves:
        str_moves.append(move.uci())

    return str_moves


def start():
    env_path = 'stockfish_14.1_win_x64_avx2.exe'
    # Stockfish is black, up, lowercase
    stockfish = Stockfish(env_path, parameters={'Threads': 1})

    # Agent is white, down, UPPERCASE
    agent = Stockfish(env_path, parameters={'Threads': 1})
    agent.set_depth(1)

    game = chess.Board()
    ms = 500

    while True:
        # ---------------================== Agent | White ==================---------------
        print_white(game)
        moves = to_list(game.legal_moves)

        agent_move = agent.get_best_move()

        print_white(f"Agent move : {agent_move}")
        print_white(f"Possible moves: {moves}")

        stockfish.make_moves_from_current_position([agent_move])
        agent.make_moves_from_current_position([agent_move])
        game.push(chess.Move.from_uci(agent_move))

        if game.is_checkmate():
            print("Agent wins.")
            break

        print('\n')
        # ---------------================== Stockfish | Black ==================---------------
        print_black(game)
        moves = to_list(game.legal_moves)

        st_move = stockfish.get_best_move_time(ms)

        print_black(f"Stockfish move : {st_move}")
        print_black(f"Possible moves: {moves}")

        stockfish.make_moves_from_current_position([st_move])
        agent.make_moves_from_current_position([st_move])
        game.push(chess.Move.from_uci(st_move))

        if game.is_checkmate():
            print("Stockfish wins.")
            break

        print('\n')


def main():
    start()


if __name__ == '__main__':
    main()

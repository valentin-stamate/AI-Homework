from stockfish import Stockfish


def start():
    env_path = 'stockfish_14.1_win_x64_avx2.exe'
    # Stockfish is white, down, UPPERCASE
    stockfish = Stockfish(env_path, parameters={'Threads': 1})
    stockfish.set_position([])

    # Agent is black, up, lowecase
    agent = Stockfish(env_path, parameters={'Threads': 1})
    agent.set_depth(1)
    agent.set_position([])

    ms = 500

    for i in range(0, 1200):
        print("Stockfis")
        st_move = stockfish.get_best_move_time(1000)
        st_eval = stockfish.get_evaluation()

        if st_move is None:
            print("Agent wins")
            print(stockfish.get_board_visual())
            break

        print(f"    Eval{stockfish.get_evaluation()}")
        print(f"    Move {st_move}")

        stockfish.make_moves_from_current_position([st_move])
        agent.make_moves_from_current_position([st_move])

        print("Agent")
        agent_move = agent.get_best_move()
        agent_eval = agent.get_evaluation()

        if agent_move is None:
            print("Stockfish wins")
            print(stockfish.get_board_visual())
            break

        print(f"    Eval{agent.get_evaluation()}")
        print(f"    Move {agent_move}")

        stockfish.make_moves_from_current_position([agent_move])
        agent.make_moves_from_current_position([agent_move])

        print(stockfish.get_board_visual())

def main():
    # env_path = 'stockfish_14.1_win_x64_avx2.exe'
    # stockfish = Stockfish(env_path, parameters={'Threads': 1})
    #
    # agent = Stockfish(env_path, parameters={'Threads': 1})
    # agent.set_depth(1)
    #
    # print(agent.get_evaluation(), stockfish.get_evaluation())
    #
    # # Makes a move
    # stockfish.set_position(['e2e4']) # down, up - white, black
    # agent.set_position(['e2e4', 'e7e6'])
    #
    # print(stockfish.get_board_visual())
    #
    # print(agent.get_evaluation(), stockfish.get_evaluation())
    # # This is how we'll interact with the stockfish
    # move = stockfish.get_best_move_time(500)
    # print(move)
    #
    # stockfish.make_moves_from_current_position(['e3e4'])
    # agent.make_moves_from_current_position(['e2e4'])
    #
    # print(stockfish.get_evaluation(), agent.get_evaluation())
    #
    # print(stockfish.get_board_visual())
    # print(stockfish.get_fen_position())

    start()


if __name__ == '__main__':
    main()

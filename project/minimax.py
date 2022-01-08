import chess
from chess.engine import BestMove
from stockfish import Stockfish
from util import to_list

INFINITY = 5000
ENV_PATH = 'stockfish_14.1_win_x64_avx2.exe'


def minimax(game: chess.Board, depth, is_maximizing_player, alpha, beta, max_depth, best_move: BestMove):

    if depth == max_depth:
        fen_position = game.fen()

        agent = Stockfish(ENV_PATH, parameters={'Threads': 1})
        agent.set_depth(1)
        agent.set_fen_position(fen_position)

        v = agent.get_evaluation()
        print(v, is_maximizing_player)
        return v['value']

    if is_maximizing_player:
        best_val = -INFINITY

        moves = to_list(game.legal_moves)
        for move in moves:
            game.push(chess.Move.from_uci(move))
            value = minimax(game, depth + 1, False, alpha, beta, max_depth, best_move)
            game.pop()

            if value > best_val:
                best_val = value
                best_move.move = move

            alpha = max(alpha, best_val)

            if beta <= alpha:
                break

        return best_val

    else:
        best_val = -INFINITY

        moves = to_list(game.legal_moves)

        for move in moves:
            game.push(chess.Move.from_uci(move))
            value = minimax(game, depth + 1, True, alpha, beta, max_depth, best_move)
            game.pop()

            if value > best_val:
                best_val = value
                best_move.move = move

            alpha = max(alpha, best_val)

            if beta <= alpha:
                break

        return best_val

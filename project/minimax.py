import chess
from stockfish import Stockfish
from util import to_list

INFINITY = 50000
ENV_PATH = 'stockfish_14.1_win_x64_avx2.exe'


cache = {}

agent = Stockfish(ENV_PATH, parameters={'Threads': 1})
agent.set_depth(1)
agent.set_position()


def minimax(game: chess.Board, depth, maximizing, alpha, beta, max_depth):
    current_fen = game.fen()
    state = f'{current_fen}{depth % 2}'

    global agent

    # if state in cache:
    #     return cache[state]

    if depth == max_depth or game.is_checkmate():
        agent.set_fen_position(current_fen)
        _eval = agent.get_evaluation()
        check_mate(_eval, depth + 1)

        # cache[state] = _eval
        return _eval

    moves = to_list(game.legal_moves)
    best_eval = None

    if maximizing:
        best_val = -INFINITY
        for move in moves:
            game.push(chess.Move.from_uci(move))
            _eval = minimax(game, depth + 1, False, alpha, beta, max_depth)
            game.pop()

            value = _eval['value']

            if value > best_val:
                best_val = value
                best_eval = _eval
                best_eval['move'] = move

            alpha = max(alpha, _eval['value'])

            if beta <= alpha:
                break

        cache[state] = best_eval
        return best_eval

    if not maximizing:
        best_val = +INFINITY

        for move in moves:
            game.push(chess.Move.from_uci(move))
            _eval = minimax(game, depth + 1, True, alpha, beta, max_depth)
            game.pop()

            value = _eval['value']

            if value < best_val:
                best_val = value
                best_eval = _eval
                best_eval['move'] = move

            beta = min(beta, _eval['value'])

            if game.is_checkmate():
                game.pop()
                return _eval

            if beta <= alpha:
                break

        cache[state] = best_eval
        return best_eval


def check_mate(_eval, depth):
    if _eval['type'] == 'mate':
        if depth % 2 == 0:
            _eval['value'] = 10000
        if depth % 2 == 1:
            _eval['value'] = -10000

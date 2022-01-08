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

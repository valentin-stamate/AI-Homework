import re


class Problem:

    def __init__(self, n):
        """ ('s', 's') -> (husband, wife)
            d -> right side
            s -> left side
        """
        self.state = Problem.initialize(n)
        self.boat_side = 's'

    @staticmethod
    def initialize(n):
        """ initial state -> all couples are ('s', 's') """
        return [('s', 's') for i in range(n)]

    @staticmethod
    def is_solution(state, boat):
        """ final state -> all couples are ('d', 'd') """
        if boat != 'd':
            return False

        for pair in state:
            if pair[0] == 's' or pair[1] == 's':
                return False
        return True

    @staticmethod
    def is_valid(state):
        return Problem.check_condition(state, 's') and Problem.check_condition(state, 'd')

    @staticmethod
    def check_condition(state, side):
        for pair in state:
            if pair[1] == side and pair[0] != side:
                for pair_2 in state:
                    if pair_2[0] == side:
                        return False
        return True

    @staticmethod
    def valid_transition(state, pair_1_index, pair_1_type, pair_2_index = None, pair_2_type = None):
        new_state = list(state)
        new_state = Problem.transition(new_state, pair_1_index, pair_1_type, pair_2_index, pair_2_type)

        if Problem.is_valid(new_state):
            return True, new_state

        return False, state

    @staticmethod
    def transition(state, pair_1_index, pair_1_type, pair_2_index = None, pair_2_type = None):
        state[pair_1_index][pair_1_type] = Problem.change_side(state[pair_1_index][pair_1_type])

        if pair_2_index is not None:
            state[pair_2_index][pair_2_type] = Problem.change_side(state[pair_2_index][pair_2_type])

        return state

    @staticmethod
    def change_side(side):
        if side == 'd':
            return 's'
        return 'd'


def main():
    print("Hello World!")


if __name__ == '__main__':
    main()

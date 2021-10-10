import copy

left = 0
right = 1


class State:

    def __init__(self, couples, position=None, boat=None):
        """ ('0', '0') -> (husband, wife)
            0 -> left side
            1 -> right side
        """
        if position is None or boat is None:
            position, boat = State.initialize(couples)

        self.positions = position
        self.boat = boat
        self.couples = couples

    def is_solution(self):
        """ final state -> all couples are (1, 1) """
        if self.boat != right:
            return False

        for pair in self.positions:
            if pair[0] == left or pair[1] == left:
                return False
        return True

    def side_is_valid(self, side):
        for pair in self.positions:
            if pair[1] == side and pair[0] != side:
                for pair_2 in self.positions:
                    if pair_2[0] == side:
                        return False
        return True

    def state_is_valid(self):
        return self.side_is_valid(left) and self.side_is_valid(right)

    @staticmethod
    def initialize(couples):
        """ initial state -> all couples are (0, 0) """
        return [[left, left] for i in range(couples)], left

    @staticmethod
    def copy(state):
        new_position = copy.deepcopy(state.positions)
        return State(state.couples, new_position, state.boat)

    def valid_transition(self, couple_1_index, couple_1_type, couple_2_index=None, couple_2_type=None):
        """ If the transition is valid, the new transition is returned """
        if self.positions[couple_1_index][couple_1_type] != self.boat:
            return None

        if couple_2_index is not None:
            if self.positions[couple_2_index][couple_2_type] != self.boat:
                return None

        new_transitioned_state = State.transition(State.copy(self), couple_1_index, couple_1_type, couple_2_index, couple_2_type)

        if new_transitioned_state.state_is_valid():
            return new_transitioned_state

        return None

    @staticmethod
    def transition(state, couple_1_index, couple_1_type, couple_2_index, couple_2_type):
        """ The new transition is returned """
        state.positions[couple_1_index][couple_1_type] = 1 - state.positions[couple_1_index][couple_1_type]

        if couple_2_index is not None:
            state.positions[couple_2_index][couple_2_type] = 1 - state.positions[couple_2_index][couple_2_type]

        state.boat = 1 - state.boat

        return state

    def show(self):
        print(self.positions)
        print(self.boat)

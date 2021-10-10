import copy

left = 0
right = 1


class State:

    def __init__(self, couples, position=None, boat=None):
        """ 01010011  -> 2*k : husband, 2*k + 1 : wife
            0 -> left side
            1 -> right side
        """
        self.length = couples * 2

        if position is None or boat is None:
            position, boat = State.initialize(self.length)

        self.positions = position
        self.boat = boat

    def is_solution(self):
        """ final state -> the state looks like 000.0 """
        if self.boat != right:
            return False

        for i in range(0, self.length, 2):
            if self.positions[i] == left or self.positions[i + 1] == left:
                return False
        return True

    def side_is_valid(self, side):
        for i in range(0, self.length, 2):
            if self.positions[i + 1] == side and self.positions[i] != side:
                for j in range(0, self.length, 2):
                    if self.positions[j] == side:
                        return False
        return True

    def state_is_valid(self):
        return self.side_is_valid(left) and self.side_is_valid(right)

    @staticmethod
    def initialize(length):
        """ initial state -> 000..0 """
        return [left for i in range(length)], left

    @staticmethod
    def copy(state):
        new_position = copy.deepcopy(state.positions)
        return State(state.length // 2, new_position, state.boat)

    @staticmethod
    def valid_transition(state, person_a, person_b=None):
        """ If the transition is valid, the new transition is returned """
        if state.positions[person_a] != state.boat:
            return None

        if person_b is not None:
            if state.positions[person_b] != state.boat:
                return None

        new_transitioned_state = State.transition(State.copy(state), person_a, person_b)

        if new_transitioned_state.state_is_valid():
            return new_transitioned_state

        return None

    @staticmethod
    def transition(state, person_a, person_b):
        """ The new transition is returned """
        state.positions[person_a] = 1 - state.positions[person_a]

        if person_b is not None:
            state.positions[person_b] = 1 - state.positions[person_b]

        state.boat = 1 - state.boat

        return state

    @staticmethod
    def neighbours(state):
        n = state.length

        neighbours = []
        for i in range(n):
            neighbour = State.valid_transition(state, i)

            if neighbour is not None:
                neighbours.append(neighbour)

            for j in range(i + 1, n):
                neighbour = State.valid_transition(state, i, j)

                if neighbour is not None:
                    neighbours.append(neighbour)

        return neighbours

    def show(self):
        print(f"State: {self.positions}")
        print(f"Boat: {self.boat}")

    def as_key(self):
        key = 0

        for i in range(self.length):
            key += (1 << i) * self.positions[i]

        key += (1 << self.length) * self.boat

        return key

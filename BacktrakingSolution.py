import copy

from state import State


class BKTSolution:
    def __init__(self, state):
        self.state = state
        self.solution = []
        self.BKT(self.state, None, self.state.boat)

    def BKT(self, state, previous_state, boat_side):
        if state.is_solution():
            print(self.solution)
        else:
            for p1 in range(len(state.positions)):
                for p2 in range(len(state.positions)):
                    for t1 in range(2):
                        for t2 in range(2):
                            if p1 != p2 or (p1 == p2 and t1 != t2):
                                status = state.valid_transition(p1, t1)
                                previous_state = copy.deepcopy(state.positions)
                                if status is not None and status != previous_state:
                                    state = status
                                    print(state.positions)
                                    self.solution.append(
                                        {"side-from": boat_side, "index1": p1, "type1": t1})
                                    self.state.boat = 1 - self.state.boat
                                    self.BKT(state, previous_state, boat_side)
                                    # self.solution.remove(
                                    #     {"side-from": boat_side, "index1": p1, "type1": t1})
                                status = state.valid_transition(p2, t2)
                                if status is not None and status != previous_state:
                                    state = status
                                    print(state.positions)
                                    self.solution.append(
                                        {"side-from": boat_side, "index1": p2, "type1": t2})
                                    self.state.boat = 1 - self.state.boat
                                    self.BKT(state, previous_state, boat_side)
                                    # self.solution.remove(
                                    #     {"side-from": boat_side, "index1": p2, "type1": t2})
                                status = state.valid_transition(p1, t1, p2, t2)
                                if status is not None and status != previous_state:
                                    state = status
                                    print(state.positions)
                                    self.solution.append(
                                        {"side-from": boat_side, "index1": p1, "type1": t1,
                                         "index2": p2, "type2": t2})
                                    self.state.boat = 1 - self.state.boat
                                    self.BKT(state, previous_state, boat_side)
                                    # self.solution.remove(
                                    #     {"side-from": boat_side, "index1": p1, "type1": t1,
                                    #      "index2": p2, "type2": t2})

    def print_transition(self, boat_side, p1, t1, p2, t2):
        print()


if __name__ == "__main__":
    state = State(3)
    BKTSolution(state)

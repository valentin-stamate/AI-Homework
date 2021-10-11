import copy
import sys
import time


from state import State
# import resource, sys

# resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
sys.setrecursionlimit(10 ** 6)


def sol_print(solution):
    for x in solution:
        print(x)


def print_river(states):
    for state in states:
        for x in range(len(state)):
            if state[x] == 0:
                print("* | |  ")
            else:
                print("  | | *")
        time.sleep(1)
        import os
        os.system('cls')


class BKTSolution:
    def __init__(self, state):
        self.state = state
        self.best_solution = []
        self.solution = []
        self.previous_states = [[0, 0, 0, 0, 0, 0]]
        self.best_len = 100
        self.BKT(self.state)
        print_river(self.best_solution)

    def BKT(self, current_state):
        if current_state.is_solution():
            if len(self.solution) < self.best_len:
                self.best_len = len(self.solution)
                self.best_solution = copy.deepcopy(self.solution)
        else:
            for p1 in range(self.state.length):
                for p2 in range(p1 + 1, self.state.length):
                    self.previous_states.append(current_state.positions)
                    new_state = State.valid_transition(current_state, p1, p2)
                    if new_state is not None:
                        if new_state.positions not in self.previous_states:
                            self.solution.append(current_state.positions)
                            self.BKT(new_state)
                            self.solution.pop()
                            self.previous_states.pop()
                    new_state = State.valid_transition(current_state, p2)
                    if new_state is not None:
                        if new_state.positions not in self.previous_states:
                            self.solution.append(current_state.positions)
                            self.BKT(new_state)
                            self.solution.pop()
                            self.previous_states.pop()
                    new_state = State.valid_transition(current_state, p1)
                    if new_state is not None:
                        if new_state.positions not in self.previous_states:
                            self.solution.append(current_state.positions)
                            self.BKT(new_state)
                            self.solution.pop()
                            self.previous_states.pop()
                    self.previous_states.pop()


if __name__ == "__main__":
    state = State(3)
    BKTSolution(state)

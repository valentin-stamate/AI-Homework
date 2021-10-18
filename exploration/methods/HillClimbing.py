from state import State


def f(state):
    return len([x for x in state.positions if x == 1])


def hill_climbing(state):
    visited = set()
    parents = dict()

    ok = True
    while not state.is_solution() and ok:
        max_f = 0
        ok = False
        visited.add(state.as_key())
        neighbours = State.neighbours(state)
        for neighbour in neighbours:
            key = neighbour.as_key()
            if key not in visited and f(neighbour) + (1 - neighbour.boat) > max_f:
                max_f = f(neighbour)
                new_key = key
                new_neighbour = neighbour
                ok = True
        parents[new_key] = state
        state = new_neighbour
        if state.is_solution():
            return state, parents

    print("Complete solution not found")
    print("Best solution found is:")
    return state, parents

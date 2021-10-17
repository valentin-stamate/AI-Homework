from state import State


def backtracking(state: State, visited: set, parents: dict, solution):
    if state.is_solution():
        current_key = state.as_key()

        steps = [state]

        while parents.get(current_key) is not None:
            parent = parents.get(current_key)
            steps.append(parent)
            current_key = parent.as_key()

        if len(solution[0]) == 0:
            solution[0] = steps

        if len(solution[0]) >= len(steps):
            solution[0] = steps

        solution[1] += 1
        return None

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

    visited.add(state.as_key())

    unvisited_neighbours = [n for n in neighbours if n.as_key() not in visited]

    if len(neighbours) == 0:
        visited.remove(state.as_key())
        return None

    for node in unvisited_neighbours:
        parents[node.as_key()] = state
        backtracking(node, visited, parents, solution)

    visited.remove(state.as_key())
    return None

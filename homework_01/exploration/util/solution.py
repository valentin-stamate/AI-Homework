def print_transition(state, new_state):
    persons = []
    for i in range(len(state.positions)):
        if state.positions[i] != new_state.positions[i]:
            persons.append(i)
    p_type = ["Husband ", "Wife    "]
    side = ["Left", 'Right']
    if len(persons) == 2:
        if state.positions[persons[1]] == 1:
            sides = " " + side[1] + '->' + side[0]
        else:
            sides = " " + side[0] + '->' + side[1]
        if persons[0] % 2 == 0:
            p1 = p_type[0] + str(persons[0] // 2)
        else:
            p1 = p_type[1] + str(persons[0] // 2)
        if persons[1] % 2 == 0:
            p2 = p_type[0] + str(persons[1] // 2)
        else:
            p2 = p_type[1] + str(persons[1] // 2)
        print(p1 + ", " + p2 + sides)

    else:
        if state.positions[persons[0]] == 1:
            sides = " " + side[1] + '->' + side[0]
        else:
            sides = " " + side[0] + '->' + side[1]
        if persons[0] % 2 == 0:
            p = p_type[0] + str(persons[0] // 2)
        else:
            p = p_type[1] + str(persons[0] // 2)
        print(p + "           " + sides)


def print_solution(node, parents):
    print("Raw Steps:")
    current_key = node.as_key()

    steps = []

    while parents.get(current_key) is not None:
        parent = parents.get(current_key)
        steps.append(parent)
        current_key = parent.as_key()

    i = 0
    while len(steps) > 0:
        print(i)
        state = steps.pop()
        state.show()
        i += 1
        print()

    print(i + 1)
    node.show()


def build_transitions(node, parents):
    print("Transitions:")
    current_key = node.as_key()
    steps = []

    while parents.get(current_key) is not None:
        parent = parents.get(current_key)
        steps.append(parent)
        current_key = parent.as_key()

    i = 0
    state = steps.pop()
    while len(steps) > 0:
        new_state = steps.pop()
        print_transition(state, new_state)
        state = new_state
        i += 1
    print_transition(state, node)

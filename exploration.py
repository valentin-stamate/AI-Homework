import HillClimbing
from back import backtracking
from state import State


# noinspection DuplicatedCode
class Exploration:

    @staticmethod
    def buildSolution(node, parents):
        print("Steps:")
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

    @staticmethod
    def build_transitions(node, parents):
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
            Exploration.print_transition(state, new_state)
            i += 1
        Exploration.print_transition(state, node)

    @classmethod
    def print_transition(cls, state, new_state):
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
            if state.positions[persons[0]] == 0:
                sides = " " + side[1] + '->' + side[0]
            else:
                sides = " " + side[0] + '->' + side[1]
            if persons[0] % 2 == 0:
                p = p_type[0] + str(persons[0] // 2)
            else:
                p = p_type[1] + str(persons[0] // 2)
            print(p + sides)

    @staticmethod
    def BackTracking(state):
        # BKTSolution(state)
        solution = [[], 0]
        backtracking(state, set(), dict(), solution)

        print("Best solution:")

        n = len(solution[0])
        for i in range(n):
            print(i)
            solution[0][n - i - 1].show()
            print()

    # noinspection DuplicatedCode
    @staticmethod
    def bfs(state):

        queue = [state]

        visited = set()
        parents = dict()

        while len(queue) > 0:
            node = queue.pop(0)
            visited.add(node.as_key())

            if node.is_solution():
                Exploration.buildSolution(node, parents)
                return node

            neighbours = State.neighbours(node)

            for neighbour in neighbours:
                key = neighbour.as_key()
                if key not in visited:
                    parents[key] = node
                    queue.append(neighbour)

        print("Not found")
        return state

    @staticmethod
    def dfs(state):
        stack = [state]

        visited = set()
        parents = dict()

        while len(stack) > 0:
            node = stack.pop()
            visited.add(node.as_key())

            if node.is_solution():
                Exploration.build_transitions(node, parents)
                return node

            neighbours = State.neighbours(node)

            for neighbour in neighbours:
                key = neighbour.as_key()

                if key not in visited:
                    parents[key] = node
                    stack.append(neighbour)

        print("Not found")
        return state

    @staticmethod
    def hill_climbing(state):
        results = HillClimbing.hill_climbing(state)
        Exploration.build_transitions(results[0], results[1])

        return None

    @staticmethod
    def astar(state):
        print("Not implemented yet.")
        return None

    @staticmethod
    def start():
        print("""
        Backtracking = 1
        BFS          = 2
        DFS          = 3
        HillClimbing = 4
        AStar        = 5
        """)

        choice = int(input("Enter your choice: "))
        couples = int(input("The number of couples: "))
        print("")

        state = State(couples)

        if choice == 1:
            Exploration.BackTracking(state)

        if choice == 2:
            Exploration.bfs(state)

        if choice == 3:
            Exploration.dfs(state)

        if choice == 4:
            Exploration.hill_climbing(state)

        if choice == 5:
            Exploration.astar(state)

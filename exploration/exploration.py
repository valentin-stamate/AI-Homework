from exploration.methods import HillClimbing
from exploration.methods.astar import AStar
from exploration.methods.back import backtracking
from exploration.util.solution import print_solution, build_transitions, print_transition
from state import State


# noinspection DuplicatedCode
class Exploration:

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

        print("Transitions:")
        state = solution[0].pop()
        while len(solution[0]) > 0:
            new_state = solution[0].pop()
            print_transition(state, new_state)
            state = new_state


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
                print_solution(node, parents)
                print("")
                build_transitions(node, parents)
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
                print_solution(node, parents)
                print("")
                build_transitions(node, parents)
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
        build_transitions(results[0], results[1])

        return None

    @staticmethod
    def astar(state):
        AStar.fun(state)

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

from back import backtracking
from state import State
from BacktrakingSolution import BKTSolution


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
                Exploration.buildSolution(node, parents)
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
        print("Not implemented yet.")
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


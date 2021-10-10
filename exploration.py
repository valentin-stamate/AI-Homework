from state import State
from BacktrakingSolution import BKTSolution

class Exploration:

    @staticmethod
    def BackTracking(state):
        BKTSolution(state)
        return None

    @staticmethod
    def BFS(state):
        return None

    @staticmethod
    def DFS(state):
        return None

    @staticmethod
    def HillClimbing(state):
        return None

    @staticmethod
    def AStar(state):
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

        choice = int(input("Enter your choise: "))
        couples = int(input("The number of couples: "))

        state = State(couples)
        if choice == 1:
            Exploration.BackTracking(state)

        if choice == 2:
            Exploration.BFS(state)

        if choice == 3:
            Exploration.DFS(state)

        if choice == 4:
            Exploration.HillClimbing(state)

        if choice == 5:
            Exploration.AStar(state)

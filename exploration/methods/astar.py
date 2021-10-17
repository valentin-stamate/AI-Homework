from exploration.util.solution import print_solution, build_transitions
from state import State

class AStar:

    @staticmethod
    def fun(state: State):
        n = state.length
        goal = State(n)
        goal.boat = 1
        goal.positions = [1 for i in range(n)]

        cost = dict()
        heuristic = dict()
        visited = set()
        parents = dict()

        cost[state.as_key()] = 0
        heuristic[state.as_key()] = AStar.distance(state, goal)

        pq = []
        pq.append([cost[state.as_key()] + heuristic[state.as_key()], state])

        while len(pq) > 0:
            AStar.sort(pq)
            node = pq.pop(0)[1]
            visited.add(node.as_key())

            if node.is_solution():
                print_solution(node, parents)
                print("")
                build_transitions(node, parents)
                return

            neighbours = State.neighbours(node)

            for neighbour in neighbours:
                key = neighbour.as_key()
                if key not in visited:
                    c = cost[node.as_key()] + 1
                    h = AStar.distance(neighbour, goal)

                    if AStar.is_in_priority_queue(neighbour, pq):
                        old_c = cost[key]
                        old_h = heuristic[key]

                        if old_c + old_h > c + h:
                            cost[key] = c
                            heuristic[key] = h

                            AStar.update(neighbour, pq, c + h)
                            parents[key] = node
                    else:
                        cost[neighbour.as_key()] = c
                        heuristic[neighbour.as_key()] = h

                        pq.append([c + h, neighbour])
                        parents[key] = node

        print("Not found")

    @staticmethod
    def sort(list_: []):
        list_.sort(key=lambda x: x[0])

    @staticmethod
    def update(state, list_, new_cost):
        for i in range(len(list_)):
            if list_[i][1].as_key() == state.as_key():
                list_[i][0] = new_cost
                return
        return

    @staticmethod
    def is_in_priority_queue(state, pq):
        for el in pq:
            if el[1].as_key() == state.as_key():
                return True
        return False

    @staticmethod
    def distance(a, b):
        sum_a = sum(a.positions) + a.boat
        sum_b = sum(b.positions) + b.boat

        return abs(sum_b - sum_a)



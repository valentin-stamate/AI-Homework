
# Environment based on the Frozen Lake game
import numpy as np


class Experience:
    def __init__(self, state, action, reward, next_state):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state

    def __str__(self):
        return f'State={self.state}\nAction={self.action}\nReward={self.reward}\nNextState={self.next_state}\n'

    def get_attributes(self):
        return [self.state, self.action, self.reward, self.next_state]

    def split(self):
        return self.state, self.action, self.reward, self.next_state


class CellType:
    PLAYER = 0
    SOLID = 1
    HOLE = 2
    FINISH = 3


class ActionType:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    actions = [0, 1, 2, 3]


class Environment:
    rows = 4
    columns = 4
    actions = ActionType.actions

    initial_state = [
        [0, 1, 1, 1],
        [1, 2, 1, 2],
        [1, 1, 1, 2],
        [2, 1, 1, 3],
    ]

    final_state = [
        [1, 1, 1, 1],
        [1, 2, 1, 2],
        [1, 1, 1, 2],
        [2, 1, 1, 0],
    ]

    @staticmethod
    def make_transition(state, action):
        player = Environment.player_position(state)

        new_state = Environment.copy_state(state)

        changed = False

        if action == ActionType.LEFT and player[1] != 0:
            new_state[player[0]][player[1] - 1] = CellType.PLAYER
            changed = True

        if action == ActionType.UP and player[0] != 0:
            new_state[player[0] - 1][player[1]] = CellType.PLAYER
            changed = True

        if action == ActionType.RIGHT and player[1] != 3:
            new_state[player[0]][player[1] + 1] = CellType.PLAYER
            changed = True

        if action == ActionType.DOWN and player[0] != 3:
            new_state[player[0] + 1][player[1]] = CellType.PLAYER
            changed = True

        if changed:
            new_state[player[0]][player[1]] = CellType.SOLID

            new_player = Environment.player_position(new_state)

            i = new_player[0]
            j = new_player[1]

            if state[i][j] == CellType.HOLE:
                return Experience(state, action, -50, None)

        else:
            new_state = Environment.copy_state(state)

        reward = 0

        # If The Player Moved to a
        if action == ActionType.LEFT and player[1] == 0:
            reward = -10

        if action == ActionType.UP and player[0] == 0:
            reward = -10

        if action == ActionType.RIGHT and player[1] == 3:
            reward = -10

        if action == ActionType.DOWN and player[0] == 3:
            reward = -10

        if Environment.is_final_state(new_state):
            reward = 100

        return Experience(state, action, reward, new_state)

    @staticmethod
    def player_position(state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == CellType.PLAYER:
                    return [i, j]

        return None

    @staticmethod
    def is_final_state(state):
        return np.array_equal(state, Environment.final_state)

    @staticmethod
    def copy_state(state):
        new_state = []

        for i in range(len(state)):
            new_state.append([])
            for j in range(len(state[0])):
                new_state[i].append(state[i][j])

        return np.array(new_state)

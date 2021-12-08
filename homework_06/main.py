import numpy as np

from game import Environment


def main():
    learning_rate = 0.05
    discount_factor = 0.99
    # Used for Exploration VS Exploitation
    e_start = 1
    e_end = 0.1
    e_step = 0.01

    env = Environment()
    actions = env.actions

    q_table = np.random.rand(env.rows * env.columns, len(env.actions))
    print("QTable")
    print(q_table, '\n')

    state = env.initial_state

    experience = env.make_transition(state, actions[3])
    print("Moving Down\n", experience, '\n')

    experience = env.make_transition(experience.next_state, actions[2])
    print("Moving Right\n", experience, '\n')


if __name__ == '__main__':
    main()


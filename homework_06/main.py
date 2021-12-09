import random
import matplotlib.pyplot as plt
import numpy as np

from game import Environment


def main():

    # HyperParameters
    eps = 1
    eps_step = 0.8

    lr = 0.1
    df = 0.8
    episodes = 100

    # Environment
    env = Environment()
    table = np.random.rand(env.rows * env.columns, len(env.actions))

    history = []
    for ep in range(episodes):
        state = env.initial_state

        steps = 0

        while state is not None:
            # print(state)

            pos = env.player_position(state)
            ind = pos[0] * env.rows + pos[1]

            if pos == [3, 3]:
                # print('Finish')
                break

            action = np.argmax(table[ind])
            rnd = random.random()
            if rnd < eps:
                action_index = random.sample(range(len(env.actions)), 1)[0]
                action = env.actions[action_index]

            if eps > 0.01:
                eps *= eps_step

            # print(f'Action {action}\n')

            exp = env.make_transition(state, action)

            # If the next state is final
            if exp.next_state is None:
                table[ind][action] = (1 - lr) * table[ind][action] + lr * exp.reward
                state = exp.next_state
                steps = 0
                continue

            next_pos = env.player_position(exp.next_state)
            next_ind = next_pos[0] * env.rows + next_pos[1]
            best_next_state_action = np.argmax(table[next_ind])
            next_reward = table[next_ind][best_next_state_action]

            table[ind][action] = (1 - lr) * table[ind][action] + lr * (exp.reward + df * next_reward)

            state = exp.next_state

            steps += 1

        history.append(steps)

    plt.plot(history)
    plt.xlabel('Episode')
    plt.ylabel('Steps To Finish')
    plt.show()


if __name__ == '__main__':
    main()


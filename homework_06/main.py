import random
import time

import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from tensorflow.keras import models, layers
from keras import models
from tensorflow.keras import activations, losses

from game import Environment
from replay import ReplayMemory


def copy_model(model):
    model_copy = keras.models.clone_model(model)
    model_copy.build((None, 16))  # replace 10 with number of variables in input layer
    model_copy.compile(optimizer='rmsprop', loss=losses.MeanSquaredError(), metrics=['accuracy'])
    model_copy.set_weights(model.get_weights())

    return model_copy


def as_np_array(obj):
    """
    It should receve a list of objects
    """
    return np.array(obj).reshape(len(obj), 16)


def iterative_q_learning():
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
            print(state, '\n')

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


def neural_net_q_learning():
    nn = models.Sequential([
        layers.Dense(32, activation=activations.relu, input_shape=(16, )),
        layers.Dense(4, activation=activations.linear)
    ])
    # nn = models.load_model('model')

    nn.compile(optimizer='adam', loss=losses.MeanSquaredError(), metrics=['accuracy'])

    # HyperParameters
    eps = 1
    eps_step = 0.99

    lr = 0.1
    df = 0.95
    episodes = 300

    # Environment
    env = Environment()

    replay_memory = ReplayMemory(50, 100)

    itr = 3
    current_itr = 0

    # target_nn = copy_model(nn)

    for ep in range(episodes):
        print(f"Episode {ep}")
        state = env.initial_state

        steps = 0

        while state is not None:
            print(state)
            steps += 1

            if env.is_final_state(state):
                print("\nFinal State\n")
                nn.save('model')
                break

            # Get Current QValue
            _input = np.array([state]).reshape(1, 16) / 3
            outputs = nn.predict(_input)[0]
            action = np.argmax(outputs)

            # Exploration VS Exploitation
            rnd = random.random()
            if eps >= 0.01 and rnd < eps or steps >= 10:
                print("Random Move")
                action_index = random.sample(range(len(env.actions)), 1)[0]
                action = env.actions[action_index]

            if eps >= 0.01:
                eps *= eps_step

            # print(actions[action], '\n')

            # Get the next experience
            experience = env.make_transition(state, action)
            replay_memory.push(experience)

            # Training
            if replay_memory.can_sample():
                print('Training')
                experiences = replay_memory.sample()

                _inputs = []
                _actions = []
                _q_next = []

                valid_next_states = []
                valid_map = []
                rewards = []

                for j in range(len(experiences)):
                    exp = experiences[j]
                    state, action, reward, next_state = exp.split()

                    rewards.append(reward)
                    _inputs.append(state)
                    _actions.append(action)
                    _q_next.append(0)

                    if next_state is not None:
                        valid_next_states.append(next_state)
                        valid_map.append(j)

                _inputs = np.array(_inputs, dtype='float32').reshape(len(_inputs), 16) / 3
                _outputs = nn.predict(_inputs)

                _targets = np.array(_outputs, copy=True)

                _inputs_next = np.array(valid_next_states, dtype='float32').reshape(len(valid_next_states), 16) / 3
                _outputs_next = nn.predict(_inputs_next)

                for j in range(len(valid_map)):
                    ind = valid_map[j]
                    _q_next[ind] = np.argmax(_outputs_next[j])

                current_q = np.amax(_outputs, axis=1)

                for j in range(len(_targets)):
                    _targets[j][_actions[j]] = rewards[j] + _q_next[j] * df

                # print(_outputs[:2])
                # print(_targets[:2])
                nn.fit(_inputs, _targets, epochs=1, batch_size=10, verbose=0)

                current_itr += 1

            state = experience.next_state

            if state is None:
                print("Dead")

            print("\n")


def main():
    iterative_q_learning()
    # neural_net_q_learning()


if __name__ == '__main__':
    main()

import random
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


def simple_q_learning():
    # HyperParameters
    eps = 1
    eps_step = 0.8

    lr = 0.1
    df = 0.9
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


def neural_net_q_learning():
    nn = models.Sequential([
        layers.Dense(16, activation=activations.relu, input_shape=(16, )),
        layers.Dense(8, activation=activations.relu),
        layers.Dense(4, activation=activations.linear)
    ])

    nn.compile(optimizer='rmsprop', loss=losses.MeanSquaredError(), metrics=['accuracy'])

    # HyperParameters
    eps = 1
    eps_step = 0.6

    lr = 0.01
    df = 0.95
    episodes = 300

    # Environment
    env = Environment()

    replay_memory = ReplayMemory(10, 20)

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
                print("Final State")
                break

            # Get Current QValue
            outputs = nn.predict(np.array([state]).reshape(1, 16))[0]
            action = np.argmax(outputs)

            # Exploration VS Exploitation
            rnd = random.random()
            if rnd < 1:
                action_index = random.sample(range(len(env.actions)), 1)[0]
                action = env.actions[action_index]

            if eps > 0.01:
                eps *= eps_step

            print(action, '\n')

            # Get the next experience
            experience = env.make_transition(state, action)
            replay_memory.push(experience)

            # Training
            if replay_memory.can_sample():

                experiences = replay_memory.sample()

                _inputs = []
                _target = []
                _rewards = []
                _outputs = []

                mp = []
                _inputs_next = []
                _q_next = []

                for j in range(len(experiences)):
                    exp = experiences[j]
                    state, action, reward, next_state = exp.split()

                    _inputs.append(state)
                    _rewards.append(reward)

                    if next_state is not None:
                        mp.append(j)
                        _inputs_next.append(next_state)

                    _q_next.append(0)
                    # inp = as_np_array([state]) / 3
                    #
                    # output = nn.predict(inp)[0]
                    # _outputs.append(output)
                    # action = np.argmax(output)
                    #
                    # q = max(output)
                    #
                    # q_next = 0
                    # if next_state is not None:
                    #     output_next = nn.predict(as_np_array([next_state]))[0]
                    #     q_next = max(output_next)
                    #
                    # q_target = (1 - lr) * q + lr * (reward + df * q_next)
                    #
                    # target = np.array(output, copy=True)
                    # target[action] = q_target
                    #
                    # _input.append(state)
                    # _target.append(target)

                _inputs = np.array(_inputs, dtype='float32').reshape(len(_inputs), 16) / 3
                _outputs = nn.predict(_inputs)

                print(_outputs)

                _inputs_next = np.array(_inputs_next, dtype='float32').reshape(len(_inputs_next), 16) / 3
                _outputs_next = nn.predict(_inputs_next)

                _temp_q_next = np.amax(_outputs_next, 1)

                for j in range(len(mp)):
                    inx = mp[j]
                    _q_next[inx] = _temp_q_next[j]

                _rewards = np.array(_rewards, dtype='float32')
                _q_next = np.array(_q_next, dtype='float32')

                _q_current = np.amax(_outputs, 1)
                _q_target = _q_current * (1 - lr) + lr * (_rewards + np.array(_q_next) * df)

                for j in range(len(_outputs)):
                    _output = _outputs[j]
                    act = np.argmax(_output)
                    _output[act] = _q_target[j]

                _target = _outputs
                print(_target)
                # print('Input\n', _input)
                # print('Target\n', _target)
                # print('Output\n', _outputs)

                nn.fit(_inputs, _target, epochs=5, batch_size=10)

                current_itr += 1

                # if current_itr == itr:
                #     current_itr = 0
                #     target_nn = copy_model(nn)

                # for experience in experiences:
                #     state = experience.state
                #     reward = experience.reward
                #     next_state = experience.next_state
                #
                #     # Get QValue
                #     output = nn_get_output(nn, state)
                #     action = np.argmax(output[0])
                #     predicted_q = output[0][action]
                #
                #     # Get Next QValue
                #     predicted_q_next = 0
                #
                #     if next_state is not None:
                #         output_next = nn_get_output(nn, next_state)
                #         action_next = np.argmax(output_next[0])
                #         predicted_q_next = output_next[0][action_next]
                #
                #     target = (1 - lr) * predicted_q + lr * (reward + df * predicted_q_next)
                #
                #     nn_target = np.array(predictions, copy=True)
                #     nn_target[0][action] = target
                #
                #     _input.append(raw_to_nn_input([state])[0])
                #     _target.append(nn_target[0])
                #
                # nn.fit(_input, _target, epochs=5)

            state = experience.next_state


def main():
    # simple_q_learning()
    neural_net_q_learning()


if __name__ == '__main__':
    main()

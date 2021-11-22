import math

import numpy as np

from neural_network import NeuralNetwork

epsilon = 0.001


def normalize(x):
    if x == 0.0:
        return epsilon

    return x


def read_dataset(path):
    _list = []
    with open(path) as f:
        lines = f.readlines()

        for line in lines:
            _input = np.array([[normalize(float(line[0]))], [normalize(float(line[2]))]])
            _target = np.array([[float(line[4])]])
            _list.append([_input, _target])

    return _list


def main():
    dataset = read_dataset('dataset/training_data.txt')

    learning_rate = float(input('Learning Rate: '))
    epochs = int(input('Epochs: '))

    # best 0.5 lr, 500 epochs

    neural_network = NeuralNetwork([2, 2, 1], learning_rate)
    neural_network.train(dataset, epochs)


if __name__ == '__main__':
    main()

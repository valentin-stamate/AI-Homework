import math

import numpy as np


def sigmoid(x):
    return 1 / (1 + (np.exp(-x)))


def read_dataset(path):
    _list = []
    with open(path) as f:
        lines = f.readlines()

        for line in lines:
            _input = np.array([[float(line[0])], [float(line[2])]])
            _target = np.array([[float(line[4])]])
            _list.append([_input, _target])

    return _list


def main():
    dataset = read_dataset('dataset/training_data.txt')

    for ins in dataset:
        print(sigmoid(ins[0]))


if __name__ == '__main__':
    main()



import random

import numpy as np

from initializer import Initializer


class NeuralNetwork:

    def __init__(self, dimension, learning_rate):
        self.learning_rate = learning_rate
        self.brain = []
        self.biases = []

        for i in range(0, len(dimension) - 1):
            self.brain.append(Initializer.init(dimension[i + 1], dimension[i]))
            self.biases.append(Initializer.init(dimension[i + 1], 1))

    def feed_forward(self, _input):
        current_input = _input

        for layer in self.brain:
            current_input = NeuralNetwork.sigmoid(layer.dot(current_input))

        return current_input

    def feed_forward_save(self, _input):
        current_input = _input

        inputs = [current_input]

        for i in range(len(self.brain)):
            layer = self.brain[i]
            bias = self.biases[i]

            current_input = NeuralNetwork.sigmoid(layer.dot(current_input) + bias)
            inputs.append(current_input)

        return inputs

    def train(self, dataset, epochs):
        n = len(dataset)

        evolution = []

        for epoch in range(epochs):
            dataset = random.sample(dataset, n)

            # self.print_brain()

            err = 0
            for data in dataset:
                _input = data[0]
                _target = data[1]

                error = _target - self.feed_forward(_input)

                inputs = self.feed_forward_save(_input)
                errors = self.back_propagation(error)

                err += NeuralNetwork.check_output(inputs[-1], _target)

                for i in range(len(self.brain) - 1, -1, -1):
                    delta_w = self.cost_derivative(self.brain[i].shape, errors[i + 1], inputs[i + 1], inputs[i])
                    delta_b = self.cost_derivative(self.biases[i].shape, errors[i + 1], inputs[i + 1])

                    self.brain[i] -= delta_w * self.learning_rate
                    self.biases[i] -= delta_b * self.learning_rate

            evolution.append(1 - err / n)
            print('Epoch %d | Accuracy %f' % (epoch, 1 - err / n))

        return evolution

    @staticmethod
    def check_output(output, target):
        o_index = np.argmax(output)
        t_index = np.argmax(target)

        # print("Comp")
        # NeuralNetwork.print_array(output)
        # NeuralNetwork.print_array(target)

        return o_index != t_index

    def back_propagation(self, _output):
        current_output = _output

        outputs = [current_output]

        for i in range(len(self.brain) - 1, -1, -1):
            transp = self.brain[i].transpose()
            current_output = transp.dot(current_output)

            outputs.insert(0, current_output)

        return outputs

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + (np.exp(-x)))

    @staticmethod
    def cost_derivative(shape, _error, _output, _input=None):
        arr = np.zeros(shape, dtype='float32')

        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                der = (_error[i] * -1) * (_output[i] * (1 - _output[i]))

                if _input is not None:
                    der *= _input[j]

                arr[i, j] = der

        return arr

    @staticmethod
    def print_array(array):
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                print(f'{array[i, j]} ', end='')
            print("")

    def print_brain(self):
        print("---=== Brain ===---")
        print("Weights")
        for i in range(len(self.brain)):
            print(f'Layer: {i + 1}')
            NeuralNetwork.print_array(self.brain[i])
            print()

        print("\nBiases")
        for i in range(len(self.biases)):
            print(f'Layer: {i + 1}')
            NeuralNetwork.print_array(self.biases[i])
            print()

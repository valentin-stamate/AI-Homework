import random

import numpy as np

from initializer import Initializer


class NeuralNetwork:

    def __init__(self, dimension, learning_rate):
        self.learning_rate = learning_rate
        self.brain = []

        for i in range(0, len(dimension) - 1):
            self.brain.append(Initializer.init(dimension[i + 1], dimension[i]))

    def feed_forward(self, _input):
        current_input = _input

        for layer in self.brain:
            current_input = NeuralNetwork.sigmoid(layer.dot(current_input))

        return current_input

    def feed_forward_save(self, _input):
        current_input = _input

        inputs = [current_input]

        for layer in self.brain:
            current_input = NeuralNetwork.sigmoid(layer.dot(current_input))
            inputs.append(current_input)

        return inputs

    def train(self, dataset, epochs):
        n = len(dataset)

        for epoch in range(epochs):
            dataset = random.sample(dataset, n)

            err = 0
            for data in dataset:
                _input = data[0]
                _target = data[1]

                error = _target - self.feed_forward(_input)

                inputs = self.feed_forward_save(_input)
                errors = self.back_propagation(error)

                err += NeuralNetwork.check_output(inputs[-1], _target)

                for i in range(len(self.brain) - 1, -1, -1):
                    delta = self.cost_derivative(self.brain[i].shape, errors[i + 1], inputs[i], inputs[i + 1])

                    # NeuralNetwork.print_array(delta)
                    # print("")

                    self.brain[i] -= delta * self.learning_rate

            print('Epoch %d | Accuracy %f' % (epoch, 1 - err / n))

    @staticmethod
    def check_output(output, target):
        output = output[0, 0]
        target = target[0, 0]

        # print(f'{output} -- {target}')
        out = 0.0
        if output > 0.4:
            out = 1.0

        # print(f'{out} -- {target}')
        return out != target

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
    def cost_derivative(shape, _error, _input, _output):
        arr = np.zeros(shape, dtype='float32')

        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                arr[i, j] = (_error[i] * -1) * (_output[i] * (1 - _output[i])) * _input[j]

        return arr

    @staticmethod
    def print_array(array):
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                print(f'{array[i, j]} ')
            print("")

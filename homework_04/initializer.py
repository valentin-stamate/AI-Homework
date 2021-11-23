import random
import numpy as np


class Initializer:
    @staticmethod
    def init(n, m):
        arr = np.zeros((n, m), dtype='float32')

        mag = 0.1
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                arr[i, j] = mag * (random.random())

        return arr

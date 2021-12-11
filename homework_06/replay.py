import random
from game import Experience


class ReplayMemory:
    buffer: [Experience] = []

    def __init__(self, batch, capacity):
        self.batch = batch
        self.capacity = capacity
        self.length = 0

    def push(self, experience: Experience):
        if self.length < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.length % self.capacity] = experience

        self.length += 1

    def can_sample(self):
        return self.length >= self.capacity

    def sample(self):
        return random.sample(self.buffer, self.batch)

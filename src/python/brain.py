import random
import copy

class Brain:

    def __init__(self, brain_size):
        self.dna = []
        self.brain_size = brain_size
        self.brain_step = 0

    def randomize(self):
        for i in range(self.brain_size):
            # Adds a random tuple of directions: (x, y)
            self.dna.append((random.randint(-10, 10), random.randint(-10, 10)))

    def mutate(self, mutation_rate):
        for i in range(self.brain_size):
            if random.random() < mutation_rate:
                self.dna[i] = (random.randint(-10, 10), random.randint(-10, 10))
    
    def clone(self):
        clone = copy.copy(self)
        return clone
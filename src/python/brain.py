"""Brain module: stores and evolves a dot's movement DNA."""

import copy
import random


class Brain:
    """Stores a sequence of movement steps (DNA) for a dot.

    Attributes:
        dna: List of (dx, dy) direction tuples.
        brain_size: Total number of steps in the DNA sequence.
        brain_step: Index of the next step to execute.
    """

    def __init__(self, brain_size: int) -> None:
        """Initializes a Brain with an empty DNA sequence.

        Args:
            brain_size: Number of movement steps to allocate.
        """
        self.dna: list[tuple[int, int]] = []
        self.brain_size: int = brain_size
        self.brain_step: int = 0

    def randomize(self) -> None:
        """Fills the DNA sequence with random (dx, dy) step tuples."""
        for _ in range(self.brain_size):
            self.dna.append((random.randint(-10, 10), random.randint(-10, 10)))

    def mutate(self, mutation_rate: float) -> None:
        """Randomly replaces steps in the DNA sequence.

        Args:
            mutation_rate: Probability in [0, 1] that any given step is replaced.
        """
        for i in range(self.brain_size):
            if random.random() < mutation_rate:
                self.dna[i] = (random.randint(-10, 10), random.randint(-10, 10))

    def crossover(self, other: "Brain") -> "Brain":
        """Creates a child Brain via single-point crossover with another Brain.

        Picks a random cut point and splices self's DNA up to the cut with
        other's DNA from the cut onward. This is the core recombination
        operator in genetic algorithms: rather than relying on mutation alone
        to search the space, crossover lets two fit parents combine partial
        solutions. A dot that navigated the first half of a path well can
        donate those genes to a dot that handled the second half well.

        The resulting child still has brain_step=0 and must be mutated
        separately if desired.

        Args:
            other: The second parent Brain. Must have the same brain_size.

        Returns:
            A new Brain whose DNA is self.dna[:cut] + other.dna[cut:].
        """
        child = Brain(self.brain_size)
        cut = random.randint(0, self.brain_size)
        child.dna = self.dna[:cut] + other.dna[cut:]
        return child

    def clone(self) -> "Brain":
        """Returns a shallow copy of this Brain.

        Returns:
            A new Brain instance with the same dna, brain_size, and brain_step.
        """
        return copy.copy(self)

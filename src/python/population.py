"""Population module: manages dot generations and the genetic selection loop."""

import random
import time
import tkinter
from tkinter import Canvas, Tk

import dot


class Population:
    """Manages a population of dots across multiple generations.

    Only the current generation is kept in memory at any time. Previous
    generations are deleted from the canvas and garbage collected after
    each selection step.

    Attributes:
        population: Current generation of Dot instances (length == pop_size).
        tk: The root tkinter window.
        canvas: The tkinter Canvas used for rendering.
        pop_size: Number of dots per generation.
        brain_size: Number of steps in each dot's brain.
        mutation_rate: Probability that each DNA step mutates on reproduction.
        num_parents: How many top-fitness dots are eligible to breed each
            generation. With num_parents=1 (the prior default), only the
            single best dot is ever cloned — this is random local search, not
            a true genetic algorithm. Raising this to 3–5 preserves genetic
            diversity: a dot that found a detour around an obstacle may rank
            5th by raw fitness but carries the only viable path genes.
        generation: Index of the current generation (0-based).
        best_dot: Reference to the fittest Dot from the most recent generation.
        goal_reached: True once any dot has reached the goal.
        goal: Canvas item ID of the goal oval.
        gen_label: Canvas item ID of the generation counter text.
        obstacle: Canvas item ID of the obstacle rectangle.
    """

    def __init__(
        self,
        pop_tk: Tk,
        pop_size: int,
        brain_size: int,
        mutation_rate: float,
        num_parents: int = 1,
        use_crossover: bool = False,
    ) -> None:
        """Initializes the population, canvas, and static canvas elements.

        Args:
            pop_tk: The root tkinter window.
            pop_size: Number of dots per generation.
            brain_size: Number of movement steps per dot brain.
            mutation_rate: Probability in [0, 1] that a DNA step mutates.
            num_parents: Number of top-fitness dots eligible to breed.
                Must be >= 1 and <= pop_size.
            use_crossover: If True, each offspring is produced by splicing
                the DNA of two roulette-selected parents before mutating.
                Requires num_parents >= 2 to have any effect. Crossover lets
                complementary partial paths recombine: a dot that navigated
                the first half of a route well can donate those genes to one
                that handled the second half well.
        """
        self.population: list[dot.Dot] = []
        self.tk: Tk = pop_tk
        self.canvas: Canvas = Canvas(self.tk, width=600, height=600)
        self.canvas.pack()
        self.pop_size: int = pop_size
        self.brain_size: int = brain_size
        self.mutation_rate: float = mutation_rate
        self.num_parents: int = num_parents
        self.use_crossover: bool = use_crossover
        self.generation: int = 0
        self.best_dot: dot.Dot | None = None
        self.goal_reached: bool = False

        self.goal: int = self.canvas.create_oval(293, 5, 307, 19, fill="green")
        self.gen_label: int = self.canvas.create_text(
            10, 10, anchor="nw", text="Generation: 0", fill="black"
        )
        self.obstacle: int = self.canvas.create_rectangle(
            150, 200, 450, 215, fill="brown"
        )

    def _select_parent(self, parents: list[dot.Dot]) -> dot.Dot:
        """Selects a parent via fitness-proportionate (roulette wheel) selection.

        Each parent's probability of selection is proportional to its fitness,
        so fitter dots are more likely to contribute genes without completely
        monopolising reproduction. This is preferable to always picking rank-1:
        a dot that ranked 4th but found a path around an obstacle should still
        have a chance to pass on those genes.

        Falls back to random.choice if all fitnesses are zero (degenerate case).

        Args:
            parents: Candidate dots, already filtered to the top-N by fitness.

        Returns:
            One dot chosen with probability proportional to its fitness.
        """
        total = sum(d.fitness for d in parents)
        if total == 0.0:
            return random.choice(parents)
        threshold = random.uniform(0, total)
        cumulative = 0.0
        for d in parents:
            cumulative += d.fitness
            if cumulative >= threshold:
                return d
        return parents[-1]

    def make_first_pop(self) -> None:
        """Creates the initial generation of dots with randomized brains."""
        for _ in range(self.pop_size):
            self.population.append(dot.Dot(self.canvas, self.brain_size))

    def run_generation(self) -> None:
        """Runs one full generation: animates all dots and computes fitness.

        Steps each dot through its full brain sequence, then calculates fitness
        for every dot in the current generation and identifies the best performer.
        """
        self.canvas.itemconfigure(
            self.gen_label, text=f"Generation: {self.generation}"
        )
        obstacle_coords: tuple[float, float, float, float] = tuple(  # type: ignore[assignment]
            self.canvas.coords(self.obstacle)
        )

        for _ in range(self.brain_size + 1):
            for d in self.population:
                d.update(self.canvas, obstacle_coords)
            self.tk.update()
            time.sleep(0.01)

        max_fitness = -1.0
        best_index = 0
        for i, d in enumerate(self.population):
            d.calc_fitness(self.canvas, self.goal)
            if d.fitness > max_fitness:
                max_fitness = d.fitness
                best_index = i

        self.best_dot = self.population[best_index]
        self.canvas.itemconfigure(self.best_dot.obj_id, fill="purple")
        if self.best_dot.reached_goal:
            self.goal_reached = True
        self.tk.update()

    def new_population(self) -> None:
        """Replaces the current generation with a new one bred from top parents.

        Selects the top num_parents dots by fitness as the breeding pool, then
        builds the next generation:
          - Slot 0: an unmodified clone of the best dot (elitism — guarantees
            the best solution found so far is never lost).
          - Remaining slots: clones of parents chosen by fitness-proportionate
            (roulette wheel) selection, each mutated at mutation_rate.

        Old canvas items are deleted once the new generation is placed.
        """
        parents = sorted(self.population, key=lambda d: d.fitness, reverse=True)[
            : self.num_parents
        ]

        # Build new generation before deleting anything so parent canvas items
        # are still valid during clone calls.
        new_gen: list[dot.Dot] = []
        new_gen.append(parents[0].clone(self.canvas))  # elite pass-through
        for _ in range(self.pop_size - 1):
            if self.use_crossover and len(parents) >= 2:
                # Pick two parents independently; they may be the same dot,
                # which degrades gracefully to plain mutation.
                parent_a = self._select_parent(parents)
                parent_b = self._select_parent(parents)
                child_brain = parent_a.dot_brain.crossover(parent_b.dot_brain)
                child_brain.mutate(self.mutation_rate)
                child = parent_a.clone(self.canvas)
                child.dot_brain = child_brain
                new_gen.append(child)
            else:
                parent = self._select_parent(parents)
                new_gen.append(parent.clone_and_mutate(self.canvas, self.mutation_rate))

        for d in self.population:
            self.canvas.delete(d.obj_id)

        self.population = new_gen
        self.generation += 1
        self.tk.update()

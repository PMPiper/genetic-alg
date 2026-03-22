"""Population module: manages dot generations and the genetic selection loop."""

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
    ) -> None:
        """Initializes the population, canvas, and static canvas elements.

        Args:
            pop_tk: The root tkinter window.
            pop_size: Number of dots per generation.
            brain_size: Number of movement steps per dot brain.
            mutation_rate: Probability in [0, 1] that a DNA step mutates.
        """
        self.population: list[dot.Dot] = []
        self.tk: Tk = pop_tk
        self.canvas: Canvas = Canvas(self.tk, width=600, height=600)
        self.canvas.pack()
        self.pop_size: int = pop_size
        self.brain_size: int = brain_size
        self.mutation_rate: float = mutation_rate
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
        """Replaces the current generation with a new one bred from the best dot.

        Deletes all current canvas items (except the best dot, which is cloned
        first), then replaces self.population with the new generation.
        """
        # Clone the new generation before deleting anything so best_dot is
        # still valid when we call clone/clone_and_mutate.
        new_gen: list[dot.Dot] = []
        new_gen.append(self.best_dot.clone(self.canvas))
        for _ in range(self.pop_size - 1):
            new_gen.append(self.best_dot.clone_and_mutate(self.canvas, self.mutation_rate))

        # Remove old canvas items now that we no longer need them.
        for d in self.population:
            self.canvas.delete(d.obj_id)

        self.population = new_gen
        self.generation += 1
        self.tk.update()

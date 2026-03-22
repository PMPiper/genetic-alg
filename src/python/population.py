"""Population module: manages dot generations and the genetic selection loop."""

import time
import tkinter
from tkinter import Canvas, Tk

import dot


class Population:
    """Manages a population of dots across multiple generations.

    Attributes:
        population: Flat list of all Dot instances across all generations.
        tk: The root tkinter window.
        canvas: The tkinter Canvas used for rendering.
        pop_size: Number of dots per generation.
        brain_size: Number of steps in each dot's brain.
        mutation_rate: Probability that each DNA step mutates on reproduction.
        generation: Index of the current generation (0-based).
        best_dot_index: Population-list index of the fittest dot this generation.
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
        self.best_dot_index: int = -1
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
            for j in range(self.pop_size):
                pop_index = j + self.generation * self.pop_size
                self.population[pop_index].update(self.canvas, obstacle_coords)
            self.tk.update()
            time.sleep(0.01)

        max_fitness = -1.0
        for i in range(self.pop_size):
            pop_index = i + self.generation * self.pop_size
            self.population[pop_index].calc_fitness(self.canvas, self.goal)
            if self.population[pop_index].fitness > max_fitness:
                max_fitness = self.population[pop_index].fitness
                self.best_dot_index = pop_index

        self.best_dot = self.population[self.best_dot_index]
        self.canvas.itemconfigure(self.best_dot.obj_id, fill="purple")
        if self.best_dot.reached_goal:
            self.goal_reached = True
        self.tk.update()

    def new_population(self) -> None:
        """Hides the current generation and seeds the next from the best dot."""
        for i in range(self.pop_size):
            pop_index = i + self.generation * self.pop_size
            self.canvas.itemconfig(self.population[pop_index].obj_id, state="hidden")
        self.tk.update()

        for i in range(self.pop_size):
            if i == 0:
                self.population.append(self.best_dot.clone(self.canvas))
            else:
                self.population.append(
                    self.best_dot.clone_and_mutate(self.canvas, self.mutation_rate)
                )

        self.generation += 1

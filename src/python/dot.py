"""Dot module: individual agent in the genetic algorithm simulation."""

import copy
import math
import tkinter

import brain


class Dot:
    """A single dot that moves according to its brain's DNA sequence.

    Attributes:
        dead: True when the dot has run out of steps or gone out of bounds.
        reached_goal: True when the dot has overlapped the goal region.
        fitness: Fitness score calculated after a generation ends.
        obj_id: Tkinter canvas item ID for the dot oval.
        dot_brain: Brain instance controlling this dot's movement.
    """

    def __init__(self, canvas: tkinter.Canvas, brain_size: int) -> None:
        """Creates a dot at the center of the canvas with a randomized brain.

        Args:
            canvas: The tkinter Canvas to draw the dot on.
            brain_size: Number of movement steps the dot's brain will contain.
        """
        self.dead: bool = False
        self.reached_goal: bool = False
        self.fitness: float = 0.0
        self.obj_id: int = canvas.create_oval(297, 303, 303, 297, fill="black")
        self.dot_brain = brain.Brain(brain_size)
        self.dot_brain.randomize()

    def move(self, canvas: tkinter.Canvas) -> None:
        """Advances the dot one step according to its brain DNA.

        If the brain has no remaining steps, the dot is marked dead.

        Args:
            canvas: The tkinter Canvas containing the dot.
        """
        if self.dot_brain.brain_step < self.dot_brain.brain_size:
            dx, dy = self.dot_brain.dna[self.dot_brain.brain_step]
            canvas.move(self.obj_id, dx, dy)
            self.dot_brain.brain_step += 1
        else:
            canvas.itemconfigure(self.obj_id, fill="orange")
            self.dead = True

    def update(
        self,
        canvas: tkinter.Canvas,
        obstacle_coords: tuple[float, float, float, float] | None = None,
    ) -> None:
        """Moves the dot and checks boundary, obstacle, and goal collisions.

        Args:
            canvas: The tkinter Canvas containing the dot.
            obstacle_coords: Optional (x1, y1, x2, y2) bounding box of an
                obstacle. The dot dies on overlap.
        """
        if self.dead or self.reached_goal:
            return

        self.move(canvas)
        c = canvas.coords(self.obj_id)  # [x1, y1, x2, y2]

        if c[2] >= 596 or c[3] >= 596 or c[0] <= 4 or c[1] <= 4:
            self.dead = True
            canvas.itemconfigure(self.obj_id, fill="red")
        elif obstacle_coords is not None:
            ox1, oy1, ox2, oy2 = obstacle_coords
            if c[2] >= ox1 and c[0] <= ox2 and c[3] >= oy1 and c[1] <= oy2:
                self.dead = True
                canvas.itemconfigure(self.obj_id, fill="red")
        elif c[2] >= 293 and c[0] <= 307 and c[3] >= 5 and c[1] <= 19:
            self.reached_goal = True

    def distance(self, canvas: tkinter.Canvas, goal_id: int) -> float:
        """Computes the Euclidean distance from the dot's center to the goal's center.

        Args:
            canvas: The tkinter Canvas containing the dot and goal.
            goal_id: Canvas item ID of the goal oval.

        Returns:
            Euclidean distance in canvas pixels.
        """
        gx1, gy1, gx2, gy2 = canvas.coords(goal_id)
        goal_x = (gx1 + gx2) / 2
        goal_y = (gy1 + gy2) / 2
        dx1, dy1, dx2, dy2 = canvas.coords(self.obj_id)
        dot_x = (dx1 + dx2) / 2
        dot_y = (dy1 + dy2) / 2
        return math.sqrt((goal_x - dot_x) ** 2 + (goal_y - dot_y) ** 2)

    def calc_fitness(self, canvas: tkinter.Canvas, goal_id: int) -> None:
        """Computes and stores the dot's fitness score.

        Dots that reached the goal are rewarded more heavily, with a bonus
        for doing so in fewer steps.

        Args:
            canvas: The tkinter Canvas containing the dot.
            goal_id: Canvas item ID of the goal oval.
        """
        if self.reached_goal:
            self.fitness = 1.0 / 16.0 + 10000.0 / (self.dot_brain.brain_step ** 2)
        else:
            self.fitness = 1.0 / (self.distance(canvas, goal_id) ** 2)

    def clone(self, canvas: tkinter.Canvas) -> "Dot":
        """Returns a copy of this dot with reset state, placed on the canvas.

        Args:
            canvas: The tkinter Canvas to place the cloned dot on.

        Returns:
            A new Dot with identical brain DNA but reset position and state.
        """
        clone = copy.deepcopy(self)
        clone.dead = False
        clone.reached_goal = False
        clone.fitness = 0.0
        clone.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        clone.dot_brain = clone.dot_brain.clone()
        clone.dot_brain.brain_step = 0
        return clone

    def clone_and_mutate(self, canvas: tkinter.Canvas, mutation_rate: float) -> "Dot":
        """Returns a mutated clone of this dot placed on the canvas.

        Args:
            canvas: The tkinter Canvas to place the cloned dot on.
            mutation_rate: Probability in [0, 1] that each DNA step is randomized.

        Returns:
            A new Dot with mutated brain DNA and reset position and state.
        """
        clone = copy.deepcopy(self)
        clone.dead = False
        clone.reached_goal = False
        clone.fitness = 0.0
        clone.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        clone.dot_brain = clone.dot_brain.clone()
        clone.dot_brain.brain_step = 0
        clone.dot_brain.mutate(mutation_rate)
        return clone

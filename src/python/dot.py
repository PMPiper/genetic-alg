"""Dot module: individual agent in the genetic algorithm simulation."""

import copy
import math
import tkinter

import brain


class Dot:
    """A single dot that moves according to its brain's DNA sequence.

    Attributes:
        dead: True when the dot has run out of steps or gone out of bounds.
        hit_obstacle: True when the dot died specifically from an obstacle
            collision (as opposed to a wall or step exhaustion).
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
        self.hit_obstacle: bool = False
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
                obstacle. The dot dies on overlap and hit_obstacle is set.
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
                self.hit_obstacle = True
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

    def _waypoint_distance(
        self,
        canvas: tkinter.Canvas,
        goal_id: int,
        obstacle_coords: tuple[float, float, float, float],
    ) -> float:
        """Returns path length to the goal routed around a rectangular obstacle.

        Straight-line distance creates a misleading fitness gradient when an
        obstacle blocks the direct path: dots that approach the obstacle head-on
        look very fit (they're close to the goal in Euclidean terms) but have
        no viable route through it. This biases selection toward paths that are
        evolutionary dead-ends and prevents the population from discovering the
        route around the obstacle.

        This method instead measures the shorter of the two detour paths — via
        the left edge of the obstacle or via the right edge — only when the dot
        is on the far side of the obstacle from the goal. When the dot is already
        past the obstacle, it falls back to direct Euclidean distance.

        The obstacle is treated as a generic axis-aligned rectangle; no
        assumptions are made about its position or size.

        Args:
            canvas: The tkinter Canvas containing the dot and goal.
            goal_id: Canvas item ID of the goal oval.
            obstacle_coords: (x1, y1, x2, y2) bounding box of the obstacle.

        Returns:
            Estimated path distance in canvas pixels.
        """
        ox1, oy1, ox2, oy2 = obstacle_coords
        gx1, gy1, gx2, gy2 = canvas.coords(goal_id)
        goal_x = (gx1 + gx2) / 2
        goal_y = (gy1 + gy2) / 2
        dx1, dy1, dx2, dy2 = canvas.coords(self.obj_id)
        dot_x = (dx1 + dx2) / 2
        dot_y = (dy1 + dy2) / 2

        # Determine which side of the obstacle the goal is on relative to the
        # dot. If the dot and goal are on the same side, use direct distance.
        # Otherwise route via the nearer exposed corner of the obstacle.
        goal_above_obstacle = goal_y < oy1
        dot_below_obstacle = dot_y > oy2

        if goal_above_obstacle and dot_below_obstacle:
            # Must detour: measure via the top-left and top-right corners.
            d_left = (
                math.sqrt((dot_x - ox1) ** 2 + (dot_y - oy1) ** 2)
                + math.sqrt((ox1 - goal_x) ** 2 + (oy1 - goal_y) ** 2)
            )
            d_right = (
                math.sqrt((dot_x - ox2) ** 2 + (dot_y - oy1) ** 2)
                + math.sqrt((ox2 - goal_x) ** 2 + (oy1 - goal_y) ** 2)
            )
            return min(d_left, d_right)

        return math.sqrt((goal_x - dot_x) ** 2 + (goal_y - dot_y) ** 2)

    def calc_fitness(
        self,
        canvas: tkinter.Canvas,
        goal_id: int,
        fitness_mode: str = "distance",
        obstacle_coords: tuple[float, float, float, float] | None = None,
        penalize_obstacle_death: bool = False,
    ) -> None:
        """Computes and stores the dot's fitness score.

        Dots that reached the goal are rewarded more heavily, with a bonus
        for doing so in fewer steps.

        fitness_mode controls the distance heuristic used for dots that did
        not reach the goal:

          "distance" — 1 / straight_line_distance². Simple and fast, but
              creates a misleading gradient when an obstacle blocks the direct
              path. Dots approaching the obstacle head-on score well and
              dominate selection, preventing the population from finding the
              route around it.

          "waypoint" — 1 / detour_distance². Routes the measured distance
              around the obstacle when the dot is on the opposite side from
              the goal. Requires obstacle_coords. Gives a more accurate
              fitness signal that guides the population toward viable paths.

        When penalize_obstacle_death is True, dots that collided with an
        obstacle have their fitness halved after the base score is computed.

        Args:
            canvas: The tkinter Canvas containing the dot.
            goal_id: Canvas item ID of the goal oval.
            fitness_mode: "distance" or "waypoint".
            obstacle_coords: (x1, y1, x2, y2) bounding box of the obstacle,
                required when fitness_mode is "waypoint".
            penalize_obstacle_death: If True, halve the fitness of any dot
                that died by hitting an obstacle.
        """
        if self.reached_goal:
            self.fitness = 1.0 / 16.0 + 10000.0 / (self.dot_brain.brain_step ** 2)
        else:
            if fitness_mode == "waypoint" and obstacle_coords is not None:
                dist = self._waypoint_distance(canvas, goal_id, obstacle_coords)
            else:
                dist = self.distance(canvas, goal_id)
            self.fitness = 1.0 / (dist ** 2)

        if penalize_obstacle_death and self.hit_obstacle:
            self.fitness *= 0.5

    def clone(self, canvas: tkinter.Canvas) -> "Dot":
        """Returns a copy of this dot with reset state, placed on the canvas.

        Args:
            canvas: The tkinter Canvas to place the cloned dot on.

        Returns:
            A new Dot with identical brain DNA but reset position and state.
        """
        clone = copy.deepcopy(self)
        clone.dead = False
        clone.hit_obstacle = False
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
        clone.hit_obstacle = False
        clone.reached_goal = False
        clone.fitness = 0.0
        clone.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        clone.dot_brain = clone.dot_brain.clone()
        clone.dot_brain.brain_step = 0
        clone.dot_brain.mutate(mutation_rate)
        return clone

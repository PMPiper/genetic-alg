from tkinter import *
import time
import dot
import random

class Population:

    def __init__(self, pop_tk, pop_size, brain_size, mutation_rate):
        self.population = []
        self.tk = pop_tk
        self.canvas = Canvas(self.tk, width=600, height=600,)
        self.canvas.pack()
        self.pop_size = pop_size
        self.brain_size = brain_size
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.best_dot_index = -1
        self.best_dot = None

        # Create the goal dot.
        # the goal id is alway 1, which is stored by the canvas.
        self.goal = self.canvas.create_oval(293, 5, 307, 19, fill="green")

    # creates a new batch of dots for the first generation.
    def make_first_pop(self):
        for i in range(self.pop_size):
            # dots are always added to the population and canvas, never removed
            self.population.append(dot.Dot(self.canvas, self.brain_size))

    def run_generation(self):
        print("generation: {0}".format(self.generation))

        # We could do this while all not dead or reached goal and skip the dead dots, 
        # but this is simpler without worrying about performance/time complexity for now.
        # Update the dots the number of times that there are brain steps.
        # Loop over the population so the update/redraw method is only called after every 
        # dot has been moved.
        # 1 is added to the range so the brain can get past its end and be marked 
        # complete.
        for i in range(self.brain_size + 1):
            for j in range(self.pop_size):

                # The population array start its index at zero, and the canvas containing
                # the dots starts its index at 1 and a goal dot has already been created.
                # Therefore, for the same dot its index_population + 2 = canvas_index

                # this will only update dots in the current generation
                # First iteration ex: pop_size = 10, generation = 0.
                # j = 0
                # updating dot ((0 + 0*10) + 2) = 2
                # j = 1
                # updating dot ((1 + 0*10) + 2) = 3
                # ...
                # j = 9
                # updating dot ((9 + 0*10) + 2) = 11

                # Second iteration ex: pop_size = 10, generation = 1.
                # j = 0
                # updating dot ((0 + 1*10) + 2) = 12
                # j = 1
                # updating dot ((1 + 1*10) + 2) = 13
                # ...
                # j = 9
                # updating dot ((9 + 1*10) + 2) = 21
                # and so on
                print("updating dot {0}".format(int(j + self.generation * self.pop_size) + 2))
                self.population[int(j + self.generation * self.pop_size)].update(self.canvas)
            self.tk.update()
            time.sleep(.01)

        # Loop through the current generation and calulated the fitness once the generation
        # has ended
        max_fitness = -1
        for i in range(self.pop_size):
            pop_index = int(i + self.generation * self.pop_size)
            self.population[pop_index].calc_fitness(self.canvas, 1)

            # If the dot has the highest fitness, store its population index
            if self.population[pop_index].fitness > max_fitness:
                max_fitness = self.population[pop_index].fitness
                self.best_dot_index = pop_index

        # Set the best dot in the population to be cloned
        self.best_dot = self.population[self.best_dot_index]
        print("The best dot is {0}".format(self.best_dot.obj_id))
        self.canvas.itemconfigure(self.best_dot.obj_id, fill="purple")
        self.tk.update()

    def new_population(self):
        # Hide all dots from previous generation
        for i in range(self.pop_size):
            self.canvas.itemconfig(self.population[int(i + self.generation * self.pop_size)].obj_id, state="hidden")
        self.tk.update() 

        # Clone the best dot once
        # Clone and mutate the rest to fill out the batch
        for i in range(self.pop_size):
            if i == 0:
                first_clone = self.best_dot.clone(self.canvas)
                print("first_clone.obj_id: {0}".format(first_clone.obj_id))
                self.population.append(first_clone)
            else:
                self.population.append(self.best_dot.clone_and_mutate(self.canvas, self.mutation_rate))

        self.generation += 1
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

        # the goal id is alway 1
        self.goal = self.canvas.create_oval(293, 5, 307, 19, fill="green")

    def make_first_pop(self):
        # dot id = pop[dot index] + 2
        for i in range(self.pop_size):
            self.population.append(dot.Dot(self.canvas, self.brain_size))

    def run_generation(self):
        # I could do this while all not dead or reached goal, but this is easier
        for i in range(self.brain_size + 1):
            for j in range(self.pop_size):
                print("updating dot {0}".format(int(j + self.generation * self.pop_size) + 2))
                self.population[int(j + self.generation * self.pop_size)].update(self.canvas)
            self.tk.update()
            time.sleep(.01)

        #calc fitness
        max_fitness = -1
        self.best_dot_index = -1
        for i in range(self.pop_size):
            self.population[int(i + self.generation * self.pop_size)].calc_fitness(self.canvas, 1)
            if self.population[int(i + self.generation * self.pop_size)].fitness > max_fitness:
                max_fitness = self.population[int(i + self.generation * self.pop_size)].fitness
                self.best_dot_index = i

        self.best_dot = self.population[self.best_dot_index]
        self.canvas.itemconfigure(self.best_dot.obj_id, fill="purple")

    def new_population(self):
        #hide all dots from previous generation
        #clone best dot
        #clone and mutate best dot pop_size -1 times
        #print("sup")
        for i in range(self.pop_size):
            #print(int(i + self.generation * 50) + 2)
            #self.canvas.itemconfig(1 , state="hidden")
            self.canvas.itemconfig(self.population[int(i + self.generation * self.pop_size)].obj_id, state="hidden")
        self.tk.update() 

        for i in range(self.pop_size):
            if i == 0:
                self.population.append(self.best_dot.clone(self.canvas))
                print("first clone's obj_id")
                print(self.population[self.pop_size].obj_id)
            else:
                self.population.append(self.best_dot.clone_and_mutate(self.canvas, self.mutation_rate))

        self.generation += 1

        #print("best_dot.coords: {0}".format(self.canvas.coords(self.best_dot.obj_id)))
        #print("find all: ")
        #print(self.canvas.find_all())


"""
print("best_dot.obj_id: {0}".format(best_dot.obj_id))
print("best_dot_idex in pop[]: {0}".format(best_dot_index))
print("best_dot: {0}".format(best_dot))
my_clone = best_dot.clone_and_mutate(canvas, 0.01)
print("my_clone: {0}".format(my_clone))
print("my_clone.obj_id: {0}".format(my_clone.obj_id))
print("find all: ")
print(canvas.find_all())
print("best_dot.coords: {0}".format(canvas.coords(best_dot.obj_id)))
print("my_clone.coords: {0}".format(canvas.coords(my_clone.obj_id)))
#canvas.delete(best_dot.obj_id)
print("find all: ")
print(canvas.find_all())
print("best_dot.obj_id: {0}".format(best_dot.obj_id))
print("my_clone.obj_id: {0}".format(my_clone.obj_id))
print("best_dot.coords: {0}".format(canvas.coords(best_dot.obj_id)))
print("my_clone.coords: {0}".format(canvas.coords(my_clone.obj_id)))

canvas.move(my_clone.obj_id, 0, -50)
print("my_clone.coords: {0}".format(canvas.coords(my_clone.obj_id)))
tk.update()

canvas.delete(ALL)
print("find all: ")
print(canvas.find_all())
goal = canvas.create_oval(293, 5, 307, 19, fill="green")
print("find all: ")
print(canvas.find_all())
canvas.itemconfig(53, state="hidden")


tk.mainloop()
"""
from tkinter import *
import population
import time
#import dot
#import random

tk = Tk()

# Creates a population of dots.
# pop_size is the "batch" size per generation of dots.
# brain_size is the number of steps each dot takes before it dies or hits a wall.
# mutation_rate is the p(a step gets changed).
pop = population.Population(pop_tk=tk, pop_size=15, brain_size=75, mutation_rate=0.1)
pop.make_first_pop()
pop.run_generation()
time.sleep(2)

for i in range(15):
    pop.new_population()
    pop.run_generation()
    time.sleep(2)

tk.mainloop()






"""
canvas = Canvas(tk, width=600, height=600,)
canvas.pack()
brain_Size = 50
pop_size = 50

goal = canvas.create_oval(293, 5, 307, 19, fill="green")

pop = []

# these are all going to be functions of my population class
for i in range(pop_size):
    pop.append(dot.Dot(canvas, brain_Size))

# need to change this to while all not dead
for i in range(brain_Size + 1):
    for j in range(pop_size):
        pop[j].update(canvas)
    tk.update()
    time.sleep(.01)

#calc fitness
max_fitness = -1
best_dot_index = -1
for i in range(pop_size):
    pop[i].calc_fitness(canvas, goal)
    if pop[i].fitness > max_fitness:
        max_fitness = pop[i].fitness
        best_dot_index = i

best_dot = pop[best_dot_index]
canvas.itemconfigure(best_dot.obj_id, fill="purple")

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
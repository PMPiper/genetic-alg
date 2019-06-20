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

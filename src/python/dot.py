import time
import brain
import math
import copy

class Dot:

    def __init__(self, canvas, brain_size):
        self.dead = False
        self.reached_goal = False
        self.fitness = 0
        # Start at the bottom
        #self.obj_id = canvas.create_oval(297, 595, 303, 589, fill="black")
        # Start at the middle
        self.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        self.dot_brain = brain.Brain(brain_size)
        self.dot_brain.randomize()
    
    # Called by the update method
    def move(self, canvas):
        print("dot {0} brain_step: {1}; brain_size {2}".format(self.obj_id, 
                self.dot_brain.brain_step, self.dot_brain.brain_size))
        
        # At this point the dot is still alive, so we have to check to see
        # if it has any remaining steps in its brain.
        if self.dot_brain.brain_step < self.dot_brain.brain_size:
            print("I am moving dot {0}, {1}dx, {2}dy".format(self.obj_id, 
                    self.dot_brain.dna[self.dot_brain.brain_step][0],
                    self.dot_brain.dna[self.dot_brain.brain_step][1]))
            
            # Each object in the dotbrain has a tuple of directions.
            # We tell the canvas to update the dot of the cooresponding obj_id
            # and move it according to the directions at the current brain_step.
            # Increase brain_step by one for the next move call.
            canvas.move(self.obj_id, 
                        self.dot_brain.dna[self.dot_brain.brain_step][0], 
                        self.dot_brain.dna[self.dot_brain.brain_step][1])
            self.dot_brain.brain_step += 1
        else:
            print("dot {0} has no more brain steps".format(self.obj_id))
            canvas.itemconfigure(self.obj_id, fill="orange")
            self.dead = True

    # Called when the generation runs
    def update(self, canvas):
        print("I am updating dot {0}".format(self.obj_id))

        # Only update the dot if it hasn't died and hasn't reached the goal
        if not self.dead and not self.reached_goal:
            print("dot {0} is not dead and hasn't reached goal".format(self.obj_id))

            # Moves the dot based on its next brain_step
            self.move(canvas)
            
            # Checks to see if the dot is out of bounds and updates its status
            if (canvas.coords(self.obj_id)[0] >= 596 
                or canvas.coords(self.obj_id)[1] >= 596 
                or canvas.coords(self.obj_id)[0] <= 4 
                or canvas.coords(self.obj_id)[1] <= 4): 

                print("dot {0} is dead".format(self.obj_id))
                self.dead = True
                canvas.itemconfigure(self.obj_id, fill="red")
            
            # Checks to see if the dot has reached it's goal and updates its status
            elif (canvas.coords(self.obj_id)[0] >= 293 
                and canvas.coords(self.obj_id)[1] >= 5 
                and canvas.coords(self.obj_id)[0] <= 307 
                and canvas.coords(self.obj_id)[1] <= 19): 

                self.reached_goal = True
        else:
            print("dot {0} is dead or has reached goal".format(self.obj_id))

    # Canvas object coordinates have 4 defined by a rectangle the dot lies in
    def distance(self, canvas, goal_id):
        # Middle of x 
        goal_x = (canvas.coords(goal_id)[0] + canvas.coords(goal_id)[2]) / 2
        # Middle of y
        goal_y = (canvas.coords(goal_id)[1] + canvas.coords(goal_id)[3]) / 2
        dot_x = (canvas.coords(self.obj_id)[0] + canvas.coords(self.obj_id)[2]) / 2
        dot_y = (canvas.coords(self.obj_id)[1] + canvas.coords(self.obj_id)[3]) / 2
        
        # Return the Euclidean Distance
        return math.sqrt((goal_x - dot_x)**2 + (goal_y - dot_y)**2)

    # goal_id is always 1
    def calc_fitness(self, canvas, goal_id):
        if self.reached_goal:
            # Need to do some more research on this, just copied this from codebullet
            self.fitness = 1.0/16.0 + 10000.0/(self.dot_brain.brain_step**2)
        else:
            dist_to_goal = self.distance(canvas, goal_id)
            self.fitness = 1.0/(dist_to_goal**2)

    def clone(self, canvas):
        clone = copy.deepcopy(self)
        clone.dead = False
        clone.reached_goal = False
        clone.fitness = 0
        # Start at the bottom
        #clone.obj_id = canvas.create_oval(297, 595, 303, 589, fill="black")
        # Start at the middle
        clone.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        clone.dot_brain = clone.dot_brain.clone()
        clone.dot_brain.brain_step = 0
        return clone

    def clone_and_mutate(self, canvas, mutation_rate):
        clone = copy.deepcopy(self)
        clone.dead = False
        clone.reached_goal = False
        clone.fitness = 0
        # Start at the bottom
        #clone.obj_id = canvas.create_oval(297, 595, 303, 589, fill="black")
        # Start at the middle
        clone.obj_id = canvas.create_oval(297, 303, 303, 297, fill="black")
        clone.dot_brain = clone.dot_brain.clone()
        clone.dot_brain.brain_step = 0
        clone.dot_brain.mutate(mutation_rate)
        return clone
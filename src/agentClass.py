#This subclass of a base Thing class represents an Agent
'''It has one required slot (attribute), .program, which reperesents Agent Program (the Core of Agent's logic).
Agent Program should hold a function that takes one argument, the Percept, and returns an action.'''

'''!!! Note that '.program' is a slot, not a method.
If it were a method, then the program could 'cheat' and look at aspects of the agent.
It's not supposed to do that: the program can only look at the percepts'''

'''
There is an optional slot, .performance, which is a number giving
the performance measure of the agent in its environment.'''
from src.thingClass import Thing
from src.catFriendlyHouse_membersClass import Milk, Sausage, Mouse

import collections.abc #we need collections.abc which provides abstract base classes that can be used to test whether a class provides a particular interface

class Agent(Thing):

    def __init__(self, program=None):
        self.alive = True
        self.performance = 0
        self.location=None

        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

directions={
    True:'Left to Right',
    False:'Right to Left',
}

class CatAgent(Agent):
    '''Agent-Cat for the Task2: it can drink, eat and catch.
    Its performance grows by the energy of the food (energy depends on weight and calories).'''

    def __init__(self, program=None, performance=10):
        super().__init__(program)
        self.performance = performance
        self.direction = True #True: from Left to Right
        print("Agent-Cat will move {} with a performance {}".format(directions[self.direction], self.performance))

    def changeDirection(self):
        self.direction = not self.direction
        print("Agent-Cat will move {}".format(directions[self.direction]))

    def drink(self, food):
        #the Cat can drink Milk only (it can't drink an instance of Sausage)
        if isinstance(food, Milk):
            self.performance += food.energy
            print("The Cat drank the {} and got {} energy".format(food, food.energy))
            return True
        print("The Cat can't drink {}".format(food))
        return False

    def eat(self, food):
        #the Cat can eat a Sausage only (Milk is for drinking, a Mouse must be caught first)
        if isinstance(food, Sausage):
            self.performance += food.energy
            print("The Cat ate the {} and got {} energy".format(food, food.energy))
            return True
        print("The Cat can't eat {}".format(food))
        return False

    def catch(self, mouse):
        #only a strong Cat can catch a Mouse: it needs at least 10% of the Mouse's power
        if not isinstance(mouse, Mouse):
            print("The Cat can't catch {}".format(mouse))
            return False
        if self.performance < mouse.energy / 10:
            print("The Cat (performance {}) is too weak to catch the {} (power {})".format(self.performance, mouse, mouse.energy))
            return False
        self.performance += mouse.energy
        print("The Cat caught the {} and got {} energy".format(mouse, mouse.energy))
        return True


class proCatAgent(Agent):

    def __init__(self, program=None):
         super().__init__(program)
         self.performance = 30
         self.direction = True #True: from Left to Right
         print("ProAgent-Cat will move {} with a performance {}".format(directions[self.direction], self.performance))

    def changeDirection(self):
        self.direction = not self.direction
        print("ProAgent-Cat will move {}".format(directions[self.direction]))


class MouseAgent(Agent):
    def __init__(self, program=None, size=1):
        super().__init__(program)
        self.size = size
        self.performance = 5 * size
        print("Mouse Agent has a performance {}".format(self.performance))

        


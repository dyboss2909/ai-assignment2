from src.thingClass import Thing

class Food(Thing):
    '''Any food in the Cat-Friendly-House.
    weight - in grams, calories - kcal per 100 g,
    energy - kcal in this portion (the Cat's performance grows by this value)'''
    def __init__(self, weight=0, calories=0):
        self.weight = weight
        self.calories = calories
        self.energy = weight * calories // 100

    def sayHi(self):
        print("There is a {}".format(self.__class__.__name__.lower()))


class Milk(Food):
    #the Cat can only drink it
    def sayHi(self):
        print("There is a milk")

class Sausage(Food):
    #the Cat can only eat it
    def sayHi(self):
        print("There is a sausage")

class Mouse(Food):
    #the Cat has to catch it first; its energy depends on its size only
    def __init__(self, size=1):
        super().__init__()
        self.size = size
        self.energy = size * 1000

    def sayHi(self):
        print("There is a Mouse with a power {}".format(self.energy))


class Dog(Thing):
    #not a food: the Cat can only fight it (Task 3)
    def sayHi(self):
        print("There is a Dog. Woof!")

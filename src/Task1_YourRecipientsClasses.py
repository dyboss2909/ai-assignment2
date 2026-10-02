from src.thingClass import Thing

class OfficeManager(Thing):
  #a recipient who is waiting for the daily mail
  def __init__(self, name='Joe'):
    self.name = name
    print("I am {} {}".format(self.__class__.__name__, self.name))

class ITStaff(Thing):
  #a recipient who ordered donuts from Tim Hortons
  def __init__(self, name='Jack'):
    self.name = name
    print("I am {} {}".format(self.__class__.__name__, self.name))

class Student(Thing):
  #a recipient who ordered a pizza from Domino Pizza
  def __init__(self, name='Hanna'):
    self.name = name
    print("I am {} {}".format(self.__class__.__name__, self.name))

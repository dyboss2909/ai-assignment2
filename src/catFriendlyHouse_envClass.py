import random
from src.environmentProClass import environmentPro
from src.thingClass import Thing
from src.locations import *

from src.catFriendlyHouse_membersClass import Food,Milk,Sausage,Mouse,Dog

from src.agentClass import Agent, proCatAgent, MouseAgent


#catFriendlyHouse_envClass
class catFriendlyHouse_env(environmentPro):
  def __init__(self):
    super().__init__()
    self.locations=[loc_A, loc_B, loc_C]
    self.status={loc: 'Unknown' for loc in self.locations} #unknown until the Cat percepts the room

  def default_location(self, thing):
    print("The item is starting in random location...")
    return random.choice(self.locations)

  def add_thing(self, thing, location=None):
    #keep the Agent-Cat's own initial performance (the parent class resets it to 0)
    performance = getattr(thing, 'performance', None)
    super().add_thing(thing, location)
    if isinstance(thing, Agent):
      thing.performance = performance

  def percept(self, agent):
    #return a list of things that are in our agent's location
    #set the state of the room based on the kind of Food located there: 'Milk'/'Sausage'/'Mouse', a list of them or 'Empty'
    items = [type(thing).__name__ for thing in self.list_things_at(agent.location, Food)]
    if len(items)==0:
      self.status[agent.location] = 'Empty'
    elif len(items)==1:
      self.status[agent.location] = items[0]
    else:
      self.status[agent.location] = items
    return agent.location, self.status[agent.location]

  def execute_action(self, agent, action):
    #changes the state of the environment based on what the agent does.
    if self.is_agent_alive(agent):
      if action=='GoAhead':
        self.go_ahead(agent)
      elif action=='Drink':
        self.consume(agent, Milk, agent.drink)
      elif action=='Eat':
        self.consume(agent, Sausage, agent.eat)
      elif action=='Catch':
        if not self.consume(agent, Mouse, agent.catch):
          #the only case when the Mouse can survive: the Cat-Agent is weak to catch it
          for mouse in self.list_things_at(agent.location, Mouse):
            print("The {} survived and ran away from the house!".format(mouse))
            self.delete_thing(mouse)

  def consume(self, agent, foodClass, method):
    #apply the Cat's method (drink/eat/catch) to the food of the suitable type in the Cat's room
    items = self.list_things_at(agent.location, foodClass)
    if len(items)==0:
      print("There is no {} at location: {}".format(foodClass.__name__, agent.location))
      return False
    if method(items[0]):
      self.delete_thing(items[0])
      return True
    return False

  def go_ahead(self, agent):
    #1 move in the Cat's direction; at the last room it turns back (some items are not consumed yet),
    #and on the way back the first room (0,0) is the end of its hunt
    index = self.locations.index(agent.location)
    if agent.direction and index==len(self.locations)-1:
      print("The Cat reached the last room {}, but not all items are consumed".format(agent.location))
      agent.changeDirection()
    elif not agent.direction and index==0:
      print("The Cat is back in the first room {}. The hunt is over!".format(agent.location))
      agent.alive=False
      return
    agent.location = self.locations[index+1 if agent.direction else index-1]
    agent.performance -= 1
    print("The Agent decided to GoAhead to location: {}".format(agent.location))
    self.update_agent_alive(agent)

  def is_done(self):
    no_agents = not any(agent.is_alive() for agent in self.agents)
    no_items = not any(isinstance(thing, Food) for thing in self.things)
    return no_agents or no_items



  #catFriendlyHouse_envClass
class catFriendlyHouse2_env(environmentPro):
  def __init__(self):
    super().__init__()
    self.locations=[loc_A, loc_B, loc_C, loc_D]

  def default_location(self, thing):
    print("The item is starting in random location...")
    return random.choice(self.locations)

  #Return all agants exactly at a given location
  def list_agents_at(self, location, thingClass=Thing):
      return [agent for agent in self.agents if agent.location == location and isinstance(agent, thingClass)]



  def percept(self, agent):
    #return a list of things AND a list of agents that are in our agent's location
    things = self.list_things_at(agent.location)
    agents = self.list_agents_at(agent.location)
    return agent.location, things, agents


  def add_thing(self, thing, location=None): # improved
    # perf = original one not 0 like in parent class
    #from src.agentClass import Agent
    if thing in self.agents:
      print("Can't add the same agent twice")
    else:
      if isinstance(thing, Agent):
        #thing.performance = 0
        thing.location = location if location is not None else self.default_location(thing)
        self.agents.append(thing)
        print(f"Welcome! You are added in location {thing.location}")
    if thing in self.things and thing.location==location:
      print("Can't add the same agent twice")
    else:
      if not isinstance(thing, Agent):
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)

  def update_agent_alive(self, agent):
    super().update_agent_alive(agent)
    if isinstance(agent, proCatAgent) and not agent.alive:
      print("....GAME OVER!")

  def mice_left(self):
    #a Mouse is still in the house (even if it can't move anymore)
    return any(isinstance(agent, MouseAgent) for agent in self.agents)

  def move_cat(self, agent):
    #1 move in the Cat's direction; if it is the last room in this direction - change the direction automatically
    index = self.locations.index(agent.location)
    nextIndex = index+1 if agent.direction else index-1
    if not 0 <= nextIndex < len(self.locations):
      agent.changeDirection()
      nextIndex = index+1 if agent.direction else index-1
    agent.location = self.locations[nextIndex]
    agent.performance -= 5
    self.update_agent_alive(agent)

  def execute_action(self, agent, action):
    #changes the state of the environment based on what the agent does.
    if self.is_agent_alive(agent):
      #the current agent is Cat & Mouse is still there
      if isinstance(agent, proCatAgent) and self.mice_left():
        print("Some items are still there ....")
        if action=='Go ahead':
          print("The Agent decided to {} at location: {}".format(action,agent.location))
          self.move_cat(agent)


        elif action=='Catch':
          mice = self.list_agents_at(agent.location, MouseAgent)
          if len(mice)==0:
            print("Agent tried to Catch, but no MouseAgent was found at {}.".format(agent.location))
          elif agent.performance < mice[0].performance*5:
            #the Cat is weak and can't catch a Mouse, but it loses its strength
            print("The Agent is too weak to Catch {} at location: {}".format(mice[0],agent.location))
            agent.performance -= 10
            self.update_agent_alive(agent)
          else:
            print("The Agent did Catch {} at location: {}".format(mice[0],agent.location))
            agent.performance += 10
            self.delete_thing(mice[0])
            if not self.mice_left():
              print("There is nothing for Agent Cat here. Done!")
              agent.alive=False

        elif action=='Check direction':
          print("The Agent decided to {} at location: {}".format(action,agent.location))
          self.move_cat(agent)

        elif action=='Fight':
          dogs = self.list_things_at(agent.location, Dog)
          if len(dogs)==0:
            print("Agent tried to Fight, but no Dog was found at {}.".format(agent.location))
          elif agent.performance >= 10:
            #only super strong Cat can win; the beaten Dog runs away
            print("The Agent won the fight with {} at location: {}".format(dogs[0],agent.location))
            agent.performance += 20
            self.delete_thing(dogs[0])
          else:
            print("{} won the fight at location: {}. The Agent loses its strength".format(dogs[0],agent.location))
            agent.performance -= 10
            self.update_agent_alive(agent)


      elif isinstance(agent, MouseAgent):
        print("the Agent Mouse is still running with a performance {}".format(agent.performance))
        print("The Agent Mouse decided to move to {}".format(action))
        agent.location = action
        agent.performance -= 1
        self.update_agent_alive(agent)

      else:
          print("There is nothing for Agent Cat here. Done!")
          agent.alive=False


  def is_done(self):
    #GAME OVER when there is no live Cat (the Mouse can't play alone)
    no_cats = not any(agent.is_alive() for agent in self.agents if isinstance(agent, proCatAgent))
    return no_cats












# Runs the Task 1, Task 2, and Task 3 demos back-to-back in the terminal,

from src.CompanyEnvironmentClass import CompanyEnvironment
from src.Task1_YourRecipientsClasses import OfficeManager, Student, ITStaff
from src.agents import ReflexAgentA2pro

from src.catFriendlyHouse_envClass import catFriendlyHouse_env, catFriendlyHouse2_env
from src.catFriendlyHouse_membersClass import Milk, Sausage, Mouse, Dog
from src.agents import ReflexAgentA3pro, RandomMouseAgent, ReflexAgentA4pro
from src.locations import loc_A, loc_B, loc_C


def header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def task1():
    header("TASK 1 - Reflex Delivery Agent")
    ce = CompanyEnvironment()
    s = Student()
    i = ITStaff()
    o = OfficeManager()
    ce.add_thing(i)
    ce.add_thing(s)
    ce.add_thing(o)
    agent = ReflexAgentA2pro()
    ce.add_thing(agent)
    ce.run()


def task2():
    header("TASK 2 - Reflex Cat-Agent")
    e = catFriendlyHouse_env()
    e.add_thing(Mouse(size=2), loc_A)
    e.add_thing(Milk(weight=200, calories=50), loc_B)
    e.add_thing(Sausage(weight=150, calories=505), loc_C)
    cat = ReflexAgentA3pro()
    e.add_thing(cat, loc_B)
    e.run()


def task3():
    header("TASK 3 - Reflex Cat-Agent vs Random Mouse-Agent")
    e2 = catFriendlyHouse2_env()
    mouse_agent = RandomMouseAgent()
    e2.add_thing(mouse_agent)
    cat_agent = ReflexAgentA4pro()
    e2.add_thing(cat_agent)
    dog = Dog()
    e2.add_thing(dog)
    e2.run()


if __name__ == "__main__":
    task1()
    task2()
    task3()

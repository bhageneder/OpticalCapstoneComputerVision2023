import serial
from src.classes.RobotLink import RobotLink

a = RobotLink('a', None, None, None, None)
b = RobotLink('a', None, None, None, None)
c = RobotLink('a', None, None, None, None)

robot_links = [a, b, c]

robot_link = robot_links[0]

def doStuff(link):
        link.name = 'l'
        #print(robot_links[0].name)
        #print(link.name)

doStuff(robot_link)

print(robot_link.name)

#robot_links = robot_links[1:]

if robot_link not in robot_links:
        print('not in')
else:
        print('in')

print(3 * 2  +1)
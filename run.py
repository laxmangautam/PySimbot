#!/usr/bin/python3

import os, sys
import random

from pysimbotlib.App import PySimbotApp
from pysimbotlib.Robot import Robot
from kivy.core.window import Window
from kivy.logger import Logger

# Number of robot that will be run
ROBOT_NUM = 1

# Delay between update (default: 1/60 (or 60 frame per sec))
TIME_INTERVAL = 1.0/60 #10frame per second 

# Max tick
MAX_TICK = 5000

# START POINT
START_POINT = (20, 560)

# Map file
MAP_FILE = 'maps/default_map.kv'

class MyRobot(Robot):
    def __init__(self):
        super(MyRobot, self).__init__()
        self.pos = START_POINT

    def update(self):
        ''' Update method which will be called each frame
        '''
        # r = random.randint(0, 3)
        # self.move(5)
        # if(r == 1):
        #     self.turn(15)
        # elif(r == 2):
        #     self.turn(-15)
        pass

if __name__ == '__main__':
    app = PySimbotApp(MyRobot, ROBOT_NUM, mapPath=MAP_FILE, interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()




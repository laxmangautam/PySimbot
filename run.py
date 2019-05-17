#!/usr/bin/python3

import os, sys
import random

from pysimbotlib.Window import PySimbotApp
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
START_POINT = (400, 200)

class MyRobot(Robot):
    def __init__(self):
        super(MyRobot, self).__init__()
        self.pos = START_POINT
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def update(self):
        ''' Update method which will be called each frame
        '''
        r = random.randint(0, 3)
        self.move(5)
        if(r == 1):
            self.turn(15)
        elif(r == 2):
            self.turn(-15)
        pass
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.move(5)
        elif keycode[1] == 'a':
            self.turn(-5)
        elif keycode[1] == 'd':
            self.turn(5)
        elif keycode[1] == 's':
            self.move(-5)

if __name__ == '__main__':
    app = PySimbotApp(MyRobot, ROBOT_NUM, mapPath='maps/default_map.kv', interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()




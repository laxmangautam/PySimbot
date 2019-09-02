#!/usr/bin/python3
import os, sys

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.logger import Logger
from kivy.core.window import Window

import random

from . import Obstacle
from . import Objective

class PySimbotMap(Widget):
    playground = ObjectProperty(None)
    obstacles = ObjectProperty(None)
    objectives = ObjectProperty(None)
    iteration = NumericProperty(0)
    max_iter = NumericProperty(0)
    eat_count = NumericProperty(0)
    food_move_count = NumericProperty(0)
    score = NumericProperty(0)

    def __init__(self, mapPath, **kwargs):
        super(PySimbotMap, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.mapPath = mapPath
        self.robots = list()
    
    def before_update(self):
        Logger.info('Map: Iteration: {}'.format(self.iteration))
    
    def after_update(self):
        Logger.info('Map: End Iteration')

    def update(self, dt):
        if self.max_iter > 0 and self.iteration >= self.max_iter:
            return
        self.iteration += 1
        self.before_update()
        for robot in self.robots:
            robot.update()
        self.after_update()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            for r in self.robots:
                r.move(5)
        elif keycode[1] == 'a':
            for r in self.robots:
                r.turn(-5)
        elif keycode[1] == 'd':
            for r in self.robots:
                r.turn(5)
        elif keycode[1] == 's':
            for r in self.robots:
                r.move(-5)
        elif keycode[1] == 'n':
            for obj in self.objectives.get_objectives():
                self.change_objective_pos(obj)
                self.food_move_count += 1
                self.score = int(self.eat_count * 100 / self.food_move_count)

    def on_robot_eat(self, robot, obj):
        self.change_objective_pos(obj)
        self.eat_count += 1
        self.food_move_count += 1
        self.score = int(self.eat_count * 100 / self.food_move_count)

    def change_objective_pos(self, obj, pos=None):
        if pos is None:
            new_pos = Vector(random.randrange(self.playground.size[0]), random.randrange(self.playground.size[1]))
            while not self.is_obj_pos_valid(obj, new_pos):
                new_pos = Vector(random.randrange(self.playground.size[0]), random.randrange(self.playground.size[1]))
            obj.pos = new_pos
        else:        
            obj.pos = pos

    def is_obj_pos_valid(self, obj, pos):
        # check wall
        if pos.x < 10 or pos.x > self.size[0] - 210 - obj.size[0]:
            return False
        if pos.y < 10 or pos.y > self.size[1] -  10 - obj.size[1]:
            return False

        # check obstracles
        for obs in self.obstacles.get_obstacles():
            if (obs.pos[0] < pos.x < obs.pos[0] + obs.size[0] or obs.pos[0] < pos.x + obj.size[0] < obs.pos[0] + obs.size[0])\
                and (obs.pos[1] < pos.y < obs.pos[1] + obs.size[1] or obs.pos[1] < pos.y + obj.size[1] < obs.pos[1] + obs.size[1]):
                return False
        return True

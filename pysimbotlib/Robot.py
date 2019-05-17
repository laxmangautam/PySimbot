#!/usr/bin/python3

import os, sys
import math

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,\
                            ReferenceListProperty,\
                            ObjectProperty
from kivy.vector import Vector
from kivy.logger import Logger
from . import Window

DEFAULT_DISTANCE_ANGLE = list(range(0, 360, 45))

class Robot(Widget):
    # Facing 0 degree direction
    direction = NumericProperty(0)
    mycolor_r = NumericProperty(0)
    mycolor_g = NumericProperty(0)
    mycolor_b = NumericProperty(0)
    mycolor_a = NumericProperty(0)
    mycolor = ReferenceListProperty(mycolor_r, mycolor_g, mycolor_b, mycolor_a)
    _sm = ObjectProperty(None)

    @property
    def _obstacles(self):
        if self._sm and hasattr(self._sm, 'obstacles'):
            return self._sm.obstacles.get_obstacles()
        return [] 
    
    @property
    def _objectives(self):
        if self._sm and hasattr(self._sm, 'objectives'):
            return self._sm.objectives.get_objectives()
        return []
    
    def _isValidPosition(self, p):
        # Check for outside wall
        if (p[0] < self.parent.x) or (p[0] > self.parent.x + self.parent.width) or (p[1] < self.parent.y) or (p[1] > self.parent.y + self.parent.height):
            return False
        # Check obstacles
        for obs in self._obstacles:
            if (p[0] < obs.x) or\
                (p[0] > obs.x + obs.width) or\
                (p[1] < obs.y) or\
                (p[1] > obs.y + obs.height):
                continue
            return False
        return True

    def _distance(self, angle):
        rad_angle = math.radians((360-(self.direction+angle))%360)
        unit_x = math.cos(rad_angle)
        unit_y = math.sin(rad_angle)
        # Start position
        surf = Vector(self.width / 2.0 * unit_x, self.height/2.0 * unit_y) + self.center
        for i in range(0, 100):
            new_i = Vector(i * unit_x, i * unit_y) + surf
            if self._isValidPosition(new_i):
                continue
            return i
        return 100
    
    def distance(self):
        r = []
        for angle in DEFAULT_DISTANCE_ANGLE:
            r.append(self._distance(angle))
        return r
    
    def smell(self, index=0):
        if(index >= 0 and index < len(self._objectives)):
            # Get angle
            obj = self._objectives[index]
            dvx = self.center_x - obj.center_x
            dvy = self.center_y - obj.center_y
            rad = math.atan2(dvy, dvx)
            deg = ((540 - (math.degrees(rad) + self.direction))%360)
            if(deg <= 180):
                return deg
            else:
                return deg - 360
        return -1
    
    def turn(self, degree=1):
        self.direction = (self.direction + degree + 360) % 360
    
    def _isValidMove(self, next_position):
        # Check for outside wall
        if (next_position[0] < self.parent.x) or (next_position[0] + self.width > self.parent.x + self.parent.width) or (next_position[1] < self.parent.y) or (next_position[1] + self.height > self.parent.y + self.parent.height):
            return False
        # Check obstacles
        for obs in self._obstacles:
            if (next_position[0] < obs.x and next_position[0] + self.width < obs.x) or\
                (next_position[0] > obs.x + obs.width and next_position[0] + self.width > obs.x + obs.width) or\
                (next_position[1] < obs.y and next_position[1] + self.height < obs.y) or\
                (next_position[1] > obs.y + obs.height and next_position[1] + self.height > obs.y + obs.height):
                continue
            return False
        return True
    
    def _isObjective(self):
        for i, obj in enumerate(self._objectives):
            if (self.pos[0] < obj.x and self.pos[0] + self.width < obj.x) or\
                (self.pos[0] > obj.x + obj.width and self.pos[0] + self.width > obj.x + obj.width) or\
                (self.pos[1] < obj.y and self.pos[1] + self.height < obj.y) or\
                (self.pos[1] > obj.y + obj.height and self.pos[1] + self.height > obj.y + obj.height):
                continue
            return i 
        return -1

    def move(self, step=1):
        rad_angle = math.radians((360-self.direction)%360)
        new_x = step * math.cos(rad_angle)
        new_y = step * math.sin(rad_angle)
        next_position = Vector(new_x, new_y) + self.pos
        # If can move
        if self._isValidMove(next_position):
            self.pos = Vector(new_x, new_y) + self.pos
            obj_i = self._isObjective()
            if(obj_i >= 0):
                Logger.info('Robot: Eat Objective[{}]'.format(obj_i))
            return True
        return False
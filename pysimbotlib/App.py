from typing import ClassVar
from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import os
import platform
from kivy.app import App
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

from .PySimbotMap import PySimbotMap
from .Scaler import Scaler
from .Obstacle import Obstacle
from .Objective import Objective

from . import Robot

MAP_DIRECTORY = '/maps'
DEFAULT_MAP_NAME = 'default_map.kv'
DEFAULT_INTERVAL = 1.0/60.0

class PySimbotApp(App):
    title = 'PySimbot (Created by Saran(Bird) Khotsathian CPE25)'

    def __init__(self, robotCls, numRobot = 1, mapPath=os.path.join(MAP_DIRECTORY, DEFAULT_MAP_NAME), interval=DEFAULT_INTERVAL, maxtick=5000, **kwargs):
        super(PySimbotApp, self).__init__(**kwargs)
        Logger.info('Map Path: %s' % mapPath)
        self.numRobot = numRobot
        self.robotCls = robotCls
        self.mapPath = mapPath
        self.interval = interval
        self.maxtick = maxtick
        self.simbotMap = None

    def build(self):
        Window.size = (900, 600)
        
        Builder.load_file(self.mapPath)
        Builder.load_file('pysimbotlib/widget/robot.kv')
        Builder.load_file('pysimbotlib/widget/simbotmap.kv')

        self.simbotMap = PySimbotMap(self.mapPath)
        self.simbotMap.robots = []
        self.simbotMap.max_iter = self.maxtick

        obs = Obstacle()
        self.simbotMap.obstacles = obs

        obj = Objective()
        self.simbotMap.objectives = obj

        if self.simbotMap.playground:
            self.simbotMap.playground.add_widget(obs)
            self.simbotMap.playground.add_widget(obj)
        else:
            self.simbotMap.add_widget(obs)
            self.simbotMap.add_widget(obj)

        for _ in range(self.numRobot):
            r = self.robotCls()
            r._sm = self.simbotMap
            if self.simbotMap.playground:
                self.simbotMap.playground.add_widget(r)
            else:
                self.simbotMap.add_widget(r)
            self.simbotMap.robots.append(r)

        Clock.schedule_interval(self.simbotMap.update, self.interval)

        if platform.system() == 'Darwin':
            self._scaler = Scaler(size=Window.size, scale=2)
            Window.add_widget(self._scaler)
            parent = self._scaler or Window
            parent.add_widget(self.simbotMap)
        else:
            return self.simbotMap

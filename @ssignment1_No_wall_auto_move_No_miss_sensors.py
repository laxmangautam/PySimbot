#!/usr/bin/python3

import os, platform
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config

# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

# update robot every 0.5 seconds (2 frames per sec)
REFRESH_INTERVAL = 1/30

class MyRobot_Assignment1(Robot):
    sefty_distance = 20
    close_distance = 5
    hit_distance = 0
    
    def update(self):
        
       
        # Fraont Sessor = FS = IR[0], FRightS=IR[1],RIGHT Sensor = IR[2],Back Right S= IR[3] ,
        # Back Sesor = IR4 ,BLS=IR[5],RIGHT Seson = IR[6],Front left S= IR[7]
        FS,FRS,LS,BRS,BS,BLS,RS,FLS = self.distance(); 
        
        if (FS >=self.sefty_distance) and (FRS >= self.sefty_distance) and (FLS>=self.sefty_distance):
            step = int(FS/self.close_distance)
            Logger.info("1st sefty_distance condition ")
            Logger.info("Food direciton is {}".format(self.smell()))
            if(self.smell()>10):
                self.turn(10)
            elif(self.smell()<- 10):
                self.turn(-10)
            else :
                self.move_with_sefty()
       
            Logger.info("Distance: {0}".format(self.distance()))
    
        
    

    def move_with_sefty(self):
        IR_Min = min(self.distance())
        min_index = self.distance().index(IR_Min)
        if (IR_Min <= self.close_distance) and (self.close_distance ==0 or min_index ==1 or min_index == 7 ): # avoid heating obrder.
            self.turn(-180)
        self.move(5)

if __name__ == '__main__':
    app = PySimbotApp(
        robot_cls=MyRobot_Assignment1, 
        num_robots=1, 
        interval=REFRESH_INTERVAL, 
        enable_wasd_control=True
        ,map="no_Wall"
        )
    app.run()
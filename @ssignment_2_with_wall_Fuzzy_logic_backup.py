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
REFRESH_INTERVAL = 1/40

class MyRobot_Assignment1(Robot):
    sefty_distance = 25
    close_distance = 7
    hit_distance = 0
    
    def update(self):

        self.ir_values = self.distance();
        self.target= self.smell()
        rules = list();
        turns = list();
        moves = list();

        # First rules obstacles are far away
        rules.append(self.front_far() * self.left_far() * self.right_far())
        turns.append(0)
        moves.append(10)

        # 2nd rules non of the sensor is near obstacles and food is smelling from left.
        rules.append(self.smell_left() * self.front_far() * self.left_far() * self.right_far())
        turns.append(-55)
        moves.append(10)

         # 3nd rules non of the sensor is near obstacles and food is smelling from right
        rules.append(self.smell_right() * self.front_far() * self.left_far() * self.right_far())
        turns.append(55)
        moves.append(7)

         # 4rth rules Front sensor is near obstacles and rgith sesnor is far from obstacles
        rules.append(self.front_near() * self.front_right_far())
        turns.append(40)
        moves.append(2)

        # 5th rules Front sensor is near obstacles and  left sesnor is far from obstacles
        rules.append(self.front_near() * self.front_left_far())
        turns.append(-40)
        moves.append(2)

        #6th rules Front sensor is near obstacles and  left and right sesnor is far from obstacles
        rules.append(self.front_near() * self.front_right_far() * self.front_left_far() )
        turns.append(-5)
        moves.append(2)

        #7th left sensor is near from obstacles
        rules.append(self.left_near())
        turns.append(14)
        moves.append(2)

        #8th right sensor is near from obstacles
        rules.append(self.right_near())
        turns.append(-14)
        moves.append(2)
       
        # Fraont Sessor = FS = IR[0], FRightS=IR[1],RIGHT Sensor = IR[2],Back Right S= IR[3] ,
        # Back Sesor = IR4 ,BLS=IR[5],RIGHT Seson = IR[6],Front left S= IR[7]
        FS,FRS,RS,BRS,BS,BLS,LS,FLS = self.distance(); 
        
        
        if (FS >=self.sefty_distance) and (FRS >= self.sefty_distance) and (FLS>=self.sefty_distance) and\
                                            (not((LS < self.close_distance) or (RS < self.close_distance))):
            step = int(FS/self.close_distance)
           
            if(self.smell()>20):
                self.turn(20)
            elif(self.smell()<- 20):
                self.turn(-20)
            
            Logger.info("Distance: {0}".format(self.distance()))
        
        elif ((FS >=self.close_distance) and (FRS >= self.close_distance) and (FLS >= self.close_distance)):   
            step = int(FS/self.close_distance)
            
    
            if (FRS > FLS):
                self.turn(15)
            elif(FRS < FLS):
                self.turn(-15)
            
    
        elif ((FRS < self.close_distance) or (FLS < self.close_distance) or (LS < self.close_distance)or (RS < self.close_distance)):   
            step = int(FS/self.close_distance)
        
            
            if (FRS > FLS or RS > LS):
                self.turn(20)
            elif(FRS < FLS or RS < LS):
                self.turn(-20)
            

        elif (FS <= self.close_distance):
            
            self.move_with_sefty(unit=-20)
            if (FRS > FLS):
                self.turn(30)
            elif(FRS < FLS):
                self.turn(-30)
            

        self.move_with_sefty(unit=5)
        Logger.info("Distance: {0}".format(self.distance()))
        
        
    

    def move_with_sefty(self,unit= 5):
        IR_Min = min(self.distance())
        min_index = self.distance().index(IR_Min)
        if (IR_Min <= self.close_distance) and (self.close_distance ==0 or min_index ==1 or min_index == 7 ): # avoid heating obrder.
            self.turn(-180)
        self.move(unit)

    def front_far(self):
        irFraont = self.ir_values[0]
        if irFraont <=7:
            return 0.0
        elif irFraont >=75:
            return 1.0
        else:
            return (irFraont - 5.0)/70.0

    def front_near(self):
        return 1 - self.front_far()

    def left_near(self):
        return 1 - self.left_far()

    def left_far(self):
        irLeft = self.ir_values[6]
        if irLeft <=7:
            return 0.0
        elif irLeft >=55:
            return 1.0
        else:
            return (irLeft - 5.0)/50.0

    def front_left_far(self):
        irLeft = self.ir_values[7]
        if irLeft <=7:
            return 0.0
        elif irLeft >=55:
            return 1.0
        else:
            return (irLeft - 5.0)/50.0

    def front_left_near(self):
        return 1 - self.front_left_far()

    def front_right_far(self):
        irRight = self.ir_values[1]
        if irRight <=7:
            return 0.0
        elif irRight >=55:
            return 1.0
        else:
            return (irRight - 5.0)/50.0

    def front_right_near(self):
        return 1 - self.front_right_far()


    def right_far(self):
        irRight = self.ir_values[2]
        if irRight <=7:
            return 0.00
        elif irRight >=55:
            return 1.0
        else:
            return (irRight - 5.0)/50.0

    def right_near(self):
        return 1 - self.right_far()

    def smell_right(self):
        target = self.smell()
        if target >=90:
            return 1.0
        elif target <=0:
            return 0.0
        else:
            return (target/90.0)


    def smell_center(self):
        target = abs(self.smell())
        if target >=45:
            return 1.0
        elif target <=0:
            return 0.0
        else:
            return (target/45.0)

    def smell_left(self):
        target = abs(self.smell())
        if target <=-90:
            return 1.0
        elif target >=0:
            return 0.0
        else:
            return (target/90.0)

if __name__ == '__main__':
    app = PySimbotApp(
        robot_cls=MyRobot_Assignment1, 
        num_robots=1, 
        interval=REFRESH_INTERVAL, 
        enable_wasd_control=True,
         max_tick = 5000,
        #,map="no_Wall"
        )
    app.run()
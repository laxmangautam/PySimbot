#!/usr/bin/python3

import os, platform
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config

from random import seed

# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

# update robot every 0.5 seconds (2 frames per sec)
REFRESH_INTERVAL = 1/40

seed(1)

class FuzzyRobot_Assignment_2(Robot):
   
    def __init__(self) -> None:
        super(FuzzyRobot_Assignment_2,self).__init__();

    
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

        #9th left sensor is near from obstacles and front sessor is far
        rules.append(self.front_left_near() * self.front_far())
        turns.append(15)
        moves.append(2)

        #10th rright sensor is near from obstacles and front sessor is far
        rules.append(self.front_right_near() * self.front_far())
        turns.append(-15)
        moves.append(5)

        #11th lleft sensor is near from obstacles and front sessor is also near
        rules.append(self.front_left_near() * self.front_near())
        turns.append(20)
        moves.append(5)

        #12th rright sensor is near from obstacles and front sessor is also near
        rules.append(self.front_right_near() * self.front_near())
        turns.append(-20)
        moves.append(2)

        actual_turn = 0.0
        actual_move = 0.0
        for r, t, m  in zip(rules,turns,moves):
            actual_turn += t * r;
            actual_move += m * r;
        
        self.turn(actual_turn)
        self.move(actual_move)

        Logger.info("Distance: {0}".format(self.distance()))
        

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
        robot_cls=FuzzyRobot_Assignment_2, 
        num_robots=1, 
        interval=REFRESH_INTERVAL, 
        enable_wasd_control=True
        #,map="no_Wall"
        )
    app.run()
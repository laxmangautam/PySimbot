#!/usr/bin/python3

from pysimbotlib.core import PySimbotApp, Robot

from kivy.config import Config
from matplotlib import pyplot as plt1
from matplotlib import pyplot as plt2
Config.set('kivy', 'log_level', 'info')

import random
import pandas as pd
import numpy as np
#from sqlalchemy import create_engine
dataplot1 = []
dataplot2 = []

alpha = 0.5
gamma = 0.9

state_values = []
accumulated_reward = 0

max_q = list()

# generate a random multi dimensions array, value will between 0 and 1
Q = np.random.rand(2,2,2,2,2,2,2)

print('init Q -------> ',Q)
at = 0
st0 = 0
st1 = 0
st2 = 0
st3 = 0
st4 = 0
sm = 0


class RL_Robot(Robot):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.step = 0

    def track_sensor_data_table(self,FIR,LIR,RIR,LLIR,RRIR,SM):
        action0 = Q[0][st0][st1][st2][st3][st4][sm]
        action1 = Q[1][st0][st1][st2][st3][st4][sm]
        max_value = max(list([action0,action1]))
        # record
        max_q.append(max_value)

        return max_value       
   
    def update(self):
        reward = float()
        global action,numIterations
        global rt
        global at,st0,st1,st2,st3,st4,sm
        ir_values = self.distance()  # distance range [0, 100]
        target = self.smell()         # angle range [-180, 180]
        self.just_eat = False
        #print('ir_values',ir_values)
        #print('target',target)
        

        if target > 180:
            target = target-360

        
        FIR = int(self.distance()[0] < 10)
        LIR = int(self.distance()[7] < 10)
        RIR = int(self.distance()[1] < 10)
        LLIR = int(self.distance()[6] < 10)
        RRIR = int(self.distance()[2] < 10)
        
        if(target >= 0):
            SM = 0
        elif(target < 0):
            SM = 1
 
        #if random.randint(0,9) > 0:
        if(random.random() < 0.9):
            # defult
            action = 0
            # select the action have the largest q value

            if(Q[0][FIR][LIR][RIR][LLIR][RRIR][SM] > Q[1][FIR][LIR][RIR][LLIR][RRIR][SM]):
                action = 0

            if(Q[1][FIR][LIR][RIR][LLIR][RRIR][SM] > Q[0][FIR][LIR][RIR][LLIR][RRIR][SM]):
                action = 1
            
        # randomly
        else: 
            action = np.random.randint(0,2)
           

        # turn right
        if(action == 0):
            self.turn(15) #20
            self.move(10) #5
            if self.stuck :
                rt = -100
            elif self.just_eat:
                rt = 80
            elif (abs(target) < 15):
                rt = 2 
            else: 
                rt = -0.1 - (abs(target)/180)
            print('rt',rt)            
            Q[at][st0][st1][st2][st3][st4][sm] += alpha * (rt + gamma*self.track_sensor_data_table(FIR,LIR,RIR,LLIR,RRIR,SM)-Q[at][st0][st1][st2][st3][st4][sm])
            print('Q',Q[at][st0][st1][st2][st3][st4][sm])
            at = action
            st0 = FIR
            st1 = LIR
            st2 = RIR
            st3 = LLIR
            st4 = RRIR
            sm = SM

        # turn left
        elif(action == 1):
            self.turn(-15)
            self.move(10)
            if self.stuck :
                rt = -100
            elif self.just_eat:
                rt = 80
            elif (abs(target) < 15):
                rt = 2 
            else: 
                rt = -0.1 - (abs(target)/180)
            print('rt',rt)
            Q[at][st0][st1][st2][st3][st4][sm] += alpha * (rt + gamma*self.track_sensor_data_table(FIR,LIR,RIR,LLIR,RRIR,SM)-Q[at][st0][st1][st2][st3][st4][sm])
            print('Q',Q[at][st0][st1][st2][st3][st4][sm])
            at = action
            st0 = FIR
            st1 = LIR
            st2 = RIR
            st3 = LLIR
            st4 = RRIR
            sm = SM
        
        if (self.step % 1000 == 0) and (self.step > 0):
            dataplot1.append(self.eat_count/self.step)
            dataplot2.append(self.collision_count/self.step)
        self.step += 1
        pass

if __name__ == '__main__':
    app = PySimbotApp(
        robot_cls=RL_Robot, 
        simulation_forever=False,
        max_tick=300000,
        interval=1/1000.0,
        food_move_after_eat=True,
        num_robots=1
        )
    app.run()
    plt1.plot(dataplot1)
    plt1.show()
    plt2.plot(dataplot2)
    plt2.show()
    print(dataplot1)
    print(dataplot2)
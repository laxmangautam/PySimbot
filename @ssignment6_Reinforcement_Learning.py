#!/usr/bin/python3
from pysimbotlib.core import PySimbotApp, Simbot, Robot, Util
from kivy.config import Config
# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

import csv
import datetime

import random
import pandas as pd
import numpy as np

alpha = 0.5
gamma = 0.9

rt = 0
SM = 0
action = 0

state_values = []
accumulated_reward = 0

max_q = list()

# generate a random multi dimensions array, value will between 0 and 1
Q = np.random.rand(2,2,2,2,2,2,2)

#Initialize Q table by all zeros.it is 7 dimensions array
#Q = [[[[[[[random.random() for t in range(2)]for i in range(3)]for j in range(2)]for k in range(2)]for a in range(2)]for n in range(2)]for m in range(3)]
print('init Q -------> ',Q)
at = 0
st0 = 0
st1 = 0
st2 = 0
st3 = 0
st4 = 0
sm = 0


class Reinforcement_Learning_Robot(Robot):

    def track_sensor_data_table(self,FIR,LIR,RIR,LLIR,RRIR,SM):
        action0 = Q[0][st0][st1][st2][st3][st4][sm]
        action1 = Q[1][st0][st1][st2][st3][st4][sm]
        max_value = max(list([action0,action1]))
        # record
        max_q.append(max_value)

        return max_value       


    def update(self):
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
        self.record_time_eat_count()
        
    def record_time_eat_count(self):
        with open("Time_vs_eat_count.csv","a") as file:
            writer = csv.writer(file, lineterminator="\n")
            data = [self._sm.iteration, self.eat_count, self.collision_count, self._sm.score]
            print("Writing Time-Iteration - {},  Eating Count- {}, self.collision_count -{},".format(self._sm.iteration , self.eat_count, self.collision_count))
            writer = csv.writer(file)
            writer.writerow(data)   

if __name__ == '__main__':
    app = PySimbotApp(robot_cls=Reinforcement_Learning_Robot, 
                        num_robots=1,
                        num_objectives=4,
                        theme='default',
                        simulation_forever=True,
                        max_tick=500000,
                        interval=1/500.0,
                        food_move_after_eat=True,
                        save_wasd_history = True)

    app.run()
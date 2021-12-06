#!/usr/bin/python3

from pysimbotlib.core import PySimbotApp, Simbot, Robot, Util
from kivy.logger import Logger
from kivy.config import Config

from copy import deepcopy
import random
import csv
import os
import copy 

# # Force the program to show user's log only for "info" level or more. The info log will be disabled.
# Config.set('kivy', 'log_level', 'debug')
Config.set('graphics', 'maxfps', 10)

class StupidRobot(Robot):

    RULE_LENGTH = 11
    NUM_RULES = 10


    def __init__(self, **kwarg):
        super(StupidRobot, self).__init__(**kwarg)
        self.RULES = [[0] * self.RULE_LENGTH for _ in range(self.NUM_RULES)]

        # initial list of rules
        self.rules = [0.] * self.NUM_RULES
        self.turns = [0.] * self.NUM_RULES
        self.moves = [0.] * self.NUM_RULES

        self.fitness = 0
        self.lazy_count = 0
        self.headache_count = 0
        self.energy = 300
        self.just_eat = False
        self.iteration = 0

    def update(self):
        ''' Update method which will be called each frame
        '''        
        self.ir_values = self.distance()
        self.S0, self.S1, self.S2, self.S3, self.S4, self.S5, self.S6, self.S7 = self.ir_values
        self.target = self.smell_nearest()

        if self.energy < 100 :
            self.set_color(0,0,0,1)
        elif self.energy < 300 :
            self.set_color(0,255,0,1)
        elif self.energy < 500 :
            self.set_color(0,0,255,1)
        elif self.energy < 700 :
            self.set_color(255,0,255,1)
        elif self.energy < 900 :
            self.set_color(255,255,0,1)
        elif self.energy < 1200 :
            self.set_color(255,0,0,1)

        for i, RULE in enumerate(self.RULES):
            self.rules[i] = 1.0
            for k, RULE_VALUE in enumerate(RULE):
                if k < 8:
                    if RULE_VALUE % 5 == 1:
                        if k == 0: self.rules[i] *= self.S0_near()
                        elif k == 1: self.rules[i] *= self.S1_near()
                        elif k == 2: self.rules[i] *= self.S2_near()
                        elif k == 3: self.rules[i] *= self.S3_near()
                        elif k == 4: self.rules[i] *= self.S4_near()
                        elif k == 5: self.rules[i] *= self.S5_near()
                        elif k == 6: self.rules[i] *= self.S6_near()
                        elif k == 7: self.rules[i] *= self.S7_near()
                    elif RULE_VALUE % 5 == 2:
                        if k == 0: self.rules[i] *= self.S0_far()
                        elif k == 1: self.rules[i] *= self.S1_far()
                        elif k == 2: self.rules[i] *= self.S2_far()
                        elif k == 3: self.rules[i] *= self.S3_far()
                        elif k == 4: self.rules[i] *= self.S4_far()
                        elif k == 5: self.rules[i] *= self.S5_far()
                        elif k == 6: self.rules[i] *= self.S6_far()
                        elif k == 7: self.rules[i] *= self.S7_far()
                elif k == 8:
                    temp_val = RULE_VALUE % 6
                    if temp_val == 1: self.rules[i] *= self.smell_left()
                    elif temp_val == 2: self.rules[i] *= self.smell_center()
                    elif temp_val == 3: self.rules[i] *= self.smell_right()
                elif k==9: self.turns[i] = (RULE_VALUE % 91) - 45
                elif k==10: self.moves[i] = (RULE_VALUE % 9) + 2
        
        answerTurn = 0.0
        answerMove = 0.0
        for turn, move, rule in zip(self.turns, self.moves, self.rules):
            answerTurn += turn * rule
            answerMove += move * rule

        if int(answerMove) == 0 and int(answerTurn) == 0:
            self.lazy_count += 1
        
        if int(answerMove) < 0 or abs(answerTurn) > 30:
            self.headache_count += 1

        self.turn(answerTurn)
        self.move(answerMove)

        # every step the robot lost its energy
        self.energy -= 1

        # if the robot hit, it also lost energy
        if self.just_hit :
            self.energy -= 2
            pass        
        
        # if the robot eat food, it gets some energy back
        if self.just_eat :
            self.energy += 200
            pass

        if self.energy < 0 :
            # die and find a new robot
            self.iteration = 0
            print (self._sm.iteration)
            write_death(self._sm.iteration)
            
            # record that there is a dead one
            
            # generate new robot by usubg genetic operations
            temp = StupidRobot()
            temp = self.generate_new_robot()
            self.RULES = deepcopy(temp.RULES)

            # give this new born some energy
            self.energy += 300
            pass

        self.iteration += 1
        if self.iteration == 5000 :
            Logger.info("************* old die **************")
            self.energy = 0
            self.iteration = 0
            # die and find a new robot
            print (self._sm.iteration)
            write_death(self._sm.iteration)
            
            # record that there is a dead one
            
            # generate new robot by usubg genetic operations
            temp = StupidRobot()
            temp = self.generate_new_robot()
            self.RULES = deepcopy(temp.RULES)

            # give this new born some energy
            self.energy += 300
            pass

        
    def generate_new_robot(self):
        simbot = self._sm
        num_robots = len(simbot.robots)
        
        def select() -> StupidRobot:
            index = random.randrange(num_robots)
            return simbot.robots[index]
    
        select1 = select()   # design the way for selection by yourself
        select2 = select()   # design the way for selection by yourself

        while select1 == select2:
            select2 = select()

        

        temp = StupidRobot()
        crossPoint = random.randint(1,109)
        cutRule = int(crossPoint/11)
        cutPoint = int(crossPoint%11)
        
        temp.RULES[0:cutRule] = copy.deepcopy(select1.RULES[0:cutRule])
        temp.RULES[cutRule+1:] = copy.deepcopy(select2.RULES[cutRule+1:])
        temp.RULES[cutRule][:cutPoint] = copy.deepcopy(select1.RULES[cutRule][:cutPoint])
        temp.RULES[cutRule][cutPoint+1:] = copy.deepcopy(select2.RULES[cutRule][cutPoint+1:])

        

        # Doing mutation
        #     generally scan for all next_gen_robots we have created, and with very low
        #     propability, change one byte to a new random value.

        if random.randrange(15) < 5:
            # Logger.info("************* Mutation **************")
            i = random.randrange(len(temp.RULES))
            j = random.randrange(len(temp.RULES[i]))
            temp.RULES[i][j] = random.randrange(256)

        pass
        
        return temp

    def S0_near(self):
        if self.S0 <= 0: return 1.0
        elif self.S0 >= 100: return 0.0
        else: return 1 - (self.S0 / 100.0)

    def S0_far(self):
        if self.S0 <= 0: return 0.0
        elif self.S0 >= 100: return 1.0
        else: return self.S0 / 100.0
    
    def S1_near(self):
        if self.S1 <= 0: return 1.0
        elif self.S1 >= 100: return 0.0
        else: return 1 - (self.S1 / 100.0)
    
    def S1_far(self):
        if self.S1 <= 0: return 0.0
        elif self.S1 >= 100: return 1.0
        else: return self.S1 / 100.0
    
    def S2_near(self):
        if self.S2 <= 0: return 1.0
        elif self.S2 >= 100: return 0.0
        else: return 1 - (self.S2 / 100.0)
    
    def S2_far(self):
        if self.S2 <= 0: return 0.0
        elif self.S2 >= 100: return 1.0
        else: return self.S2 / 100.0
    
    def S3_near(self):
        if self.S3 <= 0: return 1.0
        elif self.S3 >= 100: return 0.0
        else: return 1 - (self.S3 / 100.0)
    
    def S3_far(self):
        if self.S3 <= 0: return 0.0
        elif self.S3 >= 100: return 1.0
        else: return self.S3 / 100.0
    
    def S4_near(self):
        if self.S4 <= 0: return 1.0
        elif self.S4 >= 100: return 0.0
        else: return 1 - (self.S4 / 100.0)
    
    def S4_far(self):
        if self.S4 <= 0: return 0.0
        elif self.S4 >= 100: return 1.0
        else: return self.S4 / 100.0
    
    def S5_near(self):
        if self.S5 <= 0: return 1.0
        elif self.S5 >= 100: return 0.0
        else: return 1 - (self.S5 / 100.0)
    
    def S5_far(self):
        if self.S5 <= 0: return 0.0
        elif self.S5 >= 100: return 1.0
        else: return self.S5 / 100.0
    
    def S6_near(self):
        if self.S6 <= 0: return 1.0
        elif self.S6 >= 100: return 0.0
        else: return 1 - (self.S6 / 100.0)
    
    def S6_far(self):
        if self.S6 <= 0: return 0.0
        elif self.S6 >= 100: return 1.0
        else: return self.S6 / 100.0
    
    def S7_near(self):
        if self.S7 <= 0: return 1.0
        elif self.S7 >= 100: return 0.0
        else: return 1 - (self.S7 / 100.0)
    
    def S7_far(self):
        if self.S7 <= 0: return 0.0
        elif self.S7 >= 100: return 1.0
        else: return self.S7 / 100.0
    
    def smell_right(self):
        if self.target >= 45: return 1.0
        elif self.target <= 0: return 0.0
        else: return self.target / 45.0
    
    def smell_left(self):
        if self.target <= -45: return 1.0
        elif self.target >= 0: return 0.0
        else: return 1-(-1*self.target)/45.0
    
    def smell_center(self):
        if self.target <= 45 and self.target >= 0: return self.target / 45.0
        if self.target <= -45 and self.target <= 0: return 1-(-1*self.target)/45.0
        else: return 0.0

def write_rule(robot, filename):
    with open(filename, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(robot.RULES)

def write_death(deathiteration):
    with open("Death-iteration.csv","a") as f:
        writer = csv.writer(f, lineterminator="\n")
        death_list = list()
        death_list.append(deathiteration)
        writer.writerow(death_list)




def before_simulation(simbot: Simbot):
    for robot in simbot.robots:
        # random RULES value for the first generation
        if simbot.simulation_count == 0:
            Logger.info("GA: initial population")
            for i, RULE in enumerate(robot.RULES):
                for k in range(len(RULE)):
                    robot.RULES[i][k] = random.randrange(256)
        
def after_simulation(simbot: Simbot):

    for robot in simbot.robots:
        robot.fitness = robot.energy

    # descending sort and rank: the best 10 will be on the list at index 0 to 9
    simbot.robots.sort(key=lambda robot: robot.fitness, reverse=True)

    write_rule(simbot.robots[0], "best_robot.csv")

if __name__ == '__main__':

    app = PySimbotApp(robot_cls=StupidRobot, 
                        num_robots=20,
                        num_objectives=4,
                        theme='default',
                        simulation_forever=False,
                        max_tick=100000,
                        interval=1/2000.0,
                        food_move_after_eat=True,
                        robot_see_each_other=True,
                        # map="no_wall",
                        customfn_before_simulation=before_simulation, 
                        customfn_after_simulation=after_simulation)
    app.run()
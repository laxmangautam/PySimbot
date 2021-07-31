# PySimbot

PySimbot is a software for simple robot simulation

## Installation

- Install Python3 (The supported version currently are [3.6-3.9](https://www.python.org/downloads/))
- If needed, you can use [virtualenv](https://virtualenv.pypa.io/en/latest/) before installing the libraries.
- To install the libraries, use the program such as cmd, powershell, or terminal. The command will be based on your OS.
- for Windows, `pip install -r requirements_windows.txt`

- for macOS, `pip3 install -r requirements_macos.txt`

- for Linux, `pip3 install -r requirements_linux.txt`

## Getting Started

- Running an example file to understand how PySimbot works. `python example1_wasd_robot.py`
- While running the example, you can see the messages in the command window. It will describe the simulation.
- The coding of the simulation is wrapped in PySimbotApp. The instance contains objects from the other classes by the following structure.

```lang-none
pysimbotlib.core.PySimbotApp
ㄴSimbot
  ㄴSimbotMap
    ㄴRobot
    ㄴObstacle
    ㄴObjective
```

- You can create your own Robot code by extends the pysimbotlib.core.Robot class. The robot class contains following properties and methods.

|     Property    |        Type       |                             Description                             |
|:---------------:|:-----------------:|:-------------------------------------------------------------------:|
| color           | Tuple[r, g, b, a] | color of the robot                                                  |
| eat_count       | int               | number of foods that robot has eaten                                |
| collision_count | int               | number of collisions that the robot made                            |
| just_eat        | bool              | flag that would be True if the robot ate food in the last iteration |
| stuck           | bool              | flag that would be True when the robot is stuck to the wall         |

|     Method                            | Return Type |                                    Description                                                      |
|:-------------------------------------:|-------------|:---------------------------------------------------------------------------------------------------:|
| update()                              | None        | update the robot state for each simbot's iteration                                                  |
| set_color(r:, g, b, a)                | None        | set the robot color in RGBA. The values are between 0 to 1. (a is optional, default to 1)           |
| turn(degree)                          | None        | turn the robot by the specifying degree (floating point number)                                     |
| move(step)                            | None        | move the robot forward by the specified step (integer number). The robot will not move if collides. |
| distance()                            | List[float] | get the 8 sensor distances in pixels from the sensors around the robot side                         |
| smell(index)                          | float       | get the turning angle to the food corresponding to the food index. (index is optional, default to 0)|
| smell_nearest()                       | float       | get the turning angle to the nearest food                                                           |

- Override the update() method to implement the robot's logic.
- Pass your robot's class as the parameter to the PySimbotApp to make a simulation.

## Advanced usages

You can configure the PySimbotApp in several ways by passing the parameters to the PySimbotApp's constructor.

- robot_cls: the robot class for initialing all robots in the simulation
- num_robots: the number of robots
- num_objectives: the number of foods
- robot_default_start_pos: the start position of the robot in (x, y) tuple format
- obj_default_start_pos: the start position of the food in (x, y) tuple format
- interval: the time interval between each frame of simulation
- max_tick: the maximum frame for a simulation
- map: the name of the map. It could be ['default', 'no_wall'] 
- theme: the name of the map's theme. It could be ['default', 'dark', 'light']
- customfn_create_robots: the custom function that returns the list of robots.
- customfn_before_simulation: the custom function that would run before each simulation. It could use for logging purpose
- customfn_after_simulation: the custom function that would run after each simulation. It could use for logging purpose
- enable_wasd_control: the boolean flag that enables the WASD robot control
- simulation_forever: the boolean flag that enables the simulation with no stop.
- food_move_after_eat: the boolean flag that enables changing position of food after the robot eat.
- save_wasd_history: the boolean flag that enables the robot logging with WASD control.
- robot_see_each_other: the boolean flag that enables the robots to measure the distance of other robots.

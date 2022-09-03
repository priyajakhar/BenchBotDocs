Look for connections for stepper motor included in the directory 'Circuit Diagrams'. PIN connections are as such:
| For 1 motor connection | For 2 motor connection |
| :---: | :---: |
| PUL = 17 | PULL = 17, PULR = 26 |
| DIR = 27 | DIRL = 27, DIRR = 13 |
| ENA = 22 | ENAL = 22, ENAR = 19 |

**Example PWM code.py**\
This file was used to develop the other codes, this was taken from the site https://www.instructables.com/Raspberry-Pi-Python-and-a-TB6600-Stepper-Motor-Dri/

**Simple Forward Motion.py**\
Use this file to simply move the stepper motor in one direction without accounting for acceleration and de-acceleration.

**Forward Motion with Acceleration.py**\
Use this file to move the stepper motor in one direction with acceleration loop but without de-acceleration.

**1Motor.py**\
Use this file to move the stepper motor in one direction with acceleration and de-acceleration loops.

**2Motors.py**\
Use this file to move 2 stepper motors in one direction with acceleration and de-acceleration loops included.

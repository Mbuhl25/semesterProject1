#Main.py

#Importing necessary libraries
import math
from machine import Pin, PWM
from steppermotor import StepperMotor
from differentialdrive import DifferentialDrive
from time import sleep
import uasyncio

# Variable to change the pwm percentage from the main file
pwm_procent=0.2
delay_val = 0.01

# Initializes the right and left motor pins, and initializes the stepper
right = StepperMotor([0,1,2,3], pwm_procent)
left = StepperMotor([4,5,6,7], pwm_procent)

stepper = DifferentialDrive(left, right)

going = True

# move functions
async def main():
    global going
    while going:
        await stepper.move_forward(10, left.half_step(), delay = delay_val)
        await uasyncio.sleep(1)
        await stepper.move_distance(5, delay = delay_val)
        await uasyncio.sleep(1)
        await stepper.turn_degree(5, left.half_step(), "right", delay = delay_val)
        await uasyncio.sleep(1)
        await stepper.turn_degree(5, left.half_step(), "left", delay = delay_val, direction = -1)
        await uasyncio.sleep(1)
        await stepper.turn_in_place(5, left.half_step(), "right", delay = delay_val)
        await uasyncio.sleep(1)
        await stepper.turn_degree_in_place(5, left.half_step(), "left", delay = delay_val, direction = 1)
        going = False

uasyncio.run(main())

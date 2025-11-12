

#Importing necessary libraries
import math
from machine import Pin, PWM
from steppermotor import StepperMotor
#from differentialdrive import DifferentialDrive
from drive import Drive
from time import sleep
from pControl import pController
from sensor import Sensor


if __name__ == "__main__":

    # Variable to change the pwm percentage from the main file
    pwm_procent=0.3
    delay_val_1 = 0.0001

    # Initializes the right and left motor pins, and initializes the stepper
    right = StepperMotor([0,1,2,3], pwm_procent)
    left = StepperMotor([4,5,6,7], pwm_procent)

    stepper = Drive(left, right)

    counter = 0

    acc_left = 0
    acc_right = 0

    pControl = pController()
    sensor1 = Sensor()
    sensorLookup = 0
    #print("calibrating min")
    #sleep(2)
    #min_sensor = sensor1.calibrate()
    #print("calibrating max")
    #sleep(5)
    #max_sensor = sensor1.calibrate()
    new_step_left, new_step_right = pControl.adjustStep(0.5, sensor1.runSensor())
    while True:
        sensorLookup+=1
        #sensorVal = int(pControl.adjustSpeed(new_step_left, new_step_right))
        if sensorLookup%10 ==0:
            new_step_left, new_step_right = pControl.adjustStep(0.5, sensor1.runSensor())
            sensorLookup = 0
         
        #new_step_left, new_step_right = 0.5, 0.5
       
        acc_left += new_step_left
        acc_right += new_step_right
        
        if acc_left >=1:
            stepper.turnLeftWheel()
            acc_left -= 1
        if acc_right >= 1:
            stepper.turnRightWheel()
            acc_right -=1
        #delay_val_1
    

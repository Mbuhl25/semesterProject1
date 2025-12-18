#importing necessary libaries
from machine import Pin, ADC, PWM
from time import sleep_us
import time
from sensor import Sensor
from pControl import pController
from stepperdrive import StepperDrive

if __name__ == "__main__":
    pwm_procent = 0.99

    stepper = StepperDrive([0,1,2,3], [4,5,6,7], pwm_procent)

    acc_left = 0
    acc_right = 0

    pControl = pController(0.5)
    sensor1 = Sensor()

    sensorTimout = 0
    sensorDelay = 
    new_step_right, new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
    
    index = 0
    turn = False
    outOfTurn = False
    whichTurn = True

    while True:
        sensorTimout += 1

        if sensorTimout > sensorDelay:
            new_step_right, new_step_left = pControl.adjustStep(
                1.0, sensor1.runSensor()
            )
            sensorTimout = 0

        # ---------- STATE LOGIC ----------
        if not turn and outOfTurn and abs(new_step_left - new_step_right) > 0.35:
            turn = True
            outOfTurn = True
            index = 0

        if turn and outOfTurn and whichTurn:
            #print("2")
            new_step_left = 1
            new_step_right = 0.75
            index += 1
            if index == 3000:
                whichTurn = False
                turn = False
                outOfTurn = False
                index = 0
        
        if turn and outOfTurn and not whichTurn:
            #print("3")
            new_step_left = 1
            new_step_right = 0.75
            index += 1
            if index == 3000:
                whichTurn = True
                turn = False
                outOfTurn = False
                index = 0
                
        if not outOfTurn:
            
            #print("1")
            index += 1
            if index == 300:
                outOfTurn = True
                turn = True
                index = 0

        # ---------- ACCUMULATOR ----------
        acc_left += new_step_left
        acc_right += new_step_right

        if acc_left >= 1:
            stepper.turnLeftWheel()
            acc_left -= 1

        if acc_right >= 1:
            stepper.turnRightWheel()
            acc_right -= 1

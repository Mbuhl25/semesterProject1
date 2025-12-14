#importing necessary libaries
from machine import Pin, ADC, PWM
from time import sleep_us
from sensor import Sensor
from pControl import pController
from stepperdrive import StepperDrive

if __name__ == "__main__":
    
    
    # Variable to change the pwm percentage from the main file
    pwm_procent=0.6

    # Initializes the right and left motor pins, and initializes the stepper
    stepper = StepperDrive([0,1,2,3],[4,5,6,7], pwm_procent)

    acc_left = 0
    acc_right = 0

    #Initialize the pController and Sensor
    pControl = pController(1.0)
    sensor1 = Sensor()

    
    #sensorTimeout 
    sensorTimout = 0
    
    new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
    sensorDelay = 100
    
    while True:
        sensorTimout+=1
        

        if sensorTimout > sensorDelay:
            new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
            sensorTimout = 0    
    
        acc_left += new_step_left
        acc_right += new_step_right
        
        
        if acc_left >=1:
            stepper.turnLeftWheel()
            acc_left -= 1
        if acc_right >= 1:
            stepper.turnRightWheel()
            acc_right -=1 
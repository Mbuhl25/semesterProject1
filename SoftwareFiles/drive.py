#drive.py

from time import sleep
import math
from machine import Pin, PWM
from steppermotor import StepperMotor

class Drive:
    def __init__(self, left, right, steps_per_revolution = 50, wheel_circumference = 26.7, wheelbase = 23.5):
        """
        Initialize the navigation system with two stepper motors.

        :param left: Instance of StepperMotor class for the left motor.
        :param right: Instance of StepperMotor class for the right motor.

        :param steps_per_revolution: how many steps for a full rotation on the stepper motor
        :type steps_per_revolution: int

        :param wheel_circumference: The circumference of the wheel in centimeters
        :type wheel_circumference: float

        :param wheelbase: The distance between the wheels in centimeters
        :type wheelbase: float
        """

        self.left = left
        self.right = right

        self.left_pins = left.initialize_pins()
        self.right_pins = right.initialize_pins()
        
        self.left_seq_index = 0
        self.right_seq_index = 0
        self.seq = left.half_step()
    
    def adjustLeftPwm(self, new_pwm):
        self.left.adjustPwm(new_pwm)
    
    def adjustRightPwm(self, new_pwm):
        self.right.adjustPwm(new_pwmSS)
        
    def stop(self, side):
        '''
        This function sets the stepper sequence on each motor to be:
        [0,0,0,0]
        '''
        if side == "left":
            self.left.stop_step(self.left_pins)
        if side == "right":
            self.right.stop_step(self.right_pins)
        

    def turnLeftWheel(self, direction = 1):

        '''
        This function moves the robot either left or right. It will only move one motor.

        :param steps: Number of steps to turn
        :type steps: Int

        :param step_sequence: The sequence of the steps.
        :type step_sequence: List, matrix

        :param turning_direction: The direction we want to turn in.
        :type turning_direction: String. Either "left" or "right"

        :param delay: The delay between each step sequence.
        :type delay: Float or int

        :param direction: The direction we want to move the motors.
        :type direction: Int. Must be either 0 or 1

        '''
        
        self.left.set_duty(self.left_pins, self.seq[self.left_seq_index])
        self.left_seq_index = (self.left_seq_index + direction) % len(self.seq)
                    
        
    def turnRightWheel(self, direction = 1):
        self.right.set_duty(self.right_pins, self.seq[self.right_seq_index])
        self.right_seq_index = (self.right_seq_index + direction) % len(self.seq)
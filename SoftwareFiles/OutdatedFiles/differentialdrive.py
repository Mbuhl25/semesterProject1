#DifferentialDrive

from time import sleep
import math
from machine import Pin, PWM
from steppermotor import StepperMotor
import uasyncio


class DifferentialDrive:
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

        self.distance_per_step = wheel_circumference/steps_per_revolution
        self.wheelbase = wheelbase

    def stop(self):
        '''
        This function sets the stepper sequence on each motor to be:
        [0,0,0,0]
        '''
        self.left.stop_step(self.left_pins)
        self.right.stop_step(self.right_pins)


    async def turn_onewheel(self, steps, step_sequence, turning_direction, delay = 0.01, direction = 1):

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

        if turning_direction == "left":
            for _ in range(steps):
                for seq in step_sequence[::direction]:
                    self.left.set_duty(self.left_pins, seq)
                    await uasyncio.sleep(delay)
                    

        elif turning_direction == "right":
            for _ in range(steps):
                for seq in step_sequence[::direction]:
                    self.right.set_duty(self.right_pins, seq)
                    await uasyncio.sleep(delay)
        else:
            raise ValueError("Direction must be 'left' or 'right'")

        self.stop()

    async def move_forward(self, steps, step_sequence, delay = 0.01, direction = 1, decay = 0):
        '''
        This function is used to move the stepper.
        It loops through the range of the steps and then uses the set_duty function to
        change the duty for each pin with the sequence as argument.

        :param steps: Number of steps.
        :type steps: int

        :param step_sequence: The sequence of the steps.
        :type step_sequence: List, matrix

        :param delay: The delay every time we take a step. Default value 0.001 seconds
        :type delay: float or int

        :param direction: Direction of the stepper. 1 for clockwise, -1 for counterclockwise
        :type direction: int

        :param decay: The decay value to decrease the delay over time.
        :type decay: float or int
        '''

        await uasyncio.gather(self.turn_onewheel(steps, step_sequence, "right", delay, direction), self.turn_onewheel(steps, step_sequence, "left", delay, direction))

    async def move_distance(self, cm, delay = 0.01, direction = 1):
        '''
        This function is used to move the stepper a given distance.
        It calculate how many steps is needed to move a given distance:
          step=cm/(cm/step)

        :param cm: The length the robot should go
        :type cm: float

        :param delay: The delay every time we take a step. Default value 0.001 seconds
        :type delay: float or int

        :param direction: Direction of the stepper. 1 for clockwise, -1 for counterclockwise
        :type direction: int
        '''
        number_of_steps=int(cm/self.distance_per_step)
        await self.move_forward(number_of_steps, self.left.half_step(), delay, direction)

    async def turn_degree(self, degree, step_sequence, turning_direction, delay = 0.01, direction = 1):
        '''
        This function moves the robot either left or right in a certain degree. It will only move one motor.
        It uses the turn function to turn the number of steps we calculate as steps_turn_degree.

        :param degree: The wanted degree to turn
        :type degree: Int or float. Must be between 0 < degree ≤ 360

        :param step_sequence: The sequence of the steps.
        :type step_sequence: List, matrix

        :param turning_direction: The direction we want to turn in.
        :type turning_direction: String. Either "left" or "right"

        :param delay: The delay between each step sequence.
        :type delay: Float or int

        :param direction: The direction we want to move the motors.
        :type direction: Int. Must be either 0 or 1

        '''

        turning_circumference = 2*math.pi*self.wheelbase
        full_turn_steps = turning_circumference/self.distance_per_step
        steps_turn_degree = abs(full_turn_steps/(360/degree))

        await self.turn_onewheel(steps_turn_degree, step_sequence, turning_direction, direction = direction, delay = delay)

    async def turn_in_place(self, steps, step_sequence, turning_direction, delay = 0.01, direction = -1):

        '''
        This function turns the robot either left or right, and rotates it in place like a tank

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

        if turning_direction == "left":
            for _ in range(steps):
                for seq in step_sequence[::direction]:
                    self.left.set_duty(self.left_pins, seq[::direction])
                    self.right.set_duty(self.right_pins, seq[::-direction]) #"[::Direction] invertes the sequence"
                    await uasyncio.sleep(delay)

        elif turning_direction == "right":
            for _ in range(steps):
                for seq in step_sequence[::direction]:
                    self.right.set_duty(self.right_pins, seq[::direction])
                    self.left.set_duty(self.left_pins, seq[::-direction]) #"[::Direction] invertes the sequence"
                    await uasyncio.sleep(delay)
        else:
            raise ValueError("Direction must be 'left' or 'right'")

        self.stop()

    async def turn_degree_in_place(self, degree, step_sequence, turning_direction, delay = 0.01, direction = -1):
        '''
        This function turns the robot either left or right in a certain degree angle, and rotates it in place like a tank
        It uses the turn_in_place function to turn the number of steps we calculate as steps_turn_degree.

        :param degree: The wanted degree to turn
        :type degree: Int or float. Must be between 0 < degree ≤ 360

        :param step_sequence: The sequence of the steps.
        :type step_sequence: List, matrix

        :param turning_direction: The direction we want to turn in.
        :type turning_direction: String. Either "left" or "right"

        :param delay: The delay between each step sequence.
        :type delay: Float or int

        :param direction: The direction we want to move the motors.
        :type direction: Int. Must be either 0 or 1

        '''

        turning_circumference = math.pi*self.wheelbase
        full_turn_steps = turning_circumference/self.distance_per_step

        #Calculate the steps to turn the given degree
        steps_turn_degree = abs(full_turn_steps/(360/degree))

        #Uses the turn_in_place function to turn the given steps.
        await self.turn_in_place(steps_turn_degree, step_sequence, turning_direction, direction = direction, delay = delay)

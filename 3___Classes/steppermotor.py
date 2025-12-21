#steppermotor
from time import sleep
import math
from machine import Pin, PWM


class StepperMotor:
    def __init__(self, pins, pwm_pct = 0.2, frequency=18_000):
        """
        Initialize a StepperMotor object.

        :param pins: List of GPIO pin numbers connected to the motor driver.
        :param pwm_pct: Percentage of the maximum PWM duty cycle.
        :param frequency: Frequency for the PWM signals.
        """
        self.pins = pins
        self.pwm_pct = pwm_pct
        self.frequency = frequency
        self.pwm_max = 65535



    def initialize_pins(self):
        '''
        This function initializes the pins for PWM.
        And adds the frequency to each pin.

        :param pins: List of GPIO pin numbers.
        :return: List of initialized PWM objects.
        '''
        initialize_pins = []
        for pin_num in self.pins:
            pwm = PWM(Pin(pin_num))
            pwm.freq(self.frequency)
            initialize_pins.append(pwm)
        return initialize_pins

    def get_duty(self):
        '''
        This function calculates the duty cycle based on the percentage.


        :return: Duty cycle as an integer.
        '''
        return int(self.pwm_max * self.pwm_pct)


    def stop_step(self, pins):
        '''
        This function is used to stop the steppermotor. The PWM is equal to zero.
        '''
        stop_sequence = [0, 0, 0, 0]
        self.set_duty(pins,stop_sequence)


    def half_step(self):
        '''
        This function creates a step sequence for the half step.
        Returns the step sequence

        '''
        duty_procentage = self.get_duty()

        step_sequence = [
            [duty_procentage,0,0,0],
            [duty_procentage,duty_procentage,0,0],
            [0,duty_procentage,0,0],
            [0,duty_procentage,duty_procentage,0],
            [0,0,duty_procentage,0],
            [0,0,duty_procentage,duty_procentage],
            [0,0,0,duty_procentage],
            [duty_procentage,0,0,duty_procentage]
        ]
        return step_sequence


    def set_duty(self, pins, sequence):
        '''
        This function loops through the pins and sets the duty to the right sequence.

        It uses the enumerate to keep track of the index

        :param pins: The PWM pin list
        :param sequence: The sequence list
        '''
        for index, pin in enumerate(pins):
            pin.duty_u16(sequence[index])
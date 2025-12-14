#stepperdrive.py onsdag 11/19
from machine import Pin, ADC, PWM

class StepperDrive:
    def __init__(self, left_pins, right_pins, pwm_pct=0.2, frequency=18000):
        # Setup basic config
        self.pwm_pct = pwm_pct
        self.frequency = frequency
        self.pwm_max = 65535
        
        # Save pins
        self.left_pins_nums = left_pins
        self.right_pins_nums = right_pins

        # Convert GPIO pins to PWM objects
        self.left_pins = self.initialize_pins(left_pins)
        self.right_pins = self.initialize_pins(right_pins)

        # Step indexes
        self.left_seq_index = 0
        self.right_seq_index = 0
        
        #Half step
        self.half_seq = self.half_step()
        
        

    def initialize_pins(self, pins):
        
        '''
        We use this function to initialize the pins
        
        :param pins: The pin list for a motor
        
        :return pwm_list: The list of pins initialized with pwm
        '''
        pwm_list = []
        for pin in pins:
            p = PWM(Pin(pin))
            p.freq(self.frequency)
            pwm_list.append(p)
        return pwm_list

    def get_duty(self):
        '''
        Uses this function to calculate the pwm with the given percentage
        
        :return: Returns the calculated pwm
        
        '''
        return int(self.pwm_max * self.pwm_pct)

    def stop_step(self, pwm_list):
        '''
        This function kills the pwm on the motor.
        '''
        stop_seq = [0, 0, 0, 0]
        self.set_duty(pwm_list, stop_seq)

    def set_duty(self, pwm_list,seq):
        '''
        We uses this function to set the duty on each pin.
        '''
        for i, pwm_pin in enumerate(pwm_list):
            pwm_pin.duty_u16(int(seq[i]))
            
    def half_step(self):
        
        '''
        The half_step sequence is created with the given pwm.
        
        
        :return seq: The sequence of the half step
        '''
        d = self.get_duty()
        seq = [
               [d,0,0,0],
               [d,d,0,0],
               [0,d,0,0],
               [0,d,d,0],
               [0,0,d,0],
               [0,0,d,d],
               [0,0,0,d],
               [d,0,0,d],
               ]
        return seq
    
    def stop(self, side):
        '''
        This function sets the stepper sequence on each motor to be:
        [0,0,0,0]
        '''
        if side == "left":
            self.left.stop_step(self.left_pins)
        if side == "right":
            self.right.stop_step(self.right_pins)

    def turnLeftWheel(self, direction=1):
        '''
        Uses this function to turn the left wheel with the given sequence.
        We only move one step of the sequence and saves the index we got to.
        '''
    
        self.set_duty(self.left_pins, self.half_seq[self.left_seq_index])
        self.left_seq_index = (self.left_seq_index + direction) % len(self.half_seq)

    def turnRightWheel(self, direction=1):
        '''
        Uses this function to turn the right wheel with the given sequence.
        We only move one step of the sequence and saves the index we got to.
        
        '''
        #sleep_us(100)
        
        self.set_duty(self.right_pins, self.half_seq[self.right_seq_index])
        self.right_seq_index = (self.right_seq_index + direction) % len(self.half_seq)


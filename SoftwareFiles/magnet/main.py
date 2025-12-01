#Class to control the magnet grapper
from time import sleep
from machine import Pin, PWM


class StepperMotor:
    def __init__(self, pins, frequency=18000):
        # Setup basic config
        self.frequency = frequency
        self.pwm_max = 65535
        
        #Save pins
        self.pins = pins

        # Convert GPIO pins to PWM objects
        self.pins_init = self.initialize_pins(pins)
        
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

    def stop_step(self, pwm_list):
        '''
        This function kills the pwm on the motor.
        '''
        stop_seq = [0, 0, 0, 0]
        self.set_duty(pwm_list, stop_seq)

    def set_duty(self, pwm_list, seq):
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
        seq = [
               [self.pwm_max,0,0,0],
               [self.pwm_max,self.pwm_max,0,0],
               [0,self.pwm_max,0,0],
               [0,self.pwm_max,self.pwm_max,0],
               [0,0,self.pwm_max,0],
               [0,0,self.pwm_max,self.pwm_max],
               [0,0,0,self.pwm_max],
               [self.pwm_max,0,0,self.pwm_max]]
        return seq
    
    def move_stepper(self,steps, direction = 1, delay = 0.001):
        for _ in range(steps):
                for seq in self.half_seq[::direction]:
                    self.set_duty(self.pins_init, seq)
                    sleep(delay)
        self.stop_step(self.pins_init)
        

if __name__ == "__main__":
    grapper = StepperMotor([8,9,10,11])
    grapper.move_stepper(500, direction = -1)
    
    
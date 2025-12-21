from machine import Pin
from time import sleep
class Mircrostepper:
    def __init__(self, pins=[12, 13, 14, 15]):
        """
        param, int_list, pins: steppe moter pins
        varibale, pin, IN1-IN4: sets the pins list to GIPO and say they are outputs
        varibale, matrix_list, step_sequence: a list of sequence the steppe coils are set to
        """
        self.IN1 = Pin(pins[0], Pin.OUT)
        self.IN2 = Pin(pins[1], Pin.OUT)
        self.IN3 = Pin(pins[2], Pin.OUT)
        self.IN4 = Pin(pins[3], Pin.OUT)
        self.step_sequence = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]

    def step_motor(self, delay, steps, direction):
        """
        funktion: moves the steppemoter
        
        param, float, delay: sets the speed on the moter
        param, int, steps: sets the lenth of the actuater
        param, int(1 or -1) direction: sets the direction of the actuater
        variable, matrix_list, seq if the direction is -1 the sequence are reversed
        
        """

        
        seq = self.step_sequence if direction == 1 else list(reversed(self.step_sequence))

        for i in range(steps):
            for pattern in seq:
                self.IN1.value(pattern[0])
                self.IN2.value(pattern[1])
                self.IN3.value(pattern[2])
                self.IN4.value(pattern[3])
                sleep(delay)

        
        self.cleanup()

    def cleanup(self):
        """
        funktion turns sets alle coils value to 0
        """
        self.IN1.value(0)
        self.IN2.value(0)
        self.IN3.value(0)
        self.IN4.value(0)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      

      
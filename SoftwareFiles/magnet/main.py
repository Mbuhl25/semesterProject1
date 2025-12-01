# Class to control the magnet grapper
from time import sleep
from machine import Pin, PWM


class Grapper:
    def __init__(self, pinsStepper, pinsServo, frequency=18000):
        # Setup basic config
        self.frequency = frequency
        self.pwm_max = 65535
        
        # --- Setup servo PWM ---
        self.servo = PWM(Pin(pinsServo))
        self.servo.freq(50)     # IMPORTANT for servos (50 Hz)

        # Servo pulse calibration
        self.servo_min = 1638   
        self.servo_max = 8192   
        
        # Initialize stepper PWM pins
        self.pinsStepper_init = self.initialize_pins(pinsStepper)
        
        # Half-step sequence
        self.half_seq = self.half_step()

    def initialize_pins(self, pins):        
        pwm_list = []
        for pin in pins:
            p = PWM(Pin(pin))
            p.freq(self.frequency)
            pwm_list.append(p)
        return pwm_list

    def stop_step(self, pwm_list):
        stop_seq = [0, 0, 0, 0]
        self.set_duty(pwm_list, stop_seq)

    def set_duty(self, pwm_list, seq):
        for i, pwm_pin in enumerate(pwm_list):
            pwm_pin.duty_u16(int(seq[i]))
            
    def half_step(self):
        return [
            [self.pwm_max,0,0,0],
            [self.pwm_max,self.pwm_max,0,0],
            [0,self.pwm_max,0,0],
            [0,self.pwm_max,self.pwm_max,0],
            [0,0,self.pwm_max,0],
            [0,0,self.pwm_max,self.pwm_max],
            [0,0,0,self.pwm_max],
            [self.pwm_max,0,0,self.pwm_max]
        ]
    
    def move_stepper(self, steps, direction=1, delay=0.001):
        for _ in range(steps):
            for seq in self.half_seq[::direction]:
                self.set_duty(self.pinsStepper_init, seq)
                sleep(delay)
        self.stop_step(self.pinsStepper_init)
    
    def set_angle(self, angle):
        # Map 0-180° to servo_min - servo_max
        duty = int(self.servo_min + (angle / 180) * (self.servo_max - self.servo_min))
        self.servo.duty_u16(duty)
        
    def servo_stop(self):
        self.servo.duty_u16(0)

if __name__ == "__main__":
    grapper = Grapper([8,9,10,11], 12)
    grapper.move_stepper(200, direction =1)
    grapper.set_angle(-20)
    sleep(1)
    grapper.servo_stop()
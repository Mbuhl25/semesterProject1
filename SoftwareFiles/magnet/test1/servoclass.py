from machine import Pin, PWM
from time import sleep

class Servo:
    def __init__(self, pin=21, frequency=50000):
        self.servo = PWM(Pin(pin))
        self.servo.freq(frequency)

    def setangle(self, angle):
        duty = int((angle / 180 * 2000) + 500)
        self.servo.duty_u16(int(duty * 65535 / 20000))

    def moveservo(self, start, end, speed, dirction):
        step = speed*dirction
        for i in range(start, end, step):
            self.setangle(i)
            sleep(0.05)
    def conmove(self, start, end, speed):
        while True:
            self.moveservo(end, start, speed, 1)
            self.moveservo(start, end, speed, -1)
            
    
    
    
    
servo1 = Servo(18)

    
servo1.moveservo(180, 0, 5, -1) 

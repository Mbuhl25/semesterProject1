from machine import ADC, Pin, SoftI2C, UART
import ssd1306
from time import sleep
import time
import utime
import math
from steppermotor import StepperMotor
from drive import Drive
import sys
# Joystick connected to:
#  - X axis → GP26 (ADC0)
#  - Y axis → GP27 (ADC1)
#  - VCC → 3.3V
#  - GND → GND

x_axis = ADC(Pin(26))  # ADC0
y_axis = ADC(Pin(27))  # ADC1
acc_left = 0
acc_right = 0

pwm_procent=0.2
delay_val_1 = 0.25
minLimitValue = 0.05
xminlimitvalue = -0.15

#kill switch
kill = Pin(15, Pin.IN, Pin.PULL_UP)
    
def check_Kill():
    if kill.value() == 0:
        print("Killed")
        sys.exit()
        
i2c = SoftI2C(scl=Pin(3), sda=Pin(2),freq=100000)
print("device",i2c.scan())
oled = ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(0)
oled.text("Friend!",0,0)
oled.show()

# Initializes the right and left motor pins, and initializes the stepper
right = StepperMotor([0,1,2,3], pwm_procent)
left = StepperMotor([4,5,6,7], pwm_procent)

stepper = Drive(left, right)

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) # TX on GPIO 1, RX on GPIO 2
led = Pin("LED", Pin.OUT)

print("Joystick test started. Move the stick!")



def init_motor(x_val, y_val):
    motor1 = 0
    motor2 = 0

    x_val=(x_val)/(65535)*2-1
    y_val=(y_val)/(65535)*2-1
    motor1 = y_val
    motor2 = y_val



    if x_val > 0:
        motor1 += abs(x_val)

    if x_val < 0:
        motor2 += abs(x_val)
    
#    if motor1 < minLimitValue:
#        motor1 = 0
#    
#    if motor2 < minLimitValue:
#        motor2 = 0
    if abs(motor1) < minLimitValue:
        motor1 = 0

    if abs(motor2) < minLimitValue:
        motor2 = 0
    
        
    return motor1, motor2
    
while True:
    check_Kill()
    
    # Read 16-bit analog values (0–65535)
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()
    
    motor1, motor2 = init_motor(x_val, y_val)
   
    acc_left += motor1
    acc_right += motor2
    
#    if xminlimitvalue < motor1 < minLimitValue:
    if motor1 == 0:
        stepper.stop(left)
#    if xminlimitvalue < motor2 < minLimitValue:
    if motor2 == 0:
        stepper.stop(right)

    if acc_left >=1:
        stepper.turnLeftWheel()
        acc_left -= 1
    if acc_right >= 1:
        stepper.turnRightWheel()
        acc_right -=1
       
    if acc_left <-1:
        stepper.turnLeftWheel(-1)
        acc_left += 1
    if acc_right <-1:
        stepper.turnRightWheel(-1)
        acc_right += 1
    print(motor1, motor2)
    message1=str(motor1)
    message2=str(motor2)
    
    message = message1 + "," + message2
    uart.write(message) # Send message to the receiver
    led.toggle()
    
    sleep(delay_val_1)

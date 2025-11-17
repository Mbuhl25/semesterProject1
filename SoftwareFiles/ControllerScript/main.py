from machine import ADC, Pin
from time import sleep
import math
from steppermotor import StepperMotor
from drive import Drive
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
delay_val_1 = 0.00005
minLimitValue = 0.05

# Initializes the right and left motor pins, and initializes the stepper
right = StepperMotor([0,1,2,3], pwm_procent)
left = StepperMotor([4,5,6,7], pwm_procent)

stepper = Drive(left, right)

print("Joystick test started. Move the stick!")



def init_motor(x_val, y_val):
    motor1 = 0
    motor2 = 0

    x_val=(x_val-16307)/(49900-16308)-0.5
    y_val=(y_val-16307)/(49900-16308)-0.5
    motor1 = y_val
    motor2 = y_val

    if x_val > 0:
        motor1 += abs(x_val)

    if x_val < 0:
        motor2 += abs(x_val)
    
    if motor1 < minLimitValue:
        motor1 = 0
    
    if motor2 < minLimitValue:
        motor2 = 0
    
    return motor1, motor2
    
while True:
    # Read 16-bit analog values (0–65535)
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()
    
    motor1, motor2 = init_motor(x_val, y_val)
   
    acc_left += motor1
    acc_right += motor2
    
    if motor1 < minLimitValue:
        stepper.stop(left)
        print("motor left stopped")
        sleep(0.5)
    if motor2 < minLimitValue:
        stepper.stop("right")
        print("motor right stopped")
        sleep(0.5)
    
    if acc_left >=1:
        stepper.turnLeftWheel()
        acc_left -= 1
    if acc_right >= 1:
        stepper.turnRightWheel()
        acc_right -=1
    
    sleep(delay_val_1)


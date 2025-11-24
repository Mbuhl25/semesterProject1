from machine import ADC, Pin, SoftI2C, UART
import ssd1306
from time import sleep_us
import sys
# Joystick connected to:
#  - X axis → GP26 (ADC0)
#  - Y axis → GP27 (ADC1)
#  - VCC → 3.3V
#  - GND → GND

x_axis = ADC(Pin(26))  # ADC0
y_axis = ADC(Pin(27))  # ADC1

delay_val_1 = 250000
minLimitValue = 0.05
xminlimitvalue = -0.15

#kill switch
kill = Pin(15, Pin.IN, Pin.PULL_UP)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) # TX on GPIO 1, RX on GPIO 2


# oled skærm initializing
i2c = SoftI2C(scl=Pin(3), sda=Pin(2),freq=100000)
print("device",i2c.scan())
oled = ssd1306.SSD1306_I2C(128,64,i2c)
oled.fill(0)
oled.text("Friend!",0,0)
oled.show()

def check_Kill():
    if kill.value() == 0:
        print("Killed")
        sys.exit()

def Get_Motor_Values(x_val, y_val):
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
    
    if abs(motor1) < minLimitValue:
        motor1 = 0

    if abs(motor2) < minLimitValue:
        motor2 = 0
    
    return motor1, motor2
    
print("Joystick test started. Move the stick!")

while True:
    check_Kill()
    
    # Read 16-bit analog values (0–65535)
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()
    
    motor1, motor2 = Get_Motor_Values(x_val, y_val)
    
    message1=str(motor1)
    message2=str(motor2)
    
    message = message1 + "," + message2
    uart.write(message) # Send message to the receiver

    sleep_us(delay_val_1)

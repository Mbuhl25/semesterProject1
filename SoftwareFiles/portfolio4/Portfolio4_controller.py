from machine import ADC, Pin, SoftI2C, UART
from time import sleep_us
import ssd1306

#Variables for the script
delay_val_1 = 50000
minLimitValue = 0.05

# Joystick connected to:
#  - X axis → GP26 (ADC0)
#  - Y axis → GP27 (ADC1)
#  - VCC → 3.3V
#  - GND → GND
x_axis = ADC(Pin(26))  # ADC0
y_axis = ADC(Pin(27))  # ADC1

# For the Kill switch

kill_triggered = False
def Kill_Handler(pin):
    global kill_triggered
    kill_triggered = True
    print("Killed")
    
kill_switch = Pin(19, Pin.IN, Pin.PULL_UP)
kill_switch.irq(trigger=Pin.IRQ_FALLING, handler=Kill_Handler)

#Initialize the 2 Uart pins
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) # TX on GPIO 1, RX on GPIO 2


# initialize oled skærm 
i2c = SoftI2C(scl=Pin(3), sda=Pin(2),freq=100000)
print("device has number",i2c.scan())
oled = ssd1306.SSD1306_I2C(128,64,i2c)


def Get_Motor_Values(x_val, y_val):
    motor_left = round(2*(x_val/65535)-1,  2)
    motor_right = round(2*(y_val/65535)-1,  2)

    if abs(motor_left) < minLimitValue:
        motor_left = 0
    if abs(motor_right) < minLimitValue:
        motor_right = 0
    
    return motor_left*0.5, motor_right*0.5
    
print("Joystick test started. Move the stick!")

while True:
    if kill_triggered:
        uart.write("0") # Send message to the receiver
        break
        
    # Read 16-bit analog values (0–65535)
    x_val = x_axis.read_u16()
    y_val = y_axis.read_u16()
    
    motor_right, motor_left = Get_Motor_Values(x_val, y_val)

    motor_right=str(motor_right)
    motor_left=str(motor_left)
    
    oled.fill(0)
    oled.text("right: " + motor_right,0,24)
    oled.text("left:  " + motor_left,0,48)
    oled.show()
    
    uart.write(motor_right + "," + motor_left) # Send message to the receiver

    sleep_us(delay_val_1)
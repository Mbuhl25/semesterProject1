#importing necessary libaries
from machine import Pin, ADC, PWM, UART
from time import sleep_us
from stepperdrive import StepperDrive

if __name__ == "__main__":
    # Variable to change the pwm percentage from the main file
    pwm_procent=0.3

    # Initializes the right and left motor pins, and initializes the stepper
    stepper = StepperDrive([0,1,2,3],[4,5,6,7], pwm_procent)

    acc_left = 0
    acc_right = 0
    new_step_left = 0
    new_step_right = 0
    
    uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13)) # TX on GPIO 1, RX on GPIO 2
    
    while True:
        if uart.any(): # Check if data is available to read
            data = uart.read() # Read the incoming data
            if data:
                if data.decode('utf-8') == "0":
                    print(data.decode('utf-8'))
                    stepper.stop("left")
                    stepper.stop("right")
                    print("Killed")
                    break
                
                parts = data.decode('utf-8').split(",")
                new_step_left=float(parts[1])
                new_step_right=float(parts[0])
                print(parts)
                
        
        acc_left += new_step_left
        acc_right += new_step_right
        
        # if xminlimitvalue < motor1 < minLimitValue:
        if new_step_left == 0:
            stepper.stop("left")
        # if xminlimitvalue < motor2 < minLimitValue:
        if new_step_right == 0:
            stepper.stop("right")
        
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
        
        sleep_us(100)
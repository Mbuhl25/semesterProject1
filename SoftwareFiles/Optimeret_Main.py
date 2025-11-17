#Optimeret main

#Sensor
from machine import Pin, ADC, PWM
from time import sleep

class Sensor():
    def __init__(self, z0 = 8, z1 = 9, z2 = 10, a0 = 28):
        self.z0 = Pin(z0, Pin.OUT)
        self.z1 = Pin(z1,Pin.OUT)
        self.z2 = Pin(z2, Pin.OUT)
        self.adc_input = ADC(Pin(a0))
        self.sensor = [(0,0,0),
                       (0,0,1),
                       (1,0,0),
                       (0,1,0),
                       (1,1,0),
                       (1,1,1)]
 
    def readAdc(self):
        '''
        This function is used to measure the adc value
        
        :return adcValue: The adc value over self.adc_input
        '''
        adcValue = self.adc_input.read_u16()
        return adcValue
        
    def zSetValue(self,row):
        '''
        This function is used to set the z values.
        It will allow the multiplexer to change wich input we are measuring over with our adc
        
        :param row: The row of the sequence we want to use
        :type row: Int
        '''
        self.z0.value(self.sensor[row][0]), self.z1.value(self.sensor[row][1]), self.z2.value(self.sensor[row][2])

    
    def runSensor(self):
        current_adc = []
        for number_Z_List in range(len(self.sensor)):
            self.zSetValue(number_Z_List)
            adc_value = self.readAdc()
            current_adc.append(adc_value)
        return current_adc


class pController():
    def __init__(self, kp = 0.8):
        self.positions = [-3, -2, -1, 1, 2, 3]
        self.weights = [1, 1, 1, 1, 1, 1]
        self.kp = kp
    
    def weightedSum(self, listSensor):
        """
        This function is giving each sensor a position and a weight.
        
        :Param listSensor: The sensor inputs
        :Type listSensor: List
        
        :Return: A list with the weighted position for each sum.
        
        """
        weightedSum = 0
        for index, value in enumerate(listSensor):
            weightedSum += value*self.positions[index]*self.weights[index]
        weightedSum= weightedSum/sum(listSensor)
        return weightedSum
    
    def findError(self,listSensor):
        sensorSum = self.weightedSum(listSensor)
        #Our setpoint is 0, so we use that to calculate the error
        error = 0-sensorSum
        return error

    def findControl(self,listSensor):
        error = self.findError(listSensor)
        control = self.kp*error
        return control
    
    def adjustStep(self, base_step, listSensor):
        control = self.findControl(listSensor)
        new_step_left = base_step+control
        new_step_right = base_step-control
        new_step_left = max(0, min(1, new_step_left))
        new_step_right = max(0, min(1, new_step_right))
        return new_step_left, new_step_right
    
    def adjustSpeed(self, new_step_left, new_step_right):
        max_delay = 40
        min_delay = 1
        constant = max_delay - min_delay
        diff = abs(new_step_left - new_step_right)

        new_delay = max_delay - constant * diff
        new_delay = max(min_delay, min(max_delay, new_delay))  # clamp til intervallet
        return new_delay
    
    def adjustPwmPct(self, new_delay):
        max_pwm = 0.6
        min_pwm = 0.3
        constant = 4
        new_pwm = max_pwm-new_delay*constant
        new_pwm = max(min_pwm, min(max_pwm, new_pwm)) #We are clamping the new_pwm
        return new_pwm
    
    
class StepperMotor:
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

        # Default step type
        self.seq = self.half_step()

    def adjustPwm(self, new_pwm):
        self.pwm_pct = new_pwm

    def initialize_pins(self, pins):
        pwm_list = []
        for pin in pins:
            p = PWM(Pin(pin))
            p.freq(self.frequency)
            pwm_list.append(p)
        return pwm_list

    def get_duty(self):
        return int(self.pwm_max * self.pwm_pct)

    def stop_step(self, pwm_list):
        stop_seq = [0, 0, 0, 0]
        self.set_duty(pwm_list, stop_seq)

    def full_step(self):
        d = self.get_duty()
        return [
            [d,0,0,0],
            [0,d,0,0],
            [0,0,d,0],
            [0,0,0,d],
        ]

    def half_step(self):
        d = self.get_duty()
        return [
            [d,0,0,0],
            [d,d,0,0],
            [0,d,0,0],
            [0,d,d,0],
            [0,0,d,0],
            [0,0,d,d],
            [0,0,0,d],
            [d,0,0,d],
        ]

    def set_duty(self, pwm_list, seq):
        for i, pwm_pin in enumerate(pwm_list):
            pwm_pin.duty_u16(seq[i])

    def turnLeftWheel(self, direction=1):
        seq = self.seq[self.left_seq_index]
        self.set_duty(self.left_pins, seq)
        self.left_seq_index = (self.left_seq_index + direction) % len(self.seq)

    def turnRightWheel(self, direction=1):
        seq = self.seq[self.right_seq_index]
        self.set_duty(self.right_pins, seq)
        self.right_seq_index = (self.right_seq_index + direction) % len(self.seq)

if __name__ == "__main__":

    # Variable to change the pwm percentage from the main file
    pwm_procent=0.5
    delay_val_1 = 0.0001

    # Initializes the right and left motor pins, and initializes the stepper
    stepper = StepperMotor([0,1,2,3],[4,5,6,7], pwm_procent)

    acc_left = 0
    acc_right = 0

    pControl = pController()
    sensor1 = Sensor()
    sensorTimout = 0
    #print("calibrating min")
    #sleep(2)
    #min_sensor = sensor1.calibrate()
    #print("calibrating max")
    #sleep(5)
    #max_sensor = sensor1.calibrate()
    new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
    sensorVal = 10
    while True:
        sensorTimout+=1
        
        #print(sensorVal)
        if sensorTimout > sensorVal:
            sensorVal = int(pControl.adjustSpeed(new_step_left, new_step_right))
            new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
            sensorTimout = 0
            
         
        #new_step_left, new_step_right = 0.5, 0.5
       
        acc_left += new_step_left
        acc_right += new_step_right
        
        if acc_left >=1:
            stepper.turnLeftWheel()
            acc_left -= 1
        if acc_right >= 1:
            stepper.turnRightWheel()
            acc_right -=1

#importing necessary libaries
from machine import Pin, ADC, PWM
from time import sleep_us
import _thread
import gc


#Sensor class
class Sensor():
    def __init__(self, z0 = 8, z1 = 9, z2 = 10, a0 = 28): #Pins to multiplexer and adc
        self.z0 = Pin(z0, Pin.OUT)
        self.z1 = Pin(z1,Pin.OUT)
        self.z2 = Pin(z2, Pin.OUT)
        self.adc_input = ADC(Pin(a0))
        self.current_adc_list = []
        self.adc_value = 0
        self.weightedSum = 0
        
        #Sensor sequence from left to right sensor
        self.sensor = [(1,0,1),
                       (0,0,0),
                       (0,0,1),
                       (1,0,0),
                       (0,1,0),
                       (1,1,0),
                       (1,1,1),
                       (0,1,1)]
 
        
    def zSetValue(self,row):
        '''
        This function is used to set the z values.
        It will allow the multiplexer to change wich input we are measuring over with our adc
        
        :param row: The row of the sequence we want to use
        :type row: Int
        '''
        self.z0.value(self.sensor[row][0]), self.z1.value(self.sensor[row][1]), self.z2.value(self.sensor[row][2])

    
    def runSensor(self):
        '''
        This function collects the sensor data and stores it in a list
        
        :return current_adc_list: A list containing the sensor values.
        '''
        self.current_adc_list = []
        for number_Z_List in range(len(self.sensor)):
            self.zSetValue(number_Z_List)
            self.adc_value = self.adc_input.read_u16()
            self.current_adc_list.append(self.adc_value)
        return self.current_adc_list


class pController():
    def __init__(self, kp = 2.0):
        
        #The position of each sensor
        self.positions = [-4,-3, -2, -1, 1, 2, 3,4]
        
        #The wegiht of each sensor. 
        self.weights = [1, 1, 1, 1, 1, 1, 1,1]
        
        #The P constant for P control
        self.kp = kp
        
        self.control = 0
        self.weightSum = 0
    
    def weightedSum(self, current_adc_list):
        """
        This function is giving each sensor a position and a weight.
        
        :Param listSensor: The sensor inputs
        :Type listSensor: List
        
        :Return: A list with the weighted position for each sum.
        
        """
        self.weightSum = 0
        
        #Sums the list of adc with each position and weight.
        for index, value in enumerate(current_adc_list):
            self.weightSum += value*self.positions[index]*self.weights[index]
        self.weightSum= self.weightSum/sum(current_adc_list)
        
        #Returns the weighted sum.
        return self.weightSum
    
    def findError(self,current_adc_list):
        '''
        This function calculates the error for the current_adc_list it includes the function weightedSum.
        
        :return error: It returns the error.
        '''
        sensorSum = self.weightedSum(current_adc_list)
        #Our setpoint is 0, so we use that to calculate the error
        error = 0-sensorSum
        return error

    def findControl(self,current_adc_list):
        '''
        This function evaluate the error and uses the P constant
        to determine the control that each motor should be adjustet by.
        
        :return control: It returns the control. 
        '''
        error = self.findError(current_adc_list)
        control = self.kp*error
        
        return control
    
    def adjustStep(self, base_step, current_adc_list):
        '''
        This function is uses the findControl function to adjust the step for each motor.
        We clamp each motors step. Wich means we make it return a value at least zero.
        
        :return new_step_left: How many steps the left motor should make
        :return new_step_right: How many steps the right motor should make
        '''
        self.control = self.findControl(current_adc_list)
        new_step_left = base_step+self.control
        new_step_right = base_step-self.control
        new_step_left = max(0, min(base_step, new_step_left))
        new_step_right = max(0, min(base_step,new_step_right))
        return new_step_left, new_step_right  

#New steppermotor class. Steppermotor + drive
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

    def get_duty(self):
        '''
        Uses this function to calculate the pwm with the given percentage
        
        :return: Returns the calculated pwm
        
        '''
        return int(self.pwm_max * self.pwm_pct)

    def stop_step(self, pwm_list):
        '''
        This function kills the pwm on the motor.
        '''
        stop_seq = [0, 0, 0, 0]
        self.set_duty(pwm_list, stop_seq)

    def set_duty(self, pwm_list,seq):
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
        d = self.get_duty()
        seq = [
               [d,0,0,0],
               [d,d,0,0],
               [0,d,0,0],
               [0,d,d,0],
               [0,0,d,0],
               [0,0,d,d],
               [0,0,0,d],
               [d,0,0,d],
               ]
        return seq
    
    

    def turnLeftWheel(self, direction=1):
        '''
        Uses this function to turn the left wheel with the given sequence.
        We only move one step of the sequence and saves the index we got to.
        '''
    
        self.set_duty(self.left_pins, self.half_seq[self.left_seq_index])
        self.left_seq_index = (self.left_seq_index + direction) % len(self.half_seq)

    def turnRightWheel(self, direction=1):
        '''
        Uses this function to turn the right wheel with the given sequence.
        We only move one step of the sequence and saves the index we got to.
        
        '''
        #sleep_us(100)
        
        self.set_duty(self.right_pins, self.half_seq[self.right_seq_index])
        self.right_seq_index = (self.right_seq_index + direction) % len(self.half_seq)

if __name__ == "__main__":
    
    
    # Variable to change the pwm percentage from the main file
    pwm_procent=0.6

    # Initializes the right and left motor pins, and initializes the stepper
    stepper = StepperMotor([0,1,2,3],[4,5,6,7], pwm_procent)

    acc_left = 0
    acc_right = 0

    #Initialize the pController and Sensor
    pControl = pController()
    sensor1 = Sensor()

    
    #sensorTimeout 
    sensorTimout = 0
    
    new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
    sensorDelay = 6
    #gc.disable()
    gc.enable()
    while True:
        sensorTimout+=1
        

        if sensorTimout > sensorDelay:
            new_step_right,new_step_left = pControl.adjustStep(1.0, sensor1.runSensor())
            sensorTimout = 0
            
            
    
        acc_left += new_step_left
        acc_right += new_step_right
        
        
        if acc_left >=1:
            stepper.turnLeftWheel()
            acc_left -= 1
        if acc_right >= 1:
            stepper.turnRightWheel()
            acc_right -=1 

        
         


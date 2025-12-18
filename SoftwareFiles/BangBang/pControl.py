# pController.py onsdag 11/19
from machine import Pin, ADC, PWM

class pController():
    def __init__(self, kp = 1.0):
        
        #The position of each sensor
        self.positions = [-4,-3, -2, -1, 1, 2, 3, 4]
        
        #The wegiht of each sensor. 
        self.weights = [3,3.5,2,1,1,2,3.5,3]
        #self.weights = [2.3,3,1,1,1,1,3,2.3]
        
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


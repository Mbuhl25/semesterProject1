#P controller
from sensor import Sensor


class pController():
    def __init__(self, kp = 0.4):
        self.positions = [-3, -2, -1, 1, 2, 3]
        self.weights = [1, 1, 1, 1, 1, 1]
        self.kp = kp
    
    def weightedSum(self, listSensor):
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
        max_delay = 60
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

        
        
         

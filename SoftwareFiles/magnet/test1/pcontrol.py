#P controller
from sensor import Sensor


class pController():
    def __init__(self, kp = 2):
        self.positions = [-4,-3,-2,-1, 1, 2, 3, 4]
        self.weights = [0.72, 0.91, 0.86, 0.76, 0.93, 1.00, 0.53, 0.57]
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
    
#bangBang
from machine import Pin, ADC, PWM

class bangBang():
    def __init__(self):
        self.weights = [0.72, 0.92, 0.91, 0.88, 0.89, 1.00, 0.76, 0.83]
    
    def normaliser(self,sensorList):
        normaliser = [x * y for x, y in zip(sensorList, sensor.weights)]
        normaliser = self.weights
        return normaliser
    
    def adjustStep(self, normSensorList):
        
        if normSensorList
        
        
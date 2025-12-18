#sensor.py onsdag 19/11
from machine import Pin, ADC, PWM
from time import sleep

class Sensor():
    def __init__(self, z0 = 8, z1 = 9, z2 = 10, a0 = 28): #Pins to multiplexer and adc
        self.z0 = Pin(z0, Pin.OUT)
        self.z1 = Pin(z1,Pin.OUT)
        self.z2 = Pin(z2, Pin.OUT)
        self.adc_input = ADC(Pin(a0))
        self.current_adc_list = []
        self.adc_value = 0
        self.weightedSum = 0
        self.weights = [0.710,0.902,0.894,0.877,0.893,1.000,0.784,0.838]
        
        #Sensor sequence from left to right sensor
        self.sensor = [(1,0,1),
                       (0,1,1)]
        '''
        self.sensor = [(1,0,1),
                       (0,0,0),
                       (0,0,1),
                       (1,0,0),
                       (0,1,0),
                       (1,1,0),
                       (1,1,1),
                       (0,1,1)]'''
 
        
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
    

if __name__ == "__main__":
    sensor = Sensor()
    while True:
        resultat = [x * y for x, y in zip(sensor.runSensor(), sensor.weights)]
        print(resultat)
        sleep(0.1)

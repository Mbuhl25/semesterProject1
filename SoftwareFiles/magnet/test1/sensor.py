#Sensor
from machine import Pin, ADC
import asyncio
from time import sleep



#Sort GPIO 8
#Rød GPIO 9
#Gul GPIO 10

class Sensor():
    def __init__(self, z0 = 8, z1 = 9, z2 = 10, a0 = 28):
        self.z0 = Pin(z0, Pin.OUT)
        self.z1 = Pin(z1,Pin.OUT)
        self.z2 = Pin(z2, Pin.OUT)
        self.adc_input = ADC(Pin(a0))
        self.current_adc = []
        self.sensor = [(0,0,0),
                       (0,0,1),
                       (1,0,0),
                       (0,1,0),
                       (1,1,0),
                       (1,1,1)]
        
        self.sensor8 = [(0,1,1),
                       (1,1,1),
                       (1,0,1),
                       (0,0,1),
                       (1,0,0),
                       (0,1,0),
                       (0,0,0),
                       (1,1,0)]
        
        self.sensor_lookup = {
                            (1,0,1): 1,
                            (0,0,0): 2,
                            (0,0,1): 3,
                            (1,0,0): 4,
                            (0,1,0): 5,
                            (1,1,0): 6,
                            (1,1,1): 7,
                            (0,1,1): 8
                            }
                            
        
    def calibrate(self, number_calibrations = 10):
        '''
        This function is used to calibrate the sensors.
        It will make X measurements and use the averageList function to generate and average sensorList.
        
        :param number_calibrations: How many calibrations
        :type number_calibrations: Int
        
        :return sensor_calibration_total: A list with the average measurements
        '''
        
        sensor_calibration_total = []
        for number_cal in range(number_calibrations):
            sensor_calibration = []
            sleep(0.2)
            for number_Z_List in range(len(self.sensor8)):
                self.zSetValue(number_Z_List)
                adc_value = self.readAdc()
                sensor_calibration.append(adc_value)
            sensor_calibration_total.append(sensor_calibration)
        sensor_calibration_total = averageList(sensor_calibration_total)
        return sensor_calibration_total
        
        
    def readAdc(self):
        '''
        This function is used to measure the adc value
        
        :return adcValue: The adc value over self.adc_input
        '''
        adcValue = self.adc_input.read_u16()
        return adcValue
    
    def sensorLookup(self, row):
        '''
        This function is used to lookup wich sensor is connected to wich sequence.
        :param row: The row of the sequence you want to lookup
        :type row: Int
        
        :return sensor: Int, A number of wich sensor is connected to that specefic row of the sequence.
        '''
        sensor = self.sensor_lookup[(self.sensor8[row][0],self.sensor8[row][1],self.sensor8[row][2])]
        #print(self.sensor[row][0],self.sensor[row][1],self.sensor[row][2])
        return sensor
        
    def zSetValue(self,row):
        '''
        This function is used to set the z values.
        It will allow the multiplexer to change wich input we are measuring over with our adc
        
        :param row: The row of the sequence we want to use
        :type row: Int
        '''
        self.z0.value(self.sensor8[row][0]), self.z1.value(self.sensor8[row][1]), self.z2.value(self.sensor8[row][2])
    
    
    def runSensorNorm(self, minList,maxList):
        self.current_adc = []
        for number_Z_List in range(len(self.sensor8)):
            self.zSetValue(number_Z_List)
            adc_value = self.readAdc()
            self.current_adc.append(adc_value)
        self.current_adc = norm(self.current_adc, minList, maxList)
        return self.current_adc
    
    def runSensor(self):
        self.current_adc = []
        for number_Z_List in range(len(self.sensor8)):
            self.zSetValue(number_Z_List)
            adc_value = self.readAdc()
            self.current_adc.append(adc_value)
        return self.current_adc
    
if __name__ == "__main__":
    sensor = Sensor()
    while True:
        print(sensor.runSensor())
        sleep(0.1)

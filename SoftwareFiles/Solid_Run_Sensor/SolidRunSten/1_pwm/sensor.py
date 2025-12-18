# sensor.py onsdag 19/11
from machine import Pin, ADC, PWM
from time import sleep
import array

class Sensor():
    def __init__(self, z0=8, z1=9, z2=10, a0=28):

        # Pins to multiplexer
        self.z0 = Pin(z0, Pin.OUT)
        self.z1 = Pin(z1, Pin.OUT)
        self.z2 = Pin(z2, Pin.OUT)

        self.adc_input = ADC(Pin(a0))

        # ADC values (unsigned 16-bit)
        self.current_adc_list = array.array('H', [0]*8)

        self.adc_value = 0

        # Sensor weights
        self.weights = array.array(
            'f',
            [0.710, 0.902, 0.894, 0.877, 0.893, 1.000, 0.784, 0.838]
        )

        # Sensor sequence (flattened: z0,z1,z2 per sensor)
        self.sensor = array.array(
            'b',
            [
                1,0,1,
                0,0,0,
                0,0,1,
                1,0,0,
                0,1,0,
                1,1,0,
                1,1,1,
                0,1,1
            ]
        )

    def zSetValue(self, row):
        '''
        Set multiplexer values
        '''
        base = row * 3
        self.z0.value(self.sensor[base])
        self.z1.value(self.sensor[base + 1])
        self.z2.value(self.sensor[base + 2])

    def runSensor(self):
        '''
        Collect sensor data
        '''
        for i in range(8):
            self.zSetValue(i)
            self.current_adc_list[i] = self.adc_input.read_u16()
        return self.current_adc_list


if __name__ == "__main__":
    sensor = Sensor()

    while True:
        # Weighted result using array
        resultat = array.array(
            'f',
            (x * y for x, y in zip(sensor.runSensor(), sensor.weights))
        )

        print(resultat)
        sleep(0.1)

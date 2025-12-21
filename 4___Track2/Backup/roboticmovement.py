from drive import Drive
from steppermotor import StepperMotor
from machine import Pin
import math
from sensor import Sensor
from pcontrol import pController
from time import sleep
from micro_actuator_stepper import Mircrostepper


class Roboticmovements:
    def __init__(self):
        
        
        self.sensor1 = Sensor()
        
        
        # robot geometry
        self.wheel_circumference = 26.7
        self.wheelbase = 23.5
        self.distance_per_step = self.wheel_circumference / 400

        # motors
        
        self.left = StepperMotor([0,1,2,3])
        self.leftseq = self.left.half_step()
        self.right = StepperMotor([4,5,6,7])   
        self.robot = Drive(self.left, self.right)
        
        # p-control
        self.pwm_procent = 0.3
        self.delay_val_1 = 0.0001

        self.pControl1 = pController()          
                   

        self.acc_left = 0
        self.acc_right = 0
        
        self.new_step_left ,self.new_step_right = self.pControl1.adjustStep(1.0, self.sensor1.runSensor())
        
        # sensor
        self.converted_sen= []
        
        
        #othermotors
        self.magnet = Pin(19, Pin.OUT)         
        self.actutor1 = Mircrostepper()
        
        self.weights = [0.72, 0.91, 0.86, 0.76, 0.93, 1.00, 0.53, 0.57]
    def sensorfollow(self):
        """
        Funktion: this funktion make the robot follow the black line
        """ 
        # calibations
        self.new_step_right, self.new_step_left = self.pControl1.adjustStep(1.0, self.sensor1.runSensor())
        
        # accumulate step changes
        self.acc_left += self.new_step_left 
        self.acc_right += self.new_step_right
        
        # LEFT wheel trigger
        if self.acc_left >= 1:
            self.robot.turnWheel(self.leftseq, "left", 0.0001, 1)
            self.acc_left -= 1

        # RIGHT wheel trigger
        if self.acc_right >= 1:
            self.robot.turnWheel(self.leftseq, "right", 0.0001, 1)
            self.acc_right -= 1
    
            
    def move_distance(self, cm, direction, speed=0.01):
        """
        funktion moves the robot in a line in the given leanght
        
        param, float, cm: the distance to move
        
        variable, int, number_of_steps: caluclate the number of steps from cm
        
         retruns a movement
        """

        number_of_steps=int(cm/self.distance_per_step)
        
        
        for i in range(number_of_steps): # moves the motors  changingly one step a time
                self.robot.turnWheel(self.leftseq, "left", speed, direction)
                self.robot.turnWheel(self.leftseq, "right", speed, direction)
     
        self.robot.stop() # set all motors to seqensce to 0 
    
    
    
    def turn_degree(self, degree=90, direction=1, speed=0.01):
        
        
        """
        funktion: this funktion make the robot turn an x dergree
        
        param, float, degree: the distance to move
        
        variable, float, turning_circumference: caluclate the circumference around the wheels
        
        variable, float, full_turn_steps: 
        
        variable, steps_turn_degree
        
        retruns a movement
        """
        
        #calculate degrees to steps
        turning_circumference = 2*math.pi*self.wheelbase
        full_turn_steps = turning_circumference/self.distance_per_step
        steps_turn_degree = abs(full_turn_steps * (degree / 360)) / 2
        
        
        for i in range(int(steps_turn_degree)):
               
            self.robot.turnWheel(self.leftseq, "left", speed, -direction)
            self.robot.turnWheel(self.leftseq, "right", speed, direction)
        self.robot.stop()
        
        
    def converted_sensorupdate(self):
        sensorList = self.sensor1.runSensor()
        self.converted_sen = self.blackconvertor(sensorList)
        return self.converted_sen
        
    
        
    def blackconvertor(self, sensorList, thedshoald=26000):
        sensorList = resultat = [x * y for x, y in zip(sensorList, self.weights)]
        result = []
        for value in sensorList:
            if value < thedshoald:
                result.append("1")
            else:
                result.append("2")
        return result
    
    
    def turndetect(self, direction=1):
        while True:
            self.converted_sensorupdate()
            self.turn_degree(1, direction, speed=0.004)
            if self.converted_sen[0] == "2":
                self.turn_degree(25, 1)
                break
            if self.converted_sen[7] == "2":
                self.turn_degree(25, -1, speed=0.004)
                break  
    
    
    def pickup(self):
        self.actutor1.step_motor(0.001, 1280, -1)
        self.magnet(1)
        self.mag_scan()
        self.actutor1.step_motor(0.002, 1350, 1)
        self.magnet(0)
        sleep(1)
        
    
    def pickup_center(self):
        self.actutor1.step_motor(0.001, 1280, -1)
        self.magnet(1)
        self.mag_scan()
        self.actutor1.step_motor(0.002, 1350, 1)
        self.magnet(0)
        
    def pickup_right(self):
        self.move_distance(10, -1, speed=0.004)
        self.turn_degree(175, 1, speed=0.004)
        self.move_distance(13, -1, speed=0.004)
        
        self.pickup()       

        self.move_distance(5, 1, speed=0.004)
        self.turn_degree(140, 1, speed=0.004)
        self.turndetect()
        self.move_distance(10, 1, speed=0.004)
        
        
    def pickup_left(self):
        self.move_distance(10, -1, speed=0.004)
        self.turn_degree(170, -1, speed=0.004)
        self.move_distance(13, -1, speed=0.004)
        self.pickup()  
        
        

        self.move_distance(5, 1, speed=0.004)
        self.turn_degree(140, -1, speed=0.004)
        self.turndetect(-1)
        self.move_distance(10, 1, speed=0.004)
    
    
    
        
    def mag_scan(self, degrre=10, direction=1):
        if direction == 1:
            for i in range(2):
                self.turn_degree(degrre, -1)
                self.turn_degree(degrre, 2)
                self.turn_degree(degrre, -1)
                self.move_distance(2, 1)
        if direction == -1:
            for i in range(2):
                self.turn_degree(degrre, 1)
                self.turn_degree(degrre, -2)
                self.turn_degree(degrre, 1)
                
                self.move_distance(2, -1)
    
    def cluetjek1(self):
        clueright = False
        clueleft = False
        
        for i in range(2):
            self.converted_sensorupdate()
            if self.converted_sen[0] == "2":
                clueright = True

                self.turn_degree(5, -1)
                print("ø")
            self.converted_sensorupdate()
            if self.converted_sen[7] == "2":
                clueleft = True
                self.turn_degree(5, 1)
                print("l")
            if clueleft == True and clueright == True:
                print("å")
                return(True)
        
        return(False)

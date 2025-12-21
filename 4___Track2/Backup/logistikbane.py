from drive import Drive
from steppermotor import StepperMotor
from machine import Pin
import math
from sensor import Sensor
from pcontrol import pController
from time import sleep
from micro_actuator_stepper import Mircrostepper
from servoclass import Servo
from eletromagnet import Eletromagnet
"""
specifik move varibals 
"""

wheel_circumference = 26.7
wheelbase = 23.5
button = Pin(8, Pin.IN, Pin.PULL_DOWN)
left = StepperMotor([0,1,2,3])
leftseq=left.half_step()
right = StepperMotor([4,5,6,7])
distance_per_step = 26.7/400
robot = Drive(left, right)

"""
pcontrol varibals
"""

pwm_procent=0.2
delay_val_1 = 0.0001
pControl1 = pController()
sensor1 = Sensor()
acc_left = 0
acc_right = 0
sensorLookup = 0
new_step_left, new_step_right = pControl1.adjustStep(0.5, sensor1.runSensor())

pp = 0
progress = 3



def sensorfollow():
    global sensorLookup, new_step_left, new_step_right, acc_left, acc_right
    sensorLookup+=1
    #sensorVal = int(pControl.adjustSpeed(new_step_left, new_step_right))
    if sensorLookup%1 == 0:
        new_step_right, new_step_left = pControl1.adjustStep(1.0, sensor1.runSensor())
        sensorLookup = 0
     
    #new_step_left, new_step_right = 0.5, 0.5
   
    acc_left += new_step_left
    acc_right += new_step_right
    
    if acc_left >=1:
        robot.turnWheel(leftseq, "left", 0.01, 1)
        acc_left -= 1
    if acc_right >= 1:
        robot.turnWheel(leftseq, "right", 0.01, 1)
        acc_right -=1
    #delay_val_1
        
#def sensorfollowline_step

        
def move_distance(cm, direction):
    """
    funktion moves the robot in a line in the given leanght
    
    param, float, cm: the distance to move
    
    variable, int, number_of_steps: caluclate the number of steps from cm
    """

    number_of_steps=int(cm/distance_per_step)
    if direction == 1:
        for i in range(number_of_steps):
            robot.turnWheel(leftseq, "left", 0.01, 1)
            robot.turnWheel(leftseq, "right", 0.01, 1)
    if direction == -1:
        for i in range(number_of_steps):
            robot.turnWheel(leftseq, "left", 0.01, -1)
            robot.turnWheel(leftseq, "right", 0.01, -1)
 
    robot.stop()
def turn_degree(degree=90, direction=1):
    
    
    """
    param, float, degree: the distance to move
    
    variable, float, turning_circumference: caluclate the circumference around the wheels
    
    variable, float, full_turn_steps: 
    
    variable, steps_turn_degree
    """
    turning_circumference = 2*math.pi*wheelbase
    full_turn_steps = turning_circumference/distance_per_step
    steps_turn_degree = abs(full_turn_steps/(360/degree))
    steps_turn_degree = steps_turn_degree/2
    if direction == 1:
        for i in range(steps_turn_degree):
            robot.turnWheel(leftseq, "left", 0.01, -1)
            robot.turnWheel(leftseq, "right", 0.01, 1)
    if direction == -1:
         for i in range(steps_turn_degree):
            robot.turnWheel(leftseq, "left" ,0.01, 1)
            robot.turnWheel(leftseq, "right", 0.01, -1)
    robot.stop()
    
def præs(degree=5, direction=1):
    if direction == 1:
        for i in range(2):
            turn_degree(degree, -1)
            turn_degree(degree, 1)
          
            move_distance(1.25, 1)
    if direction == -1:
         for i in range(2):
            turn_degree(degree, -1)
            turn_degree(degree, 1)
         
            move_distance(1.25, -1)       




def blackconvertor(sensorlist):
    result = []
    for value in sensorlist:
        if value < 25000:
            result.append("1")
        else:
            result.append("2")
    return result

     
 
def bane1():
    global progress
    if cluetjek() == True:
        move_distance(20, 1)
        turn_degree(90, 1)
        print("6")
        progress = 1 + progress
    
    

def cluetjek1():
    clueright = False
    clueleft = False
    
    for i in range(2):
        sen = sensor1.runSensor()
        converted_sen = blackconvertor(sen)
        if converted_sen[0] == "2":
            clueright = True

            turn_degree(5, -1)
            print("ø")
        sen = sensor1.runSensor()
        converted_sen = blackconvertor(sen)
        if converted_sen[7] == "2":
            clueleft = True
            turn_degree(5, 1)
            print("l")
        if clueleft == True and clueright == True:
            print("å")
            return(True)
    
        return(False)
  
      
    

def nutvarify(turn=90, dist= 20):
    global pp
    global progress
    if converted_sen[0] == "2" or converted_sen[7] == "2":
        turn_degree(90, -1)
        præs(5, 1)
        move_distance(5, -1)
        turndetect()
        move_distance(dist, 1)
        progress = progress + 1
        
        
def turndetect(direction=1):
    while True:
        sen = sensor1.runSensor()
        converted_sen = blackconvertor(sen)
        turn_degree(1, )
        if converted_sen[0] == "2":
            turn_degree(25, 1)
            break
        if converted_sen[7] == "2":
            turn_degree(25, -1)
            break





    

sen = sensor1.runSensor()
 #print(blackconvertor(sen))
    #print(sen)
    #sleep(1)
#sen = sensor1.runSensor()
def banetjek():
    global progress
    global converted_sen
    
    if progress < 2:
        nutvarify()
        #print(progress)
    if progress == 2:
        if converted_sen[0] == "2" or converted_sen[7] == "2":
            move_distance(27, 1)
            turn_degree(100, 1)
            progress = 1 + progress
            print(progress)
            sen = sensor1.runSensor()
            converted_sen = blackconvertor(sen)
    if  2 < progress < 5:
        nutvarify()
    if progress == 5:
        turn_degree(180, 1)
        progress = 1 + progress
    if progress > 5:
        if converted_sen == ["2","2","2","2","2","2","2","2"]:
            move_distance(15, 1)
            print(progress)
            
            
            
            
magnet1 =  Eletromagnet(pin=19)          
actutor1 = Mircrostepper()            
def pickup():
    actutor1.step_motor(0.002, 1400, -1)    
    magnet1.eletromagnetstatus("on")
    actutor1.step_motor(0.002, 1400, 1)
    magnet1.eletromagnetstatus("off")
    
    
def pickup_right():
    move_distance(10, -1)
    turn_degree(170, 1)
    move_distance(2.5, -1)
    pickup()
    move_distance(2.5,1)
    turn_degree(-170, 1)    
 
 
sensorLookup = 0
new_step_right = 0
new_step_left = 0
acc_left = 0
acc_right = 0
while True:
    sensorLookup+=1
    #sensorVal = int(pControl.adjustSpeed(new_step_left, new_step_right))
    if sensorLookup%1 == 0:
        new_step_right, new_step_left = pControl1.adjustStep(1.0, sensor1.runSensor())
        sensorLookup = 0
     
    #new_step_left, new_step_right = 0.5, 0.5
   
    acc_left += new_step_left
    acc_right += new_step_right
    
    if acc_left >=1:
        robot.turnWheel(leftseq, "left", 0.001, 1)
        acc_left -= 1
    if acc_right >= 1:
        robot.turnWheel(leftseq, "right", 0.001, 1)
        acc_right -=1




    
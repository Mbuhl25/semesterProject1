import time
from roboticmovement import Roboticmovements
""" final"""
nextstate = False
loop = -1

"""
hvis state = start
loop = -1 samler de to første op
loop = 0 samler de 3 øverste op
loop = 1 samler venste arm op
loop = 2 samler højre arm op

"""

indivprogressleft = 0
indivprogressrright = 0
#states
START =0
TORSO = 1
NECK = 2
HOME = 3
TRANSIT_TORSO = 4
HEAD = 5
LEFTARM = 6
TRANSIT_LEFTARM = 7
RIGHT_ARM = 8





# start state
state = START


robot = Roboticmovements()
def Run_right_arm():
    """
    Funktion: when the robot is on the right arm the funktion
    tell what is should do
    
    returns: robotic movment
    """
    global nextstate
    global indivprogressrright
    sen = robot.Converted_sensorupdate()
    robot.Sensorfollow()
    
    if indivprogressrright == 0 and sen[0] == "2":
        robot.Turn_degree(40, 1, 0.002)
        robot.Move_distance(24, 1, 0.002)
        robot.Turn_degree(80, 1, 0.002)
        indivprogressrright += 1
        
    elif indivprogressrright == 1 and sen[7] == "2":
        robot.Pickup_right()
        indivprogressrright = 0
        Nutsnipe()
         
       

def Nutsnipe():
    
    """
    funktion: when the robot have picked up one nut one right arm
    it will hardcoded go for the last and return home
    
    returns:  a robotic movement
    """
    global nextstate
    
    robot.Turn_degree(1.5,1, 0.002)
    robot.Move_distance(153.5, -1, 0.002)
    robot.Pickup()
    robot.Move_distance(2,-1, 0.002)
    robot.Move_distance(100,-1, 0.001)
    robot.Turn_degree(95,-1, 0.002)
    robot.Move_distance(500,-1, 0.001)
    
     
    
    
def Drive_look_sides():
    
    """
    funktion: Looks for black spaces to pickup nuts.
    and indicate when driven over left side it the state can begin looking for transisions points.
    
    """
    global nextstate
    sen = robot.Converted_sensorupdate()                       
    robot.Sensorfollow()
    if sen[7] == "2":
        robot.Pickup_right()
        robot.Move_distance()
        
    elif sen[0] == "2":
        robot.Pickup_left()
        
        nextstate = True

def Headsearch():
    global nextstate
    """
    Funktion: Hardcoded seqence to pickup nuts in STATE_4
    """
    if sen[0] == "2":
        robot.Turn_degree(190,1, 0.004)
        robot.Move_distance(65,-1, 0.004)
        robot.Pickup()
        robot.Move_distance(30,-1, 0.004)
        robot.Turn_degree(45,1, 0.004)
        robot.Move_distance(15,-1, 0.004)
        robot.Pickup()
        time.sleep(1)
        robot.Move_distance(13,1, 0.004)
        robot.Turn_degree(90,-1, 0.004)
        robot.Move_distance(15,-1, 0.004)
        robot.Pickup()
        time.sleep(1)
        robot.Move_distance(14,1, 0.004)
        print("1")
        robot.Turn_degree(45,1)
        robot.Move_distance(30,1, 0.004)
        
        nextstate = True

# main loop

def State_Machine():
    global nextstate, loop, TORSO, NECK, HOME, TRANSIT_LEFTARM, TRANSIT_TORSO, LEFTARM, RIGHT_ARM, state
     """
    funktion: main State_Machine 
    """
    
    """
    State START: This state count a loop up for every time the robot gets back
    and make it turn around and to the main line.
    """
    # start state
    if state == START:
        loop = loop + 1
        time.sleep(10)
        
        # If loop = 0 
        if loop == 0:
            robot.Move_distance(30, 1, 0.004)
            state = TORSO
            
            
        # if loop = 1 or 2
        if loop == 1 or loop == 2:
            robot.Move_distance(50, -1, 0.004)
            robot.Turn_degree(100, 1, 0.004)
            robot.Turndetect()
            
            state = TRANSIT_TORSO
            
        # if loop = 3
        if loop == 3:
            # state run
            robot.Move_distance(50, -1, 0.004)
            
            robot.Turn_degree(100, 1, 0.004)
            
            # New state Condition
            robot.Turndetect()
            nextstate = False
            
            # new state
            state = RIGHT_ARM
    
    
    
    
    
    
    
    # state TORSO
    elif state == TORSO:
        
        # state run
        if nextstate == False:
            Drive_look_sides()
         
        # New state Condition
        if nextstate:
            robot.Sensorfollow()
            if robot.Cluetjek1():
                
                # new state
                state = NECK
                robot.Move_distance(20, 1, 0.004)
                nextstate = False
                
                
     # state NECK       
    elif state == NECK:
        if nextstate == False:
            
           Drive_look_sides()
           
           # New state Condition (toggled in Drive_look_sides)
        if nextstate:
            
            # new state
            state = HOME
            nextstate = False
        
        # state HOME   
    elif state == HOME:
        if nextstate == False:
             # state run
            robot.Move_distance(10, -1, 0.004)
            robot.Turn_degree()
            robot.Turndetect()
            nextstate = True
            
            
        if nextstate:
            robot.Sensorfollow()
            sen = robot.Converted_sensorupdate()
            # New state Condition
            if sen == ["1","1","1","1","1","1","1","1"]:
                robot.Move_distance(50, 1, 0.002)
                # new state
                state = START
                nextstate = False
                
                
                
    # state TRANSIT_LEFTARM    
    elif state == TRANSIT_LEFTARM:
        # state run
        robot.Sensorfollow()
        sen = robot.Converted_sensorupdate()
        # New state Condition
        if sen == ["1","1","1","1","1","1","1","1"]:
            robot.Move_distance(30, 1, 0.004)
            robot.Turn_degree(70, -1, 0.004)
            robot.Turndetect(-1)
            # new state
            state = HOME
            nextstate = True    
        
    # state TRANSIT_TORSO
    elif state == TRANSIT_TORSO:
        robot.Sensorfollow()
        # New state Condition
        if robot.Cluetjek1():
            if loop == 1:
                robot.Move_distance(20, 1, 0.004)
                 # new state
                state = HEAD
            if loop == 2:
                robot.Move_distance(20, 1, 0.004)
                robot.Turn_degree(90, 1, 0.004)
                 # new state
                state = LEFTARM
            if loop == 3:
                robot.Move_distance(20, 1, 0.002)
                robot.Turn_degree(90, -1)
                
                state = RIGHT_ARM
                    
                
                
    # state LEFTARM
    elif state == LEFTARM:
        # state run
        robot.Sensorfollow()
        sen = robot.Converted_sensorupdate()
        if sen[7] == "2":
            print ("right")
            robot.Pickup_right()
            robot.Move_distance(5, 1, speed=0.004)
            indivprogressleft = indivprogressleft + 1
             # New state Condition
            if indivprogressleft == 2:
                
                robot.Move_distance(10, -1, speed=0.004)
                robot.Turn_degree(175, 1, speed=0.004)
                robot.Move_distance(13, -1, speed=0.004)
                 # new state
                state = TRANSIT_LEFTARM
                
                
    
    # state HEAD
    elif state == HEAD:
        # state run
        if nextstate == False:
            robot.Sensorfollow()
            sen = robot.Converted_sensorupdate()
            Headsearch()
        # New state Condition(Condition is in Headsearch)
        if nextstate:
            # new state
            state = HOME
            
     # state RIGHT_ARM        
    elif state == RIGHT_ARM:
        Run_right_arm()

while True:
    State_Machine()


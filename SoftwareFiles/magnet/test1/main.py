import time
from roboticmovement import Roboticmovements
nextstate = False


#states
Home = 0
start = 1
STATE_1 = 2
STATE_2 = 3


# start state
state = STATE_1


robot = Roboticmovements()

def home():
    global nextstate
    robot.sensorfollow() 
    
    
def run_state1():
    global nextstate
    sen = robot.converted_sensorupdate()
    robot.sensorfollow()
    if sen[7] == "2":
        print("picked up right")
        robot.pickup_right()
        
    elif sen[0] == "2":
        print("picked up left")
        robot.pickup_left()
        
        nextstate = True
        
    return STATE_1

def run_state2():
    global nextstate
    sen = robot.converted_sensorupdate()
    robot.sensorfollow()
    
    if sen[7] == "2":
        print("picked up right")
        robot.pickup_right()
        

    elif sen[0] == "2":
        print("picked up left")
        robot.pickup_left()
      
        nextstate = True 
    return STATE_2




# main loop
while True:
    if state == STATE_1:
        
        # state run
        if nextstate == False:
            run_state1()
         
        # next state transet   
        if nextstate:
            robot.sensorfollow()
            if robot.cluetjek1():
                state = STATE_2
                robot.move_distance(25, 1, 0.001)
                nextstate = False
                
    elif state == STATE_2:
        if nextstate == False:
           run_state2()
           
        if nextstate:
            state = Home
            nextstate = False
        
        
        
    elif state == Home:
        if nextstate == False:
            robot.move_distance(10, -1, 0.001)
            robot.turn_degree()
            robot.turndetect()
            nextstate = True
        if nextstate:
            home()
            sen = robot.converted_sensorupdate()
            if sen == ["1","1","1","1","1","1","1","1"]:
                robot.move_distance(20, 1)
                state = start
                nextstate = False
                
        
    elif state == start:
        print("help meee")
                




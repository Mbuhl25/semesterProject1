import time
from roboticmovement import Roboticmovements

nextstate = False
loop = -1
indivprogress=0
#states
Home = 0
start = 1
STATE_1 = 2
STATE_2 = 3
State_4 = 4
transit = 5
state_3 = 6
transit2 = 7





# start state
state = start


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
        robot.move_distance
        
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

def headsearch():
    global nextstate
    if sen[0] == "2":
        robot.turn_degree(190,1, 0.004)
        robot.move_distance(65,-1, 0.004)
        robot.pickup()
        robot.move_distance(30,-1, 0.004)
        robot.turn_degree(45,1, 0.004)
        robot.move_distance(17,-1, 0.004)
        robot.pickup()
        time.sleep(1)
        robot.move_distance(13,1, 0.004)
        robot.turn_degree(90,-1, 0.004)
        robot.move_distance(15,-1, 0.004)
        robot.pickup()
        time.sleep(1)
        robot.move_distance(14,1, 0.004)
        print("1")
        robot.turn_degree(45,1)
        robot.move_distance(30,1, 0.004)
        
        nextstate = True
        print(nextstate)

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
                robot.move_distance(40, 1, 0.001)
                state = start
                nextstate = False
                
                
                
                
    elif state == transit2:
        home()
        sen = robot.converted_sensorupdate()
        if sen == ["1","1","1","1","1","1","1","1"]:
            robot.move_distance(30, 1, 0.001)
            robot.turn_degree(70, -1)
            robot.turndetect(-1)
            state = Home
            nextstate = True
        
    elif state == start:
        loop = loop + 1
        time.sleep(10)
        if loop == 0:
            robot.move_distance(30, 1, 0.001)
            state = STATE_1
        if loop == 1 or loop == 2:
            robot.move_distance(30, -1, 0.001)
            
            robot.turn_degree(100, 1)
            robot.turndetect()
            

            state = transit
        
            
        
        
    elif state == transit:
        robot.sensorfollow()
        if robot.cluetjek1():
            if loop == 1:
                robot.move_distance(20, 1, 0.001)
                state = State_4
            if loop == 2:
                robot.move_distance(25, 1, 0.001)
                robot.turn_degree(90, 1)
                
                state = state_3
                
                
    
    elif state == state_3:
        robot.sensorfollow()
        sen = robot.converted_sensorupdate()
        if sen[7] == "2":
            print ("right")
            robot.pickup_right()
            robot.move_distance(5, 1, speed=0.004)
            indivprogress = indivprogress+ 1
            if indivprogress == 2:
                
                robot.move_distance(10, -1, speed=0.004)
                robot.turn_degree(175, 1, speed=0.004)
                robot.move_distance(13, -1, speed=0.004)
                state = transit2
                
                
    
    
    elif state == State_4:
        if nextstate == False:
            sen = robot.converted_sensorupdate()
            robot.sensorfollow()
            headsearch()
        if nextstate:
            print("1")
            state = Home

    


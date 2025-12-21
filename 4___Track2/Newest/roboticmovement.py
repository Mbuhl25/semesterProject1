from drive_logistik import Drive
from steppermotor import StepperMotor
from machine import Pin
import math
from sensor import Sensor
from pcontrol import pController
from time import sleep
""" final"""

class Roboticmovements:
    def __init__(self):
        self.sensor1 = Sensor()

        # robot geometry
        self.wheel_circumference = 26.7
        self.wheelbase = 23.5
        self.distance_per_step = self.wheel_circumference / 400

        # motors
        self.leftmoter = StepperMotor([0,1,2,3])
        self.leftseq = self.leftmotor.half_step()
        self.rightmoter = StepperMotor([4,5,6,7])
        self.actoator = StepperMotor([12, 13, 14, 15])
        self.robot = Drive(self.leftmotor, self.rightmotor, self.actoator)

        # p-control
        self.pwm_procent = 0.3
        self.delay_val_1 = 0.0001
        self.pControl1 = pController()          

        self.acc_left = 0
        self.acc_right = 0

        self.new_step_left, self.new_step_right = self.pControl1.adjustStep(
            1.0, self.sensor1.runSensor()
        )

        # sensor
        self.converted_sen = []

        # other motors
        self.magnet = Pin(19, Pin.OUT)         
        

        self.weights = [0.72, 0.91, 0.86, 0.76, 0.93, 1.00, 0.53, 0.57]

    def SensorFollow(self):
        """
        Funktion: this funktion make the robot follow the black line
        
        Returns: A movement
        """ 
        self.new_step_right, self.new_step_left = self.pControl1.adjustStep(
            1.0, self.sensor1.runSensor()
        )
         # accumulate step changes
        self.acc_left += self.new_step_left 
        self.acc_right += self.new_step_right
        # LEFT wheel trigger
        if self.acc_left >= 1:
            self.robot.turnWheel(self.leftseq, "left", 0.00001, 1)
            self.acc_left -= 1
        # RIGHT wheel trigger
        if self.acc_right >= 1:
            self.robot.turnWheel(self.leftseq, "right", 0.00001, 1)
            self.acc_right -= 1

    def MoveDistance(self, cm, direction, speed=0.01):
        """
        Function: Moves the robot in a straight line for a given length.

        Param, float, cm: The distance to move.

        Param, float, speed: The lower the value, the faster the movement.

        Variable, int, number_of_steps: Calculated number of steps based on the distance in cm.

        Returns: A movement command.
        """
        number_of_steps = int(cm / self.distance_per_step)

        for i in range(number_of_steps):
            self.robot.turnWheel(self.leftseq, "left", speed, direction)
            self.robot.turnWheel(self.leftseq, "right", speed, direction)

        self.robot.stop()

    def TurnDegree(self, degree=90, direction=1, speed=0.01):
        """
        Function: Turns the robot by a given number of degrees.

        Param, float, degree:
        The number of degrees to turn.

        Param, float, speed:
        The lower the value, the faster the movement.

        Variable, float, turning_circumference:
        The calculated circumference around the wheels during a turn.

        Variable, float, full_turn_steps:
        The number of steps required for a full 360-degree turn.

        Variable, float, steps_per_degree:
        The number of steps required per degree of rotation.

        Returns:
        A movement command.
        """
         #calculate degrees to steps
        turning_circumference = 2 * math.pi * self.wheelbase
        full_turn_steps = turning_circumference / self.distance_per_step
        steps_turn_degree = abs(full_turn_steps * (degree / 360)) / 2

        for i in range(int(steps_turn_degree)):
            self.robot.turnWheel(self.leftseq, "left", speed, -direction)
            self.robot.turnWheel(self.leftseq, "right", speed, direction)

        self.robot.stop()

    def ConvertedSensorUpdate(self):
        """
        Function: Updates the sensors and returns a new refined list.

        Variable, list, sensorList:
        A list of raw LDR values with 7 elements.

        Variable, list, self.converted_sensorval:
        A list of refined LDR values with 7 elements, where the value is
        1 if the sensor detects white and 2 if it detects black.

        Returns:
        self.converted_sensorval
        """
        
        sensorList = self.sensor1.runSensor()
        self.converted_sen = self.BlackConvertor(sensorList)
        return self.converted_sen

    def BlackConvertor(self, sensorList, thedshoald=26000):
        """
        Function, that, converts raw LDR values to 1 or 2 depending on a threshold.

        Param, list, sensorList: A list of raw LDR values.

        Param, list, threshold: Controls when the value should be 1 (white) if under the threshold,
        or 2 (black) if over the threshold.

        Returns a list with 7 elements, each having a value of 1 or 2.
        """
        
        sensorList = [x * y for x, y in zip(sensorList, self.weights)]
        result = []
        for value in sensorList:
            if value < thedshoald:
                result.append("1")
            else:
                result.append("2")
        return result

    def TurnDetect(self, direction=1):
        """
        Function: Continuously turns until the line is detected again.

        Param, int, direction: 1 if the robot should turn one way to find the line, -1 if it should turn the other way.

        Returns: A movement command.
        """
        while True:
            self.ConvertedSensorUpdate()
            self.TurnDegree(1, direction, speed=0.004)

            if self.converted_sen[0] == "2":
                self.TurnDegree(25, 1)
                break

            if self.converted_sen[7] == "2":
                self.TurnDegree(25, -1, speed=0.004)
                break  

    def Pickup(self):
        """
        Makes the actuator move, turns on the magnet, retrieves the object,
        and drops it.

        Returns:
        A movement command.
        """
        self.robot.move_actuator(0.001, 1280,self.leftseq , -1)
        self.magnet(1)
        self.MagScan()
        self.robot.move_actuator(0.001, 1350,self.leftseq, 1)
        self.magnet(0)
        sleep(1)


    def PickupRight(self):
        """
        Aligns with and picks up the magnet if it is on the right side.

        Returns:
        A movement command.
        """
        self.MoveDistance(10, -1, speed=0.004)
        self.TurnDegree(175, 1, speed=0.004)
        self.MoveDistance(13, -1, speed=0.004)

        self.Pickup()

        self.MoveDistance(5, 1, speed=0.004)
        self.TurnDegree(140, 1, speed=0.004)
        self.TurnDetect()
        self.MoveDistance(10, 1, speed=0.004)

    def PickupLeft(self):
        """
        Aligns with and picks up the magnet if it is on the left side.

        Returns:
        A movement command.
        """
        
        self.MoveDistance(10, -1, speed=0.004)
        self.TurnDegree(170, -1, speed=0.004)
        self.MoveDistance(13, -1, speed=0.004)

        self.Pickup()

        self.MoveDistance(5, 1, speed=0.004)
        self.TurnDegree(140, -1, speed=0.004)
        self.TurnDetect(-1)
        self.MoveDistance(10, 1, speed=0.004)

    def MagScan(self, degrre=20, direction=1):
        """
        Param, int, degree:
        Controls how much range the wiggle movement covers.

        Returns:
        A movement command.
        """
        if direction == 1:
            for i in range(2):
                self.TurnDegree(degrre, -1)
                self.TurnDegree(degrre, 1)
                self.TurnDegree(degrre, -1)
                self.MoveDistance(2, 1)

        if direction == -1:
            for i in range(2):
                self.TurnDegree(degrre, 1)
                self.TurnDegree(degrre, -1)
                self.TurnDegree(degrre, 1)
                self.MoveDistance(2, -1)

    def Cluetjek1(self):
        """
        Checks for two black spaces on each side to compensate
        for the short sensor range.

        Returns:
        A movement command.
        """
        clueright = False
        clueleft = False

        for i in range(2):
            self.ConvertedSensorUpdate()

            if self.converted_sen[0] == "2":
                clueright = True
                self.TurnDegree(5, -1)

            if self.converted_sen[7] == "2":
                clueleft = True
                self.TurnDegree(5, 1)

            if clueleft and clueright:
                return True

        return False
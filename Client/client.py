################# IMPORTS #################
import socket, json, time, os
from tkinter import CURRENT
from turtle import left
import turtle

from numpy import tri
from SensorReading.CompassLib.i2c_hmc5883l import HMC5883
from SensorReading.infrared import Infrared
from SensorReading.ranger import Ranger
from MotorControl.motor_controller import Motor
from MotorControl.driver import Driver
import WifiTri.indoor_localization
import WifiTri.data_collect
import RPi.GPIO as GPIO
###########################################


################# CONSTANTS #################
TRIG1 = 23 # GPIO pins for front ranger
ECHO1 = 17
TRIG2 = 24 # GPIO pins for back ranger
ECHO2 = 27
TRIG3 = 5 # GPIO pins for right side ranger
ECHO3 = 7
TRIG4 = 6 # GPIO pins for left side ranger
ECHO4 = 8
IR_FRONT = 15 # GPIO pins for front and back Infrared
IR_BACK = 25
IN1 = 16 # GPIO pins for control of right motor
IN2 = 20
IN3 = 10 # GPIO pins for control of left motor
IN4 = 9
ADDRESS = "172.20.3.95" # Address and port number of UDP server
PORT = 44444
START_HEADING = (180, 190, 210)
A_HEADING = (-1, 0, 0)
B_HEADING = (0, -1, 0)
C_HEADING = (0, 0, -1)
CURRENT_LOC = 'start'
#############################################


################# GLOBAL VARIABLES #################
command_queue = [] # Queue of voice commands
tableA = dict() # Fingerprint table at location A
tableB = dict() # Fingerprint table at location B
tableC = dict() # Fingerprint table at location C
rangerF = Ranger(TRIG1, ECHO1) # Front ranger object
rangerB = Ranger(TRIG2, ECHO2) # Back ranger object
rangerR = Ranger(TRIG3, ECHO3) # Right ranger object
rangerL = Ranger(TRIG4, ECHO4) # Left ranger object
infraredF = Infrared(IR_FRONT) # Front infrared object
infraredB = Infrared(IR_BACK) # Back infrared object
compass = HMC5883(gauss=4)  # Electronic compass object
rightMotor = Motor(IN2, IN1) # Right motor object
leftMotor = Motor(IN3, IN4) # Left motor object
driver = Driver(rightMotor, leftMotor) # driver object
####################################################

def get_command():
    # Handles the commands received from Google API
    dir = "/home/pi/VCAvoidanceCar/Client/data"
    name = "request.json"
    path = os.path.join(dir, name)
    f = open(path, '+')
    request = json.loads(f.read())
    if request["valid"] == True:
        cmd = (request['trigger'].lower(), request['direction'].lower(), request['amount'])
        command_queue.append(cmd)
        request["valid"] = False
        f.write(json.dumps(request))
    else: return None

def is_at_Location(location, signature):
    # Returns True if car is within threshold range of given location, False elsewise
    if location == "A":
        table = tableA
        common_keys = set(tableA.keys()) & set(signature.keys())
    elif location == "B":
        table = tableB
        common_keys = set(tableB.keys()) & set(signature.keys())
    elif location == "C":
        table = tableC
        common_keys = set(tableC.keys()) & set(signature.keys())

    dist = WifiTri.indoor_localization.subtract_all_signatures(table, signature, common_keys)
    norm = WifiTri.indoor_localization.l2norm(dist)
    if(norm <= 5): return True
    else: return False

def orient(current, destination):
    num = 0 # default case
    if destination == 'A': num = 0  
    elif destination == 'B': num = 1
    elif destination == 'C': num = 2
    
    if current == 'start': 
        right_lim = START_HEADING[num] + 5
        left_lim = START_HEADING[num] - 5
    elif current == 'A':
        right_lim = A_HEADING[num] + 5
        left_lim = A_HEADING[num] - 5
    elif current == 'B':
        right_lim = B_HEADING[num] + 5
        left_lim = B_HEADING[num] - 5
    elif current == 'C':
        right_lim = C_HEADING[num] + 5
        left_lim = C_HEADING[num] - 5    

    if right_lim > 359: right_lim -= 360
    if left_lim < 0: left_lim += 360
    while True:
        driver.turnRight()
        if left_lim < compass_reading < right_lim:
            driver.stop()
            break
        driver.stop()
        compass_reading = compass.get_heading()[0]
    
def avoidObstacle():
    # Get original direction
    originalDir = driver.getMovement()
    driver.stop()
    # Determine best way to turn based on side sensors
    turnDir = rangerL.isMax(rangerR)
    originalTurn = 'right' # default case 
    # Left turn case
    if turnDir:
        originalTurn = 'left'
        driver.turnLeft()
        if originalDir == 'forward':
            while rangerR.getDist() < 50:
                driver.forward()
        else:
            while rangerL.getDist() < 50:
                driver.forward()
    # Right turn case
    else:
        driver.turnRight()
        if originalDir == 'forward':
            while rangerL.getDist() < 50:
                driver.forward()
        else:
            while rangerR.getDist() < 50:
                driver.forward()
    # After obstacle not visible, turn to original direction             
    if originalTurn == 'right':
        driver.turnLeft()
    else:
        driver.turnRight()
    if originalDir == 'forward':
        driver.forward()
    else:
        driver.backward()

def send_packet(port, ip, msg):
    """
    Send packet to server containing message
    """
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        
        sock.send(msg.encode())

        ack = sock.recv(1024).decode()
        print("Server ACKed packet")
        if(ack != "acked"): print("Server dropped packet")

    except ConnectionRefusedError:
        print("Connection refused. Server program not running.")
        return False
    finally:
        sock.close()
        return True

def system_init():
    GPIO.setmode(GPIO.BCM) # Set GPIO numbering scheme to Broadcom
    GPIO.setwarnings(False) # Disable GPIO warnings
    
    # Setup all sensors and motors
    rangerF.setup()
    rangerB.setup()
    rangerR.setup()
    rangerL.setup()
    infraredF.setup()
    infraredB.setup()
    compass.set_declination(-13, 67)
    rightMotor.setup()
    leftMotor.setup()  
    driver.setup()
    return

if __name__ == "__main__":

    fA = open("a_table.json")
    fB = open("b_table.json")
    fC = open("c_table.json")
    tableA = json.loads(fA.read())
    tableB = json.loads(fB.read())
    tableC = json.loads(fC.read())
    fA.close()
    fB.close()
    fC.close()

    system_init()

    while True:
        get_command()
        if(len(command_queue) == 0): continue # no commands to execute

        cmd = command_queue.pop(0) # pop first command in the queue

        trig = cmd[0]
        dir = cmd[1]
        amt = cmd[2]

        if trig == 'go':
            send_packet(PORT, ADDRESS, "Recieved Command\nStarting Navigation to Location {} from {}".format(dir, CURRENT_LOC))
            orient(CURRENT_LOC, dir)
            signature = dict()
            arrived = False
            driver.forward()
            while arrived == False:
                if rangerF.getDist() < 30: avoidObstacle()
                signature = WifiTri.data_collect.do_scan(signature)
                arrived = is_at_Location(dir, signature)
            driver.stop()
            CURRENT_LOC = dir
            continue

        elif trig == 'drive':
            send_packet(PORT, ADDRESS, "Recieved Command\nBegin driving {} for {} seconds".format(dir, amt))
            if dir == 'forward':
                starttime = time.time()
                totaltime = 0
                endtime = amt
                driver.forward()
                while rangerF.getDist() > 30 or totaltime <= endtime:
                    totaltime = time.time() - starttime
                driver.stop()
                if rangerF.getDist() < 30:
                    send_packet(PORT, ADDRESS, "Obstacle Detected {:.1f} cm away, stopping movement".format())
                    continue
                
                
            elif dir == 'backward':
                starttime = time.time()
                totaltime = 0
                endtime = amt
                driver.backward()
                while rangerB.getDist() > 30 or totaltime <= endtime:
                    totaltime = time.time() - starttime
                driver.stop()
                if rangerB.getDist() < 30:
                    send_packet(PORT, ADDRESS, "Obstacle Detected {:.1f} cm away, stopping movement".format())
                    continue
            send_packet(PORT, ADDRESS, "Completed driving {} for {} seconds".format())
        
        elif trig == 'turn':
            send_packet(PORT, ADDRESS, "Executing {} turn".format(dir))
            driver.turn90(dir, compass)
            send_packet(PORT, ADDRESS, "Turned {}, vehicle oriented facing {} degrees".format(dir, compass.get_heading()[0]))
            continue
    
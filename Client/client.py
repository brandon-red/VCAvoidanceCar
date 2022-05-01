################# IMPORTS #################
import socket
import json
import time
from Client.WifiTri.indoor_localization import NUM_LOCATIONS
from SensorReading.CompassLib.i2c_hmc5883l import HMC5883
from SensorReading.infrared import Infrared
from SensorReading.ranger import Ranger
from MotorControl.motor_controller import Motor
from MotorControl.driver import Driver
import WifiTri.indoor_localization
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
ADDRESS = "127.0.0.1" # Address and port number of UDP server
PORT = 44444
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
    f = open("data/requests.json")
    request = json.loads(f.read())
    if request["Valid"] == "True":
        command_queue.append(request["words"])
        request["Valid"] = "False"
        f.write(json.dumps(request))
    else: return None

def interpret_command():

    pass

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

def avoidObstacle():
    pass

def send_packet(port, ip):
    """
    called every ~20ms
    """
    try:
        print("Trying to connect to %s:%d" % (ip, port))
        sock = socket.socket()
        sock.connect((ip, port))
        
        packet = getSensors()

        packet_json = json.dumps(packet)
        sock.send(packet_json.encode())

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
    #setup all sensors and motors
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

def getSensors():
    readings = {
            'IR': [infraredF.getProximity(), infraredF.getProximity()],
            'compass': compass.get_heading(),
            'ranger': [rangerF.getDist(), rangerB.getDist(), rangerR.getDist(), rangerL.getDist()]
        }
    return readings


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
        ret = interpret_command(cmd) # Interpret what to do from the list of words

    # Call get_command() -> opens json file updated by google home and adds commands to the queue if a new request was made
    # Pop command from queue and interpret the command
    
    # compass.get_heading() used to get the measurement of compass it returns a tuple (degrees, minutes)

    
    

    # Main Loop



import socket
import json
import time
from SensorReading.CompassLib import Compass
from SensorReading.infrared import Infrared
from SensorReading.ranger import Ranger
from MotorControl.motor_controller import Motor
from MotorControl.driver import Driver
import RPi.GPIO as GPIO

"""
- initialize list of commands
- will be appended to after receiving command from Google API
- will pop as commands are executed
"""
command_queue = []

valid_commands = {"go forward", "go backward", "turn left", 
    "turn right", "go to A", "go to B", "go to C"}

# Front Ranger Pin Setup
TRIG1 = 23 
ECHO1 = 17

# Back Ranger Pin Setup
TRIG2 = 24
ECHO2 = 27

# Right Ranger Pin Setup
TRIG3 = 5
ECHO3 = 7

# Left Ranger Pin Setup
TRIG4 = 6
ECHO4 = 8

# IR Setup

IR_FRONT = 15
IR_BACK = 25

# Motor 1 Setup

IN1 = 16
IN2 = 20

# Motor 2 Setup

IN3 = 10
IN4 = 9

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

port = 44444
port = "127.0.0.1"

def get_command():
    """
    handles the commands received from Google API
    """
    f = open("data/requests.json", "rw")
    requests = json.loads(f)
    if requests["Valid"] == "True":
        command_queue.append(requests["words"])
        requests["Valid"] = "False"
        updated = json.dumps(requests)
        f.write(updated)
    else:
        return "No new command"

def send_packet(port, ip):
    """
    called every ~20ms
    """
    try:
        print("Trying to connect to %s:%d" % (ip, port))
        sock = socket.socket()
        sock.connect((ip, port))

        front_range = rangerF.measureDistance()
        back_range = rangerB.measureDistance()
        right_range = rangerR.measureDistance()
        left_range = rangerL.measureDistance()
        front_proximity = infraredF.getProximity()
        back_proximity = infraredB.getProximity()
        direction = compassObj.getPosition()

        packet = {
            'IR': [front_proximity, back_proximity],
            'compass': direction,
            'ranger': [front_range, back_range, right_range, left_range]
        }

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
    
if __name__ == "__main__":
    rangerF = Ranger(TRIG1, ECHO1)
    rangerF.setup()

    rangerB = Ranger(TRIG2, ECHO2)
    rangerB.setup()

    rangerR = Ranger(TRIG3, ECHO3)
    rangerR.setup()
    
    rangerL = Ranger(TRIG4, ECHO4)
    rangerL.setup()

    infraredF = Infrared(IR_FRONT)
    infraredF.setup()

    infraredB = Infrared(IR_BACK)
    infraredB.setup()

    compassObj = Compass()
    compassObj.setup()

    rightMotor = Motor(IN2, IN1)
    rightMotor.setup()

    leftMotor = Motor(IN3, IN4)
    leftMotor.setup()  

    driver = Driver(rightMotor, leftMotor)
    driver.setup()

    # Main Loop



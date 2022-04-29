import socket
import json
import time
from MotorControl.motor_controller import Motor
from SensorReading.compass import Compass
from SensorReading.infrared import Infrared
from SensorReading.ranger import Ranger
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
ENA = 12

# Motor 2 Setup

IN3 = 10
IN4 = 9
ENB = 13

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
        front_proximity = infraredF.measureDistance()
        back_proximity = infraredB.measureDistance()
        direction = compass_obj.getPosition()

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

    compass_obj = Compass()
    compass_obj.setup()

    right = Motor(IN1, IN2, ENA)
    left =  Motor(IN3, IN4, ENB)
    
    while True:
        x = input()
        
        if x == 'f':
            print("right motor")
            right.forward()
            print("left motor")
            left.forward()
        
        elif x == 'b':
            print("right motor")
            right.backward()
            print("left motor")
            left.backward()

        elif x == 's':
            print("right motor")
            right.stop()
            print("left motor")
            left.stop()

        elif x == 'r':
            print("right motor")
            right.backward()
            print("left motor")
            left.forward()
        
        elif x == 'l':
            print("right motor")
            right.forward()
            print("left motor")
            left.backward()
        elif x=='e':
            GPIO.cleanup()
            break
        
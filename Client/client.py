import socket
import json
import time
from SensorReading.compass import Compass
from SensorReading.encoder import Encoder
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

# Compass Setup

""" Unsure what sensor to use """ 

# IR Setup

IR_FRONT = 15
IR_BACK = 25

# Encoder Setup
"""
Might not use
"""
CLK = 23
DT = 24

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
        position = encoder_obj.getPosition(0)
        front_proximity = infraredF.measureDistance()
        back_proximity = infraredB.measureDistance()
        direction = compass_obj.getPosition()

        packet = {
            'encoder': position,
            'IR': [front_proximity, back_proximity],
            'compass': direction,
            'ranger': [front_range, back_range]
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

    encoder_obj = Encoder(CLK, DT)
    encoder_obj.setup()

    infraredF = Infrared(IR_FRONT)
    infraredF.setup()

    infraredB = Infrared(IR_BACK)
    infraredB.setup()

    compass_obj = Compass()
    compass_obj.setup()

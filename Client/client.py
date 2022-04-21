"""
Client program


How To Run
------------

python3 Client.py -p <a port number> [-s server ip]

E.g. 
python3 Client.py -p 1234 -s 192.168.1.10       # connect server at 192.168.1.10 port 1234
python3 Client.py -p 1234 -s raspberrypi.local  # connect server at raspberrypi.local port 1234
python3 Client.py -p 1234                       # connect server at 127.0.0.1 port 1234

"""

import socket
import json
import time
from Client.SensorReading.compass import Compass
from Client.SensorReading.encoder import Encoder
from Client.SensorReading.infrared import Infrared
from Client.SensorReading.ranger import Ranger
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
TRIG1 = 16 
ECHO1 = 11

# Back Ranger Pin Setup
TRIG2 = 18
ECHO2 = 13

# Compass Setup

""" Unsure what sensor to use """ 

# IR Setup

IR_DATA1 = 15

IR_DATA2 = 22

# Encoder Setup
"""
Might not use
"""
CLK = 23
DT = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

rangerF = Ranger(TRIG1, ECHO1)
rangerF.setup()

rangerB = Ranger(TRIG2, ECHO2)
rangerB.setup()

encoder_obj = Encoder(CLK, DT)
encoder_obj.setup()

infraredF = Infrared(IR_DATA1)
infraredF.setup()

infraredB = Infrared(IR_DATA2)
infraredB.setup()

compass_obj = Compass()
compass_obj.setup()

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
        if(ack is not "acked"): print("Server dropped packet")

    except ConnectionRefusedError:
        print("Connection refused. Server program not running.")
        return False
    finally:
        sock.close()
        return True
    
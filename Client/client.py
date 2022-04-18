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

import encoder
import compass
import infrared
import ranger


port = 44444
port = "127.0.0.1"

def send_packet(port, ip):
    try:
        print("Trying to connect to %s:%d" % (ip, port))
        sock = socket.socket()
        sock.connect((ip, port))

        range = ranger.read()
        position = encoder.read(0)
        proximity = infrared.read()
        direction = compass.read()

        packet = {
            'encoder': position,
            'IR': proximity,
            'compass': direction,
            'ranger': range
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
    
from socket import *
import argparse
import json



parser = argparse.ArgumentParser(description='Server program')
parser.add_argument("-p", "--port", type=int, \
                    help="port of the server to connect", required=True)
args = parser.parse_args() 
port = args.port # get the ip and port of the server

try:
        
    sock = socket()
    sock.bind(('', port))
    print("="*30)
    print("Sever listening on", port)
    print("="*30)


    while True:
        connection, address = sock.accept()
        print("Message from", connection)
        packet_json = connection.recv().decode()
        packet = json.loads(packet_json)
        # packet is a json with entries from 4 different sensors
        encoder = packet['encoder']
        infrared = packet['IR']
        compass = packet['compass']
        range = packet['ranger']

        print("New sensor update received")
        print("Ranger measurement:", range)
        print("Infrared sensor detected:", infrared)
        print("Position of car:", encoder)
        print("Current direction of the car:", compass)
except ConnectionRefusedError:
    print("Connection refused. Server program not running.")
finally:
    print("Socket released")



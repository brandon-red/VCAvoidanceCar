import socket
import argparse
import json



parser = argparse.ArgumentParser(description='Server program')
parser.add_argument("-p", "--port", type=int, \
                    help="port of the server to connect", required=True)
args = parser.parse_args() 
port = args.port # get the ip and port of the server

try:
    sock = socket.socket()
    sock.bind(('', port))
    sock.listen(10) 
    print("="*30)
    print("Sever listening on", port)
    print("="*30)

    while True:
        connection, address = sock.accept()
        print("Message from", address)
        packet_json = connection.recv(1024).decode()
        packet = json.loads(packet_json)
        # packet is a json with entries from 4 different sensors
        encoder = packet['encoder']
        infrared = packet['IR']
        compass = packet['compass']
        range = packet['ranger']
        message = packet['message']
        
        print(message)
        print("New sensor update received")
        print("Front Ranger measurement:", range[0])
        print("Back Ranger measurement:", range[1])
        print("Infrared sensor detected:", infrared[0])
        print("Infrared sensor detected:", infrared[1])
        print("Position of car:", encoder)
        print("Current direction of the car:", compass)

        msg = "acked"
        connection.send(msg.encode())                              

except ConnectionRefusedError:
    print("Connection refused. Server program not running.")
finally:
    print("Socket released")



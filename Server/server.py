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
        message = connection.recv(1024).decode()

        print(message)

        msg = "acked"
        connection.send(msg.encode())                              

except ConnectionRefusedError:
    print("Connection refused. Server program not running.")
finally:
    print("Socket released")



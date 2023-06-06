import cv2
import depthai as dai
import numpy as np
import sys
import json
import socket, pickle, struct
import time
import json_numpy


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 6666
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)

client_socket, addr = server_socket.accept()
print('Got Connection from:', addr)


if client_socket:
    while True:
        cmd = client_socket.recv(1024)
        if not cmd:
            break

        try:
            d_rcv = json.loads(cmd)
        except Exception:
            print("Receive Error")

        c_key = d_rcv.get("key")

        if(c_key == "Start"):
            print("\nStarting")
            arr = cv2.imread('img2.jpg')
            nw = time.time()
            alst = arr.tolist()
            print(time.time()-nw)
            encoded_arr = json_numpy.dumps({'mydata': alst})

        if(c_key == "TakeSnapShot"):
            try:
                print("\nSending data")
                message = (encoded_arr + '\n').encode()
                print(sys.getsizeof(message), len(message))
                client_socket.sendall(message)
            except:
                print('Error!!')
                client_socket.close()
                sys.exit()

        if(c_key == "Stop"):
            print("\nStoping")
            break

client_socket.close()
print("Server Closed")

import socket, cv2, pickle, struct
import json
import sys
import numpy as np
import json_numpy
import time
import select

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.181.1'
port = 6666
client_socket.connect((host_ip, port))


str_cmd = { "key":"Start" }
str_msg = json.dumps(str_cmd)
img_cmd = { "key":"TakeSnapShot" }
img_msg = json.dumps(img_cmd)
stp_cmd = { "key":"Stop" }
stp_msg = json.dumps(stp_cmd)


print("Start")
message = str_msg.encode()
client_socket.sendall(message)
time.sleep(2)

print("Get Image")
message = img_msg.encode()
client_socket.sendall(message)
time.sleep(0.1)

data = b""
while len(data)<7251561:
    # print(sys.getsizeof(packet))
    packet = client_socket.recv(65536) #4*1024 #16384
    if not packet:
        break
    data+=packet
    print(len(data))

arr = data.decode()
decoded_arr = json.loads(arr)
dd = decoded_arr.get("mydata")
cv2.imwrite("decoded.jpg", np.asarray(dd))

print("\nStop")
message = stp_msg.encode()
client_socket.sendall(message)

client_socket.close()
print("Client Closed")



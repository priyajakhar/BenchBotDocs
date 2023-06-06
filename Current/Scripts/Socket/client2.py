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
img_cmd = { "key":"Preview" }
img_msg = json.dumps(img_cmd)
img_scmd = { "key":"StopPreview" }
img_smsg = json.dumps(img_scmd)
stp_cmd = { "key":"Stop" }
stp_msg = json.dumps(stp_cmd)


print("Start")
message = str_msg.encode()
client_socket.sendall(message)
time.sleep(5)

print("Get Image")
message = img_msg.encode()
client_socket.sendall(message)
time.sleep(5)


for i in range(5):
    t = time.time()
    data = b""
    while len(data) < 65536*21 + 1: #1441793:
        packet = client_socket.recv(65536) #4*1024 #16384
        data+=packet

    print(len(data))
    arr = data.decode()
    decoded_arr = json.loads(arr)
    dd = decoded_arr["data"]["pixels"] #.get("mydata") 
    cv2.imwrite(f"preview/decoded_{t}.jpg", np.asarray(dd))

time.sleep(10)

# time.sleep(30)
print("\nStop Camera")
message = img_smsg.encode()
client_socket.sendall(message)
time.sleep(5)

print("\nStop")
message = stp_msg.encode()
client_socket.sendall(message)

time.sleep(1)
client_socket.close()
print("Client Closed")



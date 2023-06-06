import socket, cv2, pickle, struct
import json
import sys
import numpy as np
import json_numpy
import time
import select

host_ip = '192.168.181.1'
port = 6666

# for starting up the camera on server side
str_cmd = { "key":"Start" }
str_msg = json.dumps(str_cmd)
# for getting a preview frame from camera
img_cmd = { "key":"Preview" }
img_msg = json.dumps(img_cmd)
# for getting a set of images (1 RGB + 2 Mono + 1 Depth)
snap_cmd = { "key":"TakeSnapshot" }
snap_msg = json.dumps(snap_cmd)
# for stopping the camera on server side
img_scmd = { "key":"StopPreview" }
img_smsg = json.dumps(img_scmd)
# for closing the client connection to the server
stp_cmd = { "key":"Close" }
stp_msg = json.dumps(stp_cmd)


for i in range(1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_ip, port))

    # start preview
    print("\nStart")
    message = str_msg.encode()
    client_socket.sendall(message)
    time.sleep(5)

    # preview messages
    message = img_msg.encode()
    j = time.time()
    #for j in range(5):
    while(time.time()-j < 2):
        client_socket.sendall(message)
        t = time.time()
        # get length of message
        data = b""
        data = client_socket.recv(10) #4*1024 #16384
        l = int( data.decode() )
        #print(l, type(l))
        # get actual frame
        data = b""
        while len(data) < l: #1441793:
            packet = client_socket.recv(1024*1000) #4*1024 #16384
            data += packet

        #print(len(data))
        arr = data.decode()
        decoded_arr = json.loads(arr)
        dd = decoded_arr["data"]["pixels"] #.get("mydata") 
        cv2.imwrite(f"preview/prv_{t}.jpg", np.asarray(dd))
        #cv2.imshow("feed", np.asarray(dd, dtype=np.uint8))


    # ask for a snapshot
    print("Get image set")
    message = snap_msg.encode()
    client_socket.sendall(message)
    t = time.time()

    data = b""
    l = 10
    for i in range(4):
        print(i)

        while len(data) < l:
            packet = client_socket.recv(1024)
            if not packet:	break
            data += packet
        
        
        if i==0:
            msg_size = json.loads(data[:l].decode())
            data = data[l:]
        else:
            msg_size = json.loads(data[:l].decode())
            data = data[l:]
        ln = int(msg_size)
        #print(l)
        
        while len(data) < ln:
            data += client_socket.recv(1024*4000)
            #print(len(data))
        decoded_arr = json.loads(data[:ln].decode())
        data = data[ln:]
    
        dd = decoded_arr["data"]["pixels"]
    
        #print("Saving")
        if (decoded_arr["type"]=="RGB"):
            #img = np.asarray(dd, dtype=np.int8) 
            img = np.array(dd).astype(np.int8)
            im = cv2.imdecode(img, cv2.IMREAD_COLOR)
            print(type(img), len(img), np.shape(img), img[5:15], np.shape(im))
            cv2.imwrite(f"preview/rgb_{t}.png", im)
        if (decoded_arr["type"]=="MonoLeft"):
            cv2.imwrite(f"preview/left_{t}.jpg", np.asarray(dd))
        if (decoded_arr["type"]=="MonoRight"):
            cv2.imwrite(f"preview/right_{t}.jpg", np.asarray(dd))
        if (decoded_arr["type"]=="Depth"):
            cv2.imwrite(f"preview/Depth_{t}.png", np.asarray(dd))

















    # stop preview
    print("\nStop Camera")
    message = img_smsg.encode()
    client_socket.sendall(message)
    time.sleep(5)


    # closing connection
    print("Close")
    message = stp_msg.encode()
    client_socket.sendall(message)
    time.sleep(1)
    client_socket.close()
    print("Client Closed")



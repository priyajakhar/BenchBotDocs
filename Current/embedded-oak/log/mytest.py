import os
from datetime import datetime
from pathlib import Path
from from_root import from_root, from_here
import csv
import cv2
import json
import numpy as np
import time
import re

import logger, sys

import tarfile



# image = cv2.imread("Image.jpg")
# st = time.time()
# for z in range(2):
    # logger.log_image(z+1, image, "Rgb", [35.773713, -78.672968], True)
# et = time.time()

# print(et-st)

# img_log_dir = from_here("images_log")
# img_archive = img_log_dir / "images.tar.gz"
# with tarfile.open(name=img_archive, mode='r') as imgtar:
    # imgtar.list()

# 




    
import random

list1 = ['Connected', 'NotConnected', 'Connected', 'NotConnected']
for j in range(1):
    for i in range(4):
        logger.log_camera_status(i+1, random.choice(list1))
# logger.system_status_cameras()



sys.exit()











img_log_dir = from_here("images_log")
cam_log_dir = from_here("camera_log")
'''
    added functionality for not updating status of cameras if they were not recently used
'''
def system_status_cameras():
    camera_dict = {'Timestamp': None, 'Connected': [], 'NotConnected': []}
    json_files = [cam_json for cam_json in os.listdir(cam_log_dir) if cam_json.endswith('.json')]
    json_files.sort()
    t_stamps = np.array([])
    
    for cam_file in json_files:
        with open(cam_log_dir / cam_file) as json_file:
            data = json.load(json_file)
            
            t_obj = datetime.strptime(data['Timestamp'], '%Y/%m/%d %H:%M:%S')
            unix_t = datetime.timestamp(t_obj)
            t_stamps = np.append(t_stamps, unix_t)
            
            if data['Status'] == 'Connected':
                camera_dict['Connected'].append(data['Camera_ID'])
            else:
                camera_dict['NotConnected'].append(data['Camera_ID'])
    camera_dict['Timestamp'] = datetime.utcnow()
    camera_dict['Connected'], camera_dict['NotConnected'] = filter_lists(t_stamps, camera_dict['Connected'], camera_dict['NotConnected'])

    print("----- Current System Status -----")
    print("Connected Cameras:", camera_dict['Connected'])
    print("Disconnected Cameras:", camera_dict['NotConnected'])

    
def filter_lists(t_list, a_list, b_list):
    # filter out camera if they were not used in last 1 minute of camera with latest timestamp of usage
    latest = np.max(t_list)
    result = np.where(t_list<=(latest-60))
    indices = list(result[0])

    for idx in indices:
        idx += 1
        if idx in a_list:
            a_list.remove(idx)
        elif idx in b_list:
            b_list.remove(idx)
    return a_list, b_list
    
system_status_cameras()



'''
find specific camera status update by comparing the last status log and the current one
arguments: latest list of connected and disconneted cameras
'''
def find_diff(new_c, new_nc):
    new_c = np.array(new_c)
    new_nc = np.array(new_nc)
    # read last logged status
    try:
        with open(cam_status_file, 'r') as f:
            last_log = f.readlines()[-1]
    except:
        lstc = np.setdiff1d(new_c, [])
        lstnc = np.setdiff1d(new_nc, [])
        return lstc, lstnc
    # convert from string to list format
    res = []
    for part in last_log.split('['):
        if part.find(']')>=0:
            lst = re.findall('[0-9]', part)
            res.append(lst)
    last_c = np.array([int(i) for i in res[0]])
    last_nc = np.array([int(i) for i in res[1]])
    # find differences in the lists
    lstc = np.setdiff1d(new_c, last_c)
    lstnc = np.setdiff1d(new_nc, last_nc)
    return lstc, lstnc
    
    
'''
add list of all connected and disconneted cameras in the system in a single log file
also log explicit differences/updates in status
'''
def system_status_cameras():
    conn_cams = []
    disconn_cams = []
    cam_files = [file for file in os.listdir(cam_log_dir) if file.endswith('.log') and file.startswith('cam')]
    cam_files.sort()
    for cam_file in cam_files:
        with open(cam_log_dir / cam_file) as f:
            last_log = f.readlines()[-1]
            data = last_log.split()
            cam_id = int( re.findall('[0-9]', cam_file)[0] )
            if data[1] == 'Connected':
                conn_cams.append(cam_id)
            else:
                disconn_cams.append(cam_id)
    log_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    c_list, nc_list = find_diff(conn_cams, disconn_cams)
    upd = ''
    for idx in c_list:
        upd = f"Camera {idx} connected"
    for idx in nc_list:
        upd = f"Camera {idx} disconnected"
    with open(cam_status_file, 'a') as fp:
        status = f"[{log_time}] {upd} Connected: {conn_cams} NotConnected: {disconn_cams}\n"
        fp.write(status)
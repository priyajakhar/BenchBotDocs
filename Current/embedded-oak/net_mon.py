#!/usr/bin/env python3

import time
import psutil

def net_monitor():
    old_value = 0

    # io = psutil.net_io_counters()
    # bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
    # print(io, bytes_sent, bytes_recv)

    strtime = time.time()
    
    while time.time()-strtime < 10:
        new_value =  psutil.net_io_counters().bytes_recv # + psutil.net_io_counters().bytes_sent
        if old_value:
            send_stat(new_value - old_value)
        old_value = new_value
        time.sleep(1)


def convert_to_mbit(value):
    return value/1024./1024.*8

def send_stat(value):
    print ("%0.3f" % convert_to_mbit(value), "at", time.time())
    
net_monitor()


import sys
sys.exit()


'''
    Another way of doing things
'''
def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

UPDATE_DELAY = 1
        
while True:
    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the stats again
    io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    # print the total download/upload along with current speeds
    print(f"Upload: {get_size(io_2.bytes_sent)}   "
          f", Download: {get_size(io_2.bytes_recv)}   "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
    # update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
    

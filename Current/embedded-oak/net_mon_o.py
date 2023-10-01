import psutil
import time
import numpy as np

UPDATE_DELAY = 1

def get_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

start_time = time.time()
bw_util = np.array([])

while (time.time()-start_time) < 40:
    # sleep for `UPDATE_DELAY` seconds
    time.sleep(UPDATE_DELAY)
    # get the stats again
    io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    
    print(f"Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ")

    # update the bytes_sent and bytes_recv for next iteration
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv

    bw_util = np.append(bw_util, ds)


print("\nAvg:", get_size(np.mean(bw_util)), "Min:", get_size(np.min(bw_util)), "Max:", get_size(np.max(bw_util)))
print("\n")





# leonos = device.getLeonCssCpuUsage().average
# leonrt = device.getLeonMssCpuUsage().average
# print( round(leonos*100, 2), round(leonrt*100, 2) )
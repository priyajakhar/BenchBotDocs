import os
import time
from multiprocessing import Process

def do_sum(pid):
	start = time.time()
	print("Internal", pid)
	sum = 0
	for num in range(100):
		time.sleep(0.1)
		sum += num
		#print(pid)
	print(sum, "of", pid, time.time()-start)


if __name__ == '__main__':
	for idx in range(2):
		commd = "python3 test2.py "+str(idx)+" &"
		#print(commd)
		#os.system(commd)
		p = Process(target=do_sum, args=(idx,))
		p.start()
		p.join
		
	print("Done")
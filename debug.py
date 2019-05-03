import sys
import os
import time

if __name__ == '__main__':
	while(True):
		if(os.stat("reqs.txt").st_size != 0):
			file=open("reqs.txt")
			lines=file.readlines();
			os.system(lines[0])
			os.system("rm reqs.txt; touch reqs.txt")
			file.close()
		else:
			print("-----")
		time.sleep(3)

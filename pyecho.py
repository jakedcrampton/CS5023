import sys
import os

if __name__ == '__main__':
	file=open("reqs.txt", "w")
	file.write(sys.argv[1])
	file.close()
	#os.system("echo \""+sys.argv[1]+"\" > reqs.txt")

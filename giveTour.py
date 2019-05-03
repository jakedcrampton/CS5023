'''
Final Project CS 4023/5023
Jake Crampton, Kalen Smith, Jackson Pollard

Edit the list of points to be relative to your map, and edit the details in each project as such
'''
# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script
import sys
import os
import math
#############
# Helper Methods  #
#############
def getPosition():
	file=open("position.txt")
	lines=file.readlines()
	x=float(lines[-4].partition("[")[2].partition(",")[0])
	y=float(lines[-4].partition("[")[2].partition(",")[2].partition(",")[0])
	file.close()
	return {'x': x, 'y' : y}

def dist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

#returns current distance to passed in point
def close(x,y):
	curPos=getPosition()

	return dist(curPos['x'],curPos['y'],x,y)

def goToPosition(project):
	# while loop the locomotion until arrival then do the talk script
	while (close(project.x,project.y)>3):
		#print (curPos)
		os.system("python go_to_specific_point_on_map.py "+str(project.x)+" "+str(project.y))
	f=open(project.script,"r")
	f1=f.readlines()
	for x in f1:
			os.system("python saySomething.py \""+x[:-1]+"\"")
#############
# Helper Classes    #
#############

#this class keeps data for each location
class project:
	def __init__(self,name,x,y,script):
		self.name=name
		self.x=x
		self.y=y
		self.script=script
	def getCoordinates():
		return {'x': self.x, 'y' : self.y}
	def getName():
		return self.name
	def getScript():
		self.script

if __name__ == '__main__':
	#change this for your map and tour points
	projects = [project("rocket",-1.98,-8.15,"rocket.txt"),project("racecar",-1.21,-1.42,"racecar.txt"),project("uav",6.69,-0.51,"uav.txt"),project("buggy",12.22,-0.52,"buggy.txt"),project("rover",19.33,-10.9,"rover.txt")]
	command = sys.argv[1]
	#check the type of tour to give
	if(command=="fullTour"):
		for p in projects:
			goToPosition(p)
	if(command=="buggy"):
		for p in projects:
			if(p.name==command):
				goToPosition(p)
	if(command=="uav"):
		for p in projects:
			if(p.name==command):
				goToPosition(p)
	if(command=="racecar"):
		for p in projects:
			if(p.name==command):
				goToPosition(p)
	if(command=="rover"):
		for p in projects:
			if(p.name==command):
				goToPosition(p)
	if(command=="rocket"):
		for p in projects:
			if(p.name==command):
				goToPosition(p)
	if(command=="goToNearest"):
		small=project("tmp",0,0,"tmp")
		closest=99999
		for p in projects:
			if(close(p.x,p.y)<closest):
				small=p
				closest=close(p.x,p.y)
		goToPosition(small)

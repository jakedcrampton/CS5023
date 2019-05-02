#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script
import sys
import os
#############
# Helper Methods  #
#############
def getPosition():
	lines=open("position.txt").readlines()
	x=float(lines[-4].partition("[")[2].partition(",")[0])
	y=float(lines[-4].partition("[")[2].partition(",")[2])
	return {'x': x, 'y' : y}
def dist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
def goToPosition(project):
	curPos=getPosition()
	while (dist(curPos['x'],curPos['y'],project.x,project.y)>1):
		os.system("python go_to_specific_point_on_map.py "+str(project.x)+" "+str(project.y))
	f=open(project.script,"r")
	f1=f.readlines()
	for x in f1:
			os.system("python saySomething.py \""+x[:-1]+"\"")
#############
# Helper Classes    #
#############
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

	projects = [project("rocket",-1.98,-8.15,"rocket.txt"),project("racecar",-1.21,-1.42,"racecar.txt"),project("uav",6.69,-0.51,"uav.txt"),project("buggy",12.22,-0.52,"buggy.txt"),project("rover",19.33,-10.9,"rover.txt")]
	command = sys.argv[1]
	if(command=="fullTour"):
		for p in projects:
			goToPosition(p)

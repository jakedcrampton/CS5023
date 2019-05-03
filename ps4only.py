##################################################################################
## Note: we took our project script from a project that used ps4 control
## and made it to where it now only does ps4 control
## you control it with d pad
##################################################################################


################################################################################
## Title: Project1.py
## Authors: Jake Crampton, Kalen Smith, Jackson Pollard

## Description: This python script runs on an active Turtlebot gazebo
## simulation. It follows the following behavior hierarchy, from most
## to least important:
##  1) Halt on bumper collision
##  2) Accept Movement Commands
##  3) Escape Symmetric obstacles within 1ft
##  4) Avoid Asymmetric Obstacles within 1 ft
##  5) Turn Randomly within +-15 deg ebvery 1 ft
##  6) Drive forward
################################################################################

##******************************************************************************
## Imports and Variables
##******************************************************************************
#!/usr/bin/env pyth on
import roslib
import time
import rospy
import random
import math
import sys
import thread

# import the PS3 and PS4 controller support
# must be installed. Instructions at https://pypi.org/project/inputs/
from inputs import get_gamepad

#import messages
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from sensor_msgs.msg import LaserScan

##******************************************************************************
## Variables
##******************************************************************************
# Variables to handle general movement
default_speed = 0.15
default_turn_speed = 0.5

# Threshold distance for turning due to laser input. 0.3 m ~~ 1f
# NOTE: this is distance from the kinect, which is at the back of the robot
turnThreshold=0.65

#This is which direction laser says we should move.
turnDirection = 0

# Variables to handle the bump sensor
bumpHappened = False

#variables to handle Controller input
isMovePressed=0
isTurnPressed=0

##******************************************************************************
## Helper Methods
##******************************************************************************

# set movement to forward using default speed
def moveForward(movement):
	movement.linear.x = default_speed
	movement.linear.y = 0
	movement.linear.z = 0
	movement.angular.x = 0
	movement.angular.y = 0
	movement.angular.z = 0

#set movement to turn in a given direction (-1 or 1) with default speed
def turn(movement,dir):
	movement.linear.x = 0
	movement.linear.y = 0
	movement.linear.z = 0
	movement.angular.x = 0
	movement.angular.y = 0
	movement.angular.z = dir*default_turn_speed

#setmovement to a custom Vx and Vth (Vtheta)
def customMove(movement,Vx,Vth):
	movement.linear.x = Vx
	movement.linear.y = 0
	movement.linear.z = 0
	movement.angular.x = 0
	movement.angular.y = 0
	movement.angular.z = Vth

#Print the current mode, but only if it is new
def printMode(str,modes):
	modes[0]=str
	if modes[1]!=modes[0]:
		print "Mode: "+modes[0]
	modes[1]=modes[0]
	return modes

##******************************************************************************
## Methods corresponding to overarching rules
##******************************************************************************

##---------------------------------------
## RULE 1: Halt on Bump
##---------------------------------------
# This is the function to be passed to the bump subscriber
def bumpHandler(data):
	#Global so main can see it
	global bumpHappened
	if (data.state == BumperEvent.PRESSED):
		bumpHappened = True
	else:
		bumpHappened = False

##---------------------------------------
## RULE 2: Let Human Control
##---------------------------------------

# Function to run controller input grabbing
# NOTE: put this in a thread
def updateControllers():

	# the global variable saying if user has given a turn command
	# -1 for left, +1 for right
	global isTurnPressed
	# the global variable saying if user has given a move command
	# -1 for back, +1 for forward
	global isMovePressed
	#this is a THREAD, so loop infinite
	while 1:
		#When you unplug the controller or dont start with one, it errors
		try:
			# This gets the most recent events. Events are lost after a certain
			# time in the controller buffer, which is why this needs to be threaded.
			# Without threading, it wouldn't see the event because it wouldn't
			# check often enough.
			events = get_gamepad()

			# check the d-pad events by their name
			# In a separate script, print event.code,event.state for all events
			# to figure out the names and magnitudes for pressing buttons
			for event in events:

				#PS4 Controller
				if event.code=="ABS_HAT0X" :
					isTurnPressed=int(event.state)
				elif event.code=="ABS_HAT0Y":
					isMovePressed=int(event.state)*-1

				## PS3 Controller
				elif event.code=="BTN_DPAD_UP":
					isMovePressed=int(event.state)
				elif event.code=="BTN_DPAD_LEFT":
					isTurnPressed=int(event.state)*-1
				elif event.code=="BTN_DPAD_RIGHT":
					isTurnPressed=int(event.state)
				elif event.code=="BTN_DPAD_DOWN":
					isMovePressed=int(event.state)*-1
		except:
			pass

#Let the human drive
def humanDrive(movement,pub):
	customMove(movement,isMovePressed*0.39,isTurnPressed*-1)
	pub.publish(movement)

##---------------------------------------
## RULE 3 & 4: Escape
##---------------------------------------

# Use laser data to determine if turn is necessary
def laserHandler(laserData):
	# 0: Nothing in Way
	# 1: Thing on right, turn left
	# 2: Things everywhere, turn around
	# 3: Thing on left, turn right
	global turnDirection

	# the minDist's are the minimum distance in laserData.ranges in each of the
	# left, middle, and right third. We'll use these to determine symmetric vs
	# asymmetric and when to turn
	minDistLeft = 1.0
	minDistMid = 1.0
	minDistRight = 1.0

	# laserData.ranges is a list of all the distances the kinect sees, in order
	# from RIGHT to LEFT
	numDataPoints = len(laserData.ranges)

	# Calculate the smallest distance in the left third, middle third, and right third
	for p_i in range(0, numDataPoints):
		# if it's in our range to consider
		if 0.01 < laserData.ranges[p_i] < 1.00:

			# 0<x<1/3 => right third
			if 0 < p_i < 1.0/3.0*numDataPoints:
				minDistRight = min(minDistRight, laserData.ranges[p_i])

			# 1/3<x<2/3 => middle third
			if 1.0/3.0*numDataPoints < p_i < 2.0/3.0*numDataPoints:
				minDistMid = min(minDistMid, laserData.ranges[p_i])

			# 2/3<x<1 => left Third
			if 2.0/3.0*numDataPoints < p_i < numDataPoints:
				minDistLeft = min(minDistLeft, laserData.ranges[p_i])

	# Decide turn Direction
	# NOTE: Case only mid < threshold is asymmetric, so we'll choose turn right arbitrarily

	# right and left less than threshold is symmetric
	if minDistLeft < turnThreshold and minDistRight < turnThreshold:
		turnDirection = 2
	# none under threshold is straight
	elif minDistLeft > turnThreshold and minDistMid > turnThreshold and minDistRight > turnThreshold :
		turnDirection = 0
	#only right is under or only mid is under => turn left
	elif minDistLeft > minDistRight or ((not minDistLeft < turnThreshold) and minDistMid < turnThreshold and  (not minDistRight < turnThreshold)):
		turnDirection = 1
	# only left is under => turn right
	elif minDistLeft < minDistRight:
		turnDirection = 3

##---------------------------------------
## RULE 5: Turn Randomly
##---------------------------------------

# Turn to a random angle between lw and high IN RADIANS
# For rule 5, this should be between -15 and 15 DEGREES
def turnRand(lw,high,movement,pub):
	t0 = rospy.Time.now().to_sec()
	current_angle = 0
	#angle between 0 and 15 degrees in radians
	angle = float(random.randrange(int(1000*lw),int(1000*high)))/1000
	if angle<0:
		dir = -1.0
	else:
		dir = 1.0
	while(current_angle < abs(angle)):
		turn(movement,dir)
		#Publish the velocity
	    	pub.publish(movement)
	    	#Takes actual time to velocity calculus
	    	t1=rospy.Time.now().to_sec()
	    	#Calculates distancePoseStamped
	    	current_angle= default_turn_speed*(t1-t0)

##---------------------------------------
## RULE 6: Go Forward
##---------------------------------------

# Go a certian distance.
# For Rule 6, this should be small so it is still sensitive
def goDistance(dist,movement,pub):
	t0 = rospy.Time.now().to_sec()
	current_distance = 0

	#Loop to move the turtle in an specified distance
	while(current_distance < dist):
		moveForward(movement)
		#Publish the velocity
	    	pub.publish(movement)
	    	#Takes actual time to velocity calculus
	    	t1=rospy.Time.now().to_sec()
	    	#Calculates distancePoseStamped
	    	current_distance= default_speed*(t1-t0)

##******************************************************************************
## Main
##******************************************************************************
def main():
	# First create the Controller Input Thread
	try:
		thread.start_new_thread( updateControllers, ())
	except:
		print "failed to start thread"
	print "finished creating humanInputThread"

	# Make the publisher to velocity
	pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size = 10)
	# Subscribe to bumper and laser (scan)
	rospy.Subscriber('mobile_base/events/bumper', BumperEvent, bumpHandler)
	rospy.Subscriber('/scan', LaserScan, laserHandler)
	# dAnK mEmEs tImE
	rospy.init_node('tUrTlEbOT')

	# the condensed variables from the sensors
	global bumpHappened
	global turnDirection

	# contains [currentMode, lastMode]. We need memory so that we only print when it switches.
	modes =["", ""]

	# standard Twist object
	movement= Twist()

	# measure distance as a function of speed and time so that you know when to turn
	lstTurnTime=rospy.Time.now().to_sec();

	#loop the mode chack and execution
	while not rospy.is_shutdown():

		# bumpHappened == true when it get de bump
		if bumpHappened==True:
			modes=printMode("Halt on Bump",modes)
			break

		#check for if a human commands the bot to do something
		elif isTurnPressed != 0 or isMovePressed !=0:
			modes=printMode("User Input",modes)
			humanDrive(movement,pub)

		# turnDirection == 2 => symmetric object, turn around
		#elif turnDirection == 2:
		#	modes=printMode("Escape Symmetric",modes)
		#	turnRand(2.617,3.663,movement,pub)

		# turnDirection == 2 or 3 => asymmetric object, turn a bit, loop until no flag
		#elif turnDirection == 1:
		#	modes=printMode("Avoid Asymmetric",modes)
		#	turnRand(0.6,1.4,movement,pub)
		#elif turnDirection == 3:
		#	modes=printMode("Avoid Asymmetric",modes)
		#	turnRand(-1.4,-0.6,movement,pub)

		# turnDirection == 0 => go sraight & turn every ft
		#elif turnDirection == 0:
		#	modes=printMode("MoveForward",modes)
		#	goDistance(0.015,movement,pub)
		#	# turn when you've gone a foot
		#	if rospy.Time.now().to_sec()-lstTurnTime > 0.4/default_speed:
		#		modes=printMode("Turn every ~1 ft",modes)
		#		lstTurnTime=rospy.Time.now().to_sec()
		#		#-15 to 15 deg
		#		turnRand(-0.262,0.262,movement,pub)


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass

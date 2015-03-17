# ------------------------------------------------------------------------
# driveMain.py
# ------------------------------------------------------------------------
#
#  Alan Li written on March 17, 2015
# 
#  Waffle Revengeance
#
# ------------------------------------------------------------------------

from .ev3dev import LegoSensor, Motor

#Sensor Init
colorL = ColorSensor(0)
colorR = ColorSensor(1)
gyro = ColorSensor(2)
ultrasonic = ColorSensor(3)

#MotorInit



driveState = 0 	#driveState variable
				#0 is get next instruction
				#1 is turn left
				#2 is go forward
				#3 is turn right
				#4 is park

#Method to turn left
def turnLeft():

#Method to turn right
def turnRight():

#Method to continue going forward
def goStraight():

#Method to stop at the redline for some time and then continue
def redLine():

#Method to park the robot
def park():

#Method to maintain the current drive state
def main(instructions):
	while(len(instructions) != 0):
		if(driveState == 0):
			driveState = instructions.pop(0)
		elif(driveState == 1):
			redLine()
			turnLeft()
			driveState = 0
		elif(driveState == 2):
			redLine()
			goStraight()
			driveState = 0
		elif(driveState == 3):
			redLine()
			turnRight()
			driveState = 0
		elif(driveState == 4):
			park()
			driveState = 0

nodePath = [0,0,0,1,1,0,1,0,1,0,0,4,1,0,1,1,0,0,1,4,1,0,1,1,1,1,1,1,0,4] #List of instructions
main(nodePath)
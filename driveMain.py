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
import time

#Sensor Init
colorL = ColorSensor(port=0)
colorR = ColorSensor(port=1)
gyro = ColorSensor(port=2)
ultrasonic = ColorSensor(port=3)

#MotorInit
def init_motor(motor):
	print ("Initializing motor")
	motor.reset()
	motor.run_mode = 'forever'
	motor.stop_mode = Motor.STOP_MODE.BRAKE
	motor.regulation_mode = True
	motor.pulses_per_second_sp = 0
	motor.start()
	print ("Motor Initialized")
	return;

a = Motor(port=Motor.PORT.A)
b = Motor(port=Motor.PORT.B)
c = Motor(port=Motor.PORT.C)
init_motor(a)
init_motor(b)
init_motor(c)
a.pulses_per_second_sp = 2000
b.pulses_per_second_sp = 2000
c.pulses_per_second_sp = 2000
time.sleep(5)
a.pulses_per_second_sp = 0
b.pulses_per_second_sp = 0
c.pulses_per_second_sp = 0
defaultSpeed = 1000

driveState = 0 	#driveState variable
				#-1 is get next instruction
				#0 is turn left
				#1 is go forward
				#2 is turn right
				#3 is park

				

#Method to get Sensor Readings
def getSensor():
	output = [0 for x in range(4)]
	#output[0] = colorL.getValue()
	#output[1] = colorR.getValue()
	output[0] = colorL.color()
	output[1] = colorR.color()
	output[2] = gyro.ang_and_rate()
	output[3] = ultrasonic.dist_in()
	return output

def getColorL():
	return colorL.rgb()

def getColorR():
	return colorR.rgb()

def getGyro():
	return gyro.ang()

def getUS():
	return ultrasonic.dist_in()

#Method to turn
def pointTurn(angle):
	gyroStartAngle = gyro.ang()
	gyroCurrentAngle = gyroStartAngle
	while(abs(gyroCurrentAngle - gyroStartAngle) == angle):
		gyroCurrentAngle = gyro.ang()
		if(angle > 0):
			a.run_forever(defaultSpeed)
			b.run_forever(-defaultSpeed)
		else:
			a.run_forever(-defaultSpeed)
			b.run_forever(defaultSpeed)
	a.stop()
	b.stop()


#Method to drive forward
def driveFoward(speed):
	a.run_forever(speed)
	b.run_forever(speed)

#Method to drive a certain distance
def driveForwardDist(speed, dist):
	a.run_position_limited(dist, speed)
	b.run_position_limited(dist, speed)

def driveCorrection():
	if(colorL.color == 'white'):
		speed = b.pulses_per_second_sp
		motor.pulses_per_second_sp = speed*9.0/10.0
	elif(colorR.color == 'white'):
		speed = a.pulses_per_second_sp
		motor.pulses_per_second_sp = speed*9.0/10.0
	if(colorL.color != 'white' and colorR.color != 'white')
		driveForward(defaultSpeed)

#Method to transition
def redLineStraighten():
	if(colorL.color == 'red'):
		a.stop()
		while(colorR.color() != 'red'):
			b.run_forever(defaultSpeed)
		b.stop()
	elif(colorR.color == 'red'):
		b.stop()
		while(colorR.color() != 'red'):
			a.run_forever(defaultSpeed)
		a.stop()
	time.sleep(1)

def atRedLine()
	if(colorL.color == 'red' or colorR.color == 'red'):
		return True

def park():


#Method to maintain the current drive state
def main(instructions):
	instruct = instructions.pop(0)
	driveForward(defaultSpeed)
	driveState = 1;
	while(len(instructions) != 0):
		sensorInput = getSensor()
		if(driveState == 0):					#Red Line state
			redLineStraighten()
			driveForwardDist(defaultSpeed, 20)
			pointTurn(instruct)
			driveState = 1
		if(driveState == 1):					#Drive down lane state
			driveCorrection()
		if(driveState == 2):					#Park Lane state 		!!!!
		if(driveState == 3):					#Exit Lane state 		!!!!


		if(atRedLine())
			instruct = instructions.pop(0)
			if(instruct == 'P'):
				driveState = 2
			if(instruct == 'E'):
				driveState = 3
			else:
			driveState = 0;


				#0: at a node
					#pause
					#straighten up
						#both sensors are read
				#1: transition nodes
					#read instruction
					#follow instruction
				#2: drive to node
					#drive forward
						#stay on road



#		if(driveState == -1):
#			driveState = instructions.pop(0)
#		elif(driveState == 0):
#			redLine()
#			turnLeft()
#			driveState = -1
#		elif(driveState == 1):
#			redLine()
#			goStraight()
#			driveState = -1
#		elif(driveState == 2):
#			redLine()
#			turnRight()
#			driveState = -1
#		elif(driveState == 3):
#			park()
#			driveState = -1

nodePath = [-90,-90,-90,0,0,-90,0,-90,0,-90,-90,'P',0,0,0,0,0,0,0,-90,'P',-90,0,0,0,-90,0,'P',0,-90,-90,0,0,-90,0,'E'] #List of instructions
main(nodePath)
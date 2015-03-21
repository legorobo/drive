# ------------------------------------------------------------------------
# driveMain.py
# ------------------------------------------------------------------------
#
#  Alan Li written on March 17, 2015
#
#  Waffle Revengeance
#
# ------------------------------------------------------------------------

from ev3.lego import LegoSensor, Motor, ColorSensor, GyroSensor, UltrasonicSensor
import time

#Sensor Init
colorL = ColorSensor(port=2)
colorR = ColorSensor(port=1)
colors = (None, 'black', 'blue', 'green',
              'yellow', 'red', 'white', 'brown')

gyro = GyroSensor(port=3)
ultrasonic = UltrasonicSensor(port=4)
global USAngle
USAngle = 0
global USDist
USDist = 2515			#Absolute amount to turn US 360 degrees
global twentyCM
twentyCM = 360

#MotorInit
def init_motor(motor):
	print("Initializing motor")
	motor.reset()
	motor.run_mode = 'forever'
	motor.stop_mode = Motor.STOP_MODE.BRAKE
	motor.regulation_mode = True
	motor.pulses_per_second_sp = 0
	motor.start()
	print("Motor Initialized")
	return;

a = Motor(port=Motor.PORT.B)
b = Motor(port=Motor.PORT.A)
c = Motor(port=Motor.PORT.C)
init_motor(a)
init_motor(b)
init_motor(c)
defaultSpeed = 1000

global driveState
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
	output[0] = colorL.color
	output[1] = colorR.color
	output[2] = gyro.ang_and_rate
	output[3] = ultrasonic.dist_in
	return output

def getColorL():
	return colorL.rgb

def getColorR():
	return colorR.rgb

def getColorLRaw():
    return colorL.ref_raw()

def getColorRRaw():
    return colorR.ref_raw()

def getGyro():
	return gyro.ang

def getUS():
	return ultrasonic.dist_in

#Method to turn
def pointTurn(angle):
	if(angle == 90):
		driveForwardMotorDist(a,defaultSpeed,180)
		driveForwardMotorDist(b,defaultSpeed,-180)
	if(angle == -90):
		driveForwardMotorDist(a,defaultSpeed,-180)
		driveForwardMotorDist(b,defaultSpeed,180)
#	gyroStartAngle = gyro.ang
#	gyroCurrentAngle = gyroStartAngle
#	while (abs(gyroCurrentAngle - gyroStartAngle) == angle):
#		gyroCurrentAngle = gyro.ang
#		if (angle > 0):
#			a.run_forever(defaultSpeed)
#			b.run_forever(-defaultSpeed)
#		else:
#			a.run_forever(-defaultSpeed)
#			b.run_forever(defaultSpeed)
#	a.stop()
#	b.stop()


#Method to drive forward
def driveFoward(speed):
	a.run_forever(speed)
	b.run_forever(speed)

def driveForwardMotorDist(motor,speed, dist):
	aDist = motor.position_sp + dist
	motor.run_position_limited(aDist, speed)

#Method to drive a certain distance
def driveForwardDist(speed, dist):
	aDist = a.position_sp + dist
	bDist = b.position_sp + dist
	a.run_position_limited(aDist, speed)
	b.run_position_limited(bDist, speed)

def driveCorrection():
	if (colors[colorL.color] == 'white'):
		speed = b.pulses_per_second_sp
		b.pulses_per_second_sp = speed * 0.9
	elif (colors[colorR.color] == 'white'):
		speed = a.pulses_per_second_sp
		a.pulses_per_second_sp = speed * 0.9
	if (colors[colorL.color] != 'white' and colors[colorR.color] != 'white'):
		driveForward(defaultSpeed)

#Method to transition
def redLineStraighten():
	if (colors[colorL.color] == 'red'):
		a.stop()
		while (colors[colorR.color] != 'red'):
			b.run_forever(defaultSpeed)
		b.stop()
	elif (colors[colorR.color] == 'red'):
		b.stop()
		while (colors[colorR.color] != 'red'):
			a.run_forever(defaultSpeed)
		a.stop()
	time.sleep(1)

def atRedLine():
	if (colors[colorL.color] == 'red' or colors[colorR.color] == 'red'):
		return True

def checkCollision():
	initialUSAngle = USAngle
	resetUSToZero()
	turnUS(135)
	for i in range(7):
		turnUS(-15 * (i))
		if (ultrasonic.dist_in <= 120):
			return True;
	return False


def hugWallR(color):
	if (colors[colorR.color] == 'black'):
		speedL = a.pulses_per_second_sp
		if (speedL * 1.05 <= defaultSpeed):
			a.pulses_per_second_sp = speedL * 1.1
		speedR = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedR * 0.95
	if (colors[colorR.color] == color or colors[colorR.color] == 'yellow'):
		speedR = b.pulses_per_second_sp
		if (speedR * 1.05 <= defaultSpeed):
			b.pulses_per_second_sp = speedR * 1.05
		speedL = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedL * 0.95

def hugWallL(color):
	if (colors[colorL.color] == 'black'):
		speedR = a.pulses_per_second_sp
		if (speedR * 1.05 <= defaultSpeed):
			a.pulses_per_second_sp = speedR * 1.1
		speedL = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedL * 0.95
	if (colors[colorL.color] == color or colors[colorR.color] == 'yellow'):
		speedL = b.pulses_per_second_sp
		if (speedL * 1.05 <= defaultSpeed):
			b.pulses_per_second_sp = speedL * 1.05
		speedR = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedR * 0.95

def findPark():
	hugWallR('white')

	if (colors[colorR.color] == 'blue'):
		a.stop()
		b.stop()
		time.sleep(4)
	canParked = scanPark()
	driveForward(defaultSpeed)
	while (canParked == False):
		if (colors[colorR.color] == 'white'):
			canParked = scanPark()
		hugWallR('blue')
	a.stop()
	b.stop()
	park()
	return 1

def turnUS(angle):
	c.run_position_limited((angle/360.0) * USDist, 1000)
	USAngle += angle
	if (USAngle < 0):
		USAngle += 360
	elif (USAngle > 360):
		USAngle -= 360

def resetUSToZero():
	if (USAngle != 0):
		if (USAngle > 180):
			turnUS(-(360-USAngle))
		else:
			turnUS(360-USAngle)

def scanPark():
	for i in range(6):
		turnUS(-15 * (i + 1))
		if (ultrasonic.dist_in >= 100):
			return True;
	return False

def park():
	while (colors[colorL.color] != 'blue'):
		b.run_forever(defaultSpeed)
	b.stop()
	driveForwardDist(defaultSpeed, 0.85*twentyCM)
	time.sleep(4)
	driveForwardDist(defaultSpeed, -0.85*twentyCM)
	pointTurn(-90)

def exit():
	hugWallL('white')
	if (colors[colorL.color] == 'red'):
		a.stop()
		b.stop()
		while (colors[colorR.color] != 'red'):
			b.run_forever(defaultSpeed)
		b.stop()
		driveForwardDist(1000, 0.85*twentyCM)
		sys.exit(0);

#Method to maintain the current drive state
def main(instructions):
	instruct = instructions.pop(0)
	driveForward(defaultSpeed)
	driveState = 1;
	while (len(instructions) != 0):
		if (instructions.get(0) == 'P'):
			instructions.pop(0)
			driveState = 2
		if (instructions.get(0) == 'E'):
			instructions.pop(0)
			driveState = 3
		if (driveState == 0):					#Red Line state
			redLineStraighten()
			rightOfWay = checkCollision()
			if (rightOfWay):
				driveForwardDist(defaultSpeed, twentyCM)
				pointTurn(instruct)
				driveState = 1
		if (driveState == 1):					#Drive down lane state
			driveCorrection()
		if (driveState == 2):					#Park Lane state 		!!!!
			driveState = findPark()
		if (driveState == 3):					#Exit Lane state 		!!!!
			exit()


		if (atRedLine()):
			instruct = instructions.pop(0)
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

def calibrateMotors():
	driveForwardDist(1000,360)

def calibrateUS():
	turnUS(360)

turnUS(90)
#nodePath = [-90,-90,0,'P',-90,0,0,0,0,-90,-90,90,'P',0,0,0,90,'P',0,0,-90,0,'E'] #List of instructions
#main(nodePath)
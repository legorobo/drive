from ev3.ev3dev import Motor
import time

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
init_motor(a)
init_motor(b)
a.pulses_per_second_sp = 2000
b.pulses_per_second_sp = 2000
time.sleep(5)
a.pulses_per_second_sp = 0
b.pulses_per_second_sp = 0;



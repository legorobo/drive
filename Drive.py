# ------------------------------------------------------------------------
# Drive.py
# ------------------------------------------------------------------------
#
#  Alan Li written on March 17, 2015
# 
#  Waffle Revengeance
#
# ------------------------------------------------------------------------


from .ev3dev import Motor
import time


class Drive(object):

    """
    This object implements the drive system using the unicycle drive model. Instead of
    thinking of the velocities of each wheel separately, we consider a single linear
    velocity and an angular velocity
    """


    WHEEL_RADIUS = 0.063 # meters
    WHEELBASE_LENGTH = 0.6969 # meters (also not accurate)

    LEFT_MOTOR = Motor.PORT.A
    RIGHT_MOTOR = Motor.PORT.B


    def __init__(self):

        """
        Basic constructor
        """

        self.left_motor = Motor(port = LEFT_MOTOR)
        self.right_motor = Motor(port = RIGHT_MOTOR)
        self.v = 0
        self.omega = 0

    @property
    def v(self):
        return self.v

    @property
    def omega(self):
        return self.omega


# ------------------------------------------------------------------------

    def drive_left_motor(v, time):

        """
        A function that runs the left motor using linear velocity. Allows for limited
        time intervals (seconds).

        TODO: Test the functionality
        """

        if time == -1:
            self.left_motor.run_forever(v)
        else:
            self.left_motor.run_time_limited(time, v)

    def drive_right_motor(v, time):

        """
        A function that runs the right motor using linear velocity. Allos for limited
        time intervals (seconds).

        TODO: Test the functionality
        """

        if time == -1:
            self.right_motor.run_forever(v)
        else:
            self.right_motor.run_time_limited(time, v)

    def drive_left_motor_dist(v, dist):

        """
        Drives the left motor a set number of rotations.

        TODO: Determine the units in run position limited
        """

        self.left_motor.run_position_limited(dist, v)

    def drive_right_motor_dist(v, dist):

        """
        Drives the right motor a set number of rotations
        """

        self.right_motor.run_position_limited(dist, v)

# ------------------------------------------------------------------------

    def drive(v, omega, time = -1):

        """
        Our drive operates on a unicycle system. We define the motion of our robot by its
        linear velocity and angular velocity. This is easily converted to linear velocities
        for both motors.

        TODO: Test this
        """

        self.v = v
        self.omega = omega

        v_left = ( (2.0 * v) - (omega * L) ) / (2.0 * R)
        v_right = ( (2.0 * v) + (omega * L) ) / (2.0 * R)

        self.drive_left_motor(v_left, time)
        self.drive_right_motor(v_right, time)

    def drive_dist(v, omega, linear_dist, angular_dist):

        """
        Drives the robot to a coordinate expressed by delta theta and delta l. 
        
        TODO: Implement
        """

        self.v = v
        self.omega = omega

        # basically do a point turn and then yeah

        self.v = 0
        self.omega = 0



    def stop():

        """
        Stops the drive train and resets the motors
        """

        drive(0, 0)

        self.left_motor.reset()
        self.right_motor.reset()

# ------------------------------------------------------------------------

    def init_motor(motor):

        """
        Initializes the behavior of a given motor
        """

        motor.reset()

        motor.run_mode = 'forever'
        motor.stop_mode = Motor.STOP_MODE.BRAKE
        motor.regulation_mode = True
        motor.pulses_per_second_sp = 0
        
        motor.start()


# ------------------------------------------------------------------------
# Sensor.py
# ------------------------------------------------------------------------
#
#  Antares Chen written on March 17, 2015
# 
#  Waffle Revengeance
#
# ------------------------------------------------------------------------


from .ev3.lego import ColorSensor, GyroSensor, UltrasonicSensor
from .ev3dev import Motor


class SensorsArray(object):

    """
    A class for managing the robot's array of sensors. The below are constants for 
    each sensor's port number.
    """


    COLOR_SENSOR_LEFT = 0
    COLOR_SENSOR_RIGHT = 1
    GYRO_SENSOR = 2
    ULTRASONIC_SENSOR = 3

    ULTRASONIC_MOTOR = Motor.PORT.C


    def __init__(self, calibrated_colors):

        """
        Basic constructor. Note that calibrated colors should be a dictionary mapping
        color to RAW indicator.
        """

        self.left_color = ColorSensor(port = COLOR_SENSOR_LEFT)
        self.right_color = ColorSensor(port = COLOR_SENSOR_RIGHT)
        self.gyro = GyroSensor(port = GYRO_SENSOR)
        self.ultrasonic = UltrasonicSensor(port = ULTRASONIC_SENSOR)
        self.ultrasonic_motor = Motor(port = ULTRASONIC_MOTOR)

        self.calibrated_colors = calibrated_colors

# ------------------------------------------------------------------------

    def get_left_color(self):
        
        """
        Returns the RGB reading on the left color sensor
        """

        return self.left_color.ref_raw()

    def get_right_color(self):

        """
        Returns the RGB reading on the right color sensor
        """

        return self.right_color.ref_raw()

    def get_calibrated_left_color(self):
        
        """
        We only need WHITE (1), YELLOW (2), RED (3), BLUE (4), GREEN (5), GRAY 
        (6), BLACK (7).
        """

        raw_color = self.left_color.ref_raw()

        color = -1
        delta = float("inf")

        for key in calibrated_colors.keys():
            delta_0 = (calibrated_colors[key][0] - raw_color[0]) ^ 2 + (calibrated_colors[key][1] - raw_color[1]) ^ 2
            if delta_0 < delta:
                delta = delta_0
                color = key
        return key




    def get_calibrated_right_color(self):
        
        """
        We only need WHITE (1), YELLOW (2), RED (3), BLUE (4), GREEN (5), GRAY 
        (6), BLACK (7).
        """

        raw_color = self.right_color.ref_raw()

        color = -1
        delta = float("inf")

        for key in calibrated_colors.keys():
            delta_0 = (calibrated_colors[key][0] - raw_color[0]) ^ 2 + (calibrated_colors[key][1] - raw_color[1]) ^ 2
            if delta_0 < delta:
                delta = delta_0
                color = key
        return key


# ------------------------------------------------------------------------

    def get_angle(self):

        """
        Returns the angle reading off the gyroscope
        """

        return self.gyro.ang()

    def get_rate(self):

        """
        Returns the angle reading off the gyroscope
        """

        return self.gyro.rate()

    def gyro_reset(self):

        """
        Resets the gyro
        """

        del(self.gyro)
        self.gyro = GyroSensor(port = GYRO_SENSOR)

# ------------------------------------------------------------------------

    def get_distance(self):

        """
        Returns the distance read by the ultrasonic sensor in meters
        """

        return (float)self.ultrasonic.dist_cm() / 100

    def rotate_ultrasonic(theta):

        """
        Rotates the ultrasonic sensor to the desired theta

        TODO: Implement
        """

        gear_ratio = 9001 / 10 # That's not right least to say. 

        # TODO implement










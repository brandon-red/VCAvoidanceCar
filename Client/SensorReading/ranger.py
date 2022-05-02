######################################################################################
            # Raspberry Pi source code for reading from ultrasonic ranger #
# Should be structured as a function that can be called from main and other processes #
                    # Look at encoder.py as a template example #
######################################################################################

import RPi.GPIO as GPIO
import time

class Ranger:
    def __init__(self, TRIG_pin, ECHO_pin):
        self.TRIG_pin = TRIG_pin
        self.ECHO_pin = ECHO_pin
        self.isInit = False
        self.SOUND_SPEED = 34300 # cm/sec
    
    def setup(self):
        GPIO.setup(self.TRIG_pin, GPIO.OUT)
        GPIO.setup(self.ECHO_pin, GPIO.IN)
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.TRIG_pin, False)
        time.sleep(0.080) 
        print("sensor is ready")
        self.isInit = True
    
    def getInit(self):
        return self.isInit

    def getDist(self):
        if not self.isInit:
            self.setup()

        # send a 10usec gate signal to Trig
        GPIO.output(self.TRIG_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_pin, False)

        # when the wave is sent, ECHO reads 1
        pulse_start = time.time()
        while GPIO.input(self.ECHO_pin) == 0:
            pulse_start = time.time()

        # when the wave is heard, ECHO reads 0
        pulse_end = time.time()
        while GPIO.input(self.ECHO_pin) == 1:
            pulse_end = time.time()

        pulse_travel_time = pulse_end - pulse_start
        distance = pulse_travel_time * self.SOUND_SPEED / 2 # in unit cm
        time.sleep(0.080)
        return distance

    def isMax(self, other):
        """
        returns True if the current ranger's distance measurement
        is greater than the other ranger's, False otherwise

        will be used in Obstacle Avoidance algorithm
        """
        if not self.isInit:
            self.setup()
        if not other.getInit():
            other.setup()
        dist1 = self.getDist()
        dist2 = other.getDist()

        return dist1 > dist2
        
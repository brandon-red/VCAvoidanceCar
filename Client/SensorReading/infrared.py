######################################################################################
        # Raspberry Pi source code for reading from an Infrared Sensor #
    # Structured as a function that can be called from main and other processes #
######################################################################################

import RPi.GPIO as GPIO
import time

class Infrared:
    def __init__(self, DATA_pin):
        self.DATA_pin = DATA_pin
        self.isInit = False

    def setup(self):
        GPIO.setup(self.DATA_pin, GPIO.IN)
        GPIO.setmode(GPIO.BCM)
        time.sleep(0.080) 
        print('sensor is ready')
        self.isInit = True

    def getProximity(self):
        """
        return 1 if doesn't see ground
        return 0 for normal operation
        """
        if self.isInit == False:
            self.setup()
        proximity = GPIO.input(self.DATA_pin)
        return proximity
######################################################################################
                # Raspberry Pi source code for sensing infrared #
# Should be structured as a function that can be called from main and other processes #
                # Look at encoder.py as a template example #
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
        self.isInit = True

    def measureDistance(self):
        if self.isInit == False:
            self.setup()

        # decide what measurement should signal an alert
        return
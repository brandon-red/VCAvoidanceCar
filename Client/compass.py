######################################################################################
                # Raspberry Pi source code for sensing electronic compass #
# Should be structured as a function that can be called from main and other processes #
                # Look at encoder.py as a template example #
######################################################################################

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def read():
    #
    #GPIO.setup(, GPIO.IN)  # Physical pin n as an input
    #GPIO.setup(17, GPIO.IN) # set a port/pin as an input

    return


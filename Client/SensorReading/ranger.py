######################################################################################
                # Raspberry Pi source code for sensing ultrasonic ranger #
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
    
        GPIO.output(self.TRIG_pin, False)
        time.sleep(0.080) 
        print("sensor is ready")
        self.isInit = True

    def measureDistance(self):
        if self.isInit == False:
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
         
######################################################################################
                # Raspberry Pi source code for controlling a motor #
   # Structured as a function that can be called from main and other processes #
                        # To be used in the driver class #
######################################################################################

import RPi.GPIO as GPIO
import time

LOW = GPIO.LOW
HIGH = GPIO.HIGH

class Motor:
    def __init__(self, IN1, IN2):
        self.IN1 = IN1
        self.IN2 = IN2
        self.isInit = False
    
    def setup(self):
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, LOW)
        self.isInit = True
    
    def forward(self):
        """
        sets motor to run forward
        """
        if not self.isInit:
            self.setup()
        GPIO.output(self.IN1, HIGH)
        GPIO.output(self.IN2, LOW)
        print("moving forward")
    
    def backward(self):
        """
        sets motor to run backward
        """
        if not self.isInit:
            self.setup()
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, HIGH)
        print("moving backward")
    
    def stop(self):
        """
        sets motor to stop
        """
        if not self.isInit:
            self.setup()
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, LOW)
        print("stopping")
        
        



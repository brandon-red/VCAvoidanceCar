import RPi.GPIO as GPIO 
import time

LOW = GPIO.LOW
HIGH = GPIO.HIGH

class Motor:
    def __init__(self, IN1, IN2, EN):
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN = EN
        self.isInit = False
    
    def setup(self):
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, LOW)
        p = GPIO.PWM(self.EN, 1000)
        p.start(25)
        



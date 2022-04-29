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
        pwm = GPIO.PWM(self.EN, 100)
        pwm.start(25)
        self.isInit = True
    
    def forward(self):
        GPIO.output(self.IN1, HIGH)
        GPIO.output(self.IN2, LOW)
        print("forward")
    
    def backward(self):
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, HIGH)
        print("backward")
    
    def stop(self):
        GPIO.output(self.IN1, LOW)
        GPIO.output(self.IN2, LOW)
        print("stop")
        
        



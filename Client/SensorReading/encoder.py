import RPi.GPIO as GPIO
import time

class Encoder():
    def __init__(self, CLK_pin, DT_pin):
        self.CLK_pin = CLK_pin
        self.DT_pin = DT_pin
        self.isInit = False
        self.A = self.B = 0

    def setup(self):
        GPIO.setup(self.CLK_pin, GPIO.IN)
        GPIO.setup(self.DT_pin, GPIO.IN)
        self.isInit = True
    def getPosition(self, position):
        if self.isInit == False:
            self.setup()
        
        ######### READ PIN STATE #########
        self.A = GPIO.input(self.CLK_pin) # read status of pin/port and assign to variable i
        self.B = GPIO.input(self.DT_pin) # read status of pin/port and assign to variable i


        ######### CHECK ENCODER A OUTPUT OF MOTOR #########
        if(self.A): # LOW to HIGH transition on A    
            if(not self.B): position += 1 # going clockwise: increment
            else: position -= 1 # going counterclockwise: decrement

        else: #HIGH to LOW transition on A
            if(self.B): position += 1 # going clockwise: increment
            else: position -= 1 # going counterclockwise: decrement        


        ######### CHECK ENCODER B OUTPUT OF MOTOR #########
        if(self.B): # LOW to HIGH transition on B    
            if(self.A): position += 1 # going clockwise: increment
            else: position -= 1 # going counterclockwise: decrement

        else: #HIGH to LOW transition on B
            if(not self.A): position += 1 # going clockwise: increment
            else: position -= 1 # going counterclockwise: decrement
        return position

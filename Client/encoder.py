import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.IN)  # Physical pin n as an input  physical pin : 7
GPIO.setup(17, GPIO.IN) # set a port/pin as an input physical pin :11

stateA = stateB = position = 0

while True:
    
    ######### READ PIN STATE #########
    stateA = GPIO.input(4) # read status of pin/port and assign to variable i
    steteB = GPIO.input(17) # read status of pin/port and assign to variable i
    
    
    ######### CHECK ENCODER A OUTPUT OF MOTOR #########
    if(stateA): # LOW to HIGH transition on A    
        if(not stateB): position += 1 # going clockwise: increment
        else: position -= 1 # going counterclockwise: decrement
        
    else: #HIGH to LOW transition on A
        if(stateB): position += 1 # going clockwise: increment
        else: position -= 1 # going counterclockwise: decrement        
        

    ######### CHECK ENCODER B OUTPUT OF MOTOR #########
    if(stateB): # LOW to HIGH transition on B    
        if(stateA): position += 1 # going clockwise: increment
        else: position -= 1 # going counterclockwise: decrement
        
    else: #HIGH to LOW transition on B
        if(not stateA): position += 1 # going clockwise: increment
        else: position -= 1 # going counterclockwise: decrement
    
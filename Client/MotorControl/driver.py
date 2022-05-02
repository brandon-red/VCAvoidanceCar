from motor_controller import Motor
from SensorReading.ranger import Ranger
import time

class Driver:
    def __init__(self, right, left):
        self.right = right
        self.left = left
        self.is_forward = False
        self.is_backward = False
        self.isInit = False

    def setup(self):
        self.right.setup()
        self.left.setup()
        self.isInit = True
    
    def getMovement(self):
        """
        gets what movement the vehicle is doing 
        """
        if self.is_forward:
            return 'forward'
        elif self.is_backward:
            return 'backward'
        return 'stopped'

    def forward(self):
        """
        sets both motors to forward 
        """
        if not self.isInit:
            self.setup()
        self.right.forward()
        self.left.forward()
        self.is_forward = True
        self.is_backward = False
        self.is_stopped = False

    def backward(self):
        """
        sets both motors to backward 
        """
        if not self.isInit:
            self.setup()
        self.right.backward()
        self.left.backward()
        self.is_forward = False
        self.is_backward = True
        self.is_stopped = False

    def turnRight(self):
        """
        sets right side to go backward 
        sets left side to go forward
        turns the vehicle right
        """
        if not self.isInit:
            self.setup()
        self.right.backward()
        self.left.forward()    

    def turnLeft(self):
        """
        sets right side to go forward
        sets left side to go backward
        turns the vehicle left
        """
        if not self.isInit:
            self.setup()
        self.right.forward()
        self.left.backward()

    def stop(self):
        """
        sets right side to stop
        sets left side to stop
        stops the vehicle
        """
        if not self.isInit:
            self.setup()
        self.right.stop()
        self.left.stop()
        self.is_forward = False
        self.is_backward = False
        self.is_stopped = True


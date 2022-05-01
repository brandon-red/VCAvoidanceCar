from motor_controller import Motor
from SensorReading.ranger import Ranger

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
        gets what setting the car is in 
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
        
        if not self.isInit:
            self.setup()
        self.right.backward()
        self.left.forward()    
    
    def turnLeft(self):
        if not self.isInit:
            self.setup()
        self.right.forward()
        self.left.backward()

    def stop(self):
        if not self.isInit:
            self.setup()
        self.right.stop()
        self.left.stop()
        self.is_forward = False
        self.is_backward = False
        self.is_stopped = True


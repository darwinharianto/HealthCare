import time
from utility.buzzer import ActiveBuzzer

class Buzzer(object):
    def __init__(self, pin):
        self.pin = pin
        
    def Positive(self):
        ActiveBuzzer(self.pin, 0.25, 0.5, 1).on()
    
    def Negative(self):
        ActiveBuzzer(self.pin, 0.25, 0.25, 2).on()
        
    def Shutdown(self):
        ActiveBuzzer(self.pin, 1.5, 0.5, 1).on()
        
    def Phase(self):
        time.sleep(3)
        ActiveBuzzer(self.pin, 1.5, 0.5, 1).on()
        ActiveBuzzer(self.pin, 0.5, 0.5, 1).on()
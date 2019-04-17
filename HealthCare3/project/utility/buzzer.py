import time
import RPi.GPIO as GPIO



class PassiveBuzzer(object):
    
    
    def __init__(self ,pin , hz, loop, duration):
        self.pin = pin
        self.hz = hz
        self.loop = loop
        self.duration = duration


    def on(self):
        SOUNDER = self.pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)
        p = GPIO.PWM(SOUNDER, 1)
        for i in range(self.loop):
            p.start(50)
            p.ChangeFrequency(self.hz)
            time.sleep(self.duration)
            p.stop()
        time.sleep(0.2)
        GPIO.cleanup(SOUNDER)



""" sample
buzzer = Buzzer_ByGPIO(4, 2000,1,0.05)
buzzer.on()
"""
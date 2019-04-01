# buzzer.py

import time
import RPi.GPIO as GPIO

class Buzzer_ByGPIO(object):
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



buzzer = Buzzer_ByGPIO(4, 2000,1,0.05)
buzzer.on()


"""


class ActiveBuzzer_byGPIO(object):
    def __init__(self, pin, sec, waitsec=0, cnt=1):
        self.pin = pin
        self.sec = sec
        self.cnt = cnt
        self.waitsec = waitsec

    def on(self):
        for i in range(self.cnt):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.sec)
            GPIO.output(self.pin, GPIO.LOW)
            GPIO.cleanup(self.pin)
            time.sleep(self.waitsec)


"""

""" sample

buzzer = ActiveBuzzer(17, 0.5, 0, 1)
buzzer.on()

buzzer = Buzzer_ByGPIO(4, 2000,1,0.5)

"""

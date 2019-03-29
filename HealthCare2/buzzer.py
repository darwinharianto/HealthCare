# buzzer.py

import time
import RPi.GPIO as GPIO


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


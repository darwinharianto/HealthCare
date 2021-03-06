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



class ActiveBuzzer(object):
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



if __name__ == "__main__":
    buzzer = ActiveBuzzer(26, 5)
    buzzer.on()
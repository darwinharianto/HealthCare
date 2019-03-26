import RPi.GPIO as GPIO
import time

def buzzer(pin, hz, loop, duration):
    SOUNDER = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)
    p = GPIO.PWM(SOUNDER, 1)
    for i in range(loop):
        p.start(50)
        p.ChangeFrequency(hz)
        time.sleep(duration)
        p.stop()
    time.sleep(0.2)

    GPIO.cleanup(SOUNDER)

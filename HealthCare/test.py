
#!/usr/bin/python

#import subprocess
#import os
#import sys
#import struct
#import numpy as np


#os.system('x-terminal-emulator -e /bin/bash -c\"python2 /usr/share/HealthCare/test.py"')

#a = subprocess.check_output(["sudo", "gatttool","-t","random","-b", "6f:89:da:83:b8:32", "--char-read", "--handle=0x40", "--value=0100"])
#u = unicode(a, "utf-8")
#print(u)

#x = u.split(":",1)[1]
#y = x.split(" ")
#bluetoothString = " "
#for i in range(len(y)-1):
	#bluetoothString+=str(y[i].decode("hex"))
#print bluetoothString


#print subprocess.check_output(['curl','-X','GET', '--header', 'Accept:application/json', 'http://40.74.88.202:3000/api/Commodity'])


#print subprocess.check_output(['curl', '-X', 'POST', '--header', 'Content-Type:application/json', '--header', 'Accept:application/json', '-d', '{"$class":"org.stock.mynetwork.Trader","tradeId":"JapanTHC","firstName":"a","lastName":"a"}', 'http://40.74.88.202:3000/api/Trader'])

#subprocess.check_output(['mysql', '-h', '52.193.188.33', '--port=3306', '-u', 'pasonatech', '-p' ])
#subprocess.check_output(['pasonatech'])
#subprocess.check_output(['use', 'demodb'])



# coding: utf-8

import RPi.GPIO as GPIO
import time

def buzzer(pin, hz, loop):
    SOUNDER = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUNDER, GPIO.OUT, initial = GPIO.LOW)
    p = GPIO.PWM(SOUNDER, 1)
    for i in range(loop):
	p.start(50)
	p.ChangeFrequency(hz)
	time.sleep(0.1)
	p.stop()
	time.sleep(0.2)

    GPIO.cleanup(SOUNDER)



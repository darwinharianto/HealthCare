# function.py
import os
import sys
import json
import time
import unit
from buzzer import ActiveBuzzer_byGPIO
from card_reader import NFC_byUSB

# const param
BUZZER_PIN = 17


# global object
nfc = NFC_byUSB()
beforeID = None
beforeTime = None


#
# sequence buzzer 
#
def sequenceBuzzer_systemup():
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.5, 0.5).on()
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.05, 1).on()


def sequenceBuzzer_actionStart():
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.5, 0.5).on()
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.05, 2).on()


#
# message buzzer
#
def buzzer_systemdown():
    ActiveBuzzer_byGPIO(BUZZER_PIN, 1.5).on()


def buzzer_complated():
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.1, 1).on()

def buzzer_invalidCard():
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.1, 1).on()
    ActiveBuzzer_byGPIO(BUZZER_PIN, 0.25, 0.1, 1).on()


#
# system command
#
def reboot():
    print("reboot!!")
    sys.exit()
#    os.system("sudo reboot")


def shutdown():
    print("shutdown!!")
    sys.exit()
#    os.system("sudo shutdown!!")


#
# read nfc card
#
def touch_wait():

    while True:
        ret, id = nfc.read_wait()
        if ret == False:
            continue
        else:
            return id


#
# get mode
#
def select_mode():
    mode = None
    try:
        file = open('config.json', 'r')
        data = json.load(file)
        mode = data["MODE"]
    except IOError as e:
        pass
    except AttributeError as e:
        pass

    return mode


#
# check double touch
#
def check_enableTouch(id):
    global beforeID
    global beforeTime

    # check first touch by systemup
    if (beforeID == None) and (beforeTime == None):
        return True

    # except double touch
    # if last touched 5sec ago, enable
    if (beforeID == id) and ((time.time() - beforeTime) > 5):
        return True

    if (beforeID != id):
        return True

    # bad touch
    return False


#
# sequence complate
#
def sequence_complate(id):
    global beforeID
    global beforeTime
    beforeID = id
    beforeTime = time.time()


#
# select unit
#

def select_unit(unitname):
    unit= None
    if(unitname == "Entrance"):
        unit = unit.Entrance()
    elif(unitname == "Exit"):
        unit = unit.Exit()
    elif(unitname == "BodyScale"):
        unit = unit.BodyScale()


    return unit

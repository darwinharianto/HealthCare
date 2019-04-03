# function.py
import os
import sys
import ble
import json
import time
import unit
import subprocess
from ble import Central
from config_reader import ConfigReader
from buzzer import Buzzer_ByGPIO
from card_reader import NFC_byUSB
from card_reader import NFC_byGPIO

# const param
BUZZER_PIN = 4


# global object
nfc = NFC_byUSB()
beforeID = None
beforeTime = None


#
# sequence buzzer 
#
def sequenceBuzzer_systemup():
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 0.5).on()
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 0.05).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.5, 0.5).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.05, 1).on()


def sequenceBuzzer_actionStart():
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 0.5).on()
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 2, 0.05).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.5, 0.5).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.05, 2).on()


#
# message buzzer
#
def buzzer_systemdown():
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 1.5).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 1.5).on()


def buzzer_complated():
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 0.05).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.1, 1).on()

def buzzer_invalidCard():
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 2, 0.05).on()
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 2, 0.25).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.05, 0.1, 1).on()
    #ActiveBuzzer_byGPIO(BUZZER_PIN, 0.25, 0.1, 1).on()


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
    #check which reader is available
    
    while True:
        ret, id = nfc.read_wait()
        if ret == False:
            continue
        else:
            return id

def check_availableReader():
    global nfc
    usb_list = subprocess.check_output(['lsusb'])
    NFC_list = subprocess.check_output(['i2cdetect', '-y', '1'])
    if "Sony Corp." in usb_list:
        nfc = NFC_byUSB()
        print("Pasori detected")
    elif "24" in NFC_list:
        nfc = NFC_byGPIO()
        print("PN532 detected")
    else:
        nfc = None
#
# get mode
#
def select_mode():
    mode = None
    try:
        mode = ConfigReader("/home/pi/HealthCare/HealthCare2/config.txt").read_config()
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
# check for setting signal
#

def config_setting():
    #read current config
    configReader = ConfigReader("/home/pi/HealthCare/HealthCare2/config.txt")
    config = configReader.read_config()
    
    central = Central()
    
    #search for beacon for 30 secs
    timeBefore = time.time()
    settingMode = False
    while True:
        devs = central.scan("00000000-0000-0000-0000-000000000001")
        if not devs == None:
            settingMode = True
            break
        if (time.time()-timeBefore > 30):
            break
    if not settingMode:
        return
    central.connectTo(devs[0])
    data = central.getNotify("00000000-0000-0000-0000-000000000001","00000000-0000-0000-0000-000000000001",30)
    Buzzer_ByGPIO(BUZZER_PIN, 2000, 1, 0.05).on()
    if data is None:
        data = config
    #
    #handle = central.getHandle("00000000-0000-0000-0000-000000000001")
    #send config to phone
    #central.writeCharacteristic(handle, bytes(data))
    if data is None:
        print("None")
        return
    else:
        print(data)
        configReader.write_config(data)
    central.disconnect()

#
# select unit
#

def select_unit(unitname):
    unitMode= None
    if(unitname == "Entrance"):
        unitMode = unit.Entrance()
    elif(unitname == "Exit"):
        unitMode = unit.Exit()
    elif(unitname == "BodyScale"):
        unitMode = unit.BodyScale()
    elif(unitname == "Apply"):
        unitMode = unit.Apply()
    return unitMode

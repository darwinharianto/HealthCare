import utility.nfclib as nfclib
import utility.blelib as blelib
import buzzer
import sys
import json
import requests
import os
import env
from unit import DC320

DEBUG               = True
CONFIG_WAITTIME     = 2
UUID_SERVICE        = "00000000-0000-0000-0000-000000000000"
UUID_CHAR_MODE      = "00000000-0000-0000-0000-000000000001"


buzzer    = buzzer.Buzzer(26)
nfc       = nfclib.PN532()
ble       = blelib.Central()
unit      = None
currentID = None


def debug_print(msg):
    if DEBUG:
        print(msg)


def abort():
    debug_print("Abort!!")
    sys.exit()
    

def shutdown():
    debug_print("shutdown!!")
#    os.system("sudo shutdown")
    sys.exit()
    

def phase_config():
    debug_print("Phase : Config phase start.")
    buzzer.Phase()
    
    # scan peripheral
    debug_print("BLE scan start.")
    success, devs = ble.scan(UUID_SERVICE, CONFIG_WAITTIME)
    if not (devs is None):
        # connect peripheral
        ble.connectTo(devs[0])
        debug_print("connected.")
        mode_num = None
        # wait notify
        if ble.waitNotify(UUID_SERVICE, UUID_CHAR_MODE, 30):
            mode_num = ble.readNotify()
            if (not mode_num is None) and (not mode_num == ""):
                # save mode num
                buzzer.Positive()
                with open(env.CONFIG_PATH, mode="w") as f:
                    f.write('{"MODE":%s}'%mode_num)
            else:
                debug_print("Invalid notify data.")
        else:
            debug_print("Notify not found.")
            return False
        
    debug_print("Phase : Config phase ended.")
    return True
    

def phase_setup():
    global unit
    debug_print("Phase : Setup start.")
    buzzer.Phase()

    debug_print("Load config.")
    config = None
    with open(env.CONFIG_PATH, "r") as f:
        config = json.load(f)

    debug_print("Select unit.")
    unit = None
    print("config ==>  %s"%config)
    if not config is None:
        mode = config["MODE"]
#        if mode == 1: unit = Entrance()
#        if mode == 2: unit = Exit()
        if mode == 3: unit = DC320()
        
    if unit is None:
        debug_print("Invalid unit mode.")
    else:
        debug_print("Unit mode --> %s"%mode)
        unit.setup(env.WEBAPI_SERVER, env.WEBAPI_PORT)
    
    debug_print("Phase : Setup ended.")
    return True if (not unit is None) else False

        
        
def phase_nfc():
    global currentID
    debug_print("Phase : Touch NFC.")

    # reset currentID
    currentID = None

    # touch nfc phase
    success, idm = nfc.read_wait()
    if not success:
        debug_print("NFC read failed.")
        buzzer.Negative()
    else:
        debug_print("Detect tag. IDm --> [%s]"%idm)
        currentID = idm
        buzzer.Positive()
        
    return success, idm
    
    
def phase_checkID():
    debug_print("Phase : Check registred ID.")

    data = {"ID":"%s"%currentID}
    url = "http://%s:%s/api/v1/%s"%(env.WEBAPI_SERVER, env.WEBAPI_PORT, "user_data")
    res = requests.get(url, data, timeout=5.0)
    if res.status_code != 200:
        debug_print("Status code not 200.  [code=%s]"%res.status_code)
        return False

    if (res.text == ""):
        debug_print("This ID is disable.")
        buzzer.Negative()
        return False
    else:
        debug_print("This ID is enable.")
        return True


def phase_unitAction():
    debug_print("Phase : unit sequence start.")
    
    if not unit.sequence(currentID):
        debug_print("Unit action abort.")
        return False
    else:
        debug_print("Unit action complete.")
        return True
    
import nfc
import unit
import time
import json
import bluetooth
from utility.buzzer import ActiveBuzzer

# const value
CONFIG_WAITTIME= 5
BUZZER_PIN     = 4
UUID_SERVICE   = "00000000-0000-0000-0000-000000000000"
UUID_CHAR_MODE = "00000000-0000-0000-0000-000000000001"
CONFIG_PATH    = "/home/pi/HealthCare3/project/config.ini"

# global value
NFC        = nfc.PN532()
MODE       = None
BLE        = bluetooth.Central()
ID         = None



def debug_string(msg):
    print(msg)


def buzzer_configPhase():
#    ActiveBuzzer(BUZZER_PIN, 0.5, 0.5).on()
#    ActiveBuzzer(BUZZER_PIN, 0.1, 0.2).on()
    pass


def buzzer_actionPhase():
#    ActiveBuzzer(BUZZER_PIN, 0.5, 0.5).on()
#    ActiveBuzzer(BUZZER_PIN, 0.1, 2, 0.05).on()
    pass


def buzzer_systemdown():
#    ActiveBuzzer(BUZZER_PIN, 1.5).on()
    pass
    

def buzzer_positive():
#    ActiveBuzzer(BUZZER_PIN, 0.1).on()
    pass
    
    
def buzzer_positive_long():
#    ActiveBuzzer(BUZZER_PIN, 0.5).on()
    pass


def buzzer_negative():
#    ActiveBuzzer(BUZZER_PIN, 0.1, 0.1, 2).on()
    pass
        
    
def reboot():
    print("reboot!!")
    sys.exit()
#    os.system("sudo reboot")


def shutdown():
    print("shutdown!!")
#    os.system("sudo shutdown!!")
        
    
def setup():
    bluetooth.setupBLE()
    
    
def load_mode():
    global MODE
    debug_string("Load phase...")
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
        mode = data["MODE"]
        if mode == 1: MODE = unit.Entrance()
        if mode == 2: MODE = unit.Exit()
        if mode == 3: MODE = unit.DC320()
        
    
def save_mode(mode):
    data = '{"MODE":%s}'%(mode)
    with open(CONFIG_PATH, mode="w") as f:
        f.write(data)
        

def config():
    debug_string("config phase.")
    
    # connection phase
    timeBegin = time.time()
    while True:
        debug_string("scaning...")
        devs = BLE.scan(UUID_SERVICE)
        if devs is None:
            timeCurrent = time.time()
            if (timeCurrent - timeBegin) > CONFIG_WAITTIME:
                return
            else:
                continue
        else:
            BLE.connectTo(devs[0])
            svc = BLE.mPeripheral.getServiceByUUID("00000000-0000-0000-0000-000000000000")
            ch = svc.getCharacteristics("00000000-0000-0000-0000-000000000001")[0]    
            BLE.mPeripheral.writeCharacteristic(ch.valHandle+1, "\x01\x00")
            break
    
    # wait notify phase
    timeBegin = time.time()
    while True:
        debug_string("wait notity...")
        if not BLE.mPeripheral.waitForNotifications(1.0):
            continue
        else:
            buzzer_positive()
            break
    
    # save mode
    debug_string("save config.")
    mode = BLE.readNotify()
    save_mode(mode)


def nfc_read():
    global ID
    debug_string("please touch tag.")
    ID = NFC.read_wait()
    
    
def mode_sequence():
    MODE.setUserID(ID)
    MODE.sequence()
        
        
if __name__ == "__main__":
    try:
        config()
        load_mode()
        while True:
            nfc_read()
            mode_sequence()
        
    except IOError as e:
        buzzer_systemdown()
        shutdown()
        
    except nfc.exception.NFC_DeviceNotFound as e:
        buzzer_systemdown()
        shutdown()
        
#    except:
#        print("Unexpected error.")
#        shutdown()

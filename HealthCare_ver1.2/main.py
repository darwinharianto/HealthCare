import core
import serial
import bluepy
import requests

core.debug_print("Start program.")
try:
    # config
    success = core.phase_config()
    if not success: core.abort()

    # unit setup
    success = core.phase_setup()
    if not success: core.abort()

    while True:
        
        # get id
        success = core.phase_nfc()
        if not success: continue

        # check read id
        success = core.phase_checkID()
        if not success: continue

        # unit action
        success = core.phase_unitAction()
        if not success: continue

except bluepy.btle.BTLEManagementError as e:
    core.debug_print("**Exception** : BTLEManagementError exception. (maybe... Bluetooth module not found.)")
    core.shutdown()
    
except serial.serialutil.SerialException as e:
    core.debug_print("**Exception** : Serial exception. (maybe...Serial device not found.)")
    core.shutdown()

except requests.ConnectionError as e:
    core.debug_print("**Exception** : Http connection error exception. (maybe... WiFi module not found.)")
    core.shutdown()
    


core.debug_print("End program.")
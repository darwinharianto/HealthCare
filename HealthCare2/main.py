# main.py
import unit
import time
import function as fnc

def debug_print(msg):
    print(msg)

#
# systemup
#
debug_print("system up.")

#
# TODO check config mode
#
print("start reading config")
fnc.config_setting()

debug_print("sequence: check config mode.")
fnc.sequenceBuzzer_systemup()
debug_print("systemup sound")
time.sleep(2)

#
# select unit
#



#unit = unit.BodyScale()
#print(unit.name)
debug_print("sequence: select mode")
unitMode = fnc.select_mode()
unit = fnc.select_unit(unitMode)
if unitMode is None:
    fnc.buzzer_systemdown()
    fnc.reboot()


#
# start: mode action
#
debug_print("sequence: action start.")
fnc.sequenceBuzzer_actionStart()
time.sleep(2)
while True:
    id = None

    #check Available Reader
    fnc.check_availableReader()
    if fnc.nfc == None:
        # critical error
        print("No reader detected")
        fnc.buzzer_systemdown()
        fnc.shutdown()
        
    try:
        ### read id ###
        print("touch card.")
        id = fnc.touch_wait()
        fnc.buzzer_complated()

        ### check enable touch ###
        if not fnc.check_enableTouch(id):
            print("not avaliable card.")
            continue
        else:
            print("ID: %s")%id

        ### mode action ###
        unit.action(id)

        ### process complate ###
        debug_print("complete.")
        fnc.buzzer_complated()
        fnc.sequence_complate(id)


    except AttributeError as e:
         # can't read nfc tag
         fnc.buzzer_invalidCard()
         print(e)
         continue

    except Exception as e:
        # critical error
        print(e)
        fnc.buzzer_systemdown()
        fnc.shutdown()

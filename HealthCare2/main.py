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
debug_print("sequence: check config mode.")
fnc.sequenceBuzzer_systemup()


#
# select unit
#
unit = unit.BodyScale()
print(unit.name)
#debug_print("sequence: select mode")
#unit = fnc.select_unit()
#if not mode is None:
#    fnc.buzzer_systemdown()
#    fnc.reboot()


#
# start: mode action
#
debug_print("sequence: action start.")
fnc.sequenceBuzzer_actionStart()
while True:
    id = None

    try:
        ### read id ###
        print("touch card.")
        id = fnc.touch_wait()

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
#         print(e)
         continue

    except Exception as e:
        # critical error
        print(e)
        fnc.buzzer_systemdown()
        fnc.shutdown()

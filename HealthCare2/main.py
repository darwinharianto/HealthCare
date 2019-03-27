# main.py
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
# select mode
#
debug_print("sequence: select mode")
#mode = fnc.select_mode()
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
        id = fnc.touch_wait()

        ### check enable touch ###
        if not fnc.check_enableTouch(id):
            continue
        else:
            debug_print("ID: {}".format(id))

        ### mode action ###
        

        ### process complate ###
        debug_print("complate.")
        fnc.buzzer_complated()
        fnc.sequence_complate(id)


    except AttributeError as e:
         # can't read nfc tag
         fnc.buzzer_invalidCard()
#         print(e)
         continue

    except:
        # critical error
        fnc.buzzer_systemdown()
        fnc.shutdown()

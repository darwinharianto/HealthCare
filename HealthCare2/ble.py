import subprocess
import binascii
import re
import os
import time


# encode function
def hexstr(data):
    chars = [c.encode("hex") for c in data]
    str = ""
    for char in chars:
        str += char + " "
    return str


# BLE class
class BLE(object):
    def __init__(self):
        self.clear()
#        self.init()


    def _set_data(self, msg):
        self.msg = hexstr(msg)
        self.len = len(msg)


    def clear(self):
        self.msg = None
        self.len = None
        self.cmd = None


    def init(self):
        ### execute cmd ####
        cmds = []
        cmds.append("sudo hciconfig hci0 reset")
        cmds.append("sudo invoke-rc.d bluetooth restart")
        cmds.append("sudo hciconfig hci0 up")
        for cmd in cmds:
            os.system(cmd)


    def startAdvertise(self):
        os.system("sudo hciconfig hci0 leadv")


    def stopAdvertise(self):
        os.system("sudo hciconfig hci0 noleadv")


    def send(self, msg):
        ### set data ###
        self._set_data(msg)

        ### struct cmd ###
        cmds = []
#        cmds.append("sudo hciconfig hci0 leadv")
        cmds.append("sudo hcitool -i hci0 cmd 0x08 0x0008 {0:02x} 02 01 1a {1:02x} ff 18 01 {2}".format(self.len + 1, self.len + 3, self.msg))
        
#        cmds.append("sudo hcitool -i hci0 cmd 0x08 0x0008 " + str(self.len + 1) + " 02 01 1a " + "{0:02x}".format(self.len + 3) + " ff 18 01 " +  self.msg)
        cmds.append("sudo hciconfig hci0 leadv 0")

        ### execute cmd ###
        for cmd in cmds:
            print("Command: {}".format(cmd))
            os.system(cmd)

        ### send complate ####
        self.clear()


ble = BLE()
ble.init()

ble.startAdvertise()
for i in range(2):
    ble.send("testaaaaaaa")
    time.sleep(5)
ble.stopAdvertise()


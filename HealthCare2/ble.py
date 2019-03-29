import subprocess
import binascii
import re
import os
import time


#
# encode function
#
def hexstr(data):
    chars = [c.encode("hex") for c in data]
    str = ""
    for char in chars:
        str += char + " "
    return str


#
# select most dBm device
#
def best_device_mac(devs):

    ### get best device ###
    best_index = None
    best_dBm = 100
    for i, dev in enumerate(devs):

        ### regex ###
        r = re.compile("([0-9]+) dBm")
        m = r.search(dev)
        dBm = int(m.group(1))

        ### check best dBm ###
        if best_dBm > dBm:
            best_dBm = dBm
            best_index = i
    bestDev = devs[best_index]

    ### get best device mac address ###
    r = re.compile("(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)")
    m = r.search(bestDev)
    bestDevMac = m.group(0)
    return bestDevMac;


#
# find service handle
#
def find_service_handle(mac, uuid):

    ### scan service ###
    cmd = ["sudo", "gatttool", "-t", "random", "-b", mac, "--char-desc"]
    output = subprocess.check_output(cmd);

    ### check output ###
    # TODO

    ### split output ###
    services = output.split("\n")

    ### find uuid ###
    handle = None
    for service in services:
        if uuid in service:
            m = re.compile("(0x[0-9]*),").search(service)
            handle = m.group(0)
    return handle


#
# BLE class
#
class BLE(object):


    def scan(self, uuid):
        ### get BLE list ###
        cmd = ["sudo", "blescan", "-t", "1"]
        bleDevs = subprocess.check_output(cmd)

        ### check list string ###
        if not (("Device" in bleDevs) and ("dBm" in bleDevs)):
            raise AttributeError("scrayping failed.")

        ### data split ###
        bleDevs = bleDevs.split("Device")

        ### get target info ###
        targetDevs = []
        for bleDev in bleDevs:
            if uuid in bleDev:
                targetDevs.append(bleDev)

        ### check exists, target device ###
        if len(targetDevs) <= 0:
            return None

        return targetDevs;


    def select_best_device(self, devs):
        ### get best device ###
        best_index = None
        best_dBm = 100
        for i, targetDev in enumerate(targetDevs):

            ### regex ###
            r = re.compile("([0-9]+) dBm")
            m = r.search(targetDev)
            dBm = int(m.group(1))

            ### check best dBm ###
            if best_dBm > dBm:
                best_dBm = dBm
                best_index = i
        bestDev = targetDevs[best_index]
        print(bestDev)

	### get best device mac address ###
        r = re.compile("(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)")
        m = r.search(bestDev)
        bestDevMac = m.group(0)
        return bestDevMac;



    def send(self, msg, mac, ):
        cmd = ["sudo", "gatttool", "-t", "random", "-b", mac, "--char-write-req", ]



"""
SERVICE_UUID = "00000000-0000-0000-0000-000000000001"
CHARACTERISTIC_UUID = "00000000-0000-0000-0000-000000000002"
ble = BLE()
devs = ble.scan(SERVICE_UUID)
if devs is None:
    print("service not found.")

else:
    mac = best_device_mac(devs)
    if mac is None:
        print("this uuid is not exists.")
    else:
        handle = find_service_handle(mac, CHARACTERISTIC_UUID)
        print(handle)
"""

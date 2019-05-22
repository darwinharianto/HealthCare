import os
import re
import time
import binascii
from bluepy import btle
from bluepy.btle import Scanner
from bluepy.btle import DefaultDelegate


gBLEScanner = None
gBLEDevices = []
gBLENotify  = None

#
# bluetooth device restart
#
def setupBLE():
    os.system("sudo systemctl restart bluetooth")
    time.sleep(2)


#
# scan delegate class
#
class ScanDelegate(DefaultDelegate):


    def __init__(self):
        DefaultDelegate.__init__(self)


    def handleDiscovery(self, dev, isNewDev, isNewData):
        global gBLEDevices
        global gBLEScanner
        if isNewDev:
            for (_, desc, value) in dev.getScanData():
                m = re.match("\w\w\w\w\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w\w\w\w\w\w\w\w\w", value)
                if m:
                    gBLEDevices.append([dev.addr, dev.addrType, dev.rssi, value])


#
# peripheral delegate class
#
class PeripheralDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)


    def handleNotification(self, cHandle, data):
        global gBLENotify
	gBLENotify = data


#
# ble device class
#
class Device(object):
    def __init__(self, addr, addrType, rssi, uuid):
        self.addr = addr
        self.addrType = addrType
        self.rssi = rssi
        self.uuid = uuid


#
# ble Central class
#
class Central(object):


    mPeripheral = None


    def __init__(self):
        global gBLEScanner
        global gBLEDevices
        gBLEScanner = Scanner().withDelegate(ScanDelegate())
        gBLEDevices = []


    def scan(self, uuid, timeout=5.0):
        timeBegin = time.time()
        while (time.time() - timeBegin) < timeout:
            devs = self.search("00000000-0000-0000-0000-000000000000")
            if not devs == None:
                return True, devs
        return False, None


    def search(self, uuid, timeout=0.15):
        global gBLEScanner
        global gBLEDevices
        targetUUID = uuid

        # scan service
        gBLEDevices = []
        gBLEScanner.scan(timeout)
        matchDevs = []
        if not (gBLEDevices == []):

            # check match uuid
            for i in range(len(gBLEDevices)):
                addr = gBLEDevices[i][0]
                type = gBLEDevices[i][1]
                rssi = gBLEDevices[i][2]
                uuid = gBLEDevices[i][3]
                m = re.match(uuid, targetUUID)
                if m:
                    matchDevs.append(Device(addr, type, rssi, uuid))

        # check hit device
        if matchDevs == []:
            return None
        else:
            return matchDevs


    def connectTo(self, dev):
        self.mPeripheral = btle.Peripheral(dev.addr, dev.addrType)
	self.mPeripheral.withDelegate(PeripheralDelegate())


    def disconnect(self):
        if not (self.mPeripheral is None):
            self.mPeripheral.disconnect()
            self.mPeripheral = None


    # get characteristic handle
    # uuid --> chracteristic uuid
    def getHandle(self, uuid):
        if not (self.mPeripheral is None):
            descs = self.mPeripheral.getDescriptors()
            for desc in descs:
                m = re.match(str(desc.uuid), uuid)
                if m:
                    return desc.handle


    def writeCharacteristic(self, handle, data):
        if not (self.mPeripheral is None):
            self.mPeripheral.writeCharacteristic(handle, data, True)


    def readCharacteristic(self, uuid):
        recv = None
        if not (self.mPeripheral is None):
            recv = self.mPeripheral.readCharacteristic(handle)
        return recv

    def waitNotify(self, service_uuid, characteristic_uuid, sec):
        svc = self.mPeripheral.getServiceByUUID(service_uuid)
        ch = svc.getCharacteristics(characteristic_uuid)[0]
        self.mPeripheral.writeCharacteristic(ch.valHandle+1, "\x01\x00")
        return self.mPeripheral.waitForNotifications(sec)
            
    def readNotify(self):
        global gBLENotify
        data = gBLENotify
        gBLENotify = None
        return data

#    def waitNotification(self, time=10):
#        global gBLENotify
#        gBLENotify = []
#        counter = time/0.1
#        while counter:
#            self.mPeripheral.waitForNotifications(0.1)
#            if gBLENotify == []:
#                counter = counter -1
#                continue;
#            return gBLENotify[0]
#        return None
    
    

if __name__ == "__main__":
    #setupBLE()
    central = Central()
    success, devs = central.scan("00000000-0000-0000-0000-000000000000", 10)
    if success:
        central.connectTo(devs[0], "00000000-0000-0000-0000-000000000000", "00000000-0000-0000-0000-000000000001")
        while True:
            if central.waitNotify(5):
                print("notify --> %s")%(central.readNotify())
            else:
                print("not notify.")
    else:
        print("device not found.")
        
        
        
"""
print("scan phase.")
while True:
    devs = central.scan("00000000-0000-0000-0000-000000000000")
    if not devs == None:
        break

print("connect phase.")
central.connectTo(devs[0])



print("notify phase.")
notify = central.waitNotification(10)

if not (notify is None):
    print("Notify : " + notify)

#handle = central.getHandle("00000000-0000-0000-0000-000000000001")

#print("write")
#central.writeCharacteristic(handle, b"BodyWeight")

#print("read")
#data = central.readCharacteristic(handle)
#if data is None:
#    print("None")
#else:
#    print(data)

print("disconnect.")
central.disconnect()
"""
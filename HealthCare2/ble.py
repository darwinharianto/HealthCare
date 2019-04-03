import re
import time
from bluepy import btle
from bluepy.btle import Scanner
from bluepy.btle import DefaultDelegate


gBLEScanner = None
gBLEDevices = []
gBLENotifyData = None


#
# scan delegate class
#
class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)
        global gBLENotifyData
        gBLENotifyData = data


    def handleDiscovery(self, dev, isNewDev, isNewData):
        global gBLEDevices
        global gBLEScanner
        if isNewDev:
            for (_, desc, value) in dev.getScanData():
                #m = re.match("\w\w\w\w\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w\w\w\w\w\w\w\w\w", value)
                m = re.match("\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", value)
                if m:
                    gBLEDevices.append([dev.addr, dev.addrType, dev.rssi, value])

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


    def scan(self, uuid, timeout=0.15, autoloop=False):
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


    def disconnect(self):
        if self.mPeripheral is not None:
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


    def readCharacteristic(self, handle):
        recv = None
        if not (self.mPeripheral is None):
            recv = self.mPeripheral.readCharacteristic(handle)

        return recv
    
    
    def getNotify(self, service_uuid, char_uuid, sec):
        global gBLENotifyData
        gBLENotifyData = None
        self.mPeripheral.setDelegate(ScanDelegate())

        svc = self.mPeripheral.getServiceByUUID("00000000-0000-0000-0000-000000000001")
        ch = svc.getCharacteristics("00000000-0000-0000-0000-000000000001")[0]
        self.mPeripheral.writeCharacteristic(ch.valHandle+1, "\x01\x00")
        loopCount = 0
        while True:
            loopCount += 1
            if self.mPeripheral.waitForNotifications(1.0):
                data = gBLENotifyData
                print("notify data = ", data)
                break
            print("waiting")
            if loopCount == sec:
                break
        return gBLENotifyData
    
    
        
""" notify example
central = Central()
while True:
    devs = central.scan("00000000-0000-0000-0000-000000000001")
    if not devs == None:
        break


central.connectTo(devs[0])
central.mPeripheral.setDelegate(ScanDelegate())

handle = central.getHandle("00000000-0000-0000-0000-000000000001")
svc = central.mPeripheral.getServiceByUUID("00000000-0000-0000-0000-000000000001")
ch = svc.getCharacteristics("00000000-0000-0000-0000-000000000001")[0]
print(ch)
#central.writeCharacteristic(handle, "\x01\x00")
central.mPeripheral.writeCharacteristic(ch.valHandle+1, "\x01\x00")
#ch = ch.valHandle+1
#ch.write("\x01\x00")
while True:
    if central.mPeripheral.waitForNotifications(1.0):
        print("get notif")
        data = central.getNotify()
        print("notify data = ", data)
        continue
    print("waiting")
"""
"""
central = Central()
while True:
    devs = central.scan("00000000-0000-0000-0000-000000000001")
    if not devs == None:
        break

central.connectTo(devs[0])
handle = central.getHandle("00000000-0000-0000-0000-000000000001")

print("write")
central.writeCharacteristic(handle, b"BodyWeight")

print("read")
data = central.readCharacteristic(handle)
if data is None:
    print("None")
else:
    print(data)

central.disconnect()




central = Central()
while True:
    devs = central.scan("00000000-0000-0000-0000-000000000002")
    if not devs == None:
        break

central.connectTo(devs[0])
handle = central.getHandle("00000000-0000-0000-0000-000000000002")

print("write")
central.writeCharacteristic(handle, b"BodyWeight")

print("read")
data = central.readCharacteristic(handle)
if data is None:
    print("None")
else:
    print(data)

central.disconnect()

"""

import subprocess
import os
import binascii
import nfc
import commands
import re
import codecs
from time import sleep
import buzzer

def readBLEData(uuid):
    bleList = None
    print("search BLE")
    a = False
    bleList = subprocess.check_output(["sudo", "blescan"]).split("Device")

    for i, str in enumerate(bleList):
        if "00000000-0000-0000-0000-000000000002" in str:
            print("find ble device")
            bleList = bleList[i]
	    print(bleList)
            a = True
	    break

    if a == False:
        return;

    sleep(0.2)

    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    state = bleList.split(" ")[3]
    bleList = bleList.split(" ")[2]
    bleList = ansi_escape.sub('',bleList)
    a = ["sudo hciconfig hci0 reset", "sudo invoke-rc.d bluetooth restart","sudo hciconfig hci0 up","hciconfig"]
    for i in a:
        os.system(i)
    if "random" in state:
	bleValue =  subprocess.check_output(["sudo", "gatttool", "-t", "random", "-b", bleList, "--char-read", "--uuid=%s"%uuid]).split("value: ")[1].split(" ")
    else:
        bleValue =  subprocess.check_output(["sudo", "gatttool", "-b", bleList, "--char-read", "--uuid=%s"%uuid]).split("value: ")[1].split(" ")
    breakindex = None
    for i, str in enumerate(bleValue):
            breakindex = i
            if not str.isdigit():
                    break
    bleValue = bleValue[0:breakindex]
    str = ""
    for i in bleValue:
            str += codecs.decode(i, "hex_codec")
    print("read BLE data: %s" %str)
    return str

def exchangeBLE(data, uuid):
    hciCommand = constructBLEData(data)
    print("acting as beacon")
    print(data)
    a = ["sudo hciconfig hci0 reset", "sudo invoke-rc.d bluetooth restart","sudo hciconfig hci0 up","hciconfig"]
    b = [hciCommand, "sudo hciconfig hci0 leadv 0"]
    for i in a:
        os.system(i)
    while True:
        for i in b:
            os.system(i)
        data = readBLEData(uuid)
	if data is not None:
	    print("complate")
	    return data
	sleep(0.5)


def constructBLEData(data):
    asciiArray = [c.encode("hex") for c in data]
    hciCommand = "sudo hcitool -i hci0 cmd 0x08 0x0008 "
    hciCommand += str(len(data)+1)
    hciCommand += " 02 01 1a " + '{0:02x}'.format(len(data)+3) + " ff 18 01 "
    for c in asciiArray:
        hciCommand += c + " "
    return hciCommand


class MyCardReader(object):

    def on_connect(self, tag):
        print "detected"
	buzzer.buzzer(4,2000,1,0.1)
        self.idm = binascii.hexlify(tag.idm)
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()


def readNFC():

    cr = MyCardReader()
    while True:
        try:
            print "touch card:"
            cr.read_id()
            print "released"
            return cr.idm
            break
        except AttributeError as e:
            print(e)
            break

def logUser(userID):

    a = ("curl -X POST 52.193.188.33:8080/api/v1/io -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\"}'" %userID)
    error = os.system(a)
    errorCheck(error)

def createUser(userID):

    a = ("curl -X POST 52.193.188.33:8080/api/v1/add -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\":\"%s\", \"name\":\"sawada\", \"io\":\"0\"}'" %userID)
    error = os.system(a)
    errorCheck(error)


def errorCheck(number):

    if number == 1792:
	print("server is down")
    else:
        print("Request success")


def testcommands():

    userID = "12312312321"
    a = ("curl -X POST 52.193.188.33:8080/api/v1/io -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\"}'" %userID)
    test = commands.getoutput(a)
    print("testcommands")
    print(test)

def updateWeight(userID, weight):

    os.system("curl -X POST 52.193.188.33:8080/api/v1/weight -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\", \"weight\":%s}'" %(userID,weight))

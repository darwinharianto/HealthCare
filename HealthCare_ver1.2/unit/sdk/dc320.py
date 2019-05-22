import serial
import re
import json
import time
import sys

DEBUG_OUT = True
SEQUENCE_DELAY = 0.1


# basic functions
def debug_print(msg):
    if DEBUG_OUT:
        print(msg)

def openDevice(port):
    return serial.Serial(port, 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, None, 0, 0)

def closeDevice(dev):
    dev.close()

def send(dev, msg):
    return dev.write(msg + "\r\n")

def recv(dev):
    msg = dev.readline()
    return msg

def cancel(dev):
    send(dev, "q")
    return isSuccess(recv(dev))
     
def sequence(msg):
    debug_print(msg)
    time.sleep(SEQUENCE_DELAY)
    
def buzzer1(dev):
    send(dev, "Z1")
    return isSuccess(recv(dev))

def buzzer2(dev):
    send(dev, "Z2")
    return isSuccess(recv(dev))


# check functions
def isAccept(msg):
    return msg[0] == "@"

def isBusy(msg):
    return msg[0] == "#"

def isError(msg):
    return msg[0] == "E"

def isResult(msg):
    return msg[0:2] == "{0"

def isGetoff(msg):
    return msg[0] == "F"

def isSuccess(msg):
    if isBusy(msg): return False;
    if isError(msg): return False;
    return True


# set functions
def setMode(dev, mode):
    send(dev, "M%s"%mode)
    return isSuccess(recv(dev))

def setTare(dev, tare):
    send(dev, "D0{:04.01f}".format(tare))
    return isSuccess(recv(dev))

def setSex(dev, sex):
    send(dev, "D1{}".format(sex+1))
    return isSuccess(recv(dev))

def setBodyType(dev, type):
    send(dev, "D2{}".format(type))
    return isSuccess(recv(dev))

def setBodyHeight(dev, height):
    send(dev, "D3{:05.01f}".format(height))
    return isSuccess(recv(dev))  

def setAge(dev, age):
    send(dev, "D4{}".format(age))
    return isSuccess(recv(dev))
    

# sequence functions    
def startMeasure(dev):
    send(dev, "G0")
    return isSuccess(recv(dev))

def waitResult(dev):
    msg = ""
    while True:
        msg = recv(dev)
        if not isSuccess(msg): return False, None
        if not isResult(msg): continue
        return True, msg

def waitGetoff(dev):
    while True:
        send(dev, "F2")
        msg = recv(dev)
        if not isSuccess(msg): return False
        if not isGetoff(msg): continue
        return True
    
def result_to_dict(result):
    data = "{"
    result = result.split(",")
    result = json.dumps(result)
    result = json.loads(result)
    for index in range(len(result)/2):
        key = result[index*2]
        val = result[index*2+1].replace("/","")
        if key == "ID": data += '"ID":%s,'%val; continue;
        if key == "DA": data += '"Data":%s,'%val; continue;
        if key == "TI": data += '"Time":%s,'%val; continue; 
        if key == "Bt": data += '"BodyType":%s,'%val; continue;
        if key == "GE": data += '"Sex":%s,'%(int(val)-1); continue;
        if key == "AG": data += '"Age":%s,'%val; continue;
        if key == "Hm": data += '"BodyHeight":%s,'%val; continue;
        if key == "Pt": data += '"Tare":%s,'%val; continue;
        if key == "Wk": data += '"BodyWeight":%s,'%val; continue;
        if key == "FW": data += '"BodyFatPer":%s,'%val; continue;
        if key == "fW": data += '"BodyFatMass":%s,'%val; continue;
        if key == "MW": data += '"LeanBodyMass":%s,'%val; continue;
        if key == "mW": data += '"MuscleMass":%s,'%val; continue;
        if key == "sW": data += '"MuscleScore":%s,'%val; continue;
        if key == "bW": data += '"BoneMass":%s,'%val; continue;
        if key == "wW": data += '"WaterMass":%s,'%val; continue;
        if key == "MI": data += '"BMI":%s,'%val; continue;
        if key == "Sw": data += '"StandardWeight":%s,'%val; continue;
        if key == "OV": data += '"DoO":%s,'%val; continue;
        if key == "IF": data += '"FatLevel":%s,'%val; continue;
        if key == "LP": data += '"LegPoint":%s,'%val; continue;
        if key == "rB": data += '"BMR":%s,'%val; continue;
        if key == "rJ": data += '"BMD":%s,'%val; continue;
        if key == "rA": data += '"BodyAge":%s,'%val; continue;
        if key == "RO": data += '"LaurelIndex":%s,'%val; continue;
        
    # to json
    data = data[:-1]
    data += "}"
    data = json.loads(data)
    
    # convert
    if not (data["Data"] is None): data["Data"] = "\"%s\""%data["Data"];
    if not (data["Time"] is None): data["Time"] = "\"%s\""%data["Time"];                
    return data

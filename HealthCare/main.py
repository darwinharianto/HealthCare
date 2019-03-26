import subprocess
import os
import binascii
import nfc
import nfcController as nfcctl
import commands
import buzzer
from time import sleep

#b = nfcctl.readNFC()
#nfcctl.createUser(a)
#nfcctl.logUser(a)
#nfcctl.updateWeight("aa", 22)

#a = nfcctl.exchangeBLE(b,"00000000-0000-0000-0000-000000000002")
#print(a)
buzzer.buzzer(4,2000,1,1)

configDirectory = "/home/pi/HealthCare/HealthCare/config.txt"

with open(configDirectory) as file:
    config = file.read()

print(config)
oldConfig = config
config = nfcctl.settingMode(config, "00000000-0000-0000-0000-000000000002")
if config is not None:
    buzzer.buzzer(4,2000,2,0.05)
    with open(configDirectory, mode="w") as file:
        file.write(config)

with open(configDirectory) as file:
    config = file.read()
    print("Written File: ",config)
    
sleep(10)

buzzer.buzzer(4,2000,3,0.05)

while True:
    a = commands.getoutput('lsusb')
    if "Sony" in a:
        userID = nfcctl.readNFC()
        print(userID)
	if userID is None:
	    continue
        if config == "Entrance":
            print("logging user")
            nfcctl.logUser(userID)
        elif config == "Application":
 	    print("create new user")
            nfcctl.createUser(userID)
        elif config == "Body Weight":
	    print("update user weight")
            weight = nfcctl.exchangeBLE(userID, "00000000-0000-0000-0000-000000000002")
            nfcctl.updateWeight(userID,weight)
        else:
            print("Error 404")
    else:
        userID = nfcctl.readByPN532()
        print(userID)
	if userID is None:
	    continue
        if config == "Entrance":
            print("logging user")
            nfcctl.logUser(userID)
        elif config == "Application":
 	    print("create new user")
            nfcctl.createUser(userID)
        elif config == "Body Weight":
	    print("update user weight")
            weight = nfcctl.exchangeBLE(userID, "00000000-0000-0000-0000-000000000002")
            nfcctl.updateWeight(userID,weight)
        else:
            print("Error 404")
    

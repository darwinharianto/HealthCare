import subprocess
import os
import binascii
import nfc
import nfcController as nfcctl
import commands
import buzzer
from time import sleep

buzzer.buzzer(4,2000,1,1)
sleep(5)
configDirectory = "/home/pi/HealthCare/HealthCare/config.txt"

with open(configDirectory) as file:
    config = file.read()

print(config)
oldConfig = config
while True:
    try:
	config = nfcctl.settingMode(config, "00000000-0000-0000-0000-000000000002")
        break
    except subprocess.CalledProcessError, e:
        print("Settting BLE Error")
        continue
 	
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
    else:
        try:
            userID = nfcctl.readByPN532()
        except subprocess.CalledProcessError, e:
            print("No data detected until timed out")
            continue
        
    if userID is None:
	continue
    if config == "In Entrance":
        print("logging user")
        nfcctl.loginUser(userID)
    elif config == "Out Entrance":
 	print("create new user")
        nfcctl.logoutUser(userID)
    elif config == "Application":
 	print("create new user")
        nfcctl.createUser(userID)
    elif config == "Body Weight":
	print("update user weight")
        weight = nfcctl.exchangeBLE(userID, "00000000-0000-0000-0000-000000000002")
        nfcctl.updateWeight(userID,weight)
    else:
        print("Error 404")


import subprocess
import os
import binascii
import nfc
import nfcController as nfcctl
import commands
import buzzer

#b = nfcctl.readNFC()
#nfcctl.createUser(a)
#nfcctl.logUser(a)
#nfcctl.updateWeight("aa", 22)

#a = nfcctl.exchangeBLE(b,"00000000-0000-0000-0000-000000000002")
#print(a)
buzzer.buzzer(4,2000,1,1)

while True:
    a = commands.getoutput('lsusb')
    if "Sony Corp" in a:
        userID = nfcctl.readNFC()
        print(userID)
	if userID is None:
	    continue
	a = commands.getoutput('lsusb')
        if ("Apple, Inc. Mighty Mouse" in a) & ("Apple, Inc. Aluminum Keyboard" in a):
            print("logging user")
            nfcctl.logUser(userID)
        elif "Apple, Inc. Mighty Mouse" in a:
 	    print("create new user")
            nfcctl.createUser(userID)
        elif "Apple, Inc. Aluminum Keyboard" in a:
	    print("update user weight")
            weight = nfcctl.exchangeBLE(userID, "00000000-0000-0000-0000-000000000002")
            nfcctl.updateWeight(userID,weight)
        else:
            print("Error 404")
    else:
        print("Error 404")

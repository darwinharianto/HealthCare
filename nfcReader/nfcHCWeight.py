import subprocess
import os
import re
import codecs
from time import sleep

print("tap NFC")
proc = subprocess.check_output(["nfc-poll"])

print("--------------------------------")
proc = str(proc)
a = proc.split(":")

nfcString = str(a[4:5])

nfcString = nfcString.replace(" ", "")
nfcString = nfcString.split("\\n")
nfcString = str(nfcString[0][2:])
print("User ID: %s" %nfcString)


print("acting as beacon")
a = ["sudo hciconfig hci0 reset", "sudo invoke-rc.d bluetooth restart","sudo hciconfig hci0 up","hciconfig" , "sudo hcitool -i hci0 cmd 0x08 0x0008 11 02 01 1a 0d ff 18 01 48 45 4c 4c 4f 57 4f 52 4c 44", "sudo hciconfig hci0 leadv 0"]


for i in a:
    os.system(i)

bleList = None
while True:
    print("search BLE")
    a = False
    bleList = subprocess.check_output(["sudo", "blescan"])
    bleList = bleList.split("Device")

    for i, str in enumerate(bleList):
        if "00000000-0000-0000-0000-000000000002" in str:
            print("find ble device")
            bleList = bleList[i]
            a = True
    if a == True:
        break;

    sleep(0.1)


bleList = bleList.split(" ")
bleList = bleList[2]
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
bleList = ansi_escape.sub('',bleList)
bleValue =  subprocess.check_output(["sudo", "gatttool", "-b", bleList, "--char-read", "--uuid=00000000-0000-0000-0000-000000000002"])

bleValue = bleValue.split("value: ")

bleValue = bleValue[1]
bleValue = bleValue.split(" ")
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

print("update user weight")
os.system("curl -X POST 52.193.188.33:8080/api/v1/weight -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\", \"weight\":%s}'" %(nfcString,str))

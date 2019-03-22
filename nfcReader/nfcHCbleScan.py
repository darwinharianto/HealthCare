
import subprocess
import re
import codecs
import os


bleList = subprocess.check_output(["sudo", "blescan"])

bleList = bleList.split("Device")


for i, str in enumerate(bleList):
	if "00000000-0000-0000-0000-000000000002" in str:
		bleList = bleList[i]

bleList = bleList.split(" ")
bleList = bleList[2]
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
bleList = ansi_escape.sub('',bleList)
bleValue =  subprocess.check_output(["sudo", "gatttool", "-b", bleList, "--char-read", "--uuid=00000000-0000-0000-0000-000000000002"])

bleValue = bleValue.split("value: ")

bleValue = bleValue[1]
bleValue = bleValue.split(" ")
print(bleValue)
#######need fix
breakindex = None
for i, str in enumerate(bleValue):
	breakindex = i
	if not str.isdigit():
		break
bleValue = bleValue[0:breakindex]
str = ""
for i in bleValue:
	str += codecs.decode(i, "hex_codec")

print(str)




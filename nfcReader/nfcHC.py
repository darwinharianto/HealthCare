
import subprocess
import os

print("tap nfc")
proc = subprocess.check_output(["nfc-poll"])

print("--------------------------------")
proc = str(proc)
a = proc.split(":")

b = str(a[4:5])

b = b.replace(" ", "")
b = b.split("\\n")
b = str(b[0][2:])
print("user ID: %s" %b)

print("send Data to server")
a = ("curl -X POST 52.193.188.33:8080/api/v1/add -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\", \"name\":\"sawada\", \"io\":\"0\"}'" %b)

os.system(a)

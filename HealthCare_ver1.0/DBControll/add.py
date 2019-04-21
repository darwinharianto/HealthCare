from http import WebAPI
from nfc import PN532

nfc = PN532()

# read id
print("touch id...")
id  = nfc.read_wait()
print(id)

# create json
json = { "ID": id, "name": "sample", "io": False }

# send server
WebAPI.post("52.193.188.33", 8080, "apply", json)

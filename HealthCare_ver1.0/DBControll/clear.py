from http import WebAPI
from nfc import PN532

nfc = PN532()

# read id
print("touch id...")
id  = nfc.read_wait()

# create json
json = {
    "ID": '%s'%id,
    "Data": '"000000"',
    "Time": '"00:01"',
    "BodyType": 1,
    "Sex": 0,
    "Age": 0,
    "BodyHeight":0,
    "Tare":0.0,
    "BodyWeight":0.0,
    "BodyFatPer":0.0,
    "BodyFatMass":0.0,
    "LeanBodyMass":0.0,
    "MuscleMass":0.0,
    "MuscleScore":0,
    "BoneMass":0.0,
    "WaterMass":0.0,
    "BMI":0.0,
    "StandardWeight":0.0,
    "DoO":0.0,
    "FatLevel":0,
    "LegPoint":0,
    "BMR":0,
    "BMD":0,
    "BodyAge":0,
    "LaurelIndex":0
    }

# send server
WebAPI.post("52.193.188.33", 8080, "body_scale", json)

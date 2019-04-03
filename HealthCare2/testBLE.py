from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)


p = btle.Peripheral("67:58:96:cc:dd:d6", btle.ADDR_TYPE_RANDOM)
p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID( "FFE0" )
ch = svc.getCharacteristics()[0]
print(ch.valHandle)

p.writeCharacteristic(ch.valHandle+1, "\x01\x00")

while True:
    if p.waitForNotifications(1.0):
        # handleNotification() was called
        continue

    print("Waiting...")
    # Perhaps do something else here

import subprocess
import os
import binascii
import nfc

class MyCardReader(object):

    def on_connect(self, tag):
        print "detected"
        self.idm = binascii.hexlify(tag.idm)
        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()

b = ""
if __name__ == '__main__':
    cr = MyCardReader()
    while True:
        try:
            print "touch card:"
            cr.read_id()
            print "released"
            print cr.idm
            b = cr.idm
            break
        except AttributeError as e:
            print(e)
            break

print("User ID: %s" %b)

print("User logger send")
a = ("curl -X POST 52.193.188.33:8080/api/v1/io -H \"Accept: application/json\" -H \"Content-Type: application/json\" -d '{\"id\": \"%s\"}'" %b)
os.system(a)


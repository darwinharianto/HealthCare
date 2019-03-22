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

if __name__ == '__main__':
    cr = MyCardReader()
    while True:
        try:
            print "touch card:"
            cr.read_id()
            print "released"
            print cr.idm
        except AttributeError as e:
            print(e)
            break

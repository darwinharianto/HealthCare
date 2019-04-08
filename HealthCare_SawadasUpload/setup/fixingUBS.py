import re
import sys
import subprocess


args = sys.argv
if not len(args) == 3:
	print("Invalid argument.")
	sys.exit()

srcName = args[1]
dstName = args[2]

cmd = "lsusb -v"
ret = subprocess.check_output(cmd.split())
ret = ret.split("\n")

vendorIDs = [s for s in ret if re.match(" *idVendor *", s)]
productIDs = [s for s in ret if re.match(" *idProduct *", s)]

targetIndex = None
for i, vendorID in enumerate(vendorIDs):
	if srcName in vendorID:
		targetIndex = i

vendorIDLine = vendorIDs[targetIndex]
productIDLine = productIDs[targetIndex]

vendorID = re.search("0x\w\w\w\w", vendorIDLine).group(0)
productID = re.search("0x\w\w\w\w", productIDLine).group(0)
print("VendorID   : %s"%vendorID)
print("ProductID  : %s"%productID)


str = "KERNEL==\"*\",ATTRS{idVendor}==\"%s\",ATTRS{idProduct}==\"%s\",GROUP=\"tty\",SYMLINK+=\"%s\"\r\n"%(vendorID[2:], productID[2:], dstName)
with open("/etc/udev/rules.d/99-com.rules", "a") as f:
	f.write(str)



""" 
sample

1.check device vendor name (CMD: lsusb -v | grep idVendor)
2.execute this program (CMD: python FixingUSB.py vendorName fixingDeviceName)
3.usb device reconnecting
4.check device name (ls /dev/ | grep changedName)

"""

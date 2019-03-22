import time
import os


while True:
    os.system('/opt/vc/bin/vcgencmd measure_temp')
    time.sleep(0.2)

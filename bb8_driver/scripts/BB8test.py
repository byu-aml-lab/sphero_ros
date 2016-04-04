#!/usr/bin/python
from bluepy import btle
import struct
import time
from bb8_driver import BB8_driver
import sys
bb8 = BB8_driver.Sphero()
bb8.connect()


bb8.start()
time.sleep(2)
bb8.set_rgb_led(255,0,0,0,False)
time.sleep(1)
bb8.set_rgb_led(0,255,0,0,False)
time.sleep(1)
bb8.set_rgb_led(0,0,255,0,False)
time.sleep(3)
bb8.join()
time.sleep(3)
response = 0
bb8.set_stablization(True, response)
print "stabilization " + str(response)
time.sleep(3)
bb8.set_heading(45, response)
print "heading " + str(response)
time.sleep(3)
bb8.roll(100, 90, 1, response)
print "rool " + str(response) 
bb8.disconnect()
sys.exit(1)


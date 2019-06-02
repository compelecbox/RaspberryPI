#!/usr/bin/env python
# coding: latin-1
# By Ralph Beardmore Jan 2017 for PI 3
# this is a temperature control. It runs in Python 2.x so code accordingly
# this is designed for NPN transistor and is normally OFF

# Import the libary functions we need
import RPi.GPIO as GPIO
import time
import subprocess

# Set which GPIO pins the fan output and power switch inputs are connected to
fanOUT = 8  #pin 3 = GPIO channel 8 see mode
fanPower = False

# configure the input and output pins
GPIO.setmode(GPIO.BOARD)                 # GPIO mode - BCM = channel, BOARD= pin number
GPIO.setup(fanOUT, GPIO.OUT)             # fan control variable
                   

# Map the on/off state to nicer names for display
dName = {}                        # make a list
dName[True] = 'ON '
dName[False] = 'OFF'

 
# CPU temperature monitor, all temperatures in centigrade!
pathSensor = '/sys/class/thermal/thermal_zone0/temp'    # File path used to read the temperature
readingMultiplier = 0.001                          # Value to multiply the reading by for user display
tempHigh = 60000                                        # Reading at which the fan(s) will be started (same units as file)
tempLow = 50000                                         # Reading at which the fan(s) will be stopped (same units as file)
interval = 2                                            # Time in seconds between readings in seconds

print '\nFAN TURNS ON  AT ', int(tempHigh * readingMultiplier)
print '\nFAN TURN OFF AT ', int(tempLow * readingMultiplier)
print '\n interval = ', interval, ' seconds'


# we will use a try loop so that it will exit when 'ctrl' + c is pressed and program ends gracefully, resetting GPIO
try:
    # initialise fan by making it switch on for 5 seconds
    print '\nFan test 5 seconds'
    GPIO.output([fanOUT], GPIO.HIGH)
    time.sleep(5)
    GPIO.output([fanOUT], GPIO.LOW) # just so we know everything works!
       
    print '\nCPU Fan Control is now ON. Press ctrl+c to exit' # raw_input('Fan Controller is ON Press [Enter] to continue')
    while True:
        # Read the temperature in C from the operating system
        fSensor = open(pathSensor, 'r')
        reading = float(fSensor.read())
        fSensor.close()

        # control CPU fan by comparing temperature with preset variables tempHigh, tempLow
        if fanPower:
            if reading <= tempLow:
                GPIO.output([fanOUT], GPIO.LOW)
                fanPower = False
                # We have cooled down enough, turn the fans off
	else:
            if reading >= tempHigh:
                GPIO.output([fanOUT], GPIO.HIGH)
                fanPower = True
                # We have warmed up enough, turn the fans on

    	temp = reading * readingMultiplier

       
	# display the temperature to the console
	print str(temp), dName[GPIO.input(fanOUT)]

	# Wait a while
	time.sleep(interval)

except KeyboardInterrupt:
    # 'CTRL'+c to exit, turn off the drives and release the GPIO pins
    #print 'Terminated'
    raw_input('\nFan controller is now OFF! \n')
    GPIO.cleanup()                     #reset the GPIO ports


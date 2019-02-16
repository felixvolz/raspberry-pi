#http://www.toptechboy.com/tutorial/raspberry-pi-lesson-29-configuring-gpio-pins-as-inputs/
#https://raspi.tv/2014/rpi-gpio-update-and-detecting-both-rising-and-falling-edges
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os
import dbus
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from datetime import datetime
import sys
import logging
import time
timestr = time.strftime("%Y%m%d")

logging.basicConfig(filename='pusbutton-'+timestr+'.log',format='%(asctime)s %(message)s',level=logging.INFO)
logging.info('push_button.py starting up...') 

#global variables
VIDEO_PATH = Path("./Videos/big_buck_bunny_720p_1mb.mp4")
player = None
isPlaying = False
isButtonDepressed = False

#callback - invoked on completion of video
#resets isPlaying check to false
def playerExitEventCallback():
    global isPlaying
    isPlaying = False

#callback - we are only interested in RELEASE of button, but need to make sure starts from PRESSED state
#1. plays video IFF video not already playing AND button released
#2. registers callback that tracks if video has copmleted or not
def button_callback(channel):
    global player
    global isPlaying
    global isButtonDepressed
    
    if GPIO.input(12):     # if port 12 == 1
        #rising edge indicates that button was released OR power surge (Ive noticed lightswitch triggers RISING)
        #print ("Rising edge detected on 12", datetime.now().strftime("%H:%M:%S.%f\n\n") )
        if(isButtonDepressed == True):
            isButtonDepressed = False
            print ("button let go") #we check that the button was prev depressed and now released
        else:
            print("false positive??")
            return #if rising edge AND button NOT depressed then must be false positive
    else:                  # if port 25 != 1
        #print ("Falling edge detected on 12",datetime.now().strftime("%H:%M:%S.%f"))
        isButtonDepressed = True
        print ("button depressed")
        return #if button depressed, dont play video
        
    if(not isPlaying):
        isPlaying = True
        player = OMXPlayer(VIDEO_PATH, args='-o hdmi')
        player.exitEvent += lambda _, exit_code: playerExitEventCallback()
        player.play()
        logging.info("  video now playing!")
        print("  video now playing!")
    else:
        logging.info("  video not playing, prob already playing!")
        print("  video not playing, prob already playing!")
                 
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 12 to be an input pin and set initial value to be pulled high 

# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
#fv - RISING detects button release,
#GPIO.add_event_detect(12,GPIO.RISING,callback=button_callback,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(12,GPIO.BOTH,callback=button_callback)

message = input("Press enter to quit\n\n") # Run until someon,e presses enter
GPIO.cleanup() # Clean up

#15/02 - had issues wiht lightswith/poewr surge triggering false positeive
#I observed lightswitch would trigger a GPIO.RISING only so updated callback to GPIO.BOTH and code to check if
#if button depressed AND RISING THEN play video (i.e ignore false GPIO.RISING)
#OLD - GPIO starts pulled up, button press will GROUND, we detect RISING (button release)
#OLD - having pull down, detect RISING AND input != low -> a) triggers movie on downpress and b) prevents false positive


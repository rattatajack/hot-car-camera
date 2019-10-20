import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import atexit
import time
import _thread

from RPLCD import CharLCD
GPIO.setmode(GPIO.BOARD)
dataPins = [33, 15,13,11]

GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
    
 
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16,rows=2,pin_rs=37, pin_e=35, pins_data=[33, 15,13,11])

shouldDisplayWIFIName = True

        
def blankScreen():
    lcd.cursor_pos = (0,0)
    lcd.write_string("                ")
    lcd.cursor_pos = (1,0)
    lcd.write_string("                ")

def create(WifiName):
    global shouldDisplayWIFIName
    while(shouldDisplayWIFIName):

        lcd.cursor_pos = (0,0)
        lcd.write_string("Connect to WiFi:")
        lcd.cursor_pos = (1,0)
        lcd.write_string(WifiName)
    
def addContact(contactName):
    global shouldDisplayWIFIName
    print("called")
    shouldDisplayWIFIName = False
    blankScreen()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Added Contact:")
    lcd.cursor_pos = (1,0)
    lcd.write_string(contactName)
    time.sleep(2)
    shouldDisplayWIFIName = False

def restOfDef():
    print("running")
    time.sleep(4)
    addContact("Ivor Page")
    

_thread.start_new_thread(create("TESTWIFINAME"), ())
_thread.start_new_thread(restOfDef(), ())
lcd.close(clear=True)
GPIO.cleanup()
#GPIO.cleanup()
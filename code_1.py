import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD
import time


lcd = Adafruit_CharLCD()
lcd.begin(16, 1)
lcd.clear()
lcd.message("Hello World")

LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(1)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.cleanup()


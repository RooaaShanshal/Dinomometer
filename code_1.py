import RPi.GPIO as GPIO
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from hx711 import HX711
import sys
import time

LED_1 = 21 # green
LED_2 = 25 # green
LED_3 = 20 # yellow
LED_4 = 19 # yellow
LED_5 = 26 # red

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_1, GPIO.out)
GPIO.setup(LED_2, GPIO.out)
GPIO.setup(LED_3, GPIO.out)
GPIO.setup(LED_4, GPIO.out)
GPIO.setup(LED_4, GPIO.out)

I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 16

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

threshold = 0.5 #CHANGE

# Code below from: https://github.com/j-dohnalek/hx711py/blob/master/calibration.py

# START OF REFERENCED CODE
hx = HX711(6, 5, 128, 'A')


def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    lcd.clear()
    print("Bye!")
    sys.exit()

def setup():
    """
    code run once
    """
    print("Initializing.\n Please ensure that the scale is empty.")
    scale_ready = False
    while not scale_ready:
        if (GPIO.input(hx.DOUT) == 0):
            scale_ready = False
        if (GPIO.input(hx.DOUT) == 1):
            print("Initialization complete!")
            scale_ready = True

def calibrate():
    readyCheck = input("Remove any items from scale. Press any key when ready.")
    offset = hx.read_average()
    print("Value at zero (offset): {}".format(offset))
    hx.set_offset(offset)
    print("Please place an item of known weight on the scale.")

    readyCheck = input("Press any key to continue when ready.")
    measured_weight = (hx.read_average()-hx.get_offset())
    item_weight = input("Please enter the item's weight in grams.\n>")
    scale = int(measured_weight)/int(item_weight)
    hx.set_scale(scale)
    print("Scale adjusted for grams: {}".format(scale))

def get_value(time):
    grip = []
    lcd.putstr("Hold down!")
    while(time>0):
        grip.append(hx.get_grams())
        time -= 1
    lcd.move_to(3, 1)
    lcd.putstr("Let go!")
    lcd.clear()
    return max(grip)

def dino():
    numTests = int(input("Input number of tests desired"))
    value = 0
    LED_counter = 1
    totalTests = numTests
    while(numTests>0):
        measure = get_value(3)
        while(measure<=threshold):
            #no response from dynomometer
            measure = get_value(3)
        value+=measure
        LED = "LED_"+LED_counter # String? maybe it shouldn't be
        GPIO.output(LED, GPIO.HIGH)
        numTests -= 1
    message_1 = "Number of tests conducted:"+totalTests 
    message_2 = "Average force: "+ value/totalTests
    lcd.clear()
    lcd.putstr(message_1)
    lcd.move_to(3, 1)
    lcd.putstr(message_2)
    time.sleep(10)
    # GPIO.output(LED_1, GPIO.LOW)
    # GPIO.output(LED_2, GPIO.LOW)
    # GPIO.output(LED_3, GPIO.LOW)
    # GPIO.output(LED_4, GPIO.LOW)
    # GPIO.output(LED_5, GPIO.LOW)
    # GPIO.cleanup()



def loop():
    """
    code run continuously
    """
    try:
        prompt_handled = False
        while not prompt_handled:
            #val = hx.get_grams()
            #hx.power_down()
            #time.sleep(.001)
            #hx.power_up()
            #print("Item weighs {} grams.\n".format(val))
            choice = input("Please choose:\n"
                           "[1] Recalibrate.\n"
                           "[2] Start the Dinomometer\n"
                           "[0] Clean and exit.\n>")
            if choice == "1":
                calibrate()
            elif choice == "2":
                dino()
                #print("\nOffset: {}\nScale: {}".format(hx.get_offset(), hx.get_scale()))# CHANGE 
            elif choice == "0":
                prompt_handled = True
                cleanAndExit()
            else:
                print("Invalid selection.\n")
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

#END OF REFERENCED CODE
        





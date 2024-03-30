import gpiozero import LED
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from hx711 import HX711
import sys
import time

LED = [LED(21), LED(25), LED(20), LED(19), LED(26)]

I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 16

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

hx = HX711(6, 5, 128, 'A')

Offset = 0
Ratio = 1

def cleanAndExit():
    lcd.clear()
    lcd.putstr("Cleaning up...")
    print("Cleaning up...")
    for led in LED:
        led.off()
    lcd.clear()
    lcd.putstr("Shutting down, Bye!")
    time.sleep(5)
    lcd.clear()
    print("Bye!")


def calibrate():
    lcd.clear()
    lcd.putstr("Remove items from strain gauge, press any key to continue")
    readyCheck = input("Remove items from Strain gauge, press any key to continue")
    Offset = int(hx.get_raw_data(5))/5
    lcd.clear()
    lcd.putstr("place an object w/ known weight, press any key when ready")
    readyCheck = input("Place an object with a known weight on strain gauge, press any key when ready")
    measured = (hx.get_raw_data(5))/5
    print("Done")
    lcd.clear()
    lcd.putstr("Enter known weight into terminal")
    weight = int(input("Enter known weight of object here"))
    Ratio = (int(measured)-Offset)/weight
    lcd.clear()
    lcd.putstr("Calibration complete")

def get_kg(value):
    return value/Ratio

def get_average(time):
    return get_kg(sum(hx.get_raw_data(time))/time)


def dino():
    lcd.clear()
    lcd.putstr("Enter number of tests in terminal")
    numTests = int(input("Input number of tests desired"))
    value = 0
    LEDcounter = 0
    testCounter = numTests

    while(testCounter>0):
        lcd.clear()
        lcd.putstr("Hold strain gauge, press any key to continue")
        readyCheck = input("Hold strain gauge, press any key to continue")
        measured = get_average(3)
        lcd.clear()
        lcd.putstr("Measurement taken!")
        value+=measured
        time.sleep(5)
        lcd.clear()
        lcd.putstr("Force: "+str(measured))

        led_now = LED[LEDcounter]
        led_now.on()

        LEDcounter += 1
        testCounter -= 1

        time.sleep(5)

    message_1 = "Number of tests conducted:"+str(numTests)+"\n" 
    message_2 = "Average force: "+ str(value/numTests)+"\n"
    print(message_1)
    print(message_2)
    lcd.clear()
    lcd.putstr(message_1)
    lcd.putstr(message_2)



def loop(): #code run continuously
    try:
        prompt_handled = False
        while not prompt_handled:
            choice = input("Please choose:\n"
                           "[1] Calibrate.\n"
                           "[2] Start the Dinomometer\n"
                           "[0] Clean and exit.\n>")
            if choice == "1":
                calibrate()
            elif choice == "2":
                dino()
            elif choice == "0":
                prompt_handled = True
                cleanAndExit()
            else:
                print("Invalid selection.\n")
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

        

loop()



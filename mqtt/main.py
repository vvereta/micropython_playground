import machine
import mp_i2c_lcd1602
from machine import Pin, I2C
#from lcd_api import LcdApi
#from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)       #initializing the I2C method for ESP8266
lcd = mp_i2c_lcd1602.LCD1602(i2c,I2C_ADDR)
#lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

#lcd.putstr("0123456789\n01234567890123456789")
lcd.print("0123456789\n0123456789abcdefg")
#while True:
#    lcd.putstr("I2C LCD Tutorial")
#    sleep(2)
#    lcd.clear()
#    lcd.putstr("Lets Count 0-10!")
#    sleep(2)
#    lcd.clear()
#    for i in range(11):
#        lcd.putstr(str(i))
#        sleep(1)
#        lcd.clear()

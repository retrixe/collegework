# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for monochromatic character LCD on Raspberry Pi"""
import sys
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_d7 = digitalio.DigitalInOut(board.D7)
lcd_d6 = digitalio.DigitalInOut(board.D8)
lcd_d5 = digitalio.DigitalInOut(board.D25)
lcd_d4 = digitalio.DigitalInOut(board.D24)
lcd_en = digitalio.DigitalInOut(board.D23)
lcd_rs = digitalio.DigitalInOut(board.D18)
lcd_backlight = digitalio.DigitalInOut(board.D4)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

line1 = bytes.fromhex(sys.argv[1]).decode('ascii')
line2 = bytes.fromhex(sys.argv[2]).decode('ascii')

lcd.message = line1 + "\n" + line2

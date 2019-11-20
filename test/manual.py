import sys
sys.path.append("..")

import serial
import RPi.GPIO as GPIO

if __name__ == "__main__":

    gpio_pins = {'m0': 16, 'm1': 18, 'aux': 12}

    ser = serial.Serial('/dev/ttyS0', 9600)

    

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(gpio_pins['m0'], GPIO.OUT)
    GPIO.setup(gpio_pins['m1'], GPIO.OUT)
    GPIO.setup(gpio_pins['aux'], GPIO.IN)

    GPIO.output(gpio_pins['m0'], 1)
    GPIO.output(gpio_pins['m1'], 1)

    time.sleep(1)

    req = bytearray([0xC1, 0xC1, 0xC1])
    ser.write(req)

    print(ser.read(6))
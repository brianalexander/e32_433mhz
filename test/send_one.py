import sys
sys.path.append('..')

from message import Message
from transceiver import Transceiver
import serial
import time

if __name__ == "__main__":
    print('in main')
    transceiver = serial.Serial('/dev/ttyUSB0', 19200)

    transceiver.rts = 1
    transceiver.dtr = 1
    # message = Message(3, data=[11, 12])
    time.sleep(3)
    # transceiver.write(message)
    msg = bytearray([0xC1, 0xC2, 0xC3])
    transceiver.write(b'hello')
    #transceiver.read(1)

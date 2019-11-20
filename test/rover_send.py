import sys
sys.path.append("..")

import serial
from message import Message
from transceiver import Transceiver


if __name__ == "__main__":
    # 115200 or 9600
    transceiver = Transceiver(
        '/dev/ttyUSB0', 19200)
    message = Message(3, data=[11, 12])
    print(message.checksum)
    transceiver.write(message)

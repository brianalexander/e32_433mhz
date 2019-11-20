import serial
from message import Message
from transceiver import Transceiver
import sys
sys.path.append("..")

if __name__ == "__main__":
    # 115200 or 9600
    transceiver = Transceiver(
        '/dev/ttyUSB0', 19200)
    print(transceiver.get_message())

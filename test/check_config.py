import sys
sys.path.append("..")

import serial
from transceiver import Transceiver


if __name__ == "__main__":
    transceiver = Transceiver('/dev/ttyUSB0', 9600)
    print(transceiver.configuration)
    print(transceiver.m0)
    print(transceiver.m1)

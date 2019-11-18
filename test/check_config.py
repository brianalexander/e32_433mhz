import sys
sys.path.append("..")

import serial
from transceiver import Transceiver


if __name__ == "__main__":
    transceiver = Transceiver(path='/dev/ttyUSB0')
    print(transceiver.configuration)

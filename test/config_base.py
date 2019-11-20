import sys
sys.path.append("..")

import serial
from transceiver import GPIOTransceiver


if __name__ == "__main__":
    # 115200 or 9600
    transceiver = GPIOTransceiver('/dev/ttyUSB0', 115200)
    print(transceiver.configuration)

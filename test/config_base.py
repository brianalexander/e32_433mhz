import sys
sys.path.append("..")
from transceiver import GPIOTransceiver
import serial

if __name__ == "__main__":
    # 115200 or 9600
    transceiver = GPIOTransceiver(
        '/dev/ttyS0', 115200, {'m0': 16, 'm1': 18, 'aux': 12})
    print(transceiver.configuration)

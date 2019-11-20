from transceiver import GPIOTransceiver
import serial
import sys
sys.path.append("..")


if __name__ == "__main__":
    # 115200 or 9600
    transceiver = GPIOTransceiver(
        '/dev/ttyUSB0', 115200, {'m0': 16, 'm1': 18, 'aux': 12})
    print(transceiver.configuration)

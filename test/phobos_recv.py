import sys
sys.path.append("..")
from transceiver import GPIOTransceiver
from message import Message
import serial

if __name__ == "__main__":
    # 115200 or 9600
    transceiver = GPIOTransceiver(
        '/dev/serial0', 19200, {'m0': 23, 'm1': 24, 'aux': 18})
    print('Waiting for message...')
    print(transceiver.get_message())
    # message = Message(3, data=[11, 12])
    # transceiver.write(message)

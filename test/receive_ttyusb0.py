from ..message import Message
from ..transceiver import Transceiver


def gps(lat, lng):
    print("lat", lat, "long", lng)


def dispatch_to_rover(msg):
    op_to_func = {
        3: gps
    }

    op_to_func[msg.op_code](*msg.data)


if __name__ == "__main__":
    transceiver = Transceiver(path='/dev/ttyUSB0')

    while(True):
        print('waiting for message...')
        dispatch_to_rover(transceiver.get_message())

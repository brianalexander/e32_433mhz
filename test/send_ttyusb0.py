from ..message import Message
from ..transceiver import Transceiver


def gps(lat, lng):
    print("lat", lat, "long", lng)


def dispatch_to_base_station(msg):
    op_to_func = {
        3: gps
    }

    op_to_func[msg.op_code](*msg.data)


if __name__ == "__main__":
    print('in main')
    transceiver = Transceiver(path='/dev/ttyUSB0')

    message = Message(3, data=[11, 12])
    transceiver.write(message)

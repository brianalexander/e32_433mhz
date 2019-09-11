from struct import pack, unpack
import time
import serial

# Define the format of messages here
OP_TO_FMT_STR = {
    1: "! 10s",  # String with 10 characters
    2: "! 5I",  # 5 integers
    3: "! 2f"  # 2 floats - GPS
}


class Message:

    def __init__(self, op_code=None, data=None):
        '''
        Creates a new message object.

        Creates a new message object given an op-code, data, and a format type
        for the data that can be sent using the Transceiver object.

        Parameters:
        op_code (byte): Code that defines the message type.
        pack_fmt (string): Format string provided to struct.pack.
        data (bytearray): data to be sent over the line.

        Returns:
        Nothing.
        '''
        self._op_code = op_code
        self._pack_fmt = OP_TO_FMT_STR[op_code]
        self._data = data
        self._byte_string = self._build_byte_string()
        self._checksum = self._get_checksum()

    @property
    def op_code(self):
        return self._op_code

    @property
    def data(self):
        return self._data

    @property
    def checksum(self):
        return self._checksum[0]

    @property
    def bytes(self):
        return self._byte_string + self._checksum

    def _get_checksum(self):
        length = len(self._byte_string)
        individual_bytes = unpack("{}B".format(length), self._byte_string)
        checksum = individual_bytes[0]
        for current_byte in individual_bytes[1:]:
            checksum = checksum ^ current_byte

        return pack('B', checksum)

    def _build_byte_string(self):
        op_code = pack('B', self._op_code)
        data = pack(self._pack_fmt, *self._data)
        length = pack('B', len(data))

        byte_string = op_code+length+data

        return byte_string

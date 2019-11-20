from struct import pack, unpack
import time
import serial
from message import OP_TO_FMT_STR
from message import Message

# from abc import ABC, abstractmethod


class Transceiver(object):
    AIR_DATA_RATES = {
        0: "0.3k",
        1: "1.2k",
        2: "2.4k",
        3: "4.8k",
        4: "9.6k",
        5: "19.2k",
        6: "19.2k",
        7: "19.2k"
    }

    MIN_FREQUENCY = 410

    def __init__(self, path, baudrate):
        # Set serial object
        self._serial = serial.Serial(path, baudrate, timeout=None)
        print('serial device created')
        self._unique_initalization()
        self._fininalize_initialization()

    #
    # Properties
    #
    @property
    def m1(self):
        return self._serial.rts

    @m1.setter
    def m1(self, value):
        self._serial.rts = value

    @property
    def m0(self):
        return self._serial.dtr

    @m0.setter
    def m0(self, value):
        self._serial.dtr = value

    @property
    def aux(self):
        return self._serial.cts

    @property
    def is_available(self):
        return (not self.aux)

    @property
    def version(self):
        self._set_config_mode()
        req = bytearray([0xC3, 0xC3, 0xC3])
        self._serial.write(req)
        resp = self._serial.read(4)
        self._set_transmission_mode()

        return ", ".join(["0x{0:02X}".format(byte)for byte in resp])

    @property
    def configuration(self):
        # Get configuration information from E32
        self._set_config_mode()
        req = bytearray([0xC1, 0xC1, 0xC1])
        self._serial.write(req)
        print('waiting for configuration')
        resp = self._serial.read(6)
        print('got configuration')
        self._set_transmission_mode()

        # Save last received configuration
        self._last_config = resp

        # Parse confiugration byte-string to dictionary
        current_config = {}

        # Add raw configuration string to dict
        current_config['hex'] = ", ".join(
            ["0x{0:02X}".format(byte)for byte in resp])

        if (resp[0] == 0xC0):
            current_config['save_on_shutdown'] = True
        else:
            current_config['save_on_shutdown'] = False

        if (((resp[1] & resp[2]) == 0x0) or ((resp[1] & resp[2]) == 0xF)):
            current_config['broadcast'] = True
        else:
            current_config['broadcast'] = False
            current_config['address'] = "0x{0:02X}".format(
                resp[1])+"0x{0:02X}".format(resp[2])

        bit_mask = 7
        adr_key = resp[3] & bit_mask

        current_config['air_data_rate'] = self.AIR_DATA_RATES[adr_key]
        current_config['frequency'] = str(
            self.MIN_FREQUENCY + resp[4]) + " Mhz"

        print('end config')
        return current_config

    #
    # Send/Receive Messages
    #
    def write(self, message):
        self._wait_until_ready()
        self._serial.write(message.bytes)

    def read(self, num_bytes):
        data = self._serial.read(num_bytes)
        # print('Received..', data)
        return data

    def _get_first_byte(self):
        return self.read(1)
        # self._wait_until_ready()
        # buf_byte = None

        # # If state is good since last read, clear the null-bytes
        # # and return the first data byte
        # if(self._state == 0):
        #     print('state good')
        #     while(True):
        #         print('waiting for byte')
        #         buf_byte = self._serial.read(1)
        #         print('byte read', buf_byte)
        #         if(buf_byte != b'\x00'):
        #             print('breaking')
        #             break
        #     print('returning first byte', buf_byte)
        #     return buf_byte

        # # If the state is bad, begin resetting the state. First, clear
        # # all bad bytes from previous message, then set the state to correcting.
        # while(self._state == 2):
        #     buf_byte = self._serial.read(1)
        #     if(buf_byte is 0x00):
        #         self._state == 1

        # # Next remove all null bytes and set the mode back to good. Return first
        # # good byte to the user.
        # while(self._state == 1):
        #     buf_byte = self._serial.read(1)
        #     if(buf_byte is not 0x00):
        #         self._state = 0
        #         return buf_byte

    def get_message(self):
        # get the op_code
        op_code = unpack('B', self.read(1))[0]
        print("opcode", op_code)

        # get the length
        length = unpack('B', self.read(1))[0]
        print("length", length)

        # get the data
        data = unpack(OP_TO_FMT_STR[op_code], self.read(length))
        print("data", data)

        # get the checksum
        checksum = unpack('B', self.read(1))[0]
        print("recv_checksum", checksum)

        # create a message object from given data
        message = Message(op_code=op_code, data=data)

        # if the data is invalid, throw an error
        # The XOR (^) of two identical numbers will result in 0
        # Therefore, if the checksum from rebuilding the message
        # XOR'd with the checksum sent over the line is non-zero,
        # data was corrupted.
        print('built_checksum', message.checksum)
        if(message.checksum ^ checksum):
            # throw error
            # Set state to bad (2)
            print('Invalid data')

        # all clear, return message object to the user
        return message

    #
    # Change Device Settings
    #
    def _set_config_mode(self):
        if(self.mode != "config"):
            print('setting config mode')
            self._wait_until_ready()
            time.sleep(0.02)
            self.m0 = False
            self.m1 = False
            self.mode = "config"
            self._wait_until_ready()
            time.sleep(0.02)
            print('finished setting mode')

    def _set_transmission_mode(self):
        if(self.mode != "transmission"):
            print('setting transmit mode:')
            self._wait_until_ready()
            time.sleep(0.02)
            self.m0 = True
            self.m1 = True
            self.mode = "transmission"
            self._wait_until_ready()
            time.sleep(0.02)
            print('finished setting mode')


    def set_frequency(self, freq):
        adj_freq = freq - self.MIN_FREQUENCY
        if(adj_freq <= 0x1F and adj_freq >= 0x00):
            last_config = self._last_config
            self._set_config_mode()
            req = bytearray(
                [0xC2, last_config[1],
                 last_config[2],
                 last_config[3],
                 adj_freq,
                 last_config[5]]
            )
            self._serial.write(req)
            self._set_transmission_mode()

    def set_air_data_rate(self, data_rate):
        if(data_rate <= 0x5 and data_rate >= 0x00):
            last_config = self._last_config
            self._set_config_mode()
            req = bytearray(
                [0xC2,
                 last_config[1],
                 last_config[2],
                 last_config[3],
                 data_rate,
                 last_config[5]]
            )
            self._serial.write(req)
            self._set_transmission_mode()

    #
    # Utility methods -- NOT WORKING IMPLEMENTATION
    #
    def _wait_until_ready(self):
        '''
        Blocks execution of code until device is ready.
        '''
        while(not self.is_available):
            continue

    def _fininalize_initialization(self):
        # Default starting mode is transmission mode
        self.mode = "config"
        self._set_transmission_mode()

    def _unique_initalization(self):
        pass


# Current pinout on FTDI chip
# CTS := AUX
# RTS := M1
# DTR := M0


class GPIOTransceiver(Transceiver):
    def __init__(self, path, baudrate, gpio_pins):
        self.gpio_pins = gpio_pins
        super(GPIOTransceiver, self).__init__(path, baudrate)

    def __del__(self):
        self.GPIO.cleanup()

    def _unique_initalization(self):
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.gpio_pins['m0'], GPIO.OUT)
        GPIO.setup(self.gpio_pins['m1'], GPIO.OUT)
        GPIO.setup(self.gpio_pins['aux'], GPIO.IN)

        self.GPIO = GPIO

    #
    # Properties
    #
    @property
    def m1(self):
        return self.GPIO.input(self.gpio_pins['m1'])

    @m1.setter
    def m1(self, value):
        print(not value)
        self.GPIO.output(self.gpio_pins['m0'], not value)

    @property
    def m0(self):
        return self.GPIO.input(self.gpio_pins['m0'])

    @m0.setter
    def m0(self, value):
        print(not value)
        self.GPIO.output(self.gpio_pins['m0'], not value)

    @property
    def aux(self):
        return self.GPIO.input(self.gpio_pins['aux'])

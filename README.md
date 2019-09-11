# 433 Mhz Comms

Code for 433 Mhz backup communications channel for CSUF Titan Rover 2020 Competition Year.

### Prerequisites

[USB-to-Serial Converter](https://www.amazon.com/HiLetgo-FT232RL-Converter-Adapter-Breakout/dp/B00IJXZQ7C) or similar

[E32-433T30D](http://www.ebyte.com/en/product-view-news.aspx?id=108) or similar version

The pinout between the E32 and USB-to-Serial Converter is as follows:

| USB-to-Serial | E32 |
| ------------- | --- |
| M0            | DTR |
| M1            | RTS |
| AUX           | CTS |

## Running the tests

From the top level directory:

To listen for messages:

- sudo python3 -m test.receive
- sudo python3 -m test.receive_ttyusb0

To send messages:

- sudo python3 -m test.send
- sudo python3 -m test.send_ttyusb0

## Built With

[pyserial](https://pythonhosted.org/pyserial/)

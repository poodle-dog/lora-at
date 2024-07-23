# LoRaModule

This is a userspace Python application designed to control a LoRA radio made by REYAX. 

This module uses AT commands over a serial connection to control the modem and the flow of data to and from the host. 

The userspace driver relies on a serial filehandle (like `/dev/ttyUSB0`) to send and receive serial data. 

# Testing

The `socat` command line program is used to test the module's AT command set. 

`socat` sets up two fake, linked serial devices. The `LoRaModule()` class is given one `pty` device to communicate to; the other is driven by the test program. The test program ensures that the AT command set sent by the module matches the expected serial traffic. 




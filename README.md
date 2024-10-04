# LoRaModule

This is a Python module for controlling REYAX RYLR993 LoRA modules. 

These modules use AT commands over a serial connection to control the modem and the flow of data to and from the host. 

The application relies on a standard serial device file (like `/dev/ttyUSB0`) to communicate with the module. 

# Quickstart

The fastest way to demonstrate LoRA comms is to have two radios speak directly to one another in proprietary mode.

You will need:
- two FTDI USB/UART cables
- two RYLR993 modules 
- jumper wires
- a breadboard

Once you have properly connected FTDI cables to modules, start the receiver script by running:

```shell
> python3 examples/rx_prop.py /dev/ttyUSB0
```

This starts the server in one terminal console. Note that `/dev/ttyUSB0` may enumerate differently on your machine. 

```shell
> python3 examples/tx_prop.py /dev/ttyUSB1 hello 0
```

This sends the message `hello` over the radio connected to `/dev/ttyUSB1`, with a destination LoRA radio address of `0`. 

If all wiring is successfully connected, a message like the following should pop up into the console of your window running `rx_prop.py`:

```shell
$ python3 examples/rx_prop.py /dev/ttyUSB0
Starting LoRA Rx server
{'address': 0, 'length': 5, 'data': 'hello', 'rssi': -11, 'snr': 11}
```

Note that your values for `rssi` and `snr` will likely vary, as these values are environment-dependent. 

# Making an Echo Node

A simple echo server is used in `examples/rx_echo.py`. This is useful for testing transmission. To run it, execute:

```shell
$ python3 examples/rx_prop.py /dev/ttyUSB0
```

This will begin listening at LoRA address 101, and will echo back any messages received to the sending node. 

This can also be run at login via a `systemd` service; see `templates/lora.service` for a service declaration file. 

To run on a echo node system like a Raspberry Pi, run the following:

```shell
cp templates/lora.service /etc/systemd/system
systemctl enable lora.service
systemctl start lora.service
```

Note that some systems require `sudo` for copying into `/etc` or running `systemctl`. 

# Design

RYLR993 modules operate in one of two modes:

- a generic LoRAWAN mode, and 
- a proprietary LoRA Mode

"Proprietary" in this case appears to mean that the node is running some of REYAX's custom protocol engines for driving a Semtech radio. It does not appear to be doing any special sauce on the LoRA transmission side. 

Correspondingly, there are two classes within `lora_module.py` that encompass each of these modes:

- `LoRaProp`: the class for a proprietary implementation
- `LoRaWAN`: the class for a LoRAWAN implementation

#!/usr/bin/python

########################################################################
### Python class for interacting with LoRA module via serial AT cmds ###
########################################################################

import serial
from enum import Enum

error_messages = {
    "AT_ERROR": "Generic AT error",
    "AT_PARAM_ERROR": "Parameter of the command is wrong.",
    "AT_BUSY_ERROR": "LoRa network is busy, so the command could not complete.",
    "AT_TEST_PARAM_OVERFLOW": "Parameter is too long.",
    "AT_NO_NETWORK_JOINED": "LoRa network is not joined.",
    "AT_RX_ERROR": "Error detection during the reception of the command."
}

class LoRaMode(Enum):
    MODE_LORAWAN = 0
    MODE_PROPRTY = 1

class LoRaModule:
    def __init__(
            self, 
            port, 
            baudrate=9600, 
            timeout=1
        ):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        """Sends an AT command and waits for a response."""
        command_with_newline = command + "\r\n"
        self.ser.write(command_with_newline.encode())

        response_lines = []
        status_line = ""
        while True:
            line = self.ser.readline().decode().strip()
            if not line:
                continue  # Ignore empty lines
            response_lines.append(line)
            if line in error_messages.keys() or line in ("OK", "+READY"):
                status_line = line
                break

        if status_line in ("OK", "+READY"):
            return response_lines[:-1] if response_lines else status_line
        elif status_line in error_messages.keys():
            error_code = status_line.split("=")[-1]
            self._handle_error(error_code)
        else:
            raise Exception(f"Unexpected response: {response_lines}")

    def _handle_error(self, error_code):
        """Handles error codes returned by the LoRa module."""
        error_message = error_messages.get(error_code, "Unknown error code.")
        raise Exception(f"Error {error_code}: {error_message}")

    def reset(self):
        """Resets the module."""
        return self.send_command("ATZ")
    
    def get_mode(self):
        """Gets the operating mode of the module."""
        return self.send_command(f"AT+OPMODE=?")
    
    def set_mode(self, opmode):
        """Sets the operating mode of the module.

        opmode=0 : LoRAWAN
        opmode=1 : Proprietary LoRA
        """
        return self.send_command(f"AT+OPMODE={opmode}")
    
    def get_firmware_version(self):
        """Gets the firmware version."""
        return self.send_command("AT+VER=?")

    def set_band(self, frequency):
        """Sets the LoRa center frequency (in Hz)."""
        return self.send_command(f"AT+BAND={frequency}")

    def get_band(self):
        """Retrieves the LoRa center frequency (in Hz)."""
        return self.send_command("AT+BAND=?")

    def set_parameters(self, sf, bw, cr, preamble):
        """Sets the LoRa RF parameters."""
        return self.send_command(f"AT+PARAMETER={sf},{bw},{cr},{preamble}")

    def set_address(self, address):
        """Sets the module address."""
        return self.send_command(f"AT+ADDRESS={address}")

    def set_network_id(self, network_id):
        """Sets the LoRa network ID."""
        return self.send_command(f"AT+NETWORKID={network_id}")

    def send_data(self, address, data):
        """Sends data to the specified address."""
        payload_length = len(data)
        return self.send_command(f"AT+SEND={address},{payload_length},{data}")

    def set_password(self, password):
        """Sets the AES128 encryption password."""
        return self.send_command(f"AT+CPIN={password}")

    def set_rf_power(self, power):
        """Sets the RF output power (0-15 dBm)."""
        return self.send_command(f"AT+CRFOP={power}")

    def get_unique_id(self):
        """Gets the module's unique ID."""
        return self.send_command("AT+UID=?")

    def factory_reset(self):
        """Resets all parameters to factory defaults."""
        return self.send_command("AT+FACTORY")

class LoRaWAN(LoRaModule):
    def send_data(self, port, confirmed, data):
        return self.send_command(f"AT+SEND={port},{confirmed},{data}")


class LoRaProp(LoRaModule):
    def __init__(self, port, baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.set_mode(LoRaMode.MODE_PROPRTY.value) 
        self.reset() # Reset req'd for mode setting to take

    def get_band(self):
        """Gets current frequency setting, in Hz"""
        return self.send_command(f"AT+BAND=?")

    def set_band(self,frequency):
        """Sets current frequency setting, in Hz 
        e.g. frequency=915000000 for 915MHz
        """
        return self.send_command(f"AT+BAND={frequency}")

    def get_parameter(self):
        """Gets current rf parameter settings (sf, bw, cr, preamble)
        sf: spreading factor
        bw: bandwidth
        cr: coding rate
        preamble: programmed preamble

        """
        return self.send_command(f"AT+PARAMETER=?")

    def set_parameter(self, sf, bw, cr, preamble):
        """Sets rf parameter settings 
        sf: spreading factor
        bw: bandwidth
        cr: coding rate
        preamble: programmed preamble

        """
        return self.send_command(f"AT+PARAMETER={sf},{bw},{cr},{preamble}")

    def get_address(self):
        """Gets current node address (0-65535)"""
        return self.send_command(f"AT+ADDRESS=?")

    def set_address(self, address):
        """Sets current node address (0-65535)"""
        return self.send_command(f"AT+ADDRESS={address}")

    def get_node_pin(self):
        """Gets eight character node pin"""
        return self.send_command(f"AT+CPIN=?")

    def set_node_pin(self, node_pin):
        """Sets eight character node pin"""
        return self.send_command(f"AT+CPIN={node_pin}")

    def get_tx_power(self):
        """Gets RF transmit power (in dBm)"""
        return self.send_command(f"AT+CRFOP=?")

    def set_tx_power(self, pwr_dbm):
        """Sets RF transmit power,in dBm - (0-22dBM)"""
        return self.send_command(f"AT+CRFOP={pwr_dbm}")

    def send_data(self, rx_addr, data):
        payload_length = len(data)
        return self.send_command(f"AT+SEND={rx_addr},{payload_length},{data}")
    
    def get_received_data(self):
        """Checks for and returns received data (if any)."""
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode().strip()
            if line.startswith("+RCV="):
                parts = line[5:].split(",")
                return {
                    "address": int(parts[0]),
                    "length": int(parts[1]),
                    "data": parts[2],
                    "rssi": int(parts[3]),
                    "snr": int(parts[4]),
                }
        return None  # No data received


    def factory_reset(self):
        """Restores device to mfg defaults
        BAND: 915MHz
        UART: 115200baud
        SF: 9
        BW: 125kHz
        CR: 1
        Preamble Length: 12
        Address: 0
        NetID: 18
        Tx Power: 22dBm"""
        return self.send_command(f"AT+FACTORY")


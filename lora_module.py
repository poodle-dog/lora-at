#!/usr/bin/python

########################################################################
### Python class for interacting with LoRA module via serial AT cmds ###
########################################################################

import serial
import time

class LoRaModule:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        """Sends an AT command and waits for a response."""
        command_with_newline = command + "\r\n"
        self.ser.write(command_with_newline.encode())

        response_lines = []
        while True:
            line = self.ser.readline().decode().strip()
            if not line:  # Empty line indicates end of response
                break
            response_lines.append(line)

        if response_lines[-1] in ("+OK", "+READY"):
            return response_lines[0]
        elif "+ERR" in response_lines[-1]:
            error_code = response_lines[-1].split("=")[-1]
            self._handle_error(int(error_code))
        else:
            raise Exception(f"Unexpected response: {response_lines}")

    def _handle_error(self, error_code):
        """Handles error codes returned by the LoRa module."""
        error_messages = {
            1: "Missing newline or carriage return at the end of the AT command.",
            2: "Command does not start with 'AT'.",
            3: "Missing '=' symbol in the AT command.",
            4: "Unknown command.",
            10: "TX timeout.",
            11: "RX timeout.",
            12: "CRC error.",
            13: "TX data exceeds 240 bytes.",
            15: "Unknown error."
        }
        error_message = error_messages.get(error_code, "Unknown error code.")
        raise Exception(f"Error {error_code}: {error_message}")


    def reset(self):
        """Resets the module."""
        return self.send_command("AT+RESET")

    def set_mode(self, mode):
        """Sets the module mode (0: Transmit/Receive, 1: Sleep)."""
        return self.send_command(f"AT+MODE={mode}")

    def set_baudrate(self, baudrate):
        """Sets the UART baud rate."""
        return self.send_command(f"AT+IPR={baudrate}")

    def set_parameters(self, sf, bw, cr, preamble):
        """Sets the LoRa RF parameters."""
        return self.send_command(f"AT+PARAMETER={sf},{bw},{cr},{preamble}")

    def set_frequency(self, frequency):
        """Sets the LoRa center frequency (in Hz)."""
        return self.send_command(f"AT+BAND={frequency}")

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

    def get_firmware_version(self):
        """Gets the firmware version."""
        return self.send_command("AT+VER?")

    def get_unique_id(self):
        """Gets the module's unique ID."""
        return self.send_command("AT+UID?")

    def factory_reset(self):
        """Resets all parameters to factory defaults."""
        return self.send_command("AT+FACTORY")

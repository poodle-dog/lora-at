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

        if (response_lines[-1] == "+OK") or (response_lines[-1] == "+READY"):
            return response_lines[0]  
        else:
            raise Exception(f"Error in response: {response_lines}")

    def reset(self):
        """Resets the module."""
        return self.send_command("AT+RESET")

    def set_frequency(self, frequency):
        """Sets the LoRa center frequency (in Hz)."""
        return self.send_command(f"AT+BAND={frequency}")

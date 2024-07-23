import unittest
import subprocess
import time
import serial
from lora_module import LoRaModule

class TestLoRaModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start socat to create linked pseudo-terminals
        cls.proc = subprocess.Popen(['socat', '-d', '-d', 'pty,raw,echo=0', 'pty,raw,echo=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Allow some time for socat to start
        time.sleep(2)

        # Read the output without waiting for the process to finish
        stderr_output = []
        while True:
            line = cls.proc.stderr.readline()
            if not line:
                break
            stderr_output.append(line.decode().strip())
            if len(stderr_output) >= 2:
                break

        # Extract pseudo-terminal names
        cls.pty1 = stderr_output[0].split()[-1]
        cls.pty2 = stderr_output[1].split()[-1]

        print(f"Linked pseudo-terminals: {cls.pty1} <-> {cls.pty2}")

    @classmethod
    def tearDownClass(cls):
        # Terminate the socat process
        cls.proc.terminate()

    def test_lora_reset(self):
        # Create instance of LoRaModule using the first pty
        lora = LoRaModule(self.pty1)

        # Open the second pty to simulate the receiving end
        with serial.Serial(self.pty2, baudrate=115200, timeout=1) as receiver:
            # Define expected response
            expected_response = "+RESET"

            # Start a background thread to simulate the module's response
            def respond():
                time.sleep(0.1)  # Wait for the command to be sent
                receiver.write(("+RESET\r\n+READY\r\n").encode())

            import threading
            response_thread = threading.Thread(target=respond)
            response_thread.start()

            # Send the command and get the response
            response = lora.reset()

            # Assert that the received response matches the expected response
            self.assertEqual(response, expected_response)

            # Ensure the response thread has finished
            response_thread.join()

    def test_lora_set_frequency(self):
        # Create instance of LoRaModule using the first pty
        lora = LoRaModule(self.pty1)

        # Open the second pty to simulate the receiving end
        with serial.Serial(self.pty2, baudrate=115200, timeout=1) as receiver:
            freq = 868500000

            # Define expected response
            expected_response = "+OK"

            # Start a background thread to simulate the module's response
            def respond():
                time.sleep(0.1)  # Wait for the command to be sent
                receiver.write(("+OK\r\n").encode())

            import threading
            response_thread = threading.Thread(target=respond)
            response_thread.start()

            # Send the command and get the response
            response = lora.set_frequency(freq)

            # Assert that the received response matches the expected response
            self.assertEqual(response, expected_response)

            # Ensure the response thread has finished
            response_thread.join()

if __name__ == '__main__':
    unittest.main()


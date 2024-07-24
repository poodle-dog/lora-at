import argparse
import serial
import subprocess
import time
import unittest
from lora_module.lora_module import LoRaModule

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

        if not self.real_device:
            # Open the second pty to simulate the receiving end
            with serial.Serial(self.pty2, baudrate=115200, timeout=1) as receiver:
                # Define a test command and expected response
                test_command = "AT+RESET"
                expected_response = "+RESET\n+READY"

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
                self.assertEqual(response, "+RESET")

                # Ensure the response thread has finished
                response_thread.join()
        else:
            # Send the command and get the response (real device)
            response = lora.reset()
            self.assertIn("+READY", response)

    def test_lora_set_mode(self):
        lora = LoRaModule(self.pty1)  # Create instance of LoRaModule using the first pty
        mode = 0                      # Corresponds to Tx/Rx mode; 1=Sleep
        expected_response = "+OK"     # Define expected response

        if not self.real_device:
            # Open the second pty to simulate the receiving end
            with serial.Serial(self.pty2, baudrate=115200, timeout=1) as receiver:

                # Start a background thread to simulate the module's response
                def respond():
                    time.sleep(0.1)  # Wait for the command to be sent
                    receiver.write(("+OK\r\n").encode())

                import threading
                response_thread = threading.Thread(target=respond)
                response_thread.start()

                response = lora.set_mode(mode)
                self.assertEqual(response, expected_response)
                
                # Ensure the response thread has finished
                response_thread.join()
        else:
            # Send the command and get the response (real device)
            response = lora.set_mode(mode)
            self.assertIn(expected_response, response)

    def test_lora_set_parameters(self):
        lora = LoRaModule(self.pty1)  # Create instance of LoRaModule using the first pty
        sf = 12                       # Spreading factor
        bw = 7                        # bandwidth
        cr = 1                        # coding rate 
        preamble = 4                  # preamble
        expected_response = "+OK"     # Define expected response

        if not self.real_device:
            # Open the second pty to simulate the receiving end
            with serial.Serial(self.pty2, baudrate=115200, timeout=1) as receiver:

                # Start a background thread to simulate the module's response
                def respond():
                    time.sleep(0.1)  # Wait for the command to be sent
                    receiver.write(("+OK\r\n").encode())

                import threading
                response_thread = threading.Thread(target=respond)
                response_thread.start()

                response = lora.set_parameters(sf, bw, cr, preamble)
                self.assertEqual(response, expected_response)
                
                # Ensure the response thread has finished
                response_thread.join()
        else:
            # Send the command and get the response (real device)
            response = lora.set_parameters(sf, bw, cr, preamble)
            self.assertIn(expected_response, response)


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
    parser = argparse.ArgumentParser(description='Run LoRaModule unit tests.')
    parser.add_argument('--device', type=str, help='Path to the real /dev/ file to test against.')
    args = parser.parse_args()

    # Set class variable for real device path
    TestLoRaModule.real_device = args.device

    unittest.main(argv=['first-arg-is-ignored'])

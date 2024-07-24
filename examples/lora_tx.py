import argparse
from lora_module.lora_module import LoRaModule

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transmit a single message using LoRaModule')
    parser.add_argument('device', type=str, help='Name of serial device file (e.g. /dev/ttyUSB0)')
    parser.add_argument('address', type=int, help='Address to send the message to (e.g. 120)')
    parser.add_argument('message', type=str, help='Message to transmit (e.g. "HELLO")')
    args = parser.parse_args()

    lora = LoRaModule(args.device)
    response = lora.reset()
    print(f"Reset response: {response}")

    try:
        response = lora.send_data(args.address, args.message)
        print(f"Send response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        lora.ser.close()


import argparse
import sys
import time
from lora_module.lora_module import LoRaProp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
            'Simple Rx server for Proprietary LoRA'
    )
    parser.add_argument(
        'device', 
        type=str, 
        help='Name of serial device file (e.g. /dev/ttyUSB0)'
    )
    args = parser.parse_args()

    lora = LoRaProp(args.device)
    print("Starting LoRA Rx server")
    while True:
        response = lora.get_received_data()
        if response:
            print(response)
            time.sleep(0.1)
            lora.send_data(f"echoing message: {response}")


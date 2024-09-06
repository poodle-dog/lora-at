import argparse
import sys
from lora_module.lora_module import LoRaProp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='simple rx server for Proprietary LoRA')
    parser.add_argument(
            'device', 
            type=str, 
            help='Name of serial device file (e.g. /dev/ttyUSB0)'
    )
    args = parser.parse_args()

    lora = LoRaProp(args.device)
    lora.set_address(101)
    print("Starting LoRA Rx server")
    while True:
        response = lora.get_received_data()
        if response:
            print(response)



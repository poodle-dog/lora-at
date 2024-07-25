import argparse
import sys
from lora_module.lora_module import LoRaProp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='simple transmit using Proprietary LoRA')
    parser.add_argument(
            'device', 
            type=str, 
            help='Name of serial device file (e.g. /dev/ttyUSB0)'
    )
    parser.add_argument(
            'data', 
            type=str, 
            help='Data to send (e.g. "hello")'
    )
    parser.add_argument(
            'rx_addr', 
            type=str, 
            help='Address to send to (e.g. 101)'
    )
    args = parser.parse_args()

    lora = LoRaProp(args.device)
    response = lora.send_data(args.rx_addr, args.data)



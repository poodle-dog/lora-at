import argparse
import sys
from lora_module.lora_module import LoRaModule

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='example loraModule reset command'
    )
    parser.add_argument(
            'device', 
            type=str,
            help='Name of serial device file (e.g. /dev/ttyUSB0'
    )
    args = parser.parse_args()

    lora = LoRaModule(args.device)
    response = lora.reset()



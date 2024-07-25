import argparse
import sys
from lora_module.lora_module import LoRaModule

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='gets FW version of LoRA module'
    )
    parser.add_argument(
            'device', 
            type=str, 
            help='Name of serial device file (e.g. /dev/ttyUSB0'
    )
    args = parser.parse_args()

    lora = LoRaModule(args.device)
    response = lora.get_firmware_version()
    print('\n'.join(response))



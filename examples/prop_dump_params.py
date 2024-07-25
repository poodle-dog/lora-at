import argparse
import sys
from lora_module.lora_module import LoRaProp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='example loraModule reset command')
    parser.add_argument(
            'device', 
            type=str, 
            help='Name of serial device file (e.g. /dev/ttyUSB0'
    )
    args = parser.parse_args()

    lora= LoRaProp(args.device)

    print("Band      : ", lora.get_band())
    print("Params    : ", lora.get_parameter())
    print("Address   : ", lora.get_address())
    print("Node Pin  : ", lora.get_node_pin())
    print("Tx Pwr    : ", lora.get_tx_power())



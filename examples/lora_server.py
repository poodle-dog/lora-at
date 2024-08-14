import argparse
import sys
import threading
import time
from lora_module.lora_module import LoRaProp

from flask import Flask, request, jsonify
import requests

app = Flask(__name__, static_url_path='/static')

def lora_receiver(device):
    lora = LoRaProp(device)
    while True:
        response = lora.get_received_data()
        if response:
            print(f"Posting data to server: {response}")
            try:
                requests.post(
                    'http://localhost:8000/receive', 
                    json={'data': response}
                )
            except requests.exceptions.RequestException as e:
                print(f"Failed to post data: {e}")

        time.sleep(0.1)  


@app.route('/tx', methods=['POST'])
def lora_send():
    data = request.json
    message = data.get('message')

    # TODO: fix hardcoded receiver address
    response = lora.send_data(101, message)
    return jsonify({'status': 'message sent'}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='http frontend for LoRA w/ callback hook'
    )
    parser.add_argument(
            'device', 
            type=str, 
            help='Name of serial device file (e.g. /dev/ttyUSB0)'
    )
    args = parser.parse_args()

    lora_thread = threading.Thread(
        target=lora_receiver, args=(args.device,)
    )
    lora_thread.daemon = True
    lora_thread.start()

    app.run(debug=True, port=8001)


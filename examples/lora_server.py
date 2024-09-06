import argparse
import socket
import time
import requests
from queue import Queue
from lora_module.lora_module import LoRaProp

def initialize_socket(host='localhost', port=8001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.setblocking(False)  # Non-blocking socket
    return server_socket

def process_socket_data(server_socket, tx_queue):
    try:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print(f"Received from socket: {data}")
            tx_queue.put(data)
        client_socket.close()
    except BlockingIOError:
        pass  # No incoming connection

def process_serial_data(lora, rx_queue):
    response = lora.get_received_data()
    if response:
        print(f"Received from LoRa: {response}")
        rx_queue.put(response)

def process_tx_queue(lora, tx_queue):
    if not tx_queue.empty():
        message = tx_queue.get()
        lora.send_data(101, message)
        print(f"Sent to LoRa: {message}")

def process_rx_queue(rx_queue):
    if not rx_queue.empty():
        message = rx_queue.get()
        requests.post("http://localhost:5000/lora/recv",json={'message':message})
        print(f"Sent LoRA message to server")

def main_loop(lora, server_socket, tx_queue, rx_queue):
    while True:
        # Process data from socket and place it into the Tx queue
        process_socket_data(server_socket, tx_queue)

        # Process data from LoRa and place it into the Rx queue
        process_serial_data(lora, rx_queue)

        # Send data from the Tx queue to LoRa
        process_tx_queue(lora, tx_queue)

        # Send data from the Rx queue to Server
        process_rx_queue(rx_queue)

        # Add a short delay to prevent high CPU usage
        time.sleep(0.1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='LoRa radio Tx/Rx queue manager'
    )
    parser.add_argument(
        'device',
        type=str,
        help='Name of serial device file (e.g. /dev/ttyUSB0)'
    )
    args = parser.parse_args()

    # Initialize the LoRa module
    lora = LoRaProp(args.device)
    lora.set_address(100)

    # Initialize queues for Tx and Rx
    tx_queue = Queue()
    rx_queue = Queue()

    # Initialize the socket
    server_socket = initialize_socket()
    print("Socket initialized.")

    # Start the main loop
    print("Starting main loop; Listening on port 8001...")
    main_loop(lora, server_socket, tx_queue, rx_queue)


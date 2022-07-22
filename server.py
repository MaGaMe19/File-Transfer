from re import S
from socket import socket, AF_INET, SOCK_STREAM
import tqdm
import os
import threading

HOSTNAME = "192.168.1.116"
PORT = 8008
SEPARATOR = "<SEPERATOR>"
BUFFER_SIZE = 4096

outputFolder = "received"
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

def handle_connection(sock):
    content = sock.recv(BUFFER_SIZE).decode()
    if content:
        filename, filesize = content.split(SEPARATOR)

        filename = os.path.basename(filename) # remove absolute path
        filesize = int(filesize)

        # progress bar
        progress = tqdm.tqdm(range(filesize), f"Receiving '{filename}'", unit="B", unit_scale=True, unit_divisor=1024)

        with open(f"./received/{filename}", "wb") as f:
            while True:
                bytes_received = sock.recv(BUFFER_SIZE)
                
                # end of file
                if not bytes_received:
                    break
                    
                f.write(bytes_received)

                progress.update(len(bytes_received))
        
        sock.close()

def server(hostname=HOSTNAME, port=PORT):
    print(f"Serving on {hostname}:{port}")
    
    # Bind socket to hostname and port and await connections
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((hostname, port))
    sock.listen()

    # accept connections and forward them to handle_connection
    try:
        while True:
            client_sock, client_addr = sock.accept()
            print(f"New connection from {client_addr[0]}:{client_addr[1]}")
            thread = threading.Thread(target=handle_connection, args=[client_sock])
            thread.start()

    finally:
        sock.close()

if __name__ == "__main__":
    server()
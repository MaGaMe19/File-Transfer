from socket import socket, AF_INET, SOCK_STREAM
import tqdm
import os

from server import SEPARATOR, BUFFER_SIZE
HOSTNAME = "192.168.1.116"
PORT = 8008

def send(hostname=HOSTNAME, port=PORT):
    while True:
        filename = input("Filename: ")

        filesize = os.path.getsize(filename)

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((hostname, port))

        sock.send(f"{filename}{SEPARATOR}{filesize}".encode("utf-8"))

        # progress bar
        progress = tqdm.tqdm(range(filesize), f"Sending '{filename}'", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            done = False
            while not done:
                bytes_read = f.read(BUFFER_SIZE)

                # end of file
                if not bytes_read:
                    break

                sock.sendall(bytes_read)

                progress.update(len(bytes_read))
        
        sock.close()
    
        print("\n")

if __name__ == "__main__":
    send()

import socket
import json

class broker:
    def __init__(self):
        self.port = 5001
        self.nodes = {}

    def main(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))
        while True:
            msg, addr = self.sock.recvfrom(1024)
            self.nodes[msg] = addr
            print self.nodes
            self.sock.sendto(json.dumps(self.nodes), addr)


if __name__ == "__main__":
    broker().main()

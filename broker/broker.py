import socket
import json
import uuid

class Broker:
    
    def __init__(self):
        self.nodes = {}
        self.port = 5002
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def main(self):
        self.sock.bind(("0.0.0.0", self.port))
        while True:
            data, addr = self.sock.recvfrom(1024)
            print data
            self.nodes[uuid.uuid4().hex] = addr
            data = json.dumps(self.nodes)
            for x in range(2):
                self.sock.sendto(data, addr)

Broker().main()
        

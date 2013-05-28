import socket
import threading
import json

nodes = {}

class Marboo:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bi = "5.44.233.7"
        self.bp = 5002
        self.cmds = {
                "checkin":self.checkin,
                "msg":self.msg, 
                
                }
        self.nick = "test"
        self.room = "a"
    def main(self):
        self.get_nodes()
        while True:
            data, addr = self.sock.recvfrom(102400)
            data = json.loads(data)
            
    def prompt(self):
        while True:
            msg = raw_input(self.nick+"> ")
            data = json.dumps({"cmd":"msg", "message":msg, "room":self.room, "nick":self.nick})
            self.send(data)

    def get_nodes(self):
        self.sock.sendto("", (self.bi, self.bp))
        data = self.sock.recv(1024)
        nodes = json.loads(data)
        for x in nodes:
            self.connect(tuple(nodes[x]))
            self.sock.sendto(json.dumps({"cmd":"checkin"}), tuple(nodes[x]))
            
    def send(self, msg):
        for x in nodes:
            self.connect(tuple(nodes[x]))
            self.sock.sendto(msg, tuple(nodes[x]))
    def connect(self, addr):
        self.sock.sendto(json.dumps({"cmd":"connect"}), addr)
    def checkin(self):
        pass
    def msg(self):
        pass

if __name__ == "__main__":
    threading.Thread(target=Marboo().prompt).start()
    Marboo().main()

import socket
import json
import cryptic
import uuid
import threading

nodes = {}

class Warbora:
    def __init__(self):
        self.port = 2122
        self.cmds = {
                "checkin":self.checkin,
                "msg":self.msg,
                }

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broker_ip = ""
        self.broker_port = 5001
        self.key = uuid.uuid4().hex       
        self.group = "_"
        self.nick = "test"

    def main(self):
        self.sock.sendto(self.key, (self.broker_ip, self.broker_port))
        data, ip = self.sock.recvfrom(1024)
        node = json.loads(data)
        for x in node:
            nodes[x] = node[x]
            self.sock.sendto(self.encrypt(json.dumps({"cmd":"checkin", "key":self.key}), x), tuple(nodes[x]))
        while True:
            try:
                msg, addr = self.sock.recvfrom(102400)
                msg = json.loads(self.decrypt(msg))
            except Exception, error:
                print error
                continue
            
            if msg['cmd'] in self.cmds:
                self.cmds[msg['cmd']](msg, addr)
    def shell(self):
        while True:
            msg = raw_input(self.nick+": ")
            self.send(msg)
    def msg(self, msg, addr):
        if msg['group'] == self.group:
            print msg['nick']+": "+msg['message']

    def checkin(self, msg, addr):
        print addr[0], "checked in"
        nodes[msg['key']] = addr

    def send(self, message):
    
        message = json.dumps({"cmd":"msg", "nick":self.nick, "group":self.group, "message":message})
        for x in nodes:
            msg = self.encrypt(message, x)
            self.sock.sendto(msg, tuple(nodes[x]))
    def encrypt(self, message, key):
        return cryptic.encrypt(message, key)
    def decrypt(self, msg):
        return cryptic.decrypt(msg, self.key)
if __name__ == "__main__":
    threading.Thread(target=Warbora().shell).start()
    Warbora().main()



import socket,threading
from network.client_handler import handle_client
class TCPServer:
    def __init__(self,cfg,proc,logger,stats):
        self.cfg=cfg;self.proc=proc;self.logger=logger;self.stats=stats
        self.s=socket.socket();self.s.bind((cfg["server"]["host"],cfg["server"]["port"]));self.s.listen()
    def start(self):
        while True:
            c,a=self.s.accept()
            c.settimeout(self.cfg["server"]["client_timeout"])
            threading.Thread(target=handle_client,args=(c,a,self.proc,self.logger,self.stats),daemon=True).start()

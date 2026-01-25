import socket
import threading
from network.client_handler import handle_client

class TCPServer:
    def __init__(self, cfg, proc, logger, stats):
        self.cfg = cfg
        self.proc = proc
        self.logger = logger
        self.stats = stats

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((cfg["server"]["host"], cfg["server"]["port"]))
        self.s.listen()

    def start(self):
        while True:
            try:
                conn, addr = self.s.accept()
                conn.settimeout(self.cfg["server"]["timeout"])

                threading.Thread(
                    target=handle_client,
                    args=(conn, addr, self.proc, self.logger, self.stats)
                ).start()

            except Exception as e:
                print("Accept error:", e)

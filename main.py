import ssl
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 500
URL = ""

class StressTester:
    def __init__(self, url):
        self.counter = 0
        url_parts = url.split('://')
        self.protocol = url_parts[0]
        url_no_protocol = url_parts[1]
        self.host, *path_parts = url_no_protocol.split('/')

        if path_parts:
            path = '/' + '/'.join(path_parts)
        else:
            path = '/'
        self.request = f"GET {path} HTTP/1.1\r\nHost: {self.host}\r\nConnection: keep-alive\r\n\r\n"
        self.lock = threading.Lock()
        self.sock_pool = []

    def start(self):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                executor.submit(self.send_request)

    def send_request(self):
        sock = self.get_socket()
        sock.sendall(self.request.encode('utf-8'))
        with self.lock:
            self.counter += 1
        self.release_socket(sock)

    def get_socket(self):
        with self.lock:
            if self.sock_pool:
                return self.sock_pool.pop()
        sock = self.create_socket()
        sock.connect((self.host, self.port))
        return sock

    def release_socket(self, sock):
        with self.lock:
            self.sock_pool.append(sock)

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 16384) 
        sock.settimeout(30)
        if self.protocol == "https":
            return ssl.create_default_context().wrap_socket(sock=sock, server_hostname=self.host)
        elif self.protocol == "http":
            return sock
        else:
            raise ValueError("Unknown protocol scheme")

    @property
    def port(self):
        if self.protocol == "https":
            return 443
        elif self.protocol == "http":
            return 80
        else:
            raise ValueError("Unknown protocol scheme")


if __name__ == "__main__":
    stress_tester = StressTester(url=URL)
    stress_tester.start()

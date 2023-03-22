import ssl
import socket
from threading import Thread
from multiprocessing import Process

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
        self.request = f"GET {path} HTTP/1.1\r\nHost: {self.host}\r\n\r\n"

    def start(self):
        try:
            processes = []
            for i in range(MAX_THREADS):
                p = Process(target=self.send_requests)
                processes.append(p)
                p.start()

            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print(self.counter)
            exit()
    def send_requests(self):
        sock = self.create_socket()
        sock.connect((self.host, self.port))
        sock.sendall(self.request.encode('utf-8'))
        while True:
            sock.sendall(self.request.encode('utf-8'))
            self.counter += 1
    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    Process(target=stress_tester.start()).start()
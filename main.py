import ssl
import socket
from threading import Thread
import multiprocessing

threads = 15


class StressTester:
    def __init__(self, url):
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
        for i in range(threads):
            Thread(target=self.send_requests).start()

    def send_requests(self):
        inc = 0
        sock, port = CreateHttpsSocket(
            url=self.host, protocol=self.protocol).create_socket_obj()
        sock.connect((self.host, port))
        sock.sendall(self.request.encode('utf-8'))
        while True:
            print(inc)
            sock.sendall(self.request.encode('utf-8'))
            inc += 1


class CreateHttpsSocket:
    def __init__(self, url: str, protocol: str):
        self.url = url
        self.protocol = protocol

    def create_socket_obj(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        if self.get_port() == 443:
            return ssl.create_default_context().wrap_socket(sock=sock, server_hostname=self.url), self.get_port()
        elif self.get_port() == 80:
            return sock, self.get_port()
        else:
            exit()

    def get_port(self) -> int or str:
        if self.protocol.split("://")[0] == "https":
            return 443
        elif self.protocol.split("://")[0] == "http":
            return 80
        else:
            return "unknown SCHEME"


if __name__ == "__main__":
    url = ""
    stress_tester = StressTester(url=url)
    multiprocessing.Process(target=stress_tester.start()).start()

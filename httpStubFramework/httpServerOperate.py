import json
import socket
import threading
import time

import requests
from httpStubFramework.httpServerStub import HttpStub


class StubOperate:
    """定义桩的操作方法"""

    def __init__(self, http_port, socket_client_port, socket_server_port):
        self.http_port = http_port  # 定义桩实例的端口
        self.socket_client_port = socket_client_port  # 定义桩的socket的客户端的端口
        self.socket_server_port = socket_server_port  # 定义python脚本的socket服务端的端口
        self.server_socket = None  # 定义一个空的socket服务端实例属性
        self.client_socket = None  # 定义一个空的socket客户端实例属性

    def server_socket_start(self):
        """桩socket客户端的启动：这里是建立channel通道的过程，持续长连接的通道"""
        self.client_socket, client_address = self.server_socket.accept()

    def start_stub(self):
        """http桩初始化"""
        # 建立socket服务端，处于端口监听状态
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.socket_server_port)
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)

        # 桩应用的实例化
        http_stub = HttpStub(self.http_port, self.socket_client_port, self.socket_server_port)

        # 桩实例启动socket客户端和app的启动
        stub_app_t = threading.Thread(target=http_stub.server_run)
        stub_app_t.start()

        # 前两步(socket服务端和客户端以及桩服务启动后)启动完成后再建立socket通道
        channel_t = threading.Thread(target=self.server_socket_start)
        channel_t.start()
        # 怎么解决flask应用在面向对象中使用实例属性？todo

    def shutdown_stub(self):
        """http桩下线"""
        requests.post(url=f'http://127.0.0.1:{self.http_port}/shutdown', timeout=3)
        self.client_socket.close()
        self.server_socket.close()

    def receive(self):
        """http桩mock消息接收"""
        data = self.client_socket.recv(1024).decode('utf-8')
        return json.loads(data)

    def send(self, data):
        data = json.dumps(data)  # 将python对象转换为json字符串
        self.client_socket.sendall(data.encode("utf-8"))
        time.sleep(2)

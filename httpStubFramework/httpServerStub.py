import json
import os
import socket
import signal

from flask import Flask, request, jsonify
from werkzeug.serving import make_server

clientSocket = None


class HttpStub:
    app = Flask(__name__)

    def __init__(self, http_port, socket_client_port, socket_server_port):
        self.client_socket = None
        self.http_port = http_port
        self.socket_client_port = socket_client_port
        self.socket_server_port = socket_server_port

    def socket_client_start(self):
        """桩服务实例化socket客户端"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_address = ("localhost", self.socket_client_port)
        self.client_socket.bind(client_address)  # 绑定socket客户端端口
        server_address = ("localhost", self.socket_server_port)
        self.client_socket.connect(server_address)  # 客户端和服务端的连接
        return self.client_socket

    @staticmethod
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def msg_collect(path):
        """http桩，兼容所有路由和请求方式"""
        try:
            re_method = request.method
            # 实现桩下线的方法，提供下线的接口shutdown
            if path == 'shutdown' and re_method == 'POST':
                os.kill(os.getpid(), signal.SIGINT)
                return 'Server shutting down...', 200

            # 实现的http接口请求获取数据的通用方法 todo
            re_headers = request.headers
            re_cookies = request.cookies
            if re_method == 'GET':
                re_data = request.args
            else:
                re_data = request.get_json()
        except Exception as e:
            print("桩接收请求数据异常")
            raise e

        # 打包桩接收到的请求数据
        receive_msg = {
            "body": dict(re_data),
            "headers": dict(re_headers),
            "cookies": dict(re_cookies),
            "path": path,
            "method": re_method
        }
        message = json.dumps(receive_msg)
        # 将桩收到的请求打包发送到socket通道，测试用例可以从channel recv下来
        clientSocket.sendall(message.encode("utf-8"))
        # 测试用例定义了桩的结果返回，结果返回需要通过channel传输到桩实例，桩实例用socket client来recv
        data = clientSocket.recv(1024).decode('utf-8')
        send_data = json.loads(data)
        send_response = send_data["body"]
        send_status_code = send_data["code"]
        return send_response, send_status_code  # 桩的结果返回给被测服务，看被测服务是否能处理用例测定义的返回结果

    def server_run(self):
        """http桩启动"""
        global clientSocket
        clientSocket = self.socket_client_start()
        server = make_server('0.0.0.0', self.http_port, self.app)  # make_server是启动一个服务，这里就是启动桩服务是flask实例服务
        server.serve_forever()
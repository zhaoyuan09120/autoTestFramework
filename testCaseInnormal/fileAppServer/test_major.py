import json
import unittest
from time import sleep

import requests
from client_stub import fileAppStub
from common.logsMethod import info
from common.yamlRead import YamlRead
from httpStubFramework.httpCommon import HttpCommon
from common.checkOutput import CheckOutput
from common.logsMethod import info, class_case_log, step


@class_case_log
class FileAppTestCase(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    host = envConfig['docteamApp']

    def setUp(self) -> None:
        info("【前置】清空file的文件协同用户")
        url = self.host + '/clear'
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.delete(url=url, headers=headers, json={'file_id': '1111'})
        self.assertEqual(200, res.status_code)

    def testCase01_fileApp_res_200(self):
        """请求文档编辑接口，fileApp返回200，expect:文档编辑返回200  body为edit success"""
        url = self.host + '/edit'
        info(f"请求地址url:{url}")
        headers = {'Content-Type': 'application/json', 'Cookie': f'user_id={self.userid1}'}
        info(f"请求头headers:{headers}")
        data = {"file_id": "1111", "status": "edit"}
        info(f"请求body:{data}")
        info("请求被测服务接口")
        # 实例化请求发送和接收
        hc = HttpCommon()
        hc.http_requests(method='post', url=url, headers=headers, json=data)
        info("桩接收消息")
        file_receive = fileAppStub.receive()
        recv_body = file_receive['body']
        info("校验fileApp桩收到的消息")
        self.assertEqual(1, len(recv_body.keys()))
        self.assertEqual(data['file_id'], recv_body['file_id'])
        self.assertEqual('file', file_receive['path'])
        info("桩服务回复正常消息")
        send_data = {"body": {"msg": "Success"}, "code": 200}
        fileAppStub.send(send_data)
        expect = {"msg": "edit success"}
        self.assertEqual(200, hc.status_code)
        CheckOutput().output_check(expect=expect, actual=json.loads(hc.res_text))

    def testCase02_fileApp_server_down(self):
        """请求文档编辑接口，fileApp服务down  expect：文档编辑返回500  body为SERVER ERROR"""
        info("请求被测服务接口")
        url = self.host + '/edit'
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=A'}
        data = {"file_id": "1111", "status": "edit"}
        hc = HttpCommon()
        hc.http_requests(url=url, method='post', headers=headers, json=data)
        info("请求文件服务，桩receive消息,被测服务校验文件是否存在")
        file_recv = fileAppStub.receive()
        print(file_recv)
        info("校验fileApp桩收到的消息")
        recv_body = file_recv["body"]
        # print(recv_body)
        self.assertEqual(1, len(recv_body.keys()))  # 校验请求body是否有其他字段
        self.assertEqual(data['file_id'], recv_body["file_id"])  # 校验file_id的值和外部接口的输入是否一致
        self.assertEqual('file', file_recv['path'])
        self.assertEqual("GET", file_recv['method'])
        info("桩回复消息")
        send_data = {"body": {"msg": "server down"}, "code": 403}
        fileAppStub.send(send_data)
        expect = {"msg": "SERVER ERROR"}
        self.assertEqual(500, hc.status_code)
        CheckOutput().output_check(expect=expect, actual=json.loads(hc.res_text))

    def testCase03_fileApp_server_timeout(self):
        """请求文档编辑接口，fileApp超时返回403状态码，expect文档编辑接返回504  body为SERVER TIMEOUT
        """
        info("请求被测服务接口")
        url = self.host + '/edit'
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=A'}
        data = {"file_id": "1111", "status": "edit"}

        hc = HttpCommon()
        hc.http_requests(url=url, method='post', headers=headers, json=data)

        info("请求文件服务，桩receive消息,被测服务校验文件是否存在")
        file_recv = fileAppStub.receive()
        recv_body = file_recv["body"]
        info("校验fileApp桩收到的消息")
        self.assertEqual(1, len(recv_body.keys()))  # 校验请求body是否有其他字段
        self.assertEqual(data['file_id'], recv_body["file_id"])  # 校验file_id的值和fileApp的输入是否一致
        self.assertEqual('file', file_recv['path'])  # 校验请求路径是否正确
        sleep(10)  # 模拟请求三方接口超时
        info("桩回复消息")
        send_data = {"body": {"msg": "timeout"}, "code": 500}
        fileAppStub.send(send_data)
        expect = {"msg": "SERVER TIMEOUT"}
        self.assertEqual(504, hc.status_code)
        CheckOutput().output_check(expect=expect, actual=json.loads(hc.res_text))

    def testCase04_fileApp_res_403(self):
        """请求文档编辑接口，fileApp返回403状态码，expect文档编辑接返回500  body为SERVER ERROR
        """
        info("请求被测服务接口")
        url = self.host + '/edit'
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=B'}
        data = {"file_id": "1111", "status": "edit"}
        hc = HttpCommon()
        hc.http_requests(url=url, method='post', headers=headers, json=data)
        info("请求文件服务，桩receive消息,被测服务校验文件是否存在")
        file_recv = fileAppStub.receive()
        info("校验fileApp桩收到的消息")
        recv_body = file_recv["body"]
        self.assertEqual(1, len(recv_body.keys()))  # 校验请求body是否有其他字段
        self.assertEqual(data['file_id'], recv_body["file_id"])  # 校验file_id的值和fileApp的输入是否一致
        self.assertEqual('file', file_recv['path'])  # 校验请求路径是否正确
        info("桩回复消息")
        send_data = {"body": {"msg": "failed"}, "code": 403}
        fileAppStub.send(send_data)
        expect = {"msg": "SERVER ERROR"}
        self.assertEqual(500, hc.status_code)
        CheckOutput().output_check(expect=expect, actual=json.loads(hc.res_text))

    def testCase05_fileApp_res_text(self):
        """请求文档编辑接口，fileApp返回异常文本，expect文档编辑接返回504  body为SERVER ERROR
        """
        info("请求被测服务接口")
        url = self.host + '/edit'
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=B'}
        data = {"file_id": "1111", "status": "edit"}
        hc = HttpCommon()
        hc.http_requests(url=url, method='post', headers=headers, json=data)
        info("请求文件服务，桩receive消息,被测服务校验文件是否存在")
        file_recv = fileAppStub.receive()
        info("校验fileApp桩收到的消息")
        recv_body = file_recv["body"]
        self.assertEqual(1, len(recv_body.keys()))  # 校验请求body是否有其他字段
        self.assertEqual(data['file_id'], recv_body["file_id"])  # 校验file_id的值和fileApp的输入是否一致
        self.assertEqual('file', file_recv['path'])  # 校验请求路径是否正确
        info("桩回复消息")

        send_data = {"body": {"msg": "failed"}, "code": 403}
        fileAppStub.send(send_data)
        expect = {"msg": "SERVER ERROR"}
        self.assertEqual(500, hc.status_code)
        CheckOutput().output_check(expect=expect, actual=json.loads(hc.res_text))

import random
import unittest
import time

import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post
from common.yamlRead import YamlRead


@class_case_log
class UploadNoteInfoInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()['uploadNoteInfo']
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    path = dataConfig['path']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def testCase01_UploadNoteInfoFailed(self):
        """上传便签主体，noteId为空字符串必填项校验"""
        url = self.host + self.path
        note_id = ""
        body = {
            "noteId": note_id,
            "star": 1,
            "remindTime": 1,
            "remindType": 0,
            "groupId": "test"
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_UploadNoteInfoFailed(self):
        """上传便签主体，noteId为None必填项校验"""
        url = self.host + self.path
        note_id = None
        body = {
            "noteId": note_id,
            "star": 1,
            "remindTime": 1,
            "remindType": 0,
            "groupId": "test"
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_UploadNoteInfoFailed(self):
        """上传便签主体，noteId不传校验"""
        url = self.host + self.path
        body = {
            "star": 1,
            "remindTime": 1,
            "remindType": 0,
            "groupId": "test"
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_UploadNoteInfoSuccess(self):
        """上传便签主体，选填字段star字段不传校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "remindTime": 1,
            "remindType": 0,
            "groupId": "test"
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase05_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段star字段越界值2"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "remindTime": 1,
            "remindType": 0,
            "groupId": "test",
            "star": 2
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase06_UploadNoteInfoSuccess(self):
        """上传便签主体，选填字段remindTime字段校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "remindType": 0,
            "groupId": "test",
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase07_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段remindType字段填写越界值"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "remindType": 3,
            "groupId": "test",
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase08_UploadNoteInfoSuccess(self):
        """上传便签主体，选填字段groupId字段填不填写校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "remindType": 3,
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase09_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段groupId不存在"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        group_id = str(int(random.randint(1, 1000))) + "_groupID"
        body = {
            "noteId": note_id,
            "remindType": 3,
            "groupId": group_id,
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase10_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段noteId类型校验"""
        url = self.host + self.path
        note_id = int(time.time() * 1000)
        body = {
            "noteId": note_id,
            "remindType": 0,
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase11_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段noteId类型校验"""
        url = self.host + self.path
        body = {
            "noteId": True,
            "remindType": 0,
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase12_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段noteId特殊字符校验"""
        url = self.host + self.path
        body = {
            "noteId": "%4￥#@&……",
            "remindType": 0,
            "star": 0
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase13_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段star为字符串校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "star": "1",
            "remindTime": 1,
            "remindType": 0,

        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase14_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段star为浮点型校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "star": 1.0,
            "remindTime": 1,
            "remindType": 0,

        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase15_UploadNoteInfoFailed(self):
        """上传便签主体，选填字段star为浮点型校验"""
        url = self.host + self.path
        note_id = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": note_id,
            "star": True,
            "remindTime": 1,
            "remindType": 0,
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

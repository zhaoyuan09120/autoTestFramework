import copy
import time
import unittest
import requests
from business.dataClear import DataClear
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class CreateGroupHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理分组"""
        DataClear().group_clear()

    def tearDown(self):
        """后置清理分组"""
        DataClear().group_clear()

    def testCase01_CreateGroupFailed(self):
        """创建分组,groupId已经存在"""
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        copy_body = {"groupId": body["groupId"],
                     "groupName": DataGenerator.generate_time_str(), "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=copy_body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_CreateGroupFailed(self):
        """创建分组,groupName已经存在"""
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        copy_body = {"groupId": DataGenerator.generate_time_str() + "groupId",
                     "groupName": body['groupName'], "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=copy_body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_CreateGroupFailed(self):
        """创建分组,order为越界值"""
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 2}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

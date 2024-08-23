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
from parameterized import parameterized


@class_case_log
class CreateGroupInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()['CreateGroupInput']
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    mustKeys = dataConfig["mustKeys"]
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理环境中的分组"""
        DataClear().group_clear()

    def tearDown(self):
        """后置清理分组"""
        DataClear().group_clear()

    @parameterized.expand(mustKeys)
    def testCase01_CreateGroupFailed(self, key):
        """创建分组，必填项不传校验"""
        info(f"必填项{key}缺失")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        body.pop(key)
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMsg": "groupId为空"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_CreateGroupFailed(self):
        """创建分组，必填项groupId为空校验"""
        info(f"必填项groupId为空")
        step("创建分组请求体")
        body = {"groupId": "",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_CreateGroupFailed(self):
        """创建分组，必填项groupId为None校验"""
        info(f"必填项groupId为None")
        step("创建分组请求体")
        body = {"groupId": None,
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_CreateGroupFailed(self):
        """创建分组，必填项groupName为空校验"""
        info(f"必填项roupName为空")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": "", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase05_CreateGroupFailed(self):
        """创建分组，必填项groupId为None校验"""
        info(f"必填项groupId为None")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str(),
                "groupName": None, "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase06_CreateGroupSuccess(self):
        """创建分组，选填项order不传校验"""
        info("选填项order不传")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str()}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "updateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": [
            {"userId": self.userid1, "groupId": body["groupId"], "groupName": body["groupName"], "order": 0,
             "valid": int, "updateTime": int}
        ]}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase07_CreateGroupFailed(self):
        """创建分组，必填项groupId数据类型为int校验"""
        info(f"必填项groupId数据类型为int")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_int(),
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase08_CreateGroupFailed(self):
        """创建分组，必填项groupId数据类型为特殊字符校验"""
        info(f"必填项groupId为特殊字符")
        step("创建分组请求体")
        body = {"groupId": "*&^%$#^",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase09_CreateGroupFailed(self):
        """创建分组，必填项groupName数据类型为int校验"""
        info(f"必填项groupName数据类型为int")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_int(), "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase10_CreateGroupFailed(self):
        """创建分组，必填项groupName数据类型为特殊字符校验"""
        info(f"必填项groupName为特殊字符")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": "*&^%$#^", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase11_CreateGroupFailed(self):
        """创建分组，选填项order数据类型为字符串校验"""
        info(f"选填项order数据类型为字符串校验")
        step("创建分组请求体")
        body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                "groupName": DataGenerator.generate_time_str() + "_groupName", "order": "0"}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

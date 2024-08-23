import copy
import time
import unittest
import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class GetGroupsGroupInput(unittest.TestCase):
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

    def testCase01_GetGroupsFailed(self):
        """获取分组列表,选填项excludeInValid为None"""
        step("前置创建分组")
        data_msg = DataCreate().create_group(order=0,num=1)
        step("获取分组列表")
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": None},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": [
            {"userId": self.userid1, "groupId": data_msg[0]["groupId"], "groupName": data_msg[0]["groupName"],
             "order": data_msg[0]['order'],
             "valid": 1, "updateTime": int}
        ]}
        self.assertEqual(500, res.status_code)
        CheckOutput().output_check(expect=expect, actual=res.json())

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
class DeleteGroupMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理分组"""
        DataClear().group_clear()

    def testCase01_DeleteGroupSuccessMajor(self):
        """删除分组主流程"""
        step("前置创建分组")
        data_msg = DataCreate().create_group(order=0, num=1)
        step("删除分组")
        res = post(url=self.host + '/notesvr/delete/notegroup', headers=self.headers, sid=self.sid1,
                   data={"groupId": data_msg[0]['groupId']})
        expect = {"responseTime": int}
        self.assertEqual(200, res.status_code)
        CheckOutput().output_check(expect=expect, actual=res.json())
        step("数据源校验")
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

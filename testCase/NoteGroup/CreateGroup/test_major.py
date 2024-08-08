import unittest
from business.dataClear import DataClear
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class CreateGroupMajor(unittest.TestCase):
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

    def testCase01_CreateGroupSuccessMajor(self):
        """创建分组主流程"""
        step("创建分组")
        body = {"groupId": DataGenerator.generate_time_str(),
                "groupName": DataGenerator.generate_time_str() + "_groupId", "order": 0}
        res = post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "updateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        step("数据源校验")
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={"excludeInValid": True},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": [
            {"userId": self.userid1, "groupId": body["groupId"], "groupName": body["groupName"], "order": body['order'],
             "valid": int, "updateTime": int}
        ]}
        CheckOutput().output_check(expect=expect, actual=res.json())

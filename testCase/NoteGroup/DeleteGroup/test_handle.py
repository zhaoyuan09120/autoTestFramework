import unittest
from business.dataClear import DataClear
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class DeleteGroupHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理环境中的分组"""
        DataClear().group_clear()

    def testCase01_DeleteGroupFailed(self):
        """删除分组,分组groupId不存在"""
        step("删除分组")
        res = post(url=self.host + '/notesvr/delete/notegroup', headers=self.headers, sid=self.sid1,
                   data={"groupId": DataGenerator.generate_time_str() + "_groupId"})
        expect = {"errorCode": -1002, "errorMsg": "GroupId Not Exist!"}
        CheckOutput().output_check(expect=expect, actual=res.json())

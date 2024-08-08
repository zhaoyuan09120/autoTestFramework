import unittest
from business.dataClear import DataClear
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log, step
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class GetNotesForGroupHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理环境中的分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def tearDown(self):
        """后置清理便签和分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def testCase01_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId传不存在groupId校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": DataGenerator.generate_time_str(),
            "startIndex": 0,
            "rows": 20
        })
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1002, "errorMessage": "GroupId Not Exist!"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNotesForGroupFailed(self):
        """查看分组下标签,当前用户查询其他用户的分组"""
        pass

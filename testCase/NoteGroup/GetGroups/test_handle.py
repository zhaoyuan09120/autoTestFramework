import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead


@class_case_log
class GetGroupsGroupHandle(unittest.TestCase):
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

    def testCase01_GetGroupsSuccess(self):
        """获取分组列表,选填项excludeInValid不传参"""
        step("前置创建分组")
        DataCreate().create_group(order=0,num=1)
        step("获取分组列表")
        res = post(url=self.host + '/v3/notesvr/get/notegroup', headers=self.headers, data={},
                   sid=self.sid1)
        expect = {"requestTime": int, "noteGroups": list}
        self.assertEqual(200, res.status_code)
        CheckOutput().output_check(expect=expect, actual=res.json())

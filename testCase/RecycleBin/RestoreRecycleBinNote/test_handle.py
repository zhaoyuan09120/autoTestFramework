import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get, patch
from common.yamlRead import YamlRead


@class_case_log
class RestoreNoteFromRecycleBinHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}
    url = "https://gonote.wps.cn/gonote/api/v5/notesvr/recover/notes"
    expectBase = {"code": int, "msg": "invalid params", "data": {"responseTime": int}}

    def setUp(self):
        """前置彻底清除回收站的便签"""
        DataClear().recycle_bin_note_clear()

    def tearDown(self):
        """后置删除便签和清除回收站的便签"""
        DataClear().note_clear()
        DataClear().recycle_bin_note_clear()

    def testCase01_RestoreRecycleBinNoteSuccessFailed(self):
        """恢复不在回收站的便签数据"""
        step("前置构建2条便签数据")
        data_msg = DataCreate().create_note(num=2)
        step("查看创建的便签数据")
        body = {"noteIds": [str(i['noteId']) for i in data_msg]}
        result = post(url=self.url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(400, result.status_code)
        expect = self.expectBase
        CheckOutput().output_check(expect=expect, actual=result.json())

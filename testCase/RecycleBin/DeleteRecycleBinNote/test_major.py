import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get, patch
from common.yamlRead import YamlRead


@class_case_log
class DeleteRecycleBinNoteMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}
    url = host + '/v3/notesvr/cleanrecyclebin'

    def setUp(self):
        DataClear().recycle_bin_note_clear()

    def testCase01_DeleteRecycleBinNoteSuccess(self):
        """删除回收站的便签"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        body = {"noteIds": [str(i['noteId']) for i in data_msg]}
        result = post(url=self.url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, result.status_code)
        expect = {"responseTime": int}
        CheckOutput().output_check(expect=expect, actual=result.json())

    def testCase02_ClearRecycleBinNoteSuccess(self):
        """清空回收站便签"""
        step("前置构建2条便签数据")
        DataCreate().create_note(num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        body = {"noteIds": ["-1"]}
        result = post(url=self.url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, result.status_code)
        expect = {"responseTime": int}
        CheckOutput().output_check(expect=expect, actual=result.json())

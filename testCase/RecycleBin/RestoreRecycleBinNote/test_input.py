import time
import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get, patch
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class RestoreNoteFromRecycleBinInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = "https://gonote.wps.cn/gonote/api/v5/notesvr/recover/notes"
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}
    expectBase = {"code": int, "msg": "invalid params", "data": {"responseTime": int}}

    def setUp(self):
        """前置彻底清除回收站的便签"""
        DataClear().recycle_bin_note_clear()

    def tearDown(self):
        """后置删除便签和清除回收站的便签"""
        DataClear().note_clear()
        DataClear().recycle_bin_note_clear()

    def testCase01_RestoreRecycleBinNoteFailed(self):
        """回收站恢复便签:noteIds为None"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        body = {"noteIds": None}
        result = post(url=self.host, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(400, result.status_code)
        expect = self.expectBase
        CheckOutput().output_check(expect=expect, actual=result.json())

    def testCase02_RestoreRecycleBinNoteFailed(self):
        """回收站恢复便签:noteIds不传"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        body = {}
        result = post(url=self.host, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(400, result.status_code)
        expect = self.expectBase
        CheckOutput().output_check(expect=expect, actual=result.json())

    def testCase03_RestoreRecycleBinNoteFailed(self):
        """回收站恢复便签:noteIds参数类型为空list校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        body = {"noteIds": []}
        result = post(url=self.host, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(400, result.status_code)
        expect = self.expectBase
        CheckOutput().output_check(expect=expect, actual=result.json())

    def testCase04_RestoreRecycleBinNoteFailed(self):
        """回收站恢复便签:noteIds不存在"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        body = {"noteIds": [DataGenerator.generate_time_str() + "invalidNoteId"]}
        result = post(url=self.host, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(400, result.status_code)
        expect = self.expectBase
        CheckOutput().output_check(expect=expect, actual=result.json())

import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead


@class_case_log
class GetNoteForRecycleBinInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().recycle_bin_note_clear()

    def testCase01_GetNoteForRecycleBinFailed(self):
        """查看回收站便签列表，startindex参数为字符串"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        res = get(url=self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/"1"/rows/50/notes',
                  sid=self.sid1, headers=self.headers)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNoteForRecycleBinFailed(self):
        """查看回收站便签列表，rows参数为字符串"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        res = get(url=self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/1/rows/"50"/notes',
                  sid=self.sid1, headers=self.headers)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_GetNoteForRecycleBinFailed(self):
        """查看回收站便签列表，startindex参数为-1"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        res = get(url=self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/-1/rows/50/notes', sid=self.sid1,
                  headers=self.headers)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_GetNoteForRecycleBinFailed(self):
        """查看回收站便签列表，rows参数为-1"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        res = get(url=self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/1/rows/-1/notes', sid=self.sid1,
                  headers=self.headers)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        CheckOutput().output_check(expect=expect, actual=res.json())

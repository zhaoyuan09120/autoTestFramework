import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import get
from common.yamlRead import YamlRead


@class_case_log
class GetNotePageInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    invalid_user_id = envConfig['invalid_user_id']
    invalid_wps_id = envConfig['invalid_wps_id']
    sid1 = envConfig['sid1']
    host = envConfig['host']

    def setUp(self):
        DataClear().note_clear()

    def testCase01_GetNotePageFailed(self):
        """获取首页便签：wps_id值为无效值"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = -1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.invalid_wps_id)
        self.assertEqual(401, res.status_code)
        expect = {"errorCode": -2010, "errorMsg": ""}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNotePageFailed(self):
        """获取首页便签：user_id值为无效值"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = -1
        path = f'/v3/notesvr/user/{self.invalid_user_id}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(412, res.status_code)
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_GetNotePageFailed(self):
        """获取首页便签：startIndex值为空字符串校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = ""
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_GetNotePageFailed(self):
        """获取首页便签：startIndex值为字符串类型校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = "0"
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(400, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase05_GetNotePageFailed(self):
        """获取首页便签：rows值为空字符串校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = ""
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(400, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase06_GetNotePageFailed(self):
        """获取首页便签：rows值为字符串校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = "10"
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(400, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase07_GetNotePageFailed(self):
        """获取首页便签：rows值为越界值校验"""
        step("前置构建1条便签数据")
        DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = -1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMsg": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

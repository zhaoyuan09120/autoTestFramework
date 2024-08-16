import unittest
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import get
from copy import deepcopy

from common.yamlRead import YamlRead


@class_case_log
class GetNotePageHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']

    def setUp(self):
        DataClear().note_clear()

    def testCase01_GetNotePageSuccess(self):
        """获取首页便签，startindex约束，存在两条便签数据，startindex的值为1"""
        step("前置构建2条便签数据")
        data_msg = DataCreate().create_note(num=2)
        step("获取首页便签")
        startindex = 1
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[0]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": data_msg[0]['title'],
             "summary": data_msg[0]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}]}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNotePageSuccess(self):
        """获取首页便签，startindex约束，存在两条便签数据，startindex的值为2校验"""
        step("前置构建2条便签数据")
        DataCreate().create_note(num=2)
        step("获取首页便签")
        startindex = 2
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": 0, "webNotes": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_GetNotePageSuccess(self):
        """获取首页便签，startindex约束场景校验，存在两条便签数据，startindex的值为0"""
        step("前置构建2条便签数据")
        data_msg = DataCreate().create_note(num=2)
        step("获取首页便签")
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[1]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": data_msg[1]['title'],
             "summary": data_msg[1]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int},
            {"noteId": data_msg[0]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": data_msg[0]['title'],
             "summary": data_msg[0]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}]}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_GetNotePageSuccess(self):
        """获取首页便签，rows约束，存在一条便签数据，rows的值为0"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("获取首页便签")
        startindex = 0
        rows = 0
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": 0, "webNotes": []}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase05_GetNotePageSuccess(self):
        """获取首页便签，rows约束，存在两条便签数据，rows的值为1"""
        step("前置构建2条便签数据")
        data_msg = DataCreate().create_note(num=2)
        step("获取首页便签")
        startindex = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=self.host + path, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[1]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": data_msg[1]['title'],
             "summary": data_msg[1]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}]}
        CheckOutput().output_check(expect=expect, actual=res.json())

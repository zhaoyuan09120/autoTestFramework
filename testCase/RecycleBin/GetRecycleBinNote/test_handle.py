import unittest
from time import sleep

import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead


@class_case_log
class GetNoteForRecycleBinHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().recycle_bin_note_clear()

    def testCase01_GetNoteForRecycleBinSuccess(self):
        """查看回收站便签列表，startindex约束场景校验,存在两条便签数据"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=url, sid=self.sid1, headers=self.headers)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[0]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 2, "infoUpdateTime": int, "groupId": None, "title": data_msg[0]['title'],
             "summary": data_msg[0]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}]}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNoteForRecycleBinSuccess(self):
        """查看回收站便签列表，startindex约束场景校验,存在两条便签数据"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note( num=2)
        step("将便签数据进行软删除到回收站")
        DataClear().note_clear()
        step("查看回收站便签数据")
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.userid1}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = get(url=url, sid=self.sid1, headers=self.headers)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[1]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 2, "infoUpdateTime": int, "groupId": None, "title": data_msg[1]['title'],
             "summary": data_msg[1]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int},
            {"noteId": data_msg[0]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 2, "infoUpdateTime": int, "groupId": None, "title": data_msg[0]['title'],
             "summary": data_msg[0]['summary'], "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}

        ]}
        CheckOutput().output_check(expect=expect, actual=res.json())

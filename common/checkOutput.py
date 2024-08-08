import unittest


class CheckOutput(unittest.TestCase):
    def output_check(self, expect, actual):
        """
        通用的断言方法
        :param expect: 描述断言的期望值 以object结构描述出期望值，支持动态值的校验和精准值的校验
        :param actual: 描述断言的实际结果 字典结构的json字符串，一般来说指的是response.json()
        :return:
        """
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='keys len error')
        for k, v in expect.items():
            self.assertIn(k, actual.keys(), msg=f"expect key:【{k}】 not in response")
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f"key:{k} type error")
            elif isinstance(v, dict):
                self.output_check(v, actual[k])  # 递归处理响应中的嵌套关系
            elif isinstance(v, list):  # 如果嵌套中有列表结果
                self.assertEqual(len(v), len(actual[k]), msg=f'key:{k} len error')
                for i in range(len(v)):
                    if isinstance(v[i], type):
                        self.assertEqual(v[i], type(actual[k][i]), msg=f"list value:【{v[i]}】 type error")
                    elif isinstance(v[i], dict):  # 如果列表中的值是dict类型
                        self.output_check(v[i], actual[k][i])
                    else:  # 精准值的校验
                        self.assertEqual(v[i], actual[k][i], msg=f"list value: 【{v[i]}】 value error")
            else:
                self.assertEqual(v, actual[k], msg=f"key:{k} value error")


if __name__ == '__main__':
    data = {
        "responseTime": 0,
        "webNotes": [
            {"noteId": "c8613731e946ebe94d8070ff59663c1f", "createTime": 1721972032520, "star": 0, "remindTime": 0,
             "remindType": 0,
             "infoVersion": 1,
             "infoUpdateTime": 1721972032520,
             "groupId": None,
             "title": "vDWXJWv2MIZMmejQICpDJg==",
             "summary": "kkYF4FcUaNVkTyed9St9dw==",
             "thumbnail": None,
             "contentVersion": 5,
             "contentUpdateTime": 1721972039589
             }
        ]
    }
    r_expect = {"responseTime": "", "webNotes": ""}
    CheckOutput().output_check(r_expect, data)


import time
import unittest
import os
from BeautifulReport import BeautifulReport
from threading import Thread
from client_stub import fileAppStub


DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRON = 'Online'  # 'Online' -> 线上环境， 'Offline' -> 测试环境


if __name__ == '__main__':
    # 启动桩
    fileAppStub.start_stub()

    def start_server():
        os.chdir(DIR + '/app')
        os.system('python docteamApp.py')  # ./XXX.sh

    t = Thread(target=start_server)
    t.start()
    time.sleep(5)

    run_pattern = 'all'  # all 全量测试用例执行   smoking 冒烟测试执行    指定执行文件
    if run_pattern == 'all':
        pattern = 'test_*.py'
    elif run_pattern == 'smoking':
        pattern = 'test_major*.py'
    else:
        pattern = run_pattern + '.py'
    suite = unittest.TestLoader().discover(DIR + '/testCase', pattern=pattern)

    result = BeautifulReport(suite)
    result.report(filename="report.html", description='测试报告', report_dir="./report")

    # server stop
    os.chdir(DIR + '/app')
    os.system('python appStop.py')

    fileAppStub.shutdown_stub()
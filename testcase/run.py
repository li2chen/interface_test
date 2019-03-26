# coding=utf-8
import os
import time
import unittest
import HTMLTestRunner
from testcase.test_cart import CartTest

report = os.path.dirname(os.path.abspath('.')) + '/report/'
time = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
test_report = report + time + '-test.html'
file = open(test_report, 'wb')
suite = unittest.TestSuite(unittest.makeSuite(CartTest))  # 添加一个模块的测试用例

if __name__ == '__main__':
	# runner = unittest.TextTestRunner()
	runner = HTMLTestRunner.HTMLTestRunner(stream=file, title='测试报告', description='测试结果详情')
	runner.run(suite)

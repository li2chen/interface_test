# coding=utf-8

import os
import unittest
import HTMLTestRunner
import time

curr_path = os.path.dirname(os.path.realpath(__file__))


def all_cases():
	case_path = os.path.join(curr_path, 'case')  # E:\develop\my_inter\case
	if not os.path.exists(case_path):
		os.mkdir(case_path)

	discover_cases = unittest.defaultTestLoader.discover(case_path)  # cases
	return discover_cases


def run_cases(cases):
	report_path = os.path.join(curr_path, 'report')
	if not os.path.exists(report_path):
		os.mkdir(report_path)
	now = time.strftime("%Y%m%d%H%M%S")
	report = os.path.join(report_path, now + '-result.html')

	f = open(report, 'wb')
	runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='test')
	runner.run(cases)
	f.close()


def get_report(report_path):
	lists = os.listdir(report_path)
	lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
	report_file = os.path.join(report_path, lists[-1])
	return report_file


if __name__ == '__main__':
	run_cases(all_cases())

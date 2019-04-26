# coding=utf-8

import os
import unittest
import HTMLTestRunner
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

curr_path = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(curr_path, 'report')
case_path = os.path.join(curr_path, 'case')


def all_cases():
	if not os.path.exists(case_path):
		os.mkdir(case_path)

	discover_cases = unittest.defaultTestLoader.discover(case_path)  # cases
	return discover_cases


def run_cases(cases):
	if not os.path.exists(report_path):
		os.mkdir(report_path)
	now = time.strftime("%Y%m%d%H%M%S")
	report = os.path.join(report_path, now + '-result.html')

	f = open(report, 'wb')
	runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='test')
	runner.run(cases)
	f.close()


def get_report():
	lists = os.listdir(report_path)
	lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
	report_file = os.path.join(report_path, lists[-1])
	return report_file


def send_mail(report_file, sender='xxx', psw='xxx', my_server='smtp.qq.com', port='25', receiver='xxx'):
	with open(report_file, 'rb') as f:
		mail_body = f.read()
	msg = MIMEMultipart()
	body = MIMEText(mail_body, 'html', 'utf-8')
	msg['Subject'] = 'auto test'
	msg['from'] = sender
	msg['to'] = psw
	msg.attach(body)

	# 附件
	att = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
	att['content-type'] = 'application/octet-stream'
	att['content-disposition'] = 'attachment;filename="test.html"'
	msg.attach(att)
	# 发邮件
	smtp = smtplib.SMTP_SSL(my_server, port)
	smtp.login(sender, psw)
	smtp.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
	smtp.quit()


if __name__ == '__main__':
	run_cases(all_cases())
# report_1 = get_report()
# send_mail(report_1)

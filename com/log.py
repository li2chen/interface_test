# coding=utf-8

import logging
import os
import time

curr_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(os.path.dirname(curr_path), 'logs')
if not os.path.exists(log_path):
	os.mkdir(log_path)


class Logger(object):
	def __init__(self, logger):
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		now = time.strftime('%Y%m%d%H%M%S')

		log_name = os.path.join(log_path, now + '.log')
		fh = logging.FileHandler(log_name, encoding='utf-8')
		fh.setLevel(logging.INFO)

		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)

		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	def log(self):
		return self.logger

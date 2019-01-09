# coding=utf-8

import logging
import os
import time


class Logger(object):
	def __init__(self, logger):
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		# rq = time.strftime('%Y%m%d-%H%M', time.localtime(time.time()))
		rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))

		log_path = os.path.dirname(os.getcwd()) + '/log/'
		log_name = log_path + rq + '.log'
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

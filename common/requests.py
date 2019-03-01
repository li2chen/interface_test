# coding=utf-8
import requests
from common.log import Logger
from common.config import get_config

log = Logger('REQUEST_LOG').log()


def request(method, url, headers=None, params=None, data=None, json=None, verify=None):
	resp = None
	try:
		log.info(f'方法 -> {method}, url -> {url}; 请求头 -> {headers}, 参数 -> {data}{json}{params}'.replace('None', ''))
		if method.upper() == 'POST':
			resp = requests.post(url=url, headers=headers, data=data, json=json, verify=verify)
			log.info(f'请求结果 -> {resp.text}')
		elif method.upper() == 'GET':
			resp = requests.get(url=url, headers=headers, params=params, verify=verify)
			log.info(f'请求结果 -> {resp.text}')
		else:
			log.error(f'method should be get or post, but {method}')
		return resp
	except BaseException as e:
		log.error('请求失败，msg ->', e)


def __get_host(index='url', item='host'):
	host = get_config(index, item)
	return host


def get_host():
	return __get_host()


def __get_pay_host(index='url', item='host_pay'):
	return get_config(index, item)


def get_pay_host():
	return __get_pay_host()


def __get_sms_host(index='url', item='host_sms'):
	return get_config(index, item)


def get_sms_host():
	return __get_sms_host()

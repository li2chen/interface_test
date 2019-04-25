# coding=utf-8
import requests
from com.log import Logger
from config.config import get_interface_host

log = Logger('REQUEST_LOG').log()
host = get_interface_host()


def request(method, url, headers=None, params=None, data=None, json=None, verify=None):
	if method.upper() not in ('POST', 'GET', 'PUT', 'DELETE'):
		log.error(f'method support only [get/post/put/delete], but {method}')
		return
	if 'http' not in url:
		url = host + url
	try:
		log.info('method >>> {}, url >>> {}; headers >>> {}, params >>> {}{}{}'.format(
			method, url, headers, data, json, params).replace('None', ''))
		if method.upper() == 'POST':
			resp = requests.post(url=url, headers=headers, data=data, json=json, verify=verify)
		elif method.upper() == 'GET':
			resp = requests.get(url=url, headers=headers, params=params, verify=verify)
		elif method.upper() == 'PUT':
			resp = requests.put(url=url, headers=headers, params=params, verify=verify)
		else:
			resp = requests.delete(url=url, headers=headers, params=params, verify=verify)
		log.info('请求结果 >>> {}'.format(resp.text))
		return resp
	except BaseException as e:
		log.error('请求失败，msg >>>', e)
		raise Exception(u'请求失败')

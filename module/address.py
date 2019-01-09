# coding=utf-8
from common.requests import request, get_host
from common.log import Logger

log = Logger('ADDRESS_LOG').log()
host = get_host()


def last_address(headers):
	url = '/addr/last'
	log.info('method : last_address() --> begin')
	resp = request('get', host + url, headers=headers)
	log.info('method : last_address() result :' + resp.text)
	log.info('method : last_address() --> end')
	return resp


def last_address_id(headers):
	resp = last_address(headers)
	log.info('method : last_address_id() --> begin')
	address_id = resp.json().get('result').get('addr_id')
	log.info('method : last_address_id() result :' + str(address_id))
	log.info('method : last_address_id() --> end')
	return address_id

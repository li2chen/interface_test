# coding=utf-8


from common.log import Logger
from common.requests import get_host, request

host = get_host()
log = Logger('DONOR_LOG').log()


def donor_ranking(headers):
	url = '/statistics/sunshine/donors'
	log.info('method : donor_ranking() --> begin')
	resp = request('get', host + url, headers=headers)
	log.info('method : donor_ranking() --> end')
	return resp


def get_open_id(headers):
	# result donor open_id
	resp = donor_ranking(headers)
	log.info('method : get_open_id() --> begin')
	open_id = resp.json().get('result').get('donor').get('open_id')
	log.info('method : get_open_id() --> end')
	return open_id

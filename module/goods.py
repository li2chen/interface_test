# coding=utf-8

from common.log import Logger
from common.requests import get_host, request

log = Logger('GOODS_LOG').log()
host = get_host()


def goods_detail(goods_id, project_code=44030025):
	url = f'/goods/info/{goods_id}'
	params = {'project_code': project_code}
	log.info('method : goods_detail() --> begin')
	resp = request(method='get', url=host + url, params=params)
	log.info('method : goods_detail() --> begin')
	return resp

# coding=utf-8

from common.requests import request as req
from common.requests import get_host
from common.log import Logger
from common.sql.product import product

log = Logger('CART_LOG').log()
host = get_host()


def get_cart(headers):
	log.info('method get_cart()--> begin')
	url = '/cart/list'
	resp = req(method='get', url=host + url, headers=headers)
	log.info('method get_cart()--> end')
	return resp


def update_cart(headers, goods_id, project_code=44030052, num=1, is_add=1):
	log.info('method update_cart()--> begin')
	url = '/cart/update'
	# args = ('id', 'price')
	# result = module_index(product, goods_id, *args)
	# product_id = int(result[0])
	product_id = product(goods_id, 'id')
	price = int(product(goods_id, 'price'))
	log.info('update_cart: product_id : %s , price : %s' % (product_id, price))
	data = {
		"project_code": project_code,
		"goods_id": goods_id,
		"product_id": product_id,
		"num": num,
		"price": price,
		"is_add": is_add
	}
	resp = req(method='pOst', url=host + url, headers=headers, json=data)
	log.info('method update_cart()--> end')
	return resp

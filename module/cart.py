# coding=utf-8


from com.req import request
from com.sql.product import product


def get_cart(headers):
	url = '/cart/list'
	return request(method='get', url=url, headers=headers)


def update_cart(headers, goods_id, project_code=44030052, num=1, is_add=1):
	url = '/cart/update'
	product_info = product(goods_id)
	product_id = product_info['id']
	price = int(product_info['price'])
	data = {
		"project_code": project_code,
		"goods_id": goods_id,
		"product_id": product_id,
		"num": num,
		"price": price,
		"is_add": is_add
	}
	return request(method='post', url=url, headers=headers, json=data)

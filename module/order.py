# coding=utf-8
from common.requests import request as req
from module.login import login_token
from module.address import last_address_id as address_id
from common.requests import get_host

from common.sql.product import product
from common.sql.goods import goods
from common.sql.logistics import logistics_info
from common.sql.activity import activity, exists_activity
from common.sql.order import orders

from common.log import Logger

log = Logger('ORDER_LOG').log()
host = get_host()


def _create_order1(headers, goods_id, bounty=0):
	url = '/order/create'
	log.info('method create_order()--> begin')
	address = address_id(headers)
	product_id = product(goods_id, 'id')
	snap_id = goods(goods_id, 'snap_id')
	price = int(product(goods_id, 'price') * 100)
	shipping = int(logistics_info(goods(goods_id, 'logistics_template_id'), 'price') * 100)
	order_price = price + shipping
	log.info('create_order --> product_id: %s, price(分): %s, snap_id: %s, logistics_price: %s, order_price: %s' % (
		product_id, price, snap_id, shipping, order_price))
	data = {
		"goods": [{
			"goods_id": goods_id,
			"product_id": product_id,
			"price": price,
			"num": 1,

			# "activity": "",
			# "activity": {
			# 	"id": 627,
			# 	"price": 2000,
			# 	"type": "GROUPON"
			# },

			"snap_id": snap_id,
			"user_info": []
		}],
		"shiping": shipping,
		"order_price": order_price,
		"addr_id": address,
		"comments": [],
		"ticket_nos": [],
		"open_bounty": "true",
		"bounty": bounty  # 奖励金
	}
	resp = req(method='post', url=host + url, headers=headers, json=data)
	log.info('method create_order()--> end')
	return resp


def order(headers, goods_id):
	res = _create_order(headers=headers, goods_id=goods_id)
	pay_id = res.json().get('result').get('order_id')
	order_id = orders(payment_id=pay_id, key='id')
	log.info(f'pay_id : {pay_id} , order_id : {order_id}')
	return pay_id


def _create_order(headers, goods_id, bounty=0):
	url = '/order/create'
	log.info('method create_order()--> begin')
	address = address_id(headers)
	product_id = product(goods_id, 'id')
	snap_id = goods(goods_id, 'snap_id')
	# 活动商品
	activity_id = activity(goods_id=goods_id, key='id')
	has_activity = exists_activity(goods_id)
	if has_activity:
		price = int(activity(goods_id=goods_id, key='activity_min_price') * 100)
	else:
		price = int(product(goods_id, 'price') * 100)
	shipping = int(logistics_info(goods(goods_id, 'logistics_template_id'), 'price') * 100)
	order_price = price + shipping
	log.info('create_order --> product_id: %s, price(分): %s, snap_id: %s, logistics_price: %s, order_price: %s' % (
		product_id, price, snap_id, shipping, order_price))
	data = {
		"goods": [{
			"goods_id": goods_id,
			"product_id": product_id,
			"price": price,
			"num": 1,
			"snap_id": snap_id,
			"user_info": []
		}],
		"shiping": shipping,
		"order_price": order_price,
		"addr_id": address,
		"comments": [],
		"ticket_nos": [],
		"open_bounty": "true",
		"bounty": bounty  # 奖励金

	}
	data_activity = {
		"goods": [{
			"goods_id": goods_id,
			"product_id": product_id,
			"price": price,
			"num": 1,
			"activity": {
				"id": activity_id,
				"price": price,
				"type": "GROUPON"
			},
			"snap_id": snap_id,
			"user_info": []
		}],
		"shiping": shipping,
		"order_price": order_price,
		"addr_id": address,
		"comments": [],
		"ticket_nos": [],
		"open_bounty": "true",
		"bounty": bounty  # 奖励金
	}
	if not has_activity:
		resp = req(method='post', url=host + url, headers=headers, json=data)
	else:
		resp = req(method='post', url=host + url, headers=headers, json=data_activity)
	log.info('method create_order()--> end')
	return resp


if __name__ == '__main__':
	headers1 = login_token()
	pay = order(headers=headers1)

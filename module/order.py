# coding=utf-8
from common.requests import request as req
from module.address import last_address_id as address_id
from common.requests import get_host

from common.sql.product import product
from common.sql.goods import goods
from common.sql.logistics import logistics_info
from common.sql.activity import activity, exists_activity
from common.sql.order import orders

from common.log import Logger
from module.goods import goods_detail

log = Logger('ORDER_LOG').log()
host = get_host()


def order(headers, goods_id, num=1):
	res = _create_order(headers=headers, goods_id=goods_id, num=num)
	if res:
		pay_id = res.json().get('result').get('order_id')
		order_id = orders(payment_id=pay_id, key='id')
		log.info(f'pay_id : {pay_id} , order_id : {order_id}')
		return pay_id
	else:
		log.error('create_order() failed')


def _create_order(headers, goods_id, num=1):
	url = '/order/create'
	log.info('method create_order()--> begin')
	try:
		address = address_id(headers)
		product_info = product(goods_id=goods_id)
		product_id = product_info['id']
		goods_info = goods(goods_id=goods_id)
		snap_id = goods_info['snap_id']
		# 活动相关
		activity_info = activity(goods_id=goods_id)  # 活动商品
		activity_active = exists_activity(goods_id=goods_id)  # 有效活动
		if activity_info and activity_active:  # 存在活动且有效，则取活动价格
			activity_id = activity_info['id']
			price = int(activity_info['activity_min_price'] * 100)
		else:
			activity_id = ''
			price = int(product_info['price'] * 100)
		shipping = int(logistics_info(goods_info['logistics_template_id'], 'price') * 100)
		# 奖励金
		resp_calc = coupon_calc(headers=headers, goods_id=goods_id, product_id=product_id, num=num)
		bounty = resp_calc.json().get('result').get('bounty')
		# 支付金额
		order_price = price + shipping - bounty
		data = {
			"goods": [{
				"goods_id": goods_id,
				"product_id": product_id,
				"price": price,
				"num": num,
				"snap_id": snap_id,
				"user_info": []
			}],
			"shiping": shipping,
			"order_price": order_price,
			"addr_id": address,
			"comments": [],
			"ticket_nos": [],
			"open_bounty": "true",
			"bounty": bounty * num
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
			"bounty": bounty * num  # 奖励金，要根据数量翻倍
		}
		if not activity_id:  # 非活动商品下单
			resp = req(method='post', url=host + url, headers=headers, json=data)
		else:
			resp = req(method='post', url=host + url, headers=headers, json=data_activity)
		log.info('method create_order()--> end')
		if resp.status_code == 200 and resp.json().get('message') == 'success':
			return resp
	except Exception as e:
		log.error('create_order() failed', e)


def coupon_calc(headers, goods_id, product_id=None, num=1):
	url = '/coupon/calc'
	try:
		log.info('method coupon_calc()--> begin')
		product_info = product(goods_id=goods_id)
		goods_info = goods(goods_id=goods_id)
		activity_info = activity(goods_id=goods_id)
		if not product_id:
			product_id = product_info['id']
		supplier_id = goods_info['supplier_id']
		category_id = goods_info['category_id']
		if activity_info:
			activity_id = activity_info['id']
			price = int(activity_info['activity_min_price'] * 100)
		else:
			activity_id = ''
			price = int(product_info['price'] * 100)
		data = {
			"goods_products": [{
				"goods_id": goods_id,
				"product_id": product_id,
				"supplier_id": supplier_id,
				"price": price,
				"num": num,
				"activity_type": "GROUPON",
				"category_id": category_id,
				"activity_id": activity_id}],
			"ticket_nos": [],
			"type": "ALL"}
		resp = req(method='post', headers=headers, url=host + url, json=data)
		if resp.status_code == 200 and resp.json().get('message') == 'success':
			log.info('method coupon_calc()--> end')
			return resp
	except Exception as e:
		log.error('coupon_calc() failed', e)

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
		order_price = price + shipping
		# 奖励金
		bounty = goods_detail(goods_id=goods_id).json().get('result').get('bounty')
		if bounty:  # 如果有奖励金，订单价格要减去奖励金；上面是单个商品的奖励金，如果多个商品，则要乘以数量
			order_price = price * num + shipping - int(bounty) * num
		else:
			log.error('获取奖励金数据失败，下单时设置奖励金为0')
			bounty = 0
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

# coding=utf-8
from common.requests import request, get_host
from common.log import Logger
from common.sql.order_item import order_item
from common.sql.order import orders

host = get_host()
log = Logger('SERVICE_LOG').log()


def get_service_reason(project_code, order_id, service_type):
	url = '/aftersales/service/goods'
	item_id = order_item(order_id=order_id, key='id')
	params = {'project_code': project_code, 'order_id': order_id, 'item_id': item_id, 'type': service_type}
	log.info('method : get_service_reason() --> begin ')
	result = request(method='get', url=host + url, params=params)
	log.info('method : get_service_reason() --> end ')
	return result


def apply_service(headers, order_id, project_code=44030052, service_type='REFUNDONLY'):
	resp_result = get_service_reason(project_code=project_code, order_id=order_id, service_type=service_type)
	if resp_result.json().get('result') == '不支持的售后类型':
		log.error('method get_service_reason() occurred error ,method apply_service(): run over')
		return
	else:
		reason = resp_result.json().get('result').get('after_service_reason')[0].get('value')  # 默认获取第一个原因
	url = '/aftersales/service/apply'
	# 判断发起的售后是否合理
	order_status = orders(order_id=order_id, key='order_status')
	if order_status in ('PAID', 'DELIVERED', 'RECEIVED'):
		if order_status == 'PAID' and service_type != 'REFUNDONLY':
			log.error(f'order_status : {order_status} ,can not apply service : {service_type}')
			return
	else:
		log.error(
			f'only order_status in [PAID, DELIVERED, RECEIVED] can apply service ,current order_status : {order_status}')
		return
	item = order_item(order_id=order_id, key='id')
	item_price = int(order_item(order_id=order_id, key='price') * 100)
	item_qty = order_item(order_id=order_id, key='quantity')
	shipping = int(orders(order_id=order_id, key='shipping') * 100)
	if service_type == 'REFUNDONLY':
		price = item_price * item_qty + shipping
	else:
		price = item_price * item_qty
	data = {
		"project_code": project_code,
		"type": service_type,
		"order_id": order_id,
		"item_id": item,
		"imgs": [],
		"after_service_reason": reason,
		"illustration": "Test",
		"price": price
	}
	log.info('method : apply_service() --> begin')
	resp = request(method='post', url=host + url, headers=headers, json=data)
	log.info('method : apply_service() --> end')
	return resp


def service_list(order_id, project_code='44030011'):
	url = '/aftersales/services/list'
	item_id = order_item(order_id=order_id, key='id')
	params = {'project_code': project_code, 'order_id': order_id, 'item_id': item_id}
	log.info('method : service_list() --> begin')
	resp = request(method='get', url=host + url, params=params)
	log.info('method : service_list() --> end')
	return resp


def service_get_logistics(headers, order_id, project_code='44030011'):
	url = '/aftersales/logistics/info'
	service_id = order_item(order_id=order_id, key='current_service')
	params = {'project_code': project_code, 'order_id': order_id, 'service_id': service_id}
	log.info('method : service_get_logistics() --> begin')
	resp = request(method='get', headers=headers, url=host + url, params=params)
	log.info('method : service_get_logistics() --> end')
	return resp


def return_logistics_info(headers, order_id, project_code='44030011', express_company='YUANTONG', express_no='A000001'):
	url = '/aftersales/goods/logistics'
	item_id = order_item(order_id=order_id, key='id')
	service_id = order_item(order_id=order_id, key='current_service')
	data = {
		"project_code": project_code,
		"order_id": order_id,
		"item_id": item_id,
		"after_service_id": service_id,
		"express_company_code": express_company,
		"tracking_number": express_no,
		"imgs": []
	}
	log.info('method : return_logistics_info() --> begin')
	resp = request(method='post', headers=headers, url=host + url, json=data)
	log.info('method : return_logistics_info() --> end')
	return resp

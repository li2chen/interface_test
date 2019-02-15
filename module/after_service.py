from common.requests import request, get_host
from common.log import Logger

from common.sql import order_item

host = get_host()
log = Logger('SERVICE_LOG').log()


def service_apply(headers, order_id, project_code=44030011, apply_type='RETURNPRODUCTANDREFUND', item_id=None):
	url = '/aftersales/service/apply'
	log.info('service_apply() --> begin , order_id --> %s ' % order_id)
	try:
		# apply_type类型和原因
		my_apply = {
			'REFUNDONLY': 'NOTRECEIVED',
			'RETURNPRODUCTANDREFUND': 'DELIVERYMISTAKE',
			'CHANGEPRODUCT': 'QUALITYPROBLEM'}
		if apply_type in my_apply.keys():
			after_service_reason = my_apply.get(apply_type)
		else:
			log.error('only [REFUNDONLY,RETURNPRODUCTANDREFUND,CHANGEPRODUCT] can select')
			return
		# 获取item_id、item_status、单价、数量，并设置申请退款金额（全额）
		if not item_id:
			item = order_item.order_item(order_id=order_id)
			item_id = item['id']
			item_status = item.get('item_status')
			item_price = item.get('price')
			item_qty = item.get('quantity')
			price = int(item_price * 100) * item_qty
		else:
			item = order_item.order_item(order_id=order_id, item_id=item_id)
			item_status = item.get('item_status')
			item_price = item.get('price')
			item_qty = item.get('quantity')
			price = int(item_price * 100) * item_qty
		# 根据item_status判断发起的售后是否合理
		if item_status in ('PAID', 'DELIVERED', 'RECEIVED'):
			if item_status == 'PAID' and apply_type != 'REFUNDONLY':
				log.error(f'item_status : [PAID] can not apply service : [REFUNDONLY]')
				return
			elif item_status in ('DELIVERED', 'RECEIVED') and apply_type not in (
					'RETURNPRODUCTANDREFUND', 'CHANGEPRODUCT'):
				log.error(
					f'only item_status : [PAID] can not apply service : [REFUNDONLY] , but current item_status :{item_status}')
				return
		else:
			log.error(
				f'only item_status in [PAID, DELIVERED, RECEIVED] can apply service ,current item_status : {item_status}')
			return
		data = {
			"project_code": project_code,
			"type": apply_type,
			"order_id": order_id,
			"item_id": item_id,
			"imgs": [],
			"after_service_reason": after_service_reason,
			"illustration": "Test",
			"price": price
		}
		resp = request(method='post', headers=headers, url=host + url, json=data)
		if resp.status_code == 200 and resp.json().get('code') == 0:
			log.info('service_apply() success')
			return resp
		else:
			log.error('service_apply() failed --> ' + resp.text)
	except Exception as e:
		log.error('service_apply() failed :', e)


def service_cancel(headers, order_id, item_id=None, project_code=44030011):
	url = '/aftersales/service/cancel/service_id'
	try:
		log.info('service_detail() --> begin , order_id --> %s ' % order_id)
		detail_resp = service_detail(headers=headers, order_id=order_id, item_id=item_id, project_code=project_code)
		service_id = detail_resp.json().get('result').get('after_service_id')
		url2 = url.replace('service_id', str(service_id))
		data = {"project_code": project_code}
		resp = request(method='post', headers=headers, url=host + url2, data=data)
		return resp
	except Exception as e:
		log.error('service_cancel() failed :', e)


def service_detail(headers, order_id, item_id=None, project_code=44030011):
	url = '/aftersales/services/list'
	try:
		log.info('service_detail() --> begin , order_id --> %s ' % order_id)
		if not item_id:
			item_info = order_item.order_item(order_id=order_id)
			item_id = item_info['id']
		params = {
			"project_code": project_code,
			"order_id": order_id,
			"item_id": item_id
		}
		resp = request(method='get', headers=headers, url=host + url, params=params)
		return resp
	except Exception as e:
		log.error('service_detail() failed :', e)


def service_reason(headers, apply_type, order_id, item_id=None, project_code=44030011, ):
	url = '/aftersales/service/goods'
	try:
		log.info('service_reason() --> begin , order_id --> %s ' % order_id)
		if apply_type not in ['REFUNDONLY', 'RETURNPRODUCTANDREFUND', 'CHANGEPRODUCT']:
			log.error(f'can only [REFUNDONLY, RETURNPRODUCTANDREFUND, CHANGEPRODUCT] ,but [{apply_type}]')
			return
		if not item_id:
			item_info = order_item.order_item(order_id=order_id)
			item_id = item_info['id']
		params = {
			'project_code': project_code,
			'order_id': order_id,
			'item_id': item_id,
			'type': apply_type
		}
		resp = request(method='get', headers=headers, url=host + url, params=params)
		return resp
	except Exception as e:
		log.error('service_detail() failed :', e)


def service_logistics(headers, order_id, item_id=None, service_id=None, project_code=44030011):
	url = '/aftersales/goods/logistics'
	try:
		log.info('service_logistics() --> begin , order_id --> %s ' % order_id)
		if not item_id:
			item_info = order_item.order_item(order_id=order_id)
			item_id = item_info['id']
			service_id = item_info['current_service']
		data = {
			"project_code": project_code,
			"order_id": order_id,
			"item_id": item_id,
			"after_service_id": service_id,
			"express_company_code": "SHUNFENG",
			"tracking_number": "123456abc",
			"imgs": []}
		resp = request(method='post', headers=headers, url=host + url, json=data)
		return resp
	except Exception as e:
		log.error('service_logistics() failed :', e)

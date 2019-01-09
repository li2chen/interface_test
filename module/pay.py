# coding=utf-8
from common.requests import request, get_host, get_pay_host, get_sms_host
from common.log import Logger
from module.donor import get_open_id
import re

host = get_host()
host_pay = get_pay_host()
host_sms = get_sms_host()
log = Logger('PAY_LOG').log()


def get_pay_info(headers, payment_id):
	# 快捷支付方式获取支付信息
	url = '/payment/pay'
	open_id = get_open_id(headers)
	pay_data = {
		"order_id": payment_id,
		"pay_method": "hundsun_quick_pay",
		"user_id": open_id,
	}
	log.info('method : get_pay_info() --> begin --> payment_id : %s' % payment_id)
	res = request(method='post', url=host + url, headers=headers, json=pay_data)
	log.info('method : get_pay_info() --> end')
	pay_info = res.json().get('result').get('pay_info')
	return pay_info


def get_bind_id(headers, pay_info):
	# 支付token(bind_id)
	url = '/cards'
	params = {'token': pay_info}
	log.info('method : get_bind_id() --> begin')
	res = request(method='get', url=host_pay + url, params=params, headers=headers)
	log.info('method : get_bind_id() --> end')
	bind_id = res.json().get('result').get('cards')[0].get('bind_id')
	return bind_id


def get_pay_token(headers, bind_id, pay_info):
	# 支付触发验证码
	url = '/pay'
	data_quick_pay = {
		"bind_id": bind_id,
		"token": pay_info,
	}
	log.info('method : get_pay_token() --> begin')
	res = request(method='post', url=host_pay + url, headers=headers, json=data_quick_pay)
	log.info('method : get_pay_token() --> end')
	quick_pay_token = res.json().get('result').get('quick_pay_token')
	return quick_pay_token


def get_sms(phone=110):  # 手机号
	log.info('method : get_sms() --> begin')
	res = request(method='get', url=host_sms)
	sms_phone = int(res.json().get('body')[-1].get('phone'))
	if sms_phone == phone:
		sms_info = res.json().get('body')[-1].get('msg')  # 最新的一条信息
		sms = re.findall('\d+', sms_info)[0]  # 从msg获取手机验证码
		log.info('method : get_sms() --> end -- > sms : %s' % sms)
	else:
		print(phone, 'do not receive any sms, check please first ')
		return None
	return int(sms)


def confirm_pay(headers, pay_info, quick_pay_token, sms):
	url = '/confirm_sms'
	data = {
		'sms_code': sms,
		'quick_pay_token': quick_pay_token,
		'token': pay_info,
	}
	log.info('method : confirm_pay() --> begin')
	res = request(method='post', url=host_pay + url, headers=headers, json=data)
	log.info('method : confirm_pay() --> end')
	if res.status_code == 200:
		transaction_id = res.json().get('result').get('transaction_id')
		log.info(f'method : confirm_pay() --> transaction_id : {transaction_id}')
		return transaction_id
	else:
		pass


def pay(headers, payment_id):
	pay_info = get_pay_info(headers, payment_id)
	bind_id = get_bind_id(headers, pay_info)
	pay_token = get_pay_token(headers, bind_id, pay_info)
	sms = get_sms(phone)
	return confirm_pay(headers, pay_info, pay_token, sms)

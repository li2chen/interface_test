# coding=utf-8
from module.order import order
from module.pay import pay
from module.login import login_token
from common.log import Logger

log = Logger('TEST_ORDER').log()


def choice(operation='create', goods_id=None, pay_id=None):
	headers = login_token()
	if operation == 'create':
		pay_id = order(headers, goods_id=goods_id)
		return pay_id
	elif operation == 'pay':
		trans_id = pay(headers=headers, payment_id=pay_id)
		return trans_id
	elif operation == 'all':
		pay_id = order(headers, goods_id=goods_id)
		trans_id = pay(headers=headers, payment_id=pay_id)
		return pay_id, trans_id
	else:
		log.error('operation args wrong: ' + operation)


if __name__ == '__main__':
	for i in range(1):
		choice(operation='all', goods_id=1655, pay_id=1901073398190793)  # 1655

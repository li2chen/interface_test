# coding=utf-8
from com.sql.order import orders
import requests
from module.login import login_token
from com.requests import request
from module.user import get_hotmoney

from com.sql import order_item

orders()

item = order_item.order_item(order_id=1901316050103376)
item_id = item['id']
item_status = item['item_status']
item_price = item['price']
item_qty = item['quantity']

item2 = order_item.order_item(order_id=1901316050103376, item_id=6241)
item_id2 = item2.get('id')
item_status2 = item2.get('item_status')
item_price2 = item2.get('price')
item_qty2 = item2.get('quantity')

'''
if not item_id:
	columns = order_item.order_item_columns(order_id, *('id', 'item_status', 'price', 'quantity'))
	item_id = columns[0]
	item_status = columns[1]
	item_price = columns[2]
	item_qty = columns[3]
	price = int(item_price * 100) * item_qty
else:
	item_status = order_item.order_item(order_id=order_id, item_id=item_id, key='item_status')
	item_price = order_item.order_item(order_id=order_id, item_id=item_id, key='price')
	item_qty = order_item.order_item(order_id=order_id, item_id=item_id, key='quantity')
	price = int(item_price * 100) * item_qty
'''

'''
id1 = orders(payment_id='1901093769492486')
id2 = orders(payment_id='1901093769492486', key='id')
id3 = orders(order_id=1901093769492408)
id4 = orders(order_id=1901093769492408, key='payment_id')
id5 = orders(payment_id='1901093769492486', order_id=1901093769492408)
id6 = orders(payment_id='1901093769492486', order_id=1901093769492408, key='payment_id')
print(id1, id2, id3, id4, id5, id6)
'''
# url = 'https://127.0.0.1/payment/notify/order'


# data = {
# 	"business_type": "BU6-01",
# 	"client_order_no": "1901083595291021",
# 	"time_end": "20181214113942",
# 	"payment_trn_no": "TEST20181214113900000006",
# 	"pay_method": "hundsun_wechat",
# 	"transaction_id": "TEST20181214113900000006"
# }
# resp = request(method='post', url=url, headers=h, data=data, verify=False)
# resp = request(method='post', url=url, json=data, verify=False)

# print(resp.status_code)

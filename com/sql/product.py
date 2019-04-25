# coding=utf-8
from com.db import exec_sql


def product(goods_id, key=None):
	sql = f'select * from goods_product where goods_id = {goods_id} and disabled = 0'
	return exec_sql(sql=sql, key=key)

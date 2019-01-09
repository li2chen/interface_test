# coding=utf-8

from common.conn_db import exec_sql


# eg:
def table_name(key_name=None, key_name2=None, key=None):
	if key_name and not key_name2:
		sql = f'select *  from table_name where key_name ={key_name}'
	elif key_name2 and not key_name:
		sql = f'select *  from table_name where key_name2 = {key_name2})'
	else:
		sql = f'select *  from table_name where (table_name = {table_name} and key_name2 ={key_name2})'
	result = exec_sql(sql=sql, key=key)
	return result

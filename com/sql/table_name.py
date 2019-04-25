# coding=utf-8

from com.db import exec_sql


# eg:
def table_name(key_name=None, key_name2=None, key=None):
	if key_name and not key_name2:
		sql = 'select * from table_name where key_name ={}'.format(key_name)
	elif key_name2 and not key_name:
		sql = 'select * from table_name where key_name2 = {}'.format(key_name2)
	else:
		sql = 'select * from table_name where (key_name = {} and key_name2 ={})'.format(key_name, key_name2)
	result = exec_sql(sql=sql, key=key)
	return result

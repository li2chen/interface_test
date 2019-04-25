# coding=utf-8
import pymysql
from config.config import get_db_info
from com.log import Logger
import json

log = Logger('DB_LOG').log()
db_info = json.loads(get_db_info())


def get_conn():
	return pymysql.connect(**db_info)


def close_db(conn, cursor):
	try:
		log.info('close db begin')
		if not cursor:
			cursor.close()
		if not conn:
			conn.close()
		log.info('close db success')
	except BaseException as e:
		log.error('close db error : ', e)


def exec_sql(sql, args=None, key=None):
	conn = get_conn()
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	result = ''
	log.info('exec sql >>> ' + sql)
	try:
		if not args:
			cursor.execute(query=sql)
			exec_result = cursor.fetchone()
			if exec_result and key:
				result = exec_result[key]
			else:
				result = exec_result
		else:
			cursor.execute(query=sql, args=args)
			exec_result = cursor.fetchone()
			if exec_result and key:
				result = exec_result[key]
			else:
				result = exec_result
	except BaseException as e:
		log.error('exec sql error >>>', e)
		conn.rollback()
	finally:
		conn.commit()
		close_db(conn, cursor)
	log.info('exec result >>> ' + str(result))
	return result


def module_index(func, arg, *args):
	index = len(args)
	result = []
	if index == 0:
		result = func(arg)
	else:
		while index > 0:
			for key in args:
				res = func(arg)[key]
				index -= 1
				result.append(res)
	return result

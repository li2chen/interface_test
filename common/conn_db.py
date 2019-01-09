# coding=utf-8
import pymysql
from common.config import get_config
import json
from common.log import Logger

log = Logger('DB_LOG').log()


def get_conn(index='db', item='db_info'):
	conn = pymysql.connect(**json.loads(get_config(index, item)))
	log.info('connect mysql success')
	return conn


def close_db(conn, cursor):
	try:
		if not cursor:
			cursor.close()
		if not conn:
			conn.close()
		log.info('close db success')
	except:
		log.error('close db error')
		print('error')


def exec_sql(sql, args=None, key=None):
	conn = get_conn()
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	result = ''
	log.info('exec sql --> begin')
	try:
		if not args:
			cursor.execute(query=sql)
			exec_result = cursor.fetchone()
			if not key:
				result = exec_result
			else:
				result = exec_result[key]
			log.info('exec sql --> end')
		else:
			cursor.execute(query=sql, args=args)
			exec_result = cursor.fetchone()
			if not key:
				result = exec_result
			else:
				result = exec_result[key]
			log.info('exec sql --> end')
	except:
		log.error('exec sql --> error')
		conn.rollback()
	finally:
		conn.commit()
		close_db(conn, cursor)
	log.info('exec_result : ↓↓↓')
	log.info(result)
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

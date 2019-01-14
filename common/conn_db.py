# coding=utf-8
import pymysql
from common.config import get_config
import json
from common.log import Logger

# import traceback

log = Logger('DB_LOG').log()


def get_conn(index='db', item='db_info'):
	conn = pymysql.connect(**json.loads(get_config(index, item)))
	return conn


def close_db(conn, cursor):
	try:
		log.info('close db --> begin')
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
	log.info('exec sql --> begin ; sql -- >' + sql)
	try:
		if not args:
			cursor.execute(query=sql)
			exec_result = cursor.fetchone()
			if not key:
				result = exec_result
			else:
				result = exec_result[key]
		else:
			cursor.execute(query=sql, args=args)
			exec_result = cursor.fetchone()
			if not key:
				result = exec_result
			else:
				result = exec_result[key]
	except BaseException as e:
		# traceback.print_exc()
		log.error('exec sql error -->', e)
		conn.rollback()
	finally:
		conn.commit()
		close_db(conn, cursor)
	log.info('exec sql --> end ; result -- >' + str(sql))
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

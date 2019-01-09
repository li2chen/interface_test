# coding=utf-8
import configparser
import os


def get_config(index, item):
	file = os.path.dirname(os.path.abspath('.')) + '/config.properties'
	# file = os.path.abspath('.') + '/config.properties'
	config = configparser.ConfigParser()
	config.read(file)
	return config.get(index, item)


if __name__ == '__main__':
	x = get_config('db', 'db_info')
	print(x)

# coding=utf-8
import configparser
import os

curr_path = os.path.dirname(os.path.realpath(__file__))
conf_path = os.path.join(curr_path, 'config.ini')


def get_conf(index, item):
	conf = configparser.ConfigParser()
	conf.read(conf_path)
	return conf.get(index, item)


def get_h5():
	url = get_conf('H5_user', 'login_url')
	user = get_conf('H5_user', 'user1')
	data = get_conf('H5_user', 'data1')
	return url, user, data


def get_interface_host():
	return get_conf('url', 'host')


def get_db_info():
	return get_conf('db', 'db_info')

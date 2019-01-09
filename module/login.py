# coding=utf-8
from common.requests import request as req
from common.config import get_config
import json
from common.log import Logger

log = Logger('LOGIN_LOG:').log()


def _get_user(index='H5_user', item='user1'):
	user = json.loads(get_config(index, item))
	log.info(f'login user :{user}')
	return user


def _get_data(index='H5_user', item='data1'):
	data = json.loads(get_config(index, item))
	return data


def _get_login_url(index='H5_user', item='login_url'):
	url = get_config(index, item)
	return url


def _get_token(user, info, url):
	data = {"scopes": "all", "submit": ""}
	data.update(user)
	data.update(info)
	log.info(f'login data :{data}')
	log.info(f'method _get_token() --> begin')
	resp = req(method='post', url=url, data=data)
	token = resp.json().get('token')
	headers = {'x-auth-token': token}
	log.info(f'login token :{token}')
	log.info(f'method _get_token() --> end')
	return headers


def login_token():
	headers = _get_token(_get_user(), _get_data(), _get_login_url())
	return headers

# coding=utf-8
import json
from config.config import get_h5
from com.req import request

login_info = get_h5()
url = login_info[0]
user = json.loads(login_info[1])
info = json.loads(login_info[2])


def login_token():
	data = {"scopes": "all", "submit": ""}
	data.update(user)
	data.update(info)
	resp = request(method='post', url=url, data=data)
	token = resp.json().get('token')
	headers = {'x-auth-token': token}  # {'x-auth-token': '6f08952a-9a23-4ede-91b6-ff274fe4bca0'}
	return headers


if __name__ == '__main__':
	login_token()

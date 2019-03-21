import requests


class MyRequestError(Exception):
	pass


class MyRequest(object):
	def __init__(self, url, data):
		if not url:
			raise MyRequestError('url is null')
		if not data:
			raise MyRequestError('data is null')
		self.url = url
		self.data = data

	def response(self):
		resp = requests.get(url=self.url, params=self.data, verify=False)
		return resp

	def deal_response(self, resp):
		if resp.status_code == 200:
			return True
		return False

	def get_result(self):
		re = self.response()
		result = self.deal_response(re)
		return result


if __name__ == '__main__':
	my_url = 'https://www.baidu.com/'
	my_data = {'wd': 'aaa'}
	my_data1 = ''
	mr = MyRequest(my_url, my_data1)
	s = mr.get_result()
	print(s)

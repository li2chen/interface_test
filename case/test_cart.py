import unittest
from module.login import login_token
from module.cart import *


class CartTest(unittest.TestCase):
	def setUp(self):
		self.token = login_token()

	def tearDown(self):
		pass

	def test_get_cart(self):
		res = get_cart(headers=self.token)
		assert '283' in res.text

	def test_update_cart(self):
		res = update_cart(headers=self.token, goods_id=1624)
		assert 'success' in res.text

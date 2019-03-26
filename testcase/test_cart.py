import unittest
from module.login import login_token
from module.cart import update_cart


class CartTest(unittest.TestCase):
	def setUp(self):
		self.token = login_token()  #

	def tearDown(self):
		pass

	def test_update_cart(self):
		# {"code":0,"result":true,"message":"success"}
		resp = update_cart(headers=self.token, goods_id=1788)
		self.assertEqual(resp.json().get('code'), 0)
		self.assertEqual('success', resp.json().get('message'))
		self.assertTrue(resp.json().get('result'))

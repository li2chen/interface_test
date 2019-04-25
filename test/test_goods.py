# coding=utf-8

from module.goods import *

if __name__ == '__main__':
	resp = goods_detail(1673)
	bounty = resp.json().get('result').get('bounty')

# coding=utf-8


def f1(a):
	print('f1', a)


def f2(b, c, e):
	print('f2', b, c, e)


def f3(n, *args):
	if n == 1:
		f1(*args)
	elif n == 2:
		f2(*args)


if __name__ == '__main__':
	f3(2, 'a', 'b', 'x')

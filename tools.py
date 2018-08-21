# -*- coding:utf-8 -*-

import hashlib
import requests
import time
import paper_crawler.constants as constants


def generate_ruc_accounts():

	with open(constants.RUC_ACCOUNTS_FILE_PATH, 'r', encoding='utf-8') as f:
		lines = f.readlines()

	for line in lines:
		yield line.strip()


def test_connected():

	connected_flag = False
	try:
		r = requests.get(constants.TEST_URL)
		if r.status_code == requests.codes.ok:
			connected_flag = True
	except:
		pass

	return connected_flag


def connect_ruc():
	""" return True if connect successfully, else False """

	errors, max_errors = 0, 10  # 异常处理
	payload = {
		'DDDDD': '', 'upass': '',
		'hid1': '', 'hid2': '0', '0MKKey': '123456', 'R6': '0'
	}
	headers = {
		'Origin': '',
		'User-Agent': constants.ua.random,
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept': '*/*',
		'Referer': '',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh; q=0.9',
		'Connection': 'close'
	}
	cookies = {'i18n_lang': 'zh-CN', 'PHPSESSID': ''}

	for a in generate_ruc_accounts():
		if errors > max_errors:
			break
		payload['DDDDD'], payload['upass'] = a, a
		try:
			time.sleep(1)
			r = requests.post(constants.CONNECT_RUC_URL, data=payload, headers=headers, cookies=cookies)
			if r.status_code == requests.codes.ok:
				if '成功登录' in r.text:
					time.sleep(1)
					if test_connected():
						return True
				else:
					errors += 1
			else:
				errors += 1
		except:
			errors += 1

	return False


def network_tester():
	""" 实现断线重连thread """
	print('network tester is working...')
	while True:
		time.sleep(constants.NET_TEST_INTEVAL)
		if test_connected():
			continue
		else:
			for a in range(0, constants.MAX_RE_CONNECT_TIMES):
				print('network: find network broken. start re_connect...{0}'.format(a))
				if connect_ruc():
					print('network tester: re_connect successfully')
					break
				else:
					if a + 1 == constants.MAX_RE_CONNECT_TIMES:
						raise Exception('network tester: cannot connect network')


def get_hash(string):

	m = hashlib.md5()
	m.update(string.encode('utf-8'))

	return m.hexdigest()


if __name__ == '__main__':
	pass

# -*- coding:utf-8 -*-

import requests
import time
import paper_crawler.constants as constants


def get_headers():

	headers = {
		'Connection': 'keep-alive',
		'Accept': 'application/json, text/plain, */*',
		'User-Agent': constants.ua.random,
		'token': constants.TOKEN,
		'deviceType': 'web',
		'Referer': '',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
	}

	return headers


def get_session():

	s = requests.Session()
	headers = get_headers()
	s.headers.update(headers)

	return s


def check_r(r):

	if r.status_code == requests.codes.ok:
		json_res = r.json()
		if json_res.get('result', ''):
			return True, json_res
		else:
			return True, ''
	elif r.status_code > 299:
		return True, ''

	return False, ''


def check_r_for_law(r):

	if r.status_code == requests.codes.ok:
		json_res = r.json()
		if json_res.get('data', ''):
			return True, json_res
		else:
			return True, ''
	elif r.status_code > 299:
		return True, ''

	return False, ''


def get_res_json_for_list(thread_id, s, payload):
	""" 实现异常处理 """
	re_request_times = 0
	r_status, json_res = False, ''
	while not r_status:
		if re_request_times == constants.MAX_RE_REQUEST_TIMES:
			raise requests.HTTPError('reach max_request_times')
		if re_request_times > 0:
			print('thread_id: {0}, re_request_times: {1}'.format(thread_id, re_request_times))
		time.sleep(constants.RE_REQ_TIME_SLEEP)
		try:
			res = s.get(constants.LIST_URL, params=payload, headers={'User-Agent': constants.ua.random}, timeout=constants.REQ_TIME_OUT)
			r_status, json_res = check_r(res)
			if not r_status:
				re_request_times += 1
		except:
			re_request_times += 1

	return json_res


def get_res_json_for_single(req_id, session, url):
	""" like get_res_json_for_list() 实现异常检测 """
	re_request_times = 0
	r_status, json_res = False, ''
	while not r_status:
		if re_request_times == constants.MAX_RE_REQUEST_TIMES:
			raise requests.HTTPError('reach max_request_times')
		if re_request_times > 0:
			print('req_id: {0}, re_request_times: {1}'.format(req_id, re_request_times))
		time.sleep(constants.TIME_SLEEP_FOR_REQ)
		try:
			res = session.get(url, headers={'User-Agent': constants.ua.random}, timeout=constants.REQ_TIME_OUT)
			r_status, json_res = check_r(res)
			if not r_status:
				re_request_times += 1
		except:
			re_request_times += 1
			time.sleep(constants.NET_TEST_INTEVAL * 2)

	return json_res


def get_res_json_for_law_list(thread_id, s, payload):
	""" 实现异常处理 """
	re_request_times = 0
	r_status, json_res = False, ''
	while not r_status:
		if re_request_times == constants.MAX_RE_REQUEST_TIMES:
			raise requests.HTTPError('reach max_request_times')
		if re_request_times > 0:
			print('thread_id: {0}, re_request_times: {1}'.format(thread_id, re_request_times))
		time.sleep(constants.RE_REQ_TIME_SLEEP)
		try:
			res = s.get(constants.LAW_LIST_URL, params=payload, headers={'User-Agent': constants.ua.random}, timeout=constants.REQ_TIME_OUT)
			r_status, json_res = check_r_for_law(res)
			if not r_status:
				re_request_times += 1
		except:
			re_request_times += 1

	return json_res


def get_res_json_for_single_law(req_id, session, url):
	""" 实现异常检测 """
	re_request_times = 0
	r_status, json_res = False, ''
	while not r_status:
		if re_request_times == constants.MAX_RE_REQUEST_TIMES:
			raise requests.HTTPError('reach max_request_times')
		if re_request_times > 0:
			print('req_id: {0}, re_request_times: {1}'.format(req_id, re_request_times))
		time.sleep(constants.TIME_SLEEP_FOR_REQ)
		try:
			res = session.get(url, headers={'User-Agent': constants.ua.random}, timeout=constants.REQ_TIME_OUT)
			r_status, json_res = check_r_for_law(res)
			if not r_status:
				re_request_times += 1
		except:
			re_request_times += 1
			time.sleep(constants.NET_TEST_INTEVAL * 2)

	return json_res


if __name__ == '__main__':
	pass


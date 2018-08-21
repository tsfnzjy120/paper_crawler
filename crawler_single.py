# -*- coding:utf-8 -*-

from queue import Queue
from multiprocessing.dummy import Pool as ThreadPool
import time
import paper_crawler.constants as constants
import paper_crawler.tools as tools
import paper_crawler.store as store
import paper_crawler.spider as spider
import time


network_tester_switcher = True


def get_single_url(url_queue):

	with store.MysqlContext(4) as mc:
		print('get_single_url thread: I am starting to work...')
		cur = mc.db.cursor()
		start_single_id = store.get_next_single_id(mc.db)
		if start_single_id is None:
			print('get_single_url thread: all work has been done successfully')
			raise StopIteration
		else:
			start_single_id = start_single_id[0]
			print('get_single_url: get_next_single_id: {0}'.format(start_single_id))
			for single_id in range(start_single_id, constants.SINGLE_NUMS[constants.MACHINE_TAG] + 1):
				time.sleep(constants.TIME_SLEEP_FOR_GET_URL)
				sql = 'select jid from i_single_{0}_read where id={1}'.format(constants.MACHINE_TAG, single_id)
				cur.execute(sql)
				result = cur.fetchone()
				if result is None:
					continue
				else:
					# put a single_dict like {'single_id': 1, 'jid': '', 'url': ''}
					url_queue.put(
						{'single_id': single_id, 'jid': result[0], 'url': constants.SINGLE_URL + result[0]},
						timeout=constants.QUEUE_TIME_OUT
					)
					if constants.PRINT_GET_URL:
						print('get_single_url: produce a url: {0}/{1}  url_queue size: {2}'.format(
							single_id, constants.SINGLE_NUMS[constants.MACHINE_TAG], url_queue.qsize()
						))

	print('get_single_url thread: all work has been done successfully')


def req_single(req_id, url_queue, res_queue):

	session = spider.get_session()
	print('req_id: {0} is working...'.format(req_id))
	while True:
		single_dict = url_queue.get(timeout=constants.QUEUE_TIME_OUT)
		json_res = spider.get_res_json_for_single(req_id, session, single_dict['url'])
		# put a dict like {'single_id': 1, 'jid': '', 'json_res': json_res}
		res_queue.put(
			{'single_id': single_dict['single_id'], 'jid': single_dict['jid'], 'json_res': json_res},
			timeout=constants.QUEUE_TIME_OUT
		)
		if constants.PRINT_REQ:
			print('req id: {0}  produce a json_res {1}/{2}  url_queue size: {3}  res_queue size: {4}'.format(
				req_id, single_dict['single_id'], constants.SINGLE_NUMS[constants.MACHINE_TAG], url_queue.qsize(), res_queue.qsize()
			))


def store_single(store_id, res_queue):

	with store.MysqlContext(store_id) as mc:
		cur = mc.db.cursor()
		print('store_single: {0} is working...'.format(store_id))
		store_last_tag = 0
		while True:
			time.sleep(constants.TIME_SLEEP_FOR_STORE_SINGLE)
			single_dict = res_queue.get(timeout=constants.QUEUE_TIME_OUT)
			if single_dict['json_res']:
				store.write_single(store_id, single_dict)
			store.store_single_last(cur, single_dict['single_id'])
			store_last_tag += 1
			if constants.PRINT_STORE_SINGLE:
				print('store single: {0}  has stored single_id {1}  res_queue size: {2}'.format(
					store_id, single_dict['single_id'], res_queue.qsize()
				))
			if store_last_tag == constants.STORE_SINGLE_LAST_INTEVAL:
				mc.db.commit()
				store_last_tag = 0


def single_crawler():

	# 准备队列
	url_queue = Queue(constants.URL_QUEUE_LENGTH)
	res_queue = Queue(constants.RES_QUEUE_LENGTH)
	# 准备线程池
	pool_cap = 1 + constants.REQ_SINGLE_THREADS + constants.STORE_SINGLE_THREADS
	if network_tester_switcher:
		pool_cap += 1
	pool = ThreadPool(pool_cap)
	# 开始线程
	# 断线重连进程
	if network_tester_switcher:
		pool.apply_async(tools.network_tester)
		time.sleep(1)
	# 生成URL进程
	pool.apply_async(get_single_url, (url_queue, ))
	time.sleep(1)
	# request进程
	for req_id in range(0, constants.REQ_SINGLE_THREADS):
		pool.apply_async(req_single, (req_id, url_queue, res_queue))
		time.sleep(constants.TIME_SLEEP_FOR_REQ / constants.REQ_SINGLE_THREADS)
	# 存储文件进程
	for store_id in range(0, constants.STORE_SINGLE_THREADS):
		pool.apply_async(store_single, (store_id, res_queue))
		time.sleep(constants.TIME_SLEEP_FOR_STORE_SINGLE / constants.STORE_SINGLE_THREADS)
	# 阻塞，等待完成
	pool.close()
	pool.join()


def get_single_law_url(url_queue):

	with store.MysqlContext(4) as mc:
		print('get_single_law_url thread: I am starting to work...')
		cur = mc.db.cursor()
		start_single_law_id = store.get_next_single_law_id(mc.db)
		if start_single_law_id is None:
			print('get_single_law_url thread: all work has been done successfully')
			raise StopIteration
		else:
			start_single_law_id = start_single_law_id[0]
			print('get_single_law_url: get_next_single_law_id: {0}'.format(start_single_law_id))
			for single_law_id in range(start_single_law_id, constants.SINGLE_LAW_NUMS + 1):
				time.sleep(constants.TIME_SLEEP_FOR_GET_URL)
				sql = 'select lid from i_law_single_read where id={0}'.format(single_law_id)
				cur.execute(sql)
				result = cur.fetchone()
				if result is None:
					continue
				else:
					# put a single_dict like {'single_law_id': 1, 'lid': '', 'url': ''}
					url_queue.put(
						{'single_law_id': single_law_id, 'lid': result[0], 'url': constants.SINGLE_LAW_URL + result[0]},
						timeout=constants.QUEUE_TIME_OUT
					)
					if constants.PRINT_GET_URL:
						print('get_single_law_url: produce a url: {0}/{1}  url_queue size: {2}'.format(
							single_law_id, constants.SINGLE_LAW_NUMS, url_queue.qsize()
						))

	print('get_single_law_url thread: all work has been done successfully')


def req_single_law(req_id, url_queue, res_queue):

	session = spider.get_session()
	print('req_id: {0} is working...'.format(req_id))
	while True:
		single_law_dict = url_queue.get(timeout=constants.QUEUE_TIME_OUT)
		json_res = spider.get_res_json_for_single_law(req_id, session, single_law_dict['url'])
		# put a dict like {'single_law_id': 1, 'lid': '', 'json_res': json_res}
		res_queue.put(
			{'single_law_id': single_law_dict['single_law_id'], 'lid': single_law_dict['lid'], 'json_res': json_res},
			timeout=constants.QUEUE_TIME_OUT
		)
		if constants.PRINT_REQ:
			print('req id: {0}  produce a json_res {1}/{2}  url_queue size: {3}  res_queue size: {4}'.format(
				req_id, single_law_dict['single_id'], constants.SINGLE_LAW_NUMS, url_queue.qsize(), res_queue.qsize()
			))


def store_single_law(store_id, res_queue):

	with store.MysqlContext(store_id) as mc:
		cur = mc.db.cursor()
		print('store_single_law: {0} is working...'.format(store_id))
		store_last_tag = 0
		while True:
			time.sleep(constants.TIME_SLEEP_FOR_STORE_SINGLE)
			single_law_dict = res_queue.get(timeout=constants.QUEUE_TIME_OUT)
			if single_law_dict['json_res']:
				store.write_single_law(store_id, single_law_dict)
			store.store_single_law_last(cur, single_law_dict['single_law_id'])
			store_last_tag += 1
			if constants.PRINT_STORE_SINGLE:
				print('store single law: {0}  has stored single_law_id {1}/{2}  res_queue size: {3}'.format(
					store_id, single_law_dict['single_law_id'], constants.SINGLE_LAW_NUMS, res_queue.qsize()
				))
			if store_last_tag == constants.STORE_SINGLE_LAST_INTEVAL:
				mc.db.commit()
				store_last_tag = 0


def single_law_crawler():

	# 准备队列
	url_queue = Queue(constants.URL_QUEUE_LENGTH)
	res_queue = Queue(constants.RES_QUEUE_LENGTH)
	# 准备线程池
	pool_cap = 1 + constants.REQ_SINGLE_THREADS + constants.STORE_SINGLE_THREADS
	if network_tester_switcher:
		pool_cap += 1
	pool = ThreadPool(pool_cap)
	# 开始线程
	# 断线重连进程
	if network_tester_switcher:
		pool.apply_async(tools.network_tester)
		time.sleep(1)
	# 生成URL进程
	pool.apply_async(get_single_law_url, (url_queue, ))
	time.sleep(1)
	# request进程
	for req_id in range(0, constants.REQ_SINGLE_THREADS):
		pool.apply_async(req_single_law, (req_id, url_queue, res_queue))
		time.sleep(constants.TIME_SLEEP_FOR_REQ / constants.REQ_SINGLE_THREADS)
	# 存储文件进程
	for store_id in range(0, constants.STORE_SINGLE_THREADS):
		pool.apply_async(store_single_law, (store_id, res_queue))
		time.sleep(constants.TIME_SLEEP_FOR_STORE_SINGLE / constants.STORE_SINGLE_THREADS)
	# 阻塞，等待完成
	pool.close()
	pool.join()


if __name__ == '__main__':
	pass
	single_crawler()
	# single_law_crawler()

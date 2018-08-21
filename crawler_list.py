# -*- coding:utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
import time
import paper_crawler.constants as constants
import paper_crawler.tools as tools
import paper_crawler.spider as spider
import paper_crawler.parser as parser
import paper_crawler.store as store


network_tester_switcher = False


def single_list_crawler(thread_id):

	s = spider.get_session()
	resume_flag = 0  # 断点续传
	has_done_req = 0  # 进度显示
	with store.MysqlContext(thread_id) as mc:
		last_query_tag = store.get_list_last(thread_id, mc.db)
		if last_query_tag == 'initial0':
			resume_flag = 1
		for single_query in parser.parse_query_json(thread_id):
			for page_index in single_query['page_indexes']:
				if resume_flag == 0:
					has_done_req += 1
				if single_query['query_hashed'] + str(page_index) == last_query_tag:
					resume_flag = 1
					continue
				if resume_flag == 1:
					payload = {
						'order': '', 'pageIndex': str(page_index), 'pageSize': constants.PAGE_SIZE,
						'query': single_query['query']
					}
					json_res = spider.get_res_json_for_list(thread_id, s, payload)
					single_list = parser.parse_list_json(json_res)
					has_done_req = store.store_list(
						thread_id, mc.db, single_query['query'], single_query['query_hashed'],
						page_index, json_res, single_list, has_done_req
					)

	print('list crawler {0} done'.format(thread_id))

	return 0


def list_crawler():

	pool_size = len(constants.RUN_LIST_THREADS) + 1 if network_tester_switcher else len(constants.RUN_LIST_THREADS)
	pool = ThreadPool(pool_size)

	# 断线重连进程
	if network_tester_switcher:
		pool.apply_async(tools.network_tester)

	# 爬虫多进程
	for thread_id in constants.RUN_LIST_THREADS:
		time.sleep(0.1)
		pool.apply_async(single_list_crawler, (thread_id, ))

	pool.close()
	pool.join()

	return 0


def single_law_list_crawler(thread_id):

	s = spider.get_session()
	resume_flag = 0  # 断点续传
	has_done_req = 0  # 进度显示
	with store.MysqlContext(thread_id) as mc:
		last_query_tag = store.get_law_list_last(thread_id, mc.db)
		if last_query_tag == 'initial0':
			resume_flag = 1
		for single_query_law in parser.parse_query_law_json(thread_id):
			for page_index in single_query_law['page_indexes']:
				if resume_flag == 0:
					has_done_req += 1
				if single_query_law['query_hashed'] + str(page_index) == last_query_tag:
					resume_flag = 1
					continue
				if resume_flag == 1:
					payload = {
						'order': constants.LAW_PAYLOAD_ORDER, 'pageIndex': str(page_index),
						'pageSize': constants.PAGE_SIZE, 'query': single_query_law['query']
					}
					json_res = spider.get_res_json_for_law_list(thread_id, s, payload)
					single_law_list = parser.parse_law_list_json(json_res)
					has_done_req = store.store_law_list(
						thread_id, mc.db, single_query_law['query'], single_query_law['query_hashed'],
						page_index, json_res, single_law_list, has_done_req
					)

	print('law list crawler {0} done'.format(thread_id))

	return 0


def law_list_crawler():

	pool_size = len(constants.RUN_LIST_THREADS) + 1 if network_tester_switcher else len(constants.RUN_LIST_THREADS)
	pool = ThreadPool(pool_size)

	# 断线重连进程
	if network_tester_switcher:
		pool.apply_async(tools.network_tester)

	# 爬虫多进程
	for thread_id in constants.RUN_LIST_THREADS:
		time.sleep(0.1)
		pool.apply_async(single_law_list_crawler, (thread_id, ))

	pool.close()
	pool.join()

	return 0


if __name__ == '__main__':
	pass
	# list_crawler()
	# network_tester()
	# single_list_crawler(4)
	# single_law_list_crawler(0)
	# law_list_crawler()


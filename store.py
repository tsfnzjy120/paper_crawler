# -*- coding:utf-8 -*-

import os
import json
import pymysql
import paper_crawler.constants as constants


ENDURE_DUP_KEY = False


class MysqlContext:

	def __init__(self, thread_id):
		self.thread_id = thread_id  # -1 for root user

	def __enter__(self):
		self.db = pymysql.connect(
			host='127.0.0.1',
			port='3306',
			user=constants.MYSQL_USERS[self.thread_id]['user'],
			password=constants.MYSQL_USERS[self.thread_id]['password'],
			db='paper',
			charset='utf8'
		)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.db.close()


def store_list(thread_id, db, query, query_hashed, page_index, json_res, single_list, has_done_req):

	# 磁盘存储list.json
	file_name = '{0}_{1}.json'.format(query_hashed, page_index)
	file_path = os.path.join(constants.STORE_LIST_PATH, str(thread_id), file_name)
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(json_res, f, ensure_ascii=False, indent=4)

	# Mysql存储single_list
	cur = db.cursor()
	sql_a = "insert into i_single_{0}(jid, number, title, cause_type, cause, paper_type, court, date)".format(
		thread_id
	)
	sql_a += " values(%s, %s, %s, %s, %s, %s, %s, %s)"
	if ENDURE_DUP_KEY:
		try:
			cur.executemany(sql_a, single_list)
		except pymysql.err.IntegrityError:
			pass
	else:
		cur.executemany(sql_a, single_list)

	# Mysql断点续传
	sql_b = "update i_list_resume set last_query='{0}', last_query_hashed='{1}', page_index={2}".format(
		query, query_hashed, page_index
	)
	sql_b += " where thread_id={0}".format(thread_id)
	cur.execute(sql_b)

	# 保存Mysql
	db.commit()
	has_done_req += 1
	print('thread_id: {0}  has done: {1}/{2}  store list: {3} {4}'.format(
		thread_id, has_done_req, constants.LIST_NUMS[thread_id], query, page_index
	))

	return has_done_req


def get_list_last(thread_id, db):
	""" return query_hashed + page_index """

	cur = db.cursor()
	sql = 'select * from i_list_resume where thread_id={}'.format(thread_id)
	cur.execute(sql)
	result = cur.fetchone()
	print('thread: {0}  last list: {1} {2}'.format(thread_id, result[1], result[3]))

	return result[2] + str(result[3])


def get_next_single_id(db):
	""" 由于tag并不连续分布，会导致下次执行重复一部分http请求和写入json """
	cur = db.cursor()
	sql = 'select id from i_single_{0}_write where tag=0 limit 1'.format(constants.MACHINE_TAG)
	cur.execute(sql)

	return cur.fetchone()


def write_single(store_id, single_dict):

	file_name = single_dict['jid'] + '.json'
	file_path = os.path.join(constants.STORE_SINGLE_PATH, str(store_id), file_name)
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(single_dict['json_res'], f, ensure_ascii=False, indent=4)

	return 0


def store_single_last(cur, single_id):
	""" 由于线程执行进度不同，写入的tag很大概率不连续分布，会导致下次执行重复一部分http请求和写入json """
	sql = "update i_single_{0}_write set tag=1 where id={1}".format(
		constants.MACHINE_TAG, single_id
	)
	cur.execute(sql)

	return 0


def store_law_list(thread_id, db, query, query_hashed, page_index, json_res, single_list, has_done_req):

	# 磁盘存储law_list.json
	file_name = '{0}_{1}.json'.format(query_hashed, page_index)
	file_path = os.path.join(constants.STORE_LAW_LIST_PATH, str(thread_id), file_name)
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(json_res, f, ensure_ascii=False, indent=4)

	# Mysql存储single_law_list
	cur = db.cursor()
	sql_a = "insert into i_law_single_{0}(lid, title, authority, law_level, number, post_date, eff_date, status)".format(
		thread_id
	)
	sql_a += " values(%s, %s, %s, %s, %s, %s, %s, %s)"
	cur.executemany(sql_a, single_list)

	# Mysql断点续传
	sql_b = "update i_law_list_resume set last_query='{0}', last_query_hashed='{1}', page_index={2}".format(
		query, query_hashed, page_index
	)
	sql_b += " where thread_id={0}".format(thread_id)
	cur.execute(sql_b)

	# 保存Mysql
	db.commit()
	has_done_req += 1
	print('thread_id: {0}  has done: {1}/{2}  store law list: {3} {4}'.format(
		thread_id, has_done_req, constants.LAW_LIST_NUMS[thread_id], query, page_index
	))

	return has_done_req


def get_law_list_last(thread_id, db):
	""" return query_hashed + page_index """

	cur = db.cursor()
	sql = 'select * from i_law_list_resume where thread_id={}'.format(thread_id)
	cur.execute(sql)
	result = cur.fetchone()
	print('thread: {0}  last list: {1} {2}'.format(thread_id, result[1], result[3]))

	return result[2] + str(result[3])


def get_next_single_law_id(db):

	cur = db.cursor()
	sql = 'select id from i_law_single_write where tag=0 limit 1'
	cur.execute(sql)

	return cur.fetchone()


def write_single_law(store_id, single_law_dict):

	file_name = single_law_dict['lid'] + '.json'
	file_path = os.path.join(constants.STORE_SINGLE_LAW_PATH, str(store_id), file_name)
	single_law_dict['json_res']['data']['content'] = constants.html_tag.sub('', single_law_dict['json_res']['data']['content'])
	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(single_law_dict['json_res'], f, ensure_ascii=False, indent=4)

	return 0


def store_single_law_last(cur, single_law_id):

	sql = "update i_law_single_write set tag=1 where id={0}".format(single_law_id)
	cur.execute(sql)

	return 0


if __name__ == '__main__':
	pass



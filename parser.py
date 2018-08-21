# -*- coding: utf-8 -*-

import json
import codecs
import paper_crawler.constants as constants


def extract_cause(a):
	"""
	return format:
	{'pid': '1010010', 'id': '1010010020', 'name': '姓名权纠纷', 'level': 4, 'description': '姓名权纠纷'}
	"""

	single_cause = {'pid': a['pid'], 'id': a['id'], 'name': a['name'], 'level': a['level'], 'description': a['description']}

	return single_cause


def parse_cause_json():
	"""
	generate
	{'pid': '1010010', 'id': '1010010020', 'name': '姓名权纠纷', 'level': 4, 'description': '姓名权纠纷'}
	from causes.json
	"""

	with codecs.open(constants.CAUSES_JSON_PATH, 'r', encoding='utf-8-sig') as f:
		json_data = json.load(f)

	for a in json_data['result']:  # a level is 1
		if a['children'] is not None:
			for b in a['children']:  # b level is 2, below is same
				if b['children'] is not None:
					for c in b['children']:
						if c['children'] is not None:
							for d in c['children']:
								if d['children'] is not None:
									for e in d['children']:
										yield extract_cause(e)
								else:
									yield extract_cause(d)
						else:
							yield extract_cause(c)
				else:
					yield extract_cause(b)
		else:
			yield extract_cause(a)

	return 0


def parse_query_json(thread_id):
	"""
	thread_id: -1  qid: 0,1,2...
	thread_id: 0  qid: 0,5,10...
	thread_id: 1  qid: 1,6,11...
	thread_id: 2  qid: 2,7,12...
	thread_id: 3  qid: 3,8,13...
	thread_id: 4  qid: 4,9,14...
	single_query = {
		'qid': 0, 'query': '', 'query_hashed': '', 'num': 0, 'page_indexes': [1,2,3...]
	}
	"""
	with open(constants.QUERY_JSON_PATH, 'r', encoding='utf-8') as f:
		json_data = json.load(f)

	if thread_id == -1:
		for qid in range(0, json_data['queries']):
			yield json_data['detail'][qid]
	else:
		for qid in range(thread_id, json_data['queries'], 5):
			yield json_data['detail'][qid]


def extract_list_item(j):

	title = constants.html_tag.sub('', j['title'])
	single_item = (
		j['jid'], j['caseNumber'], title, j['caseType'],
		j['allTextCause'], j['judgementType'], j['courtName'], j['judgementDate'],
	)

	return single_item


def parse_list_json(json_res):
	""" return [(jid, number, title, cause_type, cause, paper_type, court, date), ...] """
	single_list = []
	for j in json_res['result']['judgements']:
		single_list.append(extract_list_item(j))

	return single_list


def extract_law_list_item(l):

	title = constants.html_tag.sub('', l['title'])
	single_law_item = (
		l['lid'], title, l['dispatch_authority'], l['eff_level'],
		l['document_number'], l['posting_date'], l['effective_date'], l['time_limited'],
	)

	return single_law_item


def parse_law_list_json(json_res):
	""" return [(lid, title, authority, law_level, number, post_date, eff_date, status), ...] """
	single_law_list = []
	for l in json_res['data']['lawRegus']:
		single_law_list.append(extract_law_list_item(l))

	return single_law_list


def parse_query_law_json(thread_id):
	"""
	thread_id: -1  qid: 1,2,3...
	thread_id: 0  qid: 1,6,11...
	thread_id: 1  qid: 2,7,12...
	thread_id: 2  qid: 3,8,13...
	thread_id: 3  qid: 4,9,14...
	thread_id: 4  qid: 5,10,15...
	single_law_query = {
		'qid': 0, 'query': '', 'query_hashed': '', 'num': 0, 'page_indexes': [1,2,3...]
	}
	"""
	with open(constants.QUERY_LAW_JSON_PATH, 'r', encoding='utf-8') as f:
		json_data = json.load(f)

	if thread_id == -1:
		for _qid in range(0, json_data['queries']):
			yield json_data['detail'][_qid]
	else:
		for _qid in range(thread_id, json_data['queries'], 5):
			yield json_data['detail'][_qid]


if __name__ == '__main__':
	pass


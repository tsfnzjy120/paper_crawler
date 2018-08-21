# -*- coding:utf-8 -*-
# by tsfnzjy120@ruc.edu.cn

import re
import fake_useragent

# file path
CAUSES_JSON_PATH = ''
QUERY_JSON_PATH = ''
STORE_LIST_PATH = ''
STORE_SINGLE_PATH = ''

# parameter
# http
LIST_URL = ''
PAGE_SIZE = ''

MACHINE_TAG = 'a'  # or 'b'
SINGLE_URL = ''
SINGLE_NUMS = {'a': 15964691, 'b': 15965834}

# thread control for crawler_single.py(include single_law_crawler())
URL_QUEUE_LENGTH, RES_QUEUE_LENGTH = 500, 500
REQ_SINGLE_THREADS, STORE_SINGLE_THREADS = 10, 4
QUEUE_TIME_OUT = 1800
STORE_SINGLE_LAST_INTEVAL = 1
TIME_SLEEP_FOR_GET_URL, TIME_SLEEP_FOR_REQ, TIME_SLEEP_FOR_STORE_SINGLE = 0.01, 0.07, 0.005
PRINT_GET_URL, PRINT_REQ, PRINT_STORE_SINGLE = False, False, True

TOKEN = ''
REQ_TIME_OUT = 10
NET_TEST_INTEVAL = 6
MAX_RE_REQUEST_TIMES = 12
MAX_RE_CONNECT_TIMES = 8
RE_REQ_TIME_SLEEP = 4
RUN_LIST_THREADS = (0, 1, 2, 3, 4)

# mysql
MYSQL_USERS = [
	{'user': 'user1', 'password': 'pass1'}, {'user': 'user2', 'password': 'pass2'},
	{'user': 'user3', 'password': 'pass3'}, {'user': 'user4', 'password': 'pass4'},
	{'user': 'user5', 'password': 'pass5'},
]

# others
YEARS = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
REGIONS = [
	'北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
	'辽宁省', '吉林省', '黑龙江省',
	'上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
	'河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省',
	'重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
	'陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区',
]
LIST_NUMS = [64480, 65102, 66065, 66696, 62904]
UA_PATH = 'fake_useragent_0.1.10.json'
ua = fake_useragent.UserAgent(path=UA_PATH)

# law
LAW_LEVELS = (
	'法律', '行政法规', '司法解释/文件', '部门规章/文件', '地方法规/文件',
	'地方司法文件', '行业规定', '团体规定', '军事法规'
)
LAW_STATUS = ('现行有效', '失效', '已被修改', '征求意见稿或草案', '尚未生效')
LAW_LIST_URL = ''
LAW_SINGLE_URL = ''
QUERY_LAW_JSON_PATH = 'query_law.json'
STORE_LAW_LIST_PATH = ''
LAW_PAYLOAD_ORDER = '发文日期'
LAW_LIST_NUMS = [3523, 3394, 2966, 2876, 3098]

SINGLE_LAW_NUMS = 1407617
SINGLE_LAW_URL = ''
STORE_SINGLE_LAW_PATH = ''

# regex
html_tag = re.compile(r'<[^>]+>', re.S)

# tools
TEST_URL = 'https://www.baidu.com'
CONNECT_RUC_URL = ''
RUC_ACCOUNTS_FILE_PATH = 'ruc_accounts.txt'  # 断网重连


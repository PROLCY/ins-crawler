from crawl_utils import *
from file_utils import write_exception_log

import os

from dotenv import load_dotenv

load_dotenv()
ACCOUNT_USERNAME = 'username'
ACCOUNT_PASSWORD = 'password'

configuration = {
    'USERNAME': ACCOUNT_USERNAME,
    'PASSWORD': ACCOUNT_PASSWORD,
    'HASHTAG': 'solotravel',
    'AMOUNT': 60,
    'ITERATION_CNT': 5,
    'TIME_DELAY_FROM': 30,
    'TIME_DELAY_TO': 180 
}

## 크롤링 횟수
max_crawl = 50 

if not os.path.isdir('image'):
    os.makedirs('image')

for crawl_cnt in range(max_crawl):
    try:
        crawl(configuration, crawl_cnt)

    except Exception as e:
        write_exception_log(crawl_cnt, e)
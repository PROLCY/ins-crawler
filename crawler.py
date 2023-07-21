from crawl_utils import *
from file_utils import write_exception_log

import os

def crawler(configuration):
    ## 크롤링 횟수
    max_crawl = 50 

    if not os.path.isdir('image'):
        os.makedirs('image')

    for crawl_cnt in range(max_crawl):
        try:
            crawl(configuration, crawl_cnt)

        except Exception as e:
            write_exception_log(crawl_cnt, e)
from file_utils import *

import datetime
import time

from instagrapi import Client

## 걸린 시간 출력하는 함수
def print_time_interval(time_start, time_end):
    sec = time_end - time_start
    run_time = datetime.timedelta(seconds=sec)
    print("Runtime(h:mm:ss): " + str(run_time))

## instagrapi의 client 설정 함수
def set_up_client(username, password):
    cl = Client()

    cl.delay_range = [1, 3] 
    cl.request_timeout = 20
    cl.login(username, password)
    
    return cl

## 무작위 시간 딜레이 발생 함수
def random_time_delay(time_delay_from, time_delay_to):
        time_delay = random.randrange(time_delay_from, time_delay_to)
        print("waiting " + str(time_delay) + " seconds...")
        time.sleep(time_delay)

## 크롤링 함수
def crawl(config, crawl_cnt):

    run_time_start = time.time()

    username, password = config['USERNAME'], config['PASSWORD']
    hashtag, amount = config['HASHTAG'], config['AMOUNT']
    iteration_cnt = config['ITERATION_CNT'] 
    time_delay_from, time_delay_to = config['TIME_DELAY_FROM'], config['TIME_DELAY_TO'] 

    last_cursor = ""
    pk_list = [] 
    photo_cnt_sum = 0

    cl = set_up_client(username, password)

    pk_list, last_cursor = read_pk_list_and_last_cursor()

    ## 크롤링 본체
    for request_cnt in range(iteration_cnt):
        
        print(str(request_cnt+1) + ". " + last_cursor + "\nstart download\n")
        
        photos, last_cursor = cl.hashtag_medias_v1_chunk(hashtag, amount, "top", last_cursor)
        pk_list, downloaded_photo_cnt = download_photos(photos, hashtag, pk_list, cl)

        print(pk_list)
        print(last_cursor)

        write_pk_list_and_last_cursor(pk_list, last_cursor, hashtag)

        photo_cnt_sum += downloaded_photo_cnt
        print(str(photo_cnt_sum) + " photos were taken until now\n")

        if(request_cnt != iteration_cnt - 1):
            random_time_delay(time_delay_from, time_delay_to)

    ## 80% 확률로 로그아웃
    r = random.randrange(1, 11)
    if(r >= 1 and r <= 8):
        cl.logout()
    
    print(str(crawl_cnt+1) + " Crawling Is Finished")
    run_time_end = time.time()
    print_time_interval(run_time_start, run_time_end)

    random_time_delay(300, 600)

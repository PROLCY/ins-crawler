from instagrapi import Client
from pathlib import Path
from dotenv import load_dotenv
import os
import csv
import time
import datetime
import random

load_dotenv()

ACCOUNT_USERNAME = os.environ.get('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')  

## 가져온 사진 다운로드하는 함수
def download_photos(photos, hashtag, pk_list):
    cnt = 0

    ## pk 가져오기
    with open('data.csv', "r") as csv_file:
        image_pk = int(csv_file.readlines()[-1].split(',')[0])+1
    csv_file = open('data.csv', 'a')
    csv_writer = csv.writer(csv_file)

    recent_pk_list = []

    for photo in photos:
        ## 사진이 없을 경우
        if(len(photo.resources) == 0):
            continue
        
        ## 사진이 아닐 경우
        if(photo.resources[0].media_type != 1):
            continue

        photo_url = photo.resources[0].thumbnail_url
        photo_pk = photo.resources[0].pk

        ## 이전에 탐색한 사진일 경우
        if(photo_pk in pk_list):
            continue

        print(cl.photo_download_by_url(photo_url, image_pk, folder=Path("./image")))
        recent_pk_list.append(photo_pk)

        ## data.csv에 저장(image_pk, 해쉬태그, 좋아요 수, 사진 올린 사람)
        csv_writer.writerow([image_pk, hashtag, photo.like_count, photo.user.username])
        cnt = cnt + 1
        image_pk = image_pk + 1
    print(str(cnt) + " photos were taken")
    csv_file.close()
    return recent_pk_list, cnt


full_iteration = 50 ## 크롤링 횟수

for crawl_cnt in range(full_iteration):
    try:
        ## 시간 측정 시작
        run_time_start = time.time()

        cl = Client()

        ## 요청 딜레이, 응답 대기 시간 설정
        cl.delay_range = [1, 3] 
        cl.request_timeout = 20

        ## 로그인
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        

        hashtag = "solotravel" ## 검색할 해쉬태그
        amount = 60 ## 가져올 사진의 개수(입력한 숫자의 반틈 정도 가져옴)
        iteration_cnt = 5 ## 사진 가져오기 반복 횟수
        time_delay_from = 30 ## 가져올 때마다 시간 딜레이 랜덤 범위 시작값
        time_delay_to = 180 ## 가져올 때마다 시간 딜레이 랜덤 범위 마지막값

        last_cursor = "" ## 가장 마지막에 사진을 탐색한 커서 위치
        pk_list = [] ## 직전에 탐색한 사진들의 pk 목록

        sum = 0 ## 사진 개수 합

        ## 이전 크롤링의 pk_list와 cursor 값 가져오기
        with open('prev.csv', 'r') as prev:
            text = prev.readline().split('.')
            pk_list = eval(text[0])
            last_cursor = text[1]

        ## 크롤링 본체
        for j in range(iteration_cnt):
            
            print(str(j+1) + ". " + last_cursor)
            print("start download\n")
            
            ## 사진 가져와서 다운로드 및 마지막 커서 저장
            photos, cursor = cl.hashtag_medias_v1_chunk(hashtag, amount, "top", last_cursor)
            pk_list, cnt = download_photos(photos, hashtag, pk_list)
            last_cursor = cursor

            print(pk_list)
            print(last_cursor)

            ## 인스타에서 요청 거절 당해도 다음 실행 때 자동으로 pk_list랑 cursor 가져올 수 있도록 prev.csv 파일에 적기
            with open('prev.csv', 'w') as prev:
                prev.write(str(pk_list) + "." + last_cursor + "." + hashtag)

            sum += cnt
            print(str(sum) + " photos were taken until now\n")

            if(j != iteration_cnt - 1):
                time_delay = random.randrange(time_delay_from, time_delay_to)
                print("waiting " + str(time_delay) + " seconds...")
                time.sleep(time_delay)

        print(str(crawl_cnt+1) + "/" + str(full_iteration) + " Crawling Is Finished")


        ## 시간 측정 및 결과 출력
        run_time_end = time.time()
        sec = run_time_end - run_time_start
        run_time = datetime.timedelta(seconds=sec)
        print("Runtime(h:mm:ss): " + str(run_time))

        ## 80% 확률로 로그아웃
        r = random.randrange(1, 11)
        if(r >= 1 and r <= 8):
            cl.logout()
        
        ## 크롤링 끝나고 시간 딜레이
        time_delay = random.randrange(300, 600)
        print("wait for " + str(time_delay) + " seconds...")
        time.sleep(time_delay)

    except Exception as e:

        time_delay = random.randrange(720, 960)
        log = str(crawl_cnt+1) + " iteration, (Exception) wait for " + str(time_delay) + " seconds..."
        print(log)

        ## Exception 발생 시간 및 이유 기록
        with open('exception_log.txt', 'a') as el:
            el.write("[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + log + " Error: " + str(e) + '\n')

        time.sleep(time_delay)
        continue
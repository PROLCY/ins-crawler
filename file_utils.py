import csv
from pathlib import Path
import time
import random
import os

IMAGE_DIR_PATH = "./image"

def make_file(filename):
    file = open(filename, 'w')
    file.close()

## data.csv에서 image_pk 가져오는 함수
def read_image_pk_from_data_csv():

    image_pk = 1

    if not os.path.isfile('data.csv'):
        make_file('data.csv')

    with open('data.csv', "r") as csv_file:
        data_lines = csv_file.readlines()
        if(len(data_lines) == 0):
            return image_pk
        image_pk = int(data_lines[-1].split(',')[0])+1

    return image_pk

## 사진 한 장 다운로드하는 함수
def download_photo(photo, image_pk, prev_pk_list, client):

    ## 사진이 없을 경우
    if(len(photo.resources) == 0):
        return
    
    ## 사진이 아닐 경우
    if(photo.resources[0].media_type != 1):
        return

    photo_url = photo.resources[0].thumbnail_url
    photo_pk = photo.resources[0].pk

    ## 이전에 탐색한 사진일 경우
    if(photo_pk in prev_pk_list):
        return

    print(client.photo_download_by_url(photo_url, image_pk, folder=Path(IMAGE_DIR_PATH)))

    return photo_pk

## data.csv에 data(image_pk, hashtag, 좋아요 수, 사진 올린 사람) 적는 함수
def write_data_in_data_csv(image_pk, hashtag, photo):
    csv_file = open('data.csv', 'a')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([image_pk, hashtag, photo.like_count, photo.user.username])
    csv_file.close()

## 가져온 사진 다운로드하는 함수
def download_photos(photos, hashtag, prev_pk_list, client):
    
    downloaded_photo_cnt = 0
    image_pk = read_image_pk_from_data_csv()
    recent_pk_list = []

    for photo in photos:
        ## 사진 다운로드
        photo_pk = download_photo(photo, image_pk, prev_pk_list, client)
        if(photo_pk == None):
            continue

        recent_pk_list.append(photo_pk)
        write_data_in_data_csv(image_pk, hashtag, photo)

        downloaded_photo_cnt = downloaded_photo_cnt + 1
        image_pk = image_pk + 1

    print(str(downloaded_photo_cnt) + " photos were taken")
    return recent_pk_list, downloaded_photo_cnt

## prev.csv에서 pk_list와 last_cursor 읽는 함수
def read_pk_list_and_last_cursor():
    if not os.path.isfile('prev.csv'):
        make_file('prev.csv')

    with open('prev.csv', 'r') as prev:
        splited_row = prev.readline().split('.')
        if(splited_row == ['']):
            return '', ''
        pk_list = eval(splited_row[0])
        last_cursor = splited_row[1]
    return pk_list, last_cursor

## prev.csv에 pk_list와 last_cursor 쓰는 함수
def write_pk_list_and_last_cursor(pk_list, last_cursor, hashtag):
    with open('prev.csv', 'w') as prev:
        prev.write(str(pk_list) + "." + last_cursor + "." + hashtag)

## exception 발생 시 로그 적는 함수
def write_exception_log(crawl_cnt, exception):
    time_delay = random.randrange(720, 960)
    log = str(crawl_cnt+1) + " iteration, (Exception) wait for " + str(time_delay) + " seconds..."
    print(log)

    with open('exception_log.txt', 'a') as el:
        el.write("[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + log + " Error: " + str(exception) + '\n')
    time.sleep(time_delay)
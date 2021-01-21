from init_photo_service import service
from Uploading_Photo_to_Instagram import *
from pandas import DataFrame
from time import sleep
from random import choice
import requests
import os
from json import load
import datetime
from shutil import copy

# ------------------------------------------------------

Base_URL_list = []
x = datetime.datetime.now()
cur = x.strftime('%Y-%m-%d')

file_obj = open(r'possible_urls.txt', 'a+')
with open('./userinfo.json') as userinfo:
    userdict = load(userinfo)
user = userdict['username']
password = userdict['password']


def download_file(url: str, destination_folder: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)


log(user, password)  #log in to Instagram

response = service.mediaItems().list(pageSize=100).execute()
list_medias = response.get("mediaItems")
nextPageToken = response.get('nextPageToken')

for i in range(2):
    response = service.mediaItems().list(
        pageSize=100,
        pageToken=nextPageToken
    ).execute()
    list_medias.extend(response.get("mediaItems"))
    nextPageToken = response.get("nextPageToken")
df_media_items = DataFrame(list_medias)  #around 200 Items (100 * 2)
feature3 = [d.get('creationTime') for d in df_media_items.mediaMetadata][0][:10]  #last date of last taken photo
meta = (df_media_items[['id', 'mediaMetadata', 'baseUrl']])
file_obj.write(f'-------{feature3}-------\n')
for index, row in meta.iterrows():
    dates = (row['mediaMetadata']['creationTime'][:10])
    if dates == feature3:
        Base_URL_list.append(row['baseUrl'])
if cur == feature3:
    for j in Base_URL_list:
        j = j + '\n'
        file_obj.write(j)
    holy_image = choice(Base_URL_list)
    holy_image = holy_image + "=w1080-h1080-c"  #size of Image so ratio is 1:1

    download_file(holy_image, r'.\ImageBin', "yolo.jpg")
    cap = f"This is a random photo from @aryan_401 's Google Photo\nThis photo was shot on: {feature3} GMT\nThis photo had a 1 in {len(Base_URL_list)} Chance "
    upload_to_instagram(r'.\ImageBin\yolo.jpg', cap)
    os.remove(r'.\ImageBin\yolo.jpg.REMOVE_ME')

else:
    copy(r'C:\Users\defaultuser100000\Google Meets Intagram\yolo1.jpg', r'C:\Users\defaultuser100000\Google Meets Intagram\ImageBin')
    sleep(60)
    file_obj.write('.....NO IMAGE.....\n')
    upload_to_instagram(r'.\ImageBin\yolo1.jpg', f'If you see this image that means that no new pictures were taken on {cur}')
    os.remove(r'.\ImageBin\yolo1.jpg.REMOVE_ME')
quit()

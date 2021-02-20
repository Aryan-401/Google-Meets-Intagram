from Uploading_Photo_to_Instagram import *
from pandas import DataFrame
from time import sleep
from random import choice
import requests
import os
import traceback
from json import load
import datetime
from shutil import copy


Base_URL_list = []
x = datetime.datetime.now()
cur = x.strftime('%Y-%m-%d')
file_obj = open(r'possible_urls.txt', 'a+')

with open('./userinfo.json') as userinfo:
    userdict = load(userinfo)
user = userdict['username']
password = userdict['password']

insult = ['super ugly', 'an absolute dumbass', 'as useless as a car with 3 wheels',                              #Insults can be disabled
          'single af', ' a simp', 'Hella Emo', 'so cute', 'a Weirdo', 'Lou', 'an asshole', 'dumb', 'wholesome',  #by changing up some code on
          'stupid', 'awesome', 'a show-off-person', 'an asshole', 'butterfingers', 'a third wheel to everyone',  #line 84
          'retarded', 'a tiktok star', 'fat']

loc_no_pic_taken_og = r''  #Whole path of 'No picture taken on this day' image
loc_whole_path_Imagebin = r''  #Whole Path to ImageBin Dir
loc_no_pic_taken_Imagebin = r''  #Path of 'No picture taken on this day' inside ImageBin
loc_error_image_og = r''  #Whole Path of 'Error' image
loc_error_image_Imagebin = r''  #Path of 'Error' inside ImageBin


def download_file(url: str, destination_folder: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)


log(user, password)  #log in to Instagram

try:
    from init_photo_service import service
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
    for index, row in meta.iterrows():
        dates = (row['mediaMetadata']['creationTime'][:10])
        if dates == feature3:
            Base_URL_list.append(row['baseUrl'])
    if cur == feature3:
        file_obj.write(f'-------{feature3}-------\n')
        for j in Base_URL_list:
            j = j + '\n'
            file_obj.write(j)
        holy_image = choice(Base_URL_list)
        holy_image = holy_image + "=w1080-h1080-c"  #size of Image so ratio is 1:1

        download_file(holy_image, r'.\ImageBin', "yolo.jpg")
        cap = f"This is a random photo from @{user}'s Google Photo\nThis photo was shot on: {feature3} GMT\nThis photo had a 1 in {len(Base_URL_list)} Chance "
        upload_to_instagram(r'.\ImageBin\yolo.jpg', cap)
        if os.path.isfile(r'.\ImageBin\yolo.jpg.REMOVE_ME'):
            os.remove(r'.\ImageBin\yolo.jpg.REMOVE_ME')

    else:
        file_obj.write(f'-------{cur}-------\n')
        copy(loc_no_pic_taken_og, loc_whole_path_Imagebin)
        sleep(20)
        file_obj.write('.....NO IMAGE.....\n')
        upload_to_instagram(loc_no_pic_taken_Imagebin, f'No new pictures were taken on {cur} \n @{user} is {choice(insult)} \n\n\n[User Submitted Entries]')
        if os.path.isfile(loc_no_pic_taken_Imagebin + '.REMOVE_ME'):
            os.remove(loc_no_pic_taken_Imagebin + 'REMOVE_ME')
except Exception:
    try:
        caps = traceback.format_exc().split("\n")[-3]
        file_obj.write(f'-------{cur}-------\n')
        copy(loc_error_image_og,
             loc_whole_path_Imagebin)
        sleep(10)
        file_obj.write(f'..... {traceback.format_exc()} .....\n')
        upload_to_instagram(loc_error_image_Imagebin,
                            f'{caps} Occured on {cur} @{user} is a total Coding noob \nHopefully it gets fixed by tomorrow')
        sleep(10)
        if os.path.isfile(loc_error_image_Imagebin + ".REMOVE_ME"):
            os.remove(loc_error_image_Imagebin)
    except IndexError:
        copy(loc_error_image_og,
             loc_whole_path_Imagebin)
        file_obj.write(f'..... {traceback.format_exc()} .....\n')
        sleep(10)
        upload_to_instagram(loc_error_image_Imagebin,
                            f"Something Happened, I'm not sure what happened cuz this part of the code was never supposed to run YOLO")
        sleep(10)
        if os.path.isfile(loc_error_image_Imagebin + '.REMOVE_ME'):
            os.remove(loc_error_image_Imagebin + '.REMOVE_ME')

file_obj.close()
quit()

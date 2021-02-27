from Uploading_Photo_to_Instagram import *
from pandas import DataFrame
from random import choice
import requests
import os
import traceback
from json import load
import datetime
from shutil import copy
from datetime import date
import calendar

# -------- ^ Initiations || v META CODE --------
Base_URL_list = []
Product_URL_List = []

cur = datetime.datetime.now().strftime('%Y-%m-%d')
today = calendar.day_name[date.today().weekday()]

audit_log = open(r'audit_log.txt', 'a+')
picture_log = open(r'picture_log.txt', 'a+')
with open('./userinfo.json') as userinfo:
    user_dictionary = load(userinfo)
user = user_dictionary['username']
password = user_dictionary['password']
other_user = user_dictionary['other_user']
if len(other_user) <= 2:
    other_user = user

# -------- IMPORTANT PATHS --------
loc_no_pic_taken_og = r''  # Whole path of 'No picture taken on this day' image
loc_whole_path_image_bin = r''  # Whole Path to ImageBin Dir
loc_no_pic_taken_image_bin = r''  # Path of 'No picture taken on this day' inside ImageBin
loc_error_image_og = r''  # Whole Path of 'Error' image
loc_error_image_image_bin = r''  # Path of 'Error' inside ImageBin

# -------- HASHTAGS --------
base_hashtags = "#coding #python #automation #instabot #instapy #google #photos #github #instagram #pycharm #f4f #programming #project #pandas #datascience #💻 "
daily_hashtags = {'Monday': '#MondayMemories #MotivationMonday #MondayMotivation #MondayBlues ',
                  'Tuesday': '#TastingTuesday #TechTuesday #TipTuesday #TopicTuesday #TransformationTuesday ',
                  'Wednesday': '#HumpDay #WayBackWednesday #WonderfulWednesday #WellnessWednesday #WednesdayWisdom ',
                  'Thursday': '#ThankfulThursday #ThirstyThursday #ThrowbackThursday #TBT #ThursdayThoughts ',
                  'Friday': '#FearlessFriday #FlashBackFriday #FridayFun #Friyay #FridayVibes ',
                  'Saturday': '#SaturdaySwag #SaturdayStyle #SalesSaturday #SelfieSaturday #ShoutoutSaturday ',
                  'Sunday': '#StartupSunday #SundaySweat #SelfieSunday #SundayFunday #Weekend '}
no_photo_hashtags = "#nophoto #serious #ugly #me #bored "
error_photo_hashtags = '#error #mistake #fix #stackoverflow #oops #🔧'


def download_file(url: str, destination_folder: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)


log(user, password)  # log in to Instagram

# -------- START OF PROGRAM --------
try:
    from init_photo_service import service  # Initating Google Photos Module last so that error management can happen

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
    df_media_items = DataFrame(list_medias)  # around 200 Items (100 * 2)

    feature3 = [d.get('creationTime') for d in df_media_items.mediaMetadata][0][:10]  # last date of last taken photo
    meta = (df_media_items[['id', 'mediaMetadata', 'baseUrl', 'productUrl']])
    for index, row in meta.iterrows():
        dates = (row['mediaMetadata']['creationTime'][:10])
        if dates == feature3:
            Base_URL_list.append(row['baseUrl'])
            Product_URL_List.append(row['productUrl'])
    if cur == feature3:
        holy_image = choice(Base_URL_list)
        new_meta = meta.where(meta['baseUrl'] == holy_image).sort_values(by='productUrl')
        holy_productUrl = new_meta.iloc[0].productUrl
        holy_image = holy_image + "=w1080-h1080-c"  # size of Image so ratio is 1:1
        audit_log.write(
            f'-------{feature3}-------\nUploaded Picture from Google Photos at {datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M:%S")} ({holy_productUrl})\n')
        picture_log.write(f'-------{feature3}-------\n')
        for j in Product_URL_List:
            picture_log.write(f'{j}\n')

        download_file(holy_image, r'.\ImageBin', "yolo.jpg")
        cap = f"""Hi! If this is the first time you are seeing these types of posts, read my bio for more info
            This is an automatic account which uploads a picture from @{other_user} 's Google Photos!


            This photo was shot on: {feature3} GMT and had a 1 in {len(Base_URL_list)} Chance of being uploaded
            ---- HASHTAGS ----
            {base_hashtags}{daily_hashtags[today]}"""
        upload_to_instagram(r'.\ImageBin\yolo.jpg', cap)
        if os.path.isfile(r'.\ImageBin\yolo.jpg.REMOVE_ME'):
            os.remove(r'.\ImageBin\yolo.jpg.REMOVE_ME')

    else:
        audit_log.write(f'-------{cur}-------\n')
        picture_log.write(f'-------{cur}-------\n')
        copy(loc_no_pic_taken_og, loc_whole_path_image_bin)

        audit_log.write(
            f'Uploaded yolo1.jpg (No new photos were taken today) [{datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M:%S")}]\n')
        picture_log.write(f'No Pictures were uploaded today')
        upload_to_instagram(loc_no_pic_taken_image_bin, f"""Hi! If this is the first time you are seeing these types of posts, read my bio for more info 
                                                        No new pictures were taken on {cur}
                                                        Cheers!
                                                        ---- HASHTAGS ----
                                                        {base_hashtags}{daily_hashtags[today]}{no_photo_hashtags}""")
        if os.path.isfile(loc_no_pic_taken_image_bin + '.REMOVE_ME'):
            os.remove(loc_no_pic_taken_image_bin + '.REMOVE_ME')


except Exception:
    try:
        caps = traceback.format_exc().split("\n")[-3]
        audit_log.write(f'-------{cur}-------\n')
        picture_log.write(f'-------{cur}-------\n')
        copy(loc_error_image_og,
             loc_whole_path_image_bin)

        audit_log.write(f' {traceback.format_exc()} \n')
        picture_log.write('An error occured today, check audit_logs.txt for more info')
        upload_to_instagram(loc_error_image_image_bin,
                            f"""Hi! If this is the first time you are seeing these types of posts, read my bio for more info

                            YAY!!! {caps} Occurred on {cur} @{other_user} really needs to redo his code 
                            Hopefully it gets fixed by tomorrow
                            ---- HASHTAGS ----
                            {base_hashtags}{daily_hashtags[today]}{error_photo_hashtags}""")

        if os.path.isfile(loc_error_image_image_bin + '.REMOVE_ME'):
            os.remove(loc_error_image_image_bin + '.REMOVE_ME')
    except IndexError:
        copy(loc_error_image_og,
             loc_whole_path_image_bin)
        audit_log.write(f'..... {traceback.format_exc()} .....\n')

        upload_to_instagram(loc_error_image_image_bin,
                            f"""Hi! If this is the first time you are seeing these types of posts, read my bio for more info

                            An Index error happened... This wasn't supposed to happen @{other_user} you kinda messed up
                            ---- HASHTAGS ----
                            {base_hashtags}{daily_hashtags[today]}{error_photo_hashtags}""")

        if os.path.isfile(loc_error_image_image_bin + '.REMOVE_ME'):
            os.remove(loc_error_image_image_bin + '.REMOVE_ME')
picture_log.close()
audit_log.close()
quit()

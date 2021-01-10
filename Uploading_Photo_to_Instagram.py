from instabot import Bot
import datetime
bot = Bot()
def log(uname: str, pword: str):
    bot.login(username=uname, password=pword)
def upload_to_instagram(image: str,capti: str):
    bot.upload_photo(image, caption=capti)
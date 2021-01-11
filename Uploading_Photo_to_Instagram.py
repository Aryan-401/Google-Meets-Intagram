from instabot import Bot
bot = Bot()


def log(uname: str, password: str):
    bot.login(username=uname, password=password)


def upload_to_instagram(image: str, caption: str):
    bot.upload_photo(image, caption=caption)

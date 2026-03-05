# -----------------------------------------------
# 🔸 khitmusic Project
# 🔹 Developed & Maintained by: Stark (https://github.com/khithlainhtet)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by khithlainhtet# -----------------------------------------------
from khitmusic.core.bot import SANYA
from khitmusic.core.dir import dirr
from khitmusic.core.git import git
from khitmusic.core.userbot import Userbot
from khitmusic.misc import dbb, heroku
from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = SANYA()
userbot = Userbot()
api = SafoneAPI()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

APP = "Panda_king_HTbot"  # connect music api key "Dont change it"

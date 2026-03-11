import asyncio
import aiohttp
import random
import time
from pyrogram import filters
from pyrogram.enums import ChatType, ChatAction
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import MessageNotModified
from youtubesearchpython.__future__ import VideosSearch
import config
from khitmusic import app
from khitmusic.misc import _boot_
from khitmusic.plugins.sudo.sudoers import sudoers_list
from khitmusic.utils import bot_sys_stats
from khitmusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from khitmusic.utils.decorators.language import LanguageStart
from khitmusic.utils.formatters import get_readable_time
from khitmusic.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string
from config import BANNED_USERS

# Assets 
STICKER = [
    "CAACAgUAAxkBAAIgT2mwz8HcjYCVwtsDNf4gYRgFNtNVAAKzFwACGbigVSI-1-HziJBxHgQ",
    "CAACAgUAAxkBAAIgUmmwz9e2qCZpOEKEhAh-weLRU2joAALqGQACWZuhVcUGAq-mjrZ3HgQ",
    "CAACAgUAAxkBAAIgVWmwz-EMG84rIbbEzBPDvAy9dDAZAALgIAACirShVR_C-W73Og5YHgQ",
    "CAACAgUAAxkBAAIgWGmwz-9QsQnLOtXe7nnzxQ8FtfHxAAJPGQAC7QygVUPT1Ti2P22ZHgQ",
    "CAACAgUAAxkBAAIgW2mwz_shhAKFmAqkSJsAAakUF69vmgACzhkAAvmSoVWClmzB9TDz6R4E",
    "CAACAgUAAxkBAAIgYGmw0Akd2Lxe0oqXaj4G6_msDr12AAKWHAACxiegVfUf9hwPjXqgHgQ",
    "CAACAgUAAxkBAAIgY2mw0BwHN_TgdabNkT9_ld_D1h4EAAJ4GQACMQABoFVDxuEcxR1CQh4E",
    "CAACAgUAAxkBAAIgZmmw0Cl7waUBN-nHS7nvJCyKU7hUAAIZGwAC1TmgVSBQbkNGcGBSHgQ",
    "CAACAgUAAxkBAAIgaWmw0DQZRj1yPlrpMHOjQbsJwZSgAALgGQACfA2YVRl1rlBfNwT5HgQ",
    "CAACAgUAAxkBAAIgbGmw0FOivFrv8TcywwlFB2cygbbpAAJsHQACRvWgVVc0bfwhNM8dHgQ",
]

EMOJIOS = ["❤️", "😁", "👀", "⚡️", "🕊", "❤️‍🔥", "💅", "👻",]

STARK_IMG = [
    "https://files.catbox.moe/lsbtud.jpg",
    "https://files.catbox.moe/stqxy1.jpg",
    "https://files.catbox.moe/wz4ndo.jpg",
    "https://files.catbox.moe/02yas7.jpg",
    "https://files.catbox.moe/9qi4ot.jpg",
    "https://files.catbox.moe/e813zc.jpg",
    "https://files.catbox.moe/cdc5cz.jpg",
    "https://files.catbox.moe/83zj85.jpg"
]

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # 1. Reaction to the User's message
    try:
        await message.react(random.choice(EMOJIOS))
    except:
        pass

    # 2. Set Bot Status to Typing
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    # 4. Layer 2: Separate "Starting" Message
    _text = "𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑴𝒀 𝑭𝑹𝑰𝑬𝑵𝑫𝑺"
    starting_msg = await message.reply_text(f"**__{_text[0]}__**")
    for i in range(1, len(_text)):
        try:
            await asyncio.sleep(0.1)
            await starting_msg.edit_text(f"**__{_text[:i+1]}__**")
        except Exception:
            pass
    await starting_msg.delete()

    # 5. Send Random Sticker
    umm = await message.reply_sticker(sticker=random.choice(STICKER))
    await asyncio.sleep(0.4)
    await umm.delete()

    # 6. Main Start Logic (Deep Links)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            await message.reply_photo(
                random.choice(STARK_IMG),
                caption=_['help_1'].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"❍ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
        elif name.startswith("inf"):
            query = name.replace("info_", "", 1)
            results = VideosSearch(query, limit=1)

            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(title, duration, views, published, channellink, channel, app.mention)
            key = InlineKeyboardMarkup([[
                InlineKeyboardButton(text=_["S_B_8"], url=link),
                InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
            ]])
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
    else:
        # Standard Main Start Panel
        out = private_panel(_)
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        
        await message.reply_photo(
            random.choice(STARK_IMG),
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"❍ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(STARK_IMG),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(app.mention, f"https://t.me/{app.username}?start=sudolist", config.SUPPORT_CHAT),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    random.choice(STARK_IMG),
                    caption=_["start_3"].format(message.from_user.mention, app.mention, message.chat.title, app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)

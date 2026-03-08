from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from khitmusic import app
from config import MUST_JOIN

#--------------------------
#MUST_JOIN = "myanmar_music_Bot2027" 
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://files.catbox.moe/ffsk8y.jpg", caption=f"๏ ကျွန်ုပ်တို့၏ Database အရ သင်သည်  [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ကို မjoin ရသေးပါ!, Bot ကို ဆက်လက်အသုံးပြုနိုင်ရန် [๏sᴜᴘᴘᴏʀᴛ๏]({link})ကို joinပေးပြီးမှ /start ကို ပြန်နှိပ်ပေးပါ။  ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("๏Jᴏɪɴ๏", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛ ๏: {MUST_JOIN} !")

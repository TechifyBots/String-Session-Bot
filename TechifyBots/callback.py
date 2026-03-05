import traceback
import random
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from Script import text
from config import ADMIN, PICS
from .main import generate_session, ask_ques, buttons_ques

@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    data=query.data
    try:
        if data=="start":
            await query.message.edit_media(
                InputMediaPhoto(
                    media=random.choice(PICS),
                    caption=text.START.format(query.from_user.mention)
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ℹ️ 𝖠𝖻𝗈𝗎𝗍',callback_data='about'),
                     InlineKeyboardButton('📚 𝖧𝖾𝗅𝗉',callback_data='help')],
                    [InlineKeyboardButton('⚡ 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖲𝗍𝗋𝗂𝗇𝗀 𝖲𝖾𝗌𝗌𝗂𝗈𝗇',callback_data='generate')]
                ])
            )

        elif data=="help":
            await query.message.edit_media(
                InputMediaPhoto(
                    media=random.choice(PICS),
                    caption=text.HELP.format(query.from_user.mention)
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌',url='https://telegram.me/Techifybots'),
                     InlineKeyboardButton('🛟 𝖲𝗎𝗉𝗉𝗈𝗋𝗍',url='https://telegram.me/TechifySupport')],
                    [InlineKeyboardButton("↩️ 𝖡𝖺𝖼𝗄",callback_data="start")]
                ])
            )

        elif data=="about":
            await query.message.edit_media(
                InputMediaPhoto(
                    media=random.choice(PICS),
                    caption=text.ABOUT
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('💻 𝖱𝖾𝗉𝗈',url='https://github.com/TechifyBots/String-Session-Bot'),
                     InlineKeyboardButton('👨‍💻 𝖮𝗐𝗇𝖾𝗋',user_id=int(ADMIN))],
                    [InlineKeyboardButton("↩️ 𝖡𝖺𝖼𝗄",callback_data="start")]
                ])
            )

        elif data == "close":
            await query.message.delete()
            await query.answer()

        elif data == "generate":
            await query.answer()
            await query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

        elif data in ["pyrogram", "pyrogram_bot", "telethon", "telethon_bot"]:
            await query.answer()
            if data == "pyrogram":
                await generate_session(client, query.message)
            elif data == "pyrogram_bot":
                await query.answer("» ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
                await generate_session(client, query.message, is_bot=True)
            elif data == "telethon":
                await generate_session(client, query.message, telethon=True)
            elif data == "telethon_bot":
                await generate_session(client, query.message, telethon=True, is_bot=True)

    except Exception as e:
        print(traceback.format_exc())
        await query.message.reply(f"**Error -** `{e}`")

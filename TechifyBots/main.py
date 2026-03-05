from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ACTIVE_USERS = set()

ask_ques = "<blockquote><b>𝖢𝗁𝗈𝗈𝗌𝖾 𝖳𝗁𝖾 𝖲𝗍𝗋𝗂𝗇𝗀 𝖳𝗒𝗉𝖾</b></blockquote>"

buttons_ques = [
    [
        InlineKeyboardButton("𝖳𝖾𝗅𝖾𝗍𝗁𝗈𝗇", callback_data="telethon"),
        InlineKeyboardButton("𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆", callback_data="pyrogram")
    ], [
        InlineKeyboardButton("𝖳𝖾𝗅𝖾𝗍𝗁𝗈𝗇 𝖡𝗈𝗍", callback_data="telethon_bot"),
        InlineKeyboardButton("𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 𝖡𝗈𝗍", callback_data="pyrogram_bot")
    ], [
        InlineKeyboardButton("✗ 𝖢𝗅𝗈𝗌𝖾 ✗", callback_data="close")
    ]
]

gen_button = [[InlineKeyboardButton(text="🔄 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖲𝗍𝗋𝗂𝗇𝗀", callback_data="generate")]]

@Client.on_message(filters.private & ~filters.forwarded & filters.command("gen"))
async def main(_, msg):
    sent = await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if msg.from_user.id in ACTIVE_USERS:
        r = await msg.reply("⚠️ 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖱𝗎𝗇𝗇𝗂𝗇𝗀.\n\n𝖳𝗒𝗉𝖾 /cancel 𝗈𝗋 𝖶𝖺𝗂𝗍.")
        return await auto_delete(msg, r)
    ACTIVE_USERS.add(msg.from_user.id)

    if telethon:
        ty = "𝖳𝖾𝗅𝖾𝗍𝗁𝗈𝗇"
    else:
        ty = "𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆"
    if is_bot:
        ty += " 𝖡𝗈𝗍"
    start_msg = await msg.reply(f"⏳ 𝖲𝗍𝖺𝗋𝗍𝗂𝗇𝗀 {ty} 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝗈𝗋...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "𝖲𝖾𝗇𝖽 𝗒𝗈𝗎𝗋 <b>API_ID</b>", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            r = await api_id_msg.reply("❌ API_ID 𝗆𝗎𝗌𝗍 𝖻𝖾 𝖺 𝗇𝗎𝗆𝖻𝖾𝗋.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return await auto_delete(api_id_msg, r)
        api_hash_msg = await bot.ask(user_id, "𝖲𝖾𝗇𝖽 𝗒𝗈𝗎𝗋 <b>API_HASH</b>", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "📱 𝖲𝖾𝗇𝖽 𝗒𝗈𝗎𝗋 <b>Phone Number</b> 𝗐𝗂𝗍𝗁 𝖢𝗈𝗎𝗇𝗍𝗋𝗒 𝖢𝗈𝖽𝖾\nExample: <code>+910000000000</code>"
    else:
        t = "🤖 𝖲𝖾𝗇𝖽 𝗒𝗈𝗎𝗋 <b>Bot Token</b>"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("📩 𝖲𝖾𝗇𝖽𝗂𝗇𝗀 OTP...")
    else:
        await msg.reply("🔐 𝖫𝗈𝗀𝗀𝗂𝗇𝗀 𝗂𝗇 𝗏𝗂𝖺 𝖡𝗈𝗍 𝖳𝗈𝗄𝖾𝗇...")

    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        r = await msg.reply("❌ 𝖨𝗇𝗏𝖺𝗅𝗂𝖽 API_ID 𝗈𝗋 API_HASH.", reply_markup=InlineKeyboardMarkup(gen_button))
        return await auto_delete(msg, r)
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        r = await msg.reply("❌ 𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖯𝗁𝗈𝗇𝖾 𝖭𝗎𝗆𝖻𝖾𝗋.", reply_markup=InlineKeyboardMarkup(gen_button))
        return await auto_delete(msg, r)
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(
                user_id,
                "🔑 𝖲𝖾𝗇𝖽 OTP (Example: 1 2 3 4 5)",
                filters=filters.text,
                timeout=600
            )
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        r = await msg.reply("⏰ 𝖳𝗂𝗆𝖾 𝖫𝗂𝗆𝗂𝗍 𝖤𝗑𝗉𝗂𝗋𝖾𝖽.", reply_markup=InlineKeyboardMarkup(gen_button))
        return await auto_delete(msg, r)

    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            r = await msg.reply("❌ 𝖶𝗋𝗈𝗇𝗀 OTP.", reply_markup=InlineKeyboardMarkup(gen_button))
            return await auto_delete(msg, r)

        except (PhoneCodeExpired, PhoneCodeExpiredError):
            r = await msg.reply("❌ OTP 𝖤𝗑𝗉𝗂𝗋𝖾𝖽.", reply_markup=InlineKeyboardMarkup(gen_button))
            return await auto_delete(msg, r)
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(
                    user_id,
                    "🔒 𝖤𝗇𝗍𝖾𝗋 𝖳𝗐𝗈-𝖲𝗍𝖾𝗉 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖯𝖺𝗌𝗌𝗐𝗈𝗋𝖽",
                    filters=filters.text,
                    timeout=300
                )
            except TimeoutError:
                r = await msg.reply("⏰ 𝖳𝗂𝗆𝖾 𝖫𝗂𝗆𝗂𝗍 𝖤𝗑𝗉𝗂𝗋𝖾𝖽.", reply_markup=InlineKeyboardMarkup(gen_button))
                return await auto_delete(msg, r)
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
            except (PasswordHashInvalid, PasswordHashInvalidError):
                r = await two_step_msg.reply("❌ 𝖶𝗋𝗈𝗇𝗀 𝖯𝖺𝗌𝗌𝗐𝗈𝗋𝖽.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return await auto_delete(two_step_msg, r)
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = (
        f"<blockquote><b>{ty} 𝖲𝗍𝗋𝗂𝗇𝗀 𝖲𝖾𝗌𝗌𝗂𝗈𝗇</b></blockquote>\n\n"
        f"<code>{string_session}</code>\n\n"
        "⚠️ 𝖣𝗈 𝗇𝗈𝗍 𝗌𝗁𝖺𝗋𝖾 𝗍𝗁𝗂𝗌 𝗌𝗍𝗋𝗂𝗇𝗀 𝗐𝗂𝗍𝗁 𝖺𝗇𝗒𝗈𝗇𝖾."
    )
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    done = await bot.send_message(
        msg.chat.id,
        "✅ 𝖲𝗍𝗋𝗂𝗇𝗀 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒.\n\n📩 𝖢𝗁𝖾𝖼𝗄 𝖲𝖺𝗏𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌."
    )
    await auto_delete(msg, done)
    ACTIVE_USERS.discard(msg.from_user.id)

async def cancelled(msg):
    ACTIVE_USERS.discard(msg.from_user.id)
    if "/cancel" in msg.text:
        r = await msg.reply("❌ 𝖲𝗍𝗋𝗂𝗇𝗀 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        await auto_delete(msg, r)
        return True
    elif msg.text.startswith("/"):
        r = await msg.reply("❌ 𝖲𝗍𝗋𝗂𝗇𝗀 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽.", quote=True)
        await auto_delete(msg, r)
        return True
    else:
        return False

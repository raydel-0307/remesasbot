from pyrogram import Client, filters, errors, enums
from pyrogram.types import (
    Message,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery,
    InputMediaDocument,
    InputMediaPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
    InlineQueryResultCachedPhoto,
)

from pyrogram.errors import MessageNotModified, PeerIdInvalid
import asyncio
import tgcrypto
import sqlite3
from random import randint
import re
import threading
from time import sleep
from datetime import datetime, time, timedelta
from config import *
from functions import *

from pyrogram import utils

from threading import Thread


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

CONFIRM_STATUS = {}

channels = [int(a) for a in settings]


# bot client
@bot.on_message(filters.private)
async def start(client: Client, message: Message):
    async def worker(client: Client, message: Message):
        user_id = message.from_user.id
        otm = message.text
        usid = str(user_id)
        username = message.from_user.username
        first_name = message.from_user.first_name
        chat_id = message.chat.id

        if otm and otm.startswith("/start"):
            i = start_msg(first_name)
            await bot.send_message(chat_id, i[0])

        elif otm and otm.startswith("/change") and username in owners:
            try:
                value = json.loads(otm.split(" ", 1)[1])
                await update_message(value, bot)
                await bot.send_message(username, "Datos modificados")
            except:
                pass

        elif otm and otm.startswith("/reestart") and username in owners:
            try:
                ahora = datetime.now()
                objetivo = datetime.combine(ahora.date(), time(5, 0))

                if objetivo <= ahora:
                    objetivo += timedelta(days=1)

                delta = objetivo - ahora
                segundos_restantes = delta.total_seconds()

                data, _ = await get_balance(bot)

                for user in owners:
                    data = await get_total_zelle(bot)
                    msg = f"**⭐️ 𝙎𝙪𝙗𝙩𝙤𝙩𝙖𝙡:**\n\n"
                    msg += f"📆 𝙁𝙚𝙘𝙝𝙖: {get_date()}\n"

                    msg2 = ""
                    total = 0

                    for chid in settings:
                        try:
                            total += data["zelle"][chid]
                            msg2 += f"* **[${data['zelle'][chid]}] - {settings[chid]['name']}**\n"
                        except:
                            msg2 += f"* **[$0] - {settings[chid]['name']}**\n"

                    msg += f"💰 𝘾𝙖𝙣𝙩𝙞𝙙𝙖𝙙: ${total}\n\n"
                    msg += msg2

                    await bot.send_message(user, msg)

                await delete_zelle(bot)

            except:
                pass

        elif otm and otm.startswith("/time") and username in owners:
            await bot.send_message("raydel0307", str(datetime.now()))
            await bot.send_message("raydel0307", str(get_date()))

        elif otm and otm.startswith("/subtotal") and username in owners:
            data = await get_total_zelle(bot)
            msg = f"**⭐️ 𝙎𝙪𝙗𝙩𝙤𝙩𝙖𝙡:**\n\n"
            msg += f"📆 𝙁𝙚𝙘𝙝𝙖: {get_date()}\n"

            msg2 = ""
            total = 0

            for chid in settings:
                try:
                    total += data["zelle"][chid]
                    msg2 += (
                        f"* **[${data['zelle'][chid]}] - {settings[chid]['name']}**\n"
                    )
                except:
                    msg2 += f"* **[$0] - {settings[chid]['name']}**\n"

            msg += f"💰 𝘾𝙖𝙣𝙩𝙞𝙙𝙖𝙙: ${total}\n\n"
            msg += msg2

            await bot.send_message(user_id, msg, reply_to_message_id=message.id)

        else:
            await message.delete()

    bot.loop.create_task(worker(client, message))


@bot.on_message(filters.chat(channels))
async def start(client: Client, message: Message):
    async def worker(client: Client, message: Message):
        user_id = message.from_user.id
        otm = message.text
        usid = str(user_id)
        username = message.from_user.username
        first_name = message.from_user.first_name
        chat_id = message.chat.id

        if otm and otm.startswith("/balance") and username in owners:
            value = otm.split(" ")
            if len(value) == 2:
                await set_balance(int(value[1]), bot)
            await message.delete()

        elif otm and username in CONFIRM_STATUS:
            if CONFIRM_STATUS[username]:
                await message.delete()
                await CONFIRM_STATUS[username]["nt"].delete()

                message = CONFIRM_STATUS[username]["message"]

                caption = message.caption
                msg = f"⛔️ 𝙀𝙡𝙞𝙢𝙞𝙣𝙖𝙙𝙤: {get_date()}\n"
                msg += f"📌 𝙈𝙤𝙩𝙞𝙫𝙤: {otm}\n"
                msg += caption.split("\n", 1)[1]
                msg += f"\n👤 𝘼𝙙𝙢𝙞𝙣: @{username}\n"
                msg += f"💳 𝙍𝙚𝙨𝙚𝙡𝙡𝙚𝙧: @{CONFIRM_STATUS[username]['r']}\n"

                await CONFIRM_STATUS[username]["message"].edit(msg)
                CONFIRM_STATUS.pop(username)
                return

        elif otm and "financiamiento" in otm.lower():
            value = get_financiamiento_value(otm)
            await update_balance(value, bot, str(chat_id))
            total, _ = await get_balance(bot)
            msg = f"📆 {get_date()}\n"
            msg += "📥 𝘾𝙖𝙩𝙚𝙜𝙤𝙧í𝙖: FINANCIAMIENTO\n"
            msg += f"💰 𝘾𝙖𝙣𝙩𝙞𝙙𝙖𝙙: ${value}\n"
            msg += f"🧮 𝘽𝙖𝙡𝙖𝙣𝙘𝙚: {total['balance'][str(chat_id)]}\n"
            await bot.send_message(
                message.chat.id,
                text=msg,
                reply_to_message_id=settings[str(chat_id)]["balance"],
            )

        elif message.photo and message.caption:
            caption = message.caption
            value = extract_value(caption)
            reply_to_message_id = message.reply_to_message_id
            if not reply_to_message_id:
                reply_to_message_id = 1
            button1 = InlineKeyboardButton("✅ 𝘾𝙤𝙣𝙛𝙞𝙧𝙢𝙖𝙧", f"zelle 1 {value} {username}")
            button2 = InlineKeyboardButton("⛔️ 𝙀𝙡𝙞𝙢𝙞𝙣𝙖𝙧", f"zelle 0 - {username}")
            buttons = [[button1, button2]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await bot.send_photo(
                chat_id,
                photo=message.photo.file_id,
                caption=to_confirm(value, caption),
                reply_markup=reply_markup,
                reply_to_message_id=settings[str(chat_id)]["zelle"],
            )
            await message.delete()

    bot.loop.create_task(worker(client, message))


# callbacks
@bot.on_callback_query()
async def handle_callbacks(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    message = callback_query.message
    chat_id = message.chat.id
    button_data = callback_query.data

    if username in owners:
        values = button_data.split(" ")

        if values[0] == "/cancel":
            if username in CONFIRM_STATUS:
                await CONFIRM_STATUS[username]["nt"].delete()
                CONFIRM_STATUS.pop(username)

        if values[0] == "zelle":
            caption = message.caption
            if values[1] == "0":
                reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🚫 𝘾𝙖𝙣𝙘𝙚𝙡𝙖𝙧 🚫", callback_data="/cancel")]]
                )
                m = await bot.send_message(
                    chat_id,
                    "👇 𝙀𝙣𝙫í𝙚 𝙖 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙖𝙘𝙞ó𝙣 𝙚𝙡 𝙢𝙤𝙩𝙞𝙫𝙤 𝙙𝙚 𝙡𝙖 𝙚𝙡𝙞𝙢𝙞𝙣𝙖𝙘𝙞ó𝙣:",
                    reply_markup=reply_markup,
                    reply_to_message_id=settings[str(chat_id)]["zelle"],
                )
                CONFIRM_STATUS[username] = {"message": message, "nt": m, "r": values[3]}
            elif values[1] == "1":
                try:
                    date = get_date()
                    ZELLE_TOTAL = (await get_total_zelle(bot, str(chat_id)))["zelle"][
                        str(chat_id)
                    ]
                    msg = f"✅ 𝘾𝙤𝙣𝙛𝙞𝙧𝙢𝙖𝙙𝙤: {date}\n"
                    msg += caption.split("\n", 1)[1]
                    msg += f"\n👤 𝘼𝙙𝙢𝙞𝙣: @{username}\n"
                    msg += f"💳 𝙍𝙚𝙨𝙚𝙡𝙡𝙚𝙧: @{values[3]}\n"
                    ZELLE_TOTAL += int(values[2])
                    await update_total_zelle(ZELLE_TOTAL, str(chat_id), bot)
                    msg += f"🧮 𝙎𝙪𝙗𝙩𝙤𝙩𝙖𝙡: {ZELLE_TOTAL}"
                    await message.edit_text(msg)

                    await update_balance(int(f"-{values[2]}"), bot, str(chat_id))
                    total, _ = await get_balance(bot)
                    msg2 = f"📆 {date}\n"
                    msg2 += f"📥 𝘾𝙖𝙩𝙚𝙜𝙤𝙧í𝙖: DEPÓSITO ZELLE\n"
                    msg2 += caption.split("\n", 1)[1]
                    msg2 += f"\n📥 𝙎𝙪𝙗𝙩𝙤𝙩𝙖𝙡: {ZELLE_TOTAL}\n"
                    msg2 += f"🧮 𝘽𝙖𝙡𝙖𝙣𝙘𝙚: {total['balance'][str(chat_id)]}"
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "📄 𝙈𝙚𝙣𝙨𝙖𝙟𝙚",
                                    url=f"https://t.me/c/{settings[str(chat_id)]['button']}/{settings[str(chat_id)]['zelle']}/{message.id}",
                                )
                            ]
                        ]
                    )

                    await bot.send_message(
                        message.chat.id,
                        text=msg2,
                        reply_to_message_id=settings[str(chat_id)]["balance"],
                        reply_markup=reply_markup,
                    )
                except Exception as ex:
                    await bot.send_message(
                        chat_id,
                        f"No se puso confirmar debido a un error en los datos: {ex}",
                    )


async def send_msg(bot):
    while True:
        try:
            ahora = datetime.now()
            objetivo = datetime.combine(ahora.date(), time(5, 0))

            if objetivo <= ahora:
                objetivo += timedelta(days=1)

            delta = objetivo - ahora
            segundos_restantes = delta.total_seconds()

            print(f"Durmiendo durante {segundos_restantes:.0f} segundos...")
            sleep(segundos_restantes)

            data, _ = await get_balance(bot)

            for user in owners:
                data = await get_total_zelle(bot)
                msg = f"**⭐️ 𝙎𝙪𝙗𝙩𝙤𝙩𝙖𝙡:**\n\n"
                msg += f"📆 𝙁𝙚𝙘𝙝𝙖: {get_date()}\n"

                msg2 = ""
                total = 0

                for chid in settings:
                    try:
                        total += data["zelle"][chid]
                        msg2 += f"* **[${data['zelle'][chid]}] - {settings[chid]['name']}**\n"
                    except:
                        msg2 += f"* **[$0] - {settings[chid]['name']}**\n"

                msg += f"💰 𝘾𝙖𝙣𝙩𝙞𝙙𝙖𝙙: ${total}\n\n"
                msg += msg2

                await bot.send_message(user, msg)

            await delete_zelle(bot)

        except Exception as ex:
            for user in owners:
                await bot.send_message(
                    user, f"No se pudo reiniciar de forma automatica: {ex}"
                )


def send_msg_task():
    global bot
    asyncio.run(send_msg(bot))


print("...INICIANDO...")
bot.start()
task = threading.Thread(target=send_msg_task)
task.start()
print("<BOT STARTED>")
bot.loop.run_forever()

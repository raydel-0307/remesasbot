from pyrogram.types import (
    Message,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    CallbackQuery,
    InputMediaDocument,
    InputMediaPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
    InlineQueryResultCachedPhoto,
)
from pyrogram import Client, filters, errors, enums
from random import randint
import re
from datetime import datetime
from zoneinfo import ZoneInfo
import json


async def update_total_zelle(monto, chat_id, bot):
    data, message = await get_balance(bot)
    if not chat_id in data["zelle"]:
        data["zelle"][chat_id] = 0
    data["zelle"][chat_id] = monto
    await message.edit(json.dumps(data))


async def get_total_zelle(bot, chat_id=None):
    data, _ = await get_balance(bot)
    if chat_id:
        if not chat_id in data["zelle"]:
            data["zelle"][chat_id] = 0
    return data


async def get_balance(bot):
    message = await bot.get_messages(-4625105368, 66)
    return json.loads(message.text), message


async def delete_zelle(bot):
    data, message = await get_balance(bot)
    data["zelle"] = {}
    await message.edit(json.dumps(data))


async def set_balance(value, bot):
    data, message = await get_balance(bot)
    data["balance"] = value
    await message.edit(json.dumps(data))


async def update_balance(value, bot, chat_id):
    data, message = await get_balance(bot)
    if not chat_id in data["balance"]:
        data["balance"][chat_id] = 0
    data["balance"][chat_id] += int(value)
    await message.edit(json.dumps(data))


async def update_message(value, bot):
    data, message = await get_balance(bot)
    data.update(value)
    await message.edit(json.dumps(data))


def start_msg(first_name=None):
    msg = f"⭐️ **Hola {first_name}**\n\n"
    msg += "**¡Bienvenido a tu asistente de Telegram!**\n\n"
    msg += "__Soy tu bot diseñado para Controlar el Sistema de Almacenamiento de las Remesas__\n\n"
    msg += "**✨ ¡Comencemos a potenciar tu experiencia en Telegram! ✨**"
    return msg, None


def extract_value(text):
    try:
        match = re.search(r"\$(\d+)", text)

        if match:
            return int(match.group(1))
        else:
            return None
    except:
        return None


def get_date():
    utc_time = datetime.now(ZoneInfo("UTC"))
    local_time = utc_time.astimezone(ZoneInfo("America/Havana"))
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


def to_confirm(monto, caption):
    msg = f"⌛️ 𝙋𝙚𝙣𝙙𝙞𝙚𝙣𝙩𝙚: {get_date()}\n"
    msg += f"💰 𝘾𝙖𝙣𝙩𝙞𝙙𝙖𝙙: ${monto}\n"
    msg += f"💬 𝘾𝙖𝙥𝙩𝙞𝙤𝙣: {caption}\n"
    return msg


def get_financiamiento_value(text):
    for line in text.split("\n"):
        if "financiamiento" in line.lower():
            valor = line.split("$")[-1].strip()

            match = re.search(r"-?[\d.,]+", valor)
            if match:
                valor_limpio = match.group().replace(".", "").replace(",", ".")
                return float(valor_limpio)
    return None

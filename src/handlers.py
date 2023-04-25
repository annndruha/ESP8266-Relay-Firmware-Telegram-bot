# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging
import traceback

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from telegram.constants import ParseMode

from src.settings import Settings

settings = Settings()


async def native_error_handler(update, context):
    pass


def error_handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await func(update, context)
        except Exception as err:
            logging.error(err)
            traceback.print_tb(err.__traceback__)
            await context.bot.send_message(chat_id=update.message.chat_id, text=err)

    return wrapper


@error_handler
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   message_thread_id=update.message.message_thread_id,
                                   text='Hi from relay!',
                                   disable_web_page_preview=True,
                                   parse_mode=ParseMode('HTML'))
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /start')


@error_handler
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   message_thread_id=update.message.message_thread_id,
                                   text='Help TBD;',
                                   disable_web_page_preview=True,
                                   parse_mode=ParseMode('HTML'))
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /help')


@error_handler
async def handler_button(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                 f'[{update.callback_query.message.id}] button pressed with callback_data={update.callback_query.data}')
    callback_data = update.callback_query.data

    if callback_data == 'switch':
        r = requests.get(settings.RELAY_URL + "/switch")
        text = r.text
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    else:
        text = 'Видимо бот обновился, эту issue нельзя настроить'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
        logging.error(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                      f' button pressed with old callback_data={callback_data}')
    await update.callback_query.edit_message_text(text=text,
                                                  reply_markup=keyboard,
                                                  disable_web_page_preview=True,
                                                  parse_mode=ParseMode('HTML'))


@error_handler
async def handler_message(update: Update, context: CallbackContext) -> None:
    text = 'Button below!'
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   message_thread_id=update.message.message_thread_id,
                                   text=text,
                                   reply_markup=keyboard,
                                   disable_web_page_preview=True,
                                   parse_mode=ParseMode('HTML'))


@error_handler
async def handler_switch(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/switch")
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_turn_on(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=1")
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_turn_off(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=0")
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_uptime(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/uptime")
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_get_state(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/get")
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)

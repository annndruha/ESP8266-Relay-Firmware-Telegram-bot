# Marakulin Andrey https://github.com/Annndruha
# 2023
import datetime
import logging
import traceback

import requests
from requests import RequestException
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from src.settings import Settings
from log_formatter import log_formatter

settings = Settings()


async def native_error_handler(update, context):
    pass


def error_handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            try:
                await func(update, context)
            except RequestException as err:
                logging.error(err.__class__.__name__)
                await context.bot.send_message(chat_id=update.effective_user.id, text=str(err.__class__.__name__))
            except Exception as err:
                logging.error(err)
                traceback.print_tb(err.__traceback__)
                await context.bot.send_message(chat_id=update.effective_user.id, text=str(err.__class__.__name__))
        except Exception as err:
            logging.error("Fail to send error message:", err)
            traceback.print_tb(err.__traceback__)

    return wrapper


@error_handler
@log_formatter
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🤖 Hi from relay bot!\n\nAvailable commands:\n/switch - Change state\n/turn_on - Turn lamp on\n""" \
           """/turn_off - Turn lamp off\nYou can easy find this commands in 'Menu'"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


@error_handler
@log_formatter
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """This bot created for removed lamp control.\n\nAvailable commands:\n/switch - Change state\n""" \
           """/turn_on - Turn lamp on\n/turn_off - Turn lamp off\nYou can easy find this commands in 'Menu'""" \
           """\nTechnical commands:\n/get_state - Get current state\n/uptime - ESP uptime"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


@error_handler
@log_formatter
async def handler_button(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'switch':
        r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
        text = r.text + '\n' + str(datetime.datetime.now())
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    else:
        text = 'Видимо бот обновился, эта кнопка больше недоступна.'
        keyboard = None
        logging.warning(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                        f'[old callback {update.callback_query.message.id}]: {update.callback_query.data}')
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


@error_handler
@log_formatter
async def handler_message(update: Update, context: CallbackContext) -> None:
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    await context.bot.send_message(chat_id=update.message.chat_id, text='Button below!', reply_markup=keyboard)


@error_handler
@log_formatter
async def handler_switch(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
@log_formatter
async def handler_turn_on(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=1", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
@log_formatter
async def handler_turn_off(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=0", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
@log_formatter
async def handler_uptime(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/uptime", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
@log_formatter
async def handler_get_state(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/get", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)

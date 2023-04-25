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
                await context.bot.send_message(chat_id=update.message.chat_id, text=str(err.__class__.__name__))
            except Exception as err:
                logging.error(err)
                traceback.print_tb(err.__traceback__)
                await context.bot.send_message(chat_id=update.message.chat_id, text=str(err.__class__.__name__))
        except Exception as err:
            logging.error("Fail to send error message:", err)
            traceback.print_tb(err.__traceback__)

    return wrapper


@error_handler
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text='🤖 Hi from relay bot!')
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /start')


@error_handler
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text='Help TBD;')
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /help')


@error_handler
async def handler_button(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                 f'[{update.callback_query.message.id}] button pressed with callback_data={update.callback_query.data}')
    callback_data = update.callback_query.data

    if callback_data == 'switch':
        r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
        text = r.text + '\n' + str(datetime.datetime.now())
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    else:
        text = 'Видимо бот обновился, эта кнопка больше недоступна.'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
        logging.warning(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                        f'[{update.callback_query.message.id}] button pressed with old callback_data={callback_data}')
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


@error_handler
async def handler_message(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] send message:'
                 f'{repr(update.message.text)}')
    text = 'Button below!'
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    await context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=keyboard)


@error_handler
async def handler_switch(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /switch')
    r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_turn_on(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /turn_on')
    r = requests.get(settings.RELAY_URL + "/set?value=1", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_turn_off(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /turn_off')
    r = requests.get(settings.RELAY_URL + "/set?value=0", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_uptime(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /uptime')
    r = requests.get(settings.RELAY_URL + "/uptime", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@error_handler
async def handler_get_state(update: Update, context: CallbackContext) -> None:
    logging.info(f'[{update.message.from_user.id} {update.message.from_user.full_name}] call /get_state')
    r = requests.get(settings.RELAY_URL + "/get", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)

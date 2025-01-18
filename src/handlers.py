# Marakulin Andrey https://github.com/Annndruha
# 2023
import datetime
import logging

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackContext
from src.settings import Settings
from src.log_formatter import log_formatter
from src.errors_solver import errors_solver

settings = Settings()
switch_keyboard = ReplyKeyboardMarkup([[KeyboardButton('Switch state')]],
                                      one_time_keyboard=False,
                                      resize_keyboard=True)


@errors_solver
@log_formatter
async def handler_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🤖 Hi from relay bot!\n\nAvailable commands:\n/switch - Change state\n""" \
           """/turn_on - Turn lamp on\n/turn_off - Turn lamp off""" \
           """\n/get_state - Get current state\n/uptime - ESP uptime"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=switch_keyboard)


@errors_solver
@log_formatter
async def handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """This bot created for removed lamp control.\n\nAvailable commands:\n/switch - Change state\n""" \
           """/turn_on - Turn lamp on\n/turn_off - Turn lamp off""" \
           """\n/get_state - Get current state\n/uptime - ESP uptime"""
    await context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=switch_keyboard)


@errors_solver
@log_formatter
async def handler_button(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'switch':
        r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
        text = r.text + '\n' + str(datetime.datetime.now())
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Switch state', callback_data='switch')]])
    else:
        text = 'Apparently the bot has been updated, this button is no longer available.'
        keyboard = None
        logging.warning(f'[{update.callback_query.from_user.id} {update.callback_query.from_user.full_name}]'
                        f'[old callback {update.callback_query.message.id}]: {update.callback_query.data}')
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


@errors_solver
@log_formatter
async def handler_message(update: Update, context: CallbackContext) -> None:
    if update.message.text == 'Switch state':
        await handler_switch(update, context)
    else:
        text = 'Button below ⬇️'
        await context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=switch_keyboard)


@errors_solver
@log_formatter
async def handler_switch(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/switch", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@errors_solver
@log_formatter
async def handler_turn_on(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=1", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@errors_solver
@log_formatter
async def handler_turn_off(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/set?value=0", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@errors_solver
@log_formatter
async def handler_uptime(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/uptime", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)


@errors_solver
@log_formatter
async def handler_get_state(update: Update, context: CallbackContext) -> None:
    r = requests.get(settings.RELAY_URL + "/lamp_state", timeout=3)
    await context.bot.send_message(chat_id=update.message.chat_id, text=r.text)

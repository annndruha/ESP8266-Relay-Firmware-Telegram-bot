# Marakulin Andrey https://github.com/Annndruha
# 2023
import logging
import traceback

from requests import RequestException
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes


async def native_error_handler(update, context):
    pass


def errors_solver(func):
    """
    This is decorator for telegram handlers that catches any type of exceptions.
    If exception is possible to solve, this handler send message with exception type.
    Else just log it.
    """
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            try:
                await func(update, context)
            except RequestException as err:
                logging.error(err.__class__.__name__)
                await context.bot.send_message(chat_id=update.effective_user.id, text=str(err.__class__.__name__))
            except TelegramError as err:
                logging.error(err.__class__.__name__)
                logging.error(f'TelegramError: {str(err.message)}')
                traceback.print_tb(err.__traceback__)
        except Exception as err:
            logging.error(err)
            traceback.print_tb(err.__traceback__)

    return wrapper
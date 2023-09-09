# Marakulin Andrey https://github.com/Annndruha
# 2023

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext import filters

from src.settings import Settings
from src.handlers import handler_start, handler_help, handler_switch, handler_get_state, \
    handler_button, handler_turn_on, handler_turn_off, handler_uptime, handler_message
from src.errors_solver import native_error_handler

tg_log_handler = logging.FileHandler("tgbot_telegram_updater.log")
tg_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
tg_logger = logging.getLogger('telegram.ext._updater')
tg_logger.propagate = False
tg_logger.addHandler(tg_log_handler)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == '__main__':
    settings = Settings()

    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    only_text = filters.UpdateType.MESSAGE & filters.TEXT
    application.add_handler(CommandHandler('start', handler_start, filters=only_text))
    application.add_handler(CommandHandler('help', handler_help, filters=only_text))
    application.add_handler(CommandHandler('switch', handler_switch, filters=only_text))
    application.add_handler(CommandHandler('get_state', handler_get_state, filters=only_text))
    application.add_handler(CommandHandler('turn_on', handler_turn_on, filters=only_text))
    application.add_handler(CommandHandler('turn_off', handler_turn_off, filters=only_text))
    application.add_handler(CommandHandler('uptime', handler_uptime, filters=only_text))
    application.add_handler(MessageHandler(only_text, handler_message))
    application.add_handler(CallbackQueryHandler(handler_button))
    application.add_error_handler(native_error_handler)
    application.run_polling()

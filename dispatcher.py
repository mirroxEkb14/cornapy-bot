
"""
Configure the Dispatcher
"""

import logging
import config
from aiogram import Bot, Dispatcher

# log level
logging.basicConfig(level=logging.INFO)

# init bot
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
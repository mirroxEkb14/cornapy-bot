
"""
Launch the bot
"""

from aiogram import executor
from dispatcher import dp, bot
from handlers.keyboards import KeyBoard
from helpers import google_sheet_handler 
import bot_commands
import config
import handlers
import db

async def on_shutdown(dispatcher):
	"""When stopping the python script by ^C"""
	print('\nShutdown.\n')

async def on_startup(dispatcher):
	"""When bot is started, calls the method that sets default commands for user"""

	# connect database
	config.BotDB = db.BotDB('cinema.db')

	# connect to the google sheet
	config.GoogleSheetHandler = google_sheet_handler.GoogleSheetHandler(path_to_sa_file='service_account.json', file_name='БД фильмов', sheet_name='Sheet1')

	# temporary keyboard to the 'LANGUAGE_SELECTION_ATLAUNCH' keyboard in 'sender', 
	# lang messages at the start of the bot
	config.temp_keyboard = KeyBoard()

	# set bot commands (when user uses '/' like '/start' or 'help')
	# it's english by default and never changes
	await bot_commands.set_default_commands(dp)

# run long polling
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

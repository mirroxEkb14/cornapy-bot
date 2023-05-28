
from random import randint
from aiogram import types
import logger
import asyncio
import config

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name='logger/sender.log')

class MessageSender:

	@staticmethod
	async def send_welcome(message: types.Message, bot):
		"""
		Used in personal_actions.py in the 'filter_lang_selection()' function

		It is called only once when user starts the bot for the first time,
			then the '/start' command is replaced with '/help'

		With a certain message a certain sticker is sent: the first phrase from
			'config.users_flags[tg_id]['data_dict']['BOT_WELCOME_MESSAGES']' is sent with
			the first sticker from 'config.BOT_WELCOME_STIS' and so on
		"""

		log.info('sender_call = send_welcome()')
		tg_id = message.from_user.id

		bot_welcome_msg = config.users_flags[tg_id]['data_dict']['BOT_WELCOME_MESSAGES']
		index = randint(0, len(bot_welcome_msg) - 1)

		path_to_sti = list(config.BOT_WELCOME_STIS.values())[index]
		with open(path_to_sti, 'rb') as bot_welcome_sti: 
			await bot.send_sticker(chat_id=message.chat.id, sticker=bot_welcome_sti)

			me = await bot.get_me()
			await message.answer(bot_welcome_msg[index].format(user_name=message.from_user.first_name, bot_name=me.first_name), 
				parse_mode='html', reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION']) 


	@staticmethod
	async def send_lang_message(message: types.Message):
		"""
		Used in CommandHandler

		When user tries to type something when the language for the bot is not selected yet
		"""

		log.info('sender_call = send_lang_message()')

		bot_lang_msg = config.BOT_LANG_MESSAGES
		await message.answer(bot_lang_msg[randint(0, len(bot_lang_msg) - 1)], reply_markup=config.temp_keyboard.REPLY_KEYBOARDS['LANGUAGE_SELECTION_ATLAUNCH'])


	@staticmethod
	async def send_to_main_menu_message(message: types.Message):
		"""
		Used in personal_actions.py 

		When user leaves some mode and returns to the main-menu
		"""

		log.info('sender_call = send_to_main_menu_message()')
		tg_id = message.from_user.id

		await asyncio.sleep(0.5)
		to_main_menu_msg = config.users_flags[tg_id]['data_dict']['TO_MAIN_MENU']
		await message.answer(to_main_menu_msg[randint(0, len(to_main_menu_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])
		
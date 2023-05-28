
from aiogram import types
from random import randint
from dispatcher import bot
from helpers.sender import MessageSender
import logger
import config

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name='logger/command_handler.log')

class CommandHandler:

	@staticmethod
	async def is_inner_mode(message: types.Message) -> bool:
		"""
		Used in personal_actions.py in all cmd-commands

		This check-function is called from all the methods that process commands
			to check, if the user tries to call some command while he's in some
			another mode
		"""

		log.info('ch_call = is_inner_mode()')
		tg_id = message.from_user.id

		if config.user_exists(tg_id) and config.users_flags[tg_id]['is_first_launch']:
			"""
			User deviation during: first language selection (before the '/start' command)

			User enters some command before selecting the language at the first bot launch
			Apparently, this case is not necessary to process, because if user finds the bot for
				the first time, he cannot enter anything but '/start' command
			"""

			await MessageSender.send_lang_message(message)
			return True
	
		elif config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH']:
			"""
			User deviation during: 'Smart selection'

			User tries to call the command while 'Smart Selection'
			"""

			ss_deviation_msg = config.users_flags[tg_id]['data_dict']['SS_DEVIATION_MESSAGES']
			await message.reply(ss_deviation_msg[randint(0, len(ss_deviation_msg) - 1)])
			return True

		elif config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK']:
			"""
			User deviation during 'Send feedback'

			User tries to call the command while 'Send feedback'
			"""

			sf_deviation_msg = config.users_flags[tg_id]['data_dict']['SF_DEVIATION_MESSAGES']
			await message.reply(sf_deviation_msg[randint(0, len(sf_deviation_msg) - 1)])
			return True

		elif config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES']:
			"""
			User deviation during 'No preferences'

			User tries to call the command while 'No preferences'
			"""

			np_deviation_msg = config.users_flags[tg_id]['data_dict']['NP_DEVIATION_MESSAGES']
			await message.reply(np_deviation_msg[randint(0, len(np_deviation_msg) - 1)])
			return True

		elif config.users_flags[tg_id]['ARE_SETTINGS']:
			"""
			User deviation during: '/settings' menu

			User tries to call the command while he's in '/settings' menu
			"""

			settings_deviation_msg = config.users_flags[tg_id]['data_dict']['SETTINGS_DEVIATION_MESSAGES']
			await message.reply(settings_deviation_msg[randint(0, len(settings_deviation_msg) - 1)])
			return True

		elif config.users_flags[tg_id]['IS_OFFERING_MOVIE']:
			"""
			"User deviation during: '/offermovie' mode"

			User tries to call some command while he's offering movies
			"""

			offering_movie_deviation_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['OFFERING_MOVIE_DEVIATION']
			await message.reply(offering_movie_deviation_msg[randint(0, len(offering_movie_deviation_msg) - 1)])
			return True

		elif config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE']:
			"""
			"User deviation during: '!admin' mode"

			The admin tries to call some command while he's in '!admin' mode
			"""

			am_deviation_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['AM_DEVIATION_MESSAGES']
			await message.answer(am_deviation_msg[randint(0, len(am_deviation_msg) - 1)])
			return True

		return False


	@staticmethod
	def is_smart_search(text, tg_id):
		""" 
		Used in personal_actions.py in the 'filter_smart_selection()' function

		'config.users_flags[tg_id]['data_dict']' is checked to avoid the situation when before selecting the language in the 
			beginning, user tries to type something different, in this case we need to reach the
			'checkout' func at the end of personal_actions.py, but because of 'config.users_flags[tg_id]['data_dict']' is not 
			defined yet, there'll be a NoneType exception, so we check the dict first, before 
			'message.text == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SMART_SEARCH_BTN']', where the dict is None
		"""
		
		return config.users_flags[tg_id]['data_dict'] \
			and (text == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SMART_SEARCH_BTN'] \
					or text.lower() == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SMART_SEARCH_BTN'][2:].lower()) \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] == False \
			and config.users_flags[tg_id]['ARE_SETTINGS'] == False \
			and config.users_flags[tg_id]['IS_OFFERING_MOVIE'] == False \
			and config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] == False


	@staticmethod
	def is_send_feedback(text, tg_id):
		"""Used in personal_actions.py in the 'filter_send_feedback()' function"""

		return config.users_flags[tg_id]['data_dict'] \
			and (text == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SEND_FEEDBACK_BTN'] \
				or text.lower() == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SEND_FEEDBACK_BTN'][2:].lower()) \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] == False \
			and config.users_flags[tg_id]['ARE_SETTINGS'] == False \
			and config.users_flags[tg_id]['IS_OFFERING_MOVIE'] == False \
			and config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] == False


	@staticmethod
	def is_no_preferences(text, tg_id):
		"""Used in personal_actions.py in the 'filter_no_preferences()' function"""

		return config.users_flags[tg_id]['data_dict'] \
			and (text == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['NO_PREFERENCES_BTN'] \
				or text.lower() == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['NO_PREFERENCES_BTN'][2:].lower()) \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] == False \
			and config.users_flags[tg_id]['ARE_SETTINGS'] == False \
			and config.users_flags[tg_id]['IS_OFFERING_MOVIE'] == False \
			and config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] == False


	@staticmethod
	def is_we_recommend(text, tg_id):
		"""Used in personal_actions.py in the 'filter_we_recommend()' function"""

		return config.users_flags[tg_id]['data_dict'] \
			and (text == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['WE_RECOMMEND_BTN'] \
				or text.lower() == config.users_flags[tg_id]['data_dict']['MainMenuButtons']['WE_RECOMMEND_BTN'][2:].lower()) \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] == False \
			and config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] == False \
			and config.users_flags[tg_id]['ARE_SETTINGS'] == False \
			and config.users_flags[tg_id]['IS_OFFERING_MOVIE'] == False \
			and config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] == False


	@staticmethod
	def reset_ss_constants(tg_id):
		"""
		Used in callbacks.py in the 'process_ss_yes()' and 'on_ss_back()' functions

		After user confirms he selected all the categories right OR 
			user selects 'back' on mood selection and goes to the main menu
		"""

		config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] = False
		
		for el in config.users_flags[tg_id]['USER_DATA']:
			config.users_flags[tg_id]['USER_DATA'][el] = None

		for el in config.users_flags[tg_id]['SS_PROCESS_FLAGS']:
			config.users_flags[tg_id]['SS_PROCESS_FLAGS'][el] = False


	@staticmethod
	def reset_sf_constants(tg_id):
		"""
		Used in personal_actions.py ('message_checkout()' function) and callbacks.py ('on_sf_back()' function)

		When the user leaves feedback OR selects 'back' on movie name selection and goes to the main menu
		"""

		config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] = False

		for el in config.users_flags[tg_id]['FEEDBACK_DICT']:
			config.users_flags[tg_id]['FEEDBACK_DICT'][el] = None

		for el in config.users_flags[tg_id]['SF_PROCESS_FLAGS']:
			config.users_flags[tg_id]['SF_PROCESS_FLAGS'][el] = False


	@staticmethod
	async def is_inline_old(call, flag, tg_id) -> bool:
		"""
		Used in callbacks.py in each method

		If the bot shuts down but has some active inline-keyboard, then when he
			restarts, user can use that keyboard:
			- at bot launch when he hasn't selected the language yet, then this 
				method removes that keyboard and send a message to a user
			- when the language is already set, then we just remind a user
				to set the language first
		Returns True if it's an old keyboard
		"""

		if not config.users_flags[tg_id]['is_first_launch']:

			if not flag:
				await bot.edit_message_reply_markup(chat_id=tg_id, 
					message_id=call.message.message_id, reply_markup=None)

				old_keyboard_msg = config.users_flags[tg_id]['data_dict']['OLD_KEYBOARD']
				await call.message.answer(old_keyboard_msg[randint(0, len(old_keyboard_msg) - 1)])
				return True

		else:
			await MessageSender.send_lang_message(call.message)
			return True

		return False

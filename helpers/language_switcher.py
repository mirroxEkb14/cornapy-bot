
from bot_commands import set_default_commands
from dispatcher import dp
from handlers.keyboards import KeyBoard 	
import logger
import json
import config

log = logger.get_logger(logger_name=__name__, file_name='logger/personal_actions.log')

class LanguageSwitcher:
	"""
	During changing the language in personal_actions.py in the 'cmd_lang()' and 'filter_lang_selection()'
		functions

	Contains methods that switch the language
	"""

	@staticmethod
	async def to_eng_lang(tg_id):
		"""Resets lang-flags and dicts"""

		log.info("ls_call = to_eng_lang()")

		with open('data.json', encoding='utf-8') as f:
			json_data = json.load(f)
			config.users_flags[tg_id]['data_dict'] = json_data['english']

		config.users_flags[tg_id]['SELECTED_LANGUAGE']['en'] = True
		config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru'] = False

		if config.users_flags[tg_id]['is_first_launch']:
			"""First user's launch, set the keyboard"""
			config.users_flags[tg_id]['keyboards'] = KeyBoard()

		config.users_flags[tg_id]['keyboards'].reset_keyboards(tg_id)
		config.users_flags[tg_id]['HELP_COMMAND_MESSAGE'] = '\n\n'.join(part for part in config.users_flags[tg_id]['data_dict']['HELP_COMMAND_PARTS'].values())

	@staticmethod
	async def to_rus_lang(tg_id):
		"""Sets dics and lang-flags to rus"""

		log.info("ls_call = to_rus_lang()")

		with open('data.json', encoding='utf-8') as f:
			json_data = json.load(f)
			config.users_flags[tg_id]['data_dict'] = json_data['russian']

		config.users_flags[tg_id]['SELECTED_LANGUAGE']['en'] = False
		config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru'] = True

		if config.users_flags[tg_id]['is_first_launch']:
			"""First user's launch, set the keyboard"""
			config.users_flags[tg_id]['keyboards'] = KeyBoard()

		config.users_flags[tg_id]['keyboards'].reset_keyboards(tg_id)
		config.users_flags[tg_id]['HELP_COMMAND_MESSAGE'] = '\n\n'.join(part for part in config.users_flags[tg_id]['data_dict']['HELP_COMMAND_PARTS'].values())

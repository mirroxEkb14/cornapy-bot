
from aiogram import types
from config import data_provider

async def set_default_commands(dp):
	"""
	Sets default commands user will have when interacting with the bot
	By default it's set to english
	"""
	await dp.bot.set_my_commands(
		[
			types.BotCommand('start', data_provider['english']['LANG_CMD']['START_DESC']),
			types.BotCommand('help', data_provider['english']['LANG_CMD']['HELP_DESC']),
			types.BotCommand('lang', data_provider['english']['LANG_CMD']['LANG_DESC_GENERAL']),
			types.BotCommand('settings', data_provider['english']['LANG_CMD']['SETTINGS_DESC']),
			types.BotCommand('offermovie', data_provider['english']['LANG_CMD']['OFFERMOVIE_DESC'])
		]
	)
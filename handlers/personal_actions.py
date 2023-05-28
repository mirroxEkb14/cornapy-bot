
"""
Bot's various replies to user's messages
"""

from aiogram import types
from dispatcher import dp, bot
from random import randint
from config import data_provider
from helpers.command_handler import CommandHandler
from helpers.movie_format import MovieFormat
from helpers.language_switcher import LanguageSwitcher
from helpers.sender import MessageSender
import asyncio
import config	
import logger

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name='logger/personal_actions.log')


""" 
-----------------------------------------------------------------

'/commands'

----------------------------------------------------------------- 
"""	


"""User selects his preffered language"""
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
	
	log.info("reply_call = cmd_start()")
	tg_id = message.from_user.id

	if not config.user_exists(tg_id):
		"""
		Add a user to the dict
		Is performed only once, when user launches the bot for the first time
		"""
		config.add_user(tg_id)

	if not await CommandHandler.is_inner_mode(message):
		"""
		User tries to call '/start' command but it is not his first interaction with the bot,
			we replace the '/start' command with '/help'
		"""

		bot_second_welcome_msg = config.users_flags[message.from_user.id]['data_dict']['BOT_SECOND_WELCOME_MESSAGES']
		await message.answer(bot_second_welcome_msg[randint(0, len(bot_second_welcome_msg) - 1)])

		await asyncio.sleep(2)
		await cmd_help(message)


"""Displays the discription of each option from main-menu"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id), commands=['help'])
async def cmd_help(message: types.Message):

	log.info("reply_call = cmd_help()")
	tg_id = message.from_user.id

	if not config.users_flags[tg_id]['is_first_launch'] or not await CommandHandler.is_inner_mode(message):
		await message.answer(config.users_flags[tg_id]['HELP_COMMAND_MESSAGE'], parse_mode='html')


"""When user wants to change the language"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id), commands=['lang'])
async def cmd_lang(message: types.Message):

	log.info("reply_call = cmd_lang()")
	tg_id = message.from_user.id

	if not await CommandHandler.is_inner_mode(message):

		if config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
			await LanguageSwitcher.to_rus_lang(tg_id)
		elif config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru']:
			await LanguageSwitcher.to_eng_lang(tg_id)

		on_changed_lang_msg = config.users_flags[tg_id]['data_dict']['LANG_CMD']['ON_CHANGED_LANGUAGE']
		await message.answer(on_changed_lang_msg[randint(0, len(on_changed_lang_msg) - 1)])

		await MessageSender.send_to_main_menu_message(message)


"""Settings inline-menu"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id), commands=['settings'])
async def cmd_settings(message: types.Message):

	log.info("reply_call = cmd_settings()")
	tg_id = message.from_user.id

	if not await CommandHandler.is_inner_mode(message):
		config.users_flags[message.from_user.id]['ARE_SETTINGS'] = True

		main_settings_mgs = config.users_flags[tg_id]['data_dict']['SETTINGS_MESSAGES']['MAIN_SETTINGS_MESSAGES']
		await message.answer(main_settings_mgs[randint(0, len(main_settings_mgs) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SETTINGS_MENU'])


"""User wants to offer movies to be added to the database"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id), commands=['offermovie'])
async def cmd_offermovie(message: types.Message):
	
	log.info("reply_call = cmd_offermovie()")
	tg_id = message.from_user.id

	if not await CommandHandler.is_inner_mode(message):
		config.users_flags[tg_id]['IS_OFFERING_MOVIE'] = True

		await message.answer(config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ADDING_USER_MOVIE_FORMAT'], 
			parse_mode='html', reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['OFFERING_MOVIE_EXIT'])

		if config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
			path_to_sti = config.USER_OFFERING_MOVIE_STIS['STI_ENG']
			with open(path_to_sti, 'rb') as sticker_eng:
				await bot.send_sticker(chat_id=message.chat.id, sticker=sticker_eng)

		elif config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru']:
			path_to_sti = config.USER_OFFERING_MOVIE_STIS['STI_RUS']
			with open(path_to_sti, 'rb') as sticker_rus:
				await bot.send_sticker(chat_id=message.chat.id, sticker=sticker_rus)


"""Set selected language by user to the bot"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and (message.text == data_provider['english']['ENG_LANG_BTN'] or \
	message.text == data_provider['russian']['RUS_LANG_BTN']) and list(config.users_flags[message.from_user.id]['SELECTED_LANGUAGE'].values()) == [False, False])
async def filter_lang_selection(message: types.Message):

	log.info('reply_call = filter_lang_selection()')
	tg_id = message.from_user.id

	if message.text == data_provider['english']['ENG_LANG_BTN']: 
		await LanguageSwitcher.to_eng_lang(tg_id)
	elif message.text == data_provider['russian']['RUS_LANG_BTN']:
		await LanguageSwitcher.to_rus_lang(tg_id)
		
	await MessageSender.send_welcome(message, bot)
	config.users_flags[tg_id]['is_first_launch'] = False


""" 
-----------------------------------------------------------------

'Smart Search'

----------------------------------------------------------------- 
"""


"""'Smart Search' case """
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and CommandHandler.is_smart_search(message.text, message.from_user.id))
async def filter_smart_search(message: types.Message):
	
	log.info("reply_call = filter_smart_selection()")
	tg_id = message.from_user.id

	config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'] = True

	with open(config.SMART_SELECTION_STI, 'rb') as smrt_selection_sti: 
		await bot.send_sticker(chat_id=message.chat.id, sticker=smrt_selection_sti)
	
	at_launch_greetings_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['AT_LAUNCH_GREETINGS']
	await message.answer(at_launch_greetings_msg[randint(0, len(at_launch_greetings_msg) - 1)])
	
	await asyncio.sleep(1)

	mood_selection_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['MOOD_SELECTION']
	await message.answer(mood_selection_msg[randint(0, len(mood_selection_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_MOOD_SELECTION'])


""" 
-----------------------------------------------------------------

'Send feedback'

----------------------------------------------------------------- 
"""


""" 'Send feedback' case """
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and CommandHandler.is_send_feedback(message.text, message.from_user.id))
async def filter_send_feedback(message: types.Message):

	log.info("reply_call = filter_send_feedback()")
	tg_id = message.from_user.id

	config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] = True

	if not config.BotDB.is_user_selection(tg_id):
		"""
		If user clicks 'Send feedback', although either he hasn't used 'Smart selection' yet, or 
			he'd already sent feedbacks about all movies he watched(in both cases that means he's 
			not in the 'user_selection')
		"""

		not_in_table_msg = config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['NOT_IN_TABLE']
		await message.answer(not_in_table_msg[randint(0, len(not_in_table_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SF_GOOGLE_FORM'])
		return

	config.users_flags[tg_id]['keyboards'].set_sf_movies_keyboard(tg_id)

	config.users_flags[tg_id]['FEEDBACK_DICT']['tg_id'] = tg_id
	config.users_flags[tg_id]['FEEDBACK_DICT']['tg_name'] = message.from_user.first_name

	movie_selection_msg = config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['MOVIE_SELECTION']
	await message.answer(movie_selection_msg[randint(0, len(movie_selection_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SF_MOVIE_SELECTION'])


""" 
-----------------------------------------------------------------

'No preferences'

----------------------------------------------------------------- 
"""


"""'No preferences' case"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and CommandHandler.is_no_preferences(message.text, message.from_user.id))
async def filter_no_preferences(message: types.Message):

	log.info("reply_call = filter_no_preferences()")
	tg_id = message.from_user.id

	config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] = True

	on_start_msg = config.users_flags[tg_id]['data_dict']['NP_PROCESSING_MESSAGES']['ON_START']
	index = randint(0, len(on_start_msg) - 1)

	path_to_sti = list(config.NO_PREFERENCES_STIS.values())[index]
	with open(path_to_sti, 'rb') as np_starting_sti:
		await bot.send_sticker(chat_id=message.chat.id, sticker=np_starting_sti)
		await message.answer(on_start_msg[index])

		rand_movie = config.BotDB.get_np_random_movie(message.from_user.id)
		movie_msg = MovieFormat.get_np_movie_format(rand_movie)

		await asyncio.sleep(1)
		await message.answer(movie_msg, reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['NP_NEXT_MOVIE'])


""" 
-----------------------------------------------------------------

'We recommend'

----------------------------------------------------------------- 
"""


"""'We recommend' case"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and CommandHandler.is_we_recommend(message.text, message.from_user.id))
async def filter_we_recommend(message: types.Message):

	log.info("reply_call = filter_we_recommend()")
	tg_id = message.from_user.id

	config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] = True
	config.users_flags[tg_id]['wr_movies']['movies'] = config.BotDB.get_wr_movies(tg_id)

	wr_at_start_msg = config.users_flags[tg_id]['data_dict']['WR_PROCESSING_MESSAGES']['WR_AT_START']
	await message.answer(wr_at_start_msg[randint(0, len(wr_at_start_msg) - 1)])
	await asyncio.sleep(1)

	await message.answer(config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][0], 
		reply_markup=config.users_flags[tg_id]['keyboards'].get_wr_movies_start_keyboard(tg_id, config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][1]), parse_mode='html')


""" 
-----------------------------------------------------------------

'admin-mode'

----------------------------------------------------------------- 
"""


"""Admin command is called"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and message.text == config.ADMIN_COMMAND)
async def filter_admin(message: types.Message):

	log.info("reply_call = filter_admin()")
	tg_id = message.from_user.id

	if tg_id == config.AdminID.SERJIO_ID.value or tg_id == config.AdminID.DANCHO_ID.value:
		"""It's admins"""

		if not await CommandHandler.is_inner_mode(message):

			config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] = True

			admin_welcome_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_WELCOME']
			index = randint(0, len(admin_welcome_msg) - 1)

			path_to_sti = list(config.ADMIN_WELCOME_STIS.values())[index]
			with open(path_to_sti, 'rb') as welcome_admin_sti:
				await bot.send_sticker(chat_id=message.chat.id, sticker=welcome_admin_sti)
				await message.answer(admin_welcome_msg[index].format(user_name=message.from_user.first_name), reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])

	else:
		"""Not an admin"""

		not_an_admin_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['NOT_AN_ADMIN']
		index = randint(0, len(not_an_admin_msg) - 1)

		path_to_sti = list(config.NOT_AN_ADMIN_STIS.values())[index]
		with open(path_to_sti, 'rb') as not_an_admin_sti:
			await bot.send_sticker(chat_id=message.chat.id, sticker=not_an_admin_sti)
			await message.reply(not_an_admin_msg[index].format(user_name=message.from_user.first_name))
	

"""The admin adds a movie to the DB"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and config.users_flags[message.from_user.id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] and config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] and message.text != config.users_flags[message.from_user.id]['data_dict']['MOVIE_ADDING_BACK_BTN'])
async def filter_adding_admin_movie(message: types.Message):

	log.info("reply_call = filter_adding_admin_movie()")
	tg_id = message.from_user.id

	categories = ['rus_name', 'rus_mood', 'rus_catalogue', 'rus_genre', 'release_year', 'rus_link', 'eng_name', 'eng_link', 'poster_link']

	user_input = message.text.split('\n')
	movie_dict = {category: input_item for category, input_item in zip(categories, user_input)}

	if len(user_input) == len(categories):
		"""Message format for one movie is correct"""

		if not await MovieFormat.is_formatted_rus(message, data_provider, config.users_flags[tg_id]['data_dict'], movie_dict):
			return
		
		formatted_movie_list = MovieFormat.get_formatted_movie(data_provider, movie_dict)
		config.BotDB.add_movie(formatted_movie_list)

		if MovieFormat.is_movie(data_provider, movie_dict):
			"""If it is a movie"""
			offering_movie_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['OFFERING_MOVIE']
			await message.answer(offering_movie_msg[randint(0, len(offering_movie_msg) - 1)])

		else:
			"""If it is a series"""
			offering_serial_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['OFFERING_SERIAL']
			await message.answer(offering_serial_msg[randint(0, len(offering_serial_msg) - 1)])
		
	else:
		"""
		The format is incorrect (there more or less than 6 parameters)
		The 'config.IS_OFFERING_MOVIE' constant remains True, what means user can go on offering
		"""
		offering_movie_incorrect_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['OFFERING_MOVIE_INCORRECT']
		await message.reply(offering_movie_incorrect_msg[randint(0, len(offering_movie_incorrect_msg) - 1)])
		return

	config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] = False

	await asyncio.sleep(1)
	admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
	await message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""User wrote and sent the message, so we have to say goodbye"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] and message.text != config.users_flags[message.from_user.id]['data_dict']['MOVIE_OFFERING_BACK_BTN']
	and not config.users_flags[message.from_user.id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'])
async def filter_offering_movie(message: types.Message):

	log.info("reply_call = filter_offering_movie()")
	tg_id = message.from_user.id

	config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] = False
	config.BotDB.add_movie_offer(tg_id, message.text)

	on_user_offered_movie_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ON_USER_OFFERED_MOVIE']
	index = randint(0, len(on_user_offered_movie_msg) - 1)
	path_to_sti = list(config.USER_OFFERING_MOVIE_STIS['ON_MOVIE_OFFERED'].values())[index]

	with open(path_to_sti, 'rb') as on_offered_sti:
		if index == len(on_user_offered_movie_msg) - 1:
			await bot.send_sticker(chat_id=message.chat.id, sticker=on_offered_sti.read().decode('utf-8'))
		else:
			await bot.send_sticker(chat_id=message.chat.id, sticker=on_offered_sti)

	await message.answer(on_user_offered_movie_msg[index])

	await asyncio.sleep(1)
	await message.answer(config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['TO_MAIN_MENU'][index], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])


"""When user's leaving '/offermovie' mode and returns to the main-menu"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] and message.text == config.users_flags[message.from_user.id]['data_dict']['MOVIE_OFFERING_BACK_BTN'])
async def filter_offering_movie_exit(message: types.Message):

	log.info('reply_call = filter_offering_movie_exit()')
	tg_id = message.from_user.id
	
	on_exit_offering_movie_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ON_EXIT_OFFERING_MOVIE']
	await message.answer(on_exit_offering_movie_msg[randint(0, len(on_exit_offering_movie_msg) - 1)])

	config.users_flags[tg_id]['IS_OFFERING_MOVIE'] = False
	await MessageSender.send_to_main_menu_message(message)


"""When the admin's leaving 'add movie' mode and returns to the main admin menu"""
@dp.message_handler(lambda message: config.user_exists(message.from_user.id) and config.users_flags[message.from_user.id]['IS_OFFERING_MOVIE'] and message.text == config.users_flags[message.from_user.id]['data_dict']['MOVIE_ADDING_BACK_BTN'])
async def filter_adding_admin_movie_exit(message: types.Message):

	log.info('reply_call = filter_adding_admin_movie_exit()')
	tg_id = message.from_user.id
	
	on_exit_offering_movie_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ON_EXIT_ADDING_ADMIN_MOVIE']
	await message.answer(on_exit_offering_movie_msg[randint(0, len(on_exit_offering_movie_msg) - 1)])

	config.users_flags[tg_id]['IS_OFFERING_MOVIE'] = False
	
	await asyncio.sleep(1)
	admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
	await message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""Process user's messages that don't contain commands or btn texts"""
@dp.message_handler(state="*")
async def reply_checkout(message: types.Message):

	log.info("reply_call = reply_checkout()")
	tg_id = message.from_user.id

	if not config.user_exists(tg_id):
		"""
		Each handler in this file has the verification of 'config.user_exists(message.from_user.id)', so that
			before the next checks we check if the user who entered some random text on his first bot interaction
			exists in 'users_flags' or not

		Basically, when a user opens the bot for the first time, he has no other possibiblity but enter '/start',
			and in this case the code works properly, because in 'cmd_start()' we add the user, but for people,
			who already had a chat history with the bot, have possibility to enter whatever they want, and in
			this case without these additional verification an axeption would be thrown: "KeyError: 1234567890"
		"""
		await cmd_start(message)

	elif config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] and config.users_flags[tg_id]['SF_PROCESS_FLAGS']['verdict_selected']:
		"""
		The user sends his comment on the watched movie during Send feedback,
			it is the last step of Send feedback
		"""

		config.users_flags[tg_id]['FEEDBACK_DICT']['comment'] = message.text
		config.BotDB.add_user_to_new_feedbacks(message.from_user.id)

		config.BotDB.add_user_history(message.from_user.id)

		config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] = False
		config.BotDB.delete_user_selection_movie(message.from_user.id)
		CommandHandler.reset_sf_constants(tg_id)

		on_finish_msg = config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['ON_FINISH']
		index = randint(0, len(on_finish_msg) - 1)

		path_to_sti = list(config.SEND_FEEDBACK_STIS.values())[index]
		with open(path_to_sti, 'rb') as sf_finishing_sti:
			await bot.send_sticker(chat_id=message.chat.id, sticker=sf_finishing_sti)
			await message.answer(on_finish_msg[index])

			await asyncio.sleep(1)
			await message.answer(config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['TO_MAIN_MENU'][index], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])

	elif not await CommandHandler.is_inner_mode(message):
		"""Deviation during runtime"""

		user_deviation_msg = config.users_flags[tg_id]['data_dict']['USER_DEVIATION_MESSAGES']
		await message.reply(user_deviation_msg[randint(0, len(user_deviation_msg) - 1)])

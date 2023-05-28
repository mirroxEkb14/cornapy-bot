
"""
Handle events when clicking on inline-buttons

Every handler as 'text' takes lists from both languages, but inside
	'config.users_flags[tg_id]['data_dict']' is used, so that the handler knows what language is 
	currently specified and from what lang-dict take the data
"""

from aiogram import types
from dispatcher import dp, bot
from random import randint
from config import data_provider
from helpers.movie_format import MovieFormat
from helpers.command_handler import CommandHandler
from aiogram.utils.exceptions import MessageNotModified
import logger
import config
import asyncio

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name = 'logger/callbacks.log')


""" 
-----------------------------------------------------------------

'Smart Search'

----------------------------------------------------------------- 
"""	


"""
Processing user's mood selection
	'call.data' represents a value of selected mood by user from UserMood
"""
@dp.callback_query_handler(text=list(data_provider['english']['InlineKeyboardCallbacks']['UserMood'].values()) +
	list(data_provider['russian']['InlineKeyboardCallbacks']['UserMood'].values()))
async def process_ss_mood(call: types.CallbackQuery):

	log.info("inline_call = process_ss_mood()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	config.users_flags[tg_id]['USER_DATA']['USER_MOOD'] = call.data.capitalize()
	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['mood_selected'] = True

	catalogue_selection_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['CATALOGUE_SELECTION']
	await call.message.edit_text(text=catalogue_selection_msg[randint(0, len(catalogue_selection_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_CATALOGUE_SELECTION'])


"""Processing user's catalogue selection"""
@dp.callback_query_handler(text=list(data_provider['english']['InlineKeyboardCallbacks']['Catalogue'].values()) +
	list(data_provider['russian']['InlineKeyboardCallbacks']['Catalogue'].values()))
async def process_ss_show(call: types.CallbackQuery):

	log.info("inline_call = process_ss_show()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	config.users_flags[tg_id]['USER_DATA']['USER_CATALOGUE'] = call.data.capitalize()
	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['catalogue_selected'] = True

	genre_selection_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['GENRE_SELECTION']
	await call.message.edit_text(text=genre_selection_msg[randint(0, len(genre_selection_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_GENRE_SELECTION'])


"""Processing user's genre selection"""
@dp.callback_query_handler(text=list(data_provider['english']['InlineKeyboardCallbacks']['Genre']['Main'].values()) +
	list(data_provider['russian']['InlineKeyboardCallbacks']['Genre']['Main'].values()) +
	list(data_provider['english']['InlineKeyboardCallbacks']['Genre']['More'].values()) +
	list(data_provider['russian']['InlineKeyboardCallbacks']['Genre']['More'].values()))
async def process_ss_genre(call: types.CallbackQuery):

	log.info("inline_call = process_ss_genre()")
	tg_id = call.from_user.id
	
	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	config.users_flags[tg_id]['USER_DATA']['USER_GENRE'] = call.data.capitalize()
	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['genre_selected'] = True

	ss_verifying_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['SS_VERIFYING']
	await call.message.edit_text(text=ss_verifying_msg[randint(0, len(ss_verifying_msg) - 1)]
		.format(user_mood=config.users_flags[tg_id]['USER_DATA']['USER_MOOD'], user_catalogue=config.users_flags[tg_id]['USER_DATA']['USER_CATALOGUE'], user_genre=config.users_flags[tg_id]['USER_DATA']['USER_GENRE']), 
				reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_SUMMARY_VERIFICATION'], parse_mode='html')


"""When user clicks on the 'More' btn, a new keyboard with all the genres pops up"""
@dp.callback_query_handler(text=data_provider['english']['InlineKeyboardCallbacks']['Genre']['MORE_CB'])
async def process_ss_more_genre(call: types.CallbackQuery):

	log.info('inline_call = process_ss_more_genre()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	await bot.edit_message_reply_markup(chat_id=tg_id, message_id=call.message.message_id, 
		reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_MORE_GENRE_SELECTION'])


"""
Processing the confirmation of all user's selections from 'Smart Selection'
If user agrees that all his selections are correct
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['SSConfirmation']['YES_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['SSConfirmation']['YES_CB']])
async def process_ss_yes(call: types.CallbackQuery):

	log.info("inline_call = process_ss_yes()")
	tg_id = call.from_user.id
	
	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	ss_verified_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['SS_VERIFIED']
	await call.message.answer(ss_verified_msg[randint(0, len(ss_verified_msg) - 1)])

	db_movies = config.BotDB.get_movies(tg_id, config.users_flags[tg_id]['USER_DATA']['USER_MOOD'], config.users_flags[tg_id]['USER_DATA']['USER_CATALOGUE'], config.users_flags[tg_id]['USER_DATA']['USER_GENRE'])
	await asyncio.sleep(1.5)

	config.BotDB.add_user_search_history(tg_id, call.from_user.first_name)
	
	if not db_movies:
		"""If no movies were found referring to selected user's mood/catalogue/genre"""

		no_movies_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['NO_MOVIES']
		index = randint(0, len(no_movies_msg) - 1)

		path_to_sti = list(config.NO_MOVIES_STIS.values())[index]
		with open(path_to_sti, 'rb') as no_movie_sti:
			await bot.send_sticker(chat_id=call.message.chat.id, sticker=no_movie_sti)
			await call.message.answer(no_movies_msg[index])

			on_failure_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ON_FAILURE']
			await asyncio.sleep(2)
			await call.message.answer(on_failure_msg[randint(0, len(on_failure_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])
		
		CommandHandler.reset_ss_constants(tg_id)
		return

	config.BotDB.add_user_selection(tg_id, db_movies)
	config.BotDB.add_user_movie_selection_history(tg_id, db_movies)

	await MovieFormat.send_movies(call.message, config.users_flags[tg_id]['data_dict'], db_movies)
	CommandHandler.reset_ss_constants(tg_id)

	await asyncio.sleep(2)
	ss_on_finish_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['ON_FINISH']
	await call.message.answer(ss_on_finish_msg[randint(0, len(ss_on_finish_msg) - 1)].format(feedback_btn=config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SEND_FEEDBACK_BTN']))


"""
Processing the confirmation of all user's selections from 'Smart Selection'
Get user to the beginning - mood selection
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['SSConfirmation']['NO_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['SSConfirmation']['NO_CB']])
async def process_ss_no(call: types.CallbackQuery):

	log.info("inline_call = process_ss_no()")
	tg_id = call.from_user.id
	
	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['mood_selected'] = False
	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['catalogue_selected'] = False
	config.users_flags[tg_id]['SS_PROCESS_FLAGS']['genre_selected'] = False

	ss_summingup_back_message = config.users_flags[tg_id]['data_dict']['SS_BACK_MESSAGES']['ON_SUMMINGUP_SELECTION_BACK']
	await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id, 
		text=ss_summingup_back_message[randint(0, len(ss_summingup_back_message) - 1)], reply_markup=None)

	await asyncio.sleep(1)

	mood_selection_msg = config.users_flags[tg_id]['data_dict']['SS_PROCESSING_MESSAGES']['MOOD_SELECTION']
	await call.message.answer(mood_selection_msg[randint(0, len(mood_selection_msg) - 1)], 
		reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_MOOD_SELECTION'])


"""
Each step during 'Smart Search' has an option of going back 
	to the previous step

Basically, on each step we just change the current message text and its keyboards,
	excluding the first 'if' because it returns us to the main menu with a reply-keyboards,
	so that we have to delete the current inline-keyboards and then attach a reply-one to a
	new-written message 
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['SS_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['SS_BACK_CB']])
async def on_ss_back(call: types.CallbackQuery):

	log.info("inline_call = on_ss_back()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SMART_SEARCH'], tg_id):
		return

	if not config.users_flags[tg_id]['SS_PROCESS_FLAGS']['mood_selected']:
		"""
		Going back from 'mood' to the 'main_keyboard'
		Means user is on the step of selecting mood and wants to return to the main menu
		"""

		CommandHandler.reset_ss_constants(tg_id)

		await bot.edit_message_reply_markup(chat_id=tg_id, 
			message_id=call.message.message_id, reply_markup=None)

		on_mood_back_msg = config.users_flags[tg_id]['data_dict']['SS_BACK_MESSAGES']['ON_MOOD_SELECTION_BACK']
		await call.message.answer(on_mood_back_msg[randint(0, len(on_mood_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])

	elif not config.users_flags[tg_id]['SS_PROCESS_FLAGS']['catalogue_selected']:
		"""
		Going back from 'catalogue' to the 'mood'
		Means user on the step of selecting catalogue and wants to change his mood
		"""

		config.users_flags[tg_id]['SS_PROCESS_FLAGS']['mood_selected'] = False

		on_ss_catalogue_back_msg = config.users_flags[tg_id]['data_dict']['SS_BACK_MESSAGES']['ON_CATALOGUE_SELECTION_BACK']
		await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id, 
			text=on_ss_catalogue_back_msg[randint(0, len(on_ss_catalogue_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_MOOD_SELECTION'])

	elif not config.users_flags[tg_id]['SS_PROCESS_FLAGS']['genre_selected']:
		"""
		Going back from 'genre' to the 'catalogue'
		Means user on the step of selecting genre and wants to change his catalogue
		"""

		config.users_flags[tg_id]['SS_PROCESS_FLAGS']['catalogue_selected'] = False

		on_ss_genre_back_msg = config.users_flags[tg_id]['data_dict']['SS_BACK_MESSAGES']['ON_GENRE_SELECTION_BACK']
		await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id, 
			text=on_ss_genre_back_msg[randint(0, len(on_ss_genre_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_CATALOGUE_SELECTION'])

	elif config.users_flags[tg_id]['SS_PROCESS_FLAGS']['mood_selected'] == True and \
		config.users_flags[tg_id]['SS_PROCESS_FLAGS']['catalogue_selected'] == True and \
		config.users_flags[tg_id]['SS_PROCESS_FLAGS']['genre_selected'] == True:
		"""
		Going back from 'summing_up' to the 'genre'
		Means user on the step of summing up and wants to change his genre
		"""

		config.users_flags[tg_id]['SS_PROCESS_FLAGS']['genre_selected'] = False

		on_summary_back_msg = config.users_flags[tg_id]['data_dict']['SS_BACK_MESSAGES']['ON_SUMMARY_SELECTION_BACK']
		await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id, 
			text=on_summary_back_msg[randint(0, len(on_summary_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SS_GENRE_SELECTION'])


""" 
-----------------------------------------------------------------

'/settings'

----------------------------------------------------------------- 
"""	


"""When user wants to go back from settings-menu, we redirect him to the main-menu"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['SettingsMenu']['SETTINGS_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['SettingsMenu']['SETTINGS_BACK_CB']])
async def on_settings_back(call: types.CallbackQuery):

	log.info("inline_call = on_settings_back()")
	tg_id = call.from_user.id
	
	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ARE_SETTINGS'], tg_id):
		return

	config.users_flags[tg_id]['ARE_SETTINGS'] = False
	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	to_main_menu_msg = config.users_flags[tg_id]['data_dict']['TO_MAIN_MENU']
	await call.message.answer(to_main_menu_msg[randint(0, len(to_main_menu_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])


""" 
-----------------------------------------------------------------

'admin-mode'

----------------------------------------------------------------- 
"""	


"""Sends the next feedback from the 'feedbacks' table"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_CB'],
	data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['NEXT_FEEDBACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['NEXT_FEEDBACK_CB']])
async def process_admin_next_feedback(call: types.CallbackQuery):

	log.info("inline_call = process_admin_next_feedback()")
	tg_id = call.from_user.id

	first_feedback = False

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	if config.users_flags[tg_id]['IS_ADMIN_FEEDBACKS']: 
		"""If is not the same offer, so we delete the previous one"""
		config.BotDB.drop_and_redirect_feedback(tg_id)
	else: 
		"""The admin clicked on 'FEEDBACKS_BTN' and it's the first movie offer that he looked at"""
		config.users_flags[tg_id]['IS_ADMIN_FEEDBACKS'] = True
		first_feedback = True

	full_message = config.BotDB.get_new_feedback(tg_id)
	if not full_message:
		await drop_bot_msg(call)
		config.users_flags[tg_id]['IS_ADMIN_FEEDBACKS'] = False

		if first_feedback:
			"""The admin clicked on 'FEEDBACKS_CB' but no movies in the db"""
			no_feedbacks_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['NO_FEEDBACKS']
			await call.message.answer(no_feedbacks_msg[randint(0, len(no_feedbacks_msg) - 1)])
			first_feedback = False

		else:
			"""The db wasn't empty and the admin looked at some movie offers"""
			feedbacks_ran_out_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['FEEDBACKS_RAN_OUT']
			await call.message.answer(feedbacks_ran_out_msg[randint(0, len(feedbacks_ran_out_msg) - 1)])

		await asyncio.sleep(1)
		admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
		await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])
		
		return

	try:
		await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id, text=full_message, 
			reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_MOVIE_FEEDBACKS'], parse_mode='html')
	
	except MessageNotModified:
		"""In case if feedbacks are exactly the same"""

		await drop_bot_msg(call)
		await call.message.answer(full_message, reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_MOVIE_FEEDBACKS'],
			parse_mode='html')

	first_feedback = False


"""Get back from sending feedbacks to the main admin menu"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_BACK_CB']])
async def on_admin_feedback_back(call: types.CallbackQuery):

	log.info("inline_call = on_admin_feedback_back()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return
	
	await drop_bot_msg(call)
	config.users_flags[tg_id]['IS_ADMIN_FEEDBACKS'] = False

	admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
	await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""
When an admin selects movie offers
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['OFFERS_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['OFFERS_CB']])
async def process_admin_offers(call: types.CallbackQuery):

	log.info("inline_call = process_admin_offers()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	if await MovieFormat.is_movie_offer(call, bot):
		"""If there are movies in the dict"""

		config.users_flags[tg_id]['IS_ADMIN_OFFERS'] = True
		config.users_flags[tg_id]['SELECTING_OFFERS'] = True

		await bot.edit_message_reply_markup(chat_id=tg_id, 
			message_id=call.message.message_id, reply_markup=None)

		await MovieFormat.send_movie_offer(call, tg_id)
		

"""
When an admin selects a movie from offers and accepts one
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['ACCEPT_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['ACCEPT_CB']])
async def process_admin_offers_accept(call: types.CallbackQuery):

	log.info("inline_call = process_admin_offers_accept()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	user_tg_id = config.BotDB.get_tg_id_from_movie_offer()

	movie_accepted_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['MOVIE_ACCEPTED']
	await bot.send_message(user_tg_id, movie_accepted_msg[randint(0, len(movie_accepted_msg) - 1)])

	config.BotDB.drop_movie_offer(tg_id)

	if await MovieFormat.is_movie_offer(call ,bot):
		await drop_bot_msg(call)
		await MovieFormat.send_movie_offer(call, tg_id)


"""
When an admin selects a movie from offers and cancels one
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['CANCEL_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['CANCEL_CB']])
async def process_admin_offers_cancel(call: types.CallbackQuery):

	log.info("inline_call = process_admin_offers_cancel()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return
		
	user_tg_id = config.BotDB.get_tg_id_from_movie_offer()

	movie_canceled_msg = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['MOVIE_CANCELED']
	await bot.send_message(user_tg_id, movie_canceled_msg[randint(0, len(movie_canceled_msg) - 1)])

	config.BotDB.drop_movie_offer(tg_id)

	if await MovieFormat.is_movie_offer(call ,bot):
		await drop_bot_msg(call)
		await MovieFormat.send_movie_offer(call, tg_id)


"""
When an admin selects a movie from offers and cancels one
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['MOVIE_OFFERS_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['MOVIE_OFFERS_BACK_CB']])
async def on_admin_offers_back(call: types.CallbackQuery):

	log.info("inline_call = on_admin_offers_back()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	await drop_bot_msg(call)

	admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
	await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""
When an admin adds a movie to the DB"
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['ADD_ADMIN_MOVIE_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['ADD_ADMIN_MOVIE_CB']])
async def process_add_admin_movie(call: types.CallbackQuery):

	log.info("inline_call = process_add_admin_movie()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	config.users_flags[tg_id]['IS_OFFERING_MOVIE'] = True

	await call.message.answer(config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['ADDING_ADMIN_MOVIE_FORMAT'], 
		parse_mode='html', reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['ADDING_ADMIN_MOVIE_EXIT'])


"""
When an admin wants to update the DB (add new movies from google sheet)"
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['UPDATE_DB_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['UPDATE_DB_CB']])
async def process_admin_update_db(call: types.CallbackQuery):

	log.info("inline_call = process_admin_update_db()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	if config.GoogleSheetHandler.is_updated():
		
		new_movies = config.GoogleSheetHandler.get_new_movies()
		for new_movie in new_movies:
			config.BotDB.add_movie(list(new_movie.values())[1:])

		db_updated_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['DB_UPDATED']
		await call.message.answer(db_updated_msg[randint(0, len(db_updated_msg) - 1)])

	else:
		await drop_bot_msg(call)

		db_not_updated_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['DB_NOT_UPDATED']
		await call.message.answer(db_not_updated_msg[randint(0, len(db_not_updated_msg) - 1)])


	await asyncio.sleep(1)
	admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
	await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""
Send an excel file with the data to the admin
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['EXCEL_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['EXCEL_CB']])
async def process_admin_excel(call: types.CallbackQuery):

	log.info("inline_call = process_admin_excel()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	users_search_history = config.BotDB.get_users_search_history()
	users_feedback_history = config.BotDB.get_users_old_feedbacks_data()
	if users_search_history or users_feedback_history:
		"""There are records in the 'user_search_history' table"""

		excel_file_name = config.xlsx_handler.write_data(users_search_history, users_feedback_history)
		await drop_bot_msg(call)

		with open(excel_file_name, 'rb') as doc:
			await bot.send_document(call.message.chat.id, document=doc)

		await asyncio.sleep(0.5)
		excel_sending_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['EXCEL_SENDING']
		await call.message.answer(excel_sending_msg[randint(0, len(excel_sending_msg) - 1)])

		await asyncio.sleep(1)
		admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
		await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])
	
	else:
		"""No records yet (no one hasn't used Smart search yet)"""

		await drop_bot_msg(call)

		no_excel_sending_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['NO_EXCEL_SENDING']
		await call.message.answer(no_excel_sending_msg[randint(0, len(no_excel_sending_msg) - 1)])

		await asyncio.sleep(1)
		admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
		await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])


"""
Exit admin mode
If the user tries to enter this text and he's not an admin, some
	previous elif-block checks it
"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['AdminSelection']['EXIT_ADMIN_MODE_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['AdminSelection']['EXIT_ADMIN_MODE_CB']])
async def on_admin_back(call: types.CallbackQuery):

	log.info("inline_call = on_admin_back()")
	tg_id = call.from_user.id
	
	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'], tg_id):
		return

	config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_ADMIN_MODE'] = False
	config.users_flags[tg_id]['ON_ADMIN_MODE']['IS_OFFERING_MOVIE'] = False
	
	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	admin_farewell_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_FAREWELL']
	await call.message.answer(admin_farewell_msg[randint(0, len(admin_farewell_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])


""" 
-----------------------------------------------------------------

'Send feedback'

----------------------------------------------------------------- 
"""	


"""
During selecting his verdict about a movie in Send feedback,
now user selects his general opinion about the movie
"""
@dp.callback_query_handler(text=list(data_provider['english']['InlineKeyboardCallbacks']['SFVerdict'].values()) +
	list(data_provider['russian']['InlineKeyboardCallbacks']['SFVerdict'].values()))
async def process_sf_verdict(call: types.CallbackQuery):

	log.info('inline_call = process_sf_verdict()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'], tg_id):
		return

	config.users_flags[tg_id]['SF_PROCESS_FLAGS']['verdict_selected'] = True

	config.users_flags[tg_id]['FEEDBACK_DICT']['verdict'] = list(config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SFVerdict'].values())[list(config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SFVerdict'].values()).index(call.data)][:-1]

	comment_writings_msg = config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['COMMENT_WRITING']
	await call.message.edit_text(text=comment_writings_msg[randint(0, len(comment_writings_msg) - 1)], reply_markup=None)


"""User goes back from movie selection to the main menu (Send feedback)"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['SF_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['SF_BACK_CB']])
async def on_sf_back(call: types.CallbackQuery):

	log.info('inline_call = on_sf_back()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'], tg_id):
		return


	if not config.users_flags[tg_id]['SF_PROCESS_FLAGS']['movie_selected']:
		"""
		Going back to main-menu

		When user must select a movie name, he clicks on 'back' and we get him to the main menu
		"""

		CommandHandler.reset_sf_constants(tg_id)

		await bot.edit_message_reply_markup(chat_id=tg_id, 
			message_id=call.message.message_id, reply_markup=None)
		
		on_movie_selection_back_msg = config.users_flags[tg_id]['data_dict']['SF_BACK_MESSAGES']['ON_MOVIE_SELECTION_BACK']
		await call.message.answer(on_movie_selection_back_msg[randint(0, len(on_movie_selection_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])

		config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] = False

	elif not config.users_flags[tg_id]['SF_PROCESS_FLAGS']['verdict_selected']:
		"""
		Going back to the selection of a movie name
		User clicks on 'back' when he selects the verdict, we get him to the selection of a movie name
		"""
		
		config.users_flags[tg_id]['SF_PROCESS_FLAGS']['movie_selected'] = False

		on_verdict_selection_back_msg = config.users_flags[tg_id]['data_dict']['SF_BACK_MESSAGES']['ON_VERDICT_SELECTION_BACK']
		await bot.edit_message_text(chat_id=tg_id, message_id=call.message.message_id,
			text=on_verdict_selection_back_msg[randint(0, len(on_verdict_selection_back_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SF_MOVIE_SELECTION'])


""" 
-----------------------------------------------------------------

'We recommend'

----------------------------------------------------------------- 
"""	


"""User clicks on the 'Next one' btn during 'We recommend'"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['WeRecommend']['WR_NEXT_MOVIE_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['WeRecommend']['WR_NEXT_MOVIE_CB']])
async def process_wr_next_movie(call: types.CallbackQuery):

	log.info("inline_call = process_wr_next_movie()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'], tg_id):
		return

	config.users_flags[tg_id]['wr_movies']['counter'] += 1

	if config.users_flags[tg_id]['wr_movies']['counter'] == len(config.users_flags[tg_id]['wr_movies']['movies']) - 1:
		
		await call.message.edit_text(text=config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][0],
			reply_markup=config.users_flags[tg_id]['keyboards'].get_wr_movies_end_keyboard(tg_id, config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][1]), parse_mode='html')

	else:
		await call.message.edit_text(text=config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][0],
			reply_markup=config.users_flags[tg_id]['keyboards'].get_wr_next_movie_keyboard(tg_id, config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][1]), parse_mode='html')
		

"""User clicks on the 'Previous one' btn during 'We recommend'"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['WeRecommend']['WR_PREVIOUS_MOVIE_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['WeRecommend']['WR_PREVIOUS_MOVIE_CB']])
async def process_wr_previous_movie(call: types.CallbackQuery):

	log.info("inline_call = process_wr_previous_movie()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'], tg_id):
		return

	config.users_flags[tg_id]['wr_movies']['counter'] -= 1
	if config.users_flags[tg_id]['wr_movies']['counter'] == 0:
		
		await call.message.edit_text(text=config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][0],
			reply_markup=config.users_flags[tg_id]['keyboards'].get_wr_movies_start_keyboard(tg_id, config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][1]), parse_mode='html')

	else:
		await call.message.edit_text(text=config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][0],
			reply_markup=config.users_flags[tg_id]['keyboards'].get_wr_next_movie_keyboard(tg_id, config.users_flags[tg_id]['wr_movies']['movies'][config.users_flags[tg_id]['wr_movies']['counter']][1]), parse_mode='html')
		
		
"""User goes back from 'We recommend' to main-menu"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']["WeRecommend"]['WR_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']["WeRecommend"]['WR_BACK_CB']])
async def on_wr_back(call: types.CallbackQuery, is_btn_watched=False):

	log.info('inline_call = on_wr_back()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'], tg_id):
		return

	config.users_flags[tg_id]['MM_FLAGS']['IS_WE_RECOMMEND'] = False
	config.users_flags[tg_id]['wr_movies']['movies'] = None
	config.users_flags[tg_id]['wr_movies']['counter'] = 0

	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	to_main_menu_msg = config.users_flags[tg_id]['data_dict']['TO_MAIN_MENU']
	await call.message.answer(to_main_menu_msg[randint(0, len(to_main_menu_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])


""" 
-----------------------------------------------------------------

'No preferences'

----------------------------------------------------------------- 
"""	


"""User wants the next movie in 'No preferences'"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['NP_NEXT_MOVIE_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['NP_NEXT_MOVIE_CB']])
async def process_np_next_movie(call: types.CallbackQuery):

	log.info("inline_call = process_np_next_movie()")
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'], tg_id):
		return

	movie_msg = None
	while True:
		rand_movie = config.BotDB.get_np_random_movie(tg_id)

		if config.users_flags[tg_id]['NO_MOVIES_LEFT']:

			no_movies_left_msg = config.users_flags[tg_id]['data_dict']['NP_PROCESSING_MESSAGES']['NO_MOVIES_LEFT']
			await call.message.edit_text(text=no_movies_left_msg[randint(0, len(no_movies_left_msg) - 1)], reply_markup=None)

			await asyncio.sleep(1.5)
			to_main_menu_msg = config.users_flags[tg_id]['data_dict']['TO_MAIN_MENU']
			await call.message.answer(to_main_menu_msg[randint(0, len(to_main_menu_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])

			config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] = False
			config.users_flags[tg_id]['selected_movies'] = []
			return

		else: 
			movie_msg = MovieFormat.get_np_movie_format(rand_movie)
			break

	await call.message.edit_text(text=movie_msg, reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['NP_NEXT_MOVIE'])


"""User goes back from 'No preferences' to main-menu"""
@dp.callback_query_handler(text=[data_provider['english']['InlineKeyboardCallbacks']['NP_BACK_CB'],
	data_provider['russian']['InlineKeyboardCallbacks']['NP_BACK_CB']])
async def on_np_back(call: types.CallbackQuery):

	log.info('inline_call = on_np_back()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'], tg_id):
		return

	config.users_flags[tg_id]['MM_FLAGS']['IS_NO_PREFERENCES'] = False
	config.users_flags[tg_id]['selected_movies'] = []

	await bot.edit_message_reply_markup(chat_id=tg_id, 
		message_id=call.message.message_id, reply_markup=None)

	to_main_menu_msg = config.users_flags[tg_id]['data_dict']['TO_MAIN_MENU']
	await call.message.answer(to_main_menu_msg[randint(0, len(to_main_menu_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].REPLY_KEYBOARDS['MAIN_MENU_SELECTION'])


"""
This function catches all the callbacks that weren't catched by the functions above
In 'Send feedback' user confirms the movies he watched and gives a review, all this
	he does through inline-keyboard, so we catch his clicks on btns here
"""
@dp.callback_query_handler(lambda query: True)
async def inline_checkout(call: types.CallbackQuery):

	log.info('inline_call = inline_checkout()')
	tg_id = call.from_user.id

	if await CommandHandler.is_inline_old(call, config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'], tg_id):
		return


	if config.users_flags[tg_id]['MM_FLAGS']['IS_SEND_FEEDBACK'] and not config.users_flags[tg_id]['SF_PROCESS_FLAGS']['movie_selected']:
		"""User selected a movie name in 'Send feedback'"""

		config.users_flags[tg_id]['SF_PROCESS_FLAGS']['movie_selected'] = True
		config.users_flags[tg_id]['FEEDBACK_DICT']['watched_movie'] = call.data

		sf_verdict_msg = config.users_flags[tg_id]['data_dict']['SF_PROCESSING_MESSAGES']['VERDICT_SELECTION']
		await call.message.edit_text(text=sf_verdict_msg[randint(0, len(sf_verdict_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['SF_VERDICT_SELECTION'])


async def drop_bot_msg(call: types.CallbackQuery):
	"""Removes the last bot message"""
	await bot.delete_message(chat_id=call.from_user.id, 
		message_id=call.message.message_id)

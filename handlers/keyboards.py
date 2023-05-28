
"""
Contains all the keyboards as constants

When the bot is launched for the first time, all the keyboards in 'REPLY_KEYBOARDS' and 
	'INLINE_KEYBOARDS' are None, except for 'LANGUAGE_SELECTION' that doesn't depend on a
	specific language. They're all set by the setter that is called every time the language
	is changed. By the time we send the user first 'welcome message', he'll have already
	selected his preffered language

"""
import config
from config import data_provider
from aiogram.types import (
	ReplyKeyboardMarkup, 
	KeyboardButton, 
	InlineKeyboardMarkup, 
	InlineKeyboardButton
)


class KeyBoard:
	"""Contains all reply- and inline-keyboards and the methods to override them"""

	def __init__(self):

		"""
		REPLY-KEYBOARDS
		-----------------------
		LANGUAGE_SELECTION_ATLAUNCH ->  	Appears at the first start and when user wants to change his language at 
												runtime. It's set at once and outside the methods because it doesn't 
												require a specific language
		MAIN_MENU_SELECTION ->             	Sets up the main basic reply-keyboard where user has 4 selections
		OFFERING_MOVIE_EXIT ->        		When user offers his movies, he cannot enter any other command or text, the bot
												won't react to it, so to leave this mode there's a btn
		ADDING_ADMIN_MOVIE_EXIT ->			When the admin adds a movie to the DB, he cannot enter any other command or text, 
												the bot won't react to it, so to leave this mode there's a btn       
		"""
		self.REPLY_KEYBOARDS = \
		{
			'LANGUAGE_SELECTION_ATLAUNCH': \
				ReplyKeyboardMarkup(
					keyboard=[
						[
							KeyboardButton(data_provider['english']['ENG_LANG_BTN'])
						],
						[
							KeyboardButton(data_provider['russian']['RUS_LANG_BTN'])
						]
					],
					resize_keyboard=True,
					one_time_keyboard=True
				),

			'MAIN_MENU_SELECTION': None,
			'OFFERING_MOVIE_EXIT': None,
			'ADDING_ADMIN_MOVIE_EXIT': None
		}

		"""
		INLINE-KEYBOARDS
		-----------------------
		SS_MOOD_SELECTION ->           	User's mood selection in 'Smart Search'
		SS_CATALOGUE_SELECTION ->       User's catalogue selection in 'Smart Search'
		SS_GENRE_SELECTION ->           User's genre selection in 'Smart Search'
		SS_MORE_GENRE_SELECTION ->      User's clicks the 'more' btn and a new keyboard with more genres pops up
		SS_SUMMARY_VERIFICATION ->      Sets up inline-keyboard for verification user's selections from
											'Smart Search', if he wants to make some changes
		SETTINGS_MENU ->				A keyboard for the 'settings' cmd-command
		ADMIN_SELECTION ->				Exit btn for admins to leave the admin-mode
		SF_MOVIE_SELECTION ->           When user wants to send feedback, he must confirm what movies
											he exactly watched
		ADMIN_MOVIE_OFFERING ->			During admin-mode an admin selects 'See post' and accepts/cancels user's 
											offered movies			
		SF_VERDICT_SELECTION ->   		User selects his general opinion about the watched movie	
		SF_GOOGLE_FORM ->				A keyboard for the case when the user selects 'Send feedback' but there are no
											movies to send feedback on for the time being, so that he can fill in the form
		NP_NEXT_MOVIE ->				'No idea' case, where user can switch to the next movie or go back to the main menu
		"""
		self.INLINE_KEYBOARDS = \
		{
			'SS_MOOD_SELECTION': None,
			'SS_CATALOGUE_SELECTION': None,
			'SS_GENRE_SELECTION': None,
			'SS_MORE_GENRE_SELECTION': None,
			'SS_SUMMARY_VERIFICATION': None,
			'SETTINGS_MENU': None,
			'ADMIN_SELECTION': None,
			'SF_MOVIE_SELECTION': None,
			'ADMIN_MOVIE_OFFERING': None,
			'ADMIN_MOVIE_FEEDBACKS': None,
			'SF_VERDICT_SELECTION': None,
			'SF_GOOGLE_FORM': None,
			'NP_NEXT_MOVIE': None
		}


	def get_wr_movies_start_keyboard(self, tg_id, viewing_link):
		"""
		During 'We recommend' in personal_actions.py and in callbacks.py

		The keyboards are changing according to whether there is only last movie to show
			or we're at the beginning of the list and now we can go only 'next'
		This method needs for the beginning, where we can go only 'next'
		"""

		return InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_VIEW_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_VIEW_MOVIE_CB'], url=viewing_link),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['WeRecommend']['WR_NEXT_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['WeRecommend']['WR_NEXT_MOVIE_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_BACK_CB'])
					]
				]
			)

	def get_wr_next_movie_keyboard(self, tg_id, viewing_link):
		"""
		During 'We recommend' in callbacks.py
		
		At this point we can go whether 'next' or 'previous'
		"""

		return InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['WeRecommend']['WR_PREVIOUS_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['WeRecommend']['WR_PREVIOUS_MOVIE_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['WeRecommend']['WR_NEXT_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['WeRecommend']['WR_NEXT_MOVIE_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_VIEW_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_VIEW_MOVIE_CB'], url=viewing_link),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_BACK_CB'])
					]
				]
			)

	def get_wr_movies_end_keyboard(self, tg_id, viewing_link):
		"""
		During 'We recommend' in callbacks.py
		
		Here we're at the end of the list, now we can go only 'previous'
		"""

		return InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_VIEW_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_VIEW_MOVIE_CB'], url=viewing_link),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['WeRecommend']['WR_PREVIOUS_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['WeRecommend']['WR_PREVIOUS_MOVIE_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']["WeRecommend"]['WR_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']["WeRecommend"]['WR_BACK_CB'])
					]
				]
			)


	def reset_keyboards(self, tg_id):
		"""
		Used in the 'LanguageSwitcher' class during changing the language in personal_actions.py
			in the 'cmd_lang()' and 'filter_lang_selection()' functions
		
		Check what language the user selected and assign the right lang-dict from 
			'data_provider' that contains both dictionaries(with two languages)
		"""

		self.REPLY_KEYBOARDS['MAIN_MENU_SELECTION'] = \
			ReplyKeyboardMarkup(
				keyboard=[
					[
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SMART_SEARCH_BTN']),
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MainMenuButtons']['WE_RECOMMEND_BTN']),
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MainMenuButtons']['NO_PREFERENCES_BTN'])
					],
					[
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MainMenuButtons']['SEND_FEEDBACK_BTN'])
					]
				],
				resize_keyboard=True,
				one_time_keyboard=True
			)

		self.REPLY_KEYBOARDS['OFFERING_MOVIE_EXIT'] = \
			ReplyKeyboardMarkup(
				keyboard=[
					[
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MOVIE_OFFERING_BACK_BTN'])
					]
				],
				resize_keyboard=True,
				one_time_keyboard=True
			)

		self.REPLY_KEYBOARDS['ADDING_ADMIN_MOVIE_EXIT'] = \
			ReplyKeyboardMarkup(
				keyboard=[
					[
						KeyboardButton(config.users_flags[tg_id]['data_dict']['MOVIE_ADDING_BACK_BTN'])
					]
				],
				resize_keyboard=True,
				one_time_keyboard=True
			)

		self.INLINE_KEYBOARDS['SS_MOOD_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['DEPRESSION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['DEPRESSION_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['CHEERFUL_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['CHEERFUL_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['FIGHTING_SPIRIT_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['FIGHTING_SPIRIT_CB']),
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['FAMILY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['FAMILY_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['FRIENDS_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['FRIENDS_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['UserMood']['LOVE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['UserMood']['LOVE_CB']),
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SS_BACK_CB'])
					]
				]	
			)

		self.INLINE_KEYBOARDS['SS_CATALOGUE_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Catalogue']['MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Catalogue']['MOVIE_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Catalogue']['SERIES_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Catalogue']['SERIES_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['SS_GENRE_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['COMEDY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['COMEDY_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['DRAMA_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['DRAMA_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['MELODRAMA_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['MELODRAMA_CB']),
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['THRILLER_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['THRILLER_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['ACTION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['ACTION_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['FICTION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['FICTION_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SS_BACK_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['MORE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['MORE_CB']),
					]	
				]
			)

		self.INLINE_KEYBOARDS['SS_MORE_GENRE_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['COMEDY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['COMEDY_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['DRAMA_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['DRAMA_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['MELODRAMA_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['MELODRAMA_CB']),
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['THRILLER_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['THRILLER_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['ACTION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['ACTION_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['Main']['FICTION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['Main']['FICTION_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['FAMILY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['FAMILY_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['DETECTIVE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['DETECTIVE_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['SPORT_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['SPORT_CB']),
					],
					[	
						
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['FANTASY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['FANTASY_CB']),		
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['ANIMATION_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['ANIMATION_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['ADVENTURE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['ADVENTURE_CB'])	
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['BIOGRAPHY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['BIOGRAPHY_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['CRIMINAL_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['CRIMINAL_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['MUSIC_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['MUSIC_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['DOCUMENTARY_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['DOCUMENTARY_CB']),					
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['Genre']['More']['WAR_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['Genre']['More']['WAR_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['SS_SUMMARY_VERIFICATION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SSConfirmation']['YES_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SSConfirmation']['YES_CB']), 
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SSConfirmation']['NO_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SSConfirmation']['NO_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['SETTINGS_MENU'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SettingsMenu']['SETTINGS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SettingsMenu']['SETTINGS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['ADMIN_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['FEEDBACKS_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['OFFERS_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['OFFERS_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['ADD_ADMIN_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['ADD_ADMIN_MOVIE_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['EXCEL_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['EXCEL_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['UPDATE_DB_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['UPDATE_DB_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['EXIT_ADMIN_MODE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['EXIT_ADMIN_MODE_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['ADMIN_MOVIE_OFFERING'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['ACCEPT_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['ACCEPT_CB']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['CANCEL_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['CANCEL_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['MOVIE_OFFERS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['MOVIE_OFFERS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['ADMIN_MOVIE_FEEDBACKS'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['NEXT_FEEDBACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['NEXT_FEEDBACK_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['AdminSelection']['FEEDBACKS_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['AdminSelection']['FEEDBACKS_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['SF_VERDICT_SELECTION'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SFVerdict']['NOT_BAD_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SFVerdict']['NOT_BAD_BTN']),
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SFVerdict']['GOOD_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SFVerdict']['GOOD_BTN'])	
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SFVerdict']['DONT_KNOW_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SFVerdict']['DONT_KNOW_BTN'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SF_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SF_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['SF_GOOGLE_FORM'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SF_GOOGLE_FORM_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SF_GOOGLE_FORM_CB'], url=config.users_flags[tg_id]['data_dict']['GOOGLE_FORM_LINK'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SF_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SF_BACK_CB'])
					]
				]
			)

		self.INLINE_KEYBOARDS['NP_NEXT_MOVIE'] = \
			InlineKeyboardMarkup(
				inline_keyboard=[
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['NP_NEXT_MOVIE_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['NP_NEXT_MOVIE_CB'])
					],
					[
						InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['NP_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['NP_BACK_CB'])
					]
				]
			)


	def set_sf_movies_keyboard(self, tg_id):
		"""
		During 'Send feedback' in personal_actions.py in the 'filter_send_feedback()' function

		A keyboard for user to select what movies he watched
		"""

		movie_list = []

		def add_inline_btn(index, is_add=True):
			"""Add one btn to the keyboard"""

			movie_name = movie_list[index]
			if is_add:
				self.INLINE_KEYBOARDS['SF_MOVIE_SELECTION'].add(InlineKeyboardButton(text=movie_name, callback_data=movie_name))
			else:
				self.INLINE_KEYBOARDS['SF_MOVIE_SELECTION'].insert(InlineKeyboardButton(text=movie_name, callback_data=movie_name))

		def set_odd_structure():
			"""How btns will be located on the keyboard if we have 1 or 3 or 5 movies"""

			self.INLINE_KEYBOARDS['SF_MOVIE_SELECTION'] = InlineKeyboardMarkup(row_width=3)
			movie_indexes = []

			for i in range(0, len(movie_list)):
				if len(movie_list[i]) > max_chars:
					movie_indexes.append(i)
				else:
					add_inline_btn(i, False)

			if len(movie_list) == 1:
				if movie_indexes: add_inline_btn(movie_indexes[0])

			elif len(movie_list) == 3:
				match len(movie_indexes):
					case 1:
						add_inline_btn(movie_indexes[0])
					case 2:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1], False)
					case 3:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1])
						add_inline_btn(movie_indexes[2], False)

			elif len(movie_list) == 5:
				match len(movie_indexes):
					case 1:
						add_inline_btn(movie_indexes[0], False)
					case 2:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1], False)
					case 3:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1], False)
						add_inline_btn(movie_indexes[2])
					case 4:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1], False)
						add_inline_btn(movie_indexes[2])
						add_inline_btn(movie_indexes[3], False)
					case 5:
						add_inline_btn(movie_indexes[0])
						add_inline_btn(movie_indexes[1], False)
						add_inline_btn(movie_indexes[2])
						add_inline_btn(movie_indexes[3], False)
						add_inline_btn(movie_indexes[4])

		def set_even_structure():
			"""If we have 2 or 4 movies"""

			self.INLINE_KEYBOARDS['SF_MOVIE_SELECTION'] = InlineKeyboardMarkup(row_width=2)
			for i in range(0, len(movie_list)):
				add_inline_btn(i, False)

		def set_movie_names():
			""" Sets the list with movie names that user has from the previous 'Smart selection' in 'user_data' """

			config.users_flags[tg_id]['user_previous_movies'] = config.BotDB.get_user_selection(tg_id)
			
			# set the mood and delete from the list
			config.users_flags[tg_id]['FEEDBACK_DICT']['mood'] = config.users_flags[tg_id]['user_previous_movies'][-1]
			config.users_flags[tg_id]['user_previous_movies'].pop()

			for name in config.users_flags[tg_id]['user_previous_movies']:
				if name != None: movie_list.append(name)


		set_movie_names()

		# set the max amount of characters that the button can contain without showing '...'		
		max_chars = None
		if config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
			max_chars = 19
		elif config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru']:
			max_chars = 16

		if len(movie_list) % 2 != 0:
			set_odd_structure()
		else:
			set_even_structure()

		self.INLINE_KEYBOARDS['SF_MOVIE_SELECTION'].add(InlineKeyboardButton(text=config.users_flags[tg_id]['data_dict']['InlineKeyboardTexts']['SF_BACK_BTN'], callback_data=config.users_flags[tg_id]['data_dict']['InlineKeyboardCallbacks']['SF_BACK_CB']))

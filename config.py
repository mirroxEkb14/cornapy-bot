
"""
Contains bot's token and all the necessesary variables/constants
that don't depend on specific language(eng/rus)
"""

from helpers.xlsx_handler import XlsxHandler
from enum import Enum
import json


"""
	add to excel - movie/series

	add_user_history() - кнопка 'посмотреть' в we_recommend (process_wr_watch_movie())

	
	выводить статистику в админ моде -> затем удалить столбец чтобы в feedbacks брались фильмы из этой таблицы

	написать в readme: 
		о delimiters в баще данных(хранение списком)
		DBTable и 'get_column_value()' создал чтобы просто потренить взаимодействие с Enum
		как подключить google sheet к проекту
"""


# database
BotDB = None

# google sheets
GoogleSheetHandler = None

# a class instance for writing the data to the excel to send the file
# to admins in admin mode 'Send excel'
xlsx_handler = XlsxHandler()


# temporary keyboard to display 'LANGUAGE_SELECTION_ATLAUNCH' at the bot launch,
# so that user can select a language
temp_keyboard = None


# gets access to the admin mode - database stats
ADMIN_COMMAND = '!admin'


# used in db.py in the 'get_movies()' method
# how many movies will be displayed to user at the end of 'Smart search'
SAMPLING_SIZE = 5


# used in 'We recommend' for links
WORD_JOINER = '&#8288'


# ids of movies that are displayed in 'We recommend'
WR_MOVIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# a blank for the message with movies that is sent at the end of 'Smart search'
MOVIE_MESSAGE = "\n\n<b>{movie_name}</b>, {movie_release_year}\n{movie_link}"


# each user has his own constants, so that the bot 
# can handle several users at the same time
users_flags = {}


# contains all the text messages in both languages
with open('data.json', encoding='utf-8') as f:
	data_provider = json.load(f)


# used when user launches the bot for the first time and he must select the language,
# these messages do not depend on a specific language, so it contains here
BOT_LANG_MESSAGES = ['At first, choose your language, please\n\nДля начала, выберите, пожалуйста, язык', 
	'For convenience, decide on the language\n\nДля удобства общения, выберите язык', 
	'The language is above all\n\nПрежде всего язык']


# sticker paths	
SMART_SELECTION_STI = 'static/smart_selection_img.webp'
NO_PREFERENCES_STIS = {
	'STI_1': 'static/np_starting/np_starting_img1.tgs',
	'STI_2': 'static/np_starting/np_starting_img2.tgs',
	'STI_3': 'static/np_starting/np_starting_img3.tgs'
}
SEND_FEEDBACK_STIS = {
	'STI_1': 'static/sf_finishing/sf_finishing_img1.webp',
	'STI_2': 'static/sf_finishing/sf_finishing_img2.tgs',
	'STI_3': 'static/sf_finishing/sf_finishing_img3.tgs'
}
BOT_WELCOME_STIS = {
	'STI_1': 'static/bot_welcome/bot_welcome_img1.webp',
	'STI_2': 'static/bot_welcome/bot_welcome_img2.webp'
}
USER_OFFERING_MOVIE_STIS = {
	'STI_RUS': 'static/offering_movie/zhdun_waiting.webp',
	'STI_ENG': 'static/offering_movie/yoda_waiting.tgs',

	"ON_MOVIE_OFFERED": {
		"STI1": "static/user_offerring_movie/on_movie_offered1.tgs",
		"STI2": "static/user_offerring_movie/on_movie_offered2.tgs",
		"STI3": "static/user_offerring_movie/on_movie_offered3.txt"
	}
}
NOT_AN_ADMIN_STIS = {
	'STI_1': 'static/not_an_admin/not_an_admin_img1.webp',
	'STI_2': 'static/not_an_admin/not_an_admin_img2.webp',
	'STI_3': 'static/not_an_admin/not_an_admin_img3.webp'
}
NO_MOVIES_STIS = {
	'STI_1': 'static/no_movies/no_movies_img1.webp',
	'STI_2': 'static/no_movies/no_movies_img2.tgs',
	'STI_3': 'static/no_movies/no_movies_img3.tgs'
}
ADMIN_WELCOME_STIS = {
	'STI_1': 'static/admin_welcome/admin_welcome_img1.webp',
	'STI_2': 'static/admin_welcome/admin_welcome_img2.webp',
	'STI_3': 'static/admin_welcome/admin_welcome_img3.webp'
}


def get_passwords():
	""" 
	Get all the content from '.env' file (tokens and passwords)
	
	*could be used 'dotenv' library, but I couldn't manage to upload the library on Heroku
	"""

	with open('.env', 'r') as f:
		f_contents = f.read()

		keys = []
		values = []
		for el in f_contents.split('\n'):

			splitted_el = el.split("=")
			keys.append(splitted_el[0])
			values.append(splitted_el[1])

		return dict(zip(keys, values))

# contains the content from .env file
PASSWORD_DICT = get_passwords()
# bot's telegram token
TOKEN = PASSWORD_DICT.get('BOT_TOKEN')


class Novelty(Enum):
	"""
	Films before 2010 included are considered as old (upper bound)
	Films after 2010 are considered as modern (lower bound)
	"""
	OLD = 2010
	MODERN = 2011

class DBTable(Enum):
	"""
	All the tables in the 'cinema' DB
	Used in db.py in the 'get_column_value()' method
	"""
	MOVIE_OFFERS = ['id', 'tg_id', 'user_offer']
	MOVIES = ['id', 'rus_name', 'rus_mood', 'rus_catalogue', 'rus_genre', 'release_year', 'rus_director', 'rus_cast', 'rus_stiryline', 'rus_link', 'eng_name', 'eng_mood', 'eng_catalogue', 'eng_genre', 'eng_director', 'eng_cast', 'eng_storyline', 'eng_link', 'details_link', 'poster_link']
	NEW_FEEDBACKS = ['id', 'tg_id', 'tg_name', 'watched_movie', 'mood', 'verdict', 'comment']
	OLD_FEEDBACKS = ['id', 'tg_id', 'tg_names', 'watched_movies', 'moods', 'verdicts', 'comments']
	USER_MOVIE_HISTORY = ['id', 'tg_id', 'movie_ids']
	USER_MOVIE_SELECTION = ['id', 'tg_id', 'movie_name1', 'movie_name2', 'movie_name3', 'movie_name4', 'movie_name5', 'mood']
	USER_MOVIE_SELECTION_HISTORY = ['id', 'tg_id', 'movie_ids']
	USER_SEARCH_HISTORY = ['id', 'tg_id', 'tg_names', 'dates', 'moods', 'catalogues', 'genres']


class AdminID(Enum):
	"""Contains the IDs of admins"""
	SERJIO_ID = int(PASSWORD_DICT.get('SERJIO_TG_ID'))
	DANCHO_ID = int(PASSWORD_DICT.get('DANCHO_TG_ID'))


def add_user(tg_id):
	"""
	Adds a new user tg_id to the dict with all the flags

	is_first_launch -> 		If it is user's first interaction with the bot or not
	IS_OFFERING_MOVIE -> 	The process when user adds a movie to the database
	ARE_SETTINGS -> 		To check if user's in settings menu
	NO_MOVIES_LEFT ->		When user was shown the whole library in 'No preferences'
	user_previous_movies -> When we display the user his previously selected movies in 'Send feedback',
								we also save them here to delete a movie that the user's making a review on
								from 'user_data', so that next time when user wants to leave feedback, this
								movie will no longer be in the list
	selected_movies -> 		When user selects 'No preferences' we gets a movie, if he doesn't like it and
								click on 'Next one', we write this selected movie so that we won't offer him it again
								used in db.py in 'get_np_random_movie()'
	data_dict ->			Contains the data in a certain language that user selected
	keyboards ->			Keyboard class instance, gets the access to the keyboards
	cur_movie_offer_index ->Used when an admin views movie offerings, it contains the movie id that the admin is
								looking at at the the moment to drop it then (to avoid a situation when the admin
								views the movie and at the same time some user adds a new offer)
	SELECTING_OFFERS -> 	A flag, When an admin selects offerings from the dict
	IS_ADMIN_FEEDBACKS ->	If the admin selects feedbacks at the moment
	IS_ADMIN_OFFERS ->		If the admin selects movie offers
	HELP_COMMAND_MESSAGE ->	Contains the message that pops up when user uses '/help' command sets along with the language
	wr_movies ->			A dict with a list of top movies and counter that says what movie must be displayed next
	SELECTED_LANGUAGE -> 	To verify if user's already selected his language, so that in the future if he typies just the
 								btn-language text, the bot doesn't change the language, user can only do it using 'settings'.
								It's set so that in each neccessary file we can check user's selected language before
 								setting keyboards, messages, callbascks
	USER_DATA -> 			User's selected mood, catalogue(movie/series) and genre
								the variables are set in 'callbacks.py' and never change
	MM_FLAGS ->				Represents the process of each reply-keyboard btn in 'personal_actions.py'
	SS_PROCESS_FLAGS ->		Used in callbacks.py for verifications to go to the next step
								'SS' -> Smart selection
	SF_PROCESS_FLAGS ->		Used in callbacks.py for verifying each user's step
								'SF' -> Send feedback
	FEEDBACK_DICT ->		When user sends feedback, he must fill in the following three fileds,
								after that the values will go to the database
	ON_ADMIN_MODE -> 		If the admin panel is on, bot ignores all the messages but only reacts to inline-buttons
	"""

	users_flags[tg_id] = {
		'is_first_launch': True,
		'IS_OFFERING_MOVIE': False,
		'ARE_SETTINGS': False,
		'NO_MOVIES_LEFT': False,
		'user_previous_movies': [],
		'selected_movies': [],
		'data_dict': None,
		'keyboards': None,
		'cur_movie_offer_index': None,
		'SELECTING_OFFERS': False,
		'IS_ADMIN_FEEDBACKS': False,
		'IS_ADMIN_OFFERS': False,
		'HELP_COMMAND_MESSAGE': None,
		'wr_movies': {
			'movies': [], 
			'counter': 0
		},
		'SELECTED_LANGUAGE': {
			'en': False,
			'ru': False
		},
		'USER_DATA': {
			'USER_MOOD': None,
			'USER_CATALOGUE': None,
			'USER_GENRE': None
		},
		'MM_FLAGS': {
			'IS_SMART_SEARCH': False,
			'IS_WE_RECOMMEND': False,
			'IS_NO_PREFERENCES': False,
			'IS_SEND_FEEDBACK': False
		},
		'SS_PROCESS_FLAGS': {
			'mood_selected': False, 
			'catalogue_selected': False, 
			'genre_selected': False
		},
		'SF_PROCESS_FLAGS': {
			'movie_selected': False,
			'verdict_selected': False
		},
		'FEEDBACK_DICT': {
			'tg_id': None,
			'tg_name': None,
			'watched_movie': None,
			'mood': None,
			'verdict': None,
			'comment': None
		},	
		'ON_ADMIN_MODE': {
			'IS_ADMIN_MODE': False,
			'FEEDBACK_USER_DATA': []
		}
	}


def user_exists(tg_id):
	"""
	If there is such a tg_id in the dict or not
	It is needed in 'filter_lang_selection()'
	"""
	return tg_id in users_flags


# set the flags for the admins
add_user(AdminID.DANCHO_ID.value)
add_user(AdminID.SERJIO_ID.value)

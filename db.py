
from config import SAMPLING_SIZE
from helpers.movie_format import MovieFormat
from datetime import date
from io import BytesIO
from config import DBTable
import requests
import json
import config
import sqlite3
import logging
import logger
import random


"""
cinema.db
	movies ->						Contains the movies
	user_movie_history ->			Contains the movies that user left feedback on (that means he watched the movie), 
										it is used in 'exclude_watched_movies()' in 'Smart Search' and to display the
										statistic to the admin in admin mode
	user_movie_selection ->			Contains the movies user selected during the previous 'Smart searct', it is
										used during 'Feedback', so that we can set movie names to the keyboard
	old_feedbacks -> 				Contains the data from 'Send feedback' that user left, the feedbacks here 
										have already been watched by admins
	new_feedbacks -> 				Contains the data from 'Send feedback' that user left, it will be used in admin mode
										to display these feedbacks, then they will be replaced to the 'old_feedbacks' table
	movie_offers ->					Contains the data from '/offermovie' command that user enters, it is used
										in admin mode to display these offers
	user_search_history ->			Contains the data from 'Smart Search', it is used in admin mode to display
										these data to the admin as 'what a certain user selected in his each
										Smart search'
	user_movie_selection_history ->	Contains the movies from each 'Smart search' that the user ever had, then used
										in 'exclude_watched_movies()' during 'Smart Search' not to show the movies
										that have already been shown in smart search selection
"""

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name = 'logger/db.log')

class BotDB:

	def __init__(self, db_file):
		"""Initializing a database connection"""

		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()
		self.OLD_FEEDBACKS_DELIMITER = "|"
		self.USER_SEARCH_HISTORY_DELIMITER = ", "
		self.USER_MOVIE_SELECTION_HISTORY_DELIMITER = ", "

	def close(self):
		"""Closing the database connection"""
		self.conn.close()

	def get_column_value(self, table_name: str, column_name: str, where_column_name: str, where_column_value: str):
		"""
		Get a value from a certain column from a certain table from the 'cinema' database
		Used ...

		:param str table_name: Table that contains the column that contains the value to be found
	    :param str column_name: Column that contains the value that must be found
	    :param str where_column_name: Column by which we find the necessary row in the table
	    :param str where_column_value: Value that is in the column by which we find the necessary row
		"""

		log.info('db_call = get_column_value()')

		def check_table_name() -> bool:
			"""If such a table exists in DB with the name of the passed parameter"""
			return table_name in [constant_name.name.lower() for constant_name in list(DBTable)]

		def check_column_name() -> bool:
			"""If a column with the passed name really is in the table"""
			return column_name in DBTable[table_name.upper()].value

		def check_where_column_name() -> bool:
			return where_column_name in DBTable[table_name.upper()].value


		if not check_table_name():
			log.error('db_nested_call = check_table_name(): Incorrect table name')
			return None
		elif not check_column_name():
			log.error('db_nested_call = check_column_name(): Incorrect column name')
			return None
		elif not check_where_column_name():
			log.error('db_nested_call = check_where_column_name(): Incorrect where_column name')
			return None

		db_column_value = self.cursor.execute('SELECT {column_name} FROM {table_name} WHERE {where_column_name} = ?'
			.format(column_name=column_name, table_name=table_name, where_column_name=where_column_name), (where_column_value,))
		column_value = db_column_value.fetchone()[0]
		return column_value


	""" 
	-----------------------------------------------------------------

	The 'movies' table

	----------------------------------------------------------------- 
	"""	

	def get_movie_by_id(self, movie_id):
		"""
		Used in here in the 'get_wr_movies()' function

		Returns the dict with all the movie data from the 'movies' table
		"""

		log.info('db_call = get_movie_by_id()')

		categories = ['id', 'rus_name', 'rus_mood', 'rus_catalogue', 'rus_genre', 'release_year', 'rus_director', 'rus_cast', 'rus_storyline', 'rus_link', 'eng_name', 'eng_mood', 'eng_catalogue', 'eng_genre', 'eng_director', 'eng_cast', 'eng_storyline', 'eng_link', 'details_link', 'poster_link']
		
		db_movie_data = self.cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
		movie_data = list(db_movie_data.fetchone())

		"""
		Return value ->
		{
			'id': 1, 'rus_name': 'Интерстеллар', 'rus_mood': 'Депрессия', 'rus_catalogue': 'Фильм', 
			'rus_genre': 'Фантастика/Драма/Приключение', 'release_year': 2014, 'rus_director': 'Кристофер Нолан', 
			'rus_cast': 'Мэттью МакКонахи, Энн Хэтэуэй, Майкл Кейн, Мэтт Дэймон', 'rus_storyline': '...', 
			'rus_link': 'https://...', 'eng_name': 'Interstellar', 'eng_mood': 'Depression', 'eng_catalogue': 'Movie', 
			'eng_genre': 'Fiction/Drama/Adventure', 'eng_link': 'https://...', 'details_link': 'https://...', 
			'poster_link': 'https://...'
		}
		"""
		return {category: movie for category, movie in zip(categories, movie_data)}

	def add_movie(self, movie_list):
		"""
		Used in personal_actions.py in the 'filter_adding_admin_movie()' and 'process_admin_update_db()' functions
		Add a movie/movies to the database

		:param movie_list = [
								'Ешь, молись, люби', 
								'Депрессия', 
								'Фильм', 
								...
							]
		"""

		log.info('db_call = add_movie()')

		self.cursor.execute("INSERT INTO 'movies' ('rus_name', 'rus_mood', 'rus_catalogue', 'rus_genre', 'release_year', 'rus_director', 'rus_cast', 'rus_storyline', 'rus_link', 'eng_name', 'eng_mood', 'eng_catalogue', 'eng_genre', 'eng_director', 'eng_cast', 'eng_storyline' ,'eng_link', 'details_link', 'poster_link') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
			(movie_list[0], movie_list[1], movie_list[2], movie_list[3], movie_list[4], movie_list[5], movie_list[6], movie_list[7], movie_list[8], movie_list[9], movie_list[10], movie_list[11], movie_list[12], movie_list[13], movie_list[14], movie_list[15], movie_list[16], movie_list[17], movie_list[18]))

		return self.conn.commit()

	def get_movies(self, tg_id, user_mood, user_catalogue, user_genre):
		"""
		Used in callbacks.py in the 'process_ss_yes()' function
		Takes a certain amount of movies from the database that match all the passed parameters

		:param db_movies_all = [
								(27, 'Дэдпул', 2016, 'https://...'), 
								(28, 'Дэдпул 2', 2018, 'https://...')
							   ]
		"""

		log.info('db_call = get_movies()')
		db_movies_five = None
		
		db_sampling = None
		match config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
			case True:	
				db_sampling = self.cursor.execute("SELECT id, eng_name, release_year, eng_link FROM movies WHERE eng_mood LIKE ? AND eng_catalogue = ? AND eng_genre LIKE ?", (f'%{user_mood}%', user_catalogue, f'%{user_genre}%',))
			case False:
				db_sampling = self.cursor.execute("SELECT id, rus_name, release_year, rus_link FROM movies WHERE rus_mood LIKE ? AND rus_catalogue = ? AND rus_genre LIKE ?", (f'%{user_mood}%', user_catalogue, f'%{user_genre}%',))

		db_movies_all = db_sampling.fetchall()
		editted_movies = self.exclude_watched_movies(tg_id, db_movies_all)

		if len(editted_movies) >= SAMPLING_SIZE:
			db_movies_five = random.sample(editted_movies, SAMPLING_SIZE)
			return db_movies_five

		return editted_movies

	def get_movies_last_id(self):
		"""
		Used in google_sheet_handler.py in the 'is_updated()' function
		Gets the id of the last movie in the table
		"""

		log.info("db_call = get_movies_last_id()")

		last_movie_id_db = self.cursor.execute('SELECT max(id) FROM movies')
		return last_movie_id_db.fetchone()[0]

	def get_np_random_movie(self, tg_id):
		"""
		During 'No preferences', used in personal_actions.py ('filter_no_preferences' function) and 
			callbacks.py ('process_np_next_movie()' function)

		Gets one random movie from the DB during 'No preferences'
		"""

		log.info("db_call = get_np_random_movie()")

		movie_db_amount = self.cursor.execute("SELECT COUNT(id) FROM movies")
		movie_amount = movie_db_amount.fetchone()[0]

		while True:
			
			movie_id = random.randint(1, movie_amount)
			while True:
				if len(config.users_flags[tg_id]['selected_movies']) == movie_amount:
					config.users_flags[tg_id]['NO_MOVIES_LEFT'] = True
					return []

				elif movie_id in config.users_flags[tg_id]['selected_movies']:
					movie_id = random.randint(1, movie_amount)
				else:
					break
			config.users_flags[tg_id]['selected_movies'].append(movie_id)

			db_sampling = None
			if config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
				db_sampling = self.cursor.execute("SELECT eng_name, release_year, eng_link FROM movies WHERE id = ?", (movie_id,))
			elif config.users_flags[tg_id]['SELECTED_LANGUAGE']['ru']:
				db_sampling = self.cursor.execute("SELECT rus_name, release_year, rus_link FROM movies WHERE id = ?", (movie_id,))

			db_movie = db_sampling.fetchone()
			editted_movie = self.exclude_watched_movies(tg_id, [db_movie])

			if editted_movie:
				return editted_movie

	def get_wr_movies(self, tg_id):
		"""
		Used in pesonal_actions.py in the 'filter_we_recommend()' function

		Get TOP-10 movies during 'We recommend'

		----------------------
		top movies ->
		[
			{
				'id': 1, 'movie_name': 'Интерстеллар', 'release_year': 2014, 'director': 'Кристофер Нолан', 
				'top_cast': 'Мэттью МакКонахи, Энн Хэтэуэй, Майкл Кейн, Мэтт Дэймон', 'storyline': '...', 
				'viewing_link': 'https://...', 'details_link': 'https://...', 'poster_link': 'https://...'
			}, 
			{
				...
			}
		]
		"""

		log.info("db_call = get_wr_movies()")
		formatted_movie_list = []

		categories = ['id', 'movie_name', 'release_year', 'director', 'top_cast', 'storyline', 'viewing_link', 'details_link', 'poster_link']
		top_movies = []
		for movie_id in config.WR_MOVIES:

			movie_data = self.get_movie_by_id(movie_id)
			movie_formatted_data = None
			match config.users_flags[tg_id]['SELECTED_LANGUAGE']['en']:
				case True:	
					movie_formatted_data = [movie_data['id'], movie_data['eng_name'], movie_data['release_year'], movie_data['eng_director'], movie_data['eng_cast'], movie_data['eng_storyline'], movie_data['eng_link'], movie_data['details_link'], movie_data['poster_link']]
				case False:
					movie_formatted_data = [movie_data['id'], movie_data['rus_name'], movie_data['release_year'], movie_data['rus_director'], movie_data['rus_cast'], movie_data['rus_storyline'], movie_data['rus_link'], movie_data['details_link'], movie_data['poster_link']]

			top_movies.append({category: movie for category, movie in zip(categories, movie_formatted_data)})


		def format_wr_movies():
			"""Formats the movies from db to display it"""

			for i in range(0, len(top_movies)):
				formatted_movie_list.append([config.users_flags[tg_id]['data_dict']['WR_PROCESSING_MESSAGES']['MESSAGE_SAMPLE'].format(
					poster_link=top_movies[i]['poster_link'], word_joiner=config.WORD_JOINER, movie_name=top_movies[i]['movie_name'], release_year=top_movies[i]['release_year'], director=top_movies[i]['director'], top_cast=top_movies[i]['top_cast'], storyline=top_movies[i]['storyline'], details_link=top_movies[i]['details_link']), top_movies[i]['viewing_link']])

		format_wr_movies()
		return formatted_movie_list		

	def get_user_watched_movie_id(self, tg_id, movie_ids=None):
		"""
		Used here in the 'add_user_history()' function

		Gets the data about user's watched movie (during 'Send feedback')
		"""

		log.info("db_call = get_user_watched_movie_id()")

		user_watched_movie_name = config.users_flags[tg_id]['FEEDBACK_DICT']['watched_movie']
		db_movie = self.cursor.execute("SELECT id FROM movies WHERE rus_name = ? OR eng_name = ?", 
			(user_watched_movie_name, user_watched_movie_name,))

		return db_movie.fetchone()[0]


	""" 
	-----------------------------------------------------------------

	The 'user_movie_history' table

	----------------------------------------------------------------- 
	"""	

	def is_user_history(self, tg_id):
		"""
		Used here in the 'add_user_history()' and 'exclude_watched_movies()' functions

		Checks if user's already in 'user_history'
		"""

		log.info("db_call = is_user_history()")

		db_id = self.cursor.execute("SELECT id FROM user_movie_history WHERE tg_id = ?", (tg_id,))
		return bool(db_id.fetchone())

	def create_user_history(self, tg_id, movie_id):
		"""
		Used here in the 'add_user_history()' function

		Creates a row in 'user_history'
		"""

		log.info("db_call = create_user_history()")
		serialized_id = []

		# columns contain lists, so we need to encode them before inserting
		s = json.dumps(movie_id, ensure_ascii=False)
		serialized_id = s.replace('"', '')

		self.cursor.execute("INSERT INTO 'user_movie_history' ('tg_id', 'movie_ids') VALUES (?, ?)",
			(tg_id, serialized_id,))

		return self.conn.commit()

	def get_user_movie_history(self, tg_id):
		"""
		Used here in the 'add_user_history()' function

		Returns the 'movie_ids' column from the 'user_movie_history' table
		"""

		log.info("db_call = get_user_movie_history()")

		db_user_movie_history_data = self.cursor.execute("SELECT movie_ids FROM user_movie_history WHERE tg_id = ?", (tg_id,))
		return db_user_movie_history_data.fetchone()[0]

	def add_user_history(self, tg_id):
		"""
		During 'Send feedback' in callbacks.py in the 'message_checkout()' function

		Adds a movie to 'user_history' during 'Send feedback'
		"""

		log.info("db_call = add_user_history()")
		movie_id = self.get_user_watched_movie_id(tg_id)

		if not self.is_user_history(tg_id):
			"""If such a user is not in 'user_history' yet"""
			self.create_user_history(tg_id, movie_id)
			return

		history_ids = self.get_user_movie_history(tg_id)
		extended_ids = str(history_ids) + f', {movie_id}'

		self.cursor.execute("UPDATE user_movie_history SET movie_ids = ? WHERE tg_id = ?",
			(extended_ids, tg_id,))

		return self.conn.commit()

	def exclude_watched_movies(self, tg_id, movie_list):
		"""
		Used here in the 'get_movies()' and 'get_np_random_movie()' functions

		During 'Smart search' when we take movies from 'movies', we must show user
			only those that he hasn't watched yet
		"""
		log.info("db_call = exclude_watched_movies()")

		if self.is_user_movie_selection_history(tg_id):
			"""Take the movies that user's already watched"""
			
			watched_movie_ids = self.get_user_movie_selection_history(tg_id).split(', ') # ['1', '24', '8', '21']
			watched_movie_ids = [int(s) for s in watched_movie_ids] # [1, 24, 8, 21]

			movie_list = [movie for movie in movie_list if movie[0] not in watched_movie_ids]

		return movie_list


	""" 
	-----------------------------------------------------------------

	The 'user_movie_selection' table

	----------------------------------------------------------------- 
	"""																

	def is_user_selection(self, tg_id):
		"""
		Used here in the 'add_user_selection()' function

		Checks if user's already in 'user_selection'
		"""

		log.info("db_call = is_user_selection()")

		user_db_id = self.cursor.execute("SELECT id FROM user_movie_selection WHERE tg_id = ?", (tg_id,))
		return bool(user_db_id.fetchone())

	def add_user_selection(self, tg_id, movie_list):
		"""
		Used in callbacks.py in the 'process_ss_yes()' function
		Add user's data after Smart search

		:param movie_list = [
								(27, 'Дэдпул', 2016, 'https://rezka.ag/films/fiction/11147-dedpul-2016.html'), 
								(28, 'Дэдпул 2', 2018, 'https://rezka.ag/films/action/27599-dedpul-2-2018.html')
							]
		"""

		log.info("db_call = add_user_selection()")

		# if user's already in the 'user_selection'
		if self.is_user_selection(tg_id):
			self.delete_user_selection(tg_id)


		if len(movie_list) == 1:
			self.cursor.execute("INSERT INTO 'user_movie_selection' ('tg_id', 'movie_name1', 'mood') VALUES (?, ?, ?)",
				(tg_id, movie_list[0][1], config.users_flags[tg_id]['USER_DATA']['USER_MOOD'],))

		elif len(movie_list) == 2:
			self.cursor.execute("INSERT INTO 'user_movie_selection' ('tg_id', 'movie_name1', 'movie_name2', 'mood') VALUES (?, ?, ?, ?)",
				(tg_id, movie_list[0][1], movie_list[1][1], config.users_flags[tg_id]['USER_DATA']['USER_MOOD'],))

		elif len(movie_list) == 3:
			self.cursor.execute("INSERT INTO 'user_movie_selection' ('tg_id', 'movie_name1', 'movie_name2', 'movie_name3', 'mood') VALUES (?, ?, ?, ?, ?)",
				(tg_id, movie_list[0][1], movie_list[1][1], movie_list[2][1], config.users_flags[tg_id]['USER_DATA']['USER_MOOD'],))

		elif len(movie_list) == 4:
			self.cursor.execute("INSERT INTO 'user_movie_selection' ('tg_id', 'movie_name1', 'movie_name2', 'movie_name3', 'movie_name4', 'mood') VALUES (?, ?, ?, ?, ?, ?)",
				(tg_id, movie_list[0][1], movie_list[1][1], movie_list[2][1], movie_list[3][1], config.users_flags[tg_id]['USER_DATA']['USER_MOOD'],))

		elif len(movie_list) == 5:
			self.cursor.execute("INSERT INTO 'user_movie_selection' ('tg_id', 'movie_name1', 'movie_name2', 'movie_name3', 'movie_name4', 'movie_name5', 'mood') VALUES (?, ?, ?, ?, ?, ?, ?)",
				(tg_id, movie_list[0][1], movie_list[1][1], movie_list[2][1], movie_list[3][1], movie_list[4][1], config.users_flags[tg_id]['USER_DATA']['USER_MOOD'],))

		return self.conn.commit()

	def delete_user_selection(self, tg_id):
		"""
		Used here in the 'delete_user_selection_movie()' and 'add_user_selection()' functions

		Deletes a row from 'user_selection' 
		"""

		log.info("db_call = delete_user_selection()")

		self.cursor.execute("DELETE FROM user_movie_selection WHERE tg_id = ?", (tg_id,))
		return self.conn.commit()

	def delete_user_selection_movie(self, tg_id):
		"""
		During 'Send feedback', used in personal_actions.py in the 'message_checkout()' function

		When user makes a review on a movie, we delete this movie from his list of previous offered movies,
			in case he'll want to make more reviews (the line is erased completely only after 'Smart search')
		"""

		log.info("db_call = delete_user_selection_movie()")

		if not self.are_user_selection_movies(tg_id):
			"""If user made a review on each movie from his previous 'Smart search' """
			self.delete_user_selection(tg_id)
			return

		column_name = None
		for i in range(0, len(config.users_flags[tg_id]['user_previous_movies'])):
			if config.users_flags[tg_id]['FEEDBACK_DICT']['watched_movie'] == config.users_flags[tg_id]['user_previous_movies'][i]:
				i += 1
				column_name = f"movie_name{i}"
				break

		self.cursor.execute('UPDATE user_movie_selection SET "{}" = NULL WHERE tg_id = ?'.format(column_name), (tg_id,))
		return self.conn.commit()

	def are_user_selection_movies(self, tg_id):
		"""
		Used here in the 'delete_user_selection_movie()' function

		When we delete a movie from 'user_selection' during 'Send feedback', we check
			if there are movies that are not rated yet
		"""

		log.info("db_call = are_user_selection_movies()")

		user_db_movies = self.cursor.execute("SELECT movie_name1, movie_name2, movie_name3, movie_name4, movie_name5 FROM user_movie_selection WHERE tg_id = ?", (tg_id,))
		movie_names = list(user_db_movies.fetchone())

		return movie_names.count(None) != len(movie_names) - 1

	def get_user_selection(self, tg_id):
		"""
		During 'Send feedback', used in keyboards.py in the 'set_sf_movies_keyboard()' function

		Get user's movies that the bot offered him last time
		"""

		log.info("db_call = get_user_selection()")

		user_db_data = self.cursor.execute("SELECT movie_name1, movie_name2, movie_name3, movie_name4, movie_name5, mood FROM user_movie_selection WHERE tg_id = ?", (tg_id,))
		return list(user_db_data.fetchone())


	""" 
	-----------------------------------------------------------------

	The 'old_feedbacks' and 'new_feedbacks' tables

	----------------------------------------------------------------- 
	"""

	def is_old_feedbacks(self, tg_id):
		"""
		Used here in the 'add_user_to_old_feedbacks()' function

		If user's already in the 'old_feedbacks' table
		"""

		log.info("db_call = is_old_feedbacks()")

		db_old_feedbacks = self.cursor.execute("SELECT * FROM old_feedbacks WHERE tg_id = ?", (tg_id,))
		return bool(db_old_feedbacks.fetchone())

	def create_old_feedbacks(self, tg_id):
		"""
		Used here in the 'add_user_to_old_feedbacks()' function

		The use isn't in the 'old_feedbacks' table, we make the first record
		"""

		log.info("db_call = create_old_feedbacks()")

		self.cursor.execute("INSERT INTO 'old_feedbacks' ('tg_id', 'tg_names', 'watched_movies', 'moods', 'verdicts', 'comments') VALUES (?, ?, ?, ?, ?, ?)",
			(config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][0], config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][1], config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][2], config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][3], config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][4], config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][5],))

		return self.conn.commit()


	def add_user_to_old_feedbacks(self, user_feedback_tg_id: int, admin_tg_id: int):
		"""
		During 'admin-mode' in callbacks.py in the 

		After 'Send feedback' we have user's feedback, now we save it and 
			then we delete user's row in 'user_selection'
		"""

		if not self.is_old_feedbacks(user_feedback_tg_id):
			self.create_old_feedbacks(admin_tg_id)
			return
		
		log.info("db_call = add_user_to_old_feedbacks()")

		extended_data = []
		new_feedback_values = config.users_flags[admin_tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'] # [1148695153, 'Red Sparrow', 'Depression', 'Было не так уж и плохо ', 'wasd']
		new_feedback_values.pop(0)

		user_old_feedbacks = self.get_user_old_feedbacks_data(user_feedback_tg_id)

		user_old_feedbacks.pop(0)
		user_old_feedbacks.pop(0)
		for i in range(0, len(user_old_feedbacks)):
			extended_data.append(str(user_old_feedbacks[i]) + f'{self.OLD_FEEDBACKS_DELIMITER}{new_feedback_values[i]}')

		self.cursor.execute("UPDATE old_feedbacks SET tg_names = ?, watched_movies = ?, moods = ?, verdicts = ?, comments = ? WHERE tg_id = ?",
			(extended_data[0], extended_data[1], extended_data[2], extended_data[3], extended_data[4], user_feedback_tg_id,))

		return self.conn.commit()

	def get_user_old_feedbacks_data(self, tg_id):
		"""
		Used here in the 'add_user_to_old_feedbacks()' function
		Get all the specific user's data that is already in the table

		:return = [1, 1148695153, 'Daniyar', 'Red Sparrow', 'Depression', 'Было не так уж и плохо ', 'random, text']
		"""

		log.info("db_call = get_user_old_feedbacks_data()")

		db_user_old_feedbacks = self.cursor.execute("SELECT * FROM old_feedbacks WHERE tg_id = ?", (tg_id,))
		user_old_feedbacks = db_user_old_feedbacks.fetchone()

		return list(user_old_feedbacks)

	def get_users_old_feedbacks_data(self):
		"""
		Used here in the 'add_user_to_old_feedbacks()' function
		Get all users' data that is already in the table

		:return =  [
						(1, 1148695153, 'Daniyar, Daniyar', 'Форрест гамп|Дорогой джон', 'Депрессия|Депрессия', 'Было не так уж и плохо |Смешанные чувства ', 'ggg|wwwwwwwwww'), 
						(2, 2060283357, 'Daniyar', 'Море соблазна', 'Депрессия', 'Смешанные чувства ', 'aaaaaaa')
				   ]
		"""

		log.info("db_call = get_users_old_feedbacks_data()")

		db_user_old_feedbacks = self.cursor.execute("SELECT * FROM old_feedbacks")
		user_old_feedbacks = db_user_old_feedbacks.fetchall()

		return list(user_old_feedbacks)


	def add_user_to_new_feedbacks(self, tg_id):
		"""
		During 'Send feedback' in personal_actions.py in the 'message_checkout()' function

		After 'Send feedback' we have user's feedback, now we save it and 
			then we delete user's row in 'user_selection'
		"""
		
		log.info("db_call = add_user_to_new_feedbacks()")

		self.cursor.execute("INSERT INTO 'new_feedbacks' ('tg_id', 'tg_name', 'watched_movie', 'mood', 'verdict', 'comment') VALUES (?, ?, ?, ?, ?, ?)",
			(config.users_flags[tg_id]['FEEDBACK_DICT']['tg_id'], config.users_flags[tg_id]['FEEDBACK_DICT']['tg_name'], config.users_flags[tg_id]['FEEDBACK_DICT']['watched_movie'], config.users_flags[tg_id]['FEEDBACK_DICT']['mood'], config.users_flags[tg_id]['FEEDBACK_DICT']['verdict'], config.users_flags[tg_id]['FEEDBACK_DICT']['comment'],))

		return self.conn.commit


	def drop_and_redirect_feedback(self, tg_id):
		"""
		During 'Send feedback' in callbacks.py in the 'process_admin_next_feedback()' function

		When admins clicks 'next' to the next feedback, the one he watched
			must be removed from the 'new_feedbacks' table but added to the 'old_feedbacks' table
		"""
		
		log.info("db_call = drop_and_redirect_feedback()")

		# delete the geedback from the 'new_feedbacks' table
		last_movie_id = self.get_new_feedbacks_last_movie_id()
		self.cursor.execute("DELETE FROM new_feedbacks WHERE id = ?", (last_movie_id,))

		# reset autoincrement
		self.cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = ?", (last_movie_id - 1, "new_feedbacks",))

		# add the feedback to the 'old_feedback' table
		self.add_user_to_old_feedbacks(config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'][0], tg_id)

		return self.conn.commit()

	def get_new_feedback(self, tg_id):
		"""
		During 'Send feedback' in callbacks.py in the 'process_admin_next_feedback()' function

		Gets all the info from 'new_feedbacks', admin only
		"""
		
		log.info("db_call = get_new_feedback()")

		movie_message = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['FEEDBACKS_SAMPLE']

		last_movie_id = self.get_new_feedbacks_last_movie_id()
		if last_movie_id:
			"""If there is some feedback"""

			feedback_db = self.cursor.execute("SELECT tg_id, tg_name, watched_movie, mood, verdict, comment FROM new_feedbacks WHERE id = ?", (last_movie_id,))
			feedback = feedback_db.fetchone()
				
			full_message = movie_message.format(movie_name=feedback[2], mood=feedback[3],
				verdict=feedback[4], comment=feedback[5])

			config.users_flags[tg_id]['ON_ADMIN_MODE']['FEEDBACK_USER_DATA'] = [feedback[0], feedback[1], feedback[2], feedback[3], feedback[4], feedback[5]]
			return full_message

		else:
			"""No feedbacks in the table"""
			return False

	def get_new_feedbacks_last_movie_id(self):
		"""
		Used here in the 'drop_user_new_feedbacks()' and 'get_new_feedback()' functions

		Gets the last 'id' field from 'new_feedbacks' table
		"""

		log.info("db_call = get_last_feedback_movie_id()")

		last_movie_id_db = self.cursor.execute('SELECT max(id) FROM new_feedbacks')
		return last_movie_id_db.fetchone()[0]


	""" 
	-----------------------------------------------------------------

	The 'movie_offers' table

	----------------------------------------------------------------- 
	"""

	def is_movie_offer(self):
		"""
		During admin-mode in the 'process_admin_offers()' and 'process_admin_offers_accept()'
			and 'on_admin_offers_cancel()' functions

		It there are movie offers or not
		"""

		log.info("db_call = is_movie_offer()")

		db_rows = self.cursor.execute("SELECT * FROM movie_offers")
		return bool(db_rows.fetchone())

	def add_movie_offer(self, tg_id, user_offer):
		"""
		During cmd-offermovie in personal_actions.py in the 'filter_offering_movie()' function

		Adds a movie offer to the 'movie_offers' table
		"""

		log.info("db_call = add_movie_offer()")

		self.cursor.execute("INSERT INTO 'movie_offers' (tg_id, user_offer) VALUES (?, ?)", (tg_id, user_offer))
		return self.conn.commit()

	def get_movie_offer(self, tg_id):
		"""
		During admin-mode, used in MovieFormat in the 'send_movie_offer()' function

		Returns all the necessary values from the last row for the 'send_movie_offer()' func
		(last row because we show the offers from the end to the start to admins)
		"""
		log.info("db_call = get_movie_offer()")

		last_movie_offer_id = self.get_last_movie_offer_id()
		config.users_flags[tg_id]['cur_movie_offer_index'] = last_movie_offer_id

		movie_offer_db = self.cursor.execute('SELECT user_offer FROM movie_offers WHERE id = ?', (last_movie_offer_id,))

		return movie_offer_db.fetchone()[0]

	def drop_movie_offer(self, tg_id):
		"""
		During admin-mode, used in callbacks.py in the 'process_admin_offers_accept()' 
			and 'on_admin_offers_cancel()' functions

		Returns the last movie offer (because we show the offers from the end to the start to admins)
		"""

		log.info("db_call = drop_movie_offer()")

		self.cursor.execute('DELETE FROM movie_offers WHERE id = ?', (config.users_flags[tg_id]['cur_movie_offer_index'],))
		return self.conn.commit()

	def get_tg_id_from_movie_offer(self):
		"""
		During , used in callbacks.py in the 'process_admin_offers_accept()' and 'on_admin_offers_cancel()' functions

		Returns the 'tg_id' field of the last offer (because we show the offers from the end to the start to admins)
		"""

		log.info("function get_tg_id_from_movie_offer()")

		last_tg_id_db = self.cursor.execute('SELECT tg_id FROM movie_offers ORDER BY id DESC LIMIT 1')
		return last_tg_id_db.fetchone()[0]

	def get_last_movie_offer_id(self):
		"""
		Used here in the 'get_movie_offer()' function

		Gets the last 'id' field from 'movie_offers' table
		"""

		log.info("db_call = get_last_movie_offer_id()")

		last_movie_offer_id_db = self.cursor.execute('SELECT max(id) FROM movie_offers')
		return last_movie_offer_id_db.fetchone()[0]


	""" 
	-----------------------------------------------------------------

	The 'user_search_history' table

	----------------------------------------------------------------- 
	"""

	def is_user_search_history(self, tg_id):
		"""
		Used here in the 'add_user_search_history()' function

		Checks if user's already in 'user_search_history'
		"""

		log.info("db_call = is_user_search_history()")

		db_id = self.cursor.execute("SELECT id FROM user_search_history WHERE tg_id = ?", (tg_id,))
		return bool(db_id.fetchone())

	def create_user_search_history(self, tg_id, tg_name):
		"""
		Used here in the 'add_user_search_history()' function

		Creates a row in 'user_search_history'
		"""

		log.info("db_call = create_user_search_history()")
		serialized_data = []

		user_data = self.get_user_search_history_data(tg_id)
		for i in range(0, len(user_data)):
			s = json.dumps(user_data[i], ensure_ascii=False)
			serialized_data.append(s.replace('"', ''))

		self.cursor.execute("INSERT INTO 'user_search_history' ('tg_id', 'tg_names', 'dates', 'moods', 'catalogues', 'genres') VALUES (?, ?, ?, ?, ?, ?)",
			(tg_id, tg_name, serialized_data[0], serialized_data[1], serialized_data[2], serialized_data[3]))

		return self.conn.commit()

	def add_user_search_history(self, tg_id, tg_name):
		"""
		Used in callbacks.py in the 'process_ss_yes()' function
		Adds a new record to 'user_search_history' during at the end of 'Smart search'
		
		:param selection_history_data = ['Daniyar', '03.11.22', 'Depression', 'Movie', 'Drama']
		:param extended_data = ['Daniyar, Daniyar', '03.11.22, 03.11.22', 'Depression, Fighting', 'Movie, Movie', 'Drama, Action']
		"""

		log.info("db_call = add_user_search_history()")

		if not self.is_user_search_history(tg_id):
			"""If such a user is not in 'user_search_history' yet"""
			self.create_user_search_history(tg_id, tg_name)
			return

		user_data = self.get_user_search_history_data(tg_id)
		user_data.insert(0, tg_name)
		extended_data = []

		db_selection_history_data = self.cursor.execute("SELECT tg_names, dates, moods, catalogues, genres FROM user_search_history WHERE tg_id = ?", (tg_id,))
		selection_history_data = list(db_selection_history_data.fetchone())

		for i in range(0, len(user_data)):
			extended_data.append(str(selection_history_data[i]) + f'{self.USER_SEARCH_HISTORY_DELIMITER}{user_data[i]}')

		self.cursor.execute("UPDATE user_search_history SET tg_names = ?, dates = ?, moods = ?, catalogues = ?, genres = ? WHERE tg_id = ?",
			(extended_data[0], extended_data[1], extended_data[2], extended_data[3], extended_data[4], tg_id,))

		return self.conn.commit()

	def get_users_search_history(self):
		"""
		During admin-mode, used in callbacks.py in the 'process_admin_excel()' function
		Returns the data about all the users from 'user_search_history' table

		:return = [
					(1, 1148695153, 'Daniyar, Daniyar', '29.10, 29.10', 'Боевое, Депрессия', 'Фильм, Фильм', 'Боевик, Драма'), 
					(2, 2060283357, 'Daniyar, Daniyar', '29.10, 30.10.22', 'Family, Депрессия', 'Movie, Фильм', 'Fiction, Драма')
				  ]
		"""

		log.info("db_call = get_users_search_history()")

		db_users_search_history = self.cursor.execute("SELECT * FROM user_search_history")
		users_search_history = db_users_search_history.fetchall()

		if users_search_history:
			return list(users_search_history)
		else:
			return None

	def get_user_search_history_data(self, tg_id):
		"""
		Used here in the 'create_user_search_history()' and 'add_user_search_history()' functions
		Returns the data that must be added to the db
		
		:return = ['03.11.22', 'Depression', 'Movie', 'Drama']
		"""

		log.info("db_call = get_user_search_history_data()")

		# current date
		today = date.today()
		cur_date = today.strftime("%d.%m.%y")

		# columns contain lists, so we need to encode them before inserting
		user_data = list(config.users_flags[tg_id]['USER_DATA'].values())
		user_data.insert(0, cur_date)

		return user_data


	""" 
	-----------------------------------------------------------------

	The 'user_movie_selection_history' table

	----------------------------------------------------------------- 
	"""

	def is_user_movie_selection_history(self, tg_id):
		"""
		Used here in the 'add_user_movie_selection_history()' function

		Checks if user's already in 'user_movie_selection_history'
		"""

		log.info("db_call = is_user_movie_selection_history()")

		db_id = self.cursor.execute("SELECT id FROM user_movie_selection_history WHERE tg_id = ?", (tg_id,))
		return bool(db_id.fetchone())

	def create_user_movie_selection_history(self, tg_id, movie_ids):
		"""
		Used here in the 'add_user_movie_selection_history()' function
		Creates a row in 'user_movie_selection_history'

		:param movie_ids = [27, 28]
		"""

		log.info("db_call = create_user_movie_selection_history()")

		string_movie_ids = self.USER_MOVIE_SELECTION_HISTORY_DELIMITER.join([str(s) for s in movie_ids]) # '27, 28'
		self.cursor.execute("INSERT INTO 'user_movie_selection_history' ('tg_id', 'movie_ids') VALUES (?, ?)",
			(tg_id, string_movie_ids))

		return self.conn.commit()

	def get_user_movie_selection_history(self, tg_id):
		"""
		Used here in the 'add_user_movie_selection_history()' and '' functions

		Returns the 'movie_ids' field from the db
		"""

		log.info("db_call = get_user_movie_selection_history()")

		db_movie_ids = self.cursor.execute("SELECT movie_ids FROM user_movie_selection_history WHERE tg_id = ?", (tg_id,))
		return db_movie_ids.fetchone()[0] # '27, 28'

	def add_user_movie_selection_history(self, tg_id, movie_list):
		"""
		During 'Smart Search' in personal_actions.py in the 'process_ss_yes()' function
		Adds a movie id to the 'add_user_movie_selection_history' table

		:param movie_list = [
								(27, 'Дэдпул', 2016, 'https://...'), 
								(28, 'Дэдпул 2', 2018, 'https://...')
					   		]
		"""

		log.info("db_call = add_user_movie_selection_history()")

		# if user's not in the 'user_movie_selection_history' yet
		if not self.is_user_movie_selection_history(tg_id):
			self.create_user_movie_selection_history(tg_id, [movie[0] for movie in movie_list])
			return

		movie_ids = self.get_user_movie_selection_history(tg_id)
		for movie in movie_list: 
			new_movie_id = movie[0]
			movie_ids += f'{self.USER_MOVIE_SELECTION_HISTORY_DELIMITER}{new_movie_id}'
			
		self.cursor.execute("UPDATE user_movie_selection_history SET movie_ids = ? WHERE tg_id = ?",
			(movie_ids, tg_id,))

		return self.conn.commit()

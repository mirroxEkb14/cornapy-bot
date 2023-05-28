
from aiogram import types
from random import randint
import config
import logger
import asyncio
import re

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name='logger/movie_format.log')

class MovieFormat:

	@staticmethod
	async def is_formatted_rus(message: types.Message, data_provider, pa_data_dict, movie_dict, movie_index=None):
		"""
		During admin-mode in personal_actions.py, in the 'filter_adding_admin_movie()' function

		Checks each separated movie value that the user entered and 
			if there is a mistake in typing, sends a message to user
			where exactly he has a mistake. The 'rus_name' and 'rus_link'
			firlds are checked by admins later

		Mood/Genre note:
			For 'depression' in ENG there are two alternatives in RUS:
				'депрессия' - that is in data.json and it is saved in the database
				'депрессняк' - a variant that user may enter, so it is also considered here during verifications

			For 'cheerful in ENG there are also two alternatives in RUS':
				'весёлое' - that is in data.json and contained in the database
				'веселое' - a variant user may enter

			For 'adventure':
				'приключение' - in data.json and in the database
				'приключения' - user may type

		During these verifications the user doesn't have to type
			the '/offermovie' command again
		"""

		log.info("mf_call = is_formatted_rus()")
		is_formatted = True

		def is_formatted_mood() -> bool:
			rus_moods = list(data_provider['russian']['InlineKeyboardCallbacks']['UserMood'].values())
			input_moods = movie_dict['rus_mood'].split('/')

			counter = 0
			for input_mood in input_moods:
				if input_mood.lower() in rus_moods or input_mood.lower() in list(data_provider['russian']['RUS_SS_VARIANTS']['USERMOODS'].values()): 
					counter += 1

			return counter == len(input_moods)

		def is_formatted_catalogue() -> bool:
			rus_catalogues = list(data_provider['russian']['InlineKeyboardCallbacks']['Catalogue'].values())
			input_catalogue = movie_dict['rus_catalogue']

			if input_catalogue.lower() in rus_catalogues: return True
			else: return False

		def is_formatted_genre() -> bool:
			rus_genres = list(data_provider['russian']['InlineKeyboardCallbacks']['Genre']['Main'].values()) + list(data_provider['russian']['InlineKeyboardCallbacks']['Genre']['More'].values())
			input_genres = movie_dict['rus_genre'].split('/')

			counter = 0
			for input_genre in input_genres:
				if input_genre.lower() in rus_genres or input_genre.lower() in list(data_provider['russian']['RUS_SS_VARIANTS']['GENRES'].values()): 
					counter += 1

			return counter == len(input_genres)

		def is_formatted_year() -> bool:
			input_year = movie_dict['release_year']
			pattern = re.compile(r'[12]\d{3}')

			if len(input_year) == 4:
				for match in pattern.finditer(input_year):
					return match

			return False

		def is_formatted_rus_link() -> bool:
			input_link = movie_dict['rus_link']

			if re.findall(r'^(https://|http://).', input_link, re.IGNORECASE):
				return True

			return False


		if not is_formatted_mood():
			mood_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['MOOD_INCORRECT']
			await message.answer(mood_incorrect_msg[randint(0, len(mood_incorrect_msg) - 1)])
			is_formatted = False

		elif not is_formatted_catalogue():
			catalogue_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['CATALOGUE_INCORRECT']
			await message.answer(catalogue_incorrect_msg[randint(0, len(catalogue_incorrect_msg) - 1)])
			is_formatted = False

		elif not is_formatted_genre():
			genre_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['GENRE_INCORRECT']
			await message.answer(genre_incorrect_msg[randint(0, len(genre_incorrect_msg) - 1)])
			is_formatted = False

		elif not is_formatted_year():
			year_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['YEAR_INCORRECT']
			await message.answer(year_incorrect_msg[randint(0, len(year_incorrect_msg) - 1)])
			is_formatted = False

		elif not is_formatted_rus_link():
			link_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['LINK_INCORRECT']
			await message.answer(link_incorrect_msg[randint(0, len(link_incorrect_msg) - 1)])
			is_formatted = False


		if movie_index and not is_formatted:
			await asyncio.sleep(1)
			movie_list_incorrect_msg = pa_data_dict['OFFERING_MOVIE_MESSAGES']['MOVIE_LIST_INCORRECT']
			await message.reply(movie_list_incorrect_msg[randint(0, len(movie_list_incorrect_msg) - 1)].format(movie_index=movie_index))

		return is_formatted


	@staticmethod
	def get_formatted_movie(data_provider, movie_dict):
		"""
		During admin-mode in personal_actions.py, in the 'filter_adding_admin_movie()' function

		This method creates the rus-side and eng-side of the movie parameters
			and returns them in one sorted formatted_movie_list	
		"""

		log.info('mf_call = get_formatted_movie()')

		def get_formatted_rus(data_provider, movie_dict) -> list:
			"""
			Returns the rus-side of the formatted_movie_list
			Make the 'rus_name', 'rus_mood', 'rus_catalogue', 'rus_genre' fields upper-case
			Check if user entered the variants from 'RUS_USERMOOD_VARIANTS'
			"""

			log.info('mf_call = get_formatted_rus()')
			formattedd_rus_side = []

			formattedd_rus_side.append(movie_dict['rus_name'].lower().capitalize())

			# format the mood considering that user may type mood different from what we have in the callback container
			rus_moods = list(map(lambda mood: mood.lower(), movie_dict['rus_mood'].split('/')))
			user_mood_variants = list(data_provider['russian']['RUS_SS_VARIANTS']['USERMOODS'].values())

			if any(rus_temp_mood.lower() in rus_moods for rus_temp_mood in user_mood_variants):
				for rus_mood in rus_moods:
					for key, value in data_provider['russian']['RUS_SS_VARIANTS']['USERMOODS'].items():
						if rus_mood.lower() == value:
							rus_moods[rus_moods.index(rus_mood)] = data_provider['russian']['InlineKeyboardCallbacks']['UserMood'][key]
							break
			
			formattedd_rus_side.append('/'.join(list(i.lower().capitalize() for i in rus_moods)))
			
			formattedd_rus_side.append(movie_dict['rus_catalogue'].lower().capitalize())

			# same case like with the mood
			rus_genres = list(map(lambda genre: genre.lower(), movie_dict['rus_genre'].split('/')))
			user_genre_variants = list(data_provider['russian']['RUS_SS_VARIANTS']['GENRES'].values())

			if any(rus_temp_genre in rus_genres for rus_temp_genre in user_genre_variants):
				for rus_genre in rus_genres:
					for key, value in data_provider['russian']['RUS_SS_VARIANTS']['GENRES'].items():
						if rus_genre.lower() == value:
							rus_genres[rus_genres.index(rus_genre)] = data_provider['russian']['InlineKeyboardCallbacks']['Genre'][key]
							break

			formattedd_rus_side.append('/'.join(list(g.lower().capitalize() for g in rus_genres)))
			
			formattedd_rus_side.append(movie_dict['release_year'])
			formattedd_rus_side.append(movie_dict['rus_link'])

			return formattedd_rus_side

		def get_formatted_eng(data_provider, movie_dict) -> list:
			"""
			Returns the eng-side of the formatted_movie_list
			
			We're missing 5 columns from 'eng_name' to 'eng_link' included: eng_name, eng_mood, 
				eng_catalogue, eng_genre, eng_link. The user doesn't need to type it, so his life
				is much more easier

			We add two None to the list, the first one is for the 'eng_name' field and
				the second one is for the 'eng_link' field, these fields must be checked
				and editted later by admins themselves

			The values of 'rus_mood'/'eng_mood' and 'rus_genre'/'eng_genre' can contain more than one
				word, they're divided by '/', because one the same movie can contain two genres or 
				can be responsible for two moods at once
			"""

			log.info('mf_call = get_formatted_eng()')
			formatted_eng_side = []
			
			def get_eng_mood() -> list:
				eng_moods = []
				rus_moods = movie_dict['rus_mood'].split('/')

				for mood in rus_moods:
					mood = mood.lower()
					for eng_key, eng_value in data_provider['english']['InlineKeyboardCallbacks']['UserMood'].items():
						
						if mood == data_provider['russian']['InlineKeyboardCallbacks']['UserMood'][eng_key]:
							eng_moods.append(data_provider['english']['InlineKeyboardCallbacks']['UserMood'][eng_key].capitalize())
							break	
						
						elif mood in list(data_provider['russian']['RUS_SS_VARIANTS']['USERMOODS'].values()):
							for rus_key, rus_value in data_provider['russian']['RUS_SS_VARIANTS']['USERMOODS'].items():
								
								if mood == rus_value:
									eng_moods.append(data_provider['english']['InlineKeyboardCallbacks']['UserMood'][rus_key].capitalize())
									break
							break

				return eng_moods

			def set_eng_catalogue() -> None:
				for key, value in data_provider['english']['InlineKeyboardCallbacks']['Catalogue'].items():
					if data_provider['russian']['InlineKeyboardCallbacks']['Catalogue'][key] == movie_dict['rus_catalogue'].lower():
						formatted_eng_side.append(data_provider['english']['InlineKeyboardCallbacks']['Catalogue'][key].capitalize())
						break

			def get_eng_genre() -> list:
				eng_genres = []
				rus_genres = movie_dict['rus_genre'].split('/')

				for genre in rus_genres:

					# keys are either Main or More, values are their dicts
					genre = genre.lower()
					for eng_genre_section, eng_section_dict in data_provider['english']['InlineKeyboardCallbacks']['Genre'].items():

						# to avoid the last "MORE_CB": "more" pair
						if type(eng_section_dict) == dict:

							# keys and values inside Main or More sections
							for eng_key, eng_value in eng_section_dict.items():

								if genre == data_provider['russian']['InlineKeyboardCallbacks']['Genre'][eng_genre_section][eng_key]:
									eng_genres.append(data_provider['english']['InlineKeyboardCallbacks']['Genre'][eng_genre_section][eng_key].capitalize())
									break

								elif genre in list(data_provider['russian']['RUS_SS_VARIANTS']['GENRES'].values()):
									for rus_key, rus_value in data_provider['russian']['RUS_SS_VARIANTS']['GENRES'].items():
										
										if genre == rus_value:
											eng_genres.append(data_provider['english']['InlineKeyboardCallbacks']['Genre'][eng_genre_section][rus_key].capitalize())
											break
									break

				return eng_genres
			
			
			formatted_eng_side.append(movie_dict['eng_name'].lower().capitalize())
			formatted_eng_side.append('/'.join(get_eng_mood()))
			set_eng_catalogue()
			formatted_eng_side.append('/'.join(get_eng_genre()))
			formatted_eng_side.append(movie_dict['eng_link'])
			formatted_eng_side.append(movie_dict['poster_link'])

			return formatted_eng_side

		return get_formatted_rus(data_provider, movie_dict) + get_formatted_eng(data_provider, movie_dict)


	@staticmethod
	def get_np_movie_format(movie: tuple):
		"""
		During 'No preferences' in personal_actions.py, in the 'filter_no_preferences()' function

		Form a movie message to display
		"""

		log.info("mf_call = get_np_movie_format()")
		return f'{movie[0][0]}, {movie[0][1]}\n\n{movie[0][2]}'


	@staticmethod
	async def send_movies(message: types.Message, c_data_dict, movie_data):
		"""
		During 'Smart search' in callbacks.py, in the 'process_ss_yes()' function

		Sends a movie to the user at the end of 'Smart search'
		"""

		log.info("mf_call = send_movies()")

		def get_movie_message(c_data_dict, movie_data):
			"""Firms the message with movies for user at the end of 'Smart Selection'"""

			ss_sampling_msg = c_data_dict['SS_PROCESSING_MESSAGES']['SS_SAMPLING'] 
			full_message = ss_sampling_msg[randint(0, len(ss_sampling_msg) - 1)]

			for movie_list in movie_data:
				full_message += config.MOVIE_MESSAGE.format(movie_name=movie_list[1], 
					movie_release_year=movie_list[2], movie_link=movie_list[3])

			return full_message

		movie_full_message = get_movie_message(c_data_dict, movie_data)
		await message.answer(movie_full_message, parse_mode='html')


	@staticmethod
	async def is_movie_offer(call, bot):
		"""
		During admin-mode in callbacks.py

		Checks if there are offers and sends a message to an admin if there aren't
		"""

		log.info("mf_call = is_movie_offer()")
		tg_id = call.from_user.id

		if config.BotDB.is_movie_offer():
			return True

		else:
			await bot.delete_message(chat_id=call.from_user.id, 
				message_id=call.message.message_id)

			if config.users_flags[call.from_user.id]['IS_ADMIN_OFFERS']:
				"""It is not the first offer the admin looks at"""
				no_movies_to_offer_anymore = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['NO_MOVIES_TO_OFFER_ANYMORE']
				await call.message.answer(no_movies_to_offer_anymore[randint(0, len(no_movies_to_offer_anymore) - 1)])
			else:
				"""Admins clicks on 'OFFERS_BTN' and it's the first movie offer he looks at, but it's empty"""
				no_movies_to_offer_at_start = config.users_flags[tg_id]['data_dict']['OFFERING_MOVIE_MESSAGES']['NO_MOVIES_TO_OFFER_AT_START']
				await call.message.answer(no_movies_to_offer_at_start[randint(0, len(no_movies_to_offer_at_start) - 1)])

			await asyncio.sleep(1)
			admin_continue_msg = config.users_flags[tg_id]['data_dict']['ADMIN_MODE_MESSAGES']['ADMIN_CONTINUE']
			await call.message.answer(admin_continue_msg[randint(0, len(admin_continue_msg) - 1)], reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_SELECTION'])

			return False


	@staticmethod
	async def send_movie_offer(call, tg_id):
		"""
		During admin-mode in callbacks.py

		Sends a message to an admin with a movie offer
		"""

		log.info("mf_call = send_movie_offer()")

		movie_offer = config.BotDB.get_movie_offer(tg_id)
		await call.message.answer(movie_offer, reply_markup=config.users_flags[tg_id]['keyboards'].INLINE_KEYBOARDS['ADMIN_MOVIE_OFFERING'])


	@staticmethod
	def is_movie(data_provider, movie_dict):
		"""
		During admin-mode in personal_actions.py in the 'filter_adding_admin_movie()' function

		When the admin adds a movie/series, bot sends a message of successful adding in reply,
			our bot to look like a human being and not a machine, it replies varies by what was
			added - a movie or series

		Since the project is bound to Russian community
			at a greater degree, we make a verification by 'rus_catalogue'
		"""

		log.info("mf_call = is_movie()")
		return movie_dict['rus_catalogue'].lower() == data_provider['russian']['InlineKeyboardCallbacks']['Catalogue']['MOVIE_CB']
	
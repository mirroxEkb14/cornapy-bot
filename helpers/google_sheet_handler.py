
import gspread
import config
import logging
import logger

"""

"""

# define a logger for this file
log = logger.get_logger(logger_name=__name__, file_name = 'logger/google_sheet_handler.log')

class GoogleSheetHandler:

	def __init__(self, path_to_sa_file, file_name, sheet_name):
		"""Initializing a google sheet connection"""

		sa = gspread.service_account(path_to_sa_file)
		sh = sa.open(file_name)

		self.wks = sh.worksheet(sheet_name)

	def is_updated(self):
		"""
		Verifies if an admin made changes in google sheets
			(if the last row in the google sheet equals to the last row in the DB)
		"""

		db_last_movie_id = config.BotDB.get_movies_last_id()
		google_sheet_last_movie_id = self.wks.get_all_records()[-1]['id']

		return google_sheet_last_movie_id > db_last_movie_id

	def get_new_movies(self):
		"""
		Get the movies that are in the google sheet but aren't in the DB

		:param google_sheet_movies = [
										{
											'id': 1,
											...
										},
										{
											'id': 2,
											...
										},
										...
									 ]
		:return: [
					{
						'id': 1,
						...
					},
					{
						'id': 2,
						...
					},
					...
				 ]
		"""

		db_last_movie_id = config.BotDB.get_movies_last_id()
		google_sheet_movies = self.wks.get_all_records()

		return google_sheet_movies[db_last_movie_id:]

#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: MEDOC
# Description: SQL HELPER
# Author: Emeric Dynomant
# Contact: emeric.dynomant@gmail.com
# Date: 11/08/2017
# Language release: python 3.5.2
# ==============================================================================


import os
import sys
import logging
import pymysql.cursors


class Query_Executor:
	"""Small helper class to execute query, and log them if there is an error"""

	def __init__(self, parameters):
		self.log_file = os.path.join(parameters['paths']['program_path'], parameters['paths']['sql_error_log'])
		self.connection = pymysql.connect(
			host=parameters['database']['host'],
			port=int(parameters['database']['port']),
			user=parameters['database']['user'],
			password=parameters['database']['password'],
			database=parameters['database']['database'],
			cursorclass=pymysql.cursors.DictCursor,
			charset='utf8',
			autocommit=True)

	def execute(self, sql_command):
		connection = self.connection
		cursor = connection.cursor()
		try:
			cursor.execute(sql_command)
			connection.close()
		except Exception as E:
			logging.error('Insertion error.')
			exception = sys.exc_info()[1]
			errors_log = open(self.log_file, 'a')
			errors_log.write('{} - {}\n'.format(exception, sql_command))
			errors_log.close()

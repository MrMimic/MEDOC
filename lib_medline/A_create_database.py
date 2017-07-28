
import time
import json
import pymysql.cursors

parameters_json = open('./parameters.json')
parameters = json.load(parameters_json)

''' Step 1 : Create database if not exist '''
def create_pubmedDB(parameters):
	print('- ' * 30 + 'PUBMED DATABASE CREATION')
	# Timestamp
	start_time = time.time()
	# mySQL connexion
	connection = pymysql.connect(
		host = parameters['database']['host'],
		user = parameters['database']['user'],
		password = parameters['database']['password'],
		cursorclass = pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	# Check if 'pubmed' db exists, if not, create it by executing SQL file line by line
	cursor.execute('SHOW DATABASES ;')
	local_dbNames = []
	for row in cursor:
		local_dbNames.append(row['Database'])
	if 'pubmed' in local_dbNames:
		cursor.execute('USE pubmed ;')
		cursor.execute('SHOW TABLES ;')
		print('Database pubmed already created with tables :')
		for row in cursor:
			print('\t- {}'.format(row['Tables_in_pubmed']))	
	else:
		print('Database pubmed doesn\'t exist. Creation ..')
		cursor.execute('CREATE DATABASE pubmed ;')			
		cursor.execute('USE pubmed ;')
		print('Sourcing file {}'.format(parameters['database']['path_to_sql']))
		for command in open(parameters['database']['path_to_sql'], 'r'):
			cursor.execute(command)
		print('Database Pubmed created with tables :')
		cursor.execute('SHOW TABLES ;')
		for row in cursor:
			print('\t- {}'.format(row['Tables_in_pubmed']))
	
	print('Elapsed time: {} sec for module: {}'.format(round(time.time()-start_time, 2), create_pubmedDB.__name__))	
	
	return cursor

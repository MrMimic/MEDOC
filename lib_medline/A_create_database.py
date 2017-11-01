import time
import json
import lib_medline.I_database_utility as db_util

parameters_json = open('./parameters.json')
parameters = json.load(parameters_json)

''' Step 1 : Create database if not exist '''


def create_pubmedDB(parameters):
    db_name = parameters['database']['database']
    print('- ' * 30 + '%s DATABASE CREATION' % db_name)
    #  Timestamp
    start_time = time.time()
    #  mySQL connexion
    connection = db_util.get_sequel_connection()
    cursor = connection.cursor()
    #  Check if db exists, if not, create it by executing SQL file line by line
    cursor.execute('SHOW DATABASES ;')
    local_dbNames = []
    for row in cursor:
        local_dbNames.append(row['Database'])
    if db_name in local_dbNames:
        cursor.execute('USE %s ;' % db_name)
        cursor.execute('SHOW TABLES ;')
        print('Database %s already created with tables :' % db_name)
        for row in cursor:
            print('\t- {}'.format(row['Tables_in_%s' % db_name]))
    else:
        print('Database %s doesn\'t exist. Creation ..' % db_name)
        cursor.execute('CREATE DATABASE %s DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_unicode_ci ;' % db_name)
        cursor.execute('USE %s ;' % db_name)
        print('Sourcing file {}'.format(parameters['database']['path_to_sql']))
        for command in open(parameters['database']['path_to_sql'], 'r'):
            if command is not None and command.strip() != '':
                cursor.execute(command)
        print('Database %s created with tables :' % db_name)
        cursor.execute('SHOW TABLES ;')
        for row in cursor:
            print('\t- {}'.format(row['Tables_in_%s' % db_name]))

    print('Elapsed time: {} sec for module: {}'.format(round(time.time() - start_time, 2), create_pubmedDB.__name__))

    return cursor

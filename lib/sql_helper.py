import sys
import os


class Query_Executor:
    """
    Small helper class to execute query, and log them if there is an error
    """
    def __init__(self, parameters):
        self.log_file = os.path.join(parameters['paths']['program_path'], parameters['paths']['sql_error_log'])
        self.connection = pymysql.connect(
            host=parameters['database']['host'],
            port=int(parameters['database']['port']),
            user=parameters['database']['user'],
            password=parameters['database']['password'],
            database=parameters['database']['database'],
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4',
            autocommit=True,
            init_command='SET ROLE pubmed_role;')
    def execute(self, sql_command):
        connection = self.connection
        cursor = connection.cursor()
        try:
            #~ cursor.execute('SET ROLE pubmed_role;')
            cursor.execute(sql_command)
            connection.close()
        except:
            exception = sys.exc_info()[1]
            errors_log = open(self.log_file, 'a')
            errors_log.write('{} - {}\n'.format(exception, sql_command))
            errors_log.close()

import sys


class Query_Executor:
    """
    Small helper class to execute query, and log them if there is an error
    """
    def __init__(self, parameters):
        self.log_file = parameters['paths']['sql_error_log']

    def execute(self, connection, sql_command):
        cursor = connection.cursor()
        try:
            cursor.execute(sql_command)
            connection.close()
        except:
            exception = sys.exc_info()[1]
            errors_log = open(self.log_file, 'a')
            errors_log.write('{} - {}\n'.format(exception, sql_command))
            errors_log.close()
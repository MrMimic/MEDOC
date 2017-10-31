import os
import sys
import json
import pymysql

sql_connection = None
last_write_access = None


def __config_file_changed__(filename='./parameters.json'):
    """
    Tells if the config file has been altered recently
    :param filename: 
    :return: 
    """
    global last_write_access
    current_m_time = os.path.getmtime(filename)
    updated = False

    if last_write_access is None or last_write_access < current_m_time:
        last_write_access = current_m_time
        updated = True

    return updated


def __read_json_parameter__(filename='./parameters.json'):
    """
    Parse parameters from the json input file
    :return: 
    """
    if not os.path.exists(filename):
        raise Exception('File %s not found' % filename)

    parameters_json = open(filename)
    parameters = json.load(parameters_json)
    sql_parameters = {
        'host': parameters['database']['host'],
        'port': parameters['database']['port'],
        'user': parameters['database']['user'],
        'password': parameters['database']['password']
    }

    return sql_parameters


def get_sequel_connection():
    """
    Retrieve or instanciate a connection to the DB
    :return: 
    """
    global sql_connection
    if sql_connection is None or __config_file_changed__():
        parameters = __read_json_parameter__()
        parameters['cursorclass'] = pymysql.cursors.DictCursor
        sql_connection = pymysql.connect(**parameters)

    return sql_connection

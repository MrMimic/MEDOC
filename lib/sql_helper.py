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
import mysql.connector


class Query_Executor:
    """Small helper class to execute query, and log them if there is an error"""

    def __init__(self, parameters):

        self.log_file = os.path.join(parameters['paths']['program_path'],
                                     parameters['paths']['sql_error_log'])
        self.config = {
            'host': parameters['database']['host'],
            'user': parameters['database']['user'],
            'password': parameters['database']['password'],
            'database': parameters['database']['database'],
            'use_pure': True,
            'raise_on_warnings': True,
            'get_warnings': True,
            'autocommit': True
        }
        self.connection = mysql.connector.connect(**self.config, buffered=True)

    def execute(self, sql_command, sql_data, pmid):
        """Execute a query or write into the error log"""

        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_command, sql_data)
        except Exception as E:
            exception = sys.exc_info()[1]
            if E.errno != 1062:  # We do not need to catch every "dupplicate entry" error.
                errors_log = open(self.log_file, 'a')
                errors_log.write('{} -- {} -- {}\n'.format(
                    pmid, exception, sql_command))
                errors_log.close()
        cursor.close()

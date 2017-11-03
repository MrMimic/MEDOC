
import time
import json
import pymysql.cursors

parameters_json = open('./parameters.json')
parameters = json.load(parameters_json)

''' Step 1 : Create database if not exist '''


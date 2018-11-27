#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: MEDOC
# Description: MEDOC LAUNCH
# Author: Emeric Dynomant
# Contact: emeric.dynomant@gmail.com
# Date: 11/08/2017
# Language release: python 3.5.2
# ==============================================================================


import os
import sys
import time
import logging
import configparser
import multiprocessing as mp

sys.path.append('./lib')
import MEDOC
from lib.sql_helper import Query_Executor


def parallelize(file_to_download):

		logging.info('Processing file {}.'.format(file_to_download))
		start_time = time.time()
		parameters = configparser.ConfigParser()
		parameters.read('./configuration.cfg')

		if file_to_download not in open(insert_log_path).read().splitlines():

			file_downloaded = MEDOC.download(file_name=file_to_download)  # Download file if not already
			file_downloaded = file_to_download
			articles = MEDOC.extract_articles(file_name=file_downloaded)  # Parse XML file to extract articles
			QueryExecutor = Query_Executor(parameters=parameters)

			for article in articles:  # Instead of a dict(), now everything will be inserted one by one on multi thread

				article_data = MEDOC.get_data(article=article, gz=file_downloaded)
				if article_data is not None:
					insertion = MEDOC.insert_data(data=article_data, gz=file_downloaded, pmid=article_data[0]['medline_citation']['pmid'], QueryExecutor=QueryExecutor)

			confirmation = MEDOC.remove(file_name=file_to_download)  # Remove file and add file_name to a list to ignore this file next time
			logging.info('Processed: {} ({} min) Confirmation: {}.'.format(file_to_download, round((time.time() - start_time) / 60, 2), confirmation))

			return True

		else:
			return False


if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # ALL, DEBUG, INFO, ERROR, FATAL
	logging.info('Starting MEDOC...')
	MEDOC = MEDOC.MEDOC()
	parameters = configparser.ConfigParser()
	parameters.read('./configuration.cfg')
	insert_limit = int(parameters['database']['insert_command_limit'])
	insert_log_path = os.path.join(parameters['paths']['program_path'], parameters['paths']['already_downloaded_files'])

	MEDOC.create_pubmedDB()  # Create database if not exist
	gz_file_list = MEDOC.get_file_list()  # Get file list on NCBI
	gz_file_list = ['updatefiles/{}'.format(file_name) for file_name in os.listdir('/appli/deeplearning/EMERIC/MEDOC/pudmed_data/updatefiles/') if file_name.endswith('.gz')] + ['baseline/{}'.format(file_name) for file_name in os.listdir('/appli/deeplearning/EMERIC/MEDOC/pudmed_data/baseline/') if file_name.endswith('.gz')]
	with mp.Pool(processes=int(parameters['threads']['parallel_files'])) as pool:  # Parallelize
		pool.map(parallelize, gz_file_list)

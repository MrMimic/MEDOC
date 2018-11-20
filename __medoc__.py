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
import re
import sys
import time
import tqdm
import pickle
import logging
import configparser
import multiprocessing as mp
from bs4 import BeautifulSoup


sys.path.append('./lib')
import MEDOC
import getters




def parallelize(file_to_download):

		logging.info('Processing file {}.'.format(file_to_download))
		start_time = time.time()

		if file_to_download not in open(insert_log_path).read().splitlines():

			file_downloaded = MEDOC.download(file_name=file_to_download)  # Download file if not already

			articles = MEDOC.extract_articles(file_name=file_downloaded)  # Parse XML file to extract articles

			for article in tqdm.tqdm(articles):  # Instead of a dict(), now everything will be inserted one by one on multi thread

				article_data = MEDOC.get_data(article=article, gz=file_downloaded)

				insertion = MEDOC.insert_data(data=article_data, gz=file_downloaded)

			confirmation = MEDOC.remove(file_name=file_to_download)  # Remove file and add file_name to a list to ignore this file next time

			logging.info('Processed: {} ({} min) Confirmation: {}.'.format(file_to_download, round((time.time() - start_time) / 60, 2), confirmation))

			return True

		else:
			return False


if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # ALL, DEBUG, INFO, ERROR, FATAL

	MEDOC = MEDOC.MEDOC()
	parameters = configparser.ConfigParser()
	parameters.read('./configuration.cfg')
	insert_limit = int(parameters['database']['insert_command_limit'])
	insert_log_path = os.path.join(parameters['paths']['program_path'], parameters['paths']['already_downloaded_files'])

	MEDOC.create_pubmedDB()  # Create database if not exist
	gz_file_list = MEDOC.get_file_list()  # Get file list on NCBI

	for file_name in gz_file_list:
		confirmation = parallelize(file_name)

	#~ with mp.Pool(processes=1) as pool:  # Parallelize
		#~ pool.map(parallelize, gz_file_list)
		#~ pool.join()
	#~ pool.close()

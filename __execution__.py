#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: MEDOC
# Description: MEDOC launch
# Author: Emeric Dynomant
# Contact: emeric.dynomant@omictools.com
# Date: 11/08/2017
# Language release: python 3.5.2
# ==============================================================================



# Standart libraries
import os
import re
import json
import time
import pymysql.cursors

# Custom libraries
import MEDOC
import getters


''' Parameters '''
parameters = json.load(open('./parameters.json'))

''' Regexs '''
r_year = re.compile('<year>([0-9]{4})</year>')
r_month = re.compile('<month>([0-9]{2})</month>')
r_day = re.compile('<day>([0-9]{2})</day>')



if __name__=='__main__':

	MEDOC = MEDOC.MEDOC()

	''' Step A : Create database if not exist '''
	MEDOC.create_pubmedDB()

	''' Step B: get file list on NCBI '''
	gz_file_list = MEDOC.get_file_list()

	for file_to_download in gz_file_list:

		start_time = time.time()

		if file_to_download not in open(parameters['paths']['already_downloaded_files']).read().splitlines():

			''' Step C: download file if not already'''
			file_downloaded = MEDOC.download(file_name = file_to_download)

			''' Step D: extract file '''
			file_content = MEDOC.extract(file_name = file_downloaded)

			''' Step E: Parse XML file to extract articles '''
			articles = MEDOC.parse(data = file_content)

			print('- ' * 30 + 'SQL INSERTION')

			# Lists to create
			values_tot_medline_citation = [] ; values_tot_medline_article_language = [] ; values_tot_medline_article_publication_type = [] ; values_tot_medline_author = [] ; values_tot_medline_chemical_list = [] ; values_tot_medline_citation_other_id = [] ; values_tot_medline_citation_subsets = [] ; values_tot_medline_comments_corrections = [] ; values_tot_medline_data_bank = [] ; values_tot_medline_grant = [] ; values_tot_medline_investigator = [] ; values_tot_medline_mesh_heading = [] ; values_tot_medline_personal_name_subject = []

			articles_count = 0

			''' Step F: Create a dictionnary with data to INSERT for every article '''
			for raw_article in articles:

				# Loading
				articles_count += 1
				if articles_count % 10000 == 0:
					print('{} articles inserted for file {}'.format(articles_count, file_to_download))

				article_cleaned = re.sub('\'', ' ', str(raw_article)).encode('utf-8')
				article_INSERT_list = MEDOC.get_command(article = article_cleaned, gz = file_downloaded)

				''' Step G: For every table in articles, loop to create global insert '''
				for insert_table in article_INSERT_list:

					# ____ 1: medline_citation
					if insert_table['name'] == 'medline_citation':
						values_medline_citation = getters.get_medline_citation(insert_table)
						values_tot_medline_citation.append('(' + ', '.join(values_medline_citation[0]) + ')')
						if (len(values_tot_medline_citation) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_citation(values_medline_citation[1], values_tot_medline_citation, parameters)
							values_tot_medline_citation = []

					# ____ 2: medline_article_language
					if insert_table['name'] == 'medline_article_language':
						values_medline_article_language = getters.get_medline_article_language(insert_table)
						values_tot_medline_article_language.append('(' + ', '.join(values_medline_article_language[0]) + ')')
						if (len(values_tot_medline_article_language) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_article_language(values_medline_article_language[1], values_tot_medline_article_language, parameters)
							values_tot_medline_article_language = []

					# ____ 3: medline_article_publication_type
					if insert_table['name'] == 'medline_article_publication_type':
						values_medline_article_publication_type = getters.get_medline_article_publication_type(insert_table)
						values_tot_medline_article_publication_type.append('(' + ', '.join(values_medline_article_publication_type[0]) + ')')
						if (len(values_tot_medline_article_publication_type) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_article_publication_type(values_medline_article_publication_type[1], values_tot_medline_article_publication_type, parameters)
							values_tot_medline_article_publication_type = []

					# ____ 4: medline_author
					if insert_table['name'] == 'medline_author':
						values_medline_author = getters.get_medline_author(insert_table)
						values_tot_medline_author.append('(' + ', '.join(values_medline_author[0]) + ')')
						if (len(values_tot_medline_author) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_author(values_medline_author[1], values_tot_medline_author, parameters)
							values_tot_medline_author = []

					# ____ 5: medline_chemical_list
					if insert_table['name'] == 'medline_chemical_list':
						values_medline_chemical_list = getters.get_medline_chemical_list(insert_table)
						values_tot_medline_chemical_list.append('(' + ', '.join(values_medline_chemical_list[0]) + ')')
						if (len(values_tot_medline_chemical_list) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_chemical_list(values_medline_chemical_list[1], values_tot_medline_chemical_list, parameters)
							values_tot_medline_chemical_list = []

					# ____ 6: medline_citation_other_id
					if insert_table['name'] == 'medline_citation_other_id':
						values_medline_citation_other_id = getters.get_medline_citation_other_id(insert_table)
						values_tot_medline_citation_other_id.append('(' + ', '.join(values_medline_citation_other_id[0]) + ')')
						if (len(values_tot_medline_citation_other_id) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_citation_other_id(values_medline_citation_other_id[1], values_tot_medline_citation_other_id, parameters)
							values_tot_medline_citation_other_id = []

					# ____ 7: medline_citation_subsets
					if insert_table['name'] == 'medline_citation_subsets':
						values_medline_citation_subsets = getters.get_medline_citation_subsets(insert_table)
						values_tot_medline_citation_subsets.append('(' + ', '.join(values_medline_citation_subsets[0]) + ')')
						if (len(values_tot_medline_citation_subsets) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_citation_subsets(values_medline_citation_subsets[1], values_tot_medline_citation_subsets, parameters)
							values_tot_medline_citation_subsets = []

					# ____ 8: medline_comments_corrections
					if insert_table['name'] == 'medline_comments_corrections':
						values_medline_comments_corrections = getters.get_medline_comments_corrections(insert_table)
						values_tot_medline_comments_corrections.append('(' + ', '.join(values_medline_comments_corrections[0]) + ')')
						if (len(values_tot_medline_comments_corrections) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_comments_corrections(values_medline_comments_corrections[1], values_tot_medline_comments_corrections, parameters)
							values_tot_medline_comments_corrections = []

					# ____ 9: medline_data_bank
					if insert_table['name'] == 'medline_data_bank':
						values_medline_data_bank = getters.get_medline_data_bank(insert_table)
						values_tot_medline_data_bank.append('(' + ', '.join(values_medline_data_bank[0]) + ')')
						if (len(values_tot_medline_data_bank) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_data_bank(values_medline_data_bank[1], values_tot_medline_data_bank, parameters)
							values_tot_medline_data_bank = []

					# ____ 10: medline_grant
					if insert_table['name'] == 'medline_grant':
						values_medline_grant = getters.get_medline_grant(insert_table)
						values_tot_medline_grant.append('(' + ', '.join(values_medline_grant[0]) + ')')
						if (len(values_tot_medline_grant) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_grant(values_medline_grant[1], values_tot_medline_grant, parameters)
							values_tot_medline_grant = []

					# ____ 11: medline_investigator
					if insert_table['name'] == 'medline_investigator':
						values_medline_investigator = getters.get_medline_investigator(insert_table)
						values_tot_medline_investigator.append('(' + ', '.join(values_medline_investigator[0]) + ')')
						if (len(values_tot_medline_investigator) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_investigator(values_medline_investigator[1], values_tot_medline_investigator, parameters)
							values_tot_medline_investigator = []

					# ____ 12: medline_mesh_heading
					if insert_table['name'] == 'medline_mesh_heading':
						values_medline_mesh_heading = getters.get_medline_mesh_heading(insert_table)
						values_tot_medline_mesh_heading.append('(' + ', '.join(values_medline_mesh_heading[0]) + ')')
						if (len(values_tot_medline_mesh_heading) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_mesh_heading(values_medline_mesh_heading[1], values_tot_medline_mesh_heading, parameters)
							values_tot_medline_mesh_heading = []

					# ____ 13: medline_personal_name_subject
					if insert_table['name'] == 'medline_personal_name_subject':
						values_medline_personal_name_subject = getters.get_medline_personal_name_subject(insert_table)
						values_tot_medline_personal_name_subject.append('(' + ', '.join(values_medline_personal_name_subject[0]) + ')')
						if (len(values_tot_medline_personal_name_subject) == parameters['database']['insert_command_limit']) or (articles_count == len(articles) -1):
							getters.send_medline_personal_name_subject(values_medline_personal_name_subject[1], values_tot_medline_personal_name_subject, parameters)
							values_tot_medline_personal_name_subject = []

			''' Step H: remove file and add file_name to a list to ignore this file next time '''
			MEDOC.remove(file_name = file_to_download)
			time_file = open('../time.txt', 'a')
			time_file.write('Total time for file {}: {} min\n'.format(file_to_download, round((time.time()-start_time) / 60, 2) ))
			time_file.close()
			print('Total time for file {}: {} min\n'.format(file_to_download, round((time.time()-start_time) / 60, 2) ))

			# Flush RAM
			del articles ; del values_tot_medline_citation ; del values_tot_medline_article_language ; del values_tot_medline_article_publication_type ; del values_tot_medline_author ; del values_tot_medline_chemical_list ; del values_tot_medline_citation_other_id ; del values_tot_medline_citation_subsets ; del values_tot_medline_comments_corrections ; del values_tot_medline_data_bank ; del values_tot_medline_grant ; del values_tot_medline_investigator ; del values_tot_medline_mesh_heading ; del values_tot_medline_personal_name_subject




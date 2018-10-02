#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: MEDOC
# Description: MEDOC CLASS
# Author: Emeric Dynomant
# Contact: emeric.dynomant@gmail.com
# Date: 11/08/2017
# Language release: python 3.5.2
# ==============================================================================


import os
import re
import time
import gzip
import json
import configparser
from ftplib import FTP
import pymysql.cursors
from bs4 import BeautifulSoup


class MEDOC(object):

	def __init__(self):
		"""INIT"""
		self.parameters = self.config = configparser.ConfigParser()
		self.parameters.read('./configuration.cfg')
		self.regex_gz = re.compile('^pubmed.*.xml.gz$')
		self.insert_log_path = os.path.join(self.parameters['paths']['program_path'], self.parameters['paths']['already_downloaded_files'])
		self.download_folder = os.path.join(self.parameters['paths']['program_path'], self.parameters['paths']['pubmed_data_download'])

	def create_pubmedDB(self):
		"""DATABASE CREATION"""

		wished_schema_name = self.parameters['database']['database']
		#  Timestamp
		start_time = time.time()
		#  mySQL connexion
		connection = pymysql.connect(
			host=self.parameters.get('database', 'host'),
			port=self.parameters.getint('database', 'port'),
			user=self.parameters.get('database', 'user'),
			password=self.parameters.get('database', 'password'),
			cursorclass=pymysql.cursors.DictCursor,
			autocommit=True)
		cursor = connection.cursor()

		#  Check if 'pubmed' db exists, if not, create it by executing SQL file line by line
		cursor.execute('SHOW DATABASES ;')
		local_dbNames = []
		for row in cursor:
			local_dbNames.append(row['Database'])
		if wished_schema_name in local_dbNames:
			cursor.execute('USE {} ;'.format(wished_schema_name))
			cursor.execute('SHOW TABLES ;')

		else:
			cursor.execute('CREATE DATABASE {} ;'.format(wished_schema_name)
			cursor.execute('USE {} ;'.format(wished_schema_name))

			for command in open(self.parameters['database']['path_to_sql'], 'r'):
				if command != '\n' and not command.startswith('#'):
					cursor.execute(command)

		cursor.close()
		connection.close()

	def get_file_list(self):
		"""GET FILE LIST FROM THE NIH'S FTP"""

		start_time = time.time()

		if not os.path.exists(self.download_folder):  # Create tmp directory to keep file during INSERT
			os.makedirs(self.download_folder)
			inserted_log = open(self.insert_log_path, 'w')
			inserted_log.close()

		gz_file_list = []

		ftp_ncbi = FTP('ftp.ncbi.nlm.nih.gov')  # Connect FTP's root
		ftp_ncbi.login()

		gz_baseline = []  # Baselines
		ftp_ncbi.cwd('/pubmed/baseline/')
		file_list = ftp_ncbi.nlst()
		downloaded_files = os.listdir()
		for file_name in file_list:
			if re.match(self.regex_gz, file_name) is not None:
				gz_baseline.append('baseline/' + file_name)

		gz_update = []  # Updates
		ftp_ncbi.cwd('/pubmed/updatefiles/')
		file_list = ftp_ncbi.nlst()
		downloaded_files = os.listdir()
		for file_name in file_list:
			if re.match(self.regex_gz, file_name) is not None:
				gz_update.append('updatefiles/' + file_name)
		print('{} files in Medline\'s updates'.format(len(gz_update)))

		inserted_log = open(self.insert_log_path, 'r')  # Insert only once
		inserted_list = []
		for inserted_file_name in inserted_log:
			inserted_list.append(inserted_file_name)

		for baseline_file_name in gz_baseline:  # Join baseline + updates if not inserted already
			if baseline_file_name not in inserted_list:
				gz_file_list.append(baseline_file_name)
		for update_file_name in gz_update:
			if update_file_name not in inserted_list:
				gz_file_list.append(update_file_name)

		return gz_file_list

	def download(self, file_name):
		"""DOWNLOAD FILE"""

		os.chdir(self.download_folder)
		ftp_ncbi = FTP('ftp.ncbi.nlm.nih.gov')
		ftp_ncbi.login()
		file_name_dir = re.findall('(.*)/(.*)', file_name)
		ftp_ncbi.cwd('/pubmed/' + str(file_name_dir[0][0]))
		with open(file_name_dir[0][1], 'wb'):
			ftp_ncbi.retrbinary('RETR {}'.format(file_name_dir[0][1]), file_handle.write)
			os.chdir(self.parameters['paths']['program_path'])
		return file_name_dir[0][1]

	def extract(self, file_name):
		"""GZ EXTRACTION"""
		os.chdir(self.download_folder)
		gz_file = gzip.open(file_name, 'rt', encoding='utf-8')
		file_content = gz_file.read()
		os.chdir(self.parameters['paths']['program_path'])
		return file_content

	def parse(self, data):
		"""BS4 XML INDEXATION"""
		soup = BeautifulSoup(data, 'lxml')
		articles = soup.find_all('pubmedarticle')
		return articles

	def get_command(self, article, gz):

		soup_article = BeautifulSoup(str(article), 'lxml')
		article_INSERT_list = []
		pmid_primary_key = re.findall('<articleid idtype="pubmed">([0-9]*)</articleid>', str(article))

		r_year = re.compile('<year>([0-9]{4})</year>')
		r_month = re.compile('<month>([0-9]{2})</month>')
		r_day = re.compile('<day>([0-9]{2})</day>')

		''' - - - - - - - - - - - - - -  
		medline_citation
		- - - - - - - - - - - - - -  '''
		#  date_created
		date_created = soup_article.find_all('datecreated')
		try:
			date_completed_value = [
				re.findall(r_year, str(date_created))[0] + '-' + re.findall(r_month, str(date_created))[0] + '-' +
				re.findall(r_day, str(date_created))[0]]
		except:
			date_completed_value = ['1900-01-01']
		#  date_completed
		date_completed = soup_article.find_all('datecompleted')
		try:
			date_completed_value = [
				re.findall(r_year, str(date_completed))[0] + '-' + re.findall(r_month, str(date_completed))[0] + '-' +
				re.findall(r_day, str(date_completed))[0]]
		except:
			date_completed_value = ['1900-01-01']
		#  date_revised
		date_revised = soup_article.find_all('daterevised')
		try:
			date_revised_value = [
				re.findall(r_year, str(date_revised))[0] + '-' + re.findall(r_month, str(date_revised))[0] + '-' +
				re.findall(r_day, str(date_revised))[0]]
		except:
			date_revised_value = ['1900-01-01']
		#  date_published
		date_published = soup_article.find_all('pubdate')
		#  journal
		journal = soup_article.find_all('journal')
		#  abstract_text_list
		abstract_text_list = re.findall('<abstracttext.*?>(.*?)</abstracttext>', str(article))
		if len(abstract_text_list) > 1:
			abstract_text_raw = ''.join(abstract_text_list)
			abstract_text = re.sub('\"', ' ', str(abstract_text_raw))
		else:
			abstract_text = abstract_text_list
		#  date_of_electronic_publication
		date_of_electronic_publication = soup_article.find_all('articledate', attrs={'datetype': 'Electronic'})
		try:
			date_of_electronic_publication_value = [re.findall(r_year, str(date_of_electronic_publication))[0] + '-' +
													re.findall(r_month, str(date_of_electronic_publication))[0] + '-' +
													re.findall(r_day, str(date_of_electronic_publication))[0]]
		except:
			date_of_electronic_publication_value = ['1900-01-01']
		#  MEDLINE infos
		medline_info_journal = soup_article.find_all('medlinejournalinfo')
		#  INSERT
		article_INSERT_list.append(
			{'name': 'medline_citation',
			 'value': {
				 'pmid': pmid_primary_key,
				 'date_created': date_completed_value,
				 'date_completed': date_completed_value,
				 'date_revised': date_revised_value,
				 'issn': re.findall('<issn issntype=".*">(.*)</issn>', str(article)),
				 'volume': re.findall('<volume>([0-9]*)</volume>', str(article)),
				 'issue': re.findall('<issue>([0-9]*)</issue>', str(article)),
				 'pub_date_year': re.findall('<year>([0-9]{4})</year>', str(date_published)),
				 'pub_date_month': re.findall('<month>([0-9]{2}|\w+)</month>', str(date_published)),
				 'pub_date_day': re.findall('<day>([0-9]{2})</day>', str(date_published)),
				 'medline_date': re.findall('<medlinedate>(.*)</medlinedate>', str(date_published)),
				 'journal_title': re.findall('<title>(.*)</title>', str(journal)),
				 'iso_abbreviation': re.findall('<isoabbreviation>(.*)</isoabbreviation>', str(journal)),
				 'article_title': re.findall('<articletitle>(.*)</articletitle>', str(article)),
				 'medline_pgn': re.findall('<medlinepgn>(.*)</medlinepgn>', str(article)),
				 'abstract_text': abstract_text,
				 'copyright_info': re.findall('<copyrightinformation>(.*)</copyrightinformation>', str(article)),
				 'article_author_list_comp_yn': re.findall('<authorlist completeyn="([A-Z]{1})">', str(article)),
				 'data_bank_list_comp_yn': re.findall('<databanklist completeyn="([A-Z]{1})">', str(article)),
				 'grantlist_complete_yn': re.findall('<grantlist completeyn="([A-Z]{1})">', str(article)),
				 'vernacular_title': re.findall('<vernaculartitle>(.*)</vernaculartitle>', str(article)),
				 'date_of_electronic_publication': date_of_electronic_publication_value,
				 'country': re.findall('<country>(.*)</country>', str(medline_info_journal)),
				 'medline_ta': re.findall('<medlineta>(.*)</medlineta>', str(article)),
				 'nlm_unique_id': re.findall('<nlmuniqueid>(.*)</nlmuniqueid>', str(article)),
				 'xml_file_name': gz,
				 'number_of_references': re.findall('<numberofreferences>(.*)</numberofreferences>', str(article)),
				 'citation_owner': re.findall('<medlinecitation .*?owner="(.*?)".*?>', str(article)),
				 'citation_status': re.findall('<medlinecitation .*?status="([A-Za-z])".*?>', str(article))}
			 }
		)

		''' - - - - - - - - - - - - - -
		medline_article_language
		- - - - - - - - - - - - - -  '''
		languages_list = soup_article.find_all('language')
		for language in languages_list:
			article_INSERT_list.append(
				{'name': 'medline_article_language',
				 'value': {'pmid': pmid_primary_key, 'language': re.findall('<language>(.*)</language>', str(language))}
				 })

		''' - - - - - - - - - - - - - -
		medline_article_publication_type
		- - - - - - - - - - - - - -  '''
		publication_type_list = soup_article.find_all('publicationtype')
		for publication_type in publication_type_list:
			article_INSERT_list.append(
				{'name': 'medline_article_publication_type',
				 'value': {'pmid': pmid_primary_key,
							'publication_type': re.findall('<publicationtype ui=".*?">(.*?)</publicationtype>', str(publication_type))}
				 })

		''' - - - - - - - - - - - - - -
		medline_author
		- - - - - - - - - - - - - -  '''
		author_list = soup_article.find_all('author')
		for author in author_list:
			article_INSERT_list.append(
				{'name': 'medline_author',
				 'value': {'pmid': pmid_primary_key,
							'last_name': re.findall('<lastname>(.*)</lastname>', str(author)),
							'fore_name': re.findall('<forename>(.*)</forename>', str(author)),
							'first_name': re.findall('<firstname>(.*)</firstname>', str(author)),
							'middle_name': re.findall('<middlename>(.*)</middlename>', str(author)),
							'initials': re.findall('<initials>(.*)</initials>', str(author)),
							'suffix': re.findall('<suffix>(.*)</suffix>', str(author)),
							'affiliation': re.findall('<affiliation>(.*)</affiliation>', str(author)),
							'collective_name': re.findall('<collectivename>(.*)</collectivename>', str(author))}
				 })

		''' - - - - - - - - - - - - - -  
		medline_chemical_list
		- - - - - - - - - - - - - -  '''
		chemical_list = soup_article.find_all('chemical')
		for chemical in chemical_list:
			article_INSERT_list.append(
				{'name': 'medline_chemical_list',
				 'value': {'pmid': pmid_primary_key,
							'registry_number': re.findall('<registrynumber>(.*)</registrynumber>', str(chemical)),
							'name_of_substance': re.findall('<nameofsubstance ui=".*">(.*)</nameofsubstance>', str(chemical))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_citation_other_id
		- - - - - - - - - - - - - - '''
		other_ids_list = soup_article.find_all('otherid')
		for other_id in other_ids_list:
			article_INSERT_list.append(
				{'name': 'medline_citation_other_id',
				 'value': {'pmid': pmid_primary_key,
							'source': re.findall('<otherid source="(.*)">.*</otherid>', str(other_id)),
							'other_id': re.findall('<otherid source=".*">(.*)</otherid>', str(other_id))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_citation_subsets
		- - - - - - - - - - - - - - '''
		citation_subsets_list = soup_article.find_all('citationsubset')
		for citation_subsets in citation_subsets_list:
			article_INSERT_list.append(
				{'name': 'medline_citation_subsets',
				 'value': {'pmid': pmid_primary_key,
							'citation_subset': re.findall('<citationsubset>(.*)</citationsubset>', str(citation_subsets))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_comments_corrections
		- - - - - - - - - - - - - - '''
		medline_comments_corrections_list = soup_article.find_all('commentscorrections')
		for comment in medline_comments_corrections_list:
			article_INSERT_list.append(
				{'name': 'medline_comments_corrections',
				 'value': {'pmid': pmid_primary_key,
							'ref_pmid': re.findall('<pmid version="1">(\d+)</pmid>', str(comment)),
							'type': re.findall('<commentscorrections reftype="(.*?)">', str(comment)),
							'ref_source': re.findall('<refsource>(.*)</refsource>', str(comment))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_data_bank
		- - - - - - - - - - - - - - '''
		medline_data_bank_list = soup_article.find_all('accessionnumber')
		for databank in medline_data_bank_list:
			article_INSERT_list.append(
				{'name': 'medline_data_bank',
				 'value': {'pmid': pmid_primary_key,
							'accession_number': re.findall('<accessionnumber>(.*)</accessionnumber>', str(databank))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_grant
		- - - - - - - - - - - - - - '''
		medline_grant_list = soup_article.find_all('grant')
		for grant in medline_grant_list:
			article_INSERT_list.append(
				{'name': 'medline_grant',
				 'value': {'pmid': pmid_primary_key,
							'grant_id': re.findall('<grantid>(.*)</grantid>', str(grant)),
							'acronym': re.findall('<acronym>(.*)</acronym>', str(grant)),
							'agency': re.findall('<agency>(.*)</agency>', str(grant)),
							'country': re.findall('<country>(.*)</country>', str(grant))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_investigator
		- - - - - - - - - - - - - - '''
		medline_investigator_list = soup_article.find_all('investigator')
		for investigator in medline_investigator_list:
			article_INSERT_list.append(
				{'name': 'medline_investigator',
				 'value': {'pmid': pmid_primary_key,
							'last_name': re.findall('<lastname>(.*)</lastname>', str(investigator)),
							'fore_name': re.findall('<forename>(.*)</forename>', str(investigator)),
							'first_name': re.findall('<firstname>(.*)</firstname>', str(investigator)),
							'middle_name': re.findall('<middlename>(.*)</middlename>', str(investigator)),
							'initials': re.findall('<initials>(.*)</initials>', str(investigator)),
							'suffix': re.findall('<suffix>(.*)</suffix>', str(investigator)),
							'affiliation': re.findall('<affiliation>(.*)</affiliation>', str(investigator))}
				 })

		''' - - - - - - - - - - - - - - 
		medline_mesh_heading
		- - - - - - - - - - - - - - '''
		medline_mesh_heading_list = soup_article.find_all('meshheading')
		for mesh in medline_mesh_heading_list:
			article_INSERT_list.append(
				{'name': 'medline_mesh_heading',
				 'value': {'pmid': pmid_primary_key,
							'descriptor_name': re.findall(
								'<descriptorname .*majortopicyn="[A-Z]{1}".*?>(.*?)</descriptorname>', str(mesh)),

							'descriptor_ui': re.findall(
								'<descriptorname .*?ui="(D\d+)".*?>.*?</descriptorname>', str(mesh)),

							'descriptor_name_major_yn': re.findall(
								'<descriptorname .*?majortopicyn="([A-Z]{1})".*?>.*?</descriptorname>', str(mesh)),
							'qualifier_name': re.findall(
								'<qualifiername .*?>(.*?)</qualifiername>', str(mesh)),

							'qualifier_ui': re.findall(
								'<qualifiername .*?ui="(Q\d+)">.*?</qualifiername>', str(mesh)),

							'qualifier_name_major_yn': re.findall(
								'<qualifiername .*?majortopicyn="([A-Z]{1})".*?>.*?</qualifiername>', str(mesh))
							}
				 })

		''' - - - - - - - - - - - - - - 
		medline_personal_name_subject
		- - - - - - - - - - - - - - '''
		medline_personal_name_subject_list = soup_article.find_all('personalnamesubject')
		for subject in medline_personal_name_subject_list:
			article_INSERT_list.append(
				{'name': 'medline_personal_name_subject',
				 'value': {'pmid': pmid_primary_key,
							'last_name': re.findall('<lastname>(.*)</lastname>', str(subject)),
							'fore_name': re.findall('<forename>(.*)</forename>', str(subject)),
							'first_name': re.findall('<firstname>(.*)</firstname>', str(subject)),
							'middle_name': re.findall('<middlename>(.*)</middlename>', str(subject)),
							'initials': re.findall('<initials>(.*)</initials>', str(subject)),
							'suffix': re.findall('<suffix>(.*)</suffix>', str(subject))}
				 })

		#  Final return, for every articles
		return article_INSERT_list

	def remove(self, file_name):
		"""REMOVE FILE AND WRITE ITS NAME ON ALREADY DONE LOG"""
		with open(self.insert_log_path, 'a') as inserted_log:
			inserted_log.write('{}\n'.format(file_name))
		os.chdir(self.download_folder)
		file_name = re.findall('(.*)/(.*)', file_name)[0][1]
		os.remove('./' + file_name)

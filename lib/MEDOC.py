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
import logging
import calendar
import configparser
from ftplib import FTP
import mysql.connector
from bs4 import BeautifulSoup


class MEDOC(object):

	def __init__(self):
		"""INIT"""
		self.parameters = self.config = configparser.ConfigParser()
		self.parameters.read('./configuration.cfg')
		self.regex_gz = re.compile('^pubmed.*.xml.gz$')
		self.insert_log_path = os.path.join(self.parameters['paths']['program_path'], self.parameters['paths']['already_downloaded_files'])
		self.download_folder = os.path.join(self.parameters['paths']['program_path'], self.parameters['paths']['pubmed_data_download'])
		self.calendar = {v.lower(): k for k, v in enumerate(calendar.month_abbr) if v != ''}

	def clean_xml(self, string):
		""""""
		string = re.sub('<.*?>', '', string)
		return string

	def create_pubmedDB(self):
		"""DATABASE CREATION"""

		wished_schema_name = self.parameters['database']['database']

		#  mySQL connexion
		config = {
				'host': self.parameters['database']['host'],
				'user': self.parameters['database']['user'],
				'password': self.parameters['database']['password'],
				'use_pure': True,
				'raise_on_warnings': True,
				'get_warnings': True,
				'autocommit': True
				}
		connection = mysql.connector.connect(**config, buffered=True)
		cursor = connection.cursor()
		cursor.execute('SHOW DATABASES ;')  #  Check if 'pubmed' db exists, if not, create it by executing SQL file line by line
		local_dbNames = [db[0] for db in cursor]

		if wished_schema_name in local_dbNames:
			cursor.execute('USE {} ;'.format(wished_schema_name))
			cursor.execute('SHOW TABLES ;')

		else:
			cursor.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;'.format(wished_schema_name))
			cursor.execute('USE {} ;'.format(wished_schema_name))
			logging.info('DB {} created.'.format(wished_schema_name))

			for command in open(self.parameters['database']['path_to_sql'], 'r'):
				if command != '\n' and not command.startswith('#'):
					cursor.execute(command)

		cursor.close()
		connection.close()

	def get_file_list(self):
		"""GET FILE LIST FROM THE NIH'S FTP"""

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
		for file_name in file_list:
			if re.match(self.regex_gz, file_name) is not None:
				gz_baseline.append('baseline/' + file_name)
		logging.info('BASELINE: {} files'.format(len(gz_baseline)))

		gz_update = []  # Updates
		ftp_ncbi.cwd('/pubmed/updatefiles/')
		file_list = ftp_ncbi.nlst()
		for file_name in file_list:
			if re.match(self.regex_gz, file_name) is not None:
				gz_update.append('updatefiles/' + file_name)
		logging.info('UPDATE: {} files'.format(len(gz_update)))

		inserted_log = open(self.insert_log_path, 'r')  # Insert only once
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

		tst = time.time()

		ftp_ncbi = FTP('ftp.ncbi.nlm.nih.gov')
		ftp_ncbi.login()
		file_name_dir = file_name.split('/')

		ftp_ncbi.cwd('/pubmed/{}'.format(file_name_dir[0]))
		with open(os.path.join(self.download_folder, file_name_dir[1]), 'wb') as file_handle:
			ftp_ncbi.retrbinary('RETR {}'.format(file_name_dir[1]), file_handle.write)
		tsp = time.time()
		logging.info('Downloading file {} ({} min)'.format(file_name, round((tsp - tst) / 60, 2)))
		return file_name_dir[1]

	def extract_articles(self, file_name):
		"""GZ EXTRACTION AND INDEXATION"""
		tst = time.time()
		with gzip.open(os.path.join(self.download_folder, file_name), 'rt', encoding='utf-8') as file_handler:  # Streaming file
			soup = BeautifulSoup(file_handler.read(), 'xml')  # Indexing XML
		articles = soup.find_all('PubmedArticle')  # Get data
		tsp = time.time()
		logging.info('Parsing {} articles ({} min)'.format(len(articles), round((tsp - tst) / 60, 2)))
		return articles

	def get_data(self, article, gz):

		soup_article = BeautifulSoup(str(article), 'lxml')

		article_INSERT_list = []

		# Preprocessings
		try:
			pmid_primary_key = soup_article.pmid.text
		except AttributeError:  # No PMID, no article. Simple.
			return None

		# Abstract
		abstract_text = ''.join(soup_article.abstract.text.splitlines()) if soup_article.abstract else None

		# Medline date
		try:
			medline_date = '{}-{}-{}'.format(soup_article.pubdate.year.text, self.calendar[soup_article.pubdate.month.text.lower()] if soup_article.pubdate.month and re.search('[a-z]', soup_article.pubdate.month.text) else soup_article.pubdate.month.text, soup_article.pubdate.day.text) if soup_article.pubdate and soup_article.pubdate.year is not None and soup_article.pubdate.month is not None and soup_article.pubdate.day is not None else None
		except AttributeError:
			medline_date = None

		try:
			date_completed = '{}-{}-{}'.format(soup_article.datecompleted.year.text, self.calendar[soup_article.datecompleted.month.text.lower()] if re.search('[a-z]', soup_article.datecompleted.month.text) else soup_article.datecompleted.month.text, soup_article.datecompleted.day.text) if soup_article.datecompleted else None
		except AttributeError:
			date_completed = None

		# Now, get data for each table as dict() with data for each table in a subdict()
		article_INSERT_list.append(  # medline_citation
			{'medline_citation':
				{
					'pmid': pmid_primary_key,
					'date_created': '{}-{}-{}'.format(soup_article.datecreated.year.text, self.calendar[soup_article.datecreated.month.text.lower()] if re.search('[a-z]', soup_article.datecreated.month.text) else soup_article.datecreated.month.text, soup_article.datecreated.day.text) if soup_article.datecreated else None,
					'date_completed': date_completed,
					'date_revised': '{}-{}-{}'.format(soup_article.daterevised.year.text, self.calendar[soup_article.daterevised.month.text.lower()] if re.search('[a-z]', soup_article.daterevised.month.text) else soup_article.daterevised.month.text, soup_article.daterevised.day.text) if soup_article.daterevised else None,
					'issn': soup_article.journal.issn.text if soup_article.journal and soup_article.journal.issn else None,
					'volume': soup_article.journal.volume.text if soup_article.journal and soup_article.journal.volume else None,
					'issue': soup_article.journal.issue.text if soup_article.journal and soup_article.journal.issue else None,
					'pub_date_year': soup_article.pubdate.year.text if soup_article.pubdate and soup_article.pubdate.year else None,
					'pub_date_month': soup_article.pubdate.month.text if soup_article.pubdate and soup_article.pubdate.month else None,
					'pub_date_day': soup_article.pubdate.day.text if soup_article.pubdate and soup_article.pubdate.day else None,
					'medline_date': medline_date,
					'journal_title': soup_article.journal.title.text if soup_article.journal and soup_article.journal.title else None,
					'iso_abbreviation': soup_article.journal.isoabbreviation.text if soup_article.journal and soup_article.journal.isoabbreviation else None,
					'article_title': soup_article.articletitle.text if soup_article.articletitle else None,
					'medline_pgn': soup_article.medlinepgn.text if soup_article.medlinepgn else None,
					'abstract_text': abstract_text,
					'copyright_info': soup_article.copyright_info.text if soup_article.copyright_info else None,
					'article_author_list_comp_yn': soup_article.authorlist['completeyn'] if soup_article.authorlist else None,
					'data_bank_list_comp_yn': soup_article.databanklist['completeyn'] if soup_article.databanklist else None,
					'grantlist_complete_yn': soup_article.grantlist['completeyn'] if soup_article.grantlist else None,
					'vernacular_title': soup_article.articletitle.text if soup_article.articletitle else None,
					'date_of_electronic_publication': None,
					'country': soup_article.country.text if soup_article.country else None,
					'medline_ta': soup_article.medlineta.text if soup_article.medlineta else None,
					'nlm_unique_id': soup_article.nlmuniqueid.text if soup_article.nlmuniqueid else None,
					'xml_file_name': gz,
					'number_of_references': soup_article.numberofreferences.text if soup_article.numberofreferences is not None else None,
					'citation_owner': soup_article.medlinecitation['owner'] if soup_article.medlinecitation else None,
					'citation_status': soup_article.medlinecitation['status'] if soup_article.medlinecitation else None,
					'medline_info_journal': soup_article.medlinejournalinfo.nlmuniqueid.text if soup_article.medlinejournalinfo and soup_article.medlinejournalinfo.nlmuniqueid else None
					}
				}
			)

		if soup_article.language:  # medline_article_language
			article_INSERT_list.append(
				{'medline_article_language': {
						'pmid': pmid_primary_key,
						'language': soup_article.language.text
						}
					}
				)

		publication_type_list = soup_article.find_all('publicationtype')  # medline_article_publication_type
		if len(publication_type_list) > 0:
			publication_types = ';'.join([publication_type.text for publication_type in publication_type_list])
			article_INSERT_list.append(
				{'medline_article_publication_type': {
						'pmid': pmid_primary_key,
						'publication_type': publication_types
						}
					}
				)

		author_list = soup_article.find_all('author')  # medline_author
		for author in author_list:  # Same here, loop over authors
			article_INSERT_list.append(
				{'medline_author': {
						'pmid': pmid_primary_key,
						'last_name': author.lastname.text if author.lastname else None,
						'fore_name': author.forename.text if author.forename else None,
						'first_name': author.firstname.text if author.firstname else None,
						'middle_name': author.middlename.text if author.middlename else None,
						'initials': author.initials.text if author.initials else None,
						'suffix': author.suffix.text if author.suffix else None,
						'affiliation': author.affiliation.text if author.affiliation else None,
						'collective_name': author.collectivename.text if author.collectivename else None
						}
					}
				)

		chemical_list = soup_article.find_all('chemical')  # medline_chemical_list
		for chemical in chemical_list:
			article_INSERT_list.append(
				{'medline_chemical_list': {
						'pmid': pmid_primary_key,
						'registry_number': chemical.registrynumber.text if chemical.registrynumber else None,
						'name_of_substance': chemical.nameofsubstance.text if chemical.nameofsubstance else None
						}
					}
				)

		other_ids_list = soup_article.find_all('otherid')  # medline_citation_other_id
		for other_id in other_ids_list:
			article_INSERT_list.append(
				{'medline_citation_other_id': {
						'pmid': pmid_primary_key,
						'source': other_id['source'],
						'other_id': other_id.text
						}
					}
				)

		citation_subsets_list = soup_article.find_all('citationsubset')  # medline_citation_subsets
		for citation_subsets in citation_subsets_list:
			if citation_subsets.text:
				article_INSERT_list.append(
					{'medline_citation_subsets': {
							'pmid': pmid_primary_key,
							'citation_subset': citation_subsets.text
							}
						}
					)

		medline_comments_corrections_list = soup_article.find_all('commentscorrections')  # medline_comments_corrections
		for comment in medline_comments_corrections_list:
			article_INSERT_list.append(
				{'medline_comments_corrections': {
						'pmid': pmid_primary_key,
						'ref_pmid': comment.pmid.text if comment.pmid else None,
						'type': comment.commentscorrections['reftype'] if comment.commentscorrections else None,
						'ref_source': comment.refsource.text if comment.refsource else None
						}
					}
				)

		medline_data_bank_list = soup_article.find_all('accessionnumber')  # medline_data_bank
		for databank in medline_data_bank_list:
			if databank.accessionnumber:
				article_INSERT_list.append(
					{'medline_data_bank': {
							'pmid': pmid_primary_key,
							'accession_number': databank.accessionnumber.text if databank.accessionnumber else None
							}
						}
					)

		medline_grant_list = soup_article.find_all('grant')  # medline_grant
		for grant in medline_grant_list:
			article_INSERT_list.append(
				{'medline_grant': {
						'pmid': pmid_primary_key,
						'grant_id': grant.grantid.text if grant.grantid else None,
						'acronym': grant.acronym.text if grant.acronym else None,
						'agency': grant.agency.text if grant.agency else None,
						'country': grant.country.text if grant.country else None
						}
					}
				)

		medline_mesh_heading_list = soup_article.find_all('meshheading')  # medline_mesh_heading
		for mesh in medline_mesh_heading_list:
			try:
				qualifier_name_major_yn = mesh.qualifiername['majortopicyn'] if mesh.qualifiername and 'majortopicyn' in mesh.qualifiername.keys() else None
			except TypeError:
				qualifier_name_major_yn = None
			article_INSERT_list.append(
				{'medline_mesh_heading': {
						'pmid': pmid_primary_key,
						'descriptor_name': mesh.descriptorname.text if mesh.descriptorname else None,
						'descriptor_ui': mesh.descriptorname['ui'] if mesh.descriptorname else None,
						'descriptor_name_major_yn': mesh.descriptorname['majortopicyn'] if mesh.descriptorname else None,
						'qualifier_name': mesh.qualifiername.text if mesh.qualifiername else None,
						'qualifier_ui': mesh.qualifiername['ui'] if mesh.qualifiername else None,
						'qualifier_name_major_yn': qualifier_name_major_yn
						}
					}
				)

		medline_investigator_list = soup_article.find_all('investigator')  # medline_investigator
		for investigator in medline_investigator_list:
			article_INSERT_list.append(
				{'medline_investigator': {
						'pmid': pmid_primary_key,
						'last_name': investigator.lastname.text if investigator.lastname else None,
						'fore_name': investigator.forename.text if investigator.forename else None,
						'first_name': investigator.firstname.text if investigator.firstname else None,
						'middle_name': investigator.middlename.text if investigator.middlename else None,
						'initials': investigator.initials.text if investigator.initials else None,
						'suffix': investigator.suffix.text if investigator.suffix else None,
						'affiliation': investigator.affiliation.text if investigator.affiliation else None
						}
					}
				)

		medline_personal_name_subject_list = soup_article.find_all('personalnamesubject')  # medline_personal_name_subject
		for subject in medline_personal_name_subject_list:
			article_INSERT_list.append(
				{'medline_personal_name_subject': {
						'pmid': pmid_primary_key,
						'last_name': subject.lastname.text if subject.lastname else None,
						'fore_name': subject.forename.text if subject.forename else None,
						'first_name': subject.firstname.text if subject.firstname else None,
						'middle_name': subject.middlename.text if subject.middlename else None,
						'initials': subject.initials.text if subject.initials else None,
						'suffix': subject.suffix.text if subject.suffix else None
						}
					}
				)

		return article_INSERT_list

	def insert_data(self, data, gz, pmid, QueryExecutor):
		"""Each insertion step is parallelized"""
		for chunk in data:
			for table, data in chunk.items():
				sql_command = 'INSERT INTO {} ({}) VALUES ({}) ;'.format(
					table,
					', '.join([key for key in data.keys()]),
					', '.join(['%({})s'.format(key) for key in data.keys()]))
				QueryExecutor.execute(sql_command=sql_command, sql_data=data, pmid=pmid)

	def remove(self, file_name):
		"""REMOVE FILE AND WRITE ITS NAME ON ALREADY DONE LOG"""
		with open(self.insert_log_path, 'a') as inserted_log:
			inserted_log.write('{}\n'.format(file_name))
		try:
			os.remove(os.path.join(self.download_folder, file_name.split('/')[1]))
			return True
		except Exception as E:
			return E

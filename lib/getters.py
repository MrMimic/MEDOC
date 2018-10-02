#!/usr/bin/env python3
# coding: utf8

# ==============================================================================
# Title: MEDOC
# Description: MEDOC GETTERS
# Author: Emeric Dynomant
# Contact: emeric.dynomant@gmail.com
# Date: 11/08/2017
# Language release: python 3.5.2
# ==============================================================================


import sys
import pymysql.cursors
from lib.sql_helper import Query_Executor


''' - - - - - - - - - - - - - -  
medline_citation
- - - - - - - - - - - - - -  '''

def get_medline_citation(insert_table):
	# Table fields list
	fields_medline_citation = ['date_completed', 'pub_date_day', 'citation_owner', 'iso_abbreviation', 'article_title',
								'volume', 'vernacular_title', 'pub_date_year', 'date_revised',
								'date_of_electronic_publication', 'article_author_list_comp_yn', 'medline_pgn',
								'date_created', 'country', 'xml_file_name', 'medline_date', 'number_of_references',
								'data_bank_list_comp_yn', 'nlm_unique_id', 'abstract_text', 'citation_status',
								'grantlist_complete_yn', 'copyright_info', 'issue', 'journal_title', 'issn',
								'pub_date_month', 'pmid', 'medline_ta']
	values_medline_citation = []

	for field in fields_medline_citation:  # For every fields
		for key, value in insert_table['value'].items():
			if field == key:  # If parsed value field == actual field
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_citation.append(value_to_append)  # Add it to a list
	return values_medline_citation, fields_medline_citation

def send_medline_citation(fields_medline_citation, values_tot_medline_citation, parameters):
	sql_command = 'INSERT INTO ' + 'medline_citation' + ' (' + ', '.join(
		fields_medline_citation) + ') VALUES ' + ', '.join(values_tot_medline_citation) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_article_language
- - - - - - - - - - - - - -  '''

def get_medline_article_language(insert_table):
	fields_medline_article_language = ['pmid', 'language']
	values_medline_article_language = []
	for field in fields_medline_article_language:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_article_language.append(value_to_append)
	return values_medline_article_language, fields_medline_article_language

def send_medline_article_language(fields_medline_article_language, values_tot_medline_article_language, parameters):
	sql_command = 'INSERT INTO ' + 'medline_article_language' + ' (' + ', '.join(
		fields_medline_article_language) + ') VALUES ' + ', '.join(values_tot_medline_article_language) + ' ;'

	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_article_publication_type
- - - - - - - - - - - - - -  '''

def get_medline_article_publication_type(insert_table):
	fields_medline_article_publication_type = ['pmid', 'publication_type']
	values_medline_article_publication_type = []
	for field in fields_medline_article_publication_type:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_article_publication_type.append(value_to_append)
	return values_medline_article_publication_type, fields_medline_article_publication_type

def send_medline_article_publication_type(fields_medline_article_publication_type, values_tot_medline_article_publication_type, parameters):
	sql_command = 'INSERT INTO ' + 'medline_article_publication_type' + ' (' + ', '.join(fields_medline_article_publication_type) + ') VALUES ' + ', '.join(values_tot_medline_article_publication_type) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_author
- - - - - - - - - - - - - -  '''

def get_medline_author(insert_table):
	fields_medline_author = ['pmid', 'last_name', 'fore_name', 'first_name', 'middle_name', 'initials', 'suffix', 'affiliation', 'collective_name']
	values_medline_author = []
	for field in fields_medline_author:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_author.append(value_to_append)
	return values_medline_author, fields_medline_author

def send_medline_author(fields_medline_author, values_tot_medline_author, parameters):
	sql_command = 'INSERT INTO ' + 'medline_author' + ' (' + ', '.join(fields_medline_author) + ') VALUES ' + ', '.join(values_tot_medline_author) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_chemical_list
- - - - - - - - - - - - - -  '''

def get_medline_chemical_list(insert_table):
	fields_medline_chemical_list = ['pmid', 'registry_number', 'name_of_substance']
	values_medline_chemical_list = []
	for field in fields_medline_chemical_list:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_chemical_list.append(value_to_append)
	return values_medline_chemical_list, fields_medline_chemical_list

def send_medline_chemical_list(fields_medline_chemical_list, values_tot_medline_chemical_list, parameters):
	sql_command = 'INSERT INTO ' + 'medline_chemical_list' + ' (' + ', '.join(fields_medline_chemical_list) + ') VALUES ' + ', '.join(values_tot_medline_chemical_list) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_citation_other_id
- - - - - - - - - - - - - -  '''

def get_medline_citation_other_id(insert_table):
	fields_medline_citation_other_id = ['pmid', 'source', 'other_id']
	values_medline_citation_other_id = []
	for field in fields_medline_citation_other_id:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_citation_other_id.append(value_to_append)
	return values_medline_citation_other_id, fields_medline_citation_other_id

def send_medline_citation_other_id(fields_medline_citation_other_id, values_tot_medline_citation_other_id, parameters):
	sql_command = 'INSERT INTO ' + 'medline_citation_other_id' + ' (' + ', '.join(fields_medline_citation_other_id) + ') VALUES ' + ', '.join(values_tot_medline_citation_other_id) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_citation_subsets
- - - - - - - - - - - - - -  '''

def get_medline_citation_subsets(insert_table):
	fields_medline_citation_subsets = ['pmid', 'citation_subset']
	values_medline_citation_subsets = []
	for field in fields_medline_citation_subsets:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_citation_subsets.append(value_to_append)
	return values_medline_citation_subsets, fields_medline_citation_subsets

def send_medline_citation_subsets(fields_medline_citation_subsets, values_tot_medline_citation_subsets, parameters):
	sql_command = 'INSERT INTO ' + 'medline_citation_subsets' + ' (' + ', '.join(fields_medline_citation_subsets) + ') VALUES ' + ', '.join(values_tot_medline_citation_subsets) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_comments_corrections
- - - - - - - - - - - - - -  '''

def get_medline_comments_corrections(insert_table):
	fields_medline_comments_corrections = ['pmid', 'ref_pmid', 'type', 'ref_source']
	values_medline_comments_corrections = []
	for field in fields_medline_comments_corrections:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_comments_corrections.append(value_to_append)
	return values_medline_comments_corrections, fields_medline_comments_corrections

def send_medline_comments_corrections(fields_medline_comments_corrections, values_tot_medline_comments_corrections, parameters):
	sql_command = 'INSERT INTO ' + 'medline_comments_corrections' + ' (' + ', '.join(fields_medline_comments_corrections) + ') VALUES ' + ', '.join(values_tot_medline_comments_corrections) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_data_bank
- - - - - - - - - - - - - -  '''

def get_medline_data_bank(insert_table):
	fields_medline_data_bank = ['pmid', 'accession_number']
	values_medline_data_bank = []
	for field in fields_medline_data_bank:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_data_bank.append(value_to_append)
	return values_medline_data_bank, fields_medline_data_bank

def send_medline_data_bank(fields_medline_data_bank, values_tot_medline_data_bank, parameters):
	sql_command = 'INSERT INTO ' + 'medline_data_bank' + ' (' + ', '.join(fields_medline_data_bank) + ') VALUES ' + ', '.join(values_tot_medline_data_bank) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_grant
- - - - - - - - - - - - - -  '''

def get_medline_grant(insert_table):
	fields_medline_grant = ['pmid', 'grant_id', 'acronym', 'agency', 'country']
	values_medline_grant = []
	for field in fields_medline_grant:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_grant.append(value_to_append)
	return values_medline_grant, fields_medline_grant

def send_medline_grant(fields_medline_grant, values_tot_medline_grant, parameters):
	sql_command = 'INSERT INTO ' + 'medline_grant' + ' (' + ', '.join(fields_medline_grant) + ') VALUES ' + ', '.join(values_tot_medline_grant) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_investigator
- - - - - - - - - - - - - -  '''

def get_medline_investigator(insert_table):
	fields_medline_investigator = ['pmid', 'last_name', 'fore_name', 'first_name', 'middle_name', 'initials', 'suffix', 'affiliation']
	values_medline_investigator = []
	for field in fields_medline_investigator:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_investigator.append(value_to_append)
	return values_medline_investigator, fields_medline_investigator

def send_medline_investigator(fields_medline_investigator, values_tot_medline_investigator, parameters):
	sql_command = 'INSERT INTO ' + 'medline_investigator' + ' (' + ', '.join(fields_medline_investigator) + ') VALUES ' + ', '.join(values_tot_medline_investigator) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_mesh_heading
- - - - - - - - - - - - - -  '''


def get_medline_mesh_heading(insert_table):
	fields_medline_mesh_heading = ['pmid', 'descriptor_name', 'descriptor_ui', 'descriptor_name_major_yn', 'qualifier_name', 'qualifier_ui', 'qualifier_name_major_yn']
	values_medline_mesh_heading = []
	for field in fields_medline_mesh_heading:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_mesh_heading.append(value_to_append)
	return values_medline_mesh_heading, fields_medline_mesh_heading

def send_medline_mesh_heading(fields_medline_mesh_heading, values_tot_medline_mesh_heading, parameters):
	sql_command = 'INSERT INTO ' + 'medline_mesh_heading' + ' (' + ', '.join(fields_medline_mesh_heading) + ') VALUES ' + ', '.join(values_tot_medline_mesh_heading) + ' ;'
	Query_Executor(parameters).execute(sql_command)


''' - - - - - - - - - - - - - -  
medline_personal_name_subject
- - - - - - - - - - - - - -  '''

def get_medline_personal_name_subject(insert_table):
	fields_medline_personal_name_subject = ['pmid', 'last_name', 'fore_name', 'first_name', 'middle_name', 'initials', 'suffix']
	values_medline_personal_name_subject = []
	for field in fields_medline_personal_name_subject:
		for key, value in insert_table['value'].items():
			if field == key:
				try:
					value_to_append = '"' + (list(value)[0]).replace('"', '') + '"'
				except KeyError:
					value_to_append = '"N/A"'
				values_medline_personal_name_subject.append(value_to_append)
	return values_medline_personal_name_subject, fields_medline_personal_name_subject

def send_medline_personal_name_subject(fields_medline_personal_name_subject, values_tot_medline_personal_name_subject, parameters):
	sql_command = 'INSERT INTO ' + 'medline_personal_name_subject' + ' (' + ', '.join(fields_medline_personal_name_subject) + ') VALUES ' + ', '.join(values_tot_medline_personal_name_subject) + ' ;'
	Query_Executor(parameters).execute(sql_command)

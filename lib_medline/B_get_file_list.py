
import os
import re
import time
from ftplib import FTP

regex_gz = re.compile('^medline.*.xml.gz$')

''' Step 1: get file list on NCBI '''
def get_file_list(parameters):
	print('- ' * 30 + 'EXTRACTING FILES LIST FROM FTP')
	# Timestamp
	start_time = time.time()
	# Create directory to keep file during INSERT
	if not os.path.exists(parameters['paths']['pubmed_data_download']):
		os.makedirs(parameters['paths']['pubmed_data_download'])
		inserted_log = open(parameters['paths']['already_downloaded_files'], 'w')
		inserted_log.close()
	# List of files to download
	gz_file_list = []
	# Connect FTP's root
	ftp_ncbi = FTP('ftp.ncbi.nlm.nih.gov')
	ftp_ncbi.login()
	# BASELINE
	gz_baseline = []
	ftp_ncbi.cwd('/pubmed/baseline/')
	file_list = ftp_ncbi.nlst()
	downloaded_files = os.listdir()
	for file_name in file_list:
		if re.match(regex_gz, file_name) is not None:
			gz_baseline.append('baseline/' + file_name)
	print('{} files in Medline\'s baseline'.format(len(gz_baseline)))
	# UPDATES
	gz_update = []
	ftp_ncbi.cwd('/pubmed/updatefiles/')
	file_list = ftp_ncbi.nlst()
	downloaded_files = os.listdir()
	for file_name in file_list:
		if re.match(regex_gz, file_name) is not None:
			gz_update.append('updatefiles/' + file_name)
	print('{} files in Medline\'s updates'.format(len(gz_update)))
	# If already INSERTED before
	inserted_log = open(parameters['paths']['already_downloaded_files'], 'r')
	inserted_list = []
	for inserted_file_name in inserted_log:
		inserted_list.append(inserted_file_name)
	# Join baseline + updates if not inserted already
	for baseline_file_name in gz_baseline:
		if baseline_file_name not in inserted_list:
			gz_file_list.append(baseline_file_name)
	for update_file_name in gz_update:
		if update_file_name not in inserted_list:
			gz_file_list.append(update_file_name)
	
	print('{} files to download not in your database'.format(len(gz_file_list) - len(inserted_list)))
	print('Elapsed time: {} sec for module: {}'.format(round(time.time()-start_time, 2), get_file_list.__name__))
	
	return gz_file_list

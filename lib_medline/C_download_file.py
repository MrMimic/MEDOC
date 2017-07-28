
import re
import os
import time
from ftplib import FTP

''' Step 3 : download a file '''
def download(file_name, parameters):
	print('- ' * 30 + 'DOWNLOADING FILE')
	# Timestamp
	start_time = time.time()
	# Go to storage directory
	os.chdir(parameters['paths']['pubmed_data_download'])
	# Connect FTP root
	ftp_ncbi = FTP('ftp.ncbi.nlm.nih.gov')
	ftp_ncbi.login()
	# Change FTP directory
	file_name_dir = re.findall('(.*)/(.*)', file_name)
	ftp_ncbi.cwd('/pubmed/' + str(file_name_dir[0][0]))
	# Download file
	file_handle = open(file_name_dir[0][1], 'wb')
	with file_handle:
		print('Downloading {} ..'.format(file_name))
		ftp_ncbi.retrbinary('RETR {}'.format(file_name_dir[0][1]), file_handle.write)		
		os.chdir(parameters['paths']['program_path'])
		print('Elapsed time: {} sec for module: {}'.format(round(time.time()-start_time, 2), download.__name__))
	
	return file_name_dir[0][1]

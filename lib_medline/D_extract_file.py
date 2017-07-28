
import re
import os
import time
import gzip

''' Step : Unzip downloaded files '''
def extract(file_name, parameters):
	print('- ' * 30 + 'FILE EXTRACTION')
	# Timestamp
	start_time = time.time()
	os.chdir(parameters['paths']['pubmed_data_download'])
	# Extraction
	gz_file = gzip.open(file_name, 'rb')
	file_content = gz_file.read()
	os.chdir(parameters['paths']['program_path'])
	print('Elapsed time: {} sec for module: {}'.format(round(time.time()-start_time, 2), extract.__name__))
	
	return file_content

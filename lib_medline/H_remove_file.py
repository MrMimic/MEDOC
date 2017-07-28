
import os
import re

''' Step 8: remove file and add file_name to a list to ignore this file next time '''
def remove(file_to_download, parameters):
	inserted_log = open(parameters['paths']['already_downloaded_files'], 'a')
	inserted_log.write('{}\n'.format(file_to_download))
	inserted_log.close()
	os.chdir(parameters['paths']['pubmed_data_download'])
	file_name = re.findall('(.*)/(.*)', file_to_download)[0][1]
	os.remove('./' + file_name)
# DATA DIR


import re
import os
import time
from bs4 import BeautifulSoup

''' Step : Unzip downloaded files '''
def parse(file_content):
	print('- ' * 30 + 'XML FILE PARSING')
	# Timestamp
	start_time = time.time()
	# Souping
	soup = BeautifulSoup(file_content, 'lxml')
	articles = soup.find_all('pubmedarticle')
	print('Elapsed time: {} sec for module: {}'.format(round(time.time()-start_time, 2), parse.__name__))
	
	return articles

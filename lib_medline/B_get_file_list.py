
import os
import re
import time
from ftplib import FTP

regex_gz = re.compile('^medline.*.xml.gz$')

''' Step 1: get file list on NCBI '''


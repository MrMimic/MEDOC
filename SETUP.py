# python3 SETUP.py build_ext --inplace

''' External dependencies '''

print('Packages installation, please launch following command with root privileges:')

try:
	import pip
	print('pip already installed')
except:
	print('sudo apt-get install -U python3-pip')

try:
	import Cython
	print('Cython already installed')
except:
	print('sudo pip3 install -U Cython')
	
try:
	import pymysql
	print('pymysql already installed')
except:
	print('sudo pip3 install -U pymysql')
	
try:
	import bs4
	print('bs4 already installed')
except:
	print('sudo pip3 install bs4')
	
print('sudo pip3 install -U lxml')

''' Cythonizer '''
		
from distutils.core import setup
from Cython.Build import cythonize
import os

setup(
	ext_modules = cythonize('lib_medline/python_functions/*.py'),
)

os.system('mv *.so lib_medline/')
os.system('mv lib_medline/python_functions/*.c lib_medline/')

# To execute this file, please launch
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
	import mysql.connector
	print('mysql.connector already installed')
except:
	print('sudo pip3 install -U mysql-connector-python')
	
try:
	import bs4
	print('bs4 already installed')
except:
	print('sudo pip3 install bs4')
	
print('sudo pip3 install -U lxml')

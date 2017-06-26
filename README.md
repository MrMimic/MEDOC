# MEDOC (MEdline DOwnloading Contrivance)


## About

### What is PubMED ?

[Pubmed](https://www.ncbi.nlm.nih.gov/pubmed/) is the web interface used to query the NIH's database [MEDLINE](https://www.nlm.nih.gov/bsd/pmresources.html).

MEDLINE contains journal citations and abstracts for biomedical literature from around the world (More than 27M).

They provide free APIs to build automatic queries, however a relational database could be more efficient.

The aim of this project is to download XML files provided by MEDLINE on their FTP and to build a relational mySQL database with their content.


## Launch

### Clone this repository

The first step is to clone this Github repository to your local machine.

Open a terminal.

	git clone "http://"
	cd MEDOC_medline_downloader_contrivance

### Setup

The first step is to install external dependencies and to cythonize python functions.

Thus, run the file *SETUP.py*

	python3 SETUP.py build_ext --inplace
	
This script will:

* Check for pip3 and give command to install it
* Check for Cython and give command to install it
* Check for pymysql and give command to install it
* Check for bs4 and give command to install it
* Build .so and .c files for cython functions

### Launch the programm

Open file 'parameters.json' and change complete path value including your /home/xxx/...

If your computer has 16Go or more of RAM, you can set '_insert_command_limit_' to '1000'.

Leave database name to '_pubmed_' but change the mySQL password to yours.

Then, simply execute :

	python3 file_execution.py 
	
### Output

First line should be about database creation and number of files to download.

Then, a regular output for a file loading should look like:

	- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - DOWNLOADING FILE
	Downloading baseline/medline17n0216.xml.gz ..
	Elapsed time: 12.32 sec for module: download
	- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FILE EXTRACTION
	Elapsed time: 0.42 sec for module: extract
	- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - XML FILE PARSING
	Elapsed time: 72.47 sec for module: parse
	- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - SQL INSERTION
	10000 articles inserted for file baseline/medline17n0216.xml.gz
	20000 articles inserted for file baseline/medline17n0216.xml.gz
	30000 articles inserted for file baseline/medline17n0216.xml.gz
	Total time for file medline17n0216.xml.gz: 5.29 min



## Issues

__Program stop running because of 'Segmentation fault (core dumped)'__

Indexing a file with 30K article take some time and RAM. Try to open the function _/lib_medline/python_functions/E_parse_xml.py_ and go to the line:

	soup = BeautifulSoup(file_content, 'lxml')
	
Change '_lxml_' to '_html-parser_' and re-launch SETUP.py

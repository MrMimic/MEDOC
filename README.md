# MEDOC (MEdline DOwnloading Contrivance)

More information about MEDOC on OMICTools website or on MEDOC's publication on arXiv.org:

* https://arxiv.org/abs/1710.06590

* https://omictools.com/medline-downloading-contrivance-tool


## About

### Development

Thanks to [rafspiny](https://github.com/rafspiny) for his multiple corrections and feedback !

### What is MEDLINE?

[MEDLINE](https://www.nlm.nih.gov/bsd/pmresources.html) is a database of scientitifc articles released by the NIH. [Pubmed](https://www.ncbi.nlm.nih.gov/pubmed/) is the most common way to query this database, used daily by many scientists around the world.

The NIH provides free APIs to build automatic queries, however a relational database could be more efficient.

The aim of this project is to download XML files provided by MEDLINE on a FTP and to build a relational mySQL database with their content.


## Launch

### Clone this repository

The first step is to clone this Github repository to your local machine.

Open a terminal.

	git clone "https://github.com/MrMimic/MEDOC"
	cd ./MEDOC

### Setup

Here prerequisites and installation procedures will be discussed.

#### Prerequisites 

XML parsing libraries may be needed. You can install them on any Debian-derived system with:

	sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev

You may also need `python-dev`. You can also install it with the same command:

	sudo apt-get install python-dev

#### Installation

The second step is to install external dependencies and to cythonize python functions.

Thus, run the file *SETUP.py*

	cd /path/to/MEDOC
	python3 utils/SETUP.py build_ext --inplace

This script will:

* Check for pip3 and give command to install it
* Check for Cython and give command to install it
* Check for pymysql and give command to install it
* Check for bs4 and give command to install it

There's no need to Cythonize functions anymore, they've been optimized.

**Alternatively** you can exploit the requirements.txt file shipped with the project.
Simply run the following command from the MEDOC folder.

	pip3 install -r requirements.txt

	bs4==0.0.1
	beautifulsoup4==4.6.0
	Cython==0.27.2
	html5lib==0.999999999
	lxml==3.5.0
	PyMySQL==0.7.11

#### Configuration

Before you can run the code, you should take a look at `parameters.json` file and customize it according to your 
environment.

Plus, if you have already a user to access the DB you wish to create you can change the `schema` file to reflect that.
You can change the DB_USER and the DB_PASSWORD fields with the following command.
Suppose your credentials are: my_custom_user/my_secret_password

```bash
export MEDOC_SQL_FILE='database_creation.sql'
sed -i'' -e "s/\bdb_user\b/my_custom_user/g" $MEDOC_SQL_FILE
sed -i'' -e "s/\bDB_PASSWORD\b/my_secret_password/g" $MEDOC_SQL_FILE
```

NOTE: If python3 is your default, you do not need to specify `python3` or `pip3` but just use `python` and `pip`.

### Launch the programm

Open file 'parameters.json' and change complete path value including your /home/xxx/...

If your computer has 16Go or more of RAM, you can set '_insert_command_limit_' to '1000' of greater.

Leave database name to '_pubmed_' but change the mySQL password to yours.

Then, simply execute :

	python3 __execution__.py 

	
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

Change '_lxml_' to '_html-parser_' and re-launch SETUP.py.

Or simply try to lower the '_insert_command_limit_' parameter, to insert values more often in the database, thus saving RAM usage.


__SQL insertions are taking really a lot of time (more than 15min / file)'__

Recreate the SQL database after dropping it, by running the following command:

	DROP DATABASE pubmed ;

Then, comment every line about indexes (_CREATE INDEX_) or foreigns keys (_ALTER TABLE_) into the SQL creation file. Indexes are slowing up insertions.

When the database is full, launch the indexes and alter commands once at a time.

__Problem installing lxml__

Make sure you have all the right dependencies installed

On Debian based machines try running:

	sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev


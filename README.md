# MEDOC (MEdline DOwnloading Contrivance)

More information about MEDOC on OMICTools website or on MEDOC's publication on arXiv.org:

* https://arxiv.org/abs/1710.06590

* https://omictools.com/medline-downloading-contrivance-tool

*************
*************

__WATCH OUT__: MEDOC is now starting in parallelized mode on the __master__ branch. Switch on the branch __sequential_version__ if you have less than 30Go of RAM or a single-code CPU. Or try to lower a lot the _insert_command_limit_ parameter.

__PS__: Flake-8 formated code with 85 chars / line is ugly. Please avoid PyCharm to format it before pulling a merge request.

*************
*************

## About MEDOC

### Development

Thanks to [rafspiny](https://github.com/rafspiny) for his multiple corrections and feedback !

### What is MEDLINE?

[MEDLINE](https://www.nlm.nih.gov/bsd/pmresources.html) is a database of scientitifc articles released by the NIH. [Pubmed](https://www.ncbi.nlm.nih.gov/pubmed/) is the most common way to query this database, used daily by many scientists around the world.

The NIH provides free APIs to build automatic queries, however a relational database could be more efficient.

The aim of this project is to download XML files provided by MEDLINE on a FTP and to build a relational mySQL database with their content.


## Launch

### Clone this repository

The first step is to clone this Github repository on your local machine.

Open a terminal:

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

* Check for _pip3_ and give command to install it
* Check for _Cython_ and give command to install it
* Check for _pymysql_ and give command to install it
* Check for _bs4_ and give command to install it

There's no need to Cythonize functions anymore, they've been optimized.

**Alternatively** you can exploit the requirements.txt file shipped with the project.
Simply run the following command from the MEDOC folder.

	pip3 install -r requirements.txt

#### Configuration

Before you can run the code, you should first create a _configuration.cfg_ file and customize it according to your 
environment. Below is the dist.config:

	# ================================ GLOBAL =============================================
	[informations]
	version: 1.2.2
	author: emeric.dynomant@omictools.com
	
	# =========================== MYSQL ============================================
	[database]
	path_to_sql: ./utils/database_creation.sql
	user: YOUR_SQL_USER
	password: YOUR_SQL_PWD
	host: YOUR_SQL_HOST
	port: YOUR_SQL_PORT
	database: pubmed
	insert_command_limit: 750
	
	# =========================== PATH ============================================
	[paths]
	program_path: /home/emeric/1_Github/MEDOC
	pubmed_data_download: ./pudmed_data/
	sql_error_log: ./log/errors.log
	already_downloaded_files: ./log/inserted.log

Plus, if you have already a user to access the DB you wish to create you can change the `schema` file to reflect that.
You can change the DB_USER and the DB_PASSWORD fields with the following command.
Suppose your credentials are: my_custom_user/my_secret_password

```bash
export MEDOC_SQL_FILE='./utils/database_creation.sql'
sed -i'' -e "s/\bDB_USER\b/my_custom_user/g" $MEDOC_SQL_FILE
sed -i'' -e "s/\bDB_PASSWORD\b/my_secret_password/g" $MEDOC_SQL_FILE
```

NOTE: If python3 is your default, you do not need to specify `python3` or `pip3` but just use `python` and `pip`.

### Launch the programm

Open file 'parameters.json' and change complete path value including your /home/xxx/...

If your computer has 16Go or more of RAM, you can set '_insert_command_limit_' to '1000' of greater.

Leave database name to '_pubmed_' but change the mySQL password to yours.

Then, simply execute :

	python3 __execution__.py 


## Issues

__Program stop running because of 'Segmentation fault (core dumped)'__

Indexing a file with 30K article take some time and RAM (if you know other parser than LXML, more RAM-frieldy, do a PR). Try to open the function _/lib_medline/python_functions/E_parse_xml.py_ and go to the line:

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


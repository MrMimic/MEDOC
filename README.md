# MEDOC (MEdline DOwnloading Contrivance)

## Citing MEDOC

	@article{dynomant2017medoc,
	  title={MEDOC: a Python wrapper to load MEDLINE into a local MySQL database},
	  author={Dynomant, Emeric and Gorieu, Mathilde and Perrin, Helene and Denorme, Marion and Pichon, Fabien and Desfeux, Arnaud},
	  journal={arXiv preprint arXiv:1710.06590},
	  year={2017}
	}

## About MEDOC

### Development

Thanks to [rafspiny](https://github.com/rafspiny) for his multiple corrections and feedback !

### V1.3.0

MEDOC had multiple changes. The most important is about the XML parsing, which should return less errors than before. The way the data is parsed has been improved.

Then, the stacking of the SQL INSERT() has been removed. Files are now process in parallel by many threads and inserted during this streaming of the file.

I now assume that it is easy and cheap to get a decent multi-thread machine for 24h of processing (AWS, GoogleCloud, MAzure ...) with a decent amount of RAM.

MEDOC has been tested on a 144 cores XEON E7 with 500Go of RAM. If your want the old version, please clone the sequential branch.


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

```bash
	sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
```

You may also need `python-dev`. You can also install it with the same command:

```bash
	sudo apt-get install python-dev
```

#### Installation

The second step is to install external dependencies. First, create a virtual environment and load it:

```bash
	python3 -m venv .venv
	source .venv/bin/activate
```

Then, simply run the following commands:

```bash
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
```

Avery libraries will now be installed into this environment.

#### Configuration

Before you can run the code, you should first create a _configuration.cfg_ file (in the MEDOC folder) and customize it according to your environment. Below is the dist.config:

```yaml
	# ================================ GLOBAL =============================================
	[informations]
	version: 1.3.0
	author: emeric.dynomant@gmail.com

	# =========================== MYSQL ============================================
	[database]
	path_to_sql: ./utils/database_creation.sql
	user: <YOUR_SQL_USER>
	password: <YOUR_SQL_PASSWORD>
	host: <YOUR_SQL_HOST>
	port: <YOUR_SQL_PORT>
	database: pubmed

	# =========================== PATH ============================================
	[paths]
	program_path: ./
	pubmed_data_download: ./pudmed_data/
	sql_error_log: ./log/errors.log
	already_downloaded_files: ./log/inserted.log

	# =========================== PARALLELISM ============================================

	[threads]
	parallel_files: 10
```

### Launch the programm

Then, simply execute :

	python3 medoc.py 

It took 26H to insert 29,058,362 articles with a XEON E7. Among them, 420 insert command generated an error, aminly due to under-sized mySQL columns.

## Issues

### SQL insertions are taking really a lot of time

Recreate the SQL database after dropping it, by running the following command:

	DROP DATABASE pubmed ;

Then, comment every line about indexes (_CREATE INDEX_) or foreigns keys (_ALTER TABLE_) into the SQL creation file. Indexes are slowing up insertions.

When the database is full, launch the indexes and alter commands once at a time.

### Problem installing lxml

Make sure you have all the right dependencies installed

On Debian based machines try running:

	sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev


# 			mySQL MEDLINE Schema 

# Development:
# 		Gaurav Bhalotia (Feb. 16, 2003)
# 		Ariel Schwartz (Jun. 10, 2003)
#		Emeric Dynomant (Jun. 08, 2017, Nov. 11, 2018)

# Based on: 
# 		nlmmedline_021101.dtd 
#		nlmmedlinecitation_021101.dtd 
#		nlmcommon_021101.dtd 

# The FTP are located at: 
#		ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/

# Script to fill it available on github:
#		https://github.com/MrMimic/MEDOC
# 


#==============================================================
# TABLE: medline_citation 
#==============================================================
CREATE TABLE medline_citation (pmid INTEGER NOT NULL, date_created DATE, date_completed DATE, date_revised DATE, issn CHAR(9), volume VARCHAR(100), issue VARCHAR(100), pub_date_year VARCHAR(4), pub_date_month VARCHAR(20), pub_date_day VARCHAR(3), medline_date VARCHAR(100), journal_title VARCHAR(2000), iso_abbreviation VARCHAR(100), article_title VARCHAR(1000) NOT NULL, medline_pgn VARCHAR(100), abstract_text TEXT, copyright_info VARCHAR(1100), article_author_list_comp_yn CHAR(3), data_bank_list_comp_yn CHAR(3), grantlist_complete_yn CHAR(3), vernacular_title VARCHAR(1000), date_of_electronic_publication DATE, country VARCHAR(50), medline_ta VARCHAR(500), nlm_unique_id VARCHAR(20), xml_file_name VARCHAR(500) NOT NULL, number_of_references VARCHAR(10), citation_owner VARCHAR(30), citation_status VARCHAR(50), medline_info_journal VARCHAR(100), PRIMARY KEY (pmid)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX pk_med_citation on medline_citation(pmid, pub_date_year, journal_title(255), country);

#==============================================================
# TABLE: medline_author
#==============================================================
CREATE TABLE medline_author (pmid INTEGER NOT NULL, last_name VARCHAR(500), fore_name VARCHAR(50), first_name VARCHAR(50), middle_name VARCHAR(50), initials VARCHAR(30), suffix VARCHAR(10), affiliation TEXT, collective_name VARCHAR(500)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_author on medline_author(pmid, affiliation(255));

#==============================================================
# TABLE: medline_chemical_list
#==============================================================
CREATE TABLE medline_chemical_list (pmid INTEGER NOT NULL, registry_number VARCHAR(20), name_of_substance VARCHAR(2000) NOT NULL) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_m_chem on medline_chemical_list(pmid, name_of_substance(255));

#==============================================================
# TABLE: medline_mesh_heading 
#==============================================================
CREATE TABLE medline_mesh_heading(pmid INTEGER NOT NULL, descriptor_name VARCHAR(500) NOT NULL, descriptor_ui VARCHAR(100) NOT NULL, descriptor_name_major_yn CHAR(3), qualifier_name VARCHAR(50), qualifier_ui VARCHAR(100), qualifier_name_major_yn CHAR(3)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX pk_med_meshheading on medline_mesh_heading(pmid, descriptor_name, qualifier_name);

#==============================================================
# TABLE: medline_comments_corrections 
#==============================================================
CREATE TABLE medline_comments_corrections (pmid INTEGER NOT NULL, ref_pmid VARCHAR(15), type VARCHAR(25), ref_source VARCHAR(1000)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_comments_pmid on medline_comments_corrections(pmid);

#==============================================================
# TABLE: medline_citation_subsets 
#==============================================================
CREATE TABLE medline_citation_subsets(pmid INTEGER NOT NULL, citation_subset VARCHAR(500) NOT NULL) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX pk_med_cit_sub on medline_citation_subsets(pmid, citation_subset);

#==============================================================
# TABLE: medline_article_publication_type 
#==============================================================
CREATE TABLE medline_article_publication_type( pmid INTEGER NOT NULL, publication_type VARCHAR(100)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_pub_type_pmid on medline_article_publication_type(pmid);

#==============================================================
# TABLE: medline_article_language 
#==============================================================
CREATE TABLE medline_article_language(pmid INTEGER NOT NULL, language VARCHAR(100)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_lang on medline_article_language(pmid, language);

#==============================================================
# TABLE: medline_grant 
#==============================================================
CREATE TABLE medline_grant(pmid INTEGER NOT NULL, grant_id VARCHAR(100) NOT NULL, acronym VARCHAR(100), agency VARCHAR(500), country VARCHAR(500)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX pk_medline_grant on medline_grant(pmid, grant_id, country);

#==============================================================
# TABLE: medline_data_bank 
#==============================================================
CREATE TABLE medline_data_bank(pmid INTEGER NOT NULL, accession_number VARCHAR(100) NOT NULL) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_data_bank_pmid on medline_data_bank(pmid);

#==============================================================
# TABLE: medline_personal_name_subject 
#==============================================================
CREATE TABLE medline_personal_name_subject (pmid INTEGER NOT NULL, last_name VARCHAR(500), fore_name VARCHAR(50), first_name VARCHAR(50), middle_name VARCHAR(50), initials VARCHAR(30), suffix VARCHAR(10)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_pers_name_pmid on medline_personal_name_subject(pmid);

#==============================================================
# TABLE: medline_citation_other_id 
#==============================================================
CREATE TABLE medline_citation_other_id(pmid INTEGER NOT NULL, source VARCHAR(150), other_id VARCHAR(1000)) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_other_id_pmid on medline_citation_other_id(pmid);

#==============================================================
# TABLE: medline_investigator 
#==============================================================
CREATE TABLE medline_investigator (pmid	INTEGER NOT NULL, last_name VARCHAR(500), fore_name VARCHAR(50), first_name VARCHAR(50), middle_name VARCHAR(50), initials VARCHAR(30),  suffix VARCHAR(10), affiliation TEXT) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE INDEX idx_invest_pmid on medline_investigator(pmid);

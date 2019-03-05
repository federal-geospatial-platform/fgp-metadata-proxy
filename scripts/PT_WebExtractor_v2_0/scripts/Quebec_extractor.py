import os
import sys
import urllib2
import urllib
from bs4 import BeautifulSoup
import collections
import math
import csv
import codecs
import requests
import time
import inspect
import json
import glob
import re
import urlparse
import argparse
import traceback
import datetime

import Main_Extractor as main_ext

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

from common import shared
from common import bsoup
#from common import access_rest as rest
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		''' Initializer for the Extractor class. '''

		# Set the province
		self.province = 'Quebec'
		
		# Create the page groups dictionary
		self.page_groups = []
		self.page_groups = collections.OrderedDict()

		# Declare all the different types of pages
		pg_grp = page_group.PageGroup('cigg',
					   "Catalogue d'information geographique gouvernementale (Government Geographic Information Catalog)")
		pg_grp.add_url('main_url', 'http://catalogue-geographique.gouv.qc.ca')
		pg_grp.add_url('mdata_path', shared.get_home_folder() + "\\results\\_working\\Catalogue_Metadata")
		self.page_groups['cigg'] = pg_grp

		pg_grp = page_group.PageGroup('geoboutique', "Geoboutique Quebec")
		pg_grp.add_url('main_url', 'http://geoboutique.mern.gouv.qc.ca')
		self.page_groups['geoboutique'] = pg_grp

		pg_grp = page_group.PageGroup('opendata', "Donnees Quebec (Quebec Data)")
		pg_grp.add_url('main_url', 'https://www.donneesquebec.ca/recherche/fr/dataset')
		opts = {'format': ['shp', 'geojson', 'kml', 'json', 'xml', 'wms', 'rest', 'wfs', 'gml',
						  'zip', 'fgdb', 'kmz', 'sqlite', 'lyr', 'geotiff', 'geotif', 'shx',
						  'laz', 'gbfs', 'ecw']}
		pg_grp.set_opts(opts)
		self.page_groups['opendata'] = pg_grp

		pg_grp = page_group.PageGroup('geoinfo', "Geoinfo Quebec")
		pg_grp.add_url('main_url', 'http://geoinfo.gouv.qc.ca/portail/jsp/geoinfo.jsp')
		pg_grp.add_url('query_url', 'http://geoinfo.gouv.qc.ca/portail/Search')
		self.page_groups['geoinfo'] = pg_grp

		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Set the arguments for this extractor
		self.argmt['word'] = main_ext.Ext_Arg('word', 
										methlst=['opendata', 'geoinfo'])
		self.argmt['format'] = main_ext.Ext_Arg('format', methlst=['opendata'])
		
	def get_province(self):
		''' Gets the province name of the extractor.
		:return: The province name of the extractor.
		'''
		
		return self.province

	####################################################################################################################

	def write_to_html(self, fn, html_code):
		out_f = codecs.open(fn, encoding='utf_8_sig', mode='w')
		out_f.write(html_code)
		out_f.close()

	def extract_cigg(self):
		''' Extracts all datasets from the Catalogue d'information geographique gouvernementale site.
			The catalogue requires HTML forms to query and extract the datasets' metadata. In order to
			gather all information, each page has to be loaded one at a time.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Quebec's Catalogue d'information geographique gouvernementale (CIGG)")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		main_url = self.pg_grp.get_url('main_url')
		
		print "\nMain URL: %s" % main_url

		# Create the CSV file
		csv_fn = "CIGG_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Create the Selenium driver and open Firefox
		driver = webdriver.Firefox()
		driver.implicitly_wait(20)
		driver.get(main_url)

		# Wait for the element with ID "rechercheCiggForm:lancerRecherche" to load
		shared.wait_page_load(driver, By.ID, "rechercheCiggForm:lancerRecherche")

		# Find the element with ID "rechercheCiggForm:lancerRecherche" and
		#   activate its click function
		srch_button = driver.find_element_by_id("rechercheCiggForm:lancerRecherche")
		srch_button.click()

		# Find the element with ID "_id67:LienOui" and
		#   activate its click function
		err_button = driver.find_element_by_id("_id67:LienOui")
		err_button.click()

		# Wait for the element with ID "formresultats:series:0:lienMetadonneeDocumentActif"
		#  to load and then extract the contents of the page
		shared.wait_page_load(driver, By.ID, "formresultats:series:0:lienMetadonneeDocumentActif")
		rec_html = driver.page_source

		# Get the soup of the HTML contents
		soup = BeautifulSoup(rec_html, 'html.parser')

		# Find all <img> with title "Consulter les métadonnées"
		img_list = soup.find_all('img', attrs={'title': 'Consulter les métadonnées'})
		num_items = len(img_list)

		print "\nNumber of records: " + str(num_items)

		record_count = 0

		# FOR DEBUG PURPOSES ONLY
		# if not os.path.exists('mdata'):
		#     os.mkdir('mdata')

		for i in range(1, num_items):
			record_count += 1
			msg = "Extracting %s of %s records from CIGG" % (record_count, num_items)
			shared.print_oneliner(msg)
			try:
				# First, switch back to the first window if not already there
				window_before = driver.window_handles[0]
				driver.switch_to.window(window_before)

				# Find the metadata button with the current item number
				#   and activate its click function
				mdata_button = driver.find_element_by_id("formresultats:series:%s:lienMetadonneeDocumentActif" % i)
				mdata_button.click()

				# Wait for element with ID "section_serie" to load
				shared.wait_page_load(driver, By.ID, "section_serie", delay=2)

				# Switch to the new metadata window
				window_after = driver.window_handles[1]
				driver.switch_to.window(window_after)

				# Grab the contents of the metadata page
				mdata_html = driver.page_source
			except:
				print "\nMissed '%s' due to error." % driver.current_url
				self.write_error(driver.current_url, title='CIGG Dataset')
				continue

			# Get the URL of the metadata page
			#print driver.current_url
			mdata_url = driver.current_url

			# Get the metadata page soup
			mdata_soup = BeautifulSoup(mdata_html, 'html.parser')
			
			if not self.check_result(mdata_soup, mdata_html, 
				txt='Information could not be extracted due to missing metadata.'): continue

			# Get the title
			title_str = bsoup.get_adj_text_by_label(mdata_soup, 'td', 'Nom')

			# Get the description
			desc_str = bsoup.get_adj_text_by_label(mdata_soup, 'td', 'Sommaire')

			# Get the date
			date = bsoup.get_adj_text_by_label(mdata_soup, 'td', "Type et date d'intervention")
			match = re.search('\d{4}-\d{2}-\d{2}', date)
			if match is None:
				date_str = ''
			else:
				date_str = match.group()

			# Get the organization
			org_str = bsoup.get_adj_text_by_label(mdata_soup, 'td', 'Organisme')

			# Get the download link
			# link_td = bsoup.get_adj_tags_by_text(mdata_soup, 'td', 'Titre')
			# if len(link_td) == 0:
			#     link_str = ''
			# else:
			#     link_a = link_td[0].a
			#     link_str = link_a['href']

			# Get the cost
			lic_str = bsoup.get_adj_text_by_label(mdata_soup, 'td', 'de prix', contains=True)

			# Get the formats
			format_list = []
			format_tags = bsoup.get_adj_tags_by_text(mdata_soup, 'td', 'Format des fichiers')
			for form in format_tags:
				format_str = form.text.strip()
				if not format_str == 'Sans objet':
					format_list.append(format_str)
			format_list = list(set(format_list))

			# Set the download text
			if len(format_list) == 1:
				download_str = 'Yes'
				access = 'Download/Web Accessible'
			elif len(format_list) > 1:
				download_str = 'Multiple Downloads'
				access = 'Download/Web Accessible'
			else:
				download_str = 'No'
				access = 'Contact the Province'

			# If the dataset is not free, download_str is 'No' and access 'Contact the Province'
			if lic_str == 'Grille tarifaire' or lic_str == 'Consultation et abonnement':
				download_str = 'No'
				access = 'Contact the Province'

			# Add all values to the CSV file
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Date', date_str)
			pt_csv.add('Publisher', org_str)
			#pt_csv.add('Web Page URL', db_url)
			pt_csv.add('Access', access)
			pt_csv.add('Download', download_str)
			pt_csv.add('Licensing', lic_str)
			pt_csv.add('Available Formats', '|'.join(format_list))
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Notes', self.notes)

			# Write the results to the CSV file
			pt_csv.write_dataset()

		print

		# Close the CSV file
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time


	def extract_geoboutique(self):
		''' Extracts all datasets from the Geoboutique site. The site is accessed the same way as CIGG.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Quebec's Geoboutique")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		main_url = self.pg_grp.get_url('main_url')
		
		print "\nMain URL: %s" % main_url

		# Create the CSV file
		csv_fn = "Geoboutique_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Create the Selenium driver and open Firefox
		driver = shared.get_driver('firefox', False)
		driver.implicitly_wait(20)
		driver.get(main_url)

		try:
			# Wait for the element with ID "rechercheEdelForm:lancerRecherche" to load
			shared.wait_page_load(driver, By.ID, "rechercheEdelForm:modeRechercheSpatial")
			
			print driver
			answer = raw_input("Press enter...")

			# Find the element with ID "rechercheEdelForm:lancerRecherche" and
			#   activate its click function
			try:
				srch_button = driver.find_element_by_id("rechercheEdelForm:lancerRecherche")
			except Exception, e:
				print "\nERROR: %s" % e
				print "Try running the Geoboutique extractor again."
				return None
			srch_button.click()

			# Find the element with ID "messagesForm:LienOui" and
			#   activate its click function
			try:
				err_button = driver.find_element_by_id("messagesForm:LienOui")
			#except NoSuchElementException, e:
			except Exception, e:
				print "\nERROR: %s" % e
				print "Try running the Geoboutique extractor again."
				return None
			err_button.click()

			# Wait for the element with ID "formresultats:series:0:lienMetadonneeSerieActif"
			#  to load and then extract the contents of the page
			shared.wait_page_load(driver, By.ID, "formresultats:series:0:lienMetadonneeSerieActif")
			rec_html = driver.page_source

			# Get the soup of the HTML contents
			rec_soup = BeautifulSoup(rec_html, 'html.parser')

			# Find all <img> with title "Consulter les métadonnées"
			img_list = rec_soup.find_all('img', attrs={'title': 'Consulter les métadonnées'})
			num_items = len(img_list)

			print "\nNumber of records: " + str(num_items)

			record_count = 0

			# FOR DEBUG PURPOSES ONLY
			# if not os.path.exists('mdata'):
			#     os.mkdir('mdata')

			for i in range(1, num_items):
				record_count += 1
				msg = "Extracting %s of %s records from Geoboutique" % (record_count, num_items)
				shared.print_oneliner(msg)
				try:
					# First, switch back to the first window if not already there
					window_before = driver.window_handles[0]
					driver.switch_to.window(window_before)

					# Find the metadata button with the current item number
					#   and activate its click function
					mdata_button = driver.find_element_by_id("formresultats:series:%s:lienMetadonneeSerieActif" % i)
					mdata_button.click()

					# Wait for element with ID "section_serie" to load
					shared.wait_page_load(driver, By.ID, "section_serie", delay=2)

					# Switch to the new metadata window
					window_after = driver.window_handles[1]
					driver.switch_to.window(window_after)

					# Grab the contents of the metadata page
					mdata_html = driver.page_source
				except:
					print "Missed '%s' due to error." % driver.current_url
					self.write_error(driver.current_url, title='CIGG Dataset')
					continue

				# Get the URL of the metadata page
				#print driver.current_url
				mdata_url = driver.current_url

				# Get the metadata page soup
				mdata_soup = BeautifulSoup(mdata_html, 'html.parser')
				
				if not self.check_result(mdata_soup, mdata_html, 
					txt='Information could not be extracted due to missing metadata.'): continue

				# Get the title
				title_str = bsoup.get_adj_text_by_label(mdata_soup, 'th', 'Nom')

				# Get the description
				desc_str = bsoup.get_adj_text_by_label(mdata_soup, 'th', 'Sommaire')

				# Get the date
				date = bsoup.get_adj_text_by_label(mdata_soup, 'th', "Type et date d'intervention")
				#print "date: " + str(date)
				match = re.search('\d{4}-\d{2}-\d{2}', date)
				if match is None:
					date_str = ''
				else:
					date_str = match.group()

				# Get the organization
				org_str = bsoup.get_adj_text_by_label(mdata_soup, 'th', 'Organisme')

				download_str = 'No'
				access = 'Contact the Province'

				# Get the cost
				lic_str = bsoup.get_adj_text_by_label(mdata_soup, 'th', 'de prix', True)

				# Get the formats
				format_list = []
				format_tags = bsoup.get_adj_tags_by_text(mdata_soup, 'th', 'Format des fichiers')
				for form in format_tags:
					format_str = form.text.strip()
					if not format_str == 'Sans objet':
						format_list.append(format_str)
				format_list = list(set(format_list))

				# Add all values to the CSV file
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Date', date_str)
				pt_csv.add('Publisher', org_str)
				# pt_csv.add('Web Page URL', db_url)
				pt_csv.add('Access', access)
				pt_csv.add('Download', download_str)
				pt_csv.add('Licensing', lic_str)
				pt_csv.add('Available Formats', '|'.join(format_list))
				pt_csv.add('Metadata URL', mdata_url)
				pt_csv.add('Notes', self.notes)

				# Write the results to the CSV file
				pt_csv.write_dataset()

				# Print the progress
				# sys.stdout.write('\r')
				# sys.stdout.write("**** %s of %s records extracted ****" % (record_count, num_items))
				# sys.stdout.flush()
				
		except UnexpectedAlertPresentException:
			print traceback.format_exc()
			return None

		# Close the CSV file
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time


	def extract_opendata(self): #, word=None, format=None):
		''' Method to extract data from Quebec's open data catalogue.
		:param word: The word used to filter the results
		:param format: The format to filter to results.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Quebec's Open Data Catalogue")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# Get the parameter
		word = self.argmt['word'].get_value()
		format = self.argmt['format'].get_value()

		opendata_url = self.pg_grp.get_url('main_url')

		# Create the CSV file
		csv_fn = "OpenData_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		format_filters = ['shp', 'geojson', 'kml', 'json', 'xml', 'wms', 'rest', 'wfs', 'gml',
						  'zip', 'fgdb', 'kmz', 'sqlite', 'lyr', 'geotiff', 'geotif', 'shx',
						  'laz', 'gbfs', 'ecw']

		# Set the parameters for the URL query
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['q'] = word
		if format is not None and not format == "all" and not format == '':
			params['res_format'] = format

		# Build the URL query
		query_url = shared.get_post_query(opendata_url, params)

		# Get the soup for the query page results
		soup = bsoup.get_soup(query_url)
		
		print "\nQuery URL: %s" % query_url

		# Get the number of pages from page buttons at bottom of site
		pagination_res = soup.find('div', attrs={'class': 'pagination'})
		if pagination_res is None:
			page_count = 1
		else:
			li_list = pagination_res.find_all('li')
			page_count = li_list[len(li_list) - 2].a.string

		prev_perc = -1

		record_count = 0

		special_chr = ""

		record_total = int(page_count) * 20

		for page in range(0, int(page_count)):
			# Open each iteration of pages:
			if special_chr == "":
				# Some of the search entries can include "&" character
				#	but if an error is returned, use the "?" character instead
				try:
					page_url = "%s&page=%s" % (query_url, page + 1)
					#page_html = urllib2.urlopen(page_url)
					special_chr = "&"
				except:
					page_url = "%s?page=%s" % (query_url, page + 1)
					#page_html = urllib2.urlopen(page_url)
					special_chr = "?"
			else:
				page_url = "%s%spage=%s" % (query_url, special_chr, page + 1)
				#page_html = urllib2.urlopen(page_url)

			page_soup = bsoup.get_soup(page_url, silent=True)

			# Get all the datasets on the current page (all datasets are in a 'div' with class 'dataset-item')
			results = page_soup.find_all('div', attrs={'class': 'bottom17'})

			if len(results) == 0 and record_count == 0:
				print "No records exist with the given search parameters."
				print "URL query sample: %s" % query_url
				return None

			for dataset in results:
				record_count += 1
				msg = "Extracting %s of %s records from Open Data" % (record_count, record_total)
				shared.print_oneliner(msg)
				
				# Get the available data formats
				label_list = dataset.find_all('span', attrs={'class': 'label'})
				data_formats = []
				for lbl in label_list:
					if lbl.has_attr('data-format'):
						# data_format = lbl.string.encode('utf-8')
						data_format_str = lbl.string
						data_formats.append(str(data_format_str))

				# Determine whether to include the result based on formats
				dforms = [x.lower() for x in data_formats]
				check_set = set(dforms) & set(format_filters)
				if len(check_set) == 0: continue

				# Get the title of the dataset
				title_res = dataset.find('h2', attrs={'class': 'dataset-heading'})
				title_str = title_res.a.string

				# Get the URL of the dataset
				#web_url = domain + title_res.a['href']
				web_url = urlparse.urljoin(page_url, title_res.a['href'])

				# Get the organization name and description
				org_str = ''
				desc_str = ''
				p_res = dataset.find_all('p')
				if len(p_res) == 3:
					org_res = p_res[0]
					desc_res = p_res[2]
					org_str = org_res.a.string
					desc_str = desc_res.string

				# Get more in depth info by loading the dataset's URL
				#dataset_html = urllib2.urlopen(url_str)
				dataset_soup = bsoup.get_soup(web_url, silent=True)
				
				if self.check_result(dataset_soup, web_url, title_str, output=False):

					# Get the update date
					time_res = dataset_soup.find('th', text=u'Mise à jour')
					time_sib = time_res.find_next_sibling('td')
					date_str = time_sib.string

					# To get the downloads, extract all <a> with class piwik_download
					a_list = dataset_soup.find_all('a', attrs={'class': 'piwik_download'})

					# Remove any <a> with class 'custom-close' to remove doubles
					anchors = [a for a in a_list if 'custom-close' not in a.attrs['class']]

					# Set the download string and access depending on the number of anchors
					if len(anchors) > 1:
						download_str = 'Multiple Downloads'
						access = 'Download/Web Accessible'
					elif len(anchors) == 1:
						download_str = anchors[0]['href']
						access = 'Download/Web Accessible'
					else:
						download_str = 'No'
						access = 'Contact the Province'

					# Get the licence
					a_lic = dataset_soup.find('a', attrs={'rel': 'dc:rights'})
					licence = ''
					if a_lic is not None:
						licence = a_lic.text
				else:
					date_str = ''
					download_str = ''
					access = ''
					licence = ''

				# Add all values to the CSV file object
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Page URL', web_url)
				pt_csv.add('Date', date_str)
				pt_csv.add('Publisher', org_str)
				pt_csv.add('Licensing', licence)
				pt_csv.add('Available Formats', "|".join(data_formats))
				pt_csv.add('Access', access)
				pt_csv.add('Download', download_str)
				pt_csv.add('Notes', self.notes)
				#pt_csv.add('Spatial Reference', sp)
				# pt_csv.add('Metadata URL', mdata_url)

				# Write the dataset to the CSV file
				pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_geoinfo(self): #, word=None):
		''' Method to extract data from Quebec's Geoinfo site.
		:param word: Search word to filter the results
		:return: None
		'''
		#domain = "http://geoinfo.gouv.qc.ca"
		#search_url = "%s/portail/Search" % domain
		
		self.print_title("Extracting Quebec's Geoinfo")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the service url
		main_url = self.pg_grp.get_url('main_url')
		search_url = self.pg_grp.get_url('query_url')
		
		print "\nMain URL: %s" % main_url
		print "Query URL: %s" % search_url

		# Create the CSV file
		csv_fn = "Geoinfo_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Set the parameters for the URL query
		params = collections.OrderedDict()
		params['Request'] = "GetRecords"

		total_records = 200

		# Collect all the data as JSON first
		records_list = []
		
		record_counter = 0

		for index in range(1, total_records, 10):
			# Get the starting position
			params['startPosition'] = str(index)

			# Build the URL query
			query_url = shared.get_post_query(search_url, params) #, "Quebec's GeoInfo")

			# Get the JSON data
			json_results = shared.get_json(query_url)
			
			if not self.check_result(json_results, query_url): continue

			# Get a list of the results
			# print records
			records = json_results['result']

			for rec in records:
				record_counter += 1
				msg = "Extracting %s of approximately %s records from Geoinfo" % (record_counter, total_records)
				shared.print_oneliner(msg)
			
				records_list.append(rec)

		print "Number of results: " + str(len(records_list))

		for rec in records_list:
			# Cycle through each record

			title_str = rec['title']
			desc_str = rec['abstract']
			pub_str = rec['organisation']
			web_url = rec['online_resources'][0]['url']

			# Add all values to the CSV file object
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', web_url)
			pt_csv.add('Publisher', pub_str)
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')
			pt_csv.add('Notes', self.notes)

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

def main():
	ext = Extractor()

	try:
		pages = ext.get_pagelist()

		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--page", help="The page to extract: %s or all" % ', '.join(pages.keys()))
		parser.add_argument("-w", "--word", help="The key word(s) to search for.")
		parser.add_argument("-f", "--format", help="The format(s) to search for.")
		parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
		args = parser.parse_args()
		# print args.echo

		# print "province: " + str(args.province)
		# print "format: " + str(args.format)

		page = args.page
		srch_word = args.word
		formats = args.format
		silent = args.silent

		if page is None:
			answer = raw_input("Please enter the page you would like to use (%s or all): " % ', '.join(pages.keys()))
			if not answer == "":
				page = answer.lower()
			else:
				print "\nERROR: Please specify a web page."
				print "Exiting process."
				sys.exit(1)

		page = page.lower()

		print page

		ext.set_page(page)
		ext.run()

	except Exception, err:
		ext.print_log('ERROR: %s\n' % str(err))
		ext.print_log(traceback.format_exc())
		ext.close_log()

		# geoportal_list = extract_geoportal(province)


if __name__ == '__main__':
	sys.exit(main())

import os
import sys
import urllib2
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import collections
import math
import csv
import re
import numpy as np
import json
import urlparse
import argparse
import traceback
import datetime
import inspect
import time
import pprint
import codecs
from StringIO import StringIO

import Main_Extractor as main_ext

from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from common import shared
from common import bsoup
from common import services
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		# Set the province
		self.province = 'New_Brunswick'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Web Pages page group

		web_grp = main_ext.PageGroup('pages', 'New Brunswick Web Pages')
		
		# No arguments to add
		
		# Add URLs
		web_grp.add_url('db_url', 'https://www.pxw1.snb.ca/webnbcontrol/snbe/home.asp')
		web_grp.add_url('catalogue_url', 'http://www.snb.ca/geonb1/e/DC/catalogue-E.asp')
		
		# Add to Extractor's page group list
		self.page_groups.append(web_grp)
		
		
		####################################################################
		# Create Services page group

		srv_grp = main_ext.PageGroup('services', 'New Brunswick Web Map Services')
		
		# No arguments to add
		
		# Add URLs
		srv_grp.add_url('geonb_url', 'http://geonb.snb.ca/arcgis/rest/services')
		#srv_grp.add_url('geoportal_url', 'http://geoportal-geoportail.gc.ca/arcgis/rest/services')
		srv_grp.add_url('dnr_url', 'http://maps-dnr-mrn.gnb.ca/arcgis/rest/services')
		#srv_grp.add_url('proxy_url', 'http://proxyinternet.nrcan.gc.ca/arcgis/rest/services')
		srv_grp.add_url('erd_url', 'https://gis-erd-der.gnb.ca/arcgis/rest/services')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create Interactive Maps page group
		
		map_grp = main_ext.PageGroup('interactive', 'New Brunswick Interactive Pages')
		
		# No arguments to add
		
		# Add URLs
		map_grp.add_url('apps_url', 'http://www.snb.ca/geonb1/e/apps/apps-E.asp')
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		

	###################################################################################################################

	def extract_interactive(self):
		''' Extracts the interactive maps for New Brunswick
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting New Brunswick's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Get the URL with a list of interactive maps
		apps_url = self.pg_grp.get_url('apps_url')

		apps_soup = bsoup.get_soup(apps_url)

		# Get the table from the page
		table = apps_soup.find('table')
		table_list = shared.table_to_dict(table, header_row=0)

		for idx, table in enumerate(table_list):
			# Go through each row in the table
			
			# Print status
			msg = "Extracting %s of %s maps" % (idx + 1, len(table_list))
			shared.print_oneliner(msg)

			# Get the metadata link
			mdata_cell = table['details']
			mdata_a = mdata_cell.find('a')
			mdata_url = shared.get_anchor_url(mdata_a, apps_url)

			# Get the metadata soup
			mdata_soup = bsoup.get_soup(mdata_url)

			# Get the description
			desc_strong = mdata_soup.find('strong', text='Application description:')
			desc = desc_strong.next_sibling
			if isinstance(desc, NavigableString):
				desc_str = bsoup.get_text(desc)
			elif desc is not None:
				desc_str = desc.text
			else:
				desc_str = ''

			# Get the title, located in row with class 'toprowtext'
			toprow = mdata_soup.find('tr', attrs={'class': 'toprowtext'})
			td_title = toprow.find('td')
			title_str = td_title.text

			# Locate the unseen <div> with id 'boxes'
			boxes_div = mdata_soup.find('div', attrs={'id': 'boxes'})

			if boxes_div is None:
				# If the boxes <div> does not exist, the link is in a <span> with class 'NoDisclaimer'
				span = mdata_soup.find('span', attrs={'class': 'NoDisclaimer'})
				map_a = span.find('a')
				map_url = map_a['href']

				if map_url.find('paol.snb.ca') > -1:
					map_url = "https://paol.snb.ca/paol.html?v=1.0.29&lang=en"
			else:
				# First, located the <a> with class 'close'
				close_a = boxes_div.find('a', attrs={'class': 'close'})
				# Find the previous <a> which contains the link to the interactive map
				map_a = close_a.find_previous_sibling('a')
				#print map_a
				map_link = map_a['href']
				# Remove the javascript part of the link
				map_link = map_link.replace('javascript:myPopup', '')
				# Convert the map_link to a list using eval
				map_list = eval(map_link)
				# Get the first item in the list which is the URL
				map_url = map_list[0]

				#print map_list
			#print map_url

			data_url = ''
			dtype = 'Web Mapping Application'
			date_str = ''
			sp = ''

			# Get the data URL if it is an ArcGIS Online map
			map_soup = bsoup.get_soup(map_url)

			iframe = map_soup.find('iframe')
			if iframe is not None:
				# Get the ArcGIS URL from the iframe's src
				arcgis_url = iframe['src']

				#print arcgis_url

				data_url = shared.get_arcgis_url(arcgis_url)

				#print data_url

				# Get the information from the service URL
				data_json = shared.get_json(data_url)

				title_str = data_json['title']
				date = data_json['modified']
				date_str = shared.translate_date(date)
				dtype = data_json['type']
				# desc = data_json['description']
				sp = data_json['spatialReference']

			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', map_url)
			pt_csv.add('Data URL', data_url)
			pt_csv.add('Type', dtype)
			pt_csv.add('Date', date_str)
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')
			pt_csv.add('Spatial Reference', sp)
			pt_csv.add('Metadata URL', mdata_url)

			pt_csv.write_dataset()
			
		print

		# Get a list of the map URLs from a CSV file
		maps_fn = shared.get_home_folder() + "\\files\\NB_Interactive_Maps.csv"
		maps_csv = open(maps_fn)

		maps_reader = csv.reader(maps_csv, delimiter=',')

		for idx, row in enumerate(maps_reader):
			map_url = row[0]
			serv_url = row[1]

			# Print status
			msg = "Extracting %s of %s maps" % (idx + 1, len(list(maps_reader)))
			shared.print_oneliner(msg)

			if serv_url == '':
				# Get the soup of the map
				map_soup = bsoup.get_soup(map_url)

				# Get the title and description from the metadata on the page
				page_mdata = bsoup.get_page_metadata(map_soup)
				title_str = page_mdata['page_title']
				desc_str = ''
				if 'description' in page_mdata.keys(): desc_str = page_mdata['description']

				# # Get the title from the title of the map page
				# title_str = map_soup.find('title').text
				#
				# # Get the description from the meta tag
				# meta = map_soup.find('meta', attrs={"name": "description"})
				# if meta is None:
				#     desc = ''
				# else:
				#     desc = meta['content']

				date_str = ''
				dtype = 'Web Mapping Application'
				sp = ''

				if title_str == 'Map Preview':
					# Parse the URL query string
					query_dict = shared.query_to_dict(map_url)
					title = query_dict['MapTitle']
					title_str = title.replace('%20', ' ')
			else:
				# Get the information from the service URL
				serv_json = shared.get_json(serv_url)

				title_str = serv_json['title']
				date = serv_json['modified']
				date_str = shared.translate_date(date)
				dtype = serv_json['type']
				desc_str = serv_json['description']
				sp = serv_json['spatialReference']

			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', map_url)
			pt_csv.add('Data URL', serv_url)
			pt_csv.add('Type', dtype)
			pt_csv.add('Date', date_str)
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')
			pt_csv.add('Spatial Reference', sp)

			pt_csv.write_dataset()
			
		print

		#pt_csv.remove_duplicates('Web Map URL', True)

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_pages(self):
		''' Extract the New Brunswick pages with geospatial datasets
		:return: None
		'''

		self.print_title("Extracting New Brunswick's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		###########################################################################
		# Extract the NB Survey Control Network - Search

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting web page %s of %s pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the CCR url
		db_url = self.pg_grp.get_url('db_url')

		self.print_log("URL: %s" % db_url)

		# Create the CSV file
		csv_fn = "WebPages_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		db_soup = bsoup.get_soup(db_url)

		# Get the Database Information link by first locating <b with text 'Database Information'
		b = bsoup.find_tags_containing(db_soup, 'Database Information', 'b')
		# Get the next sibling with <a>
		a = b.find_next_sibling('a')
		download_url = shared.get_anchor_url(a, db_url)

		pt_csv.add('Title', "NB Survey Control Network - Database Information")
		pt_csv.add('Web Page URL', db_url)
		pt_csv.add('Access', 'Download/Accessible Web')
		pt_csv.add('Download', download_url)
		pt_csv.add('Available Formats', 'CSV')

		pt_csv.write_dataset()

		###########################################################################
		# Extract the Data Catalogue

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting web page %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the CCR url
		catal_url = self.pg_grp.get_url('catalogue_url')

		self.print_log("URL: %s" % catal_url)

		# Get the catalogue soup
		catal_soup = bsoup.get_soup(catal_url)

		# Get the table on the page
		table = catal_soup.find('table')
		table_dict = shared.table_to_dict(table, header_row=0)

		for res in table_dict:
			# Get the title from the Name column
			title_str = res['name'].text

			# Get the metadata link from the Details column
			mdata_link = res['details'].a['href']
			mdata_url = urlparse.urljoin(catal_url, mdata_link)

			# Get the date from the Date column
			date_str = res['date'].text

			# Get the formats from the Downloads column
			forms_a = res['downloads'].find_all('a')
			formats = [f.text for f in forms_a]

			# Open the metadata
			mdata_soup = bsoup.get_soup(mdata_url)
			p = mdata_soup.find('p')

			# Get the text of the <p> element on the page
			p_text = p.text
			p_text_list = p_text.split('\n')

			# Locate the <ol> on the page if a list of numbered items exist
			ol_text = ''
			ol = mdata_soup.find('ol')
			if ol is not None:
				# Locate all <li> under the <ol>
				li_list = ol.find_all('li')

				# Add <li> text to the ol_text
				for li in li_list:
					ol_text += li.text

			desc_str = ''
			sp_str = ''
			for line in p_text_list:
				# For each line in the <p> text
				if line.find(":") > -1:
					key = line.split(":")[0].strip()
					value = line.split(":")[1].strip()
					if key == "Data description":
						# Get the description of the dataset
						if ol_text == '':
							desc_str = value
						else:
							desc_str = value + ": " + ol_text
					elif key == 'Georeferencing':
						# Get the spatial reference
						sp_str = value

			# print "Title: " + str(title_str)
			# print "Metadata URL: " + str(mdata_url)
			# print "Formats: " + str(formats)

			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Page URL', catal_url)
			pt_csv.add('Date', date_str)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', 'Multiple Downloads')
			pt_csv.add('Spatial Reference', sp_str)
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Available Formats', "|".join(formats))

			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Extract the map services for New Brunswick
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting New Brunswick's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "MapServices_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		###########################################################################
		# Extract all services

		url_list = self.pg_grp.get_url_list()

		#print "URL List: " + str(url_list)

		for url in url_list:
		
			# Get a list of REST services
			my_rest = services.PT_REST(url)

			# Get the service and add it to the CSV file
			serv_data = my_rest.extract_data()
			
			if not self.check_result(serv_data, url, 'New Brunswick Map Service'): continue
			
			for rec in serv_data:
				for k, v in rec.items():
					pt_csv.add(k, v)

				pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time


def main():
	# tool_list = ['REST', 'GIS']
	# tool_list = ['Ducks', 'GIS', 'FlySask2']
	try:
		ext = Extractor()
		pages = ext.get_pagelist()

		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--page", help="The page to extract: %s or all" % ', '.join(pages.keys()))
		# parser.add_argument("-w", "--word", help="The key word(s) to search for.")
		# parser.add_argument("-f", "--format", help="The format(s) to search for.")
		# parser.add_argument("-c", "--category", help="The category(ies) to search for.")
		# parser.add_argument("-d", "--downloadable", help="Determines wheter to get only downloadable datasets.")
		# parser.add_argument("-l", "--html", help="The HTML file to scrape (only for OpenData website).")
		parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
		args = parser.parse_args()
		# print args.echo

		# print "province: " + str(args.province)
		# print "format: " + str(args.format)

		page = args.page
		# word = args.word
		# formats = args.format
		# html = args.html
		silent = args.silent
		# cats = args.category
		# downloadable = args.downloadable

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


if __name__ == '__main__':
	sys.exit(main())

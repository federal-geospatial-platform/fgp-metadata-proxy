import os
import sys
import urllib2
from bs4 import BeautifulSoup, Comment
import collections
import math
import csv
import re
import numpy as np
import json
import inspect
import urlparse
import argparse
import traceback
import datetime
import time
import pprint
import codecs

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
#from common import access_rest as rest
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
	
		# Set the province
		self.province = 'Nunavut'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create CGS page group

		cgs_grp = page_group.PageGroup('cgs', 'Government of Nunavut Community & Government Services Planning & Lands Division')
		
		# No arguments to add
		
		# Add URLs
		cgs_grp.add_url('main_url', 'https://cgs-pals.ca/')
		cgs_grp.add_url('shp_url', 'https://cgs-pals.ca/downloads/gis/')
		
		# Add to Extractor's page group list
		self.page_groups.append(cgs_grp)
		
		
		####################################################################
		# Create Maps & Data page group

		map_grp = page_group.PageGroup('mappage', 'Maps & Data - Department of Lands and Resources')
		
		# No arguments to add
		
		# Add URLs
		map_grp.add_url('main_url', 'http://ntilands.tunngavik.com/maps/')
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		
		
		####################################################################
		# Create Nunaliit Atlas Framework page group

		atlas_grp = page_group.PageGroup('atlas', 'Nunaliit Atlas Framework')
		
		# No arguments to add
		
		# Add URLs
		atlas_grp.add_url('main_url', 'http://nunaliit.org/')
		
		# Add to Extractor's page group list
		self.page_groups.append(atlas_grp)
		

	###################################################################################################################

	def extract_cgs(self):
		''' Extracts the Government of Nunavut Community & Government Services Planning & Lands Division
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nunavut's Community & Government Services (CGS) Planning & Lands Division")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		cgs_url = self.pg_grp.get_url('main_url')
		cgs_shp_url = self.pg_grp.get_url('shp_url')
		
		print "\nMain URL: %s" % cgs_url

		# Create the CSV file for the province
		csv_fn = "CGS_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Scraping the Shapefile download list is the best option
		#   since it contains the projection and other info
		cgs_soup = bsoup.get_soup(cgs_shp_url) #, True)

		# Get all DIV elements with class 'download-group' which contains each list
		#   of downloadable links
		div_list = cgs_soup.find_all('div', attrs={'class': 'download-group'})
		
		res_total = len(div_list)
		res_count = 0

		for div in div_list:

			# For each DIV, find a span with title 'About' (the About image)
			abouts = div.find_all('span', attrs={'title': 'About'})
			
			about_total = len(abouts)
			res_total += about_total

			for about in abouts:
				res_count += 1
				msg = "Extracting %s of %s results" % (res_count, res_total)
				shared.print_oneliner(msg)
				
				# The dataset's info is in the span's data-info attribute as JSON
				data_info = about['data-info']
				json_info = json.loads(data_info)

				#print "Data Info: " + str(json_info)

				# Get the title from the description
				title_str = json_info['description'].replace(" (Shapefile)", "")

				# Get the metadata which contains the coordinate system and date
				mdata = json_info['metadata']

				# Get the projection
				proj_str = mdata['Coordinate System']

				# Get the date
				date_str = mdata['Date Acquired']

				pt_csv.add('Title', title_str)
				pt_csv.add('Spatial Reference', proj_str)
				pt_csv.add('Date', date_str)
				pt_csv.add('Type', 'Vector File')
				pt_csv.add('Available Formats', 'SHP|DWG')
				pt_csv.add('Download', 'Multiple Downloads')
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Web Page URL', cgs_shp_url)

				pt_csv.write_dataset()
				
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_mappage(self):
		''' Extracts the Nunavut's Interactive maps
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nunavut's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		maps_url = self.pg_grp.get_url('main_url')
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Create the CSV file for the province
		csv_fn = "MapPage_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		maps_soup = bsoup.get_soup(maps_url)

		anchor = maps_soup.find('a', text='Online Interactive Map')
		interactive_url = anchor['href']

		# Get the title
		title_str = anchor.text

		# Get the date
		date = anchor.parent.text
		date_str = re.search(r'\d{4}-\d{2}-\d{2}', date).group()

		#print interactive_url

		pt_csv.add('Title', title_str)
		pt_csv.add('Date', date_str)
		pt_csv.add('Spatial Reference', 'NAD83 Geographic Projection')
		pt_csv.add('Type', 'Interactive Map')
		pt_csv.add('Download', 'No')
		pt_csv.add('Access', 'Viewable/Contact the Territory')
		pt_csv.add('Web Page URL', maps_url)
		pt_csv.add('Notes', "Currently under construction.")

		pt_csv.write_dataset()
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Find the h3 with 'GIS Datasets'
		h3 = maps_soup.find('h3', text='GIS Datasets')
		div = h3.find_next_sibling('div')

		# Get the title
		title = div.text
		start_pos = title.find("(")
		title_str = title[:start_pos]

		# Get the date
		anchor = div.a
		date = div.a.text
		start_pos = date.find("(")
		end_pos = date.find(")")
		date_str = date[start_pos+1:end_pos]

		# Get the download link
		zip_url = anchor['href']

		pt_csv.add('Title', title_str)
		pt_csv.add('Download', zip_url)
		pt_csv.add('Date', date_str)
		pt_csv.add('Type', 'ArcGIS Geodatabase')
		pt_csv.add('Spatial Reference', 'NAD83 Geographic Projection')
		pt_csv.add('Access', 'Download/Accessible Web')
		pt_csv.add('Web Page URL', maps_url)

		pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_atlas(self):
		''' Extracts the Nunaliit Atlas Framework
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nunavut's Nunaliit Atlas Framework")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		atlas_url = self.pg_grp.get_url('main_url')

		self.print_log("URL: %s" % atlas_url)

		# Create the CSV file for the province
		csv_fn = "Atlas_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		atlas_soup = bsoup.get_soup(atlas_url)

		# Get the title
		p_title = atlas_soup.find('p', attrs={'itemprop': 'name'})
		title_str = bsoup.get_text(p_title)

		# Get the description
		p_desc = atlas_soup.find('p', attrs={'itemprop': 'description'})
		desc_str = bsoup.get_text(p_desc)
		
		self.notes = 'Installed the pre-built binaries correctly but received an error ' \
						'"JSONObject["last_seq"] is not a number" when running the command ' \
						'"nunaliit run" in command prompt.'

		pt_csv.add('Title', title_str)
		pt_csv.add('Download', 'No')
		pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Application')
		pt_csv.add('Access', 'Contact the Territory')
		pt_csv.add('Web Page URL', atlas_url)
		pt_csv.add('Notes', self.notes)

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

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
		self.province = 'PEI'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Data Catalogue page group

		cat_grp = main_ext.PageGroup('catalogue', 'PEI Data Catalogue')
		
		# Add arguments
		cat_grp.add_arg('word', title='Search Word')
		ds_arg = cat_grp.add_arg('ds_type', title='Dataset Type', default='maps')
		ds_arg.add_opt('Calendars', url_tags=['calendars'])
		ds_arg.add_opt('Charts', url_tags=['charts'])
		ds_arg.add_opt('Data Lens pages', ['lens'], ['new_view'])
		ds_arg.add_opt('Datasets', url_tags=['datasets'])
		ds_arg.add_opt('External Datasets', ['external'], ['href'])
		ds_arg.add_opt('Files and Documents', ['docs'], ['blob'])
		ds_arg.add_opt('Filtered Views', ['filters'], ['filters'])
		ds_arg.add_opt('Forms', url_tags=['forms'])
		ds_arg.add_opt('Maps', url_tags=['maps'])
		
		# Add URLs
		cat_grp.add_url('main_url', 'https://data.princeedwardisland.ca/browse')
		
		# Add to Extractor's page group list
		self.page_groups.append(cat_grp)
		
		
		####################################################################
		# Create Interactive Maps page group

		map_grp = page_group.PageGroup('maps', 'PEI Interactive Maps')
		
		# No arguments to added
		
		# Add URLs
		map_grp.add_url('gallery_url',
					   'https://peitie.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title')
		map_grp.add_url('maps_url', 'http://www.gov.pe.ca/maps/index.php3')
		map_grp.add_url('eefcs_url',
					   'http://peitie.maps.arcgis.com/apps/webappviewer/index.html?webmap=d9a9d2edfe494f5e9610c3443a9032e4')
		map_grp.add_url('active_url',
					   'http://peitie.maps.arcgis.com/apps/MapJournal/index.html?appid=225121b0e2ab415fa48c3d6dad7d5df7')
		map_grp.add_url('traffic_url',
					   'https://peitie.maps.arcgis.com/apps/webappviewer/index.html?id=e41b62bff037413884cf8f44b002a200')
		map_grp.add_url('water_url', 'https://www.princeedwardisland.ca/en/service/view-groundwater-level-data')
		map_grp.add_url('xmas_url',
					   'https://www.princeedwardisland.ca/en/information/communities-land-and-environment/island-christmas-trees-and-wreaths')
		map_grp.add_url('wells_url', 'https://www.princeedwardisland.ca/en/service/high-capacity-wells')
		map_grp.add_url('watershed_url', 'https://www.princeedwardisland.ca/en/service/find-pei-watershed-group')
		map_grp.add_url('ccr_url', 'http://www.ecdaofpei.ca/registry.php')
		map_grp.add_url('points_url', 'https://www.princeedwardisland.ca/en/points-of-interest-map')
		map_grp.add_url('walking_url', 'https://www.princeedwardisland.ca/en/topic/walking-and-hiking')
		map_grp.add_url('housing_url', 'https://www.princeedwardisland.ca/en/information/family-and-human-services/housing-assistance')
		map_grp.add_url('conf_url', 'https://www.tourismpei.com/pei-confederation-trail')
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		
		
		####################################################################
		# Create GIS Pages page group

		gis_grp = page_group.PageGroup('pages', 'PEI GIS Pages')
		
		# No arguments to add
		
		# Add URLs
		gis_grp.add_url('monuments_url',
					['http://eservices.gov.pe.ca/pei-icis/monument/list.do;jsessionid=2FCC7CA75D195DB50EF2D9177B543870',
					 "http://eservices.gov.pe.ca/pei-icis/support/surveymonument.jsp;jsessionid=223C94139B11E10ABDC878FCCABD8A7C"])
		gis_grp.add_url('cat_url', 'http://www.gov.pe.ca/gis/index.php3?number=77543&lang=E')
		
		# Add to Extractor's page group list
		self.page_groups.append(gis_grp)
		
		
		####################################################################
		# Create Services page group

		srv_grp = page_group.PageGroup('services', 'Web Map Services')
		
		# No arguments to add
		
		# Add URLs
		srv_grp.add_url('serv_url', 'https://services5.arcgis.com/6bkn2iYF5h1LCwgM/arcgis/rest/services')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		

	###################################################################################################################

	def get_metadata(self, soup):
		''' Gets the metadata information in CSV inventory form from the PEI web page.
		:param soup: The soup object containing the <meta> elements.
		:return: A dictionary of inventory keys and values.
		'''
		
		# Create the output dictionary
		mdata_items = collections.OrderedDict()
	
		# Get the page's metadata
		water_mdata = bsoup.get_page_metadata(soup)
		
		# Get the title
		if 'dcterms.title' in water_mdata.keys(): title_str = water_mdata['dcterms.title']
		
		# Get the description
		if 'dcterms.description' in water_mdata.keys():
			desc_str = water_mdata['dcterms.description']
			end = desc_str.find('[')
			desc_str = desc_str[:end]
		
		# Get the date
		if 'dcterms.modified' in water_mdata.keys(): date = water_mdata['dcterms.modified']
		
		# Get the publisher
		if 'department' in water_mdata.keys(): pub_str = water_mdata['department']
		
		# Add metadata values to dictionary
		mdata_items['Title'] = title_str
		mdata_items['Description'] = desc_str
		mdata_items['Date'] = date
		mdata_items['Publisher'] = pub_str
		
		return mdata_items
	
	def extract_catalogue(self): #, word=None, ds_type=None):
		###########################################################################
		# Extract the PEI's Open Data Portal
		
		# Get the parameters
		word = self.get_arg_val('word')
		ds_type = self.get_arg('ds_type')

		main_url = self.pg_grp.get_url('main_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting PEI's Portal")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "Catalogue_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Build the search URL and search the portal
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['q'] = word
		if ds_type is not None and not ds_type == '':
			params['limitTo'] = ds_type.get_urltags()[0]

		query_url = shared.get_post_query(main_url, params)

		res_soup = bsoup.get_soup(query_url)
		
		print "Query URL: %s" % query_url
		#print res_soup
		
		# Check if there are no results
		res_span = res_soup.find('span', class_='browse2-no-results-message')
		#print "res_span: %s" % res_span
		if res_span is not None:
			print "\nNumber of results: 0"
			return None

		# Get the page count
		res_div = res_soup.find('div', attrs={'class': 'browse2-result-count'})
		res_str = res_div.text.strip()
		count_list = res_str.split(" ")
		#print count_list
		per_page_list = count_list[1].split('-')
		#print per_page_list
		per_page = per_page_list[1]
		res_count = count_list[3]
		page_count = math.ceil(float(res_count) / float(per_page))
		page_count = int(page_count)

		print "Number of pages: " + str(page_count)

		data_url = 'https://data.princeedwardisland.ca/api/views/'
		
		record_count = 0
		
		print "\nExtracting query URL: %s" % query_url

		for page in range(0, page_count):
			page_url = "%s&page=%s" % (query_url, page + 1)

			page_soup = bsoup.get_soup(page_url)

			results = page_soup.find_all('div', attrs={'class': 'browse2-result'})

			for res in results:
				record_count += 1
				msg = "Extracting record %s of %s" % (record_count, res_count)
				shared.print_oneliner(msg)
			
				title_a = res.find('a', attrs={'class': 'browse2-result-name-link'})
				title = title_a.text
				link = title_a['href']

				date_span = res.find('span', attrs={'class': 'dateLocalize'})
				date = date_span.text

				# Get JSON of the data
				desc_str = ''
				link_split = link.split('/')
				id = link_split[len(link_split) - 1]
				# print "ID: " + str(id)
				data_link = data_url + id
				data_json = shared.get_json(data_link)
				# print data_json

				# Get description
				desc_str = ''
				if 'description' in data_json:
					desc_str = data_json['description']

				# Get date
				date = data_json['indexUpdatedAt']
				date_str = shared.translate_date(date)

				# Get the license
				lic_str = data_json['license']['name']

				# Get the projection
				metadata = data_json['metadata']
				if 'geo' in metadata:
					geo = metadata['geo']
					sp_str = geo['bboxCrs']
				else:
					sp_str = ''

				# Get the author
				table_author = data_json['tableAuthor']
				author_str = table_author['displayName']

				# Create download link
				download_url = 'https://data.princeedwardisland.ca/api/' \
								'geospatial/%s?method=export&format=Original' % id

				# print "Description: " + str(desc_str)
				# print "Date: " + str(date_str)
				# print "License: " + str(lic_str)
				# print "Spatial Reference: " + str(sp_str)
				# print "Download Link: " + str(download_url)
				# print "Author: " + str(author_str)

				# answer = raw_input("Press enter...")
				
				pt_csv.add('Source', 'PEI Open Data Portal')
				pt_csv.add('Title', title)
				pt_csv.add('Date', date_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Licensing', lic_str)
				pt_csv.add('Web Page URL', link)
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Download', download_url)
				pt_csv.add('Data URL', data_link)
				pt_csv.add('Publisher', author_str)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Available Formats', 'KML|KMZ|SHP|GeoJSON')

				pt_csv.write_dataset()
		
		print
		
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting PEI's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		#db_url = self.pg_grp.get_url('db_url')

		#self.print_log("URL: %s" % db_url)

		# Create the CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		####################################################################################
		# Extract the peitie.maps.arcgis.com Gallery

		gallery_url = self.pg_grp.get_url('gallery_url')

		# Get the gallery data
		gallery_maps = shared.get_arcgis_gallery(gallery_url)

		for idx, map in enumerate(gallery_maps):
		
			msg = "Extracting %s of %s maps from gallery '%s'" % (idx + 1, len(gallery_maps), gallery_url)
			shared.print_oneliner(msg)
		
			for k, v in map.items():
				pt_csv.add(k, v)

			pt_csv.add('Source', 'PEI Interactive Maps')
				
			pt_csv.write_dataset()
			
		print

		####################################################################################
		# Extract the other ArcGIS maps

		arcgis_urls = self.pg_grp.get_arcgis_urls()

		for idx, url in enumerate(arcgis_urls):
			if url.find('gallery') == -1:
				msg = "Extracting %s of %s ArcGIS maps" % (idx + 1, len(arcgis_urls))
				shared.print_oneliner(msg)

				# Get the ArcGIS data
				arcgis_info = shared.get_arcgis_data(url)

				# Add the ArcGIS data to the CSV
				for k, v in arcgis_info.items():
					pt_csv.add(k, v)

				# Add all values to the CSV file
				pt_csv.add('Source', 'PEI Interactive Maps')
				pt_csv.add('Access', 'Viewable/Map Service')
				pt_csv.add('Download', 'No')
				#pt_csv.add('Web Page URL', url[1])
				pt_csv.add('Web Map URL', url)

				pt_csv.write_dataset()
				
		print

		##############################################################################################
		# Extract PEI's Interactive Maps

		maps_url = self.pg_grp.get_url('maps_url')

		maps_soup = bsoup.get_soup(maps_url)

		table = maps_soup.find('table')

		table_rows = shared.table_to_dict(table, header=['title', 'description'])
		
		# Create a list of maps that have sub-pages
		sub_pgs = ['Address Locator', 'Aerial Photos', #'Community Accounts', 
					'Drinking Water Quality Application', 'PEI LandOnline']

		for idx, row in enumerate(table_rows):
			msg = "Extracting %s of %s interactive maps from '%s'" % (idx + 1, len(table_rows), maps_url)
			shared.print_oneliner(msg)
		
			# Get the title
			title_str = bsoup.get_text(row['title'])

			# Get the description
			desc_str = bsoup.get_text(row['description'])

			# NOTE: Frogwatch is a broken link
			# Ignore: Geolinc Plus
			# Sport Facilities is broken link
						
			# Fill in the rest of the inventory items
			sub_url = shared.get_anchor_url(row['title'].a, maps_url)
			
			if title_str == "Frogwatch" or title_str == "Sport Facilities":
				notes_str = "This link is broken"
				
				pt_csv.add('Source', 'PEI Interactive Maps')
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Page URL', maps_url)
				pt_csv.add('Access', 'Contact the Province')
				pt_csv.add('Web Map URL', sub_url)
				pt_csv.add('Notes', notes_str)
				
				pt_csv.write_dataset()
				
				continue
						
			if title_str in sub_pgs:
				# Get the information from the sub-page
				if title_str == 'Address Locator':
					# Open the sub-page
					sub_soup = bsoup.get_soup(sub_url)
				
					# Get the map link
					strong = bsoup.find_tags_containing(sub_soup, 'Address Locator Map', 'strong')
					map_a = strong.parent
					map_url = shared.get_anchor_url(map_a, sub_url)
				elif title_str == 'Aerial Photos':
					# Open the sub-page
					sub_soup = bsoup.get_soup(sub_url)
					
					# Get the map link
					map_a = bsoup.find_tags_containing(sub_soup, 'Click here to view the map', 'a')
					map_url = shared.get_anchor_url(map_a, sub_url)
				# elif title_str == 'Community Accounts':
					# # Open the sub-page
					# sub_soup = bsoup.get_soup(sub_url)
					
					# # Get the map link
				elif title_str == 'Drinking Water Quality Application':
					# Open the sub-page
					sub_soup = bsoup.get_soup(sub_url)
					
					# Get the map link
					map_a = bsoup.find_tags_containing(sub_soup, 'Search Drinking Water Quality Application', 'a')
					map_url = shared.get_anchor_url(map_a, sub_url)
				# elif title_str == 'PEI LandOnline':
					# # Open the sub-page
					# sub_soup = bsoup.get_soup(sub_url)
					
					# # Get the map link
					# map_a = bsoup.find_tags_containing(sub_soup, 'Search Drinking Water Quality Application', 'a')
					# map_url = shared.get_anchor_url(map_a, sub_url)
			else:
				map_url = sub_url
			
			pt_csv.add('Source', 'PEI Interactive Maps')
			pt_csv.add('Title', title_str)
			#pt_csv.add('Date', date_str)
			pt_csv.add('Description', desc_str)
			#pt_csv.add('Licensing', lic_str)
			pt_csv.add('Web Page URL', maps_url)
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Web Map URL', map_url)
			#pt_csv.add('Publisher', author_str)
			#pt_csv.add('Spatial Reference', sp_str)
			#pt_csv.add('Available Formats', 'KML|KMZ|SHP|GeoJSON')

			pt_csv.write_dataset()
		
		print
		
		##############################################################################################
		# Extract Groundwater Level Data
		
		print "**** Extracting Groundwater Level Data map ****"
		
		water_url = self.pg_grp.get_url('water_url')
		water_soup = bsoup.get_soup(water_url)
		
		# Get the page's metadata
		water_mdata = self.get_metadata(water_soup)
		
		# Add metadata to the CSV file
		for k, v in water_mdata.items():
			pt_csv.add(k, v)
		
		# Get the map URL
		map_a = bsoup.find_tags_containing(water_soup, 'Access Groundwater Data by Reference Map', 'a')
		map_url = shared.get_anchor_url(map_a, map_url)
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Web Page URL', water_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract Island Christmas Trees and Wreaths
		
		print "**** Extracting Christmas Trees and Wreaths map ****"

		xmas_url = self.pg_grp.get_url('xmas_url')
		xmas_soup = bsoup.get_soup(xmas_url)
		
		# Get the page's metadata
		xmas_mdata = self.get_metadata(xmas_soup)
		
		# Add metadata to the CSV file
		for k, v in xmas_mdata.items():
			pt_csv.add(k, v)
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', xmas_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract High Capacity Wells
		
		print "**** Extracting High Capacity map ****"
		
		wells_url = self.pg_grp.get_url('wells_url')
		wells_soup = bsoup.get_soup(wells_url)
		
		# Get the metadata of the page
		wells_mdata = self.get_metadata(wells_soup)
		
		# Add metadata to the CSV file
		for k, v in wells_mdata.items():
			pt_csv.add(k, v)
			
		# Get the map URL
		map_a = bsoup.find_tags_containing(water_soup, 'View Map', 'a')
		map_url = shared.get_anchor_url(map_a, wells_url)
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		pt_csv.add('Web Page URL', wells_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract PEI Watershed Group
		
		print "**** Extracting Watershed Group map ****"
		
		watershed_url = self.pg_grp.get_url('watershed_url')
		watershed_soup = bsoup.get_soup(watershed_url)
		
		# Get the metadata of the page
		watershed_mdata = self.get_metadata(watershed_soup)
		
		# Add metadata to the CSV file
		for k, v in watershed_mdata.items():
			pt_csv.add(k, v)
			
		# Get the map URL
		map_a = bsoup.find_tags_containing(watershed_soup, 'Find my Watershed Group', 'a')
		map_url = shared.get_anchor_url(map_a, watershed_url)
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		pt_csv.add('Web Page URL', watershed_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract Child Care Registry
		
		print "**** Extracting Child Care Registry map ****"
		
		ccr_url = self.pg_grp.get_url('ccr_url')
		ccr_soup = bsoup.get_soup(ccr_url)
		
		# Get the metadata of the page
		ccr_mdata = bsoup.get_page_metadata(ccr_soup)
		
		# Get the title
		title_str = ccr_mdata['TITLE']
		
		# Get the description
		desc_str = ccr_mdata['DESCRIPTION']
		
		# Get the date
		date = ccr_mdata['creation date']
		
		# Get the publisher
		pub_str = ccr_mdata['copyright']
		
		# Get the map URL
		map_a = bsoup.find_tags_containing(ccr_soup, 'Visit the PEI ELCC Registry', 'a')
		map_url = shared.get_anchor_url(map_a, ccr_url)
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Title', title_str)
		pt_csv.add('Date', date)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Web Page URL', ccr_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		pt_csv.add('Publisher', pub_str)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract PEI's Point of Interest map
		
		print "**** Extracting PEI's Point of Interest map ****"
		
		points_url = self.pg_grp.get_url('points_url')
		
		title_str = "Prince Edward Island's Points of Interest Map"
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Title', title_str)
		pt_csv.add('Type', 'Google Maps')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', points_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract Walking and Hiking map
		
		print "**** Extracting Walking and Hiking map ****"
		
		walking_url = self.pg_grp.get_url('walking_url')
		walking_soup = bsoup.get_soup(walking_url)
		
		# Get all <div> elements with class 'views-row'
		row_divs = walking_soup.find_all('div', attrs={'class': 'views-row'})
		
		map_row = row_divs[6]
		
		# Get the map URL
		map_a = map_row.find('a')
		map_url = shared.get_anchor_url(map_a, walking_url)
		
		# Get the title from the map_a text
		title_str = bsoup.get_text(map_a)
		
		# Get the description from the <span> in the map_row
		desc_str = bsoup.get_text(map_row.find('span'))
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Web Page URL', walking_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract Seniors Housing Units
		
		print "**** Extracting Seniors Housing Units map ****"
		
		housing_url = self.pg_grp.get_url('housing_url')
		housing_soup = bsoup.get_soup(housing_url, True, delay=60)
		
		# To get the map information, locate the map link and open it
		map_a = bsoup.find_tags_containing(housing_soup, 'View a larger version of the map', 'a')
		map_url = shared.get_anchor_url(map_a, housing_url)
		map_soup = bsoup.get_soup(map_url)
		
		# Get the map page's metadata
		map_mdata = bsoup.get_page_metadata(map_soup)
		
		# Get the title
		title_str = map_mdata['og:title']
		
		# Get the description
		desc_str = map_mdata['description']
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', map_url)
		pt_csv.add('Web Page URL', housing_url)
		
		pt_csv.write_dataset()
		
		##############################################################################################
		# Extract Confederation Trail
		
		print "**** Extracting Confederation Trail map ****"
		
		conf_url = self.pg_grp.get_url('conf_url')
		conf_soup = bsoup.get_soup(conf_url, True)
		
		# Get the metadata of the page
		conf_mdata = bsoup.get_page_metadata(conf_soup)
		
		# Get the title from the metadata
		title_str = conf_mdata['name']
		
		# Get the description from the metadata
		desc_str = conf_mdata['description']
		
		# Get the date from the metadata
		date_str = conf_mdata['article:modified_time']
		
		pt_csv.add('Source', 'PEI Interactive Maps')
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Date', date_str)
		pt_csv.add('Type', 'Google Maps')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Web Map URL', conf_url)
		
		pt_csv.write_dataset()
		
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_pages(self):
		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting PEI's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "Pages_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		#pt_csv.add_header_item('Download_Link')
		pt_csv.open_csv()

		# 'monuments_url': 'http://eservices.gov.pe.ca/pei-icis/monument/list.do;jsessionid=2FCC7CA75D195DB50EF2D9177B543870')
		# 'cat_url', 'http://www.gov.pe.ca/gis/index.php3?number=77543&lang=E'

		###########################################################################
		# Extract monuments
		
		print "**** Extracting Monuments web page ****"

		monuments_url = self.pg_grp.get_url('monuments_url')[0]
		mondesc_url = self.pg_grp.get_url('monuments_url')[1]

		mondesc_soup = bsoup.get_soup(mondesc_url)

		# Get the description from another page
		brief_strong = mondesc_soup.find('strong', text='Brief History')
		desc = brief_strong.next_sibling
		desc = desc.next_sibling
		desc = desc.next_sibling
		#print "Desc: " + str(desc)
		if isinstance(desc, NavigableString):
			desc_str = bsoup.get_text(desc)
		elif desc is not None:
			desc_str = desc.text
		else:
			desc_str = ''

		# Get the title
		title_td = mondesc_soup.find('td', attrs={'class': 'header'})
		title_str = title_td.text

		pt_csv.add('Source', 'PEI Pages - Geolinc Plus')
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Point coordinates listed on the page')
		#pt_csv.add('Service URL', serv_url)
		pt_csv.add('Access', 'Web Accessible')
		pt_csv.add('Web Page URL', monuments_url)
		#pt_csv.add('Service Name', serv_name)
		pt_csv.add('Spatial Reference', 'Multiple Spatial References')
		#pt_csv.add('Service', 'ESRI REST')
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# Extract GIS catalogue
		
		print "**** Extracting GIS Catalogue web page ****"

		cat_url = self.pg_grp.get_url('cat_url')

		catal_soup = bsoup.get_soup(cat_url)

		# Get all the sub-pages in the sidebar
		ul = catal_soup.find('ul', attrs={'id': 'subnavlist'})
		a_list = ul.find_all('a')

		# Get the <a> elements of Free GIS Products from the sidebar
		prod_a = catal_soup.find('a', text='Free GIS Products')
		prod_a2 = catal_soup.find('a', text="Free GIS Products (con't)")

		# Add the Free GIS anchors to the list
		anchors = [a for a in a_list]
		anchors.append(prod_a)
		anchors.append(prod_a2)

		header = []
		for idx, a in enumerate(anchors):
			# Go through each link
			
			msg = "Extracting %s of %s sub-pages from '%s'" % (idx + 1, len(anchors), cat_url)
			shared.print_oneliner(msg)
			
			source = bsoup.get_text(a)

			url = urlparse.urljoin(cat_url, a['href'])

			# Open the sub-page
			sub_soup = bsoup.get_soup(url)

			# Get the table on the sub-page
			table = sub_soup.find('table')

			# Convert the table rows to dictionaries
			if url == 'http://www.gov.pe.ca/gis/index.php3?number=1012857&lang=E':
				table_rows = shared.table_to_dict(table, header=header)
			else:
				table_rows = shared.table_to_dict(table, 0)

			if url == 'http://www.gov.pe.ca/gis/index.php3?number=77868&lang=E':
				header = table_rows[0].keys()

			for row in table_rows:

				if 'metadata' in row.keys():
					mdata_url = ''
					mdata_cell = row['metadata']
					mdata_a = mdata_cell.find('a')
					if not mdata_a is None:
						mdata_link = mdata_a['href']
						mdata_url = urlparse.urljoin(cat_url, mdata_link)
						#print "mdata_url: " + str(mdata_url)
						mdata_soup = bsoup.get_soup(mdata_url)

						title_p = mdata_soup.find('p', attrs={'class': 'pgTitle'})
						if title_p is None:
							title_str = row['data layers'].text
						else:
							title_str = bsoup.get_text(title_p)

						desc_em = mdata_soup.find('em', text='Abstract:')
						if desc_em is None:
							desc_str = row['data layers'].text
						else:
							desc_str = desc_em.next_sibling

							desc_str = desc_str.strip()

							if desc_str == '':

								dt = desc_em.parent
								dd = dt.find_next_sibling('dd')

								if dd is None:
									desc_str = ''
								else:
									desc_str = dd.text
									desc_str = desc_str.strip()

								#print "Desc_str: '%s'" % desc_str

								#answer = raw_input("Press enter...")
					else:
						title_str = bsoup.get_text(row['data layers'])
						desc_str = ''
						mdata_url = ''

				else:
					title_str = bsoup.get_text(row['data layers'])
					desc_str = ''
					mdata_url = ''

				if 'download' in row.keys():
					download_cell = row['download']
				else:
					download_cell = row['download format']

				formats = ''
				formats_str = download_cell.text
				if formats_str == 'NA':
					formats = ''
					access_str = 'Contact the Province'
					download_url = 'No'
					lic_url = title_str
				elif formats_str == 'GIS Price List':
					download_url = 'No'
					access_str = 'For Purchase'
					lic_url = title_str
				else:
					format_list = [f.strip() for f in formats_str.split(',')]
					formats = '|'.join(format_list)

					download_a = download_cell.find_all('a')
					if len(download_a) == 0:
						download_url = 'No'
						access_str = 'Contact the Province'
						lic_url = title_str
					elif len(download_a) > 1:
						download_url = 'Multiple Downloads'
						access_str = 'Download/Web Accessible'
						lic_url = download_a[0]['href']
					else:
						link = download_a[0]['href']
						lic_url = urlparse.urljoin(url, link)

						down_soup = bsoup.get_soup(lic_url)
						input = down_soup.find('input', attrs={'name': 'downloadfile'})
						if input is None:
							download_url = 'No'
							access_str = 'Contact the Province'
						else:
							download_url = input['value']
							access_str = 'Download/Web Accessible'
							
				# if source.find('Community') > -1:
					# print
					# print title_str
					# print "mdata_url: %s" % row['metadata']
					# answer = raw_input("Press enter...")
				
				pt_csv.add('Source', 'PEI Catalogue - %s' % \
							source.replace(" (con't)", ''))
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Type', '')
				# pt_csv.add('Service URL', serv_url)
				pt_csv.add('Access', access_str)
				pt_csv.add('Web Page URL', url)
				# pt_csv.add('Service Name', serv_name)
				pt_csv.add('Spatial Reference', 'PEI Survey Reference System')
				pt_csv.add('Available Formats', formats)
				pt_csv.add('Metadata URL', mdata_url)
				pt_csv.add('Download', download_url)
				#pt_csv.add('Download_Link', lic_url)

				pt_csv.write_dataset()

		print
				
		#pt_csv.remove_duplicates('Download_Link', True)

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting PEI's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "MapServices_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# pg.add_page('geonb_url', 'http://geonb.snb.ca/arcgis/rest/services')
		# pg.add_page('geoportal_url', 'http://geoportal-geoportail.gc.ca/arcgis/rest/services')
		# pg.add_page('dnr_url', 'http://maps-dnr-mrn.gnb.ca/arcgis/rest/services')
		# pg.add_page('proxy_url', 'http://proxyinternet.nrcan.gc.ca/arcgis/rest/services')
		# pg.add_page('erd_url', 'https://gis-erd-der.gnb.ca/arcgis/rest/services/PNAs')

		###########################################################################
		# Extract all services

		serv_url = self.pg_grp.get_url('serv_url')

		#print "URL List: " + str(url_list)

		#for url in url_list:

		my_rest = services.PT_REST(serv_url)
		# services = my_rest.get_services()
		
		serv_data = my_rest.get_layers()
		
		if self.check_result(serv_data, serv_url, 'ArcGIS REST Service'):
			for rec in serv_data:
				for k, v in rec.items():
					pt_csv.add(k, v)
				
				pt_csv.add('Source', 'PEI Map Services')
				pt_csv.write_dataset()

		# for service in services:

			# if 'err' in service:
				# pt_csv.add('Title', service['name'])
				# pt_csv.add('Service Name', service['name'])
				# pt_csv.add('Service URL', service['url'])
				# pt_csv.add('Notes', 'Service could not be loaded.')

				# pt_csv.write_dataset()

				# continue

			# # Get the service name
			# serv_name = service['name']

			# # Get the map name
			# if 'mapName' in service:
				# map_name = service['mapName']
				# if map_name == "Layers":
					# # print "Map Name: '%s'" % map_name
					# # answer = raw_input("Press enter...")
					# map_name = serv_name
				# title_str = shared.split_upper(map_name)
			# else:
				# title_str = shared.split_upper(serv_name)

			# serv_type = service['type']

			# # Get the description
			# desc_str = ''
			# if 'serviceDescription' in service:
				# desc_str = service['serviceDescription']

			# # UPDATE FOR ESRI REST SERVICES
			# #   All services allow the following formats:
			# #       json (JavaScript Object Notation)
			# #       kmz (compressed KML, or Keyhole Markup Language)
			# #       lyr (layer file)
			# #       nmf (ArcGIS Explorer map file)
			# #       amf (Action Message Format)
			# #formats = ['JSON', 'KMZ', 'LYR', 'NMF', 'AMF']
			# #pt_csv.add('Available Formats', "|".join(formats))

			# # Get the service URL
			# serv_url = service['url']

			# # Get the spatial reference
			# proj_str = shared.get_spatialref(service)

			# pt_csv.add('Title', title_str)
			# pt_csv.add('Description', desc_str)
			# pt_csv.add('Type', serv_type)
			# pt_csv.add('Service URL', serv_url)
			# pt_csv.add('Access', 'Viewable/Contact the Province')
			# pt_csv.add('Service Name', serv_name)
			# pt_csv.add('Spatial Reference', proj_str)
			# pt_csv.add('Service', 'ESRI REST')
			# pt_csv.add('Download', 'Multiple Downloads')

			# pt_csv.write_dataset()

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

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
from common import access_rest as rest
from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
	
		# Set the province
		self.province = 'NL'
		
		# Create the page groups dictionary
		self.page_groups = []
		self.page_groups = collections.OrderedDict()

		pg_grp = page_group.PageGroup('catalogue', "Newfoundland & Labrador's Open Data Catalogue")
		pg_grp.add_url('open_url', 'http://opendata.gov.nl.ca/public/opendata/page/?page-id=datasets-spatial')
		self.set_args(pg_grp)
		self.page_groups['catalogue'] = pg_grp

		pg_grp = page_group.PageGroup('webpages', 'Newfoundland & Labrador Web Pages')
		pg_grp.add_url('flr_url', 'http://www.flr.gov.nl.ca/lands/maps/digital_map.html')
		pg_grp.add_url('mae_url', 'http://www.mae.gov.nl.ca/waterres/gis/gis.html')
		pg_grp.add_url('frm_url', 'http://www.mae.gov.nl.ca/waterres/flooding/frm.html')
		pg_grp.add_url('wrp_url', 'http://maps.gov.nl.ca/water/mapservices.htm')
		self.set_args(pg_grp)
		self.page_groups['webpages'] = pg_grp

		pg_grp = page_group.PageGroup('maps', "Newfoundland & Labrador Interactive Maps")
		pg_grp.add_url('ccr_url', 'http://childcare.gov.nl.ca/public/ccr/')
		pg_grp.add_url('child_url', 'http://www.ed.gov.nl.ca/edu/earlychildhood/guide.html')
		pg_grp.add_url('dvms_url', 'http://nl.communityaccounts.ca/mapcentre/')
		pg_grp.add_url('petrol_url',
				   ['http://www.arcgis.com/home/webmap/viewer.html?webmap=f6e1e859a7c24ca89b5d9d8b93148731',
					''])
		pg_grp.add_url('geol_url',
				   ['http://www.arcgis.com/apps/MapJournal/index.html?appid=98298581238b45f89aeadfb33e5036b9',
					'http://www.nr.gov.nl.ca/nr/energy/petroleum/onshore/onshore_maps.html'])
		pg_grp.add_url('app_url',
				   ['http://www.arcgis.com/apps/MapJournal/index.html?appid=98298581238b45f89aeadfb33e5036b9',
					'http://www.nr.gov.nl.ca/nr/energy/petroleum/onshore/onshore_maps.html'])
		pg_grp.add_url('geoscience_url', ['http://geoatlas.gov.nl.ca/Default.htm', 'http://gis.geosurv.gov.nl.ca/'])
		pg_grp.add_url('cims_url', ['http://nlcims.ca/CIMS.aspx', 'http://www.nlcims.ca/'])
		pg_grp.add_url('water_url', ['https://maps.gov.nl.ca/water/mapbrowser/Default.aspx',
								 'http://maps.gov.nl.ca/water/index.aspx'])
		pg_grp.add_url('comm_url', 'http://www.stats.gov.nl.ca/DataTools/RoadDB/Distance/')
		pg_grp.add_url('landuse_url',
				   ['https://gov.nl.ca/landuseatlas/details/',
					'http://www.flr.gov.nl.ca/gis/lua.html'])
		pg_grp.add_url('topo_url', 'http://mapsnl.ca/mapguide/Topo/')
		pg_grp.add_url('motor_url', 'http://opendata.gov.nl.ca/public/opendata/page/?page-id=mvr_home')
		self.set_args(pg_grp)
		self.page_groups['maps'] = pg_grp

		# Set the services page
		pg_grp = page_group.PageGroup('services', "Newfoundland & Labrador Services")
		pg_grp.add_url('dnr_url', 'http://dnrmaps.gov.nl.ca/arcgis/rest/services')
		pg_grp.add_url('gsdw_url', 'http://maps.gov.nl.ca/gsdw/rest/services')
		pg_grp.add_url('landuse_url', 'https://www.gov.nl.ca/landuseatlasmaps/rest/services')
		self.set_args(pg_grp)
		self.page_groups['services'] = pg_grp

		#######################################################################################################
		# Municipal Pages
		pg_grp = page_group.PageGroup('gander', 'Gander Map Viewer')
		pg_grp.add_url('main_url', 'http://geonl.net/mapguide/GanderPublic/')
		pg_grp.add_url('legctrl_url', 'http://geonl.net/mapguide/mapviewerphp/legendctrl.php')
		pg_grp.add_url('legend_url', 'http://geonl.net/mapguide/GanderPublic/Gander_LayerUpdates.php')
		self.set_args(pg_grp)
		self.page_groups['gander'] = pg_grp

		pg_grp = page_group.PageGroup('labrador', 'Labrador City Map Viewer')
		pg_grp.add_url('main_url', 'http://labcitymaps.ca/')
		pg_grp.add_url('legend_url', 'http://labcitymaps.ca/mapguide/LabCityPublic/LayerUpdates.php')
		self.set_args(pg_grp)
		self.page_groups['labrador'] = pg_grp

		#######################################################################################################
		# Other pages

		pg_grp = page_group.PageGroup('icemap', 'Iceberg Map')
		pg_grp.add_url('main_url', 'http://www.icebergfinder.com/')
		self.set_args(pg_grp)
		self.page_groups['icemap'] = pg_grp
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
	def get_province(self):
		''' Gets the province name of the extractor.
		:return: The province name of the extractor.
		'''
		
		return self.province

	###################################################################################################################

	def parse_legend(self, start):

		# Get the CCR url
		main_url = self.pg_grp.get_url('main_url')
		legend_url = self.pg_grp.get_url('legend_url')

		self.print_log("URL: %s" % legend_url)

		# Soup the page
		legend_soup = shared.soup_php(legend_url)

		# Get a list of all the 'p' elements on the page
		p_list = legend_soup.find_all('p')
		# groups = ul.contents

		# The spatial reference for each layer is in the second 'p'
		# print p_list[start].text
		proj_str = p_list[start].text.split(":")[1]
		proj_str = proj_str.strip()

		# Get the different layers from the rest of the 'p' elements
		rec_list = []
		for p in p_list[start + 1:]:
			rec_dict = collections.OrderedDict()

			# The title is located in the first 'b' element
			title = p.find('b').text

			# br_list = p.find_all('br')

			#p_text = p.bsoup.get_text()
			p_text = bsoup.get_text(p)
			lines = p_text.split("\n")
			# Get the last item
			date_str = lines[len(lines) - 1]
			if date_str.find('Source') > -1:
				date_str = lines[len(lines) - 2]

			if date_str.find(':') > -1:
				date_str = date_str.split(':')[1].strip()

			date_str = date_str.replace(">", "")

			rec_dict['Title'] = title
			# rec_dict['Download URL'] = data_url
			rec_dict['Download'] = 'No'
			rec_dict['Access'] = 'Viewable/Contact the Province'
			rec_dict['Type'] = "Autodesk Mapguide"
			if not date_str == "": rec_dict['Date'] = date_str
			rec_dict['Spatial Reference'] = proj_str.strip('.')
			rec_dict['Web Map URL'] = main_url

			rec_list.append(rec_dict)

		return rec_list

	def extract_catalogue(self):
		''' Extracts the NL Open Data GeoSpatial Datasets catalogue
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Newfoundland & Labrador's Catalogue")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Maps CSV file
		csv_fn = "Catalogue_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		##########################################################################
		# Extract the NL Open Data GeoSpatial Datasets search results
		###########################################################################

		# Get the elections URL
		open_url = self.pg_grp.get_url('open_url')

		self.print_log("URL: %s" % open_url)

		# Get the soup
		soup = bsoup.get_soup(open_url)
		
		if not self.check_result(soup, open_url, 'NL Open Data'):
			print soup
			return None

		results = soup.find_all('div', attrs={'class': 'well'})

		for idx, res in enumerate(results):
		
			# Print status
			msg = "Extracting %s of %s results" % (idx + 1, len(results))
			shared.print_oneliner(msg)

			# Get the metadata soup
			mdata_url = urlparse.urljoin(open_url, res.a['href'])
			mdata_soup = bsoup.get_soup(mdata_url)

			# Get the info from the page
			title = bsoup.get_adj_text_by_label(mdata_soup, 'dt', 'Title')
			creator = bsoup.get_adj_text_by_label(mdata_soup, 'dt', 'Creator')
			recdate = bsoup.get_adj_text_by_label(mdata_soup, 'dt', 'Modified Date')
			license = bsoup.get_adj_text_by_label(mdata_soup, 'dt', 'Rights')

			# Extract the table
			table = mdata_soup.find('table')
			table_vals = shared.table_to_dict(table)

			# print "table_vals: %s" % table_vals

			# Get the formats
			format_list = [d['format'].text for d in table_vals]
			formats_str = "|".join(format_list)

			# Get the download link, if applicable
			download_a = mdata_soup.find_all('a', attrs={'title': 'Download'})
			if len(download_a) == 0:
				download_str = 'No'
			elif len(download_a) > 1:
				download_str = 'Multiple Downloads'
			else:
				link = download_a[0]['href']
				download_url = urlparse.urljoin(open_url, link)
				download_str = download_url

			# Store in the CSV file
			pt_csv.add('Title', title)
			# rec_dict['Licensing'] = 'Open Data'
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Creator', creator)
			pt_csv.add('Date', date)
			pt_csv.add('Available Formats', formats_str)
			pt_csv.add('Download', download_str)
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Licensing', license)
			pt_csv.add('Web Page URL', open_url)
			# rec_dict['Data URL'] =

			pt_csv.write_dataset()
			
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		''' Extracts all the interactive maps for Newfoundland & Labrador
		:return: None
		'''

		self.print_title("Extracting Newfoundland & Labrador's Interactive Maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# Create or append the CSV file
		csv_fn = "Maps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		##########################################################################
		# Extract the Department of Education and Early Childhood Development's
		#	Early Learning and Child Care Directory map page
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the CCR url
		ccr_url = self.pg_grp.get_url('ccr_url')

		# Get the soup
		soup = bsoup.get_soup(ccr_url)
		
		if self.check_result(soup, ccr_url, 
								'Early Learning and Child Care Directory'):
			
			# Get the title of the page
			main_div = soup.find('div', attrs={'id': 'gnlcontent'})
			h1 = main_div.find('h1')
			title_str = bsoup.get_text(h1)

			#print title_str

			# Get the description
			p = main_div.p
			desc_str = bsoup.get_text(p)

			# Set the other variables
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', shared.edit_description(desc_str))
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Type', "Google Maps API")
			pt_csv.add('Web Map URL', ccr_url)
			pt_csv.add('Download', 'No')

			pt_csv.write_dataset()

			# Get the updated date
			#date_div = soup.find('div', attrs={'id': 'gnlupdated'})
			#date_str = bsoup.get_text(date_div)

		##########################################################################
		# Extract the Early Childhood Programs and Services map page
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the CCR url
		child_url = self.pg_grp.get_url('child_url')

		# self.print_log("URL: %s" % ccr_url)

		# Get the soup
		soup = bsoup.get_soup(child_url)
		
		if self.check_result(soup, child_url, 
								'Early Childhood Programs and Services'):

			# Get the title of the page
			h1 = soup.find('h1')
			title_str = bsoup.get_text(h1)

			#print title_str

			# self.print_log(soup)

			# Get the description
			main_div = soup.find('div', attrs={'class': 'section_divider'})
			desc_str = bsoup.get_text(main_div)

			# Set the other variables
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', shared.edit_description(desc_str))
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Type', "Google Maps API")
			pt_csv.add('Web Map URL', ccr_url)
			pt_csv.add('Download', 'No')

			pt_csv.write_dataset()

			# Get the updated date
			# date_div = soup.find('div', attrs={'id': 'gnlupdated'})
			# date_str = bsoup.get_text(date_div)
			# date_str = date_str.replace("Last Updated: ", "")
			# rec_dict['Date'] = date_str

		###########################################################################
		# Extract the Data Visualization Mapping Suite
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the DVMS url
		dvms_url = self.pg_grp.get_url('dvms_url')
		ds_map_url = 'http://nl.communityaccounts.ca/mapcentre/dynamicmap.asp?_=zozLioaVqaKnl2aTYpvFvqSuug__'
		aboutus_url = 'http://nl.communityaccounts.ca/about_us.asp'

		self.print_log("URL: %s" % dvms_url)

		soup = bsoup.get_soup(ds_map_url, True)
		
		if self.check_result(soup, ds_map_url, 
								'Data Visualization Mapping Suite'):
		
			#print soup
			select = soup.find('select', attrs={'id': 's_g'})
			opts = select.find_all('option')

			# Get the description from the About Us page
			about_soup = bsoup.get_soup(aboutus_url)
			desc_str = bsoup.get_text(about_soup.p)

			for opt in opts:
				title_str = bsoup.get_text(opt)
				#print title_str

				pt_csv.add('Title', title_str)
				pt_csv.add('Type', 'Google Maps API')
				pt_csv.add('Access', 'Viewable/Contact the Province')
				pt_csv.add('Download', 'No')
				pt_csv.add('Web Map URL', dvms_url)
				pt_csv.add('Description', desc_str)

				pt_csv.write_dataset()
				
			print

		###########################################################################
		# Extract the ArcGIS Maps
		###########################################################################

		# Get the ArcGIS URLs
		arcgis_urls = self.pg_grp.get_arcgis_urls('landuseatlasportal')

		for idx, url in enumerate(arcgis_urls):
			msg = "Extracting ArcGIS map %s of %s maps" % (idx + 1, len(arcgis_urls))
			shared.print_oneliner(msg)
		
			#print url

			# Get the ArcGIS data
			arcgis_info = shared.get_arcgis_data(url)

			# Add the ArcGIS data to the CSV
			for k, v in arcgis_info.items():
				pt_csv.add(k, v)

			# Add all values to the CSV file
			pt_csv.add('Access', 'Viewable/Map Service')
			pt_csv.add('Download', 'No')
			pt_csv.add('Web Page URL', url[1])
			pt_csv.add('Web Map URL', url[0])

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Geoscience Atlas
		###########################################################################
		
		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)
		
		# Get the Geoscience Atlas url
		map_url = self.pg_grp.get_url('geoscience_url')[0]
		main_url = self.pg_grp.get_url('geoscience_url')[1]

		# Get the map soup
		map_soup = bsoup.get_soup(map_url, True)

		# Get the service URL for the map
		# map_div = map_soup.find('div', attrs={'id': 'map_layer1'})
		# map_img = map_div.find('img')
		# serv_large_url = map_img['src']
		# end_pos = serv_large_url.find('GeoAtlas')
		# serv_url = serv_large_url[:end_pos]

		# Get the title from the page
		#title_str = map_soup.find('td', attrs={'id': 'a51153'})

		# Add the data to the CSV
		pt_csv.add('Title', 'Geoscience Atlas')
		#pt_csv.add('Description', desc_str)
		pt_csv.add('Download', 'No')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Type', "Google Maps API")
		pt_csv.add('Web Map URL', map_url)
		pt_csv.add('Web Page URL', main_url)

		###########################################################################
		# Extract the Community Infrastructure Mapping System
		###########################################################################

		# Get the CIMS URL
		cims_url = self.pg_grp.get_url('cims_url')[0]
		webpage_url = self.pg_grp.get_url('cims_url')[1]
		
		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Soup the page
		cims_soup = bsoup.get_soup(cims_url, True)

		# The layers list is in <ul> with id 'layerGroups'
		ul = cims_soup.find('ul', attrs={'id': 'layerGroups'})

		# Get a list of all anchors in <ul>
		a_list = ul.find_all('a', attrs={'class': 'groupToggle'})

		# Get the description from the main page
		webpage_soup = bsoup.get_soup(webpage_url)
		h3 = bsoup.find_tags_containing(webpage_soup, 'About CIMS', 'h3')
		desc_p = h3.find_next_siblings('p')
		#print ''
		#print type(desc_p)
		desc_str = bsoup.get_text(desc_p)

		for index, anchor in enumerate(a_list):

			# Get the title of the group
			group = anchor.parent
			title_str = anchor.text

			# Get the layer IDs
			lyr_lst = group.find_all('li')
			lyr_ids = []
			for lyr in lyr_lst:
				id = lyr['id'].replace('layer', '')
				lyr_ids.append(id)

			# Add the data to the CSV
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Download', 'No')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Type', "Google Maps API")
			pt_csv.add('Web Map URL', cims_url)
			pt_csv.add('Web Page URL', webpage_url)

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Topographic Map Viewer
		###########################################################################

		# Print the status
		cur_page += 1
		msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
		shared.print_oneliner(msg)
		
		# Get the CIMS URL
		topo_url = self.pg_grp.get_url('topo_url')

		# Soup the page
		topo_soup = bsoup.get_soup(topo_url)

		# Get the title from the page's title
		title_str = bsoup.get_text(topo_soup.find('title'))

		# Add the data to the CSV
		pt_csv.add('Title', title_str)
		pt_csv.add('Download', 'No')
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Type', "Autodesk Mapguide")
		pt_csv.add('Web Map URL', topo_url)
		
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_webpages(self):
		''' Extract datasets from NL webpages.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Newfoundland & Labrador's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Maps CSV file
		csv_fn = "Webpages_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()

		##########################################################################
		# Extract the Fisheries and Land Resources's Digital Map Index page
		###########################################################################

		# Get the FLI url
		flr_url = self.pg_grp.get_url('flr_url')
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		self.print_log("URL: %s" % flr_url)

		# Get the soup
		soup = bsoup.get_soup(flr_url)
		
		if not self.check_result(soup, flr_url, 
						"Fisheries and Land Resources's " \
						"Digital Map Index page"):
			print soup
			return None

		# Get the description
		pgrph = soup.p
		desc_str = bsoup.get_text(pgrph)

		links = soup.find_all('a')

		for a in links:
			a_link = a['href']
			title = a.text
			if a_link.find('.kmz') > -1 or a_link.find('.kml') > -1:

				url = urlparse.urljoin(flr_url, a_link)

				format = a_link.split(".")[1]

				pt_csv.add('Title', title)
				pt_csv.add('Type', 'Google Earth File')
				pt_csv.add('Download', url)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Page URL', flr_url)
				pt_csv.add('Access', "Viewable/Contact the Province")
				pt_csv.add('Available Formats', format.upper())

				pt_csv.write_dataset()

		###########################################################################
		# Extract the Municipal Affairs and Environment's
		#	GIS Data - Public Water Supplies map
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the FLI url
		mae_url = self.pg_grp.get_url('mae_url')

		self.print_log("URL: %s" % mae_url)

		# Get the soup
		soup = bsoup.get_soup(mae_url)

		strong = soup.find('strong', text='ILUC')
		li = strong.parent
		url = li.a['href']
		title = bsoup.get_text(li.a)

		pt_csv.add('Title', title)
		pt_csv.add('Type', 'ESRI Shapefile')
		pt_csv.add('Access', 'Download/Accessible Web')
		pt_csv.add('Web Page URL', mae_url)
		pt_csv.add('Download', url)
		pt_csv.add('Available Formats', "SHP")

		pt_csv.write_dataset()

		###########################################################################
		# Extract the Flood Risk map page
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the Flood url
		frm_url = self.pg_grp.get_url('frm_url')

		self.print_log("URL: %s" % frm_url)

		# Get the soup
		soup = bsoup.get_soup(frm_url)

		# Extract the description by finding the first 'p' element
		pgrph = soup.p
		desc_str = bsoup.get_text(pgrph)

		# Extract all the 'tr' (rows) elements on the page
		rows = soup.find_all('tr')

		# Cycle through each row and get the 'td' (column) element and
		#   find all the anchors that contain either 'DWG' or 'Shapefile'
		#   in their text and extract their URLs
		for row in rows:
			cols = row.find_all('td')

			if len(cols) == 0: continue

			# Get the title
			text = bsoup.get_first_text(cols[0])
			title = text

			# Get the date
			date_col = cols[1]
			date = date_col.text

			# Get the formats
			formats = []
			urls = []
			links = row.find_all('a')
			for a in links:
				a_text = a.text
				if a_text.find("DWG") > -1:
					formats.append('DWG')
					urls.append(a['href'])
				elif a_text.find("Shapefile") > -1:
					formats.append('SHP')
					urls.append(a['href'])

			if len(formats) > 0:
				formats = set(formats)

				pt_csv.add('Title', title)
				pt_csv.add('Type', 'Vector File')
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Description', desc_str)
				pt_csv.add('Date', date)
				pt_csv.add('Available Formats', '|'.join(formats))
				pt_csv.add('Web Page URL', frm_url)
				if len(formats) > 1:
					pt_csv.add('Download', 'Multiple Downloads')
				else:
					pt_csv.add('Download', urls[0])
				pt_csv.write_dataset()

		###########################################################################
		# Extract the Water Resources ArcGIS REST
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		# Get the URL
		wrp_url = self.pg_grp.get_url('wrp_url')

		wrp_soup = bsoup.get_soup(wrp_url)

		tables = wrp_soup.find_all('table')

		#print "Number of tables: %s" % len(tables)

		for table in tables:
			# Get the title from the <h3>
			h3 = table.find('h3')
			title_str = bsoup.get_text(h3)

			# Get the rows
			rows = table.find_all('tr')

			# Get the description
			desc_row = rows[1]
			desc_str = bsoup.get_text(desc_row)

			# Set the formats and downloads as they are the same for every dataset
			formats = ['KZM', 'NMF', 'LYR']
			download_str = 'Multiple Downloads'

			# Get the capabilities
			wms_row = rows[4]
			data_url = wms_row.a['href']

			# Add the data to the CSV file
			pt_csv.add('Title', title_str)
			pt_csv.add('Type', 'Vector Data')
			pt_csv.add('Download', download_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Page URL', wrp_url)
			pt_csv.add('Data URL', data_url)
			pt_csv.add('Access', "Download/Web Accessible")
			pt_csv.add('Available Formats', '|'.join(formats))

			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Extract NL map services.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Newfoundland & Labrador's Map Services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Maps CSV file
		csv_fn = "Services_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		url_list = self.pg_grp.get_url_list()

		for url in url_list:
			# Get a list of REST services
			my_rest = rest.MyREST(url)

			# Get the service and add it to the CSV file
			serv_data = my_rest.extract_data()
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

		##################################################################################################################
		# Extract Municipal Pages
		##################################################################################################################

	def extract_gander(self):
		''' Extracts the Gander sites
		:return: None
		'''
		###########################################################################
		# Extract from Gander Map Viewer
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Gander's interactive map")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		gander_url = self.pg_grp.get_url('main_url')
		legend_url = self.pg_grp.get_url('legend_url')

		self.print_log("URL: %s" % legend_url)

		# Create the Gander CSV file
		csv_fn = "Municipal_Gander_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		data_info = self.parse_legend(1)

		for rec in data_info:
		
			for k, v in rec.items():
				pt_csv.add(k, v)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_labrador(self):
		''' Extracts the Labrador City sites
		:return: None
		'''

		###########################################################################
		# Extract from Labrador Map Viewer
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Labrador City's interactive map")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Labrador City CSV file
		csv_fn = "Municipal_LabradorCity_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		data_info = self.parse_legend(2)

		for rec in data_info:
			for k, v in rec.items():
				pt_csv.add(k, v)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	##################################################################################################################
	# Extract Other pages
	##################################################################################################################

	def extract_icemap(self):
		''' Extract the other pages.
		:return: None
		'''

		###########################################################################
		# Extract from Gander Map Viewer
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Newfoundland & Labrador's Ice Map")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		ice_url = self.pg_grp.get_url('main_url')

		self.print_log("URL: %s" % ice_url)

		# Create the CSV file
		csv_fn = "Other_IceFinder_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		ice_soup = bsoup.get_soup(ice_url)

		# Get the title of the page
		#h1 = ice_soup.find('h1')
		#title_str = bsoup.get_text(h1)

		# Get the information from the page's metadata
		ice_mdata = bsoup.get_page_metadata(ice_soup)
		#print "ice_mdata: %s" % ice_mdata
		title_str = ice_mdata['page_title']
		desc_str = ice_mdata['description']

		# Set the other variables
		# rec_dict['Description'] = desc_str
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Type', "Google Maps API")
		pt_csv.add('Web Map URL', ice_url)
		pt_csv.add('Download', 'No')

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

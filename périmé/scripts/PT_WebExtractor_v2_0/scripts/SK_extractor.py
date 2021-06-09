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
import urlparse
import argparse
import inspect
import traceback
import datetime
import time
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
from common import services
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

# province = 'Saskatchewan'
# work_folder = 'H:\\GIS_Data\\Work\\NRCan\\FGP\\TA001\\_%s' % province
# site_list = collections.OrderedDict([
#                 ('flysask2', ('extract_flysask2()', 'https://www.flysask2.ca/cubewerx')),
#                 ('rest', ('extract_REST()', 'https://gis.saskatchewan.ca/arcgis/rest/services')),
#                 ('gistest', ('extract_GISTest()', 'https://gistest.saskatchewan.ca/arcgis/rest/services')),
#                 ('geocortex', ('extract_Geocortex()', 'https://gisappl.saskatchewan.ca/Geocortex/Essentials/EXT/REST/sites')),
#                 ('wsask_geocortext', ('extract_WSASK_Geocortext()', 'https://gis.wsask.ca/Geocortex/Essentials/GeocortexEssentials/REST/sites')),
#                 ('wsask_rest', ('extract_WSASK_REST()', 'https://gis.wsask.ca/arcgiswa/rest/services/')),
#                 ('elections', ('extract_elections()', 'http://www.elections.sk.ca/voters/maps/'))])

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		''' Initializer for the Extractor class. '''

		# Set the province
		self.province = 'Saskatchewan'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Services page group

		srv_grp = main_ext.PageGroup('services', "Saskatchewan Services")
		
		# Add arguments
		sb_arg = srv_grp.add_arg('subpage', debug=True, default='all')
		sb_arg.add_opt('Geocortex Services', url_tags=['geocortex'])
		sb_arg.add_opt('FlySask2 Services', ['flysask'], ['flysask'])
		sb_arg.add_opt('ArcGIS REST Services', ['rest'], ['rest'])
		sb_arg.add_opt('Saskatoon Services', ['sask'], ['saskatoon'])
		sb_arg.add_opt('WSask Services', ['wsask'], ['wsask'])
		sb_arg.add_opt('Ducks Unlimited Services', ['ducks'], ['ducks'])
		
		# Add URLs
		srv_grp.add_url('rest_url', 'https://gis.saskatchewan.ca/arcgis/rest/services')
		srv_grp.add_url('gistest_url', 'https://gistest.saskatchewan.ca/arcgis/rest/services')
		srv_grp.add_url('geo_url', 'https://gisappl.saskatchewan.ca/Geocortex/Essentials/EXT/REST/sites')
		srv_grp.add_url('geoportal_url', ['https://www.flysask2.ca/cubewerx/cubeserv.cgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities',
									'https://www.flysask2.ca/cubewerx/cubeserv.cgi/default/wmts/1.0.0/WMTSCapabilities.xml'])
		srv_grp.add_url('saskatoon_url', ['http://arcgis-cosgis-1729149607.us-west-2.elb.amazonaws.com/arcgis/rest/services',
									  'http://rpbackgis2.saskatoon.ca/ArcGIS/rest/services',
									  'http://rpstggis2.saskatoon.ca/ArcGIS/rest/services'])
		srv_grp.add_url('regina_url', 'https://opengis.regina.ca/arcgis/rest/services')
		srv_grp.add_url('wsask_url', 'https://gis.wsask.ca/arcgiswa/rest/services')
		srv_grp.add_url('wsaskgeo_url', 'https://gis.wsask.ca/Geocortex/Essentials/GeocortexEssentials/REST/sites')
		srv_grp.add_url('ducks_url', 'http://maps.ducks.ca/arcgis/rest/services')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create Interactive Maps page group

		map_grp = main_ext.PageGroup('maps', "Saskatchewan Interactive Maps")
		
		# Add arguments
		sb_arg = map_grp.add_arg('subpage', debug=True, default='all')
		sb_arg.add_opt('Provincial Maps', ['prov'], ['prov'])
		sb_arg.add_opt('Sasktoon Maps', ['sask_maps'], ['maps'])
		sb_arg.add_opt('Sasktoon Address Maps', ['sask_add'], ['address'])
		sb_arg.add_opt('iMap', ['imap'], ['imap'])
		sb_arg.add_opt('FlySask2 Geoportal', ['geoportal'], ['geoportal'])
		sb_arg.add_opt('Ducks Unlimited Maps', ['ducks'], ['ducks'])
		
		# Add URLs
		map_grp.add_url('saskmaps_url',
				   'http://www.saskatchewan.ca/government/notarize-documents-publications-saskatchewan-maps-and-other-publications/maps')
		map_grp.add_url('address_url',
					'https://www.saskatoon.ca/business-development/planning/planning-publications-maps/address-map')
		map_grp.add_url('zoning_url',
					'https://www.saskatoon.ca/business-development/planning/planning-publications-maps/zoning-address-map')
		map_grp.add_url('main_url', 'https://www.saskatoon.ca/interactive-maps')
		map_grp.add_url('imap_url', ['https://www.saskatoon.ca/business-development/planning/maps',
					'http://rpbackapps2.saskatoon.ca/lapp/Geocortex/Essentials/GeocortexAnon/COSSV/Viewer.html?Viewer=iMap_GeneralVW'])
		map_grp.add_url('ducks_url', 'http://www.ducks.ca/initiatives/gis-mapping-applications/')
		map_grp.add_url('geoportlet_url', {'map_url': 'https://www.flysask2.ca/cubewerx/geoportlet/',
									  'about_url': 'https://www.flysask2.ca/homepage/',
									  'serv_url': 'https://www.flysask2.ca/cubewerx/cubeserv.cgi'})
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)

		
		####################################################################
		# Create Web Pages page group
		
		web_grp = main_ext.PageGroup('webpages', 'Saskatchewan Web Pages')
		
		# Add arguments
		sb_arg = web_grp.add_arg('subpage', debug=True, default='all')
		sb_arg.add_opt('Elections Saskatchewan', ['elections'], ['elections'])
		sb_arg.add_opt('Regina Open Data', ['regina'], ['regina'])
		sb_arg.add_opt('Saskatoon Open Catalogue', ['sask'], ['saskatoon'])
		sb_arg.add_opt('Community View Catalogue', ['comm'], ['commview'])
		
		# Add URLs
		web_grp.add_url('elections_url', 'http://www.elections.sk.ca/voters/maps/')
		web_grp.add_url('regina_url', 'http://open.regina.ca/')
		web_grp.add_url('saskatoon_url',
				   ['http://opendata-saskatoon.cloudapp.net/DataBrowser/SaskatoonOpenDataCatalogueBeta',
					'http://opendata-saskatoon.cloudapp.net:8080/v1/SaskatoonOpenDataCatalogueBeta'])
		web_grp.add_url('commview_url', 'http://www.communityview.ca/Catalogue')
		
		# Add to Extractor's page group list
		self.page_groups.append(web_grp)
		
		
	###################################################################################################################

	def print_dict(self, in_dict):
		# dict_list = ["%s: '%s'" % (k, v) for k, v in in_dict.items()]
		dict_list = []
		for k, v in in_dict.items():
			try:
				dict_list.append("%s: '%s'" % (k, v))
				print '\t\t'.join(dict_list)
			except Exception as e:
				continue

	def extract_maps(self): #, subpage='all'):
		''' Extracts the pages for Saskatchewan Interactive Maps
		:return: None
		'''
		
		# Get the parameter
		subpage = self.get_arg('subpage').get_urltags()[0]
		
		#print "subpage: %s" % subpage
		#answer = raw_input("Press enter...")
		
		self.print_title("Extracting Saskatchewan Interactive Maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# NOTE: subpage is for debugging only
		if subpage is None: subpage = 'all'
		# subpage = 'all'

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		########################################################################################################
		# Go through all the interactive maps on Access Geographic Information page
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()

		if subpage == 'prov' or subpage == 'all':
		
			#print "**** Extracting Access Geographic Information page ****"

			# Create or append the CSV file
			csv_fn = "Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			saskmaps_url = self.pg_grp.get_url('saskmaps_url')

			saskmaps_soup = bsoup.get_soup(saskmaps_url)

			main_div = saskmaps_soup.find('section', attrs={'class': 'general-content'})

			map_anchors = main_div.find_all('a')

			links = []
			for idx, a in enumerate(map_anchors):
				msg = "Extracting %s of %s map from Access Geographic Information page" % (idx + 1, len(map_anchors))
				shared.print_oneliner(msg)
			
				map_link = a['href']

				if map_link in links: continue

				if map_link.find('gisappl.saskatchewan.ca') > -1 and \
					map_link.find('SilverlightExt') == -1 and map_link.find('.pdf') == -1:
					# Only choose map links with 'gisappl.saskatchewan.ca' and rule out
					#   any SilverlightExt in the URL

					# Get the title
					title_str = bsoup.get_text(a)

					# Get the network info
					map_network_info = shared.get_network_traffic(map_link, ['id', 'map'])
					
					if not self.check_result(map_network_info, map_link): continue

					# Get the service URL from the network info
					net_log = map_network_info['log']
					net_entries = net_log['entries']

					serv_url = ''
					for entry in net_entries:
						request = entry['request']
						url = request['url']

						if url.find('Geocortex') > -1:
							serv_url = url
							print url

					# Add all values to the CSV file
					pt_csv.add('Source', 'Saskatchewan Interactive Maps')
					pt_csv.add('Title', title_str)
					pt_csv.add('Type', 'Interactive Map')
					pt_csv.add('Access', 'Viewable/Map Service')
					pt_csv.add('Download', 'No')
					pt_csv.add('Web Map URL', map_link)
					pt_csv.add('Service URL', serv_url)
					pt_csv.add('Notes', self.notes)

					pt_csv.write_dataset()

					links.append(map_link)

			print
			
			#pt_csv.remove_duplicates('Web Map URL')

			pt_csv.close_csv()

		########################################################################################################
		# Get the Saskatoon page with many interactive maps

		if subpage == 'maps' or subpage == 'all':

			# Create or append the CSV file
			csv_fn = "Municipal_Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			main_url = self.pg_grp.get_url('main_url')

			# Get the soup of the map page
			main_soup = bsoup.get_soup(main_url)

			# Get the page content <div>
			main_div = main_soup.find('div', attrs={'id': 'main-content'})

			# Get the title
			buttons = main_div  .find_all('a', attrs={'class': 'btn'})

			for idx, button in enumerate(buttons):
				msg = "Extracting %s of %s map from Saskatoon's maps" % (idx + 1, len(buttons))
				shared.print_oneliner(msg)
			
				# Get map URL
				map_url = button['href']

				# Get the soup of the map
				map_soup = bsoup.get_soup(map_url)

				# Get the entries for the current button
				network_urls = shared.get_network_urls(map_url, ['id', 'divMblTabPanel'], 15)
				
				#print "network_urls: %s" % network_urls

				map_services = []
				for url in network_urls:
					# Grab any network URL that includes "MapServer"
					if url.find('MapServer') > -1:
						pos = url.find('MapServer') + len('MapServer')
						map_services.append('%s?f=pjson' % url[:pos])

				if map_url.find('arcgis') > -1:
					# Get the ArcGIS data
					arcgis_info = shared.get_arcgis_data(map_url, 'Saskatoon')

					# Add the ArcGIS data to the CSV
					for k, v in arcgis_info.items():
						pt_csv.add(k, v)
				else:
					# Get the title from the map page
					title = map_soup.find('title')
					title_str = bsoup.get_text(title)
					title_str = 'Saskatoon - %s' % title_str

					# Get the projection from one of the MapServices
					#print "map_services: %s" % map_services
					if len(map_services) > 0:
						mserver_json = shared.get_json(map_services[0])
						sp_str = shared.get_spatialref(mserver_json)

						#print "Spatial Reference: %s" % sp_str

						# Get the description
						parent_p = button.parent
						desc_p = parent_p.find_next_sibling('p')
						desc_str = bsoup.get_text(desc_p)

						pt_csv.add('Title', title_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Type', 'Interactive Map')
						pt_csv.add('Spatial Reference', sp_str)

				# Add all values to the CSV file
				pt_csv.add('Source', 'Saskatchewan Interactive Maps')
				pt_csv.add('Access', 'Viewable/Map Service')
				pt_csv.add('Download', 'No')
				pt_csv.add('Web Page URL', main_url)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Notes', self.notes)
				# pt_csv.add('Service URL', data_url)

				pt_csv.write_dataset()

			print
			
			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

		########################################################################################################
		# Get the Saskatoon Address Map and Zoning Map

		if subpage == 'address' or subpage == 'zoning' or subpage == 'all':

			# Create or append the CSV file
			csv_fn = "Municipal_Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			urls = []
			urls.append(self.pg_grp.get_url('address_url'))
			urls.append(self.pg_grp.get_url('zoning_url'))

			for idx, url in enumerate(urls):
				msg = "Extracting %s of %s map from other Saskatoon's maps" % (idx + 1, len(urls))
				shared.print_oneliner(msg)

				# Get the soup of the map page
				map_soup = bsoup.get_soup(url)

				# Get the description from the page
				desc_meta = map_soup.find('meta', attrs={'name': 'description'})
				desc_str = desc_meta['content']

				# Get the contents <div>
				content = map_soup.find('div', attrs={'id': 'main-content'})

				# Get the button of the link to the address map
				a_but = content.find('a', attrs={'class': 'btn'})
				map_url = a_but['href']

				# Get the ArcGIS data
				arcgis_info = shared.get_arcgis_data(map_url, 'Saskatoon')

				# Add the ArcGIS data to the CSV
				for k, v in arcgis_info.items():
					pt_csv.add(k, v)

				pt_csv.add('Source', 'Saskatchewan Interactive Maps')
				pt_csv.add('Description', desc_str)
				pt_csv.add('Access', 'Viewable')
				pt_csv.add('Download', 'No')
				pt_csv.add('Web Page URL', url)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Notes', self.notes)

				pt_csv.write_dataset()

			print
			
			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

		########################################################################################################
		# Get iMap using Internet Explorer

		if subpage == 'imap' or subpage == 'all':
		
			print "**** Extracting iMap ****"

			# Create or append the CSV file
			csv_fn = "Municipal_Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			# Get the home page containing a link to the iMap
			imap_home_url = self.pg_grp.get_url('imap_url')[0]
			imap_home_soup = bsoup.get_soup(imap_home_url)
			
			self.notes = 'Requires Silverlight using Internet Explorer.'

			if self.check_result(imap_home_soup, imap_home_url, 'iMap'):

				# Get the map page
				imap_url = self.pg_grp.get_url('imap_url')[1]

				# To get the title, find the <h3> with 'Interactive iMap'
				title_h3 = bsoup.find_tags_containing(imap_home_soup, 'Interactive iMap', 'h3')
				title_str = "Saskatoon - %s" % bsoup.get_text(title_h3)

				# Get the description from the first <p> sibling of the <h3>
				p_sib = title_h3.find_next_sibling('p')
				desc_str = bsoup.get_text(p_sib)

				# Add all values to the CSV file
				pt_csv.add('Source', 'Saskatchewan Interactive Maps')
				pt_csv.add('Title', title_str)
				pt_csv.add('Type', 'Interactive Map')
				pt_csv.add('Description', desc_str)
				pt_csv.add('Access', 'Viewable/Contact the Province')
				pt_csv.add('Download', 'No')
				pt_csv.add('Web Map URL', imap_url)
				pt_csv.add('Web Page URL', imap_home_url)
				pt_csv.add('Notes', self.notes)

				pt_csv.write_dataset()

			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

			# imap_soup = bsoup.get_soup(imap_url, selenium=True, browser='ie')
			#
			# # Check if Silverlight needs to be installed
			# img = imap_soup.find('img', attrs={'alt': 'Get Microsoft Silverlight'})
			# if img is not None:
			#     print "\nWARNING: Silverlight needs to be installed in order to access the iMap."
			#     print "Please install it using Internet Explorer."
			# else:
			#     # If Silverlight is installed, continue extraction
			#     print "Does nothing!"

		########################################################################################################
		# Get the FlySask2 GeoPortal

		if subpage == 'geoportal' or subpage == 'all':
		
			print "**** Extracting FlySask2 Geoportal page ****"
		
			# Create or append the CSV file
			csv_fn = "Organization_Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			map_url = self.pg_grp.get_url('geoportlet_url')['map_url']
			data_url = self.pg_grp.get_url('geoportlet_url')['serv_url']
			about_url = self.pg_grp.get_url('geoportlet_url')['about_url']

			# Get the soup of the map page
			map_soup = bsoup.get_soup(map_url)

			# Find the <div> with id 'cw_banner'
			banner_div = map_soup.find('div', attrs={'id': 'cw_banner'})

			# Find the span in the banner
			title_span = banner_div.find('span')
			title_str = bsoup.get_text(title_span)

			# To get the description, use the about page
			about_soup = bsoup.get_soup(about_url)
			cont_div = about_soup.find('div', attrs={'class': 'entry-content'})
			desc_str = bsoup.get_text(cont_div)

			# Add all values to the CSV file
			pt_csv.add('Source', 'Saskatchewan Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Type', 'Interactive Map')
			pt_csv.add('Access', 'Viewable/Map Service')
			pt_csv.add('Download', 'No')
			pt_csv.add('Web Map URL', map_url)
			pt_csv.add('Service URL', data_url)
			pt_csv.add('Notes', self.notes)

			pt_csv.write_dataset()

			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

		########################################################################################################
		# Get Ducks Unlimited map

		if subpage == 'ducks' or subpage == 'all':

			# Create or append the CSV file
			csv_fn = "Organization_Maps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			# Get the home page containing a link to the iMap
			ducks_url = self.pg_grp.get_url('ducks_url')
			ducks_soup = bsoup.get_soup(ducks_url, selenium=True)

			if ducks_soup is not None:

				# Find all <a> with text 'View Map'
				map_anchors = bsoup.find_tags_containing(ducks_soup, ['View Map'], 'a', output='list')

				#print "map_anchors: %s" % map_anchors

				for idx, a in enumerate(map_anchors):
					msg = "Extracting %s of %s Ducks Unlimited maps" % (idx + 1, len(map_anchors))
					shared.print_oneliner(msg)
				
					map_url = shared.get_anchor_url(a, ducks_url)

					map_soup = bsoup.get_soup(map_url)

					# Find the previous <h3> or <h2> tag, whichever comes first
					h = bsoup.find_prev_tag_containing(a, 'h')
					h_text = bsoup.get_text(h)

					if h_text == 'Smith Creek' or h_text == 'Canadian Wetland Inventory' \
							or h_text == 'Waterfowl Migration Map' \
							or h_text == 'Dip Your Paddle Story Map':

						# Get the desc <p>
						desc_p = h.find_next_sibling('p')
						desc_str = bsoup.get_text(desc_p)

						# Get the title
						title_str = "Ducks Unlimited - %s" % h_text
						print title_str

						# Add all values to the CSV file
						pt_csv.add('Source', 'Saskatchewan Interactive Maps')
						pt_csv.add('Title', title_str)
						pt_csv.add('Type', 'Interactive Map')
						pt_csv.add('Description', desc_str)
						pt_csv.add('Access', 'Viewable/Contact the Province')
						pt_csv.add('Download', 'No')
						pt_csv.add('Web Map URL', map_url)
						pt_csv.add('Web Page URL', ducks_url)
						pt_csv.add('Notes', self.notes)

						pt_csv.write_dataset()
						
				print

			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()
			
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_webpages(self): #, subpage='all'):
		''' Extracts all the pages for the Province of Saskatchewan,
			including municipal and private organizations linked on the
			provincial website.
		:return: None
		'''
		
		# Get the parameter
		subpage = self.get_arg('subpage').get_urltags()[0]
		
		self.print_title("Extracting Saskatchewan's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# NOTE: subpage is for debugging only
		if subpage is None: subpage = 'all'
		# subpage = 'all'

		if subpage == 'elections' or subpage == 'all':
			##########################################################################################################
			# Extract the Elections Saskatchewan website

			self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

			# Create the CSV file
			csv_fn = "Webpages_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			# Get the soup of the page
			elections_url = self.pg_grp.get_url('elections_url')
			elections_soup = bsoup.get_soup(elections_url)
			
			if self.check_result(elections_soup, elections_url, 'Elections Saskatchewan'): 

				# Find the <h2>
				h2 = bsoup.find_tags_containing(elections_soup, 'Regina Northeast', 'h2')

				#print h2

				# Get the <h2> parent
				content_div = h2.parent

				# Now get all the <a> tags in the content_div
				anchors = content_div.find_all('a')

				# Go through each <a>
				for idx, a in enumerate(anchors):
					msg = "Extracting %s of %s sub-pages of Elections Saskatchewan website" % (idx + 1, len(anchors))
					shared.print_oneliner(msg)
				
					link = a['href']

					# If the link includes '.zip', it is a shapefile and not a pdf or link
					if link.find('.zip') > -1:
						# Get the title
						title_str = bsoup.get_text(a)

						# Get the description from the heading
						desc_str = bsoup.get_text(h2)
						#print title_str

						# Get the download link
						download_str = shared.get_anchor_url(a, elections_url)

						# Get the date
						date_str = ''
						match = re.search('\D{3} \d{4}', title_str)
						if match is not None:
							date_str = match.group(0)
						else:
							match = re.search('\D{4} \d{2}, \d{4}', title_str)
							if match is not None:
								date_str = match.group(0)

						# Add all values to the CSV file
						pt_csv.add('Source', 'Saskatchewan Web Pages')
						pt_csv.add('Title', title_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Type', 'Vector Data')
						pt_csv.add('Recent Date', date_str)
						pt_csv.add('Access', 'Download/Web Accessible')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', elections_url)
						pt_csv.add('Available Formats', 'SHP')
						pt_csv.add('Notes', self.notes)

						pt_csv.write_dataset()

				print
			
			pt_csv.close_csv()

		if subpage == 'regina' or subpage == 'all':

			###########################################################################
			# Extract from the Open Data site for Regina

			# Create or append the CSV file
			csv_fn = "Municipal_Webpages_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			regina_url = self.pg_grp.get_url('regina_url')

			# Get soup
			regina_soup = bsoup.get_soup(regina_url)
			categories = regina_soup.find_all('section', attrs={'class': 'tile-section'})

			map_formats = ['xml', 'shp', 'kml', 'json', 'rest']
			
			#print categories
			#answer = raw_input("Press enter...")

			print "Number of categories: " + str(len(categories))

			for idx, cat in enumerate(categories):
			
				# Get the URL for the category
				link = shared.get_link(cat)
				sub_url = urlparse.urljoin(regina_url, link)

				h3 = cat.find('h3', class_='tile-label')
				#print "Category: " + str(h3.text)
				
				print "Extracting datasets from '%s' group" % h3.text

				# Filter the formats
				#for format in map_formats:
				# Build the query
				# query_params = collections.OrderedDict()
				# query_params['res_format'] = format.upper()
				# final_url = shared.get_post_query(sub_url, query_params)

				# Load the sub result
				sub_soup = bsoup.get_soup(sub_url)

				# Find out the page count
				page_count = bsoup.get_page_count(sub_soup, 'div', ['class', 'pagination'], 'li')

				print "Page Count: " + str(page_count)
				
				form = sub_soup.find('form', id='group-datasets-search-form')
				ds_counter = bsoup.get_text(form.h2)
				ds_count = re.findall('\d+', ds_counter)
				
				counter = 0

				for page in range(0, page_count):
					# Load the current page
					if page > 0:
						page_url = "%s?page=%s" % (sub_url, page + 1)
						sub_soup = bsoup.get_soup(page_url)

					# Open the link
					results = sub_soup.find_all('h3', attrs={'class': 'dataset-heading'})
					for idx, res in enumerate(results):
						counter += 1
						msg = "Extracting %s of %s results from Regina's Open Data site" % (counter, ds_count[0])
						shared.print_oneliner(msg)

						res_link = shared.get_link(res)
						res_url = urlparse.urljoin(sub_url, res_link)

						res_soup = bsoup.get_soup(res_url)

						# Get the title
						div = res_soup.find('div', attrs={'class': 'module-content'})
						h1 = div.find('h1')
						title_str = bsoup.get_text(h1)

						# Get the description
						notes_div = div.find('div', attrs={'class': 'notes'})
						desc_str = bsoup.get_text(notes_div)

						# Get the available formats
						spans = div.find_all('span', attrs={'class': 'format-label'})
						# print spans
						formats = []
						for span in spans:
							format = span['data-format']
							if format == 'data':
								format = "REST"
							else:
								format = format.upper()
							formats.append(format)
						# print formats
						formats_str = '|'.join(formats)

						# Get the data url
						download_url = bsoup.get_adj_text_by_label(res_soup, 'th', "Source")

						if download_url == '':
							# Get the first dataset URL
							ds_ul = res_soup.find('ul', attrs={'class': 'resource-list'})
							ds_url = shared.get_anchor_url(ds_ul.a, res_url)

							# Get the dataset soup
							ds_soup = bsoup.get_soup(ds_url)

							# Get the page heading
							h1 = ds_soup.find('h1', attrs={'class': 'page-heading'})

							# Find the <p> sibling tag
							p = h1.find_next_sibling('p')

							# Get the download from the <a> under the <p>
							download_url = shared.get_anchor_url(p.a, ds_url)

						# Get the download and access string
						download_info = shared.get_download_text(formats, download_url)
						download_str, access_str = download_info.split('|')

						# Get the date
						date_str = bsoup.get_adj_text_by_label(res_soup, 'th', "Last Updated")

						# Add all values to the CSV file
						pt_csv.add('Source', 'Saskatchewan Web Pages')
						pt_csv.add('Title', title_str)
						pt_csv.add('Type', 'Vector Data')
						pt_csv.add('Recent Date', date_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Download', download_str)
						pt_csv.add('Available Formats', formats_str)
						pt_csv.add('Web Page URL', res_url)
						pt_csv.add('Notes', self.notes)

						pt_csv.write_dataset()

					print
			# Remove duplicate datasets in the CSV based on the Title field
			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

		if subpage == 'saskatoon' or subpage == 'all':
			######################################################################################
			# Extract from Saskatoon's Open Catalogue

			# Create or append the CSV file
			csv_fn = "Municipal_Webpages_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			browser_url = self.pg_grp.get_url('saskatoon_url')[0]
			xml_url = self.pg_grp.get_url('saskatoon_url')[1]

			xml_soup = bsoup.get_xml_soup(xml_url)

			colls = xml_soup.find_all('collection')

			# print collections
			for idx, coll in enumerate(colls):
			
				msg = "Extracting %s of %s results from Saskatoon's Open Catalogue site" % (idx + 1, len(colls))
				shared.print_oneliner(msg)

				############################################################################
				# Using the web page results

				# # Build query URL
				# base_url = "%s/%s" % (browser_url, coll['href'])
				#
				# # Get the Soup
				# coll_soup = bsoup.get_soup(base_url)
				#
				# title_str = bsoup.get_adj_text_by_label(coll_soup, 'td', "Dataset name")
				# desc_str = bsoup.get_adj_text_by_label(coll_soup, 'td', "Description")
				# date = bsoup.get_adj_text_by_label(coll_soup, 'td', "Last Updated Date")
				# ref_url = bsoup.get_adj_text_by_label(coll_soup, 'td', "Links and references")
				# mdata_url = bsoup.get_adj_text_by_label(coll_soup, 'td', "Metadata Url")
				#
				# # print title_str
				# # print shared.edit_description(desc_str)
				# # print date
				# # print "ref_url: %s" % ref_url
				# # print "mdata_url: %s" % mdata_url
				#
				# if ref_url == '': ref_url = base_url
				#
				# # Get the available formats
				# form_soup = coll_soup.find('select', attrs={'id': 'eidDownloadType'})
				# opts = form_soup.find_all('option')
				# formats = []
				# for opt in opts:
				#     formats.append(opt.string)
				#
				# formats_str = '|'.join(formats)
				#
				# # Get the download and access strings
				# download_info = shared.get_download_text(formats)
				# download_str, access_str = download_info.split('|')
				#
				# # Wednesday, April 04, 2018
				# date_obj = time.strptime(date, "%A, %B %d, %Y")
				# date_str = time.strftime("%Y-%m-%d", date_obj)

				############################################################################
				# Using the XML results

				ds_xml_url = "%s/%s" % (xml_url, coll['href'])

				ds_xml = bsoup.get_xml_soup(ds_xml_url)

				# Get the dataset's web page
				ds_url = ds_xml.find('id').text.replace('v1', 'DataBrowser')

				# Get the title
				title_str = ds_xml.find('title').text

				# Get the date
				date_str = ds_xml.find('updated').text

				# Open up the dataset's web page to get the rest of the info
				ds_soup = bsoup.get_soup(ds_url)

				# Get the description
				desc_str = bsoup.get_adj_text_by_label(ds_soup, 'td', "Description")

				mdata_url = bsoup.get_adj_text_by_label(ds_soup, 'td', "Metadata Url")

				# Get the available formats
				form_soup = ds_soup.find('select', attrs={'id': 'eidDownloadType'})
				opts = form_soup.find_all('option')
				formats = []
				for opt in opts:
					formats.append(opt.string)

				formats_str = '|'.join(formats)

				# Get the download and access strings
				download_info = shared.get_download_text(formats)
				download_str, access_str = download_info.split('|')

				# Add all values to the CSV file
				pt_csv.add('Source', 'Saskatchewan Web Pages')
				pt_csv.add('Title', title_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Recent Date', date_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Download', download_str)
				pt_csv.add('Available Formats', formats_str)
				pt_csv.add('Metadata URL', mdata_url)
				pt_csv.add('Web Page URL', ds_url)
				pt_csv.add('Notes', self.notes)

				pt_csv.write_dataset()

			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()

		if subpage == 'commview' or subpage == 'all':
			######################################################################################
			# Extract from the Community View catalogue

			self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

			# Create the CSV file
			csv_fn = "Organizations_Webpages_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv('a')

			# Get all the service URLs
			commview_url = self.pg_grp.get_url('commview_url')

			commview_soup = bsoup.get_soup(commview_url)

			# Get a list of all the anchors in the treeview at the side of the page
			ul = commview_soup.find('ul', attrs={'class': 'treeview'})
			anchors = ul.find_all('a', attrs={'class': 'TreeRootStandard'})

			for anchor in anchors:
				browse_url = shared.get_anchor_url(anchor, commview_url)

				# Load the sub result
				sub_soup = bsoup.get_soup(browse_url)

				# Determine the number of pages in the search
				page_count = bsoup.get_page_count(sub_soup, 'div', ['id', 'pager'], 'a')

				for page in range(0, page_count):

					# Load the current page
					if page > 0:
						page_url = "%s?page=%s" % (browse_url, page + 1)
						sub_soup = bsoup.get_soup(page_url)

					# Get the resource list
					resources_div = sub_soup.find('div', attrs={'class': 'ResourceList'})
					resources = resources_div.find_all('table', attrs={'class': 'ResourceTable'})

					for res in resources:
						msg = "Extracting %s of %s results from Saskatoon's Open Catalogue site" % (idx + 1, len(colls))
						shared.print_oneliner(msg)
					
						map_res = res.find('img', attrs={'alt': 'Map'})
						
						self.notes = "The XLS download does not include geospatial information."

						if map_res is not None:

							# Get the name of the resource
							title_str = res.find('a', attrs={'class': "ResourceTitle"}).text

							# Get the URLs for the data
							map_url = urlparse.urljoin(commview_url, map_res.parent['href'])
							data_url = map_url.replace("Map", "Data")
							def_url = map_url.replace('Map', 'Definition')
							details_url = map_url.replace('Map', 'Details')

							# Open the definition page to get the description
							def_soup = bsoup.get_soup(def_url)

							# Get the description by locating the <div> with id 'definitionDiv'
							desc_str = ''
							def_div = def_soup.find('div', attrs={'class', 'DefinitionDiv'})
							if def_div is not None:
								def_p = def_div.find('p')
								desc_str = bsoup.get_text(def_p)

							# To get the other information load the details page
							details_soup = bsoup.get_soup(details_url)

							# Get the date
							date_str = bsoup.get_adj_text_by_label(details_soup, 'td', 'Updated On')
							if date_str == '':
								date_str = bsoup.get_adj_text_by_label(details_soup, 'td', 'Created On')

							# Get the publisher
							pub_str = bsoup.get_adj_text_by_label(details_soup, 'td', 'Source')

							# Add all values to the CSV file
							pt_csv.add('Source', 'Saskatchewan Web Pages')
							pt_csv.add('Title', title_str)
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Recent Date', date_str)
							pt_csv.add('Publisher', pub_str)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Access', 'Download/Web Accessible')
							pt_csv.add('Download', data_url)
							pt_csv.add('Available Formats', 'XLS')
							pt_csv.add('Web Map URL', map_url)
							pt_csv.add('Web Page URL', def_url)
							pt_csv.add('Notes', self.notes)

							pt_csv.write_dataset()

			#pt_csv.remove_duplicates('Title')

			pt_csv.close_csv()
			
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Extracts all services in Saskatchewan, Saskatoon, Regina and Ducks Unlimited
		:return: None
		'''
		
		self.print_title("Extracting Saskatchewan's map services")
		
		# Get the parameter
		subpage = self.get_arg('subpage').get_urltags()[0]
		
		print "subpage: %s" % subpage
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file for the province
		csv_fn = "Services_results"
		prov_csv = sh.PT_CSV(csv_fn, self)
		prov_csv.open_csv()

		# Create or append the municipal CSV
		csv_fn = "Municipal_Services_results"
		munic_csv = sh.PT_CSV(csv_fn, self)
		munic_csv.open_csv()

		# Create or append the organization CSV
		csv_fn = "Organization_Services_results"
		org_csv = sh.PT_CSV(csv_fn, self)
		org_csv.open_csv()

		# Get all the service URLs
		serv_list = self.pg_grp.get_url_list()

		for serv_url in serv_list:
			if serv_url.find('Geocortex') > -1:
				if not subpage == 'geocortex' and not subpage == 'all':
					continue
				
				# Get a list of GeoCortex services
				geocortex = services.PT_Geocortex(serv_url)

				# Get the site and add it to the CSV file
				site_data = geocortex.get_layers()

				for index, rec in enumerate(site_data):
					shared.print_oneliner("Adding %s of %s to CSV inventory" \
										% (index + 1, len(site_data)))
					# Determine which CSV file to insert the service data
					serv_url = rec['Service URL']
					if serv_url.find('saskatoon') > -1 or serv_url.find('regina') > -1 or \
									serv_url.find('cosgis') > -1:
						pt_csv = munic_csv
					elif serv_url.find('ducks') > -1 or serv_url.find('wsask') > -1:
						pt_csv = org_csv
					else:
						pt_csv = prov_csv

					for k, v in rec.items():
						pt_csv.add(k, v)
					
					pt_csv.add('Source', "Saskatchewan Map Services")
					pt_csv.write_dataset()

			elif serv_url.find('flysask2') > -1:
				if not subpage == 'flysask' and not subpage == 'all': continue
				
				# Get the Geoportal Service's soup
				geoportal_soup = bsoup.get_xml_soup(serv_url)

				# Get the name of the service
				serv_title = geoportal_soup.find('Title')
				serv_title_str = bsoup.get_text(serv_title)

				# Get the description
				desc = geoportal_soup.find('Abstract')
				desc_str = bsoup.get_text(desc)

				# Get the service type
				serv_type = geoportal_soup.find('ServiceType')
				serv_str = bsoup.get_text(serv_type)

				# Get the publisher
				pub = geoportal_soup.find('ProviderName')
				pub_str = bsoup.get_text(pub)

				layers = geoportal_soup.find_all('Layer')

				for lyr in layers:
					# Get the name of the layer
					title = lyr.find('ows:Title')
					title_str = bsoup.get_text(title)

					# Get the projection
					sp = lyr.find('ows:BoundingBox')
					crs = sp['crs']
					crs_split = crs.split(':')
					epsg = crs_split[6]

					sp_str = shared.epsg_to_spatref(epsg)

					org_csv.add('Source', "Saskatchewan Map Services")
					org_csv.add('Title', title_str)
					org_csv.add('Description', desc_str)
					org_csv.add('Type', "Geocortex Essentials REST API")
					org_csv.add('Publisher', pub_str)
					org_csv.add('Web Service URL', serv_url)
					org_csv.add('Spatial Reference', sp_str)
					org_csv.add('Service Name', serv_title_str)
					org_csv.add('Service', serv_str)
					org_csv.add('Service URL', self.root_url)
					org_csv.add('Download', 'No')
			else:
				if not subpage == 'rest' and not subpage == 'saskatoon' \
					and not subpage == 'wsask' and not subpage == 'ducks' \
					and not subpage == 'all':
					continue
			
				# Get a list of REST services
				serv_rest = services.PT_REST(serv_url)

				# Get the service and add it to the CSV file
				serv_data = serv_rest.get_layers()
				
				if not self.check_result(serv_data, serv_url, 'ArcGIS REST Service'): continue
				
				filtered_rows = shared.process_duplicates(serv_data)
				
				for idx, rec in enumerate(filtered_rows):
					shared.print_oneliner("Adding %s of %s to CSV inventory" \
										% (idx + 1, len(filtered_rows)))
				
					# Determine which CSV file to insert the service data
					serv_url = rec['Service URL']
					if serv_url.find('saskatoon') > -1 or serv_url.find('cosgis') > -1:
						if not subpage == 'saskatoon' and not subpage == 'all':
							continue
							
						# If the service is for Saskatoon
						for k, v in rec.items():
							if k == "Title":
								v = "Saskatoon - %s" % v
							munic_csv.add(k, v)
						munic_csv.add('Source', "Saskatchewan Map Services")
						munic_csv.write_dataset()
					elif serv_url.find('regina') > -1:
						if not subpage == 'regina' and not subpage == 'all':
							continue
							
						# If the service is for Regina
						for k, v in rec.items():
							if k == "Title":
								v = "Regina - %s" % v
							munic_csv.add(k, v)
						munic_csv.add('Source', "Saskatchewan Map Services")
						munic_csv.write_dataset()
					elif serv_url.find('ducks') > -1:
						if not subpage == 'ducks' and not subpage == 'all':
							continue
						# If the service is for Ducks Unlimited
						for k, v in rec.items():
							# Filter out other provinces for Ducks Unlimited
							if k == 'Data URL' and \
									(v.find('/BC_') > -1 or v.find('/AB_') > -1 or v.find('/MB_') > -1 or
											 v.find('/NA_') > -1 or v.find('/ON_') > -1 or
											 v.find('/PR_') > -1 or v.find('/QC_') > -1 or
											 v.find('/NWA_') > -1):
								continue
							if k == 'Title':
								v = "Ducks Unlimited - %s" % v
							org_csv.add(k, v)
						org_csv.add('Source', "Saskatchewan Web Map Services")
						org_csv.write_dataset()
					elif serv_url.find('wsask') > -1:
						if not subpage == 'wsask' and not subpage == 'all':
							continue
							
						# If the service is for FlySask2
						for k, v in rec.items():
							if k == 'Title':
								v = "FlySask2 - %s" % v
							org_csv.add(k, v)
						org_csv.add('Source', "Saskatchewan Web Map Services")
						org_csv.write_dataset()
					else:
						if not subpage == 'rest' and not subpage == 'all':
							continue
							
						# If the service is for the province
						for k, v in rec.items():
							prov_csv.add(k, v)
						prov_csv.add('Source', "Saskatchewan Web Map Services")
						prov_csv.write_dataset()

		prov_csv.close_csv()
		munic_csv.close_csv()
		org_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

def main():
	# parser.add_argument("-t", "--tool", help="The tool to use: %s" % ', '.join(tool_list))
	# parser.add_argument("-w", "--word", help="The key word(s) to search for.")
	# parser.add_argument("-f", "--format", help="The format(s) to search for.")
	# parser.add_argument("-c", "--category", help="The category(ies) to search for.")
	# parser.add_argument("-d", "--downloadable", help="Determines wheter to get only downloadable datasets.")
	# parser.add_argument("-l", "--html", help="The HTML file to scrape (only for OpenData website).")
	# parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")

	ext = Extractor()

	try:
		pages = ext.get_pagelist()

		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--page", help="The page to extract: %s or all" % ', '.join(pages.keys()))
		parser.add_argument("-c", "--category", help="The category for the MLI sites.")
		parser.add_argument("-s", "--silent", action='store_true',
							help="If used, no extra parameters will be queried.")
		args = parser.parse_args()
		# print args.echo

		# print "province: " + str(args.province)
		# print "format: " + str(args.format)

		page = args.page
		params = collections.OrderedDict()
		params['cat'] = args.category
		silent = args.silent

		if page is None:
			answer = raw_input(
				"Please enter the page you would like to use (%s or all): " % ', '.join(pages.keys()))
			if not answer == "":
				page = answer.lower()
			else:
				print "\nERROR: Please specify a web page."
				print "Exiting process."
				sys.exit(1)

		page = page.lower()

		print page

		ext.set_page(page)
		ext.set_params(params)
		ext.run()

	except Exception, err:
		ext.print_log('ERROR: %s\n' % str(err))
		ext.print_log(traceback.format_exc())
		ext.close_log()

if __name__ == '__main__':
	sys.exit(main())

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
from common import services
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		# Set the province
		self.province = 'Yukon'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Geoportal page group

		geo_grp = main_ext.PageGroup('geoportal', 'GeoYukon Geoportal')
		
		# Add arguments
		geo_grp.add_arg('word', title='Search Word')
		
		# Add URLs
		geo_grp.add_url('main_url', 'http://geoweb.gov.yk.ca/geoportal/catalog/main/home.page')
		geo_grp.add_url('query_url', 'http://geoweb.gov.yk.ca/geoportal/rest/find/document')
		
		# Add to Extractor's page group list
		self.page_groups.append(geo_grp)
		
		
		####################################################################
		# Create Services page group

		srv_grp = main_ext.PageGroup('services', 'Yukon Map Services')
		
		# Add URLs
		srv_grp.add_url('rest_url', 'http://mapservices.gov.yk.ca/ArcGIS/rest/services')
		srv_grp.add_url('geocortex_url', 'http://mapservices.gov.yk.ca/Geocortex/Essentials/REST/sites')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create Interactive Maps page group

		map_grp = main_ext.PageGroup('maps', 'Yukon Interactive Maps')
		
		# Add URLs
		map_grp.add_url('gallery_urls',
				   ['http://yukon.maps.arcgis.com/home/gallery.html?view=' \
					'grid&sortOrder=asc&sortField=title',
					'http://yukon2.maps.arcgis.com/home/gallery.html?view=' \
					'grid&sortOrder=desc&sortField=numviews',
					'http://yukon4.maps.arcgis.com/home/gallery.html?view=' \
					'grid&sortOrder=asc&sortField=title'])
		#map_grp.add_url('warehouse_url', ['http://yukon.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title', 
		#									'https://yukon.maps.arcgis.com/sharing/rest/search'])
		map_grp.add_url('other_urls',
				   [('http://deptweb.gov.yk.ca/YGS/Applications/PublicationBrowser',
					'http://www.arcgis.com/sharing/rest/content/items/c1f89c570b894b7790a9a885ab685291?f=pjson'),
					('http://www.geology.gov.yk.ca',
					 'https://yukon2.maps.arcgis.com/sharing/rest/content/items/48e3f508fda64dfc95c6dd0e6f821ff0?f=pjson'),
					'http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=02ad68fcb38b40149b5a313c9cbb54bc',
					'http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=5113d22270e2400581c0065d6fedfb55',
					'https://yukon2.maps.arcgis.com/apps/MapTour/index.html?appid=f9a2ada0189f4143ac64e2bc0c9111d7',
					'http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=0fa83ba4a4794b9d8432d4d1b44da967',
					'http://yukon2.maps.arcgis.com/apps/Viewer/index.html?appid=ce7893e2b1bf43a582da48fd1165f4df',
					'http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=470f246f9b0f4987ab2e590df6dd94c4',
					'http://yukon4.maps.arcgis.com/apps/webappviewer/index.html?id=fde154c2332248899bee6875b314078b',
					'http://yukon4.maps.arcgis.com/apps/webappviewer/index.html?id=2afcf62ef63b46b6bc38b38a5828c628'])
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		
		
		####################################################################
		# Create FTP page group

		ftp_grp = main_ext.PageGroup('ftp', 'Yukon Geomatics FTP')
		
		# Add URLs
		ftp_grp.add_url('ftp_url', 'ftp.geomaticsyukon.ca')
		
		# Add to Extractor's page group list
		self.page_groups.append(ftp_grp)
		
		
		####################################################################
		# Create ArcGIS Hub page group

		hub_grp = main_ext.PageGroup('hub', 'ArcGIS Hub')
		
		# Add URLs
		hub_grp.add_url('hub_url', 'https://hub.arcgis.com/datasets?source=Yukon%20Government')
		hub_grp.add_url('open_url', 'https://opendata.arcgis.com/api/v2/datasets')
		
		# Add to Extractor's page group list
		self.page_groups.append(hub_grp)
		
		
		####################################################################
		# Create CSW page group

		csw_grp = main_ext.PageGroup('csw', 'Yukon Government Corporate Spatial Warehouse Gallery')
		
		# Add URLs
		csw_grp.add_url('main_url',
					'http://yukon.maps.arcgis.com/home/group.html?id=099cc2a078c1432390cdbc90fe114179&start=1&view=list#content')
		#csw_grp.add_url('main_url', 'http://yukon.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title')
		csw_grp.add_url('query_url', 'https://yukon.maps.arcgis.com/sharing/rest/search')
		
		# Add to Extractor's page group list
		self.page_groups.append(csw_grp)
		
		
		####################################################################
		# Create Geological Survey page group

		gs_grp = main_ext.PageGroup('ygs', 'Yukon Geological Survey')
		
		# Add URLs
		gs_grp.add_url('dbgis_url', 'http://www.geology.gov.yk.ca/databases_gis.html')
		gs_grp.add_url('geochem_url', 'http://www.geology.gov.yk.ca/geochemistry.html')
		gs_grp.add_url('commap_url', 'http://www.geology.gov.yk.ca/community_mapping.html')
		gs_grp.add_url('steves_url', 'http://www.geology.gov.yk.ca/stevenson_ridge.html')
		
		# Add to Extractor's page group list
		self.page_groups.append(gs_grp)
		
		
		####################################################################
		# Create EMR page group

		emr_grp = main_ext.PageGroup('emr', 'Yukon Energy, Mines & Resources Web Pages')
		
		# Add URLs
		emr_grp.add_url('rights_url', 'http://www.emr.gov.yk.ca/oilandgas/rights_management_maps_data.html')
		emr_grp.add_url('gisdata_url', 'http://www.env.gov.yk.ca/publications-maps/geomatics/data.php')
		emr_grp.add_url('wildlife_url', 'http://www.env.gov.yk.ca/publications-maps/wka_gis_data.php')
		
		# Add to Extractor's page group list
		self.page_groups.append(emr_grp)
		
		
		####################################################################
		# Create Land Use Planning Council page group

		plan_grp = main_ext.PageGroup('landuse', 'Yukon Land Use Planning Council')
		
		# Add URLs
		plan_grp.add_url('spat_url', 'http://www.planyukon.ca/index.php/documents-and-downloads/spatial')
		
		# Add to Extractor's page group list
		self.page_groups.append(plan_grp)


	###################################################################################################################

	def extract_csw(self):
		''' Extracts the Yukon Government Corporate Spatial Warehouse Gallery
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Yukon Government Corporate Spatial Warehouse Gallery")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		query_url = self.pg_grp.get_url('query_url')

		self.print_log("URL: %s" % query_url)

		# Create the CSV file
		csv_fn = "CSW_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		record = 0

		for i in range(0, 5):
			
			# Set up the query string URL
			# num=100&start=0&sortField=title&sortOrder=asc&q=group%3A("099cc2a078c1432390cdbc90fe114179")-type%3A"Code%20Attachment"&f=json
			params = collections.OrderedDict()
			params['num'] = '100'
			start = i * 100 + 1
			if start == 1:
				start = 0
			else:
				start = start
			params['start'] = str(start)
			params['sortField'] = 'title'
			params['sortOrder'] = 'asc'
			params['q'] = 'group%3A("099cc2a078c1432390cdbc90fe114179")-type%3A"Code%20Attachment"'
			params['f'] = 'json'
			full_query_url = shared.get_post_query(query_url, params)

			#print full_query_url
			
			#answer = raw_input("Press enter...")

			# Create the BeautifulSoup object
			csw_json = shared.get_json(full_query_url)
			
			if not self.check_result(csw_json, full_query_url,	
				'Yukon Government Corporate Spatial Warehouse Gallery'): continue

			results = csw_json['results']

			for res in results:
				record += 1
				msg = "Extracting %s of less than 500 results from '%s'" % (record, full_query_url)
				shared.print_oneliner(msg)
			
				date = res['modified']
				date = shared.translate_date(date)
				title = res['title']
				res_type = res['type']
				desc = res['description']
				desc_soup = BeautifulSoup(desc, 'html.parser')
				desc_str = bsoup.get_text(desc_soup)
				url = res['url']

				pt_csv.add('Date', date)
				pt_csv.add('Title', title)
				pt_csv.add('Type', res_type)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Service URL', url)
				pt_csv.add('Download', 'No')
				pt_csv.add('Access', 'Viewable/Contact the Territory')

				pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_emr(self):
		''' Extract the Yukon Energy, Mines & Resources web pages.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Yukon Energy, Mines & Resources web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "EMR_ENV_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		###########################################################################
		# Extract the Rights Management Maps and Data page

		# Get the Rights url
		rights_url = self.pg_grp.get_url('rights_url')
		rights_soup = bsoup.get_soup(rights_url)
		
		if self.check_result(rights_soup, rights_url, 
			'Rights Management Maps and Data Page'):
			self.print_log("URL: %s" % rights_url)

			tables = rights_soup.find_all('tbody')

			for idx, table in enumerate(tables):
				msg = "Extracting %s of %s datasets of the Rights Management Maps and Data page" % (idx + 1, len(tables))
				shared.print_oneliner(msg)

				headers = ['Title', 'Datum', 'Projection']
				table_list = shared.table_to_dict(table, header=headers, start_row=1)

				table_dict = table_list[0]

				title = table_dict['Title']
				title_str = title.text
				a = title.find('a')
				download = a['href']
				sp = "%s %s" % (table_dict['Projection'].text, table_dict['Datum'].text)

				#start_pos = title_str.find('ESRI')
				#format_str = title_str[start_pos:]
				if title_str.find('ESRI Shapefile') > -1:
					format = 'SHP'
				else:
					format = 'FGDB'

				#print "Title:"
				#print title_str
				#print "Download: " + str(download)
				#print "Spatial Reference: " + str(sp)

				pt_csv.add('Title', title_str)
				pt_csv.add('Available Formats', format)
				pt_csv.add('Type', 'ESRI File')
				pt_csv.add('Download', download)
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Spatial Reference', sp)
				pt_csv.add('Web Page URL', rights_url)

				pt_csv.write_dataset()

		###########################################################################
		# Extract the GIS Data Overview page

		gisdata_url = self.pg_grp.get_url('gisdata_url')
		gisdata_soup = bsoup.get_soup(gisdata_url)
		
		if self.check_result(gisdata_soup, rights_url, 'GIS Data Overview Page'):
			# Check to see if the FTP link works
			ftp_site = shared.get_ftp('ftp.geomaticsyukon.ca')
			#print ftp_site

			ul = gisdata_soup.find('ul', attrs={'class': 'NavL3'})
			li_list = ul.find_all('li')
			
			li_count = len(li_list)
			
			ds_count = 0

			for idx, li in enumerate(li_list):
			
				sub_url = urlparse.urljoin(gisdata_url, li.a['href'])
				sub_soup = bsoup.get_soup(sub_url)

				a_list = sub_soup.find_all('a')
				
				a_count = len(a_list)

				for a_idx, a in enumerate(a_list):
					if a.has_attr('href'):
						msg = "Extracting %s of %s datasets from sub-page " \
							"'%s' of GIS Data Overview page" % (a_idx + 1, a_count, gisdata_url)
						shared.print_oneliner(msg)
						
						download = a['href']
						#print link
						if download.find('ftp.') > -1:
							# Get the 'a' parent
							p = a.parent
							#print "p: " + str(p)
							h3 = p.find_previous_sibling('h3')
							if h3 is None: continue
							title = h3.text
							desc = h3.find_next_sibling('p')
							desc_str = desc.text
							#desc_str = shared.edit_description(desc_str)

							#print "Title: " + str(title)
							#print "Description: " + str(desc_str)

							formats = ''
							notes_str = ''
							# Check the FTP to see if it exists
							ftp_files = shared.ftp_files(ftp_site, download)
							if ftp_files is None:
								notes_str = 'The download link to the FTP site is broken.'
							else:
								try:
									formats_list = [f.split('.')[1].upper() for f in ftp_files]
									formats = '|'.join(formats_list)
								except:
									formats = 'FGDB|SHP|KMZ'

							pt_csv.add('Title', title)
							pt_csv.add('Available Formats', formats)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Type', 'ESRI File')
							pt_csv.add('Download', download)
							pt_csv.add('Access', 'Download/Accessible Web')
							pt_csv.add('Spatial Reference', '(ESPG: 3578) Yukon Albers Projection')
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Notes', notes_str)

							pt_csv.write_dataset()

				print
		###########################################################################
		# Extract the Wildlife Key Area GIS Data Packages page

		wildlife_url = self.pg_grp.get_url('wildlife_url')
		wildlife_soup = bsoup.get_soup(wildlife_url)
		
		if self.check_result(wildlife_soup, wildlife_url, 
			'Wildlife Key Area GIS Data Packages'):
			body_div = wildlife_soup.find('div', attrs={'id': 'bodyContent'})

			# Get the title
			h2 = body_div.find('h2')
			title = h2.text

			# Get the description
			p_list = body_div.find_all('p')
			desc = p_list[2].text

			pt_csv.add('Title', title)
			pt_csv.add('Available Formats', 'FGDB|SHP')
			pt_csv.add('Type', 'ESRI File')
			pt_csv.add('Download', 'Multiple Downloads')
			#pt_csv.add('Description', desc)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Spatial Reference', '(ESPG: 3578) Yukon Albers Projection')
			pt_csv.add('Web Page URL', wildlife_url)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_ftp(self):
		''' Extract the datasets on Yukon's Geomatics FTP.
		:return: None
		'''
		
		self.print_title("Extracting Yukon's Geomatics FTP site")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		ftp_domain = self.pg_grp.get_url('ftp_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "FTP_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		dir_list = []
		dir_list.append('/Elevation/')
		dir_list.append('/GeoYukon/')
		dir_list.append('/Imagery/')

		ftp_files = []
		header = ['permissions', 'links', 'owner', 'group', 'filesize', 'month', 'day', 'time', 'filename']
		for dir in dir_list:
			# Get the FTP object for the current folder
			ftp = rec_ftp.RecFTP(ftp_domain, dir, header, self.debug)

			# Get a list of files under the current folder
			ftp_list = ftp.get_file_list()

			# Add the files to the overall ftp_files list
			ftp_files += ftp_list

		for f in ftp_files:
			
			if not self.check_result(f, ftp_domain, 
				'Yukon FTP'): continue

			folder = os.path.dirname(f)
			basename = os.path.basename(f)
			if basename.find('.') == -1: continue
			title_str = basename.split('.')[0]
			ext = basename.split('.')[1]

			pt_csv.add('Title', title_str)
			# pt_csv.add('Type', ds_type)
			pt_csv.add('Download', f)
			pt_csv.add('Data URL', folder)
			pt_csv.add('Access', 'Download/Accessible FTP')
			pt_csv.add('Available Formats', ext.upper())

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_geoportal(self): #, word=None):
		''' Extract the GeoYukon Geoportal
		:return: None
		'''
		
		# Get the parameters
		word = self.get_arg_val('word')

		# ###########################################################################
		# Extract the GeoYukon Geoportal
		###########################################################################

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting GeoYukon Geoportal")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the CCR url
		main_url = self.pg_grp.get_url('main_url')
		query_url = self.pg_grp.get_url('query_url')

		self.print_log("URL: %s" % main_url)

		# Create the CSV file
		csv_fn = "GeoPortal_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Build the search URL and search the portal
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['searchText'] = word
		params['max'] = '5000'
		params['f'] = 'json'
		full_query = shared.get_post_query(query_url, params)

		json_results = shared.get_json(full_query)
		
		if not self.check_result(json_results, full_query, 
			'GeoYukon Geoportal'): return None

		# Get the query from the JSON
		#source = json_results['source']

		# Get a list of the results
		records = json_results['records']

		# Start FTP
		ftp = shared.get_ftp('ftp.geomaticsyukon.ca')

		rec_total = len(records)

		print "Number of results: " + str(rec_total)

		record_count = 0

		for idx, rec in enumerate(records):
		
			msg = "Extracting %s of %s records" % (idx + 1, len(records))
			shared.print_oneliner(msg)

			mdata_url = None
			mdata_xml_url = ''
			links_list = rec['links']
			for link in links_list:
				if link['type'] == 'metadata' or link['type'] == "fullMetadata":
					mdata_xml_url = link['href']

			# Load the metadata XML
			if mdata_xml_url is not None:
				mdata_xml = bsoup.get_xml_soup(mdata_xml_url, True)
				
				if not self.check_result(mdata_xml, mdata_xml_url, 'GeoYukon Geoportal'): continue

				# Build the metadata URL for the HTML page
				id = mdata_xml_url.split("=")[1]
				mdata_url = 'http://geoweb.gov.yk.ca/geoportal/catalog/search/resource/details.page?uuid=%s' % id

				# Get the title
				title = mdata_xml.find('title').text
				title_str = shared.clean_text(title)

				# Get the description
				desc_str = mdata_xml.find('abstract').text
				#desc_str = desc

				# Get the type
				format = mdata_xml.find('distributionFormat')
				ds_type = format.find('name').text
				ds_type = shared.clean_text(ds_type)

				# Get the date
				date_el = mdata_xml.find('CI_Date')
				date = date_el.find('date').text
				date_str = shared.clean_text(date)

				# Get the web map viewer URL
				data_url = None
				map_viewer_url = ''
				webmap_url = ''
				download_link = None
				links = mdata_xml.find_all('linkage')
				link_list = [shared.clean_text(l.text) for l in links]
				for link in link_list:
					if link.find('map') > -1:
						webmap_url = link
					else:
						download_link = link

				if download_link is None:
					download_str = 'No'
					access_str = 'Contact the Territory'
				else:
					download_str = download_link
					access_str = 'Download/Accessible Web'

				# Using the FTP link, determine the available formats
				formats = ''
				if download_link is not None:
					if download_link.find('ftp') > -1:
						ftp_files = shared.ftp_files(ftp, download_link)
						if ftp_files is None:
							self.notes = 'The download link to the FTP site is broken.'
						else:
							if not self.check_result(ftp_files, download_link, txt='The download link to the FTP site is broken.'):
								self.notes = 'The download link to the FTP site is broken.'
							else:
								#print ftp_files
								formats_list = [f.split('.')[1].upper() for f in ftp_files]
								formats = '|'.join(formats_list)
				else:
					dist_form = mdata_xml.find('distributorFormat')
					if dist_form is not None:
						formats = dist_form.find('name').text

				# Get the spatial reference
				sp = mdata_xml.find('referenceSystemIdentifier')
				code = sp.find('code').text
				code = shared.clean_text(code)
				if code == '0' or code == 0:
					sp_str = ''
				else:
					sp_str = "EPSG %s" % code
				# Query URL
				#pt_csv.add('Query URL'] = full_query
				# Get the metadata ISO
				mdata_iso = mdata_xml.find('metadataStandardName').text

				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Type', ds_type)
				pt_csv.add('Date', date_str)
				pt_csv.add('Metadata URL', mdata_url)
				pt_csv.add('Metadata Type', shared.clean_text(mdata_iso))
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Download', download_str)
				pt_csv.add('Web Map URL', webmap_url)
				pt_csv.add('Access', access_str)
				pt_csv.add('Available Formats', formats)
				pt_csv.add('Notes', self.notes)

				pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_hub(self):
		''' Extracts the ArcGIS Hub of the Yukon.
		:return: None
		'''
		
		self.print_title("Extracting ArcGIS Hub of the Yukon")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		hub_url = self.pg_grp.get_url('hub_url')
		open_url = self.pg_grp.get_url('open_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "ArcGIS_Hub_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Query Example:
		# 'https://opendata.arcgis.com/api/v2/datasets?filter[source]=Yukon%20Government
		#   &filter[content]=any(web%20map,spatial%20dataset,table,raster%20dataset)
		#   &include=sites,organizations,groups
		#   &page[number]=1
		#   &page[size]=300'

		params = collections.OrderedDict()
		params['filter[source]'] = 'Yukon Government'
		params['filter[content]'] = 'any(web map,spatial dataset,table,raster dataset)'
		params['include'] = 'sites,organizations,groups'
		params['page[number]'] = '1'
		params['page[size]'] = '310'
		query_url = shared.get_post_query(open_url, params)

		#attr_name = attrb[1]
		#el_type = attrb[0]
		#attrb = ('class', 'pagination')
		hub_json = shared.get_json(query_url)
		
		if not self.check_result(hub_json, query_url, 'ArcGIS Hub'): return None

		data_list = hub_json['data']

		for idx, data in enumerate(data_list):
		
			msg = "Extracting %s of %s records" % (idx + 1, len(data_list))
			shared.print_oneliner(msg)

			attrs = data['attributes']
			title = attrs['name']

			desc = attrs['description']
			desc_soup = BeautifulSoup(desc, 'html.parser')
			desc_str = bsoup.get_text(desc_soup)

			data_type = attrs['dataType']
			date = attrs['updatedAt']

			sp = shared.get_spatialref(data, 'serviceSpatialReference')

			web_page_url = attrs['landingPage']
			web_service_url = attrs['url']

			#print "Title:"
			#print title
			#print "Description:"
			#print desc_str
			#print "Data Type: " + str(data_type)
			#print "Date: " + str(date)
			#print "Spatial Reference: " + str(sp)

			pt_csv.add('Title', title)
			#pt_csv.add('Available Formats', 'FGDB|SHP')
			pt_csv.add('Type', data_type)
			pt_csv.add('Date', date)
			pt_csv.add('Download', 'Multiple Downloads')
			pt_csv.add('Description', desc_str)
			pt_csv.add('Access', 'Viewable/Contact the Territory')
			pt_csv.add('Spatial Reference', sp)
			pt_csv.add('Web Page URL', web_page_url)
			pt_csv.add('Service URL', web_service_url)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_landuse(self):
		''' Extract the Yukon Land Use Planning Council page.
		:return: None
		'''
		
		self.print_title("Extracting Yukon Land Use Planning Council page")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		spat_url = self.pg_grp.get_url('spat_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "LandUsePlan_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		landuse_soup = bsoup.get_soup(spat_url)
		
		if not self.check_result(landuse_soup, spat_url, 
			'Yukon Land Use Planning Council'): return None

		results = landuse_soup.find_all('div', attrs={'class': 'docman_document'})

		for idx, res in enumerate(results):
		
			msg = "Extracting %s of %s results" % (idx + 1, len(results))
			shared.print_oneliner(msg)

			title_span = res.find('span', attrs={'itemprop': 'name'})
			title = title_span.text
			if title.find('Presentation') > -1: continue
			parent_a = title_span.parent
			link = urlparse.urljoin(spat_url, parent_a['href'])

			sub_soup = bsoup.get_soup(link)
			time = sub_soup.find('time')
			date = time['datetime']

			# Get the description
			desc_div = sub_soup.find('div', attrs={'itemprop': 'description'})
			desc_str = bsoup.get_text(desc_div)

			# Get the download link
			a_download = sub_soup.find('a', attrs={'class': 'docman_download__button'})
			download_link = urlparse.urljoin(link, a_download['href'])

			# Create available formats:
			if title.find('kml') > -1:
				format = 'KML'
			elif title.find('kmz') > -1:
				format = 'KMZ'
			else:
				format = 'SHP'

			#print "Title:"
			#print title
			#print "Link: " + str(link)
			#print "Date: " + str(date)
			#print "Description: " + str(desc_str)
			#print "Download Link: " + str(download_link)

			pt_csv.add('Title', title)
			pt_csv.add('Available Formats', format)
			pt_csv.add('Type', 'Vector File')
			pt_csv.add('Date', date)
			pt_csv.add('Download', download_link)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Access', 'Download/Accessible Web')
			#pt_csv.add('Spatial Reference', sp)
			pt_csv.add('Web Page URL', link)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		''' Extracts the interactive maps of the Yukon
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Yukon's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Maps CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		##################################################################################
		# Get the maps from the galleries

		# Get the URL list
		gallery_urls = self.pg_grp.get_url('gallery_urls')

		for url in gallery_urls:
		
			gallery_maps = shared.get_arcgis_gallery(url)
			
			for map in gallery_maps:
				for k, v in map.items():
					pt_csv.add(k, v)
					
				pt_csv.write_dataset()

			# gallery_soup = bsoup.get_soup(url, True)

			# gallery_div = gallery_soup.find('div', attrs={'class': 'gallery-card-wrap'})

			# # Get the <div> with class "card" to get each interactive map
			# map_anchors = gallery_div.find_all('a', attrs={'class': 'card-image-wrap'})

			# # print len(map_anchors)

			# for card in map_anchors:
				# map_url = shared.get_anchor_url(card, url)

				# #print "Map URL: %s" % map_url

				# # Get the ArcGIS data
				# arcgis_info = shared.get_arcgis_data(map_url)

				# if arcgis_info is None: continue

				# # Add the ArcGIS data to the CSV
				# for k, v in arcgis_info.items():
					# pt_csv.add(k, v)

				# # Add all values to the CSV file
				# pt_csv.add('Access', 'Viewable/Map Service')
				# pt_csv.add('Download', 'No')
				# pt_csv.add('Web Map URL', map_url)

				# pt_csv.write_dataset()

		##################################################################################
		# Get the rest of the maps

		other_urls = self.pg_grp.get_url('other_urls')

		for idx, url in enumerate(other_urls):
			msg = "Extracting %s of %s ArcGIS maps" % (idx + 1, len(other_urls))
			shared.print_oneliner(msg)
		
			map_url = ''
			
			if isinstance(url, tuple):
				map_url = url[0]
				url = url[1]

			# Get the ArcGIS data
			arcgis_info = shared.get_arcgis_data(url)

			if not self.check_result(arcgis_info, url, 'ArcGIS Map'): continue

			# Add the ArcGIS data to the CSV
			for k, v in arcgis_info.items():
				pt_csv.add(k, v)

			# Add all values to the CSV file
			pt_csv.add('Access', 'Viewable/Map Service')
			pt_csv.add('Download', 'No')
			if not map_url == '': pt_csv.add('Web Map URL', map_url)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Extract the map services of the Yukon.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Yukon's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file for the territory
		csv_fn = "Services_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		url_list = self.pg_grp.get_url_list()

		for url in url_list:
			if url.find('Geocortex') > -1:
				# Get a list of GeoCortex services
				geocortex = services.PT_Geocortex(url)

				# Get the site and add it to the CSV file
				site_data = geocortex.get_layers()
				
				if not self.check_result(site_data, url, 
					'Geocortex Service'): continue

				for index, rec in enumerate(site_data):
					shared.print_oneliner("Adding %s of %s to CSV inventory" \
											% (index + 1, len(site_data)))
					# Determine which CSV file to insert the service data
					for k, v in rec.items():
						pt_csv.add(k, v)
					
					pt_csv.add('Source', 'Yukon Map Services')
					pt_csv.write_dataset()
			else:
				# Get a list of REST services
				my_rest = services.PT_REST(url)

				# Get the service and add it to the CSV file
				lyr_info = my_rest.get_layers()
				
				if not self.check_result(lyr_info, url, 'ArcGIS REST Map'): continue
				
				filter_rows = shared.process_duplicates(lyr_info)
				
				#print "\nAdding data from ArcGIS REST service for '%s' to CSV inventory..." % url
				for index, rec in enumerate(filter_rows):
					shared.print_oneliner("Adding %s of %s to CSV inventory" \
											% (index + 1, len(filter_rows)))
					for k, v in rec.items():
						pt_csv.add(k, v)
					
					pt_csv.add('Source', 'Yukon Map Services')
					pt_csv.write_dataset()
				
				print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_ygs(self):
		''' Extact the Yukon Geological Survey pages.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting the Yukon Geological Survey page")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "YGSLinks_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# pg.add_page('dbgis_url', 'http://www.geology.gov.yk.ca/databases_gis.html')
		# pg.add_page('geochem_url', 'http://www.geology.gov.yk.ca/geochemistry.html')
		# pg.add_page('commap_url', 'http://www.geology.gov.yk.ca/community_mapping.html')
		# pg.add_page('steves_url', 'http://www.geology.gov.yk.ca/stevenson_ridge.html')

		############################################################################################
		# Start with the DB & GIS page

		dbgis_url = self.pg_grp.get_url('dbgis_url')
		dbgis_soup = bsoup.get_soup(dbgis_url)
		
		if self.check_result(dbgis_soup, dbgis_url, 'DB & GIS page'):
			tables = dbgis_soup.find_all('tbody')

			mdata_url = 'http://www.geology.gov.yk.ca/metadata.html'

			# Start with the first table
			table = tables[0]
			#headers = ['Theme', 'Description', 'Format']
			table_dict = shared.table_to_dict(table, start_row=1) #header=headers, start_row=1) #col_elem='th', start_row=1)
			
			#print table_dict

			for idx, row in enumerate(table_dict):
				msg = "Extracting %s of %s pages" % (idx + 1, len(table_dict))
				shared.print_oneliner(msg)
			
				if row['theme'].text == 'Geochem':

					link = row['format'].a['href']

					if link.find('zip') > -1:
						title = row['theme'].text
						desc_str = row['description'].text
						date = ''
						formats = ['Excel', 'SHP', 'PDF']
						download = 'Multiple Downloads'
					else:
						# Open the link
						link_soup = bsoup.get_soup(link, True, delay=10)

						# Get the title
						lyr_div = link_soup.find('div', text='Layer Name')
						title = lyr_div.find_next_sibling('div').text

						#pattern = re.compile(r'Geology')
						strong = link_soup.find('strong', text='Release Date: ')
						date = strong.parent.text.replace('Release Date: ', '')

						h3 = link_soup.find('h3', text='Abstract')
						desc_str = h3.parent.find_next_sibling('div').text
						formats = ['FGDB', 'SHP']
						download = 'Multiple Downloads'

					# ['Title', 'Type', 'Download', 'Access', 'Available Formats', 'Description']

					pt_csv.add('Title', title)
					pt_csv.add('Description', desc_str)
					pt_csv.add('Available Formats', '|'.join(formats))
					pt_csv.add('Date', date)
					pt_csv.add('Type', 'Vector File')
					pt_csv.add('Download', download)
					pt_csv.add('Access', 'Download/Accessible Web')
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Web Page URL', dbgis_url)

					pt_csv.write_dataset()

			# Second table
			table = tables[1]
			headers = ['Theme', 'Description', 'Format']
			table_dict = shared.table_to_dict(table, header=headers, start_row=1) #col_elem='th', start_row=1)

			for idx, row in enumerate(table_dict):
				msg = "Extracting %s of %s pages" % (idx + 1, len(table_dict))
				shared.print_oneliner(msg)

				if not type(row['Format']) == 'str':
					if row['Format'].text.find('Excel Spreadsheet') == -1:
						if row['Format'].text == 'Online':
							formats = ['FGDB', 'SHP', 'KMZ']
							download = 'Multiple Downloads'
						elif row['Format'].text.find('File Geodatabase') > -1:
							formats = ['FGDB', 'SHP']
							download = 'Multiple Downloads'
						else:
							formats = ['SHP']
							download = row['Format'].a['href']

						title = row['Theme'].text
						desc_str = row['Description'].text

						#print "\n"
						#print "Title: '%s'" % title
						if title.strip() == 'Bedrock Geology':
							mdata_title = 'Bedrock Contacts and Faults'
						elif title.strip() == 'Mineral Occurrences':
							mdata_title = 'Mineral Occurrences'
						elif title.strip() == 'Regional Stream Geochemistry (2003)':
							mdata_title = 'Regional Stream Geochemistry'
						elif title.strip() == 'Yukon Folds':
							mdata_title = 'Regional Scale Data'
						else:
							mdata_title = title.strip()

						pt_csv.add('Title', title)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Available Formats', '|'.join(formats))
						pt_csv.add('Type', 'Vector File')
						pt_csv.add('Download', download)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Access', 'Download/Accessible Web')
						pt_csv.add('Web Page URL', dbgis_url)

						pt_csv.write_dataset()
					
		############################################################################################
		# Till Geochemistry/Heavy Minerals
		
		geochem_url = self.pg_grp.get_url('geochem_url')
		geochem_soup = bsoup.get_soup(geochem_url)
		
		if self.check_result(geochem_soup, geochem_url, 'Till Geochemistry/Heavy Minerals'):
			# Get a list of the <hr>
			hr_list = geochem_soup.find_all('hr')
			
			#full_div = geochem_soup.find('div', attrs={'id', 'full'})
			a_list = geochem_soup.find_all('a')
			
			#print "Number of <a>'s: %s" % len(a_list)
			
			for idx, a in enumerate(a_list):
				msg = "Extracting %s of %s pages" % (idx + 1, len(a_list))
				shared.print_oneliner(msg)
			
				if a.has_attr('name'):
					# Get the text of the a
					a_text = bsoup.get_text(a)
					
					if not a_text == "":
						
						# Get the title
						title_str = bsoup.get_text(a)
						
						# Get the description by getting the parent, get the next siblings <p> elements
						#	and then get the second <p>
						strong = a.parent
						p_list = strong.find_next_siblings('p')
						desc_p = p_list[1]
						desc_str = bsoup.get_text(desc_p)
						
						for p in p_list:
							anchor = p.a
							if anchor is not None and anchor.has_attr('href') and anchor['href'].find('.zip') > -1:
								
								# Get the download URL if the <a> is not None, has 'href' attribute and contains '.zip'
								#	in the URL
								download_url = shared.get_anchor_url(anchor, geochem_url)
								
								if self.debug:
									print 
									print "\nTitle: %s" % title_str
									print "Description: %s" % desc_str
									print "Download: %s" % download_url
								
								pt_csv.add('Title', title)
								pt_csv.add('Description', desc_str)
								pt_csv.add('Available Formats', 'MDB')
								pt_csv.add('Download', download_url)
								pt_csv.add('Access', 'Download/Accessible Web')
								pt_csv.add('Web Page URL', geochem_url)

								pt_csv.write_dataset()
		
		#answer = raw_input("Press enter...")

		############################################################################################
		# Community Mapping

		commap_url = self.pg_grp.get_url('commap_url')
		commap_soup = bsoup.get_soup(commap_url)
		
		if self.check_result(commap_soup, commap_url, 'Community Mapping'):
			strong = commap_soup.find('strong', text='Surficial Geology GIS Data:')
			p = strong.parent

			ul = p.find_next_sibling('ul')

			#print ul

			a_list = ul.find_all('a')

			for idx, a in enumerate(a_list):
				msg = "Extracting %s of %s pages" % (idx + 1, len(a_list))
				shared.print_oneliner(msg)

				# Open the link
				ds_url = a['href']
				ds_soup = bsoup.get_soup(ds_url)

				# Get the dataset title
				lyr_div = ds_soup.find('div', text='Layer Name')

				if lyr_div is not None:
					title = lyr_div.find_next_sibling('div').text

					# Get the release date
					date_strong = ds_soup.find('strong', text='Release Date: ')
					date = date_strong.next_sibling

					#print "Title: " + str(title)
					#print "Date: " + str(date)

					# Get the description
					abst_h = ds_soup.find('h3', text='Abstract')
					abst_div = abst_h.parent
					desc = abst_div.find_next_sibling('div')
					desc_str = desc.text

					# Get the formats
					formats = []
					gdb_td = ds_soup.find('td', text='Geodatabase')
					if gdb_td is not None: formats.append('GDB')
					shp_td = ds_soup.find('td', text='Shapefile')
					if shp_td is not None: formats.append('SHP')
					kmz_td = ds_soup.find('td', text='Google Earth (kmz)')
					if kmz_td is not None: formats.append('KMZ')

					pt_csv.add('Title', title)
					pt_csv.add('Description', desc_str)
					pt_csv.add('Available Formats', '|'.join(formats))
					pt_csv.add('Type', 'Vector File')
					pt_csv.add('Date', date)
					pt_csv.add('Download', 'Multiple Downloads')
					pt_csv.add('Metadata URL', ds_url)
					pt_csv.add('Access', 'Download/Accessible Web')
					pt_csv.add('Web Page URL', commap_url)

					pt_csv.write_dataset()

		############################################################################################
		# Stevenson Ridge

		steves_url = self.pg_grp.get_url('steves_url')
		steves_soup = bsoup.get_soup(steves_url)
		
		if self.check_result(steves_soup, steves_url, 'Stevenson Ridge Page'):
		
			# Get the description of the page
			mdata = bsoup.get_page_metadata(steves_soup)
			desc_str = mdata['Description']

			#pattern = re.compile(r'GIS Data')
			#gis_strong = steves_soup.find('strong', text=pattern)
			gis_strong = bsoup.find_tags_containing(steves_soup, 'GIS Data', 'strong')

			gis_parent = gis_strong.parent
			ul = gis_parent.find_next_sibling('ul')

			li_list = ul.find_all('li')
			for idx, li in enumerate(li_list):
				msg = "Extracting %s of %s pages" % (idx + 1, len(li_list))
				shared.print_oneliner(msg)
			
				li_text = li.text
				end_pos = li_text.find(':')
				title = li_text[:end_pos]

				formats = ['ESRI MDB', 'KMZ']
				
				self.notes = 'The KMZ downloads are broken links.'

				pt_csv.add('Title', title)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Available Formats', '|'.join(formats))
				pt_csv.add('Type', 'Vector File')
				pt_csv.add('Download', 'Multiple Downloads')
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Web Page URL', steves_url)
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

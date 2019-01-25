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
import traceback
import datetime
import inspect
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
		self.province = 'NWT'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Discovery Portal page group
		
		disc_grp = main_ext.PageGroup('discovery', 'NWT Discovery Portal')
		
		# Add arguments
		disc_grp.add_arg('word', title='Search Word')
		
		# Add URLs
		disc_grp.add_url('main_url', 'http://nwtdiscoveryportal.enr.gov.nt.ca')
		disc_grp.add_url('query_url', 'http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/find/document')
		
		# Add to Extractor's page group list
		self.page_groups.append(disc_grp)
		
		
		####################################################################
		# Create Interactive Maps page group

		map_grp = main_ext.PageGroup('maps', 'NWT Interactive Maps')
		
		# No arguments to add
		
		# Add URLs
		map_grp.add_url('webmap_url',
					   'http://www.arcgis.com/home/webmap/viewer.html?webmap=7199b8175dac48dc8513c824e39aa3fd')
		map_grp.add_url('gomap_url', ['http://ntgomap.nwtgeoscience.ca',
									 'http://ntgomap.nwtgeoscience.ca/config/layerList.xml'])
		map_grp.add_url('hub_url', ['https://datahub-ntgs.opendata.arcgis.com/datasets',
								   'https://opendata.arcgis.com/api/v2/datasets'])
								   
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		
		
		####################################################################
		# Create Web Pages page group

		web_grp = main_ext.PageGroup('pages', 'NWT Web Pages')
		
		# No arguments to add
		
		# Add URLs
		web_grp.add_url('geomatics_url', ['http://www.geomatics.gov.nt.ca',
										 'http://www.geomatics.gov.nt.ca/dldsoptions.aspx'])
		web_grp.add_url('enr_url',
					   'http://www.enr.gov.nt.ca/en/services/mobile-core-bathurst-caribou-management-zone')
								   
		# Add to Extractor's page group list
		self.page_groups.append(web_grp)
		
		
		####################################################################
		# Create Services page group

		srv_grp = main_ext.PageGroup('services', 'NWT Map Services')
		
		# No arguments to add
		
		# Add URLs
		srv_grp.add_url('rest_url', 'https://www.apps.geomatics.gov.nt.ca/ArcGIS/rest/services')
		srv_grp.add_url('image_url', 'https://www.image.geomatics.gov.nt.ca/ArcGIS/rest/services')
		srv_grp.add_url('geocortex_url', 'http://apps.geomatics.gov.nt.ca/Geocortex/Essentials/REST/sites')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		

	###################################################################################################################

	def extract_discovery(self): #, word=None):
		''' Extract data from the NWT Discovery Portal.
		:param word: Filter the search by this search word.
		:return: None
		'''

		###########################################################################
		# Extract the NWT Discovery Portal
		
		# Get the parameters
		word = self.get_arg_val('word')
		
		self.print_title("Extracting NWT's Discovery Portal")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		main_url = self.pg_grp.get_url('main_url')
		query_url = self.pg_grp.get_url('query_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "DiscoveryPortal_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Build the search URL and search the portal
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['searchText'] = word
		params['max'] = '100'
		params['kwcustom'] = '"Geospatial Data (Raster)","Geospatial Data (Vector)"'
		params['f'] = 'pjson'

		# Get the JSON results
		full_query = shared.get_post_query(query_url, params)
		
		#print "full_query: %s" % full_query
		
		json_results = shared.get_json(full_query, False, attempts=5)
		
		# Check results
		if not self.check_result(json_results, 'NWT Discovery'): return None
		
		all_records = json_results['records']

		rec_total = len(all_records)
		print "\nNumber of records: " + str(rec_total)

		record_count = 0

		for idx, rec in enumerate(all_records):
			msg = "Extracting %s of %s records" % (idx + 1, len(all_records))
			shared.print_oneliner(msg)
		
			# Locate the metadata link in the record's 'links' items
			mdata_xml_url = None
			links_list = rec['links']
			for link in links_list:
				# The metadata link is a link with 'type' 'fullMetadata'
				if link['type'] == 'metadata' or link['type'] == "fullMetadata":
					mdata_xml_url = link['href']

			# Load the metadata XML
			if mdata_xml_url is not None:
				#mdata_xml = bsoup.get_xml_soup(mdata_xml_url, True)
				mdata_xml = bsoup.get_xml_soup(mdata_xml_url)
				
				# #print len(mdata_xml.find_all())
				# print "Number of contents: %s" % len(mdata_xml.find_all())
				
				if len(mdata_xml.find_all()) == 0:
					continue

				# Build the metadata URL for the HTML page
				id = mdata_xml_url.split("=")[1]
				mdata_url = 'http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/resource/details.page?uuid=%s' % id

				kywrd_xml = mdata_xml.find_all('keyword')

				keywords = []
				for keyword in kywrd_xml:
					keywords.append(keyword.text.strip())

				# Get the spatial reference to determine if it is spatial data
				sp = mdata_xml.find('referenceSystemIdentifier')
				sp_str = ''
				if sp is not None:
					code = sp.find('code').text
					code = shared.clean_text(code)
					if code == '0' or code == 0 or code == '':
						sp_str = ''
					else:
						sp_str = "EPSG %s" % code

				# Get the title
				title = bsoup.get_text(mdata_xml.find('title'))

				# Get the description
				desc = bsoup.get_text(mdata_xml.find('abstract'))

				# Get the type
				format = bsoup.get_text(mdata_xml.find('dateType'))
				#ds_type = format.find('name').text

				# Get the date
				date = ''
				date_el = bsoup.find_tag(mdata_xml, 'CI_Date')
				if date_el is not None:
					date = bsoup.get_text(date_el.find('date'))

				# Get the web map viewer URL
				data_url = None
				map_viewer_url = ''
				download_link = None
				links = mdata_xml.find_all('linkage')
				link_list = [shared.clean_text(l.text) for l in links]
				webmap_url = ''
				for link in link_list:
					if link.find('map') > -1:
						# rec_dict['Download'] = 'No'
						webmap_url = link
					else:
						download_link = link

				if download_link is None:
					download_str = 'No'
					access_str = 'Contact the Territory'
				else:
					if download_link.lower().find('.pdf') > -1:
						continue
					download_str = download_link
					access_str = 'Download/Accessible Web'

				# Using the FTP link, determine the available formats
				formats = ''
				notes_str = ''
				if download_link is not None:
					if download_link.find('ftp') > -1:
						ftp_files = shared.ftp_files(ftp, download_link)
						if ftp_files is None:
							notes_str = 'The download link to the FTP site is broken.'
						else:
							formats_list = [f.split('.')[1].upper() for f in ftp_files]
							formats = '|'.join(formats_list)
				else:
					dist_form = mdata_xml.find('distributorFormat')
					if dist_form is not None:
						formats = dist_form.find('name').text
				# print formats
				# answer = raw_input("Press enter..."

				params = collections.OrderedDict()
				params['start'] = str(record_count + 1)
				params['max'] = '1'
				params['f'] = 'html'
				web_page_url = shared.get_post_query(query_url, params)

				# Get the metadata ISO
				mdata_iso = ''
				stand_tag = bsoup.find_tag(mdata_xml, 'metadataStandardName')
				if stand_tag is not None:
					mdata_iso = stand_tag.text

				pt_csv.add('Metadata URL', mdata_url)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Title', shared.clean_text(title))
				pt_csv.add('Description', desc)
				pt_csv.add('Type', shared.clean_text(format))
				pt_csv.add('Recent Date', shared.clean_text(date))
				pt_csv.add('Web Map URL', webmap_url)
				pt_csv.add('Download', download_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Notes', notes_str)
				pt_csv.add('Available Formats', formats)
				pt_csv.add('Web Page URL', web_page_url)
				pt_csv.add('Metadata Type', shared.clean_text(mdata_iso))

				pt_csv.write_dataset()
				
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		''' Extract the interactive maps for NWT
		:return: None
		'''

		# urls = collections.OrderedDict()
		# urls['NWT Fish Consumption Notices'] = (
		#     'http://www.arcgis.com/home/webmap/viewer.html?webmap=7199b8175dac48dc8513c824e39aa3fd',
		#     'http://www.arcgis.com/sharing/rest/content/items/7199b8175dac48dc8513c824e39aa3fd/data')
		# urls['NWT Spatial Data Warehouse Geospatial Portal'] = (
		#     'http://apps.geomatics.gov.nt.ca/HTML5_SDW/',
		#     'http://apps.geomatics.gov.nt.ca/Geocortex/Essentials/REST/sites/Spatial_Data_Warehouse')
		# urls['NWT Photo Map Ecosystem Classification'] = (
		#     'http://apps.geomatics.gov.nt.ca/SilverlightViewer_SDW/Viewer.html?Viewer=Land%20Classification%20Photo%20Map',
		#     'http://apps.geomatics.gov.nt.ca/Geocortex/Essentials/REST/sites/Forest_Management_Division__Ecological_Land_Classification_Photo_Map')
		# urls['NWT Mercury Predictors in Lakes Web Map'] = (
		#     'http://apps.geomatics.gov.nt.ca/SilverlightViewer_SDW/Viewer.html?Viewer=NWT%20Mercury%20Predictors%20in%20Fish',
		#     'http://apps.geomatics.gov.nt.ca/Geocortex/Essentials/REST/sites/NWT_Mercury_Predictors_in_Fish_Webmap')

		webmap_url = 'http://www.arcgis.com/home/webmap/viewer.html?webmap=7199b8175dac48dc8513c824e39aa3fd'
		# data_url = 'http://www.arcgis.com/sharing/rest/content/items/7199b8175dac48dc8513c824e39aa3fd/data'

		# Create the CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		self.print_title("Extracting NWT's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the ArcGIS data
		arcgis_info = shared.get_arcgis_data(webmap_url)

		# Add the ArcGIS data to the CSV
		for k, v in arcgis_info.items():
			pt_csv.add(k, v)

		# Add all values to the CSV file
		pt_csv.add('Source', 'NWT Interactive Maps')
		pt_csv.add('Access', 'Viewable/Map Service')
		pt_csv.add('Download', 'No')
		pt_csv.add('Web Map URL', webmap_url)

		pt_csv.write_dataset()

		###########################################################################
		# Extract the NWT GoMap Layers
		###########################################################################

		gomap_url = self.pg_grp.get_url('gomap_url')[0]
		lyrxml_url = self.pg_grp.get_url('gomap_url')[1]

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the CSV file
		# csv_fn = "GoMap_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()

		xml_soup = bsoup.get_xml_soup(lyrxml_url)
		
		if self.check_result(xml_soup, 'NWT GoMap Layers'):

			layers = xml_soup.find_all('layer')

			lyr_count = len(layers)

			print "Number of layers: %s" % lyr_count

			for idx, lyr in enumerate(layers):
			
				msg = "Extracting %s of %s layers from map" % (idx + 1, len(layers))
				shared.print_oneliner(msg)

				title = lyr.find('layerID').text
				pt_csv.add('Source', 'NWT Interactive Maps')
				pt_csv.add('Title', title)
				pt_csv.add('Download', 'No')
				pt_csv.add('Access', 'Viewable/Contact the Territory')
				pt_csv.add('Web Map URL', gomap_url)
				pt_csv.add('Data URL', lyrxml_url)
				pt_csv.add('Notes', 'Web map hangs while loading.')

				# Build the available formats
				shapeSize = lyr.find('shapeSize')
				kmlSize = lyr.find('kmlSize')
				formats = []
				if shapeSize is not None and int(shapeSize.text) > 0: formats.append('SHP')
				if kmlSize is not None and int(kmlSize.text) > 0: formats.append('KML')
				pt_csv.add('Available Formats', "|".join(formats))

				pt_csv.write_dataset()

			print
		#####################################################################################################
		# Extract the ArcGIS Hub

		hub_url = self.pg_grp.get_url('hub_url')[0]
		open_url = self.pg_grp.get_url('hub_url')[1]

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the CSV file
		# csv_fn = "ArcGIS_Hub_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()

		# Query Example:
		# 'https://opendata.arcgis.com/api/v2/datasets?
		#   filter[tags]=project
		#   &filter[catalogs]=datahub-ntgs.opendata.arcgis.com
		#   &include=organizations,groups
		#   &page[number]=1
		#   &page[size]=10'

		params = collections.OrderedDict()
		params['filter[catalogs]'] = 'datahub-ntgs.opendata.arcgis.com'
		params['include'] = 'sites,organizations,groups'
		params['page[number]'] = '1'
		params['page[size]'] = '310'
		query_url = shared.get_post_query(open_url, params)

		# attr_name = attrb[1]
		# el_type = attrb[0]
		# attrb = ('class', 'pagination')
		hub_json = shared.get_json(query_url)

		data_list = hub_json['data']

		for idx, data in enumerate(data_list):
			msg = "Extracting %s of %s ArcGIS Hub maps" % (idx + 1, len(data_list))
			shared.print_oneliner(msg)
		
			# Get the attributes
			attrs = data['attributes']

			# Get the title from the attributes
			title_str = attrs['name']

			# Get the description
			desc = attrs['description']
			desc_soup = BeautifulSoup(desc, 'html.parser')
			desc_str = desc_soup.text
			# desc_str = shared.edit_description(desc_str)

			# Get the date
			data_type = attrs['dataType']
			date = attrs['updatedAt']

			# Get the spatial reference
			sp = shared.get_spatialref(data, 'serviceSpatialReference')

			# Get the web page URL
			web_page_url = attrs['landingPage']
			web_service_url = attrs['url']
			
			pt_csv.add('Source', 'NWT Interactive Maps')
			pt_csv.add('Title', title_str)
			# rec_dict['Available Formats'] = 'FGDB|SHP'
			pt_csv.add('Type', data_type)
			pt_csv.add('Recent Date', date)
			pt_csv.add('Download', 'Multiple Downloads')
			pt_csv.add('Description', desc_str)
			pt_csv.add('Access', 'Viewable/Contact the Territory')
			pt_csv.add('Spatial Reference', sp)
			pt_csv.add('Web Page URL', web_page_url)
			pt_csv.add('Service URL', web_service_url)

			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_pages(self):
		''' Extracts the web pages of the Northwest Territories
		:return: None
		'''
		
		self.print_title("Extracting NWT's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		###########################################################################
		# Extract the NWT Mobile Core Bathurst Caribou Management Zone

		# Create the CSV file
		csv_fn = "WebPages_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		enr_url = self.pg_grp.get_url('enr_url')

		enr_soup = bsoup.get_soup(enr_url)

		# Get the download link
		pattern = re.compile(r'.gpx')
		anchor = enr_soup.find('a', text=pattern)
		download_url = anchor['href']
		if download_url.find('http:') == -1:
			download_url = "http:" + download_url

		# Get the title
		title_div = enr_soup.find('div', attrs={'class': 'service-banner-title'})
		h1 = title_div.find('h1')
		title = h1.text
		# title = 'Mobile Core Bathurst Caribou Management Zone'

		formats = 'GPX|KMZ'

		# Get the description
		a = enr_soup.find('a', attrs={'id': 'what-is-the-mobile-zone-'})
		h2 = a.parent
		p_desc = h2.find_next_sibling('p')
		p_desc2 = p_desc.find_next_sibling('p')
		desc_str = "%s %s" % (p_desc.text, p_desc2.text)

		pt_csv.add('Source', 'NWT Web Pages')
		pt_csv.add('Title', title)
		pt_csv.add('Available Formats', formats)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Download', download_url)
		pt_csv.add('Access', 'Download/Accessible Web')
		pt_csv.add('Web Page URL', enr_url)

		pt_csv.write_dataset()

		###########################################################################
		# Extract the NWT Centre for Geomatics page
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		data_url = self.pg_grp.get_url('geomatics_url')[1]

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the CSV file
		# csv_fn = "Geomatics_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()

		# Open the HTML page found in the files folder
		data_html = os.path.join(os.sep, shared.get_home_folder(), "files", "NWT Centre for Geomatics.html")
		data_f = open(data_html, 'r')
		data_str = data_f.read()

		data_soup = BeautifulSoup(data_str, 'html.parser')

		table = data_soup.find('table', attrs={'id': 'MainContent_HeadLoginView_gv_dlcatlisting'})

		tbody = table.find('tbody')

		# print tbody

		table_list = shared.table_to_dict(tbody, header_row=1, start_row=1)

		for row in table_list:
			# Get the title
			title_str = row['category'].text

			# Get the description
			desc_str = row['description'].text

			pt_csv.add('Source', 'NWT Web Pages')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Available Formats', 'SHP')
			pt_csv.add('Download', 'Yes (see Access)')
			pt_csv.add('Access', 'Download/Requires Registration')
			pt_csv.add('Web Page URL', data_url)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Extract the map services of the NWT.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting NWT's map services")
		
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
				
				#print "site_data: %s" % site_data
				#answer = raw_input("Press enter...")
				
				if not self.check_result(site_data, url, \
					'NWT Geocortex Service'):
					continue

				for rec in site_data:
					# Determine which CSV file to insert the service data
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', 'NWT Map Services')
					pt_csv.write_dataset()
			else:
				# Get a list of REST services
				my_rest = services.PT_REST(url)

				# Get the service and add it to the CSV file
				serv_data = my_rest.get_layers()
				
				if not self.check_result(serv_data, url, \
					'NWT ArcGIS REST Service'):
					continue
				
				for rec in serv_data:
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', 'NWT Map Services')
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

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
from StringIO import StringIO
from pyPdf import PdfFileWriter, PdfFileReader

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
#from common import access_rest as rest
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		# Set the province
		self.province = 'Nova_Scotia'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []
		
		####################################################################
		# Create Catalogue page group

		cat_grp = main_ext.PageGroup('catalogue', 'Open Data - Nova Scotia')
		
		# Add arguments
		cat_grp.add_arg('word', title='Search Word')
		ds_arg = cat_grp.add_arg('ds_type', title='Dataset Type')
		ds_arg.add_opt('Calendars', url_tags=['calendars'])
		ds_arg.add_opt('Charts', url_tags=['charts'])
		ds_arg.add_opt('Data Lens pages', ['lens'], ['new_view'])
		ds_arg.add_opt('Datasets', url_tags=['datasets'])
		ds_arg.add_opt('External Datasets', ['external'], ['href'])
		ds_arg.add_opt('Files and Documents', ['docs'], ['blob'])
		ds_arg.add_opt('Filtered Views', ['filters'], ['filters'])
		ds_arg.add_opt('Forms', url_tags=['forms'])
		ds_arg.add_opt('Maps', url_tags=['maps'])
		ds_arg.add_opt('Stories', url_tags=['story'])
		
		# Add URLs
		cat_grp.add_url('main_url', 'https://data.novascotia.ca/browse')
		
		# Add to Extractor's page group list
		self.page_groups.append(cat_grp)
		
		
		####################################################################
		# Create Natural Resources page group

		natr_grp = main_ext.PageGroup('natr', 'Department of Natural Resources')
		
		# No arguments to add
		
		# Add URLs
		#natr_grp.add_url('flowacc_url', 'https://novascotia.ca/natr/forestry/gis/wamdownload.asp')
		natr_grp.add_url('elc_url', 'https://novascotia.ca/natr/forestry/ecological/ecolandclass.asp')
		natr_grp.add_url('forest_urls', ['https://novascotia.ca/natr/forestry/gis/DL_forestry-cycle1.asp',
					'https://novascotia.ca/natr/forestry/gis/dl_forestry.asp',
					'https://novascotia.ca/natr/forestry/gis/DL_forestry-cycle2.asp'])
		natr_grp.add_url('fernow_url', 'https://novascotia.ca/natr/forestry/gis/fernow.asp')
		natr_grp.add_url('juan_url', 'https://novascotia.ca/natr/forestry/gis/juanimg.asp')
		natr_grp.add_url('landcap_url', 'https://novascotia.ca/natr/forestry/gis/landcap.asp')
		natr_grp.add_url('wam_url', 'https://novascotia.ca/natr/forestry/gis/wamdownload.asp')
		natr_grp.add_url('habitat_url', 'https://novascotia.ca/natr/wildlife/habitats/hab-data')
		
		# Add to Extractor's page group list
		self.page_groups.append(natr_grp)
		
		
		####################################################################
		# Create Natural Resources GIS page group

		gis_grp = main_ext.PageGroup('natrgis', 'NATR Downloadable GIS Data')
		
		# No arguments to add
		
		# Add URLs
		gis_grp.add_url('main_url', 'https://novascotia.ca/natr/meb/download/gis-data-maps.asp')
		
		# Add to Extractor's page group list
		self.page_groups.append(gis_grp)
		
		
		####################################################################
		# Create Geo Data Directory page group

		geo_grp = main_ext.PageGroup('datadir', 'Geographic Data Directory')
		
		# No arguments to add
		
		# Add URLs
		geo_grp.add_url('main_url', 'https://nsgi.novascotia.ca/gdd/')
		geo_grp.add_url('json_url', 'https://nsgi.novascotia.ca/WSF_DDS/DDS.svc/ListData?tkey=kNNpTdP4QuNRSYtt')
		
		# Add to Extractor's page group list
		self.page_groups.append(geo_grp)
		
		
		####################################################################
		# Create Map Services page group

		srv_grp = main_ext.PageGroup('services', 'Nova Scotia Map Services')
		
		# Add arguments
		sp_arg = srv_grp.add_arg('subpage', debug=True)
		sp_arg.add_opt('Geocortex')
		sp_arg.add_opt('ArcGIS')
		
		# Add URLs
		srv_grp.add_url('fletcher_url', 'https://fletcher.novascotia.ca/arcgis/rest/services')
		srv_grp.add_url('nsgiwa_url', 'https://nsgiwa.novascotia.ca/arcgis/rest/services')
		srv_grp.add_url('novarocmaps_url', 'https://novarocmaps.novascotia.ca/arcgis/rest/services')
		srv_grp.add_url('nsgc_url', 'https://gis7.nsgc.gov.ns.ca/arcgis/rest/services')
		srv_grp.add_url('sparc_url', 'http://sparc.smu.ca:6080/arcgis/rest/services')
		srv_grp.add_url('fernow_url', 'https://fernow.novascotia.ca/arcgis/rest/services')
		srv_grp.add_url('geocortex_url', 'https://fletcher.novascotia.ca/Geocortex/Essentials/REST/sites')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create Interactive Maps page group

		map_grp = main_ext.PageGroup('maps', 'Nova Scotia Interactive Maps')
		
		# No arguments to add
		
		# Add URLs
		map_grp.add_url('prov_url', 'https://www.novascotia.com/map')
		map_grp.add_url('cmmns_url', 'http://cmmns.com/member-communities/')
		map_grp.add_url('esip_url', 'http://www2.gulfofmaine.org/esip/reporting/gmap2.php')
		map_grp.add_url('data_url', 'https://gis8.nsgc.gov.ns.ca/DataLocatorASP/main.html')
		map_grp.add_url('firstnation_url', 'https://novascotia.ca/abor/aboriginal-people/community-info/')
		map_grp.add_url('munic_url', 'https://novascotia.ca/dma/government/map.asp')
		map_grp.add_url('lake_url', 'http://nse.maps.arcgis.com/apps/webappviewer/index.html?id=7ded7a30bef44f848e8a4fc8672c89bd')
		map_grp.add_url('plv_url', 'https://nsgi.novascotia.ca/plv/')
		map_grp.add_url('gallery_url', "https://nse.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=true&sortField=relevance")
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)

		
	###################################################################################################################

	def get_counties(self, soup, url):
		''' Gets a list of counties and their download links from a map
		:param soup: The soup containing the map.
		:param url: The URL for the download link.
		:return: A list of counties.
		'''

		# Get all the areas from the soup
		areas = soup.find_all('area')

		counties = []

		for area in areas:
			if area.has_attr('href'):
				# Get the area URL
				download_url = shared.get_anchor_url(area, url)

				# Get the county name
				county = area['alt']
				title_str = 'County %s' % county

				# Add it to the counties list
				counties.append((title_str, download_url))

		return counties

	def get_metadata(self, mdata_url):
		''' Gets the information from a metadata XML page.
		:param mdata_url: The metadata XML URL.
		:return: A dictionary containing the metadata info.
		'''
		
		#print mdata_url
		#answer = raw_input("Press enter...")

		# Get the metadata soup
		mdata_soup = bsoup.get_xml_soup(mdata_url)

		mdata_dict = collections.OrderedDict()

		# Get the title from the title element
		title = mdata_soup.find('title')
		title_str = title.text
		mdata_dict['Title'] = title_str

		# Get the description from the abstract element
		desc = mdata_soup.find('abstract')
		desc_str = desc.text
		mdata_dict['Description'] = desc_str

		# Get the type from the geoForm element
		data_type = mdata_soup.find('geoform')
		dtype_str = data_type.text
		mdata_dict['Type'] = dtype_str

		# Get the publisher from the origin element
		origin = mdata_soup.find('origin')
		pub_str = origin.text
		mdata_dict['Publisher'] = pub_str

		# Get the date from the caldate element
		caldate = mdata_soup.find('caldate')
		date_str = caldate.text
		mdata_dict['Date'] = date_str

		# Get metadata type from the metstdn element
		metstdn = mdata_soup.find('metstdn')
		mdata_type = metstdn.text
		mdata_dict['Metadata Type'] = mdata_type

		# Get the spatial reference from the projcsn element
		projcsn = mdata_soup.find('projcsn')
		sp_str = projcsn.text
		mdata_dict['Spatial Reference'] = sp_str

		return mdata_dict

	def get_gis_page(self, url):
		''' Extracts the context of a page from the NS Natural Resources Downloadable GIS Data page
			(https://novascotia.ca/natr/meb/download/gis-data-maps.asp).
		:param url: The page URL.
		:return: A dictionary containing items for the CSV file.
		'''

		if url.find('dp473.asp') > -1:
			# This is listed as a work in progress and has no web page yet as of 29/05/2018
			return None
		elif url.find('dp188.asp') > -1:
			# There is an extra '</strong>' tag on this page
			response = shared.open_webpage(url)
			html = response.read()

			# Remove the extract <strong> tag
			init_str = '''<div class="col_two">\r
		</strong>'''
			replace_str = '''<div class="col_two">\r'''
			sub_str = html.replace(init_str, replace_str)
			sub_soup = BeautifulSoup(sub_str, 'html.parser')
		else:
			# Get all complete pages
			sub_soup = bsoup.get_soup(url)
			
		if not self.check_result(sub_soup, url, 'NATR GIS Data'):
			return None

		# Get the metadata link from the website by finding an anchor with 'Metadata' text
		mdata_a = sub_soup.find('a', text='Metadata')
		#print "mdata_a: %s" % mdata_a
		#print sub_soup
		mdata_url = urlparse.urljoin(url, mdata_a['href'])
		response = shared.open_webpage(mdata_url)
		if not self.check_result(response, mdata_url, 'NATR GIS Data'):
			return None
		html = response.read()

		mdata_str = html.replace('<td align="left"\r', '<td align="left">\r')

		if mdata_url.find('dp430md.asp') > -1:
			# There is an extra '</a>' tag in one of the metadata pages
			#   so it needs to be fixed before souping
			mdata_str = html.replace('welldatabase.asp</a>', 'welldatabase.asp')

		elif mdata_url.find('dp442md.asp') > -1 or mdata_url.find('dp181md.asp') > -1 or \
				mdata_url.find('dp447md.asp') > -1:
			# Remove the extra </td></tr> from these pages
			init_str = 'Reference</a></li></ul></td></tr>'
			replace_str = 'Reference</a></li></ul>'
			mdata_str = html.replace(init_str, replace_str)

		elif mdata_url.find('dp095md.asp') > -1:
			# Add a <ul> and next line
			init_str = '''<td colspan="3">\r
			<li><a href = "#Ident'''
			replace_str = '''<td colspan="3">\r
			<ul>\n<li><a href = "#Ident'''
			mdata_str = html.replace(init_str, replace_str)

			# Remove an extra </tr>
			init_str = '''<td colspan="3">&nbsp;</td></tr>'''
			replace_str = '''<td colspan="3">&nbsp;</td>'''
			mdata_str = mdata_str.replace(init_str, replace_str)

		# Get the metadata soup once all pages have been fixed
		mdata_soup = BeautifulSoup(mdata_str, 'html.parser')

		# Parse the URL to get the ID before the '.asp'
		basename = os.path.basename(url)
		id = basename.split('.')[0]
		#print "ID: " + str(id)

		#print "mdata_url: " + str(mdata_url)

		if mdata_url.find('dp019md.asp') > -1 or mdata_url.find('dp136md.asp') > -1:
			# Geological Map of the Eureka Area
			tables = mdata_soup.find_all('table')
			table = tables[1]
		else:
			table = mdata_soup.find('table')

		# if mdata_url.find('dp095md.asp') > -1:
		#     html_f = open('%s_table.html' % id, 'w')
		#     html_f.write(str(table))
		#     html_f.close()
		#     html_f = open('%s_full.html' % id, 'w')
		#     html_f.write(str(mdata_str))
		#     html_f.close()

		mdata_dict = shared.info_to_dict(table) #, heading_tag='a') #, heading_tag='td', heading_attrb=['class', 'heading'])

		#print "mdata_dict keys: %s" % mdata_dict.keys()
		# for k, v in mdata_dict.items():
		#     print "\n%s:" % k
		#     for sub_k, sub_v in v.items():
		#         print "\t%s: %s" % (sub_k, [bsoup.get_text(s) for s in sub_v])
		#
		# answer = raw_input("Press enter...")

		if mdata_url.find('dp030md.asp') > -1:
			# Metadata for dp030 is empty so everything has to be extracted from dp030.asp

			# Get the title
			main_div = sub_soup.find('div', attrs={'id': 'main'})
			title = main_div.find('h1')
			title_str = title.text

			# Get the abstract for the description
			abstract_h = main_div.find('h3', text='Abstract')
			p_sib = abstract_h.find_next_sibling('p')
			desc_str = p_sib.text

			sp_str = 'NAD_1983_UTM_Zone_20N'
			dtype_str = 'vector digital data'
			date_str = ''
			pub_str = ''
			mdatatype_str = ''

		else:
			# Get the title
			title_str = bsoup.get_text(mdata_dict['Citation Information']['Title'][1])

			# Get the date
			date_str = bsoup.get_text(mdata_dict['Citation Information']['Publication Date'][1])

			# Get the publisher
			pub_str = bsoup.get_text(mdata_dict['Citation Information']['Publisher'][1])

			# Get the data type
			dtype_str = bsoup.get_text(mdata_dict['Citation Information']['Data Type'][1])

			# Get the description
			desc_str = bsoup.get_text(mdata_dict['Data Description']['Abstract'][1])

			# Get the spatial reference
			if 'Spatial Reference Information' not in mdata_dict.keys():
				sp_str = bsoup.get_text(mdata_dict['Spatial Data Organization Information']
										 ['Projected Coordinate System'][1])
			else:
				sp_str = bsoup.get_text(mdata_dict['Spatial Reference Information']
										 ['Projected Coordinate System'][1])

			# Get the metadata type
			mdatatype_str = bsoup.get_text(mdata_dict['Metadata Reference']['Metadata Standard'][1])

		# answer = raw_input("Press enter...")

		# Get the download link by replacing '.asp' in the URL to 'dds.asp'
		download_url = url.replace('.asp', 'dds.asp')

		# Get available formats which is located in a DIV containing the text 'Size'
		size_div = sub_soup.find('div', text='Size')
		#print url.find('dp188.asp') > -1
		if size_div is None:
			size_div = sub_soup.find('strong', text='Size')
			td_parent = size_div.parent
			sib = td_parent.find_next_sibling('td')
			if sib is None:
				sib = td_parent.find_next_sibling('div')
		elif url.find('dp017.asp') > -1:
			sib = size_div.parent
		else:
			sib = size_div.find_next_sibling('div')
		#print "sib: " + str(sib)
		p = sib.find('p')
		formats_str = ''
		if p is not None:
			size_text = p.text
			formats = re.findall(r'\b[A-Z]{3}', size_text)
			formats_str = "|".join(formats)

		# Get the license link
		lic_url = url.replace('.asp', 'dll.asp')

		# Get the interactive map link by locating an anchor with text 'View Interactive Map'
		map_a = sub_soup.find('a', text='View Interactive Map')
		if map_a is None:
			map_url = ""
		else:
			map_url = map_a['href']

		# Get the service URL by locating an anchor with text 'ArcGIS REST Service'
		serv_a = sub_soup.find('a', text='ArcGIS REST Service')
		if serv_a is None:
			serv_url = ""
			serv_name = ""
		else:
			serv_url = serv_a['href']
			service = shared.get_json(serv_url + "?f=pjson")

			# Get the service name
			serv_name = service['mapName']

		rec_dict = collections.OrderedDict()
		
		#print "description: %s" % desc_str
		
		rec_dict['Title'] = title_str
		rec_dict['Date'] = date_str
		rec_dict['Type'] = dtype_str
		rec_dict['Description'] = desc_str
		rec_dict['Licensing'] = lic_url
		rec_dict['Web Page URL'] = url
		rec_dict['Access'] = 'Download/Accessible Web'
		rec_dict['Download'] = download_url
		# pt_csv.add('Data URL', data_link)
		rec_dict['Web Map URL'] = map_url
		rec_dict['Service Name'] = serv_name
		rec_dict['Service URL'] = serv_url
		rec_dict['Service'] = 'ESRI REST'
		rec_dict['Publisher'] = pub_str
		rec_dict['Spatial Reference'] = sp_str
		rec_dict['Metadata URL'] = mdata_url
		rec_dict['Metadata Type'] = mdatatype_str
		rec_dict['Available Formats'] = formats_str
		
		return rec_dict
	
	def extract_catalogue(self): #, word=None, ds_type=None):
		###########################################################################
		# Extract the Nova Scotia's Open Data Catalogue
		
		# Get the parameters
		word = self.get_arg_val('word')
		ds_type = self.get_arg_val('ds_type')
		
		# Convert ds_type to the proper value for the query
		ds_opts = self.get_arg_opts('ds_type')
		for opt in ds_opts:
			url_tag = opt.get_urltags()[0]
			if ds_type.lower() == url_tag.lower():
				ds_type = url_tag.lower()

		main_url = self.pg_grp.get_url('main_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's Catalogue")
		
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
			params['limitTo'] = ds_type

		query_url = shared.get_post_query(main_url, params)

		res_soup = bsoup.get_soup(query_url)

		# Get the page count
		print query_url
		res_div = res_soup.find('div', attrs={'class': 'browse2-results-title'})
		res_str = bsoup.get_text(res_div)
		reg = re.findall('\d+(?:,\d+)?', res_str)
		res_total = reg[0]
		per_page = 10
		page_count = math.ceil(float(res_total) / float(per_page))
		page_count = int(page_count)

		print "Number of pages: " + str(page_count)
		
		print "\nNumber of results found: %s" % res_total

		data_url = 'https://data.novascotia.ca/api/views/'
		
		record = 0
		for page in range(1, page_count + 1):
		
			page_url = "%s&page=%s" % (query_url, page)

			page_soup = bsoup.get_soup(page_url)

			results = page_soup.find_all('div', attrs={'class': 'browse2-result'})

			for res in results:
				record += 1
				msg = "Extracting %s of %s results from '%s'" % (record, res_total, query_url)
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
				desc_str = data_json['description']

				# Get date
				date = data_json['indexUpdatedAt']
				date_str = shared.translate_date(date)
				
				# Get created date
				startdate = data_json['createdAt']
				startdate_str = shared.translate_date(startdate)

				# Get the license
				lic_str = ''
				if 'license' in data_json:
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
				download_url = 'https://data.novascotia.ca/api/geospatial/%s?method=export&format=Original' % id

				# print "Description: " + str(desc_str)
				# print "Date: " + str(date_str)
				# print "License: " + str(lic_str)
				# print "Spatial Reference: " + str(sp_str)
				# print "Download Link: " + str(download_url)
				# print "Author: " + str(author_str)

				# answer = raw_input("Press enter...")
				
				pt_csv.add('Source', "Nova Scotia's Open Data Portal")
				pt_csv.add('Title', title)
				pt_csv.add('Start Date', startdate_str)
				pt_csv.add('Recent Date', date_str)
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

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_datadir(self):
		''' Extracts the Nova Scotia Geographic Data Directory pages.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's Data Directory pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "DataDirectory_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		###########################################################################
		# Extract the Geographic Data Directory

		main_url = self.pg_grp.get_url('main_url')
		json_url = self.pg_grp.get_url('json_url')

		json_data = shared.get_json(json_url)
		results = json_data['results']

		# Get the tkey from the JSON URL
		tkey = ''
		query = json_url.split('?')[1]
		properties = query.split('&')
		for prop in properties:
			param, value = prop.split('=')
			if param == 'tkey':
				tkey = value

		for res in results:
			id = res['id']
			title = res['title']
			desc = res['description']
			desc_str = desc
			date = res['published']
			serv_url = res['map_service_url']
			lyr_type = res['ms_layer_type']

			# Download link can be created using the tkey from the JSON URL
			download_url = "https://nsgi.novascotia.ca/WSF_DDS/DDS.svc/DownloadFile" #?tkey=kNNpTdP4QuNRSYtt&id=88"
			params = collections.OrderedDict()
			params['tkey'] = tkey
			params['id'] = id
			dlquery_url = shared.get_post_query(download_url, params)

			#print "dlquery_url: " + str(dlquery_url)
			#answer = raw_input("Press enter...")

			pt_csv.add('Source', "Nova Scotia's Geographic Data Directory")
			pt_csv.add('Title', title)
			pt_csv.add('Recent Date', date)
			pt_csv.add('Description', desc_str)
			# pt_csv.add('Licensing', lic_str)
			pt_csv.add('Web Page URL', main_url)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', dlquery_url)
			pt_csv.add('Service URL', serv_url)
			pt_csv.add('Service', lyr_type)
			pt_csv.add('Data URL', json_url)
			#pt_csv.add('Publisher', pub_str)
			pt_csv.add('Spatial Reference', 'NAD83(CSRS), Universal Transverse Mercator Zone 20')
			#pt_csv.add('Metadata URL', mdata_url)
			#pt_csv.add('Metadata Type', mdata_type)
			#pt_csv.add('Available Formats', 'SHP')

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		#pg.add_page('prov_url', 'https://www.novascotia.com/map')
		#pg.add_page('cmmns_url', 'http://cmmns.com/member-communities/')
		#pg.add_page('gulf_url', 'http://www2.gulfofmaine.org/esip/reporting/gmap2.php')
		#pg.add_page('data_url',
		#            'https://gis8.nsgc.gov.ns.ca/esrimap/esrimap.dll?name=DataLocator&cmd=0&t=5330999&b=4728598&l=169676&r=915634&nt=0&nb=0&nl=0&nr=0&action=overview&X=0&Y=0&ind=0&objid=0&DIon=True&NDIon=False&PIon=False&la=&hPid=0&pb=&sz=1&ind=25&searchType=pn&sI=&st=pn&County=&zR=2&il=25')
		#pg.add_page('firstnation_url', 'https://novascotia.ca/abor/aboriginal-people/community-info/')
		#pg.add_page('munic_url', 'https://novascotia.ca/dma/government/map.asp')
		#pg.add_page('lake_url',
		#            'http://nse.maps.arcgis.com/apps/webappviewer/index.html?id=7ded7a30bef44f848e8a4fc8672c89bd')
		#pg.add_page('plv_url', 'https://nsgi.novascotia.ca/plv/')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "Maps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		###########################################################################
		# Nova Scotia Provincial Map

		prov_url = self.pg_grp.get_url('prov_url')
		prov_soup = bsoup.get_soup(prov_url)
		
		# Get the page's metadata
		prov_mdata = bsoup.get_page_metadata(prov_soup)
		
		# Get the title from the page
		title_str = prov_mdata['page_title']

		# Get the description from the metadata
		desc_str = prov_mdata['description']

		#print "Description: " + str(desc_str)

		pt_csv.add('Source', "Nova Scotia's Interactive Maps")
		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Google Maps API')
		pt_csv.add('Web Map URL', prov_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# The Confederacy of Mainland Mi'kmaq - Member Communities

		cmmns_url = self.pg_grp.get_url('cmmns_url')
		cmmns_soup = bsoup.get_soup(cmmns_url)

		# Get the title from the web page title
		title = cmmns_soup.find('title')
		title_str = title.text

		#print "Title: " + str(title_str)

		# Get the description from the web page description
		#desc = prov_soup.find('meta', attrs={'name': 'description'})
		#desc_str = desc['content']

		#print "Description: " + str(desc_str)

		pt_csv.add('Title', title_str)
		#pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Google Maps API')
		pt_csv.add('Web Map URL', cmmns_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# The EcoSystem Indicator Partnership

		esip_url = self.pg_grp.get_url('esip_url')
		esip_soup = bsoup.get_soup(esip_url)

		# Get the title from the web page title
		title = esip_soup.find('title')
		title_str = title.text

		#print "Title: " + str(title_str)

		# Get the description from the web page description
		about_div = esip_soup.find('div', attrs={'id': 'help-box-about-esip'})
		p_desc = about_div.find('p')
		desc_str = p_desc.text

		#print "Description: " + str(desc_str)

		pt_csv.add('Title', title_str)
		pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Google Maps API')
		pt_csv.add('Web Map URL', esip_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# The DataLocator

		data_url = self.pg_grp.get_url('data_url')
		data_soup = bsoup.get_soup(data_url)

		# Get a list of item <div> elements
		item_divs = data_soup.find_all('div', attr={'class': 'item'})
		
		for item in item_divs:
			# Get the title <a>
			title_a = item.find('a', attr={'class': 'item_title'})
			title_str = bsoup.get_text(title_a)
			
			if title_str == 'Indexing System' or title_str == 'Elevation Explorer':
				# Get the description
				desc_p = item.find('p', attr={'class': 'description'})
				desc_str = bsoup.get_text(desc_p)
				
				map_url = shared.get_anchor_url(title_a, data_url)

				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Access', 'Viewable/Contact the Province')
				#pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
				pt_csv.add('Download', 'No')

				pt_csv.write_dataset()

		###########################################################################
		# The Map of First Nations in Nova Scotia

		firstnation_url = self.pg_grp.get_url('firstnation_url')
		firstnation_soup = bsoup.get_soup(firstnation_url)

		# Get the title from the web page title
		title = firstnation_soup.find('h1', attrs={'id': 'page-title'})
		title_str = title.text
		title_str = title_str.split('|')[0].strip()

		#print "Title: " + str(title_str)

		# Get the description from the web page description
		# about_div = data_soup.find('div', attrs={'id': 'help-box-about-esip'})
		# p_desc = about_div.find('p')
		# desc_str = p_desc.text

		# print "Description: " + str(desc_str)

		pt_csv.add('Title', title_str)
		#pt_csv.add('Description', shared.edit_description(desc_str))
		#pt_csv.add('Type', 'ESRI Map')
		pt_csv.add('Web Map URL', firstnation_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		# pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# Nova Scotia Provincial Map

		munic_url = self.pg_grp.get_url('munic_url')
		munic_soup = bsoup.get_soup(munic_url)

		# Get the title from the web page title
		title = munic_soup.find('title')
		title_str = title.text

		#print "Title: " + str(title_str)

		# Get the description from the web page description
		#desc = prov_soup.find('meta', attrs={'name': 'description'})
		#desc_str = desc['content']

		# Get the date from the web page elements
		meta = munic_soup.find('meta', attrs={'name': 'dcterms.modified'})
		date = meta['content']

		#print "Description: " + str(desc_str)

		pt_csv.add('Title', title_str)
		#pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'Google Maps API')
		pt_csv.add('Recent Date', date)
		pt_csv.add('Web Map URL', prov_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator (EPSG:3857)')
		pt_csv.add('Download', 'No')
		pt_csv.add('Notes', 'The page loads but no map appears.')

		pt_csv.write_dataset()

		# ###########################################################################
		# # Nova Scotia Lake Survey Program
		#
		# lake_url = self.pg_grp.get_url('lake_url')
		# json_url = shared.get_argcis_data(lake_url)
		# lake_soup = bsoup.get_soup(lake_url)
		# lake_json = shared.get_json(json_url)
		#
		# # Get the title from the web page title
		# title_str = lake_json['title']
		#
		# print "Title: " + str(title_str)
		#
		# # Get the description from the web page description
		# # desc = prov_soup.find('meta', attrs={'name': 'description'})
		# # desc_str = desc['content']
		#
		# # Get the date from the web page elements
		# #meta = munic_soup.find('meta', attrs={'name': 'dc.date'})
		# #date = meta['content']
		#
		# #print "Description: " + str(desc_str)
		#
		# sp_str = shared.get_spatialref(lake_json)
		#
		# pt_csv.add('Title', title_str)
		# # pt_csv.add('Description', desc_str)
		# pt_csv.add('Type', 'ArcGIS Online Map')
		# #pt_csv.add('Date', date)
		# pt_csv.add('Web Map URL', lake_url)
		# pt_csv.add('Access', 'Viewable/Contact the Province')
		# pt_csv.add('Spatial Reference', sp_str)
		# pt_csv.add('Download', 'No')
		#
		# pt_csv.write_dataset()

		###########################################################################
		# Provincial Landscape Viewer

		plv_url = self.pg_grp.get_url('plv_url')
		json_url = 'https://dnr-ns.maps.arcgis.com/sharing/rest/content/items/50cea634ffbf433ba5cde6961a9809b7?f=json'
		plv_soup = bsoup.get_soup(plv_url)
		plv_json = shared.get_json(json_url)

		# Get the title from the web page title
		title_str = plv_json['title']

		#print "Title: " + str(title_str)

		# Get the description from the web page description
		# desc = prov_soup.find('meta', attrs={'name': 'description'})
		# desc_str = desc['content']

		# Get the date from the web page elements
		# meta = munic_soup.find('meta', attrs={'name': 'dc.date'})
		date = plv_json['modified']
		date_str = shared.translate_date(date)

		# print "Description: " + str(desc_str)

		#sp_str = shared.get_spatialref(lake_json)

		pt_csv.add('Title', title_str)
		# pt_csv.add('Description', desc_str)
		pt_csv.add('Type', 'ArcGIS Online Map')
		pt_csv.add('Recent Date', date_str)
		pt_csv.add('Web Map URL', plv_url)
		pt_csv.add('Access', 'Viewable/Contact the Province')
		#pt_csv.add('Spatial Reference', sp_str)
		pt_csv.add('Download', 'No')

		pt_csv.write_dataset()

		###########################################################################
		# Nova Scotia Environment Publicly Featured Maps and Services
		
		gallery_url = self.pg_grp.get_url('gallery_url')
		
		# Get the gallery data
		gallery_maps = shared.get_arcgis_gallery(gallery_url)

		for map in gallery_maps:
			for k, v in map.items():
				pt_csv.add(k, v)

			pt_csv.write_dataset()

		# params = collections.OrderedDict()
		# params['q'] = 'group%3A47fb9fa286994ad58be1f448f0e1bf24%20-(type%3A"Code%20Attachment"%20OR' \
					  # '%20type%3A"Windows%20Viewer%20Add%20In"%20OR%20type%3A"Windows%20Viewer%20Configuration")'
		# params['f'] = 'pjson'
		# params['num'] = '12'
		# params['sortField'] = 'title'
		# params['sortOrder'] = 'asc'
		# params['ts'] = '1527711014313'
		# srch_url = shared.get_post_query('https://nse.maps.arcgis.com/sharing/rest/search', params)
		
		# print "srch_url: %s" % srch_url
		
		# answer = raw_input("Press enter...")

		# maps_json = shared.get_json(srch_url)
		# results = maps_json['results']

		# for res in results:
			# id = res['id']
			# title_str = res['title']
			# dtype = res['type']
			# desc = res['description']
			# if desc is not None:
				# desc_soup = BeautifulSoup(desc, 'html.parser')
				# desc_str = shared.edit_description(desc_soup.text)
			# else:
				# desc_str = ''
			# sp_str = res['spatialReference']
			# serv_url = res['url']
			# date_str = shared.translate_date(res['modified'])
			# #webmap_url = 'http://nse.maps.arcgis.com/apps/webappviewer/index.html?id=%s' % id
			# #webmap_url = 'http://nse.maps.arcgis.com/apps/Viewer/index.html?appid=%s' % id

			# if serv_url is None:
				# webmap_url = ''
				# serv_name = ''
				# serv_type = ''
			# else:
				# if serv_url.lower().find('viewer') > -1:
					# webmap_url = serv_url
					# serv_url = ''
					# serv_name = ''
					# serv_type = ''
				# else:
					# webmap_url = ''
					# json_url = serv_url + "?f=pjson"
					# print json_url
					# webmap_json = shared.get_json(json_url)
					# if 'name' in webmap_json:
						# serv_name = webmap_json['name']
					# else:
						# serv_name = webmap_json['serviceDescription']
					# if 'type' in webmap_json:
						# serv_type = webmap_json['type']
					# else:
						# serv_type = os.path.basename(serv_url)

			# pt_csv.add('Title', title_str)
			# pt_csv.add('Description', desc_str)
			# pt_csv.add('Type', dtype)
			# pt_csv.add('Date', date_str)
			# pt_csv.add('Web Map URL', webmap_url)
			# pt_csv.add('Service Name', serv_name)
			# pt_csv.add('Service', serv_type)
			# pt_csv.add('Access', 'Viewable/Contact the Province')
			# pt_csv.add('Spatial Reference', sp_str)
			# pt_csv.add('Service URL', serv_url)
			# pt_csv.add('Download', 'No')

			# pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_natr(self):
		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's Department of Natural Resources pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()

		# Create the CSV file
		csv_fn = "NATR_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# ###########################################################################
		# # Extract the Wet Areas Mapping and Flow Accumulation Channel

		# flowacc_url = self.pg_grp.get_url('flowacc_url')
		# flowacc_soup = bsoup.get_soup(flowacc_url)

		# # Get the download link
		# download_a = flowacc_soup.find('a', text='Download flow accumulation data')
		# download_url = download_a['href']

		# # Get the metadata URL
		# mdata_a = download_a.find_next_sibling('a')
		# mdata_url = urlparse.urljoin(flowacc_url, mdata_a['href'])
		# mdata_soup = bsoup.get_xml_soup(mdata_url)

		# # Get the title
		# title = mdata_soup.find('title')
		# title_str = title.text
		# #print title_str

		# # Get the description
		# desc = mdata_soup.find('abstract')
		# desc_str = shared.edit_description(desc.text)
		# #print desc_str

		# # Get the type
		# data_type = mdata_soup.find('geoform')
		# dtype_str = data_type.text
		# #print dtype_str

		# # Get the publisher
		# origin = mdata_soup.find('origin')
		# pub_str = origin.text
		# #print pub_str

		# # Get the date
		# caldate = mdata_soup.find('caldate')
		# date_str = caldate.text
		# #print date_str

		# # Get metadata type
		# metstdn = mdata_soup.find('metstdn')
		# mdata_type = metstdn.text

		# # Get the spatial reference
		# projcsn = mdata_soup.find('projcsn')
		# sp_str = projcsn.text

		# pt_csv.add('Title', title_str)
		# pt_csv.add('Date', date_str)
		# pt_csv.add('Type', dtype_str)
		# pt_csv.add('Description', desc_str)
		# pt_csv.add('Web Page URL', flowacc_url)
		# pt_csv.add('Access', 'Download/Accessible Web')
		# pt_csv.add('Download', download_url)
		# pt_csv.add('Publisher', pub_str)
		# pt_csv.add('Spatial Reference', sp_str)
		# pt_csv.add('Metadata URL', mdata_url)
		# pt_csv.add('Metadata Type', mdata_type)
		# pt_csv.add('Available Formats', 'SHP')

		# pt_csv.write_dataset()

		###########################################################################
		# Extract the Ecological Land Classification
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		elc_url = self.pg_grp.get_url('elc_url')
		elc_soup = bsoup.get_soup(elc_url)

		# Get the description
		main_div = elc_soup.find('div', attrs={'id': 'main'})
		desc_p = main_div.find('p')
		desc_str = desc_p.string

		# Locate the <h3> with a specific text
		h3 = elc_soup.find('h3', text='Ecological Land Classification for Nova Scotia:')
		# Get the licence text from the next <p>
		lic_p = h3.find_next_sibling('p')
		lic_a = lic_p.a
		lic_url = urlparse.urljoin(elc_url, lic_a['href'])

		# Locate all <strong> elements on the page
		strong_list = elc_soup.find_all('strong')

		for strong in strong_list:
			# Get the title
			title_str = strong.text

			pt_csv.add('Source', "Nova Scotia's NATR Pages")
			pt_csv.add('Title', title_str)
			pt_csv.add('Type', 'Vector Data File')
			pt_csv.add('Description', desc_str)
			pt_csv.add('Licensing', lic_url)
			pt_csv.add('Web Page URL', elc_url)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', 'Multiple Downloads')
			pt_csv.add('Spatial Reference', 'NAD_1983_CSRS_UTM_Zone_20N')
			pt_csv.add('Available Formats', 'SHP|FGDB')

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Forest Inventory pages

		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)
		
		# Get the list of URLs
		forest_urls = self.pg_grp.get_url('forest_urls')

		for url in forest_urls:
			# For each Forest Inventory page
			forest_soup = bsoup.get_soup(url)

			# Get the cycle number from the current URL
			url_parse = url.split('/')
			basename = url_parse[len(url_parse) - 1]
			parse_basename = basename.split('-')
			if len(parse_basename) == 2:
				cycle = parse_basename[1]
				cycle_str = cycle.replace('.asp', '')
			else:
				cycle_str = 'Current'

			# Get description from PDF file
			pdf_a = forest_soup.find('a', text='View Attribute Descriptions and Coding')
			#print pdf_a
			pdf_link = pdf_a['href']
			pdf_url = urlparse.urljoin(url, pdf_link)

			# Open the PDF link
			remoteFile = shared.open_webpage(pdf_url).read()
			# Store it in memory
			memoryFile = StringIO(remoteFile)

			# Create the PDF File Reader
			pdfFile = PdfFileReader(memoryFile)

			desc_str = ''
			for pageNum in xrange(pdfFile.getNumPages()):
				# For each page in the PDF file

				# Set the current page
				currentPage = pdfFile.getPage(pageNum)

				# Extract the text from the page
				pdf_page = currentPage.extractText()

				# Locate the description
				desc_pos = pdf_page.find('Description/Source')
				if desc_pos > -1:
					start_pos = desc_pos + len('Description/Source')
					desc_str = pdf_page[start_pos:]
					break

			#print desc_str

			# Get the county info from the map on the page
			counties = self.get_counties(forest_soup, url)

			for county in counties:

				# Get the county info
				county_name = county[0]
				county_download = county[1]

				pt_csv.add('Source', "Nova Scotia's NATR Pages")
				pt_csv.add('Title', "Forest Inventory, %s - %s" % (cycle_str, county_name))
				pt_csv.add('Type', 'Vector Data File')
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Page URL', url)
				pt_csv.add('Access', 'Download/Accessible Web')
				pt_csv.add('Download', county_download)
				pt_csv.add('Spatial Reference', 'UTM Zone 20N NAD83')
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

		###########################################################################
		# Extract the Geographic Information Systems - Fernow Forest Cover
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		fernow_url = self.pg_grp.get_url('fernow_url')
		fernow_soup = bsoup.get_soup(fernow_url)

		# Get the download link
		download_a = fernow_soup.find('a', text='Download data')
		download_url = download_a['href']

		# Get the metadata link
		mdata_a = download_a.find_next_sibling('a')
		mdata_url = urlparse.urljoin(fernow_url, mdata_a['href'])

		# Get the metadata dictionary
		mdata_info = self.get_metadata(mdata_url)

		# Fill in the items in pt_csv with the keys of the mdata_info
		for k, v in mdata_info.items():
			pt_csv.add(k, v)

		# Fill in the rest of the items in pt_csv
		pt_csv.add('Source', "Nova Scotia's NATR Pages")
		pt_csv.add('Web Page URL', fernow_url)
		pt_csv.add('Access', 'Download/Accessible Web')
		pt_csv.add('Download', download_url)
		pt_csv.add('Metadata URL', mdata_url)
		pt_csv.add('Available Formats', 'SHP')

		pt_csv.write_dataset()

		###########################################################################
		# Extract the Geographic Information Systems - Hurricane Juan Imagery
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		juan_url = self.pg_grp.get_url('juan_url')
		juan_soup = bsoup.get_soup(juan_url)

		# Get the description
		main_div = juan_soup.find('div', attrs={'id': 'main'})
		desc_p = main_div.find('p')
		desc_str = desc_p.string

		#print juan_soup

		# Get all the columns on the page (a table which contains all the downloads)
		td_list = juan_soup.find_all('td')

		for td in td_list:
			# Get the title from the column text
			td_a = td.find('a')
			tile_id = td_a.text
			title_str = 'Hurricane Juan Imagery - Tile %s' % tile_id

			download_url = td_a['href']

			pt_csv.add('Source', "Nova Scotia's NATR Pages")
			pt_csv.add('Title', title_str)
			pt_csv.add('Type', 'Raster Data File')
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Page URL', juan_url)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', download_url)
			pt_csv.add('Spatial Reference', 'UTM Zone 20N NAD83')
			pt_csv.add('Available Formats', 'MrSID')

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Geographic Information Systems - Land Capability for Forestry
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		landcap_url = self.pg_grp.get_url('landcap_url')
		landcap_soup = bsoup.get_soup(landcap_url)

		# Get the metadata URL which is in an anchor with text 'View Metadata'
		mdata_a = landcap_soup.find('a', text='View metadata')
		mdata_url = urlparse.urljoin(landcap_url, mdata_a['href'])
		# Get the metadata dictionary
		mdata_info = self.get_metadata(mdata_url)

		# Get the counties from the map
		counties = self.get_counties(landcap_soup, landcap_url)

		for county in counties:

			# Get the county info
			county_name = county[0]
			county_download = county[1]

			# Fill in the items in pt_csv with the keys of the mdata_info
			for k, v in mdata_info.items():
				if k == 'Title':
					title_str = v
				else:
					pt_csv.add(k, v)

			pt_csv.add('Source', "Nova Scotia's NATR Pages")
			pt_csv.add('Title', "%s - %s" % (title_str, county_name))
			pt_csv.add('Web Page URL', landcap_url)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', county_download)
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Available Formats', 'SHP')

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Wet Areas Mapping and Flow Accumulation Channel
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		wam_url = self.pg_grp.get_url('wam_url')
		wam_soup = bsoup.get_soup(wam_url)

		# Get the metadata URL which is in an anchor with text 'View Metadata'
		mdata_a = wam_soup.find('a', text='View WAM metadata')
		mdata_url = urlparse.urljoin(wam_url, mdata_a['href'])
		# Get the metadata dictionary
		mdata_info = self.get_metadata(mdata_url)

		# Get the counties from the map
		counties = self.get_counties(wam_soup, wam_url)

		for county in counties:

			# Get the county info
			county_name = county[0]
			county_download = county[1]

			# Fill in the items in pt_csv with the keys of the mdata_info
			for k, v in mdata_info.items():
				if k == 'Title':
					title_str = v
				else:
					pt_csv.add(k, v)

			pt_csv.add('Source', "Nova Scotia's NATR Pages")
			pt_csv.add('Title', "%s - %s" % (title_str, county_name))
			pt_csv.add('Web Page URL', wam_url)
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', county_download)
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Available Formats', 'SHP')

			pt_csv.write_dataset()

		###########################################################################
		# Extract the Significant Species and Habitats Database
		
		# Print the status
		cur_page += 1
		msg = "Extracting %s of %s web pages" % (cur_page, page_count)
		shared.print_oneliner(msg)

		habitat_url = self.pg_grp.get_url('habitat_url')
		habitat_soup = bsoup.get_soup(habitat_url)

		# Locate the <strong> title with the links below
		strong = habitat_soup.find('strong', text='Download ArcView Shapefiles - (UTM, NAD83, Zone 20)')

		# Locate the next strong to get the date
		date_strong = strong.find_next_sibling('strong')
		date_str = date_strong.text
		date_str = date_str.replace('last updated ', '')

		# Get the parent <p> and then the next <ul>
		p_parent = strong.parent
		ul = p_parent.find_next_sibling('ul')
		a_list = ul.find_all('a')
		for a in a_list:
			# Go through each anchor (download)

			# Get the download link
			download_url = shared.get_anchor_url(a, habitat_url)

			# Get the title from the <a> text
			title = a.text
			title_str = 'Significant Species and Habitats - %s' % title

			# For the description, search for 'p' with 'Significant habitats include; ' and its 'ol' sibling
			p_desc = habitat_soup.find('p', text='Significant habitats include; ')
			desc_str = p_desc.text
			ol_sib = p_desc.find_next_sibling('ol')
			li_list = ol_sib.find_all('li')
			for li in li_list:
				desc_str += li.text

			# Set the spatial reference
			sp_str = 'UTM, NAD83, Zone 20'

			pt_csv.add('Source', "Nova Scotia's NATR Pages")
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Recent Date', date_str)
			pt_csv.add('Web Page URL', habitat_url)
			pt_csv.add('Type', 'Vector Date File')
			pt_csv.add('Access', 'Download/Accessible Web')
			pt_csv.add('Download', download_url)
			pt_csv.add('Spatial Reference', sp_str)
			pt_csv.add('Available Formats', 'SHP')

			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_natrgis(self):
		''' Extracts all the map pages on the NS Natural Resources Downloadable GIS Data
		:return: None
		'''

		###########################################################################
		# Extract the Downloadable GIS Data

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's Department of Natural " \
							"Resources GIS Data")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "NATR_GIS_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		gis_url = self.pg_grp.get_url('main_url')
		gis_soup = bsoup.get_soup(gis_url)

		# Each list of links is in DIVs with class 'block'
		block_divs = gis_soup.find_all('div', attrs={'class': 'block'})

		for block in block_divs:
			li_list = block.find_all('li')

			for li in li_list:
				# Get the download page link and get the soup
				a = li.find('a')
				sub_sites = []
				if not a.has_attr('href'):
					ul = li.find('ul')
					a_list = ul.find_all('a')
					for a in a_list:
						url = urlparse.urljoin(gis_url, a['href'])
						sub_sites.append(url)
				else:
					url = urlparse.urljoin(gis_url, a['href'])
					sub_sites.append(url)

				map_sites = []
				map_sites.append('interactive-bedrock-DNR-map.asp')
				map_sites.append('interactive-bedrock-GSC-map.asp')
				map_sites.append('interactive-map-surficial-data.asp')
				map_sites.append('interactive-map-radar-data.asp')
				map_sites.append('interactive-seismic-map.asp')
				map_sites.append('interactive-gold-district-map-data-east.asp')
				map_sites.append('interactive-gold-district-map-data-west.asp')
				map_sites.append('interactive-agg-gis.asp')
				map_sites.append('interactive-map-airmag-1D-data.asp')
				map_sites.append('interactive-map-airmag-2DD-data.asp')
				map_sites.append('interactive-map-airmag-2DR-data.asp')
				map_sites.append('interactive-map-airmag-TF-data.asp')
				map_sites.append('interactive-map-gravity-BR-data.asp')
				map_sites.append('interactive-map-gravity-RBR-data.asp')
				map_sites.append('interactive-map-airborneVLFR-data.asp')
				map_sites.append('interactive-map-airborneVLFQR-data.asp')

				for sub_url in sub_sites:
				
					if any(x in sub_url for x in map_sites):
						# Bedrock GIS Data - DNR Maps
						sub_soup = bsoup.get_soup(sub_url)
						areas = sub_soup.find_all('area')

						for area_idx, area in enumerate(areas):
							msg = "Extracting %s of %s areas" \
									% (area_idx + 1, len(areas))
							shared.print_oneliner(msg)
							#print "Top page: " + str(sub_url)
							link = area['href']
							if not link == "#" and link.find('.pdf') == -1:
								area_url = urlparse.urljoin(sub_url, link)

								#print "area: " + str(area)

								rec_dict = self.get_gis_page(area_url)

								if rec_dict is None: continue

								for k, v in rec_dict.items():
									pt_csv.add(k, v)

								pt_csv.add('Source', "Nova Scotia's NATR GIS Pages")
								pt_csv.write_dataset()
						print
					elif sub_url.find('geochemistry.asp') > -1:
						# Get each ASP page from DIVs containing class 'ui-accordion-content'
						sub_soup = bsoup.get_soup(sub_url)

						accord_div = sub_soup.find_all('div', 
														attrs={'class': 
														'ui-accordion-content'})

						for idx, ds in enumerate(accord_div):
							msg = "Extracting %s of %s results" \
									% (idx + 1, len(accord_div))
							shared.print_oneliner(msg)
						
							# Find the anchor with text 'Find Out More'
							a = ds.find('a', text='Find Out More')
							link = a['href']
							sub_url = urlparse.urljoin(sub_url, link)

							rec_dict = self.get_gis_page(sub_url)

							if rec_dict is None: continue

							for k, v in rec_dict.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', "Nova Scotia's NATR GIS Pages")
							pt_csv.write_dataset()
						print
					elif sub_url.find('gis-data-maps-provincial.asp') > -1:
						sub_soup = bsoup.get_soup(sub_url)

						wrapper_div = sub_soup.find('div', attrs={'id': 'wrapper'})

						sub_blocks = wrapper_div.find_all('div', attrs={'class': 'block medium'})

						for idx, sub_block in enumerate(sub_blocks):
							msg = "Extracting %s of %s blocks" \
									% (idx + 1, len(sub_blocks))
							shared.print_oneliner(msg)
						
							a = sub_block.find('a')
							link = a['href']
							sub_url = urlparse.urljoin(sub_url, link)

							rec_dict = self.get_gis_page(sub_url)

							if rec_dict is None: continue

							for k, v in rec_dict.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', "Nova Scotia's NATR GIS Pages")
							pt_csv.write_dataset()
						print
					else:
						#print "Top Page: " + str()
						rec_dict = self.get_gis_page(sub_url)

						for k, v in rec_dict.items():
							pt_csv.add(k, v)

						pt_csv.add('Source', "Nova Scotia's NATR GIS Pages")
						pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Nova Scotia's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "MapServices_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		###########################################################################
		# Extract the Fletcher Map Services
		
		subpage = self.get_arg_val('subpage')

		url_list = self.pg_grp.get_url_list()

		#print "URL List: " + str(url_list)

		for url in url_list:

			if url.find('Geocortex') > -1:
				if subpage.lower() == 'arcgis': continue
				# my_rest = rest.PT_Geocortex(url)
				# my_sites = my_rest.get_sites()
				
				my_rest = services.PT_Geocortex(url)
				
				rest_data = my_rest.get_layers()
				
				for rec in rest_data:
					for k, v in rec.items():
						pt_csv.add(k, v)
						
					pt_csv.add('Source', "Nova Scotia's Map Services")
					pt_csv.write_dataset()

				pt_csv.write_dataset()
				
			else:
				
				if subpage.lower() == 'geocortex': continue
				
				#my_rest = rest.PT_REST(url)
				rest_serv = services.PT_REST(url)
				
				#rest_data = my_rest.extract_data()
				lyr_info = rest_serv.get_layers()
				
				if not self.check_result(lyr_info, url, 'ArcGIS REST Service'):
					continue
					
				filter_rows = shared.process_duplicates(lyr_info)
				
				for rec in filter_rows:
					for k, v in rec.items():
						pt_csv.add(k, v)
						
					pt_csv.add('Source', "Nova Scotia's Map Services")
					pt_csv.write_dataset()
					
				# #fletcher_url = self.pg_grp.get_url('fletcher_url')

				# my_rest = rest.PT_REST(url)
				# services = my_rest.get_services()

				# if services is None: continue

				# for service in services:

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
						# desc_str = shared.edit_description(desc_str, 'span')

					# # UPDATE FOR ESRI REST SERVICES
					# #   All services allow the following formats:
					# #       json (JavaScript Object Notation)
					# #       kmz (compressed KML, or Keyhole Markup Language)
					# #       lyr (layer file)
					# #       nmf (ArcGIS Explorer map file)
					# #       amf (Action Message Format)
					# formats = ['JSON', 'KMZ', 'LYR', 'NMF', 'AMF']
					# pt_csv.add('Available Formats', "|".join(formats))

					# # Get the service URL
					# serv_url = service['url']

					# # Get the spatial reference
					# proj_str = shared.get_spatialref(service)

					# pt_csv.add('Title', title_str)
					# pt_csv.add('Description', desc_str)
					# pt_csv.add('Type', serv_type)
					# pt_csv.add('Service URL', serv_url)
					# pt_csv.add('Access', 'Download using ESRI REST Service')
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

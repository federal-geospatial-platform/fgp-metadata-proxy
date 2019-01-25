import os
import sys
import urllib2
from bs4 import BeautifulSoup
import collections
import math
import csv
import json
import re
import urlparse
import time
import datetime
import inspect
import argparse
import traceback

# Get the shared.py
# script_file = os.path.abspath(__file__)
# script_folder = os.path.dirname(script_file)
# province_folder = os.path.dirname(script_folder)
# home_folder = os.path.dirname(province_folder)
# script_folder = home_folder + "\\scripts"
#
# sys.path.append(script_folder)
# import shared
# import access_rest as rest
# import page

import Main_Extractor as main_ext

from common import shared
from common import bsoup
from common import access_rest as rest
from common import services
from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	''' The Extractor class contains all the tools and methods to extract geospatial datasets
			from the various web pages and services from Alberta.
	'''

	def __init__(self):
		''' Initializer for the Extractor class. '''

		# Set the province
		self.province = 'Alberta'
		
		# Create the page groups dictionary
		self.page_groups = []
		self.page_groups = collections.OrderedDict()

		# Create the list for the page IDs of the MLI categories
		self.format_opts = collections.OrderedDict()
		self.format_opts['beyond 20-20'] = ['beyond+20%2F20', 'Beyond+20%2F20']
		self.format_opts['bin'] = ['BIN']
		self.format_opts['csv'] = ['CSV', '.csv']
		self.format_opts['doc'] = ['DOC']
		self.format_opts['docx'] = ['DOCX']
		self.format_opts['dwg'] = ['image%2Fvnd.dwg']
		self.format_opts['epub'] = ['application%2Fepub%2Bzip', 'epub']
		self.format_opts['fgdb'] = ['6GB+zipped+Esri+file+geodatabase+%28FGDB%29', 'GDB']
		self.format_opts['ftp'] = ['FTP', 'ftp']
		self.format_opts['gif'] = ['GIF']
		self.format_opts['gml'] = ['GML']
		self.format_opts['gridded data'] = ['Gridded+Data']
		self.format_opts['html'] = ['HTML']
		self.format_opts['http'] = ['HTTP', 'HTTPS']
		self.format_opts['ivt'] = ['IVT']
		self.format_opts['jpeg'] = ['JPEG']
		self.format_opts['json'] = ['JSON']
		self.format_opts['kml'] = ['KML']
		self.format_opts['link'] = ['LINK', 'link']
		self.format_opts['ms word'] = ['application%2Fmsword', 'MS+Word']
		self.format_opts['msi'] = ['application%2Fx-msi']
		self.format_opts['non-gis data'] = ['Non-GIS+Data']
		self.format_opts['odata'] = ['OData']
		self.format_opts['pdf'] = ['PDF']
		self.format_opts['ped'] = ['PED']
		self.format_opts['ppt'] = ['PPT']
		self.format_opts['pptx'] = ['PPTX']
		self.format_opts['shp'] = ['SHP']
		self.format_opts['tabular data'] = ['Tabular+Data']
		self.format_opts['tiff'] = ['TIFF']
		self.format_opts['txt'] = ['TXT']
		self.format_opts['url'] = ['URL']
		self.format_opts['wms'] = ['WMS']
		self.format_opts['xls'] = ['XLS', '.xls']
		self.format_opts['xlsx'] = ['XLSX', 'application%2Fvnd.ms-excel+%28xlsx%29']
		self.format_opts['xml'] = ['XML']
		self.format_opts['zip'] = ['ZIP']

		# Declare all the different types of page groups
		pg_grp = page_group.PageGroup('geodiscover', 'Alberta GeoDiscover')
		pg_grp.add_url('portal_url', 'https://geodiscover.alberta.ca/geoportal/rest/find/document')
		self.page_groups['geodiscover'] = pg_grp

		pg_grp = page_group.PageGroup('services', 'Alberta Map Services')
		pg_grp.add_url('rest_url', 'https://maps.alberta.ca/genesis/rest/services')
		pg_grp.add_url('geocortex_url', 'https://maps.alberta.ca/Geocortex/Essentials/4.6/REST/sites')
		pg_grp.add_url('services2_url', 'https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services')
		pg_grp.add_url('tiles_url', 'https://tiles.arcgis.com/tiles/jQV6VMr2Loovu7GU/arcgis/rest/services')
		self.page_groups['services'] = pg_grp

		pg_grp = page_group.PageGroup('maps', 'Alberta Interactive Maps')
		pg_grp.add_url('mins_url',
					'http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5')
		pg_grp.add_url('sands_url',
					'http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=d85fd3dd5daa424488bd82dfd9033846')
		pg_grp.add_url('radar_url',
					'http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=30e3bc42140f4979a9b2d7963e49c101')
		pg_grp.add_url('seismic_url',
					'http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=1b1efd0717c441f595dbfdba66d95217')
		self.page_groups['maps'] = pg_grp

		pg_grp = page_group.PageGroup('opendata', 'Alberta Open Government')
		pg_grp.add_url('main_url', 'https://open.alberta.ca/dataset')
		opts = {'format': self.format_opts.keys()}
		pg_grp.set_opts(opts)
		self.page_groups['opendata'] = pg_grp
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Set the arguments for this extractor
		self.argmt['word'] = main_ext.Ext_Arg('word', 
										methlst=['geodiscover', 'opendata'])
		self.argmt['start'] = main_ext.Ext_Arg('start', 0, methlst=['opendata'], 
									debug=True)
		self.argmt['format'] = main_ext.Ext_Arg('format', methlst=['opendata'])
		#self.argmt['xl'] = main_ext.Ext_Arg('xl', methlst=['fgp', 'portal'])
		
	def get_province(self):
		''' Gets the province name of the extractor.
		:return: The province name of the extractor.
		'''
		
		return self.province

	###################################################################################################################

	def get_format(self, format, name=''):
		''' Gets only the valid formats for the Open Data Catalogue.
		:param name: The name used to replace the format.
		:param format: The input format.
		:return: The proper format.
		'''
	
		valid_formats = ['JSON', 'CSV', 'XLS', 'XLSX', 'PDF', 'ZIP', 'SHP', 'TIFF', 
						'ASCII Grid', 'DOCX', 'WMS', 'KMZ', 'KML', 'REST', 'GDB']
	
		for v in valid_formats:
			if name.find(v) > -1:
				return name
				
		return format
	
	def get_download(self, url):
		''' Retrieves the download URL from a download web page in the GeoDiscover metadata
		:param url: The URL for the download page.
		:return: The download URL.
		'''
		sub_soup = bsoup.get_soup(url)
		
		# Write to error file if soup is None
		if sub_soup is None:
			self.write_error(url, 'GeoDiscover Metadata')
			return ''
		
		faqitems = sub_soup.find_all('div', attrs={'class': 'FAQItem'})
		for div in faqitems:

			td = bsoup.get_adjacent_cell(div, 'strong', 'Data Product Download')

			a = td.find('a')
			download_str = a['href']
			return download_str

	def get_xml_data(self, in_xml): #, category, return_type='value'):
		''' Retrieves the first value from an XML BeautifulSoup based on a list of tags.
			Ex: In the GeoDiscover Alberta metadata XML, the metadata type can be
				found in tags 'metstdn' or 'metadataStandardName'. This method will check
				both tags and return the first one with a value.
		:param in_xml: The BeautifulSoup XML object.
		:param tags: A list of tag options.
		:return: The first instance of a value in the XML.
		'''

		# If in_xml is None, return an empty string
		if in_xml is None: return ''
		
		mdata_info = collections.OrderedDict()
		
		######################################################################
		# Get metadata type
		mdata_keys = ['metstdn', 'metadataStandardName']
		mdata_standard = bsoup.find_xml_tags(in_xml, mdata_keys)
		mdata_standard = mdata_standard[0].text
		if mdata_standard.find('FGDC') > -1:
			self.mdata_type = 'FGDC'
		else:
			self.mdata_type = 'NAP'
		mdata_info['Metadata Type'] = mdata_standard
		
		######################################################################
		# Get the Title
		title_str = bsoup.find_xml_text(in_xml, 'title')
		mdata_info['Title'] = title_str
		
		######################################################################
		# Get the Description
		abstract = bsoup.find_xml_text(in_xml, 'abstract')
		purpose = bsoup.find_xml_text(in_xml, 'purpose')
		mdata_info['Description'] = '%s|%s' % (abstract, purpose)
		
		######################################################################
		# Get the Recent Date		
		if self.mdata_type == 'FGDC':
			mdata_info['Recent Date'] = bsoup.find_xml_text(in_xml, 'ModDate')
		else:
			mdata_info['Recent Date'] = bsoup.find_xml_text(in_xml, 'dateStamp')
		
		######################################################################
		# Get the Extents
		if self.mdata_type == 'FGDC':
			bounds_tags = bsoup.find_xml_tags(in_xml, 'spdom')
			#print "\nbounds_tags: %s" % bounds_tags
			if len(bounds_tags) == 0:
				mdata_info['Extents'] = ''
			else:
				bounds = bounds_tags[0]
				if not bounds == '':
					west = bounds.find('westbc').text
					east = bounds.find('eastbc').text
					north = bounds.find('northbc').text
					south = bounds.find('southbc').text
					
					ext = [north, south, east, west]
					mdata_info['Extents'] = shared.create_wkt_extents(ext)
		else:
			bounds_tags = bsoup.find_xml_tags(in_xml, \
											'EX_GeographicBoundingBox')
			#print "\nbounds_tags: %s" % bounds_tags
			if len(bounds_tags) == 0:
				mdata_info['Extents'] = ''
			else:
				bounds = bounds_tags[0]
				#print self.mdata_url
				#print bounds
				if not bounds == '':
					west = bsoup.find_xml_text(bounds, 'westBoundLongitude')
					east = bsoup.find_xml_text(bounds, 'eastBoundLongitude')
					north = bsoup.find_xml_text(bounds, 'northBoundLatitude')
					south = bsoup.find_xml_text(bounds, 'southBoundLatitude')
					
					ext = [north, south, east, west]
					mdata_info['Extents'] = shared.create_wkt_extents(ext)
		
		######################################################################
		# Get the Keywords
		if self.mdata_type == 'FGDC':
			kywrd_tags = bsoup.find_xml_tags(in_xml, 'keywords')
			keywords = [tag.text for tag in kywrd_tags[0].find_all('themekey')]
			mdata_info['Keywords'] = ', '.join(keywords)
		else:
			kywrd_tags = bsoup.find_xml_tags(in_xml, 'MD_Keywords')
			keywords = [tag.text for tag in kywrd_tags[0].find_all('keyword')]
			mdata_info['Keywords'] = ', '.join(keywords)
			
		######################################################################
		# Get the Spatial Reference
		if self.mdata_type == 'FGDC':
			hdatum = bsoup.find_xml_tags(in_xml, 'horizdn')
			if hdatum == 'North American Datum of 1983':
				hdatum = 'NAD 83'
			ellipsoid = bsoup.find_xml_tags(in_xml, 'ellips')
			mdata_info['Spatial Reference'] = "%s %s" % (ellipsoid, hdatum)
		else:
			#print self.mdata_url
			
			# Check to see if there is a 'referenceSystemIdentifier' in the
			#	metadata
			ref_id = in_xml.find('referenceSystemIdentifier')
			if ref_id is None:
				ref_id = in_xml.find('referencesystemidentifier')
			
			if ref_id is None:
				refsys_lst = in_xml.find_all('referenceSystemInfo')
				if len(refsys_lst) == 0:
					refsys_lst = in_xml.find_all('referencesysteminfo')
				for r in refsys_lst:
					if r.has_attr('xlink:title'):
						refsys = r['xlink:title']
						if refsys == 'North American Datum 1983':
							hdatum = 'NAD 83'
						elif refsys == 'Geodetic Reference System 1980':
							ellipsoid = refsys
						print refsys
				mdata_info['Spatial Reference'] = "%s %s" % (ellipsoid, hdatum)
			else:
				code = bsoup.find_xml_tags(ref_id, 'code')
				if not len(code) == 0:
					code_val = code[0].text
					sp = "EPSG: %s" % code_val.replace("EPSG:", "")
				else:
					sp = ''
				mdata_info['Spatial Reference'] = sp
			
		######################################################################
		# Get the Download information
		if self.mdata_type == 'FGDC':
			download_url = bsoup.find_xml_text(in_xml, 'onlink')
		else:
			download_url = bsoup.find_xml_text(in_xml, 'linkage')
			
		webmap_url = ''
		access = ''
		download_str = ''
		if download_url.find('.aspx') > -1:
			download_str = 'No'
			# See if there is another page which contains the download
			if download_url.find('hydrological.aspx') > -1:
				# Alberta ArcHydro Phase 2 Data
				download_str = self.get_download(download_url)
			elif download_url.find('default.aspx') > -1:
				# Catalogue default page
				sub_soup = bsoup.get_soup(download_url)
				# Write to error file if sub_soup is None
				if sub_soup is None:
					self.write_error(download_url, 'GeoDiscover Download URL')
				else:
					div = sub_soup.find('div', attrs={'class': 'box note'})
					a_list = div.find_all('a')
					for a in a_list:
						if a.text.strip() == title_str.strip():
							link = a['href']
							url = urlparse.urljoin(download_url, link)
							download_str = self.get_download(url)
			if download_str is None or download_str == '':
				download_str = 'No'
		elif download_url.find('www.esri.com') > -1:
			# If the link is an ESRI link, then no downloads are available
			download_str = 'No'
			access = 'Contact the Province'
		elif download_url.find('deptdocs.nsf') > -1:
			# If the link includes 'deptdocs.nsf', then there are multiple downloads
			download_str = 'Multiple Downloads'
			access = 'Download/Web Accessible'
		elif download_url.find('ags.aer') > -1 and download_url.find('.zip') == -1:
			# If the link contains 'ags.aer' and not '.zip', the download can be
			#    found in the 'linkage' tag under 'transferOptions'.
			transferOptions = in_xml.find('transferOptions')
			download_url = bsoup.find_xml_text(transferOptions, 'linkage')
		elif download_url.lower().find('viewer') > -1:
			# If the link contains 'viewer', then it is a web map and not a download
			download_str = 'No'
			access = 'Viewable/Contact the Province'
			webmap_url = download_url
		elif download_url == '':
			# If the link is empty, there is no download
			download_str = 'No'
			access = 'Contact the Province'
		else:
			# If a single download exists
			download_str = download_url
			access = 'Download/Web Accessible'
			
		mdata_info['Download'] = download_str
		mdata_info['Access'] = access
		mdata_info['Web Map URL'] = webmap_url
			
		######################################################################
		# Get the Formats
		formats = []
		if self.mdata_type == "NAP":
			md_formats = in_xml.find_all('MD_Format')
			
			for md_f in md_formats:
				# Get the formats from the MD_Formats first
				format = bsoup.get_text(md_f.find('name'))
				
				if format.lower() == 'html' or \
					format.lower() == 'xml':
					continue
				
				format = self.get_format(format)
				
				formats.append(format)
				
			if len(formats) == 0:
				# Get a list of resources
				resources = in_xml.find_all('CI_OnlineResource')
				
				#print "resources: %s" % len(resources)
				#print mdata_xml_url
				
				#formats = []
				for res in resources:
					
					#print res
					#print type(res)
					
					format = bsoup.get_text(res.find('name'))
					
					if format.lower() == 'html' or \
						format.lower() == 'xml':
						continue
					
					format = self.get_format(format)
					
					formats.append(format)
				
			formats = list(set(formats))
			
		mdata_info['Available Formats'] = '|'.join(formats)

		######################################################################
		# Get the Service Name, Type and URL, if applicable
		serv_name = ''
		if download_url.find('Server') > -1:
			# If the download link leads to a map service
			download_str = 'Multiple Downloads'
			access = 'Download/Web Accessible'

			serv_url = download_url
			#formats = ['KMZ', 'LYR', 'NMF', 'AMF']
			#format_str = '|'.join(formats)
			my_rest = rest.MyREST(serv_url)
			serv_json = my_rest.get_root_json()

			if serv_json is not None:

				#for k, v in serv_json.items():
				#	print "%s: %s" % (k, v)

				if 'mapName' in serv_json.keys():
					serv_name = serv_json['mapName']
				serv_type = os.path.basename(serv_url)
			else:
				serv_type = ''
		else:
			serv_url = ''
			serv_type = ''
			
		mdata_info['Service Name'] = serv_name
		mdata_info['Service URL'] = serv_url
		mdata_info['Service'] = serv_type
		
		######################################################################
		# Get the Data Type
		if self.mdata_type == 'FGDC':
			data_type = bsoup.find_xml_text(in_xml, 'geoform')
		else:
			data_type = bsoup.find_xml_text(in_xml, \
										'MD_SpatialRepresentationTypeCode')
		mdata_info['Type'] = data_type
		
		######################################################################
		# Get the License
		if self.mdata_type == 'FGDC':
			lic_val = bsoup.find_xml_text(in_xml, 'fees')
		else:
			lic_val = bsoup.find_xml_text(in_xml, 'useLimitation')
		
		#print "lic_val: %s" % lic_val
		
		if lic_val == '0':
			licence = 'Free'
		elif len(lic_val) > 100:
			licence = shared.edit_description(lic_val)
		else:
			licence = lic_val
		mdata_info['Licensing'] = licence
		
		######################################################################
		# Get the Publisher
		if self.mdata_type == 'FGDC':
			publisher = bsoup.find_xml_text(in_xml, 'publish')
		else:
			publisher = bsoup.find_xml_text(in_xml, 'organisationName')
		mdata_info['Publisher'] = publisher
		
		return mdata_info
		
		# # If tags is a string, convert it to a single item list
		# if isinstance(tags, str):
			# tags = [tags]

		# mdata_val = ''
		# # Cycle through each tag and retrieve the first value
		# for tag in tags:
			# if mdata_val == '':
				# mdata_tag = in_xml.find(tag)
				# if mdata_tag is None:
					# mdata_tag = in_xml.find(tag.lower())
					# if mdata_tag is None:
						# continue
				# if return_type == 'tags':
					# mdata_val = mdata_tag
				# else:
					# mdata_val = mdata_tag.text
					# mdata_val = mdata_val.strip()
				
		# return mdata_val

	def extract_geodiscover(self): #, word=None):
		''' Method to extract all geospatial data from the GeoDiscover Alberta geoportal.
			:param word: The word which will be used to query the portal.
		'''

		# Extract the Alberta GeoDiscover

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "GeoDiscover_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		self.print_title("Extracting Alberta's GeoDiscover geoportal")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the service url
		portal_url = self.pg_grp.get_url('portal_url')

		# Set the parameters for the URL query
		word = self.argmt['word'].get_value()
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['searchText'] = word
		params['max'] = '5000'
		params['f'] = 'pjson'
		params['contentType'] = 'downloadableData,offlineData'

		# Build the URL query
		query_url = shared.get_post_query(portal_url, params)
		
		#print query_url
		
		#answer = raw_input("Press enter...")

		self.print_log("URL: %s" % query_url)

		# Add the JSON text to JSON object
		json_results = shared.get_json(query_url)
		
		# If json_results is None
			
		if not self.check_result(json_results, query_url, 
			"Alberta GeoDiscover JSON Results"): return None

		# Get a list of the results
		records = json_results['records']

		print "Number of results: " + str(len(records))
		
		print

		for idx, rec in enumerate(records):

			msg = "Extracting record %s of %s records" % (idx + 1, len(records))
			shared.print_oneliner(msg)
			
			if idx == 10:
				shared.estimate_time(start_time, len(records))

			# Get the ID to build URLs
			if 'id' in rec:
				id = rec['id']
			else:
				id = ''

			# # Get the title
			# if 'title' in rec:
				# title_str = rec['title']
			# else:
				# title_str = ''

			# # Get the date
			# if 'updated' in rec:
				# recdate_str = rec['updated']
			# else:
				# recdate_str = ''

			# # Get the description
			# if 'summary' in rec:
				# desc_str = rec['summary']
			# else:
				# desc_str = ''

			# Get the full metadata URL
			mdata_url = 'https://geodiscover.alberta.ca/geoportal/catalog/search/resource/' \
						'fullMetadata.page?uuid=%s' % id

			# Build the metadata URL
			mdata_xml_url = 'https://geodiscover.alberta.ca/geoportal/csw?getxml=%s' % id

			# Build the JSON URL
			data_url = 'https://geodiscover.alberta.ca/geoportal/rest/document?f=pjson&id=%s' % id
			
			##################################################################
			# The following is using standard XML soup
			
			# Open the metadata page
			mdata_xml_soup = bsoup.get_xml_soup(mdata_xml_url)
			
			#mdata_f = open('mdata.xml', 'w')
			#mdata_f.write(str(mdata_xml_soup))
			#mdata_f.close()
			
			self.mdata_url = mdata_xml_url

			# If the metadata XML page only contains the first line, open it using selenium
			mdata_split = str(mdata_xml_soup).split('\n')
			if len(mdata_split) < 3:
				mdata_xml_soup = bsoup.get_xml_soup(mdata_xml_url, selenium=True)
				
			if mdata_xml_soup is None:
				print "\nWARNING: GeoDiscover XML metadata page '%s' could not be opened." % mdata_xml_url
				print "Please check the 'err_log.csv' file in the province/territory results folder."
				self.write_error(mdata_xml_url, 'Alberta GeoDiscover XML Metadata', 'Page could not be opened.')
				continue
				
			if not self.check_result(mdata_xml_soup, mdata_xml_url, 
				"Alberta GeoDiscover XML Metadata"): continue
				
			#print
			#print mdata_xml_url
			#answer = raw_input("Press enter...")
			
			# Get the metadata info
			mdata_info = self.get_xml_data(mdata_xml_soup)

			#print mdata_info
			#answer = raw_input("Press enter...")
			
			if self.debug:
				print "\nTitle: %s" % title_str
				print "Description: %s" % desc_str
				print 'Recent Date: %s' % recdate_str
				print 'Licensing: %s' % licence
				print 'Publisher: %s' % pub_str
				print 'Access: %s' % access
				print 'Service URL: %s' % serv_url
				print 'Service Name: %s' % serv_name
				print 'Service: %s' % serv_type
				print 'Type: %s' % dtype
				print 'Data URL: %s' % mdata_xml_url
				print 'Web Map URL: %s' % webmap_url
				print 'Download: %s' % download_str
				print 'Metadata URL: %s' % mdata_url
				print 'Metadata Type: %s' % mdata_standard
				print 'Available Formats: %s' % '|'.join(formats)
				print 'Spatial Reference: %s' % sp
				#answer = raw_input("Press enter...")
				
			for k, v in mdata_info.items():
				pt_csv.add(k, v)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Alberta GeoDiscover')
			pt_csv.add('Data URL', mdata_xml_url)
			pt_csv.add('Metadata URL', mdata_url)
			
			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		print
		
		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		''' Method to extract all interactive maps for Alberta.'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Alberta's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		url_list = self.pg_grp.get_url_list()

		#print "URL List: " + str(url_list)

		# Cycle through each interactive URL
		for idx, url in enumerate(url_list):
			msg = "Extracting %s of %s maps" % (idx, len(url_list))
			shared.print_oneliner(msg)
		
			# Convert the URL to ArcGIS data
			#data_url = shared.get_arcgis_url(url)

			#print data_url
			
			#answer = raw_input("Press enter...")
			
			arcgis_info = shared.get_arcgis_data(url)
			
			# Check if arcgis_info can be opened
			err_txt = 'ArcGIS map could not be opened.'
			if not self.check_result(arcgis_info, url, 
									'ArcGIS Map', err_txt):
				continue
			
			for k, v in arcgis_info.items():
				pt_csv.add(k, v)
				
			# Add all values to the CSV file
			pt_csv.add('Source', 'Alberta ArcGIS Maps')
			pt_csv.add('Access', 'Viewable/Map Service')
			pt_csv.add('Download', 'No')
			pt_csv.add('Web Map URL', url)

			# # Get the information from the service URL
			# data_json = shared.get_json(data_url)
			
			# # If json_results is None
			# if not self.check_result(data_json, data_url, 
				# "Interactive Map JSON Results", 'Page could not be opened.'): continue

			# # Extract values from the JSON
			# title_str = data_json['title']
			# creadate = data_json['created']
			# creadate_str = shared.translate_date(creadate)
			# moddate = data_json['modified']
			# moddate_str = shared.translate_date(moddate)
			# dtype = data_json['type']
			# desc_str = shared.edit_description(data_json['description'])
			# sp = data_json['spatialReference']

			# # Add all values to the CSV file object
			# pt_csv.add('Source', 'Alberta Interactive Maps')
			# pt_csv.add('Title', title_str)
			# pt_csv.add('Description', desc_str)
			# pt_csv.add('Web Map URL', url)
			# pt_csv.add('Data URL', data_url)
			# pt_csv.add('Type', dtype)
			# pt_csv.add('Start Date', creadate_str)
			# pt_csv.add('Recent Date', moddate_str)
			# pt_csv.add('Access', 'Viewable/Contact the Province')
			# pt_csv.add('Download', 'No')
			# pt_csv.add('Spatial Reference', sp)
			# #pt_csv.add('Metadata URL', mdata_url)

			# Write the dataset to the CSV file
			pt_csv.write_dataset()
		
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_opendata(self): #, word=None, format=None, start='0'):
		''' Method to extract data from Alberta's open data catalogue.
			:param word: The word which will be used to query the catalogue.
			:param format: The format type to search for.
		'''

		# Extract the Alberta Open Government data

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Alberta's Open Data Catalogue")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# Get the parameters
		word = self.argmt['word'].get_value()
		format = self.argmt['format'].get_value()
		start = self.argmt['start'].get_value()

		# Create the CSV file for the geospatial data
		csv_fn = "OpenData_Geo_results"
		geo_csv = sh.PT_CSV(csv_fn, self)
		geo_csv.open_csv()

		# Create the CSV file for all other data
		csv_fn = "OpenData_Other_results"
		other_csv = sh.PT_CSV(csv_fn, self)
		other_csv.open_csv()

		# Get the service url
		opendata_url = self.pg_grp.get_url('main_url')

		self.print_log("URL: %s" % opendata_url)

		query_list = []
		# Set the parameters for the URL query
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['q'] = word  # word is the search word
		params['dataset_type'] = "opendata"

		if format is not None and not format.lower() == 'all':
			# Determine the proper URL string for the format query
			if format.lower() in self.format_opts.keys():
				url_forms = self.format_opts[format.lower()]
				for form in url_forms:
					params['res_format'] = form
					query_url = shared.get_post_query(opendata_url, params)
					query_list.append(query_url)
			else:
				# If the specified format doesn't exist, run with no format filter
				query_url = shared.get_post_query(opendata_url, params)
				query_list.append(query_url)
		else:
			# If no format is specified or the format is 'all', run with no format filter
			query_url = shared.get_post_query(opendata_url, params)
			query_list.append(query_url)

		for query_url in query_list:
		
			# Get the soup for the query page results
			soup = bsoup.get_soup(query_url)
			
			# If soup is None
			if soup is None:
				print "\nWARNING: Open catalogue page '%s' could not be opened." % query_url
				self.write_error(query_url, 'Open Catalogue Page', 'Open catalogue page could not be opened.')
				continue
				
			if not self.check_result(soup, query_url, 
				"Alberta Open Catalogue Page"): continue

			# Get the page count
			page_count = bsoup.get_page_count(soup, 'div', ['class', 'pagination'], 'li')

			#print "page_count: %s" % page_count

			# Used for displaying the percentage of records during processing
			prev_perc = -1
			record_count = 0
			special_chr = ""
			record_total = page_count * 10
			
			# Determine the approximate starting position
			page_start = int(start) / 10

			time_count = 0.0

			record = page_start * 10
			for page in range(page_start, page_count):
			
				# Start time used to estimate the total length of time
				if time_count == 0.0:
					start_time = datetime.datetime.now()
			
				# Open each iteration of pages:
				if special_chr == "":
					# Some of the search entries can include "&" character
					#	but if an error is returned, use the "?" character instead
					try:
						page_url = "%s&page=%s" % (query_url, page + 1)
						special_chr = "&"
					except:
						page_url = "%s?page=%s" % (query_url, page + 1)
						special_chr = "?"
				else:
					page_url = "%s%spage=%s" % (query_url, special_chr, page + 1)

				# Create the soup object of the current page
				page_soup = bsoup.get_soup(page_url, silent=True)
				
				# If the page_soup is None
				if page_soup is None:
					print "\nWARNING: Open catalogue page '%s' could not be opened." % page_url
					self.write_error(page_url, 'Open Catalogue Page', 'Open catalogue page could not be opened.')
					continue
					
				if not self.check_result(page_soup, page_url, 
					"Alberta Open Catalogue Page"): continue

				# Get all the datasets on the current page (all datasets are in a 'div' with class 'dataset-item')
				results = page_soup.find_all('div', attrs={'class': 'dataset-item'})

				# Let the user know if there are no records
				if len(results) == 0 and record_count == 0:
					print "No records exist with the given search parameters."
					print "URL query sample: %s" % query_url
					return None
					
				##########################################################
				# Process using metadata web page

				# Cycle through each result
				for res in results:
					record += 1
					msg = "Extracting %s of approximately %s results from '%s'" % (record, record_total, query_url)
					shared.print_oneliner(msg)

					# Used to determine if the result is geospatial or not
					geo_data = False

					# Get the title of the dataset
					title_res = res.find('h3', attrs={'class': 'package-header'})
					title_str = title_res.a.string
					if title_str is None:
						title_str = ''
						
					#print page_url
					
					#answer = raw_input("Press enter...")

					# Get the URL of the dataset
					ds_url = urlparse.urljoin(page_url, title_res.a['href'])
					if ds_url is None:
						ds_url = ''
						
					#print ds_url

					# Get the available data formats
					# button_list = res.find_all('a', attrs={'class': 'btn'})
					# data_formats = []
					# for but in button_list:
						# if but.has_attr('data-format'):
							# data_format_str = but.string
							# if data_format_str is not None: data_format_str = data_format_str.encode('utf-8')
							# data_formats.append(str(data_format_str))
							
					#print res

					# Get the last modified date
					#date_res = res.find('h5', text='Last Modified').parent
					date_res = bsoup.find_tags_containing(res, 'Last Modified').parent
					datemod_str = date_res.find_next_sibling('div').p.string
					if datemod_str is None:
						datemod_str = ''
						
					
					#issdate_res = res.find('h5', text='Date Issued').parent

					# Get more in depth info by loading the dataset's URL
					ds_soup = bsoup.get_soup(ds_url, silent=True)
					
					print ds_url
					
					# If the page_soup is None
					# if ds_url is None:
						# print "\nWARNING: Open catalogue dataset result page '%s' could not be opened." % page_url
						# self.write_error(page_url, 'Open Catalogue Page', 'Open catalogue dataset result page could not be opened.')
						# continue
						
					if not self.check_result(ds_soup, ds_url, "Alberta's Open Data Catalogue"): continue
					
					# Get the issue date
					dateiss_str = ''
					issdate_res = bsoup.find_tags_containing(ds_soup, 'Date Issued')
					if issdate_res is not None:
						#issdate_res.parent
						dateiss_str = bsoup.get_text(issdate_res.find_next_sibling('p'))
						
					#print ds_soup
					#answer = raw_input("Press enter...")
						
					# Get the issue date
					freq_str = ''
					freq_res = bsoup.find_tags_containing(ds_soup, 'Update Frequency')
					if freq_res is not None:
						#freq_res.parent
						freq_p = freq_res.find_next_sibling('p')
						#print freq_p
						#answer = raw_input("Press enter...")
						freq_str = bsoup.get_text(freq_p)
					
					# Determine the download link based on the number of download anchors
					# Find the anchor with text 'Download'
					res_sect = ds_soup.find('section', attrs={'id': 'dataset-resources'})
					li_list = res_sect.find_all('li')
					download_alist = []
					for li in li_list:
						anchors = li.find_all('a')
						download_a = anchors[1]
						download_alist.append(download_a)

					# Now determine the download text and access type
					if len(download_a) == 0:
						# If no download exists
						download_str = 'No'
						access_str = 'Contact the Province'
					elif len(download_a) == 1:
						# Find the anchor with text 'Download'
						download_str = download_a['href']
						access_str = 'Download/Web Accessible'
					else:
						# If multiple downloads exist
						download_str = 'Multiple Downloads'
						access_str = 'Download/Web Accessible'
						
					# Get the formats
					formats = []
					resources = ds_soup.find_all('li', attrs={'class': 'resource-item'})
					#print resources
					for res in resources:
					
						if bsoup.get_text(res.h3).find('HTML') > -1 or \
							bsoup.get_text(res.h3).find('XML') > -1:
							continue
						
						# Get the More Information link and open it
						button = bsoup.find_tags_containing(res, 'More information', 'a')
						
						if button is None: continue
						
						#print "\nds_url: %s" % ds_url
						#print button
						
						info_url = shared.get_anchor_url(button, ds_url)
						
						print "info_url: '%s'" % info_url
						answer = raw_input("Press enter...")
						
						info_soup = bsoup.get_soup(info_url)
						
						if not self.check_result(info_soup, info_url, 'Alberta Open Data'): continue
						
						# Locate the format
						format_th = bsoup.find_tags_containing(info_soup, 'Format', 'th')
						format = bsoup.get_text(format_th.find_next_sibling('td'))
						
						if format.lower() == 'html' or format.lower() == 'xml':
							continue
							
						#print format
						
						#answer = raw_input("Press enter...")
						
						formats.append(format)
					
						#date_str = res['date_published']
						#dates.append(date_str)
						
					#answer = raw_input("Press enter...")
						
					formats = list(set(formats))

					# Get the description
					desc_res = ds_soup.find('h5', text='Description').find_next_sibling('p')
					desc_str = desc_res.string

					# Get the alternative title
					if title_str == '':
						alt_res = ds_soup.find('h5', text='Alternative Title')
						if alt_res is not None:
							alt_sib = alt_res.find_next_sibling('p')
							alt_str = alt_sib.string
							if alt_str is not None:
								# alt_str = alt_str.encode('utf-8')
								title_str = alt_str

					# Get the publisher
					publish_res = ds_soup.find('h5', text='Publisher')
					if publish_res is not None:
						pub_sib = publish_res.find_next_sibling('p')
						publish_str = pub_sib.string
						if publish_str is None:
							publish_str = ''
						else:
							publish_str = publish_str.strip()
					else:
						publish_str = ""

					# This section is not used since the data only provides
					#   extents coverage instead of an actual spatial reference.
					# Get the spatial coverage
					# coverage_res = ds_soup.find('h5', text='Spatial Coverage')
					# if coverage_res is not None:
					#     geo_data = True
					#     coverage_sib = coverage_res.find_next_sibling('p')
					#     coverage_str = coverage_sib.a.string
					#     if coverage_str is None:
					#         coverage_str = ''
					# else:
					#     coverage_str = ''
					#
					# sp_str = coverage_str.strip()

					if geo_data:
						# Add all geospatial data to the geo_csv
						geo_csv.add('Source', 'Alberta Open Data Catalogue')
						geo_csv.add('Title', title_str)
						geo_csv.add('Description', desc_str)
						geo_csv.add('Access', access_str)
						geo_csv.add('Download', download_str)
						#geo_csv.add('Spatial Reference', sp_str
						geo_csv.add('Web Page URL', ds_url)
						geo_csv.add('Start Date', dateiss_str)
						geo_csv.add('Recent Date', datemod_str)
						geo_csv.add('Update Frequency', freq_str)
						geo_csv.add('Publisher', publish_str)
						geo_csv.add('Available Formats', "|".join(formats))

						geo_csv.write_dataset()
					else:
						# Add all other data to the other_csv
						other_csv.add('Source', 'Alberta Open Data Catalogue')
						other_csv.add('Title', title_str)
						other_csv.add('Description', desc_str)
						other_csv.add('Access', access_str)
						other_csv.add('Download', download_str)
						other_csv.add('Web Page URL', ds_url)
						other_csv.add('Start Date', dateiss_str)
						other_csv.add('Recent Date', datemod_str)
						other_csv.add('Update Frequency', freq_str)
						other_csv.add('Publisher', publish_str)
						other_csv.add('Available Formats', "|".join(formats))

						other_csv.write_dataset()

					record_count += 1

				# Estimate the total time based on the access time of the first record
				if time_count == 0.0:
					end_time = datetime.datetime.now()
					total_time = end_time - start_time
					total_secs = total_time.total_seconds()

					time_count = total_secs * page_count

					mins = time_count / 60
					mins_int = int(mins)

					secs = (mins - mins_int) * 60

					print "\nTotal estimated time: %s minutes & %s seconds" % (mins_int, secs)
				print
		geo_csv.close_csv()
		other_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self):
		''' Method to extract all Alberta maps services.'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Alberta's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "MapServices_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		##################################################################
		# Extract the Alberta ESRI REST Services

		# Get the service url
		rest_url = self.pg_grp.get_url('rest_url')

		self.print_log("URL: %s" % rest_url)

		# Get a list of REST services
		rest_serv = services.MyREST(rest_url)
		
		lyr_info = rest_serv.get_layers()
		
		shared.output_json(lyr_info, 'all_data.json')
		
		print "\nNumber of layers: %s" % len(lyr_info)
		
		#dup_ids = shared.find_duplicates(lyr_info)
		
		#merged_lyrs = shared.merge_duplicates(lyr_info, dup_ids)
		
		filtered_rows = shared.process_duplicates(lyr_info)
		
		shared.output_json(filtered_rows, 'filtered_data.json')
		
		#print merged_lyrs
		
		# for lyr in merged_lyrs:
		#    print lyr
		
		print "\nNumber of final layers: %s" % len(filtered_rows)
		
		for index, rec in enumerate(filtered_rows):
			for k, v in rec.items():
				pt_csv.add(k, v)

			pt_csv.add('Source', 'Alberta Map Services')
			pt_csv.write_dataset()
			
		#if len(layers) == 0:
				
		
		answer = raw_input("Press enter...")

		# Get the first service data and add it to the CSV file
		#serv_data = my_rest.extract_data()
		
		#rest_serv.get_data()
		
		# if self.check_result(serv_data, rest_url, "ArcGIS REST Map", 
							# 'Page could not be opened.'):
			# for index, rec in enumerate(serv_data):
				# shared.print_oneliner("Adding %s of %s to CSV inventory" \
										# % (index + 1, len(serv_data)))
				# for k, v in rec.items():
					# pt_csv.add(k, v)

				# pt_csv.add('Source', 'Alberta Map Services')
				# pt_csv.write_dataset()

		yo = True
		if not yo:
			# Get a list of the services2 services
			services2_url = self.pg_grp.get_url('services2_url')
			serv2_rest = rest.MyREST(services2_url)

			# Get the second service data and add it to the CSV file
			serv2_data = serv2_rest.extract_data()
			if self.check_result(serv2_data, services2_url, "ArcGIS REST Map", 'Page could not be opened.'):
				for index, rec in enumerate(serv2_data):
					shared.print_oneliner("Adding %s of %s to CSV inventory" % (index + 1, len(serv2_data)))
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', 'Alberta Map Services')
					pt_csv.write_dataset()

			# Get a list of the tiles services
			tiles_url = self.pg_grp.get_url('tiles_url')
			tiles_rest = rest.MyREST(tiles_url)

			# Get the tiles service data and add it to the CSV file
			tiles_data = tiles_rest.extract_data()
			if self.check_result(tiles_data, tiles_url, "ArcGIS REST Map", 'Page could not be opened.'):
				for index, rec in enumerate(tiles_data):
					shared.print_oneliner("Adding %s of %s to CSV inventory" % (index + 1, len(tiles_data)))
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', 'Alberta Map Services')
					pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

def main():
	#tool_list = ['REST', 'OpenData', 'GeoDiscover']

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
		word = args.word
		formats = args.format
		silent = args.silent

		if page is None:
			answer = raw_input("Please enter the page you would like to use (%s or all): " % ', '.join(pages.keys()))
			if not answer == "":
				page = answer.lower()
			else:
				print "\nERROR: Please specify a tool."
				print "Exiting process."
				sys.exit(1)

		page = page.lower()

		# print page

		ext.set_page(page)
		ext.run()

	except Exception, err:
		ext.print_log('ERROR: %s\n' % str(err))
		ext.print_log(traceback.format_exc())
		ext.close_log()


if __name__ == '__main__':
	sys.exit(main())

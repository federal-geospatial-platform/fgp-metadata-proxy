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
import inspect
import argparse
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
from common import services
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	def __init__(self):
		''' Initializer for the Extractor class. '''

		# Set up the initial parameters
		self.province = 'Manitoba'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []

		# Create the list for the page IDs of the MLI categories
		self.mli_opts = collections.OrderedDict()
		self.mli_opts['Administrative Boundaries'] = 'admin'
		self.mli_opts['Base Maps'] = 'maps'
		self.mli_opts['Environment'] = 'environ'
		self.mli_opts['Geographical Names'] = 'names'
		self.mli_opts['Land Use/Cover Maps'] = 'land'
		self.mli_opts['Transportation'] = 'transport'
		self.mli_opts['Cadastral'] = 'cadast'
		self.mli_opts['Digital Elevation Models'] = 'dem'
		self.mli_opts['Digital Imagery'] = 'image'
		self.mli_opts['Forest Inventory'] = 'forest'
		self.mli_opts['Geology Mapping'] = 'geol'
		self.mli_opts['Hydrography'] = 'hydro'
		self.mli_opts['Municipal Maps'] = 'munic'
		self.mli_opts['Quarter Section Grids'] = 'grids'
		self.mli_opts['Soil Classification'] = 'soil'
		self.mli_opts['Spatial Referencing'] = 'spatref'
		self.mli_opts['Topographic Maps'] = 'topos'
		self.mli_opts['Town & Village Plans'] = 'towns'
		
		####################################################################
		# Create Services page group
		
		srv_grp = main_ext.PageGroup('services', "Manitoba Services")
		
		# No arguments to add
		
		# Add URLs
		srv_grp.add_url('petrol_url', 'http://maps.gov.mb.ca/arcgis/rest/services/MG_PETROLEUM_CLIENT/MapServer')
		srv_grp.add_url('rest_url', 'https://services.arcgis.com/mMUesHYPkXjaFGfS/ArcGIS/rest/services')
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create MLI page group

		mli_grp = main_ext.PageGroup('mli', "Manitoba Land Initiative")
		
		# Add arguments
		sb_arg = mli_grp.add_arg('subpage', default='all', debug=True)
		for k, v in self.mli_opts.items():
			sb_arg.add_opt(k, url_tags=[v])
		
		# Add URLs
		mli_grp.add_url('main_url', 'http://mli2.gov.mb.ca/mli_data/index.html')
		
		# Add to Extractor's page group list
		self.page_groups.append(mli_grp)
		
		
		####################################################################
		# Create Misc page group

		misc_grp = main_ext.PageGroup('misc', "Miscellaneous Web Pages")
		
		# No arguments to add
		
		# Add URLs
		misc_grp.add_url('petrol_url', 'http://www.manitoba.ca/iem/petroleum/gis/index.html')
		misc_grp.add_url('fire_url', 'http://www.gov.mb.ca/sd/fire/Fire-Maps/')
		misc_grp.add_url('fireidx_url', 'http://www.gov.mb.ca/sd/fire/Fire-Maps/fireview/')
		
		# Add to Extractor's page group list
		self.page_groups.append(misc_grp)
		
		
		####################################################################
		# Create DEM page group

		dem_grp = main_ext.PageGroup('dem', "DEMSM Downloads and Ordering")
		
		# No arguments to add
		
		# Add URLs
		dem_grp.add_url('main_url', 'http://www.gov.mb.ca/iem/geo/demsm/downloads.html')
		dem_grp.add_url('specs_url', 'http://www.gov.mb.ca/iem/geo/demsm/doispecs.html')
		dem_grp.add_url('mdata_url', 'http://www.gov.mb.ca/iem/geo/demsm/metadata.html')
		
		# Add to Extractor's page group list
		self.page_groups.append(dem_grp)
		
		
		####################################################################
		# Create Maps page group
		
		map_grp = main_ext.PageGroup('maps', "Manitoba Interactive Maps")
		
		# No arguments to add
		
		# Add URLs
		map_grp.add_url('petrol_url', ('http://www.manitoba.ca/iem/petroleum/gis/index.html',
								   'https://web33.gov.mb.ca/mapgallery/mgp.html',
								   'http://maps.gov.mb.ca/arcgis/rest/services/MG_PETROLEUM_CLIENT/MapServer'))
		map_grp.add_url('drought_url', 'http://www.gov.mb.ca/sd/waterstewardship/water_info/drought/index.html')
		map_grp.add_url('drink_url',
					'http://www.gov.mb.ca/sd/waterstewardship/odw/public-info/boil-water/water_advisories_in_mb.html')
		map_grp.add_url('weather_url', ('http://www.gov.mb.ca/sd/fire/Wx-Display/weatherview/weatherview.html',
									'http://www.gov.mb.ca/sd/fire/Wx-Display/weatherview/data/wx_last48.csv'))
		map_grp.add_url('fireview_url', ('http://www.gov.mb.ca/sd/fire/Fire-Maps/fireview/fireview.html',
									 'http://www.gov.mb.ca/sd/fire/Fire-Maps/'))
		map_grp.add_url('restrict_url', 'http://www.gov.mb.ca/sd/fire/Restrictions/index.html')
		map_grp.add_url('wild_url', ('http://www.gov.mb.ca/sd/wildlife/habcons/wmas/index.html',
								 'http://www.gov.mb.ca/sd/wildlife/habcons/wmas/gMap/index.html'))
		map_grp.add_url('beach_url', ('http://www.gov.mb.ca/sd/waterstewardship/quality/beaches.html',
								  'http://www.gov.mb.ca/sd/waterstewardship/quality/beach_table.html'))
		
		# Add to Extractor's page group list
		self.page_groups.append(map_grp)
		
		
		####################################################################
		# Create Municipal page group
		
		mun_grp = main_ext.PageGroup('municipal', "Municipal Pages")
		
		# Add arguments
		mun_grp.add_arg('word', title='Search Word')
		
		cat_arg = mun_grp.add_arg('category', default='all', title='Winnipeg Catalogue Category')
		cat_arg.add_opt('Assessment, Taxation, & Corporate', ['corp'], ['Assessment%2C+Taxation%2C+%26+Corporate'])
		cat_arg.add_opt('Cemeteries', url_tags=['Cemeteries'])
		cat_arg.add_opt('Census', url_tags=['Census'])
		cat_arg.add_opt('City Planning', ['planning'], ['City+Planning'])
		cat_arg.add_opt('Contact Centre - 311', ['contact'], ['Contact+Centre+-+311'])
		cat_arg.add_opt('Council Services', ['council'], ['Council+Services'])
		cat_arg.add_opt('Crime', url_tags=['Crime'])
		cat_arg.add_opt('Development Approvals, Building Permits, & Inspections', ['development'], ['Development+Approvals%2C+Building+Permits%2C+%26+Inspections'])
		cat_arg.add_opt('Education and Training', ['education'], ['Education+and+Training'])
		cat_arg.add_opt('Fire and Rescue Response', ['fire'], ['Fire+and+Rescue+Response'])
		cat_arg.add_opt('Insect Control', ['insect'], ['Insect+Control'])
		cat_arg.add_opt('Libraries', url_tags=['Libraries'])
		cat_arg.add_opt('Organizational Support Services', ['org'], ['Organizational+Support+Services'])
		cat_arg.add_opt('Parking', url_tags=['Parking'])
		cat_arg.add_opt('Parks', url_tags=['Parks'])
		cat_arg.add_opt('Province of Manitoba', ['province'], ['Province+of+Manitoba'])
		cat_arg.add_opt('Recreation', url_tags=['Recreation'])
		cat_arg.add_opt('Tickets and Adjudication', ['tickets'], ['Tickets+and+Adjudication'])
		cat_arg.add_opt('Transportation Planning & Traffic Management', ['traffic'], ['Transportation+Planning+%26+Traffic+Management'])
		cat_arg.add_opt('Water and Waste', ['waste'], ['Water+and+Waste'])
		
		sb_arg = mun_grp.add_arg('subpage', default='all', debug=True)
		sb_arg.add_opt('Brandon Open Data', ['br_open'], ['bdn_opendata'])
		sb_arg.add_opt('Brandon REST Services', ['br_rest'], ['bdn_rest'])
		sb_arg.add_opt('Brandon GIS', ['br_gis'], ['bdn_gis'])
		sb_arg.add_opt('Winnipeg Catalogue', ['wpg_cat'], ['wpg_catalogue'])
		sb_arg.add_opt('Winnipeg Property Map/Aerial Photography & ServiceStat', ['wpg_prop'], ['wpg_property'])
		
		# Add URLs
		mun_grp.add_url('brandon_opendata_url', 'http://opengov.brandon.ca/OpenDataService/opendata.html')
		mun_grp.add_url('brandon_rest_url', 'https://gisapp.brandon.ca/arcgis/rest/services')
		mun_grp.add_url('brandon_gis_url', 'http://gis.brandon.ca')
		mun_grp.add_url('winnipeg_opendata_url', 'https://data.winnipeg.ca/browse')
		mun_grp.add_url('winnipeg_property_url', 'http://winnipeg.ca/ppd/maps_aerial.stm')
		mun_grp.add_url('winnipeg_servstat_url', 'http://winnipeg.ca/Interhom/serviceStat')
		
		# Add to Extractor's page group list
		self.page_groups.append(mun_grp)
		

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

	def get_mdata_item(self, soup, heading, field, tag='p'):
		heading_tag = soup.find(tag, text=heading)
		fields = heading_tag.find_next_sibling('p')
		fields_text = fields.text
		fields = fields_text.split('\n')
		for f in fields:
			#print l
			if f.find(field) > -1:
				out_text = f.split(':')[1].strip()
				return out_text
		return ''

	def mdata_item(self, mdata_soup, titles, tag_name=None, multiline=False):
		for title in titles:
			# Locate the tag containing title
			tag = bsoup.find_tag_by_text(mdata_soup, title, tag_name)

			#print tag
			#answer = raw_input("Press enter...")

			if tag is None or len(tag) == 0:
				continue
			if multiline:
				# First, check to see if <pre> is a sibling
				parent_tag = tag[0].parent
				pre_tag = parent_tag.find('pre')
				if pre_tag is None:
					#print parent_tag
					sib_tag = parent_tag.next_sibling
					if sib_tag is None:
						div_tag = parent_tag.find('div')
						out_txt = shared.clean_text(div_tag.text)
					else:
						out_txt = shared.clean_text(sib_tag.text)
				else:
					out_txt = shared.clean_text(pre_tag.text)
			else:
				parent_tag = tag[0].parent
				out_txt = parent_tag.text
				if out_txt.find(u'\u2003') > -1:
					text_split = out_txt.split(u'\u2003')
					out_txt = ' '.join(text_split[1:])
				else:
					text_split = out_txt.split(': ')
					out_txt = ' '.join(text_split[1:])

				#print out_txt
				#answer = raw_input("Press enter...")

			return out_txt

		return ''

	def get_metadata(self, mdata_url):
		''' Gets the metadata for a dataset in the MLI pages
		:param mdata_url: The metadata URL.
		:return: A dictionary containing the applicable information extract
					from the metadata page.
		'''

		mdata_info = collections.OrderedDict()

		# Check the file extension of the metadata URL
		if mdata_url.find('.zip') > -1 or mdata_url.find('.pdf') > -1:
			return None

		if mdata_url.find('.txt') > -1:
			mdata_resp = shared.open_webpage(mdata_url)
			if isinstance(mdata_resp, int): return 'Metadata link is broken.'
			mdata_text = mdata_resp.read()

			# Get the description between 'Abstract:' and 'Purpose:'
			desc_str = ''
			start_pos = mdata_text.find('Abstract:') + len('Abstract:')
			end_pos = mdata_text.find('Purpose:')
			if not start_pos == len('Abstract:') - 1:
				desc = mdata_text[start_pos:end_pos]
				desc_str = shared.clean_text(desc)
				#print desc_str

			# Get the constraints between 'Use_Constraints:' and 'Point_of_Contact:'
			lic_str = ''
			start_pos = mdata_text.find('Use_Constraints:') + len('Use_Constraints:')
			end_pos = mdata_text.find('Point_of_Contact:')
			if not start_pos == len('Use_Constraints:') - 1:
				lic = mdata_text[start_pos:end_pos]
				lic_str = shared.clean_text(lic)
				#print lic_str

			# Get single line values
			date_str = ''
			sp_str = ''
			mdata_type = ''
			pub_str = ''
			m_lines = mdata_text.split('\n')
			for line in m_lines:
				if line.find('Calendar_Date') > -1:
					date_str = line.split(':')[1]
				elif line.find("Other_Projection's_Definition") > -1:
					sp_str = line.split(':')[1]
				elif line.find("Metadata_Standard_Name") > -1:
					mdata_type = line.split(':')[1]
				elif line.find("Originator") > -1:
					pub_str = line.split(':')[1]

			mdata_info['Description'] = desc_str
			mdata_info['Licensing'] = shared.reduce_text(lic_str)
			mdata_info['Date'] = date_str
			mdata_info['Spatial Reference'] = sp_str
			mdata_info['Metadata Type'] = mdata_type
			mdata_info['Publisher'] = pub_str

		elif mdata_url.find('.xml') > -1:
			mdata_xml = bsoup.get_xml_soup(mdata_url)
			if isinstance(mdata_xml, int): return 'Metadata link is broken.'

			# Get the description
			desc_str = ''
			tags = ['abstract', 'idAbs']
			desc_tag = bsoup.find_xml_tags(mdata_xml, tags)
			if len(desc_tag) > 0: desc_str = desc_tag[0].text

			# Get the date
			date_str = ''
			tags = ['ModDate', 'enddate', 'createDate']
			date_tag = bsoup.find_xml_tags(mdata_xml, tags)
			if len(date_tag) > 0: date_str = date_tag[0].text

			# Get the metadata type
			mdata_type = ''
			tags = ['metstdn']
			meta_tag = bsoup.find_xml_tags(mdata_xml, tags)
			if len(meta_tag) > 0: mdata_type = meta_tag[0].text

			# Get the spatial reference
			sp_str = ''
			tags = ['identCode', 'mapprojn']
			sp_tag = bsoup.find_xml_tags(mdata_xml, tags)

			if len(sp_tag) > 0:
				sp_str = sp_tag[0].text
			else:
				sp_str = 'UTM Zone 14, NAD 83 (EPSG:26914)'

			# Get the publisher
			pub_str = ''
			tags = ['origin', 'rpOrgName']
			pub_tag = bsoup.find_xml_tags(mdata_xml, tags)
			if len(pub_tag) > 0: pub_str = pub_tag[0].text

			mdata_info['Description'] = desc_str
			mdata_info['Date'] = date_str
			mdata_info['Spatial Reference'] = sp_str
			mdata_info['Metadata Type'] = mdata_type
			mdata_info['Publisher'] = pub_str

		else:
			if mdata_url.find('.doc') > -1: return None
		
			mdata_soup = bsoup.get_soup(mdata_url)
			if isinstance(mdata_soup, int): return 'Metadata link is broken.'
			
			if mdata_soup is None: return 'Metadata link is broken.'
			
			if not self.check_result(mdata_soup, mdata_url, 'MLI Metadata Page'): return None

			html_tag = mdata_soup.find('html')
			if html_tag is None: return None
			if isinstance(html_tag, int): return None
			if html_tag.has_attr('xmlns:res'):
				# Type 1 Metadata - ArcGIS Metadata
				# Ex: http://mli2.gov.mb.ca/dems/lidar/Arrow_Oak/Arrow_Oak_LiDAR_DEM_Metadata.htm#ID0EBLA

				# Get the description
				desc_str = self.mdata_item(mdata_soup, ['Description'], multiline=True)

				# Get the publisher

				# Get the date
				date_opts = ['Date and time', 'Revision date', 'Publication date']
				date_str = self.mdata_item(mdata_soup, date_opts)

				# Get the licence
				lic_opts = ['Use limitations', 'Access and use limitations']
				lic_str = self.mdata_item(mdata_soup, lic_opts)

				# Get the metadata type
				type_opts = ['Metadata style', 'Name of the metadata standard used']
				type_str = self.mdata_item(mdata_soup, type_opts)

				# Get the spatial reference
				sp_opts = ['Projection']
				sp_str = self.mdata_item(mdata_soup, sp_opts)

				mdata_info['Description'] = desc_str
				mdata_info['Licensing'] = lic_str
				mdata_info['Date'] = date_str
				mdata_info['Spatial Reference'] = sp_str
				mdata_info['Metadata Type'] = type_str

			else:
				# Get the metadata from the meta tags
				meta_tag_check = mdata_soup.find('meta')
				if meta_tag_check is None:
					################################################################
					# Type 3 Metadata - FGDC & ESRI Metadata
					# Ex: http://mli2.gov.mb.ca/ortho/meta_files/digital_orthophoto_images_capital_region_meta.html

					# Get the description
					desc_dt = mdata_soup.find('dt', text='Abstract:')
					if desc_dt is None: return None
					desc_pre = desc_dt.find_next_sibling('pre')
					desc_str = desc_pre.text

					# Get the publisher
					pub_dt = bsoup.find_tags_containing(mdata_soup, 'Originators:', 'dt')
					#print "pub_dt: %s" % pub_dt
					#if isinstance(pub_dt, list): pub_dt = pub_dt[0]
					pub_str = pub_dt.text.split(":")[1]
					pub_str = shared.clean_text(pub_str)

					# Get the date
					#date_dt = bsoup.find_tags_containing(mdata_soup, 'Ending date:', 'dt')
					date_opts = ['Ending date:', 'Calendar date:']
					date_str = self.mdata_item(mdata_soup, date_opts)

					# Get the metadata type from the page
					mtype_dt = bsoup.find_tags_containing(mdata_soup, 'Metadata standard name:', 'dt')
					mtype_str = mtype_dt.text.split(":")[1]
					mtype_str = shared.clean_text(mtype_str)

					type_str = ''
					lic_str = ''

				else:
					################################################################
					# Type 2 Metadata - FGDC Metadata
					# Ex: http://mli2.gov.mb.ca/dems/lidar/south_section/l384_fp_meta.html

					# Get the metadata from the <meta> tags on the page
					page_mdata = bsoup.get_page_metadata(mdata_soup)

					# Get the description
					desc_str = ''
					if 'dc.description' in page_mdata.keys(): desc_str = page_mdata['dc.description']

					# Get the publisher
					pub_str = ''
					if 'dc.publisher' in page_mdata.keys(): pub_str = page_mdata['dc.publisher']

					# Get the date
					date_str = ''
					if 'dc.date' in page_mdata.keys(): date_str = page_mdata['dc.date']

					# Get the licence
					lic_str = ''
					if 'dc.rights' in page_mdata.keys(): lic_str = page_mdata['dc.rights']

					# Get the data type
					type_str = ''
					if 'dc.type' in page_mdata.keys(): type_str = page_mdata['dc.type']

					# Get the metadata type from the page
					mtype_str = ''
					mtype_tag = bsoup.find_tags_containing(mdata_soup, 'Metadata_Standard_Version', 'em')
					if mtype_tag is not None:
						mtype_parent = mtype_tag.parent
						mtype_txt = shared.clean_text(mtype_parent.text)#.encode('ascii', 'replace'))
						mtype_str = mtype_txt.split(':')[1]

				mdata_info['Description'] = desc_str
				mdata_info['Licensing'] = lic_str
				mdata_info['Date'] = date_str
				mdata_info['Publisher'] = pub_str
				mdata_info['Type'] = type_str
				mdata_info['Metadata Type'] = mtype_str

		#for k, v in mdata_info.items():
		#	print "%s: %s" % (k, v)

		#answer = raw_input("Press enter...")

		return mdata_info

	def get_world_link(self, soup, url, txt, notes_str=''):
		''' Gets the world file URL from a soup based on the input txt.
		:param soup: The soup to perform the search.
		:param url: The root URL.
		:param txt: The text contained in the world file's <a> tag.
		:return: The world file URL.
		'''
		world_url = ''
		notes_str = notes_str
		world_a = bsoup.find_tags_containing(soup, txt, 'a')
		if world_a is not None:
			world_url = shared.get_anchor_url(world_a, url)
			if notes_str == '':
				notes_str = "The 'Data URL' contains a link to a Zip file which " \
							"contains the World file for this dataset."

		return (world_url, notes_str)
		
	def process_googleapi(self, layers, lyr_type):

		records = []

		for idx, layer in enumerate(layers):
			msg = "Extracting %s of %s layers from Google Maps API" % (idx + 1, len(layers))
			shared.print_oneliner(msg)
		
			rec_dict = collections.OrderedDict()

			# if lyr_type == "property":
			#     element = layer.find('input')
			#     id = element.get('id')
			#     id = id.replace("chk", "")
			# else:
			#     element = layer
			#     id = element.get('id')
			#     id = id.replace("chk-id", "")

			id = layer.get('id')
			id = id.replace("tbl", "")

			title_str = bsoup.get_text(layer)

			# Build query URL
			# Ex: https://mapapi.winnipeg.ca/mapapi/wfs.ashx?output=json&maptypeid=2&coordinates=&g=n&featurelist=13937
			mapapi_url = "https://mapapi.winnipeg.ca/mapapi/wfs.ashx"
			srch_params = collections.OrderedDict()
			srch_params['output'] = "json"
			srch_params['maptypeid'] = "2"
			srch_params['coordinates'] = ""
			srch_params['g'] = "n"
			srch_params['featurelist'] = id

			query_url = shared.get_post_query(mapapi_url, srch_params)

			# Get soup
			json_res = shared.get_json(query_url)

			features = json_res['features']

			serv_type = features[0]['serviceType']
			if serv_type == "both": serv_type = "WMS|WFS"

			rec_dict['Title'] = title_str
			rec_dict['Type'] = serv_type.upper()
			rec_dict['Description'] = features[0]['DESCRIPTION']
			rec_dict['Data URL'] = query_url

			records.append(rec_dict)

		return records

	def process_map(self, in_map, page_url, title_prefix=None):
		''' Goes through a map on a page and creates a dictionary
				for each <area> tag.
		:param in_map: The map to process.
		:param page_url: The URL of the page which contains the map.
		:param title_prefix: A text to be added to the front of the title.
		:return: Returns a list of dictionaries for each area.
		'''

		out_areas = []

		# Get the areas in the map
		areas = in_map.find_all('area')

		# Cycle through the areas
		for area in areas:

			# If the area has no 'href' or it is empty, skip it
			if not area.has_attr('href'): continue
			if area['href'] == '': continue

			area_dict = collections.OrderedDict()

			# Get the area link
			area_link = area['href']
			area_url = urlparse.urljoin(page_url, area_link)

			# Get the title using the 'alt' attribute and the title_prefix
			if area.has_attr('alt'):
				area_id = area['alt']
			else:
				area_id = os.path.basename(area_url).split('.')[0]
			if title_prefix is None:
				title_str = area_id
			else:
				title_str = "%s - %s" % (title_prefix, area_id)

			# Add the info to the area_dict
			area_dict['Title'] = title_str
			area_dict['Web Page URL'] = page_url
			area_dict['Download'] = area_url
			area_dict['Access'] = 'Download/Web Accessible'

			# Get the metadata link
			if page_url.find('shp') > -1:
				mdata_map_url = page_url.replace('shp', 'meta')
				mdata_map_soup = bsoup.get_soup(mdata_map_url)
				
				if mdata_map_soup is None:
					print "\nWARNING: Metadata page '%s' could not be opened." % mdata_map_url
					print "Please check the 'err_log.csv' file in the province/territory results folder."
					self.write_error(mdata_map_url, 'Metadata Page', 'Metadata page results could not be opened.')
					continue

				# Get the actual metadata URL by finding its area's id
				mdata_area = mdata_map_soup.find('area', attrs={'alt': area_id})
				mdata_link = mdata_area['href']
				mdata_url = urlparse.urljoin(mdata_map_url, mdata_link)

				mdata_info = self.get_metadata(mdata_url)
				if mdata_info is not None:
					area_dict.update(mdata_info)

				# Get a list of formats
				formats = []
				b_doc = mdata_map_soup.find('b', text='.DOC')
				p_doc = b_doc.parent
				td_doc = p_doc.parent
				tr = td_doc.parent
				td_list = tr.find_all('td')
				for td in td_list:
					if not td.text == '.DOC':
						formats.append(td.text.strip().replace('.', ''))

				# Set the formats, download_str and access_str
				formats_str = "|".join(formats)
				download_info = shared.get_download_text(formats)
				download_str, access_str = download_info.split('|')

				# Add the metadata info to the area_dict
				area_dict['Available Formats'] = formats_str
				area_dict['Download'] = download_str
				area_dict['Access'] = access_str
				area_dict['Metadata URL'] = mdata_url

			out_areas.append(area_dict)

		return out_areas

	def process_table(self, parent_title, table, index_url, unique_cols=None,
					  ignore_rows=None, replace_vals=None, title_prefix=None,
					  start_row=1):
		''' Processes a table with the first column as the item title and the values
			in the other columns.
		:param parent_title: The title of the current parent page.
		:param table: The table soup object.
		:param index_url: The URL of the page the table is on.
		:param unique_cols: The values are specified columns used for specific values.
							Ex: unique_cols['mdata_col'] = '.doc' means the column with
								heading '.doc' will only be used for metadata.
		:param ignore_rows: The values in this list will be used to ignore any rows
							where the first column is the value.
		:param replace_vals: A list of tuples where the first value of the tuple
							will be replaced by the second value in the tuple.
		:param title_append: A value to append as the start of the title.
		:return: A list of dictionaries for each row in the table.
		'''
		rec_list = []

		# Set up the unique_cols with default values if it is None
		if unique_cols is None:
			unique_cols = collections.OrderedDict()
			unique_cols['mdata_col'] = '.doc'
			unique_cols['date_col'] = 'date'
			unique_cols['ignore_cols'] = ['version']

		if not 'ignore_cols' in unique_cols:
			unique_cols['ignore_cols'] = []

		# Set up ignore_rows with default values if it is None
		if ignore_rows is None: ignore_rows = ['Go to top']

		# Get the table list
		table_rows = shared.table_to_dict(table, 0, start_row=start_row)
		
		sub_title = ''

		# Go through each row in the table_rows
		for row in table_rows:
			# Create the dictionary which will hold the values for the CSV file
			rec_dict = collections.OrderedDict()

			# Get the title of the dataset from the first column
			title_tag = row[row.keys()[0]]
			title = shared.clean_text(title_tag.text.strip())

			# If title is not blank and the first column does not contain any
			#   of the words in the ignore_rows list
			#print str(any(s in title for s in ignore_rows))
			
			bold = title_tag.find('b')
			if bold is not None:
				sub_title = "%s: " % bsoup.get_text(bold)
				
			if sub_title == 'Communities': sub_title = ''
			
			if not title == "" and not any(s in title for s in ignore_rows):
				# Remove all whitespace from the title
				title_str = "%s - %s%s" % (parent_title, sub_title, shared.clean_text(title))
				formats = []
				# Get a dictionary of downloads
				downloads = collections.OrderedDict()
				# Get the list of formats from all remaining columns
				#   which are not in the unique_cols dictionary

				dtype = ''
				for key, value in row.items()[1:]:
					key_text = shared.clean_text(key)
					if isinstance(value, str):
						val_text = shared.clean_text(value)
					else:
						val_text = shared.clean_text(value.text)
					#print "title_str: '%s'" % title_str
					#print "key_text: " + str(key_text)
					#print "val_text: " + str(val_text)
					if replace_vals is not None:
						for v in replace_vals:
							if val_text == v[0]:
								val_text = v[1]

					if not key_text in unique_cols.values() and \
							not key_text in unique_cols['ignore_cols'] and \
							not val_text == 'Link' and \
							not val_text == "":
						# Get the formats
						format = shared.clean_text(val_text)
						if format.find(u'\xa0') > -1:
							format_split = format.split(u'\xa0 ')
							for form in format_split:
								formats.append(form.replace('.', ''))
						else:
							formats.append(format)
						# Get the download list
						if not isinstance(value, str):
							a = value.find('a')
							if a is not None:
								url = shared.get_anchor_url(a, index_url)
								frm = shared.clean_text(a.text.lower())
								if replace_vals is not None:
									for v in replace_vals:
										if frm == v[0].lower():
											frm = v[1]
								frm = frm.replace('.', '')
								downloads[frm] = url
								dtype = shared.get_data_type(url)

				#print formats

				# Get the proper download and access text
				if len(downloads.keys()) == 0:
					download_str = 'No'
					access = 'Contact the Province'
				else:
					if len(formats) == 0:
						download_str = 'No'
						access = 'Contact the Province'
					elif len(formats) == 1:
						#print downloads
						#print formats
						download_str = downloads[downloads.keys()[0]]
						access = 'Download/Web Accessible'
					else:
						download_str = 'Multiple Downloads'
						access = 'Download/Web Accessible'

				# Get the metadata URL
				doc_soup = None
				mdata_url = ''
				if 'mdata_col' in unique_cols:
					mdata_col = unique_cols['mdata_col']
					if mdata_col in row:
						doc_soup = row[mdata_col]
					elif 'metadata' in row:
						doc_soup = row['metadata']

					if doc_soup is not None and not isinstance(doc_soup, str):
						mdata_a = doc_soup.find('a')
						#print mdata_a
						if mdata_a is not None:
							mdata_url = shared.get_anchor_url(mdata_a, index_url)

						# Get the metadata info
						if mdata_url is not None and not mdata_url == '':
							mdata_info = self.get_metadata(mdata_url)
							if mdata_info is not None:
								rec_dict.update(mdata_info)

				# Get the description, if applicable
				desc_str = ''
				if 'desc_col' in unique_cols:
					desc_col = unique_cols['desc_col']
					if desc_col in row:
						doc_soup = row[desc_col]

					if doc_soup is not None and not isinstance(doc_soup, str):
						desc_str = doc_soup.text

				# Get the date, if applicable
				date_str = ''
				if 'date_col' in unique_cols:
					date_col = unique_cols['date_col']
					if date_col in row:
						date_soup = row[date_col]
						if isinstance(date_soup, str):
							date_str = date_soup.strip()
						else:
							date_str = date_soup.text.strip()

				# Get the spatial reference, if applicable
				sp_str = 'UTM Zone 14, NAD 83 (EPSG:26914)'
				if 'ref_col' in unique_cols:
					ref_col = unique_cols['ref_col']
					if ref_col in row:
						sp_soup = row[ref_col]
						if isinstance(sp_soup, str):
							sp_str = sp_soup.strip()
						else:
							sp_str = sp_soup.text.strip()

				# Append the title if applicable
				if title_prefix is not None:
					title_str = "%s - %s" % (title_prefix, title_str)

				# Store the vales in the dictionary
				rec_dict['Title'] = title_str
				rec_dict['Available Formats'] = "|".join([f.replace('.', '') for f in formats])
				rec_dict['Access'] = access
				rec_dict['Type'] = dtype
				rec_dict['Download'] = download_str
				rec_dict['Metadata URL'] = mdata_url
				rec_dict['Spatial Reference'] = sp_str
				rec_dict['Web Page URL'] = index_url
				rec_dict['Date'] = date_str

				# FOR DEBUG ONLY
				#for k, v in rec_dict.items():
				#	print "%s: %s" % (k, v)

				# Add the record dictionary to the list of records
				rec_list.append(rec_dict)

		return rec_list

	def extract_dem(self):
		''' Extracts the DEM downloads
		:return: None
		'''
		
		self.print_title("Extracting Manitoba's DEM page")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get the DEM main url
		main_url = self.pg_grp.get_url('main_url')
		mdata_url = self.pg_grp.get_url('mdata_url')

		# Create the CSV file
		csv_fn = "DEM_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# First get the metadata info
		mdata_soup = bsoup.get_soup(mdata_url)
		
		if mdata_soup is None:
			print "\nWARNING: DEM metadata page '%s' could not be opened." % mdata_url
			print "Please check the 'err_log.csv' file in the province/territory results folder."
			self.write_error(mdata_url, 'DEM Metadata Page', 'DEM metadata page results could not be opened.')
			return None

		# Split the page at <h2> tags in order to separate the different datasets
		h2_list = str(mdata_soup).split('<h2')

		# Loop through each dataset on the page and add the information to a
		#   dictionary containing the <h2> text as keys
		mdata_dict = collections.OrderedDict()
		for h2 in h2_list[1:]:

			sub_soup = BeautifulSoup("<h2" + h2, 'html.parser')

			# Get the title to store in the mdata_dict
			h2_text = sub_soup.find('h2').text
			title = h2_text.split(u'\u2013')[0].strip()
			if title.find("Manitoba") > -1:
				title = title.replace(' Version', '')

			#print title

			# Get the description text
			desc_h = bsoup.find_tags_containing(sub_soup, 'Description', 'h4')
			if desc_h is None:
				desc_h = bsoup.find_tags_containing(sub_soup, 'Description', 'h5')
			desc_p = desc_h.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p).replace('Abstract: ', '')

			sp_str = 'UTM Zone 14, NAD 1983'

			# Get the data from the publication date
			date = self.get_mdata_item(sub_soup, 'Citation Information: ', 'Publication Date: ')
			date_str = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

			pub_str = self.get_mdata_item(sub_soup, 'Citation Information: ', 'Publisher: ')

			#print desc_str
			#print sp_str
			#print date_str
			#print pub_str

			info = collections.OrderedDict()
			info['Description'] = desc_str
			info['Spatial Reference'] = sp_str
			info['Date'] = date_str
			info['Publisher'] = pub_str

			mdata_dict[title] = info

		# Get the soup
		dem_soup = bsoup.get_soup(main_url)
		
		if dem_soup is None:
			print "\nWARNING: DEM main page '%s' could not be opened." % main_url
			print "Please check the 'err_log.csv' file in the province/territory results folder."
			self.write_error(main_url, 'DEM Main Page', 'Page could not be opened.')
			return None

		# Find the h2 containing the word 'Ordering'
		h2 = bsoup.find_tags_containing(dem_soup, 'Ordering', 'h2')
		ol = h2.find_next_sibling('ol')
		heading_list = ol.find_all('li')

		# Build a collection of unique datasets from the heading list
		# Ex:
		#   ds_dict =
		#   "DEMSM Version 1":
		#   {
		#	    "formats": [
		#           "ASCII Grid",
		#           "MapInfo Grid",
		#           "Tiff Image"
		#   	],
		#	    "links": [
		#           "#1",
		#           "#2",
		#           "#3"
		#	    ]
		#   },
		#   ...
		ds_dict = collections.OrderedDict()
		for h in heading_list:
			# Parse the heading text
			a = h.find('a')
			h_text = a.text
			end_pos = h_text.find('(')
			title_str = h_text[:end_pos].strip()
			if title_str in ds_dict.keys():
				info_dict = ds_dict[title_str]
			else:
				info_dict = collections.OrderedDict()
				info_dict['formats'] = []
				info_dict['links'] = []
			formats = info_dict['formats']
			format = shared.get_bracket_text(h_text)
			formats.append(format)
			info_dict['formats'] = formats
			links = info_dict['links']
			links.append(a['href'])
			info_dict['links'] = links

			ds_dict[title_str] = info_dict

		for k, v in ds_dict.items():
			idx = ds_dict.keys().index(k)
			msg = "Extracting %s of %s datasets" % (idx + 1, len(ds_dict.items()))
			shared.print_oneliner(msg)
		
			formats = v['formats']
			links = v['links']

			title_str = k
			access_str = 'Download/Web Accessible'
			available_formats = '|'.join([f.replace(" Grid", "") for f in formats])
			if len(links) > 1:
				download_str = 'Multiple Downloads'
			else:
				download_str = ''
				bookmark = links[0].replace("#", "")
				# Locate <a> with bookmark ID
				a_bkmark = dem_soup.find('a', attrs={'id': bookmark})
				li_parent = a_bkmark.parent
				a_list = li_parent.find_all('a')
				for a in a_list:
					if a.has_attr('href'):
						download_str = urlparse.urljoin(main_url, a['href'])

			mdata_key = title_str.split('-')[0]
			mdata_key = mdata_key.strip()
			mdata_key = mdata_key.replace('DEMSM ', '')
			if mdata_key in mdata_dict:
				mdata_info = mdata_dict[mdata_key]

				for mdata_k, mdata_v in mdata_info.items():
					pt_csv.add(mdata_k, mdata_v)

			# Add all geospatial data to the pt_csv
			pt_csv.add('Source', 'Manitoba DEMs')
			pt_csv.add('Title', title_str)
			pt_csv.add('Access', access_str)
			pt_csv.add('Type', 'Raster Data')
			pt_csv.add('Download', download_str)
			pt_csv.add('Web Page URL', main_url)
			pt_csv.add('Metadata URL', mdata_url)
			pt_csv.add('Available Formats', available_formats)

			pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_maps(self):
		''' Method to extract all interactive maps for Manitoba.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Manitoba's interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "InteractiveMaps_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()

		################################################################################
		# Start with the Petroleum map
		petrol_parent_url = self.pg_grp.get_url('petrol_url')[0]
		petrol_map_url = self.pg_grp.get_url('petrol_url')[1]
		petrol_service_url = self.pg_grp.get_url('petrol_url')[2]

		# Get the info from the parent page
		petrol_parent_soup = bsoup.get_soup(petrol_parent_url)
		
		if self.check_result(petrol_parent_soup, petrol_parent_url, 'Petroleum Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the main-content <div>
			content_div = petrol_parent_soup.find('div', attrs={'id': 'main-content'})

			# Get the title from the main-content <div>
			title_h = content_div.find('h1')
			title_str = bsoup.get_text(title_h)

			# Get the description from the parent page
			desc_tag = bsoup.find_tags_containing(petrol_parent_soup, 'this Interactive Map', 'strong')
			desc_str = bsoup.get_text(desc_tag)

			# Get the date from the parent page
			date_tag = bsoup.find_tags_containing(petrol_parent_soup, 'Updated:', 'strong')
			date_str = bsoup.get_text(date_tag)

			sp_str = 'UTM Zone 14, NAD 83 (EPSG:26914)'

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', petrol_map_url)
			pt_csv.add('Data URL', petrol_service_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Date', date_str)
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')
			pt_csv.add('Spatial Reference', sp_str)

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		################################################################################
		# Drought Management Map
		drought_url = self.pg_grp.get_url('drought_url')

		# Get the ArcGIS Online data URL from the <iframe> tag on the drought page
		drought_soup = bsoup.get_soup(drought_url)
		
		if self.check_result(drought_soup, drought_url, 'Drought Management Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			drought_iframe = drought_soup.find('iframe')
			drought_datasrc = drought_iframe['src']

			# Get the ArcGIS Online data
			data_url = shared.get_arcgis_url(drought_datasrc)

			map_json = shared.get_json(data_url)
			
			# If map_json is None
			if self.check_result(map_json, data_url, 'Drought Management Map JSON Results'):
				# Get the title, date and data type
				title_str = map_json['title']
				date_str = shared.translate_date(map_json['modified'])
				dtype = map_json['type']

				# Get the description
				desc_html = map_json['description']
				desc_soup = BeautifulSoup(desc_html, 'html.parser')
				desc_str = bsoup.get_text(desc_soup)

				# Get the map URL
				map_url = map_json['url']

				# Get the licence info
				lic_html = map_json['licenseInfo']
				lic_soup = BeautifulSoup(lic_html, 'html.parser')
				lic_str = bsoup.get_text(lic_soup)

				# Add all values to the CSV file object
				pt_csv.add('Source', 'Manitoba Interactive Maps')
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Web Page URL', drought_url)
				pt_csv.add('Data URL', data_url)
				pt_csv.add('Type', dtype)
				pt_csv.add('Date', date_str)
				pt_csv.add('Licensing', lic_str)
				pt_csv.add('Access', 'Viewable/Contact the Province')
				pt_csv.add('Download', 'No')
				#pt_csv.add('Spatial Reference', sp_str)

				# Write the dataset to the CSV file
				pt_csv.write_dataset()

		################################################################################
		# Drinking Water Advisories in Manitoba Map
		drink_url = self.pg_grp.get_url('drink_url')

		# Get the ArcGIS Online data URL from the <iframe> tag on the drought page
		drink_soup = bsoup.get_soup(drink_url)
		
		if self.check_result(drink_soup, drink_url, 'Drinking Water Advisories in Manitoba Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			drink_iframe = drink_soup.find('iframe')
			drink_datasrc = drink_iframe['src']

			# Get the ArcGIS Online data
			data_url = shared.get_arcgis_url(drink_datasrc)

			map_json = shared.get_json(data_url)
			
			if self.check_result(map_json, data_url, 'Drinking Water Advisories in Manitoba Map JSON Results'):
				# Get the title, date and data type
				title_str = map_json['title']
				date_str = shared.translate_date(map_json['modified'])
				dtype = map_json['type']

				# Get the description
				desc_html = map_json['description']
				desc_soup = BeautifulSoup(desc_html, 'html.parser')
				desc_str = bsoup.get_text(desc_soup)

				# Get the map URL
				map_url = map_json['url']

				# Get the licence info
				lic_html = map_json['licenseInfo']
				lic_soup = BeautifulSoup(lic_html, 'html.parser')
				lic_str = bsoup.get_text(lic_soup)

				# Add all values to the CSV file object
				pt_csv.add('Source', 'Manitoba Interactive Maps')
				pt_csv.add('Title', title_str)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Web Page URL', drought_url)
				pt_csv.add('Data URL', data_url)
				pt_csv.add('Type', dtype)
				pt_csv.add('Date', date_str)
				pt_csv.add('Licensing', lic_str)
				pt_csv.add('Access', 'Viewable/Contact the Province')
				pt_csv.add('Download', 'No')
				# pt_csv.add('Spatial Reference', sp_str)

				# Write the dataset to the CSV file
				pt_csv.write_dataset()

		################################################################################
		# WeatherView map

		wview_map_url = self.pg_grp.get_url('weather_url')[0]
		wview_data_url = self.pg_grp.get_url('weather_url')[1]

		# Get the soup of the map page
		wview_soup = bsoup.get_soup(wview_map_url)
		
		if self.check_result(wview_soup, wview_map_url, 'WeatherView Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the main-content <div>
			content_div = wview_soup.find('div', attrs={'id': 'main-content'})

			# Get the title from the main-content <div>
			title_h = content_div.find('h1')
			title_str = bsoup.get_text(title_h)

			# Get the description
			desc_p = title_h.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', wview_map_url)
			pt_csv.add('Web Page URL', wview_map_url)
			pt_csv.add('Data URL', wview_data_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		################################################################################
		# Fire View map

		fireview_url = self.pg_grp.get_url('fireview_url')[0]
		parent_url = self.pg_grp.get_url('fireview_url')[1]

		# Get the soup for the FireView map
		fireview_soup = bsoup.get_soup(fireview_url)
		
		if self.check_result(fireview_soup, fireview_url, 'Fire View Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the main-content <div>
			content_div = fireview_soup.find('div', attrs={'id': 'main-content'})

			# Get the title from the main-content <div>
			title_h = content_div.find('h1')
			title_str = bsoup.get_text(title_h)

			# Get the sibling <p> to get the description of the map
			desc_p = title_h.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', fireview_url)
			pt_csv.add('Web Page URL', parent_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

			################################################################################
			# Fire Restrictions map

			restrict_url = self.pg_grp.get_url('restrict_url')

			title_str = 'Fire Restrictions Map'

			# Get the main-content <div>
			content_div = fireview_soup.find('div', attrs={'id': 'main-content'})

			# Get the sibling <p> to get the description of the map
			desc_p = content_div.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', restrict_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		################################################################################
		# Wildlife Management Areas map

		wildmap_url = self.pg_grp.get_url('wild_url')[1]
		home_url = self.pg_grp.get_url('wild_url')[0]

		# Get the soup of the home page
		home_soup = bsoup.get_soup(home_url)
		
		if self.check_result(home_soup, home_url, 'Wildlife Management Areas Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the body <div>
			body_div = home_soup.find('div', attrs={'class': 'body'})

			# Get the title from the <h2> tag in the body_div
			title_h2 = body_div.find('h2')
			title_str = bsoup.get_text(title_h2)

			# Get the description from the <p> tags from the body_div
			p_list = body_div.find_all('p')
			desc_str = ''.join(bsoup.get_text(p) for p in p_list)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', wildmap_url)
			pt_csv.add('Web Page URL', home_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')

			# Write the dataset to the CSV file
			pt_csv.write_dataset()

		################################################################################
		# Beach Monitoring Information map

		beach_url =  self.pg_grp.get_url('beach_url')[0]
		beachmap_url = self.pg_grp.get_url('beach_url')[1]

		# Get the soup of the main page
		beach_soup = bsoup.get_soup(beach_url)
		
		if self.check_result(beach_soup, beach_url, 'Beach Monitoring Information Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the body <div>
			body_div = beach_soup.find('div', attrs={'class': 'body'})

			# Get the description from the body div by getting the first <p>
			desc_p = body_div.find('p')
			desc_str = bsoup.get_text(desc_p)

			# Now get the soup for the beach map
			beachmap_soup = bsoup.get_soup(beachmap_url)

			# Get the title string from the <h1> in the main <div>
			main_div = beachmap_soup.find('div', attrs={'id': 'main-content'})
			title_h1 = main_div.find('h1')
			title_str = bsoup.get_text(title_h1)

			# Add all values to the CSV file object
			pt_csv.add('Source', 'Manitoba Interactive Maps')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Web Map URL', beachmap_url)
			pt_csv.add('Web Page URL', beach_url)
			pt_csv.add('Type', 'Web Map Application')
			pt_csv.add('Access', 'Viewable/Contact the Province')
			pt_csv.add('Download', 'No')

			# Write the dataset to the CSV file
			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_misc(self):
		''' Extracts the miscellaneous web pages
		:return: None
		'''
		
		self.print_title("Extracting Manitoba's other web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		##########################################################################
		# Get the Petroleum page

		# Get the petroleum main url
		main_url = self.pg_grp.get_url('petrol_url')

		# Create the CSV file
		csv_fn = "Misc_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()

		# Get the soup for petroleum site
		petrol_soup = bsoup.get_soup(main_url)
		
		if self.check_result(petrol_soup, main_url, 'Petroleum Page'):
			# Print the status
			cur_page += 1
			msg = "Extracting web page %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Find the <h2> with 'GIS Shapefiles to Download'
			down_h2 = petrol_soup.find('h2', text='GIS Shapefiles to Download')
		
			# Find its sibling <div>
			down_div = down_h2.find_next_sibling('div')
			# Now get the download anchors
			a_list = down_div.find_all('a')

			for a in a_list:
				download_url = urlparse.urljoin(main_url, a['href'])
				access_str = 'Download/Web Accessible'
				title_str = a.text.replace(' (zip)', '')
				date_str = a.next_sibling
				sp_str = 'UTM Zone 14, NAD 1983'
				type_str = 'Vector Data'

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', 'Manitoba Web Pages')
				pt_csv.add('Title', title_str)
				# pt_csv.add('Description', desc_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', type_str)
				pt_csv.add('Download', download_url)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Web Page URL', main_url)
				pt_csv.add('Date', date_str)
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

		##########################################################################
		# Extract the Fire page

		# Get the soup for the fire page
		fire_url = self.pg_grp.get_url('fire_url')
		fire_soup = bsoup.get_soup(fire_url)
		
		if self.check_result(fire_soup, fire_url, 'Fire Page'):
			# Print the status
			cur_page += 1
			msg = "Extracting web page %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Find the <div> with id 'main-content'
			main_div = fire_soup.find('div', attrs={'id': 'main-content'})

			# Get a list of all the links in the <div>
			a_list = main_div.find_all('a')

			# Add links to a dictionary with the link's year as a key
			ds = collections.OrderedDict()
			for a in a_list:
				a_text = bsoup.get_text(a)

				year = re.findall('(\d{4})', a_text)

				if len(year) > 0:
					if year[0] not in ds.keys():
						ds[year[0]] = []

					ds[year[0]].append(a)

			# Loop through each year in the dictionary
			#   and add each link to the CSV file
			for k, v in ds.items():

				# Get the title
				title_str = 'Fire Locations - %s' % k

				# Determine the formats
				formats = []
				for a in v:
					a_link = a['href']
					if a_link.lower().find('.zip') > -1:
						#print a_link
						formats.append('SHP')
					elif a_link.lower().find('.kmz') > -1:
						#print a_link
						formats.append('KMZ')

				# Get the URL of the link
				download_url = shared.get_anchor_url(v[0], fire_url)

				# Determine the download_str and access_str
				download_info = shared.get_download_text(formats, download_url)
				download_str, access_str = download_info.split('|')

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', 'Manitoba Web Pages')
				pt_csv.add('Title', title_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Download', download_str)
				pt_csv.add('Web Page URL', main_url)
				pt_csv.add('Date', k)
				pt_csv.add('Available Formats', "|".join(formats))

				pt_csv.write_dataset()

			fireidx_url = self.pg_grp.get_url('fireidx_url')
			fireidx_soup = bsoup.get_soup(fireidx_url)
			
			if self.check_result(fireidx_soup, fireidx_url, 'Fire Index Page'):
				file_table = fireidx_soup.find('table')
				file_rows = shared.table_to_dict(file_table)

				for row in file_rows:
					for k, v in row.items():
						if isinstance(v, str):
							v_text = v
						else:
							v_text = v.text
						#print "%s: %s" % (k, v_text)

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_mli(self): #, subpage='all'):
		''' Extract all the different sites of Manitoba Land Initiative
			:return: None
		'''
		
		# Get the parameters
		subpage = self.get_arg_val('subpage')
		
		self.print_title("Extracting Manitoba's Land Initiative web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# NOTE: subpage is for debugging only.
		if subpage is None: subpage = 'all'
		# subpage = 'all'

		index_url = self.pg_grp.get_url('main_url')

		# Get the section DIV
		#divs = soup.find_all('div', attrs={'class': 'section'})

		# Remove <br> between Land Use Maps and Municipal Maps
		idx_page = shared.open_webpage(index_url)
		before_txt = 'Land Use/Cover Maps</a><br>'
		after_txt = "Land Use/Cover Maps</a></li><li>"
		idx_content = idx_page.read()
		#print idx_content.find(before_txt)
		idx_content = idx_content.replace(before_txt, after_txt)

		soup = BeautifulSoup(idx_content, 'html.parser')
		
		if not self.check_result(soup, index_url, 'Manitoba Land Initiative Page'):
			return None

		divs = soup.find_all('div', attrs={'class': 'section'})

		#print divs

		# Get the li
		li_list = divs[0].find_all('li')

		#print "Number of records: %s" % str(len(li_list))

		mli_folder = "%s\\MLI_Results" % self.work_folder
		if not os.path.exists(mli_folder):
			os.mkdir(mli_folder)

		for idx, li in enumerate(li_list):

			#a_list = li.find_all('a')
			anchor = li.find('a')

			#for anchor in a_list:
			item_str = bsoup.get_text(anchor)

			# Ignore about and comments
			if item_str == 'About': continue
			if item_str == 'Comments': continue

			# Get the item's link and title
			page_url = anchor['href']
			parent_title = shared.clean_text(anchor.string)

			# Check to see if the subpage matches the title
			page_id = self.mli_opts[parent_title]
			#print parent_title
			#print page_id
			if not subpage == 'all' and not subpage == page_id:
				continue

			# Build the page's URL
			if page_url.find("../../") > -1:
				page_url = page_url.replace("../", "", 1)
			page_url = urlparse.urljoin(index_url, page_url)
			
			print "\nExtracting Category: " + str(parent_title)
			print "Category URL: " + str(page_url)

			# Set up the attributes variable for the selenium
			if item_str.lower() == "digital imagery":
				selenium = True
				attr_name = ['div', 'addthis_toolbox']
			else:
				selenium = False
				attr_name = None
			
			# Get the category soup
			rec_soup = bsoup.get_soup(page_url, selenium, attr_name)
				
			if not self.check_result(rec_soup, page_url, 'Manitoba Land Initiative - %s Page' % parent_title): continue

			# Reformat the parent_title for the CSV filename
			fn_tag = shared.clean_text(parent_title)
			fn_tag = fn_tag.replace(" ", "-").replace("/", "-").replace("\\", "-")

			sp_str = 'UTM Zone 14, NAD 83 (EPSG:26914)'
			
			source = 'Manitoba MLI - %s' % parent_title

			if parent_title == 'Administrative Boundaries' or parent_title == 'Base Maps' or \
					parent_title == 'Environment' or parent_title == 'Geographical Names' or \
					parent_title == 'Land Use/Cover Maps' or parent_title == 'Transportation':

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				# These sites include standard tables with no other links
				#   on the page
				table_list = rec_soup.find_all('table')
				for table in table_list:
				
					# Set the unique_cols
					unique_cols = collections.OrderedDict()
					unique_cols['mdata_col'] = '.doc'
					unique_cols['ignore_cols'] = ['.image', '.gif', 'version']
					replace_vals = [('GEO', 'FGDB')]
					rec_list = self.process_table(parent_title, table, page_url, replace_vals=replace_vals)

					for idx, rec in enumerate(rec_list):
						msg = "Extracting %s of %s records of %s" % (idx + 1, len(rec_list), parent_title)
						shared.print_oneliner(msg)
						for k, v in rec.items():
							pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.write_dataset()
						
					print

				pt_csv.close_csv()

			elif parent_title == 'Cadastral':

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				# The Cadastral site includes a single table for the geodatabase
				#   dataset and a few links to other datasets and indices

				###########################################################
				# Start with table on the Cadastral page
				table_list = rec_soup.find_all('table')
				table = table_list[1]
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = 'metadata'
				unique_cols['date_col'] = 'date'
				unique_cols['ignore_cols'] = ['version', 'update info']
				rec_list = self.process_table(parent_title, table, page_url, unique_cols)

				# Add the table on the Cadastral page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records of %s" % (idx + 1, len(rec_list), parent_title)
					shared.print_oneliner(msg)
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
					
				print

				# FOR DEBUG ONLY:
				# print ""
				# for row in rec_list:
				#     for k, v in row.items():
				#         print "%s: %s" % (k, v)

				###########################################################
				# Next, get the Tabular selection site for scraping
				tab_a = bsoup.find_tags_containing(rec_soup, 'Tabular selection', 'a')
				tab_link = tab_a['href']
				tab_url = urlparse.urljoin(page_url, tab_link)

				# Get the Tabular soup
				tab_soup = bsoup.get_soup(tab_url)
				
				if self.check_result(tab_soup, tab_url, 'Manitoba Land Initiative - %s Sub-Page' % parent_title):
					ignore_rows = ['Go to top', 'Townships', 'Townships East', 'Townships West',
								   'Parish', 'DofS', 'Special', 'Projects', 'Portage Diversion',
								   'Winnipeg Floodway', 'St. Norbert', 'Winnipeg - Index table']

					table_list = tab_soup.find_all('table')
					unique_cols['mdata_col'] = '.doc'
					unique_cols['date_col'] = 'date'
					unique_cols['ref_col'] = 'adjust'
					unique_cols['ignore_cols'] = ['ver']

					# Go through all the tables on the page (in this case 1)
					for idx, table in enumerate(table_list):
						#msg = "Extracting table %s of %s" % (idx + 1, len(table_list))
						#shared.print_oneliner(msg)
					
						rec_list = self.process_table(parent_title, table, tab_url, unique_cols=unique_cols,
													  ignore_rows=ignore_rows)

						# FOR DEBUG ONLY:
						# print ""
						# for row in rec_list:
						#     for k, v in row.items():
						#         print "%s: %s" % (k, v)

						for idx, rec in enumerate(rec_list):
							msg = "Extracting %s of %s records of %s" % (idx + 1, len(rec_list), parent_title)
							shared.print_oneliner(msg)
							# Add record to pt_csv
							for k, v in rec.items():
								pt_csv.add(k, v)

							# Update the CSV file
							pt_csv.add('Source', source)
							pt_csv.write_dataset()
							
						print

					###########################################################
					# There are two items in the list that has a separate page that needs to be loaded.
					#   St. Norbert and Winnipeg have an item called "Image Map" with a link to another page

					# Get the St. Nobert page URL
					nobert_a = bsoup.find_tags_containing(tab_soup, 'St. Norbert', 'a')
					nobert_td = nobert_a.parent
					imgmap_td = nobert_td.find_next_sibling('td')
					imgmap_a = imgmap_td.find('a')
					nobert_link = imgmap_a['href']
					nobert_url = urlparse.urljoin(tab_url, nobert_link)
					
					#print nobert_url
					#answer = raw_input("Press enter...")

					# Soup the St. Nobert page
					nobert_soup = bsoup.get_soup(nobert_url)
					
					if self.check_result(nobert_soup, nobert_url, 'Manitoba Land Initiative - %s St. Norbert Sub-Page' % parent_title):
						# Get the areas on the St. Norbert page and soup up there pages
						nobert_areas = nobert_soup.find_all('area')
						for idx, area in enumerate(nobert_areas):
							msg = "Extracting area %s of %s from map" % (idx + 1, len(nobert_areas))
							shared.print_oneliner(msg)
						
							area_link = area['href']
							area_url = urlparse.urljoin(nobert_url, area_link)

							area_soup = bsoup.get_soup(area_url, True)
							
							if area_soup is None:
								print "\nWARNING: St. Norbert area '%s' could not be opened." % (parent_title, area_url)
								print "Please check the 'err_log.csv' file in the province/territory results folder."
								self.write_error(area_url, 'St. Norbert Area' % parent_title, 'Page could not be opened.')
							else:
								# Locate the proper table
								h5 = bsoup.find_tags_containing(area_soup, 'Manitoba Land Initiative', 'h5')
								table = h5.find_next_sibling('table')

								# Get the title string
								title_font = bsoup.find_tags_containing(table, 'wred', 'font')
								if title_font is None: title_font = bsoup.find_tags_containing(table, 'ered', 'font')
								title_str = "%s - %s" % (parent_title, bsoup.get_text(title_font))

								# Locate the metadata
								mdata_url = ''
								mdata_td = bsoup.find_tags_containing(table, 'Metadata', 'td')
								mdata_tr = mdata_td.parent
								mdata_download_tr = mdata_tr.find_next_sibling('tr')
								mdata_a = mdata_download_tr.find('a')
								if not mdata_a is None:
									mdata_link = mdata_a['href']
									mdata_url = urlparse.urljoin(area_url, mdata_link)

								# Locate the downloads
								downloads = []
								dwnld_trs = area_soup.find_all('td', text='Download')
								for dwnload in dwnld_trs:
									parent_tr = dwnload.parent
									dwnload_tr = parent_tr.find_next_sibling('tr')
									dwnload_a = dwnload_tr.find('a')
									if not dwnload_a is None:
										dwnload_link = dwnload_a['href']
										format = dwnload_a.text
										dwnload_url = urlparse.urljoin(area_url, dwnload_link)
										downloads.append((format, dwnload_url))

								# Determine the download and access strings
								if len(downloads) == 0:
									download_str = 'No'
									access_str = 'Contact the Province'
								elif len(downloads) == 1:
									download_str = downloads[0][1]
									access_str = 'Download/Web Acccessible'
								else:
									download_str = 'Multiple Downloads'
									access_str = 'Download/Web Acccessible'

								# Get the formats
								formats = '|'.join(f[0].replace('.', '') for f in downloads)

								# Add all geospatial data to the pt_csv
								pt_csv.add('Source', source)
								pt_csv.add('Title', title_str)
								pt_csv.add('Access', access_str)
								pt_csv.add('Type', 'Vector Data')
								pt_csv.add('Download', download_str)
								pt_csv.add('Web Page URL', area_url)
								pt_csv.add('Metadata URL', mdata_url)
								pt_csv.add('Spatial Reference', sp_str)
								pt_csv.add('Available Formats', formats)

								pt_csv.write_dataset()
						
						print
					# Get the Winnipeg page URL
					winnipeg_a = bsoup.find_tags_containing(tab_soup, 'Winnipeg - Index table', 'a')
					winnipeg_td = winnipeg_a.parent
					imgmap_td = winnipeg_td.find_next_sibling('td')
					imgmap_a = imgmap_td.find('a')
					winnipeg_link = imgmap_a['href']
					winnipeg_url = urlparse.urljoin(tab_url, winnipeg_link)

					# Soup the Winnipeg page
					winnipeg_soup = bsoup.get_soup(winnipeg_url)
					
					if self.check_result(winnipeg_soup, winnipeg_url, 'Manitoba Land Initiative - %s Winnipeg Sub-Page' % parent_title):
						# Get the areas on the Winnipeg page and soup up there pages
						winnipeg_areas = winnipeg_soup.find_all('area')

						# Go through all the areas in Winnipeg
						for idx, area in enumerate(winnipeg_areas):
							msg = "Extracting area %s of %s from map" % (idx + 1, len(winnipeg_areas))
							shared.print_oneliner(msg)
						
							# Each area in Winnipeg contains a web map page with a collection
							#   of tiles as <area> tags
							area_link = area['href']
							area_url = urlparse.urljoin(winnipeg_url, area_link)
							# Load the metadata page instead
							area_url = area_url.replace("shp", "meta")

							area_soup = bsoup.get_soup(area_url, True)
							
							if area_soup is None:
								print "\nWARNING: Winnipeg area '%s' could not be opened." % (parent_title, area_url)
								print "Please check the 'err_log.csv' file in the province/territory results folder."
								self.write_error(area_url, 'Winnipeg Area' % parent_title, 'Page could not be opened.')
							else:
								# Get the title of the page
								title_font = area_soup.find('font', attrs={'size': '3'})
								area_title = title_font.text

								# Collect a list of tiles from the <area> tags
								tiles = area_soup.find_all('area')

								# Get a list of formats
								formats = []
								b_doc = area_soup.find('b', text='.DOC')
								p_doc = b_doc.parent
								td_doc = p_doc.parent
								tr = td_doc.parent
								td_list = tr.find_all('td')
								for td in td_list:
									if not td.text == '.DOC':
										formats.append(td.text.strip().replace('.', ''))

								# Go through the different areas (tiles)
								for tile in tiles:
									# Get the tile name
									id = tile['alt']
									# Get the metadata URL
									mdata_link = tile['href']
									mdata_url = urlparse.urljoin(area_url, mdata_link)

									title_str = "%s - %s: %s" % (parent_title, area_title, id)

									formats_str = "|".join(formats)

									download_info = shared.get_download_text(formats)
									download_str, access_str = download_info.split('|')

									# print "Title: "
									# print title_str
									# print "Formats: " + str(formats_str)
									# print "Metadata URL: " + str(mdata_url)
									# print "Download: " + str(download_str)
									# print "Access: " + str(access_str)

									# Add all geospatial data to the pt_csv
									pt_csv.add('Source', source)
									pt_csv.add('Title', title_str)
									pt_csv.add('Access', access_str)
									pt_csv.add('Type', 'Vector Data')
									pt_csv.add('Download', download_str)
									pt_csv.add('Web Page URL', area_url)
									pt_csv.add('Metadata URL', mdata_url)
									pt_csv.add('Spatial Reference', sp_str)
									pt_csv.add('Available Formats', formats_str)

									pt_csv.write_dataset()

						print
				###########################################################
				# Get the remaining links on the Cadastral page

				# Create a list of the texts found in the links
				link_texts = ['Cadastral Index', 'Rural', 'Rural_cities', 'Townships',
							  'Winnipeg', 'All Cadastral Polygons', 'All Cadastral Lines',
							  'All Cadastral Text']
				links_table = rec_soup.find_all('table')[0]

				# Cycle through each link
				for idx, text in enumerate(link_texts):
					msg = "Extracting %s of %s records" % (idx + 1, len(link_texts))
					shared.print_oneliner(msg)
							
					anchor = bsoup.find_tags_containing(links_table, text, 'a')
					title_str = "%s - %s" % (parent_title, shared.clean_text(anchor.text))
					shp_url = shared.get_anchor_url(anchor, page_url)

					# Add all geospatial data to the pt_csv
					pt_csv.add('Source', source)
					pt_csv.add('Title', title_str)
					pt_csv.add('Access', 'Download/Web Accessible')
					pt_csv.add('Type', 'Vector Data')
					pt_csv.add('Download', shp_url)
					pt_csv.add('Web Page URL', page_url)
					pt_csv.add('Spatial Reference', sp_str)
					pt_csv.add('Available Formats', 'SHP')

					pt_csv.write_dataset()
					
				print

				pt_csv.close_csv()

			elif parent_title == 'Digital Elevation Models':

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				# Fix the errors on the page
				html_code = unicode(rec_soup)
				#print "HTML: %s" % html_code.find('Coverage Overview</font></b></td></tr></tbody></table></br></br></br></br></div></div></div></div></div></body></html>')
				html_code = html_code.replace("Coverage Overview</font></b></td></tr></tbody></table></br></br></br></br></div></div></div></div></div></body></html>",
											  "Coverage Overview</font></b></td>")
				rec_soup = BeautifulSoup(html_code, 'html.parser')

				###########################################################
				# Start with tables on the Digital Elevation Models page

				table_list = rec_soup.find_all('table')

				# FOR DEBUG ONLY
				#html_f = codecs.open('html_text.html', encoding='utf_8_sig', mode="w")
				#html_f.write(unicode(rec_soup))
				#html_f.close()

				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc metadata'
				replace_vals = [('CONTOURS', 'SHP')]
				unique_cols['ignore_cols'] = ['version', 'update info']
				ignore_rows = ['Contours']

				for idx, table in enumerate(table_list):
					
					rec_list = self.process_table(parent_title, table, page_url, unique_cols,
												  ignore_rows=ignore_rows,
												  replace_vals=replace_vals)

					#print rec_list

					# Add the table on the DEM page to the CSV
					for idx, rec in enumerate(rec_list):
						msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
						shared.print_oneliner(msg)
						for k, v in rec.items():
							pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.write_dataset()
					print

				###########################################################
				# Get the Red River sites
				redriver_font = bsoup.find_tags_containing(rec_soup, 'Red River LiDAR Contours', 'font')
				parent_td = redriver_font.parent.parent
				redriver_tds = parent_td.find_next_siblings('td')
				#print redriver_tds
				rrmdata_col = redriver_tds[1]
				rrmdata_a = rrmdata_col.find('a')
				rrmdata_url = shared.get_anchor_url(rrmdata_a, page_url)

				rr_soup = bsoup.get_soup(rrmdata_url)
				areas = rr_soup.find_all('area')

				# Get the title of the page
				title_font = rr_soup.find('font', attrs={'size': '4'})
				title = title_font.text
				title = shared.clean_text(title)

				# Get a list of formats
				formats = []
				b_doc = rr_soup.find('b', text='.DOC')
				p_doc = b_doc.parent
				td_doc = p_doc.parent
				tr = td_doc.parent
				td_list = tr.find_all('td')
				for td in td_list:
					if not td.text == '.DOC':
						formats.append(td.text.strip().replace('.', ''))

				for idx, area in enumerate(areas):
					msg = "Extracting area %s of %s from map" % (idx + 1, len(areas))
					shared.print_oneliner(msg)
				
					# Get the area name
					id = area['alt']
					# Get the metadata URL
					mdata_url = shared.get_anchor_url(area, rrmdata_url)

					title_str = "%s - %s: %s" % (parent_title, title, id)

					formats_str = "|".join(formats)

					download_info = shared.get_download_text(formats)
					download_str, access_str = download_info.split('|')

					mdata_info = self.get_metadata(mdata_url)

					for k, v in mdata_info.items():
						pt_csv.add(k, v)

					# Add all geospatial data to the pt_csv
					pt_csv.add('Source', source)
					pt_csv.add('Title', title_str)
					pt_csv.add('Access', access_str)
					pt_csv.add('Type', 'Vector Data')
					pt_csv.add('Download', download_str)
					pt_csv.add('Web Page URL', rrmdata_url)
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Spatial Reference', sp_str)
					pt_csv.add('Available Formats', formats_str)

					pt_csv.write_dataset()
					
				print

				###########################################################
				# Next get the LIDAR site

				lidar_font = rec_soup.find('font', text='LIDAR(Various')
				lidar_a = lidar_font.parent
				lidar_url = shared.get_anchor_url(lidar_a, page_url)

				lidar_soup = bsoup.get_soup(lidar_url)

				tables = lidar_soup.find_all('table', attrs={'border': '2'})

				# Get the first table on the LIDAR page
				unique_cols['mdata_col'] = 'metadata'
				unique_cols['ignore_cols'] = ['coverage overview']
				replace_vals = [('Contours', 'SHP')]
				table1 = self.process_table(parent_title, tables[0], lidar_url, unique_cols, replace_vals=replace_vals)

				#print table1

				# Add the table on the DEM page to the CSV
				for idx, row in enumerate(table1):
					msg = "Extracting %s of %s records" % (idx + 1, len(table1))
					shared.print_oneliner(msg)
				
					for k, v in row.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
				
				print

				# Get the second table on the LIDAR page
				unique_cols['mdata_col'] = '.doc metadata'
				unique_cols['ignore_cols'] = ['coverage overview']
				table1 = self.process_table(parent_title, tables[1], lidar_url, unique_cols, replace_vals=replace_vals)

				#print table1

				# Add the table on the DEM page to the CSV
				for idx, row in enumerate(table1):
					msg = "Extracting %s of %s records" % (idx + 1, len(table1))
					shared.print_oneliner(msg)
					
					for k, v in row.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()

				pt_csv.close_csv()
				
				print

			elif parent_title == 'Digital Imagery':
				#print "Digital Imagery"

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				table = rec_soup.find('table', attrs={'border': '2'})

				rows = table.find_all('tr')

				for idx, row in enumerate(rows):
					
					# Get the anchor in this row
					a = row.a
					if a is None: continue

					a_text = shared.clean_text(a.text)

					# Get a list of columns from the row
					cols = row.find_all('td')

					# Get the description from the third column of the row
					desc_str = shared.clean_text(cols[2].text)

					# Get the metadata from the second column of the row
					mdata_col = cols[1]
					mdata_info = None
					mdata_a = mdata_col.find('a')
					if mdata_a is not None:
						mdata_url = shared.get_anchor_url(mdata_a, page_url)
						mdata_info = self.get_metadata(mdata_url)

					# If the link is not to a page (.html), then skip it
					sub_url = shared.get_anchor_url(a, page_url)
					if sub_url.find('.html') == -1: continue

					sub_soup = bsoup.get_soup(sub_url)

					if a_text == 'Capital Region 50cm' or \
							a_text == 'Nickel Belt' or \
							a_text == 'Blanshard North' or \
							a_text == 'Blanshard South' or \
							a_text == 'North Cypress' or \
							a_text == 'North Norfolk' or \
							a_text == 'Park North' or \
							a_text == 'Upper Assiniboine North' or \
							a_text == 'Upper Assiniboine South' or \
							a_text == 'Vermillion River':

						# These pages contain a map with links
						#   to the datasets

						a_text = a_text.replace(" 50cm", "")

						####################################################################################
						# Get all the shapefile links on the page
						if a_text.find('Blanshard') > -1:
							shp_titles = ['%s ortho grid in SHAPE format' % a_text,
								  'Blanshard (North & South - all)']
						else:
							shp_titles = ['%s ortho grid in SHAPE format' % a_text]
						down_res = bsoup.get_link_datasets(sub_soup, shp_titles, sub_url, 'a')

						for idx, res in enumerate(down_res):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(down_res), a_text)
							shared.print_oneliner(msg)
						
							for k, v in res.items():
								pt_csv.add(k, v)

							# Add the metadata info to the CSV file
							if mdata_info is not None:
								for k, v in mdata_info.items():
									pt_csv.add(k, v)

							if res['Available Formats'] == 'SID' or \
											res['Available Formats'] == 'TIF':
								dtype = 'Raster Data'
							else:
								dtype = 'Vector Data'

							# Add all geospatial data to the pt_csv
							pt_csv.add('Source', source)
							pt_csv.add('Type', dtype)
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()

						print
						############################################################################
						# Get the map links

						area_map = sub_soup.find('map')

						# Get the world Zip file for the datasets
						world_txt = '%s Ortho World files (.SDW)' % a_text
						world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

						# Get the map info on the sub page
						area_map_info = self.process_map(area_map, sub_url, a_text)

						# Add the map info to the CSV file
						for idx, ds in enumerate(area_map_info):
							msg = "Extracting %s of %s areas on map" % (idx + 1, len(area_map_info))
							shared.print_oneliner(msg)
						
							for k, v in ds.items():
								pt_csv.add(k, v)

							# Add the metadata info to the CSV file
							if mdata_info is not None:
								for k, v in mdata_info.items():
									pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.add('Available Formats', 'SID')
							pt_csv.add('Type', 'Raster Data')
							pt_csv.add('Description', desc_str)
							pt_csv.add('Data URL', world_url)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)
							pt_csv.add('Notes', notes_str)

							pt_csv.write_dataset()
							
						print

					elif a_text == '1Km Tiles':
						# Get the 1km tiles

						#print "1km tiles"

						#########################################################
						# First, process the map on the 1km tiles page
						idx_map = sub_soup.find('map')
						map_info = self.process_map(idx_map, sub_url)

						for idx, area in enumerate(map_info):
							# Each link on the map goes to another page with a
							#   map

							# Get the download URL which is actually the sub page
							area_url = area['Download']
							area_soup = bsoup.get_soup(area_url)
							area_map = area_soup.find('map')

							#####################################################
							# Get all the image datasets from the map on the
							#   sub page

							# Get the world Zip file for the datasets
							world_txt = 'World Files required'
							world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

							# Get the map info on the sub page
							area_map_info = self.process_map(area_map, area['Download'], '1km Ortho')

							# Add the map info to the CSV file
							for idx, ds in enumerate(area_map_info):
								msg = "Extracting %s of %s areas in %s" % (idx + 1, len(area_map_info), a_text)
								shared.print_oneliner(msg)
							
								for k, v in ds.items():
									pt_csv.add(k, v)

								if mdata_info is not None:
									for k, v in mdata_info.items():
										pt_csv.add(k, v)

								pt_csv.add('Source', source)
								pt_csv.add('Available Formats', 'TIF')
								pt_csv.add('Type', 'Raster Data')
								pt_csv.add('Data URL', world_url)
								pt_csv.add('Description', desc_str)
								pt_csv.add('Metadata URL', mdata_url)
								pt_csv.add('Spatial Reference', sp_str)
								pt_csv.add('Notes', notes_str)

								pt_csv.write_dataset()
								
							print

					elif a_text == '5Km Tiles':

						#########################################################
						# Get all the shapefile links on the page
						shp_titles = ['Download 5K Ortho grid in SHAPE format',
									  'Download Township Grid in SHAPE format']
						down_res = bsoup.get_link_datasets(sub_soup, shp_titles, sub_url)

						for idx, res in enumerate(down_res):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(down_res), a_text)
							shared.print_oneliner(msg)
						
							for k, v in res.items():
								pt_csv.add(k, v)

							# Add all geospatial data to the pt_csv
							pt_csv.add('Source', source)
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()
						
						print

						# Get the world Zip file for the datasets
						world_txt = 'Download "world files" - (.tfw)'
						world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

						#########################################################
						# Process the map on the 5km tiles page
						idx_map = sub_soup.find('map')
						map_info = self.process_map(idx_map, sub_url)

						for area in map_info:
							# Each link on the map goes to another page with a
							#   map

							# Get the download URL which is actually the sub page
							sub_url = area['Download']
							if sub_url.find('.html') > -1:
								#####################################################
								# Get all the image datasets from the map on the
								#   sub page

								area_soup = bsoup.get_soup(sub_url)
								area_map = area_soup.find('map')

								# Get the map info on the sub page
								area_map_info = self.process_map(area_map, area['Download'], '5km Ortho')

								# Add the map info to the CSV file
								for idx, ds in enumerate(area_map_info):
									msg = "Extracting %s of %s areas in %s" % (idx + 1, len(area_map_info), a_text)
									shared.print_oneliner(msg)
								
									for k, v in ds.items():
										pt_csv.add(k, v)

									if mdata_info is not None:
										for k, v in mdata_info.items():
											pt_csv.add(k, v)

									pt_csv.add('Source', source)
									pt_csv.add('Available Formats', 'TIF')
									pt_csv.add('Type', 'Raster Data')
									pt_csv.add('Data URL', world_url)
									pt_csv.add('Description', desc_str)
									pt_csv.add('Metadata URL', mdata_url)
									pt_csv.add('Spatial Reference', sp_str)
									pt_csv.add('Notes', notes_str)

									pt_csv.write_dataset()
									
								print

					elif a_text == 'Mosaics - MrSid':
						#########################################################
						# Get all the shapefile links on the page

						shp_titles = ['Download MrSid Ortho grid in SHAPE format',
									  'Download 5K Ortho grid in SHAPE format',
									  'Download Township grid in SHAPE format']
						down_res = bsoup.get_link_datasets(sub_soup, shp_titles, sub_url)

						for idx, res in enumerate(down_res):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(down_res), a_text)
							shared.print_oneliner(msg)
						
							for k, v in res.items():
								pt_csv.add(k, v)

							# Add all geospatial data to the pt_csv
							pt_csv.add('Source', source)
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()
						
						print

						#########################################################
						# Now get all the image datasets from the map on the page

						# Get the world Zip file for the datasets
						world_txt = 'world files'
						world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

						area_map = sub_soup.find('map')

						# Get the map info on the sub page
						area_map_info = self.process_map(area_map, sub_url, 'MrSid  Mosaic Ortho')

						# Add the map info to the CSV file
						for idx, ds in enumerate(area_map_info):
							msg = "Extracting %s of %s areas in %s" % (idx + 1, len(area_map_info), a_text)
							shared.print_oneliner(msg)
						
							for k, v in ds.items():
								pt_csv.add(k, v)

							# Add the metadata info to the CSV file
							if mdata_info is not None:
								for k, v in mdata_info.items():
									pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.add('Available Formats', 'MrSID')
							pt_csv.add('Type', 'Raster Data')
							pt_csv.add('Spatial Reference', sp_str)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Data URL', world_url)
							pt_csv.add('Notes', notes_str)

							pt_csv.write_dataset()
							
						print

					elif a_text == 'Nickel Belt - MrSid':
						print "\nExtracting 1 record in %s" % a_text
					
						# Get the world Zip file for the datasets
						world_txt = '.SDW'
						world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

						table = sub_soup.find('table')

						ignore_rows = ['Nickel Belt World File - All']
						table_rows = self.process_table(parent_title, table, sub_url, ignore_rows=ignore_rows)

						for res in table_rows:
							for k, v in res.items():
								pt_csv.add(k, v)

						# Add the metadata info to the CSV file
						if mdata_info is not None:
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Data URL', world_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Notes', notes_str)

						pt_csv.write_dataset()

					elif a_text == 'IRS':
						print "\nExtracting 1 record in %s" % a_text
					
						# Get the world Zip file for the datasets
						world_txt = '.SDW'
						world_url, notes_str = self.get_world_link(sub_soup, sub_url, world_txt)

						table = sub_soup.find('table', attrs={'border': '1'})

						pt_csv.add('Description', desc_str)

						unique_cols = collections.OrderedDict()
						unique_cols['mdata_col'] = '.doc'
						unique_cols['ignore_cols'] = ['.gif', '.sdw']
						table_rows = self.process_table(parent_title, table, sub_url, unique_cols)

						for res in table_rows:
							for k, v in res.items():
								pt_csv.add(k, v)

						# Add the metadata info to the CSV file
						if mdata_info is not None:
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Data URL', world_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Notes', notes_str)

						pt_csv.write_dataset()

					elif a_text == 'LandSat_7':
						# The LandSat_7 page contains a map with links
						#   to other pages containing download links

						# Get all the shapefile links on the page
						shp_titles = ['Download LandSat7 WRS grid in SHAPE format',
									  'Download NTS grid in SHAPE format',
									  'Download 5K Ortho grid in SHAPE format',
									  'Download Township Grid in SHAPE format']
						down_res = bsoup.get_link_datasets(sub_soup, shp_titles, sub_url)

						for idx, res in enumerate(down_res):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(down_res), a_text)
							shared.print_oneliner(msg)
						
							for k, v in res.items():
								pt_csv.add(k, v)

							# Add all geospatial data to the pt_csv
							pt_csv.add('Source', source)
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()
							
						print

						# Process the map on the page
						idx_map = sub_soup.find('map')
						map_info = self.process_map(idx_map, sub_url)

						for idx, area in enumerate(map_info):
						
							# Get the download URL which is actually the sub page
							area_url = area['Download']
							if area_url.find('.html') > -1:
								area_soup = bsoup.get_soup(area_url, True)

								# Get the world Zip file for the datasets
								world_txt = '.SDW'
								world_url, notes_str = self.get_world_link(sub_soup, area_url, world_txt)

								# Locate a column which is green
								green_td = area_soup.find('td', attrs={'bgcolor': '#00FF00'})
								# Go to the parent row
								parent_tr = green_td.parent
								tbody = parent_tr.parent

								# Get all the rows
								rows = tbody.find_all('tr')
								#for row in rows:
								#	print ""
								#	print row
								#print "Number of rows: " + str(len(rows))

								title_row = rows[1].find_all('td')

								mdata_col = rows[2].find('td')
								#print mdata_row
								mdata_a = mdata_col.a
								mdata_url = shared.get_anchor_url(mdata_a, area_url)

								sp_col = rows[3].find('td')
								sp_a = sp_col.a
								sp_str = shared.get_anchor_url(sp_a, area_url)

								# Cycle through each column in the table
								for index, col in enumerate(title_row[1:]):
									msg = "Extracting %s of %s images in %s" % (index + 1, len(title_row[1:]), a_text)
									shared.print_oneliner(msg)
								
									# Get the title from the first row
									title = shared.clean_text(col.text)
									title_str = '%s - Band %s' % (parent_title, title)

									# Get the formats from the second and third row
									formats = []
									for row in rows[2:3]:
										cols = row.find_all('td')
										#print index
										#print "Number of columns: " + str(len(cols))
										format = shared.clean_text(cols[index + 1].text)
										format = format.replace('.', '').upper()
										download_a = cols[index + 1].a
										download_url = shared.get_anchor_url(download_a, area_url)
										if not format == '':
											formats.append(format)

									download_info = shared.get_download_text(formats, download_url)
									download_str, access_str = download_info.split('|')

									# print "Title: " + str(title_str)
									# print "Formats: " + str("|".join(formats))
									# print "Spatial Reference: " + str(sp_str)
									# print "Description: " + str(desc_str)

									# Add the metadata info to the CSV file
									if mdata_info is not None:
										for k, v in mdata_info.items():
											pt_csv.add(k, v)

									# Add all geospatial data to the pt_csv
									pt_csv.add('Source', source)
									pt_csv.add('Title', title_str)
									pt_csv.add('Access', access_str)
									pt_csv.add('Type', 'Raster Data')
									pt_csv.add('Download', download_str)
									pt_csv.add('Web Page URL', sub_url)
									pt_csv.add('Metadata URL', mdata_url)
									pt_csv.add('Spatial Reference', sp_str)
									pt_csv.add('Available Formats', "|".join(formats))
									pt_csv.add('Data URL', world_url)
									pt_csv.add('Notes', notes_str)

									pt_csv.write_dataset()
						
						print
					elif a_text == 'Lake_St_Martin_part1' or a_text == 'Lake_St_Martin_part2':

						print "\nExtracting 1 record in %s" % a_text
					
						formats = ['SID']
						download_info = shared.get_download_text(sub_url)
						download_str, access_str = download_info.split('|')

						# Add the metadata info to the CSV file
						if mdata_info is not None:
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						# Add all geospatial data to the pt_csv
						pt_csv.add('Source', source)
						pt_csv.add('Title', title_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Type', 'Raster Data')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', page_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Available Formats', "|".join(formats))

						pt_csv.write_dataset()

					elif a_text == 'Refresh - (2007-2014) Color':

						#########################################################
						# Get all the shapefile links on the page

						shp_titles = ['Ortho refresh Years 1&2 (2007-2009) 1m pixel MrSid Color 5Km tiles',
									  'Ortho refresh Years 3&4 (2008-2010) 1m pixel MrSid Color 5Km tiles',
									  'Refresh 2007-2014 Flight Lines (.SHP)',
									  'Ortho refresh Year 7 Eastern Block NE_N 1m MrSID Mosaic',
									  'Ortho refresh Year 7 Eastern Block NE_S 1m MrSID Mosaic',
									  'Ortho refresh Year 7 Eastern Block SE 1m MrSID Mosaic']
						down_res = bsoup.get_link_datasets(sub_soup, shp_titles, sub_url, 'a')

						for idx, res in enumerate(down_res):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(down_res), a_text)
							shared.print_oneliner(msg)
						
							for k, v in res.items():
								pt_csv.add(k, v)

							if res['Available Formats'] == 'SID' or \
									res['Available Formats'] == 'TIF':
								dtype = 'Raster Data'
							else:
								dtype = 'Vector Data'

							# Add the metadata info to the CSV file
							if mdata_info is not None:
								for k, v in mdata_info.items():
									pt_csv.add(k, v)

							# Add all geospatial data to the pt_csv
							pt_csv.add('Source', source)
							pt_csv.add('Type', dtype)
							pt_csv.add('Web Page URL', sub_url)
							pt_csv.add('Description', desc_str)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()
							
						print

						# Find the <tr> with a certain text
						tr = bsoup.find_tags_containing(sub_soup, 'MrSid color Mosaic tiles',
													   'tr')

						title_str = ''
						counter = 0
						while title_str.find('se  1.0m') == -1:
							counter += 1
							msg = "Extracting %s in %s" % (counter, a_text)
							shared.print_oneliner(msg)
						
							# Divide the row into the columns
							cols = tr.find_all('td')

							# Get the title from the second column
							title_str = "%s - %s" % (parent_title, bsoup.get_text(cols[1]))

							# Get the world file from the third column
							world_a = cols[2].a
							world_url = shared.get_anchor_url(world_a, sub_url)
							notes_str = "The 'Data URL' contains a link to a Zip file which " \
										"contains the World file for this dataset."

							# Add the metadata info to the CSV file
							if mdata_info is not None:
								for k, v in mdata_info.items():
									pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.add('Title', title_str)
							pt_csv.add('Available Formats', 'SID')
							pt_csv.add('Type', 'Raster Data')
							pt_csv.add('Description', desc_str)
							pt_csv.add('Data URL', world_url)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)
							pt_csv.add('Notes', notes_str)

							pt_csv.write_dataset()

							tr = tr.find_next_sibling('tr')

							#print title_str
							#print title_str.find('se  1.0m')
							
						print

					elif a_text == 'Upper Assiniboine River':
						table = sub_soup.find('table', attrs={'cellspacing': '1'})

						a_list = table.find_all('a')
						for idx, a in enumerate(a_list):
							msg = "Extracting %s of %s records in %s" % (idx + 1, len(a_list), a_text)
							shared.print_oneliner(msg)
						
							title_str = "%s - %s" % (parent_title, shared.clean_text(a.text))
							download_url = shared.get_anchor_url(a, sub_url)
							formats = ['SHP']
							
							download_info = shared.get_download_text(formats, download_url)
							download_str, access_str = download_info.split('|')

							# Add all geospatial data to the pt_csv
							pt_csv.add('Title', title_str)
							pt_csv.add('Access', access_str)
							pt_csv.add('Type', 'Raster Data')
							pt_csv.add('Download', download_str)
							pt_csv.add('Web Page URL', page_url)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)
							pt_csv.add('Available Formats', "|".join(formats))
							
						print

					elif a_text == '5K Ortho grid in .SHP format' or \
							a_text == '5K Ortho grid in KMZ format' or \
							a_text == 'Township Grid in SHP format':
							
						print "\nExtracting 1 record in %s" % a_text

						if sub_url.find('5K Ortho grid') > -1:
							title_str = '%s - 5K Ortho grid' % parent_title
							formats = ['SHP', 'KMZ']
						else:
							title_str = '%s - Township Grid' % parent_title
							formats = ['SHP']

						download_info = shared.get_download_text(formats, sub_url)
						download_str, access_str = download_info.split('|')

						# Add the metadata info to the CSV file
						if mdata_info is not None:
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						# Add all geospatial data to the pt_csv
						pt_csv.add('Source', source)
						pt_csv.add('Title', title_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Type', 'Raster Data')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', page_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Available Formats', "|".join(formats))

						pt_csv.write_dataset()

				print
			elif parent_title == 'Forest Inventory':
				#print 'Forest Inventory'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				table_list = rec_soup.find_all('table')

				#################################################################
				# Get the fires table
				fires_table = table_list[0]
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif', 'update info']
				ignore_rows = ['Boundaries']
				replace_vals = [('.GEO', 'FGDB')]
				rec_list = self.process_table(parent_title, fires_table, page_url, unique_cols,
											  ignore_rows=ignore_rows, replace_vals=replace_vals)

				#print rec_list
				#answer = raw_input("Press enter...")

				# Add the table on the Forest Inventory page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records in %s" % (idx + 1, len(rec_list), parent_title)
					shared.print_oneliner(msg)
				
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
				
				print

				#################################################################
				# Get the inventory table
				inv_table = table_list[1]

				# The table has to be divided into two by its blank middle column
				#   The table_to_dict will append a number to any duplicate column names
				inv_rows = shared.table_to_dict(inv_table, 0, start_row=1)
				# Create the lists which will store the two halves of the table
				first_half = []
				sec_half = []
				for row in inv_rows:
					# Create a list of tuples containing only columns with a '1'
					first_cols = [(key[:len(key)-1], value) for key, value in row.items() if '1' in key.lower()]
					# Convert the list of tuples to a dictionary
					first_cols_dict = dict((x, y) for x, y in first_cols)
					# Add the dictionary to the first_half list of rows
					first_half.append(first_cols_dict)
					# Create a list of tuples containing only columns with a '2'
					sec_cols = [(key[:len(key)-1], value) for key, value in row.items() if '2' in key.lower()]
					# Convert the list of tuples to a dictionary
					sec_cols_dict = dict((x, y) for x, y in sec_cols)
					# Add the dictionary to the sec_half list of rows
					sec_half.append(sec_cols_dict)

				all_rows = first_half + sec_half

				for idx, row in enumerate(all_rows):
					msg = "Extracting dataset %s of %s" % (idx + 1, len(all_rows))
					shared.print_oneliner(msg)
				
					# Get the title
					title_str = "%s - %s" % (parent_title, shared.clean_text(row['fmu'].text))
					if not title_str == '':
						# Get the date
						date_str = shared.clean_text(row['date'].text)

						# Get the metadata URL
						mdata = row['.doc']
						mdata_a = mdata.find('a')
						mdata_url = shared.get_anchor_url(mdata_a, page_url)

						# If the metadata is an HTML
						if mdata_url.find('.html') > -1:
							mdata_info = self.get_metadata(mdata_url)

							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						# Get the formats and downloads
						formats = []
						downloads = []
						# Get the shapefile if applicable
						shp_format = shared.clean_text(row['.shp'].text)
						download_a = row['.shp'].find('a')
						download = shared.get_anchor_url(download_a, page_url)
						if not shp_format == '':
							formats.append('SHP')
							downloads.append(download)
						# Get the GEO if applicable
						geo_format = shared.clean_text(row['.geo'].text)
						download_a = row['.geo'].find('a')
						download = shared.get_anchor_url(download_a, page_url)
						if not geo_format == '':
							formats.append('FGDB')
							downloads.append(download)

						download_info = shared.get_download_text(formats, downloads)
						download_str, access_str = download_info.split('|')

						# print ""
						# print "Title: " + str(title_str)
						# print "Date: " + str(date_str)
						# print "Formats: " + str('|'.join(formats))
						# print "Metadata URL: " + str(mdata_url)

						# Add all geospatial data to the pt_csv
						pt_csv.add('Source', source)
						pt_csv.add('Title', title_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Type', 'Vector Data')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', page_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Available Formats', '|'.join(formats))

						pt_csv.write_dataset()

				print
				#################################################################
				# Get the shapefile downloads at the bottom of page

				# Get the RFQ shapefile
				rfq_a = rec_soup.find('a', text='RFQ_shp')
				rfq_url = shared.get_anchor_url(rfq_a, page_url)

				title_str = "%s - %s" % (parent_title, shared.clean_text(rfq_a.text))
				access_str = 'Download/Web Accessible'
				download_str = rfq_url

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', source)
				pt_csv.add('Title', title_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Download', download_str)
				pt_csv.add('Web Page URL', page_url)
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

				# Get the FRI lines
				fri_a = bsoup.find_tags_containing(rec_soup, 'FRI Lines', 'a')
				fri_url = shared.get_anchor_url(fri_a, page_url)

				title_str = "%s - %s" % (parent_title, shared.clean_text(fri_a.text))
				access_str = 'Download/Web Accessible'
				download_str = fri_url

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', source)
				pt_csv.add('Title', title_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Download', download_str)
				pt_csv.add('Web Page URL', page_url)
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

			elif parent_title == 'Geology Mapping':
				#print 'Geology Mapping'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				# Get the link to the 1:1,000,000 table
				million_a = bsoup.find_tags_containing(rec_soup, '1: 1,000,000 Geology', 'a')
				million_url = shared.get_anchor_url(million_a, page_url)

				million_soup = bsoup.get_soup(million_url)

				table = million_soup.find('table', attrs={'border': '2'})

				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc metadata'
				unique_cols['ignore_cols'] = ['.gif overview', '.tif download']
				rec_list = self.process_table(parent_title, table, page_url, unique_cols)

				# Add the table on the Forest Inventory page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
					shared.print_oneliner(msg)
				
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
					
				print

			elif parent_title == 'Hydrography':
				#print 'Hydrology'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				###################################################################
				# Start with the Designated Drain Watercourses

				# Get the Designated Drain Watercourses link
				drain_b = rec_soup.find('b', text='Designated Drain Watercourses')
				drain_a = drain_b.find_next_sibling('a')
				drain_url = shared.get_anchor_url(drain_a, page_url)

				# Get the soup
				drain_soup = bsoup.get_soup(drain_url)

				# Get the 2 tables on the drain page
				tables = drain_soup.find_all('table', attrs={'border': '2'})

				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif']
				for idx, table in enumerate(tables):
					msg = "Extracting table %s of %s" % (idx + 1, len(tables))
					shared.print_oneliner(msg)
				
					rec_list = self.process_table(parent_title, table, page_url, unique_cols)

					# Add the table of the Designated Drain Watercourses page to the CSV
					for rec in rec_list:
						for k, v in rec.items():
							pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.write_dataset()
				print

				###################################################################
				# Next, the Basins & Watersheds of Manitoba

				# Get the Basins & Watersheds of Manitoba link
				basins_b = rec_soup.find('b', text='Basins & Watersheds of Manitoba')
				basins_a = basins_b.find_next_sibling('a')
				basins_url = shared.get_anchor_url(basins_a, page_url)

				# Get the soup
				basins_soup = bsoup.get_soup(basins_url)

				# Get the 2 tables on the drain page
				tables = basins_soup.find_all('table', attrs={'border': '2'})

				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif']
				for idx, table in enumerate(tables):
					msg = "Extracting table %s of %s" % (idx + 1, len(tables))
					shared.print_oneliner(msg)
					
					rec_list = self.process_table(parent_title, table, page_url, unique_cols)

					# Add the table of the Basins & Watersheds of Manitoba page to the CSV
					for rec in rec_list:
						for k, v in rec.items():
							pt_csv.add(k, v)

						pt_csv.add('Source', source)
						pt_csv.write_dataset()
				print

				###################################################################
				# The Floods page

				# Get the Floods link
				floods_a = rec_soup.find('a', text='Floods')
				floods_url = shared.get_anchor_url(floods_a, page_url)

				floods_soup = bsoup.get_soup(floods_url)

				# Get the Red River flood table
				redriver_table = floods_soup.find('table', attrs={'id': 'table1'})
				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif']
				title_prefix = 'Red River Floods'
				rr_list = self.process_table(parent_title, redriver_table, page_url, unique_cols,
											 title_prefix=title_prefix)

				# Get the Assiniboine River flood table
				assiniboine_table = floods_soup.find('table', attrs={'id': 'table2'})
				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif']
				title_prefix = 'Assiniboine River Floods'
				assiniboine_list = self.process_table(parent_title, assiniboine_table, page_url,
															unique_cols,
															title_prefix=title_prefix)

				# Combine both table results
				rec_list = rr_list + assiniboine_list

				# Add the table of the Red River floods page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records in %s" % (idx + 1, len(rec_list), parent_title)
					shared.print_oneliner(msg)
					
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
					
				print

				###################################################################
				# The Seamless Water page

				# Get the Seamless Water link
				seam_a = bsoup.find_tags_containing(rec_soup, 'Seamless Water', 'a')
				seam_url = shared.get_anchor_url(seam_a, page_url)

				seam_soup = bsoup.get_soup(seam_url)

				# Get the Seamless Water table
				table = seam_soup.find('table', attrs={'id': 'table2'})
				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['ignore_cols'] = ['.gif']
				rec_list = self.process_table(parent_title, table, page_url, unique_cols)

				# Add the table of the Seamless Water page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
					shared.print_oneliner(msg)
				
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
					
				print

			elif parent_title == 'Municipal Maps':
				#print 'Municipal Maps'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				###################################################################
				# Start with the Municipal maps page

				munic_table = rec_soup.find('table')

				# Get the metadata url
				h3_font = rec_soup.find('font', text='Municipal Maps ')
				h3 = h3_font.parent
				p = h3.find_next_sibling('p')
				mdata_a = p.find('a')
				mdata_url = shared.get_anchor_url(mdata_a, page_url)

				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['ignore_cols'] = ['.pdf']
				rec_list = self.process_table(parent_title, munic_table, page_url, unique_cols)

				desc_str = "Municipal maps produced by Manitoba Infrastructure and Transportation, Highway Planning " \
						   "and Design Branch, Drafting Section."

				# Add the table of the Designated Drain Watercourses page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
					shared.print_oneliner(msg)
				
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Description', desc_str)

					pt_csv.write_dataset()
					
				print

				###################################################################
				# Get the datasets before amalgamation

				# Get the before amalgamation page's URL
				amal_a = bsoup.find_tags_containing(rec_soup, 'municipal amalgamation', 'a')
				amal_url = shared.get_anchor_url(amal_a, page_url)

				# Get the before amalgamation page's soup
				amal_soup = bsoup.get_soup(amal_url)

				# Get the table of datasets
				amal_table = amal_soup.find('table')

				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['ignore_cols'] = ['.gif']
				rec_list = self.process_table(parent_title, amal_table, amal_url, unique_cols, start_row=6)

				# Add the table of the before amalgamation page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
					shared.print_oneliner(msg)
					
					for k, v in rec.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Description', desc_str)

					pt_csv.write_dataset()
					
				print

			elif parent_title == 'Quarter Section Grids':
				#print 'Quarter Section Grids'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				###################################################################
				# Get the Original Southern Grid
				south_font = bsoup.find_tags_containing(rec_soup, 'Original Southern Grid', 'font')
				south_a = south_font.parent
				south_url = shared.get_anchor_url(south_a, page_url)

				# Remove <br> between Land Use Maps and Municipal Maps
				south_page = shared.open_webpage(south_url)
				before_txt = '</CENTER></A>'
				after_txt = "</A></CENTER>"
				south_content = south_page.read()
				#print south_content.find(before_txt)
				south_content = south_content.replace(before_txt, after_txt)

				# Get the southern grid soup
				south_soup = BeautifulSoup(south_content, 'html.parser')

				# Get the southern grid table
				south_table = south_soup.find('table', attrs={'border': '2'})

				# Set the unique_cols
				unique_cols = collections.OrderedDict()
				unique_cols['mdata_cols'] = '.doc metadata'
				unique_cols['ignore_cols'] = ['.gif overview']
				ignore_rows = ['Go to top']
				rec_list = self.process_table(parent_title, south_table, south_url, unique_cols, ignore_rows=ignore_rows)

				# Add the table of the southern grid page to the CSV
				for idx, rec in enumerate(rec_list):
					msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
					shared.print_oneliner(msg)
					
					for k, v in rec.items():
						if k == 'Title':
							if v == 'All items listed below in one file':
								v = 'Entire Southern Grid'
						pt_csv.add(k, v)

					pt_csv.add('Source', source)
					pt_csv.write_dataset()
					
				print

				###################################################################
				# Get the Manitoba Reference Grid
				ref_a = bsoup.find_tags_containing(rec_soup, 'Manitoba Reference Grid', 'a')
				ref_url = shared.get_anchor_url(ref_a, page_url)
				mdata_url = ref_url.replace("shp", "meta")

				# Get the north grid soup
				ref_soup = bsoup.get_soup(ref_url)
				mdata_soup = bsoup.get_soup(mdata_url)

				# Get the metadata link from the map in mdata_soup
				mdata_area = mdata_soup.find('area')
				mdata_link = mdata_area['href']
				mdata_url = urlparse.urljoin(mdata_url, mdata_link)

				# Get the formats from the top table
				format_table = ref_soup.find('table', attrs={'border': '2'})
				columns = format_table.find_all('td')
				formats = [f.text.strip().replace('.', '') for f in columns[2:]]

				# Get the areas on the page and soup up there pages
				ref_areas = ref_soup.find_all('area')
				for idx, area in enumerate(ref_areas):
				
					msg = "Extracting %s of %s areas" % (idx + 1, len(ref_areas))
					shared.print_oneliner(msg)
				
					# Get the area link
					area_link = area['href']
					if area_link == '': continue
					area_url = urlparse.urljoin(ref_url, area_link)

					#print "area_link: '%s'" % area_link

					# Get the tile name from the shapefile filename
					base_name = os.path.basename(area_link)
					base_split = base_name.split("_")
					tile_name = base_split[2]

					# Get the metadata info
					mdata_info = self.get_metadata(mdata_url)
					if mdata_info is not None:
						for k, v in mdata_info.items():
							pt_csv.add(k, v)

					title_str = "%s - Reference Grid: %s" % (parent_title, tile_name)

					formats_str = "|".join(formats)

					download_info = shared.get_download_text(formats, area_url)
					download_str, access_str = download_info.split('|')

					# print "Title: "
					# print title_str
					# print "Formats: " + str(formats_str)
					# print "Metadata URL: " + str(mdata_url)
					# print "Download: " + str(download_str)
					# print "Access: " + str(access_str)

					# Add all geospatial data to the pt_csv
					pt_csv.add('Source', source)
					pt_csv.add('Title', title_str)
					pt_csv.add('Access', access_str)
					pt_csv.add('Type', 'Vector Data')
					pt_csv.add('Download', download_str)
					pt_csv.add('Web Page URL', ref_url)
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Spatial Reference', sp_str)
					pt_csv.add('Available Formats', formats_str)

					pt_csv.write_dataset()

				print
				###################################################################
				# Get the Northern Grid Master tiles
				north_a = bsoup.find_tags_containing(rec_soup, 'Master tiles', 'a')
				north_url = shared.get_anchor_url(north_a, page_url)

				#print "north_url: " + str(north_url)

				# Get the north grid soup
				north_soup = bsoup.get_soup(north_url.replace("shp", "meta"))

				# Get the formats from the top table
				format_table = north_soup.find('table', attrs={'border': '2'})
				columns = format_table.find_all('td')
				formats  = [f.text.strip().replace('.', '') for f in columns[2:]]

				# Get the areas on the page and soup up there pages
				north_areas = north_soup.find_all('area')
				for idx, area in enumerate(north_areas):
					msg = "Extracting %s of %s areas" % (idx + 1, len(north_areas))
					shared.print_oneliner(msg)
				
					# Get the tile name
					if area.has_attr('alt'):
						id = area['alt']
						#print "id: " + str(id)
						# Get the metadata URL
						mdata_link = area['href']
						mdata_url = urlparse.urljoin(north_url, mdata_link)

						# Get the metadata info
						mdata_info = self.get_metadata(mdata_url)
						if mdata_info is not None:
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						title_str = "%s - Northern Quarter Sections: %s" % (parent_title, id)

						formats_str = "|".join(formats)

						download_info = shared.get_download_text(formats)
						download_str, access_str = download_info.split('|')

						# Hard-code the description from the metadata
						desc_str = '''The above grid consists of a series of topologically structured Mastertiles and Subtiles.

						A Mastertile is 4 townships deep (24 miles) and extends province wide from the Manitoba/Saskatchewan boundary to the Manitoba/Ontario boundary. There are
						presently 25 Mastertiles in the grid with Mastertile 1 being the most northerly full 4 townships in the province and the Mastertile numbers increasing by one for each 4 townships one proceeds southwards.

						A Subtile is a subset of the Mastertile and generally consists of a block 4 townships deep by 10 ranges wide (40 townships in all). The actual number of townships in a Subtile will vary when a particular tile closes on a meridian, an interprovincial boundary, or large natural water body such as Hudson Bay. Each Subtile bears the Mastertile name followed by a letter designation. The letter "A"
						has been assigned to the most westerly Subtile with Subtiles "B", "C", "D" and so on occurring as one proceeds easterly.'''
						desc_str = desc_str

						# print "Title: "
						# print title_str
						# print "Formats: " + str(formats_str)
						# print "Metadata URL: " + str(mdata_url)
						# print "Download: " + str(download_str)
						# print "Access: " + str(access_str)

						# Add all geospatial data to the pt_csv
						pt_csv.add('Source', source)
						pt_csv.add('Title', title_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Type', 'Vector Data')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', north_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Available Formats', formats_str)

						pt_csv.write_dataset()

				print
				
				###################################################################
				# Get the Northern Grid Sub-tiles
				subtiles_a = bsoup.find_tags_containing(rec_soup, 'Sub-tiles', 'a')
				subtiles_url = shared.get_anchor_url(subtiles_a, page_url)

				subtiles_soup = bsoup.get_soup(subtiles_url)

				# Now get all the pages on the map to access the list of tiles
				subtiles_areas = subtiles_soup.find_all('area')
				for area in subtiles_areas:
					area_link = area['href']
					area_url = urlparse.urljoin(subtiles_url, area_link)

					# Get the formats from the top table
					format_table = north_soup.find('table', attrs={'border': '2'})
					columns = format_table.find_all('td')
					formats = [f.text.strip().replace('.', '') for f in columns[2:]]

					# Go through each area (tile) on subtiles page
					area_soup = bsoup.get_soup(area_url)
					subareas = area_soup.find_all('area')

					for idx, sub in enumerate(subareas):
						msg = "Extracting %s of %s areas" % (idx + 1, len(subareas))
						shared.print_oneliner(msg)
					
						sub_link = sub['href']
						sub_url = urlparse.urljoin(area_url, sub_link)

						# Get the tile name from the Zip file
						#tile_num = re.findall('[0-9][0-9][a-z]', sub_link)
						title_str = "%s - %s" % (parent_title, os.path.basename(sub_link).replace('_shp.zip', ''))

						# Hard-code the description from the metadata
						desc_str = '''The above grid consists of a series of topologically structured Mastertiles and Subtiles.

						A Mastertile is 4 townships deep (24 miles) and extends province wide from the Manitoba/Saskatchewan boundary to the Manitoba/Ontario boundary. There are
						presently 25 Mastertiles in the grid with Mastertile 1 being the most northerly full 4 townships in the province and the Mastertile numbers increasing by one for each 4 townships one proceeds southwards.

						A Subtile is a subset of the Mastertile and generally consists of a block 4 townships deep by 10 ranges wide (40 townships in all). The actual number of townships in a Subtile will vary when a particular tile closes on a meridian, an interprovincial boundary, or large natural water body such as Hudson Bay. Each Subtile bears the Mastertile name followed by a letter designation. The letter "A"
						has been assigned to the most westerly Subtile with Subtiles "B", "C", "D" and so on occurring as one proceeds easterly.'''

						# Get the metadata URL
						sub_mdata_url = area_url.replace('_shp', '_meta')
						sub_mdata_soup = bsoup.get_soup(sub_mdata_url)
						sub_mdata_area = sub_mdata_soup.find('area')
						mdata_link = sub_mdata_area['href']
						mdata_url = urlparse.urljoin(sub_mdata_url, mdata_link)

						formats_str = "|".join(formats)

						download_info = shared.get_download_text(formats)
						download_str, access_str = download_info.split('|')

						# print "Title: "
						# print title_str
						# print "Formats: " + str(formats_str)
						# print "Metadata URL: " + str(mdata_url)
						# print "Download: " + str(download_str)
						# print "Access: " + str(access_str)

						# Add all geospatial data to the pt_csv
						pt_csv.add('Source', source)
						pt_csv.add('Title', title_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Type', 'Vector Data')
						pt_csv.add('Download', download_str)
						pt_csv.add('Web Page URL', north_url)
						pt_csv.add('Metadata URL', mdata_url)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Available Formats', formats_str)

						pt_csv.write_dataset()

					print
				###################################################################
				# Get the Northern Grid Quarter Sections
				sect_a = bsoup.find_tags_containing(rec_soup, 'Quarter Sections', 'a')
				sect_url = shared.get_anchor_url(sect_a, page_url)
				access_str = 'Download/Web Accessible'

				title_str = "%s - %s" % (parent_title, shared.clean_text(sect_a.text))

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', source)
				pt_csv.add('Title', title_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Download', sect_url)
				pt_csv.add('Web Page URL', north_url)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

				###################################################################
				# Get the DLS corner points
				pnts_a = bsoup.find_tags_containing(rec_soup, 'corner points', 'a')
				pnts_url = shared.get_anchor_url(pnts_a, page_url)
				access_str = 'Download/Web Accessible'

				title_str = "%s - %s" % (parent_title, shared.clean_text(pnts_a.text))

				# Add all geospatial data to the pt_csv
				pt_csv.add('Source', source)
				pt_csv.add('Title', title_str)
				pt_csv.add('Access', access_str)
				pt_csv.add('Type', 'Vector Data')
				pt_csv.add('Download', pnts_url)
				pt_csv.add('Web Page URL', north_url)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Available Formats', 'SHP')

				pt_csv.write_dataset()

			elif parent_title == 'Soil Classification':
				#print 'Soil Classification'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				table = rec_soup.find('table', attrs={'border': '2'})
				a_list = table.find_all('a')

				for a in a_list:
				
					soil_url = shared.get_anchor_url(a, page_url)
					soil_soup = bsoup.get_soup(soil_url, True)

					a_text = shared.clean_text(a.text)

					if a_text.find('SoilAID') > -1:
						table = soil_soup.find('table', attrs={'border': '2'})

						table_rows = shared.table_to_dict(table, 0, start_row=6)

						#print table_rows

						for idx, row in enumerate(table_rows):
							msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
							shared.print_oneliner(msg)
						
							# Get the title and skip if 'Go to top'
							title_tag = row['block area']
							title_str = "%s - %s" % (parent_title, bsoup.get_text(title_tag))
							if title_str.find('Go to top') > -1: continue

							# Get the metadata info
							mdata_a = row['.doc'].a
							mdata_url = shared.get_anchor_url(mdata_a, soil_url)
							mdata_info = self.get_metadata(mdata_url)

							if isinstance(mdata_info, str):
								pt_csv.add('Notes', mdata_info)
							else:
								# Add the metadata info to the CSV file
								if mdata_info is not None:
									for k, v in mdata_info.items():
										pt_csv.add(k, v)

							# Set the formats
							formats = ['DXF', 'SHP', 'KMZ']

							# Set the download text and access text
							download_info = shared.get_download_text(formats)
							download_str, access_str = download_info.split('|')

							pt_csv.add('Source', source)
							pt_csv.add('Title', title_str)
							pt_csv.add('Available Formats', '|'.join(formats))
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Access', access_str)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()

							#######################################################################
							# Now get the drain dataset
							drain_kmz = row['.kmz drains']
							# Get the title
							drain_title = "%s - Drains" % title_str

							# Get the download
							drain_a = drain_kmz.a
							download_url = shared.get_anchor_url(drain_a, soil_url)

							# Set the formats
							drain_formats = ['DXF', 'SHP', 'KMZ']

							# Set the download text and access text
							download_info = shared.get_download_text(drain_formats, download_url)
							download_str, access_str = download_info.split('|')

							if isinstance(mdata_info, str):
								pt_csv.add('Notes', mdata_info)
							else:
								# Add the metadata info to the CSV file
								if mdata_info is not None:
									for k, v in mdata_info.items():
										pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.add('Title', drain_title)
							pt_csv.add('Available Formats', 'KMZ')
							pt_csv.add('Type', 'Vector Data')
							pt_csv.add('Access', access_str)
							pt_csv.add('Metadata URL', mdata_url)
							pt_csv.add('Spatial Reference', sp_str)

							pt_csv.write_dataset()

						print
					elif a.text.find('SoilSMUF') > -1:
						# Extract the Soil Map Unit File (SoilSMUF) by Municipality page
						table = soil_soup.find('table', attrs={'border': '2'})

						unique_cols = collections.OrderedDict()
						unique_cols['mdata_col'] = '.doc'
						unique_cols['ignore_cols'] = ['.gif']
						ignore_rows = ['SMUF Description', 'Go to top']
						rec_list = self.process_table(parent_title, table, soil_url, unique_cols, ignore_rows=ignore_rows)

						# Add the table on the Forest Inventory page to the CSV
						for idx, rec in enumerate(rec_list):
							msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
							shared.print_oneliner(msg)
						
							for k, v in rec.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.write_dataset()
							
						print
					elif a.text.find('Detailed Soil Map') > -1:
						# Extract the Detailed Soils (new - 2014) by Municipality page
						table = soil_soup.find('table', attrs={'border': '2'})

						unique_cols = collections.OrderedDict()
						unique_cols['mdata_col'] = '.doc'
						unique_cols['ignore_cols'] = ['.gif']
						ignore_rows = ['Detailed Soils', 'Go to top']
						rec_list = self.process_table(parent_title, table, soil_url, unique_cols, ignore_rows=ignore_rows)

						# Add the table on the Forest Inventory page to the CSV
						for idx, rec in enumerate(rec_list):
							msg = "Extracting %s of %s records" % (idx + 1, len(rec_list))
							shared.print_oneliner(msg)
							
							for k, v in rec.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.write_dataset()
							
						print

			elif parent_title == 'Spatial Referencing':
				#print 'Spatial Referencing'

				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				table = rec_soup.find('table', attrs={'id': 'table2'})

				unique_cols = collections.OrderedDict()
				unique_cols['mdata_col'] = '.doc'
				unique_cols['desc_col'] = 'description'

				table_rows = shared.table_to_dict(table, 0, start_row=2)

				for idx, row in enumerate(table_rows):
					msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
					shared.print_oneliner(msg)
				
					# Get the title of the dataset
					title_str = "%s - %s" % (parent_title, shared.clean_text(row['product'].text))

					if title_str.find('Diagrams') > -1:
						# The Township Diagrams are tiles
						formats_str = 'TIF'
						download_str = 'Multiple Downloads'
						access_str = 'Download/Web Accessible'
						desc_str = shared.clean_text(row['description'].text)
					else:

						# Get the metadata info
						mdata_a = row['.doc'].a
						mdata_url = shared.get_anchor_url(mdata_a, page_url)
						if not mdata_url == '':
							mdata_info = self.get_metadata(mdata_url)
							for k, v in mdata_info.items():
								pt_csv.add(k, v)

						# Get the description
						desc_str = shared.clean_text(row['description'].text)

						# Get the formats
						a_list = row['format'].find_all('a')
						formats = []
						downloads = []
						for a in a_list:
							link = a['href']
							url = shared.get_anchor_url(a, page_url)
							if link.find('html') == -1:
								formats.append(a.text.replace('.', ''))
								downloads.append(url)

						formats_str = '|'.join([f for f in formats if not f == ''])

						download_info = shared.get_download_text(formats)
						download_str, access_str = download_info.split('|')

					# print "Title: "
					# print title_str
					# print "Formats: " + str(formats_str)
					# print "Metadata URL: " + str(mdata_url)
					# print "Download: " + str(download_str)
					# print "Access: " + str(access_str)

					# Add all geospatial data to the pt_csv
					pt_csv.add('Source', source)
					pt_csv.add('Title', title_str)
					pt_csv.add('Description', desc_str)
					pt_csv.add('Access', access_str)
					pt_csv.add('Download', download_str)
					pt_csv.add('Web Page URL', page_url)
					pt_csv.add('Metadata URL', mdata_url)
					pt_csv.add('Spatial Reference', sp_str)
					pt_csv.add('Available Formats', formats_str)

					pt_csv.write_dataset()

				print
			elif parent_title == 'Topographic Maps':
				# Create the CSV file and determining category
				csv_fn = "MLI_%s_results" % fn_tag
				pt_csv = sh.PT_CSV(csv_fn, self)
				pt_csv.open_csv()

				table = rec_soup.find('table', attrs={'border': '2'})

				rows = table.find_all('tr')

				for row in rows:
				
					# Get the anchor in this row
					a = row.a
					if a is None: continue

					a_text = shared.clean_text(a.text)

					# Get a list of columns from the row
					cols = row.find_all('td')

					# Get the description from the second column of the row
					desc_str = shared.clean_text(cols[1].text)

					# If the link is not to a page (.html), then skip it
					sub_url = shared.get_anchor_url(a, page_url)
					if sub_url.find('.html') == -1: continue

					sub_soup = bsoup.get_soup(sub_url)

					if a_text == '1:20,000':
						# This page contains a map with links to more subpages
						#   with tables with datasets
						sub_map = sub_soup.find('map')
						map_info = self.process_map(sub_map, sub_url)

						for area in map_info:
						
							area_url = area['Download']
							area_soup = bsoup.get_soup(area_url)
							area_table = area_soup.find('table', attrs={'border': '2'})
							if area_table is None:
								area_table = area_soup.find('table', attrs={'border': '1'})

							# Process the table
							unique_cols = collections.OrderedDict()
							unique_cols['mdata_col'] = '.doc metadata'
							unique_cols['ignore_cols'] = ['.gif overview']
							table_rows = self.process_table(parent_title, area_table, area_url, unique_cols, title_prefix='Topo Map')

							# Add the table on the page to the CSV
							for idx, row in enumerate(table_rows):
								msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
								shared.print_oneliner(msg)
							
								# Add the description to the pt_csv
								pt_csv.add('Description', desc_str)

								for k, v in row.items():
									pt_csv.add(k, v)

								# Add the description to the pt_csv
								pt_csv.add('Source', source)
								pt_csv.add('Description', desc_str)

								pt_csv.write_dataset()
								
							print

					elif a_text == '1:20,000 Special':
						# Get the table with a border
						sub_table = sub_soup.find('table', attrs={'border': '2'})
						if sub_table is None:
							sub_table = sub_soup.find('table', attrs={'border': '1'})

						# Process the table
						unique_cols = collections.OrderedDict()
						unique_cols['mdata_col'] = '.doc metadata'
						unique_cols['ignore_cols'] = ['.gif overview']
						table_rows = self.process_table(parent_title, sub_table, sub_url, unique_cols, title_prefix='Topo Map')

						# Add the table on the page to the CSV
						for idx, row in enumerate(table_rows):
							msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
							shared.print_oneliner(msg)
								
							# Add the description to the pt_csv
							pt_csv.add('Description', desc_str)

							for k, v in row.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.write_dataset()
							
						print

					elif a_text == '1:20,000 FMU':
						# Get the table with different formats
						formats_table = sub_soup.find('table', attrs={'border': '2'})
						cols = formats_table.find_all('td')

						# Get the formats from the columns in the table
						formats = []
						for col in cols[2:3]:
							col_text = bsoup.get_text(col)
							formats.append(col_text.upper())

						# Now get the areas in the map
						sub_map = sub_soup.find('map')
						areas = sub_map.find_all('area')
						for idx, area in enumerate(areas):
							msg = "Extracting %s of %s areas" % (idx + 1, len(areas))
							shared.print_oneliner(msg)
						
							if area.has_attr('href'):
								area_link = area['href']
								area_url = urlparse.urljoin(sub_url, area_link)

								if area_url.find('.html') == -1:
									bsname = os.path.basename(area_url)
									title = bsname.split('_')[0]
									title_str = '%s - Topo Map FMU: %s' % (parent_title, title)

									# Add all geospatial data to the pt_csv
									pt_csv.add('Source', source)
									pt_csv.add('Title', title_str)
									pt_csv.add('Access', 'Download/Web Accessible')
									pt_csv.add('Type', 'Vector Data')
									pt_csv.add('Download', 'Multiple Downloads')
									pt_csv.add('Web Page URL', sub_url)
									pt_csv.add('Available Formats', '|'.join(formats))

									pt_csv.write_dataset()
									
						print

					elif a_text == '1:20,000 Seamless':
						# Get the table on the page
						table = sub_soup.find('table', attrs={'border': '2'})

						# Process the table
						unique_cols = collections.OrderedDict()
						unique_cols['mdata_col'] = '.doc'
						unique_cols['ignore_cols'] = ['type', '.gif']
						table_rows = self.process_table(parent_title, table, sub_url, unique_cols)

						# Add the table on the page to the CSV
						for idx, row in enumerate(table_rows):
							msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
							shared.print_oneliner(msg)
						
							# Add the description to the pt_csv
							pt_csv.add('Description', desc_str)

							for k, v in row.items():
								pt_csv.add(k, v)

							pt_csv.add('Source', source)
							pt_csv.write_dataset()
							
						print

					if a['href'].find('t50k/index.html') > -1:
						# This page contains a map with links to more subpages
						#   with tables with datasets
						sub_map = sub_soup.find('map')
						map_info = self.process_map(sub_map, sub_url)

						for area in map_info:
							area_url = area['Download']
							area_soup = bsoup.get_soup(area_url)
							if isinstance(area_soup, int):
								print "Error Code: %s" % area_soup
								if area_soup == 404:
									print "The webpage '%s' cannot be found." % area_url
									#answer = raw_input("Press enter...")
									continue
									
							# if area_soup is None:
								# print "The webpage '%s' cannot be found." % area_url
								# continue
								
							if not self.check_result(area_soup, area_url): continue
							
							area_table = area_soup.find('table', attrs={'border': '2'})
							if area_table is None:
								area_table = area_soup.find('table', attrs={'border': '1'})

							# Process the table
							unique_cols = collections.OrderedDict()
							unique_cols['mdata_col'] = '.doc metadata'
							unique_cols['ignore_cols'] = ['.gif overview']
							table_rows = self.process_table(parent_title, area_table, area_url, unique_cols, title_prefix='Topo Map')

							# Add the table on the page to the CSV
							for idx, row in enumerate(table_rows):
								msg = "Extracting %s of %s records" % (idx + 1, len(table_rows))
								shared.print_oneliner(msg)
								
								# Add the description to the pt_csv
								pt_csv.add('Description', desc_str)

								for k, v in row.items():
									pt_csv.add(k, v)

								# Add the description to the pt_csv
								pt_csv.add('Source', source)
								pt_csv.add('Description', desc_str)

								pt_csv.write_dataset()
								
							print

			elif parent_title == 'Town & Village Plans':
				#print 'Town & Village Plans'

				print 'No geospatial data, all PDFs or GIFs'
				
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time
				
	def extract_municipal(self): #, word=None, category=None, subpage='all'):
		''' Extracts all municipal pages for Manitoba (specifically Brandon and Winnipeg)
		:param word: The word used to filter the results.
		:param category: The category to filter the results.
		:param subpage: The subpage to run (only for debugging).
		:return: None
		'''
		
		# Get the parameters
		word = self.get_arg_val('word')
		category = self.get_arg('category')
		subpage = self.get_arg('subpage').get_urltags()[0]
		
		#print "subpage: %s" % subpage
		
		self.print_title("Extracting Manitoba's municipal pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# NOTE: subpage is for debugging only.
		if subpage is None: subpage = 'all'
		
		# Create CSV file
		csv_fn = "Municipal_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		#############################################################################
		# Extract from Brandon OpenData
		
		if subpage == 'bdn_opendata' or subpage == 'all':

			opendata_url = self.pg_grp.get_url('brandon_opendata_url')

			# Get soup
			opendata_soup = bsoup.get_soup(opendata_url)
			
			if self.check_result(opendata_soup, opendata_url, 'Brandon Open Data'):

				table = opendata_soup.find('table', attrs={'id': 'datasetTable'})
				rows = table.find_all('tr')

				for idx, row in enumerate(rows):
					anchor = row.find('a')
					
					msg = "Extracting %s of %s datasets from Brandon's Open Data page" % (idx + 1, len(rows))
					shared.print_oneliner(msg)

					if anchor is not None:
						# Get the parent row
						tr = anchor.parent.parent
						tds = tr.find_all('td')

						# Get the title from the first column and the format from the second column
						title_str = bsoup.get_text(tds[0])
						ds_type = bsoup.get_text(tds[1])

						# Determine if the dataset is a shapefile
						if ds_type == 'Shapefile':
							# Get the download URL and format
							download_url = shared.get_anchor_url(anchor, opendata_url)
							formats = ['SHP']

							# Get the access and download text
							download_info = shared.get_download_text(formats, download_url)
							download_str, access_str = download_info.split('|')

							pt_csv.add('Source', 'Manitoba Municipal - Brandon Open Data')
							pt_csv.add('Title', title_str)
							pt_csv.add('Type', ds_type)
							pt_csv.add('Web Page URL', opendata_url)
							pt_csv.add('Download', download_str)
							pt_csv.add('Access', access_str)
							pt_csv.add('Available Formats', formats[0])

							pt_csv.write_dataset()

				print
		##############################################################################
		# Extract from Brandon ESRI REST Service
		
		if subpage == 'bdn_rest' or subpage == 'all':

			rest_url = self.pg_grp.get_url('brandon_rest_url')
			my_rest = services.PT_REST(rest_url)

			# Get the service data and add it to the CSV file
			serv_data = my_rest.get_layers()
			for rec in serv_data:
				for k, v in rec.items():
					pt_csv.add(k, v)

				pt_csv.add('Source', 'Manitoba Municipal - Brandon Map Services')
					
				pt_csv.write_dataset()

		##############################################################################
		# Extract from what's left of Brandon GIS
		
		if subpage == 'bdn_gis' or subpage == 'all':
		
			bgis_url = self.pg_grp.get_url('brandon_gis_url')

			# Get the soup
			bgis_soup = bsoup.get_soup(bgis_url)

			# Locate the <section> tag with class 'mainContent'
			section = bgis_soup.find('section', attrs={'class': 'mainContent'})

			# Collect all the <li> tags in the section
			li_list = section.find_all('li')

			for idx, li in enumerate(li_list):
				msg = "Extracting %s of %s datasets from Brandon's GIS page" % (idx + 1, len(li_list))
				shared.print_oneliner(msg)
			
				# Get the map page URL
				map_a = li.find('a')
				map_url = shared.get_anchor_url(map_a, bgis_url)

				# Ignore the Google Maps since it's only a link to Google's Transit Map and
				#   not to a City of Brandon dataset
				if map_url.find('google.ca') > -1: continue
				elif map_url.find('snowmap') > -1:
					map_url = 'https://gisapp.brandon.ca/webmaps/snowclearing/index.html'

				# Get the map soup
				map_soup = bsoup.get_soup(map_url)

				if map_url.find('arcgis') > -1:
					# If the map is an ArcGIS Online Map
					data_url = shared.get_arcgis_url(map_url)

					map_json = shared.get_json(data_url)

					title_str = map_json['title']
					date_str = shared.translate_date(map_json['modified'])
					desc_str = map_json['description']
					lic_str = map_json['licenseInfo']
					sp_str = shared.get_spatialref(map_json)
					map_type = 'ArcGIS Online Web Map'

				else:
					# Look for text in the soup to determine the type of map
					map_type = 'Web Map Application'
					if str(map_soup).find('x-shockwave-flash') > -1:
						# The map is a Adobe Flash Web Map
						map_type = 'Adobe Flash Web Map Application'


					# Get the title
					title = map_soup.find('title')
					title_str = bsoup.get_text(title)

					# Get the description
					desc_str = ''
					desc_tag = map_soup.find('meta', attrs={'name': 'description'})
					if desc_tag is not None:
						desc_str = desc_tag['content']

					# Get the date
					date_str = ''
					date_div = map_soup.find('div', attrs={'id': 'updateDiv'})
					if date_div is not None:
						date_str = bsoup.get_text(date_div).replace('Last Updated: ', '')

					lic_str = ''
					sp_str = ''
					data_url = ''

				pt_csv.add('Source', 'Manitoba Municipal - Brandon GIS')
				pt_csv.add('Title', title_str)
				pt_csv.add('Type', map_type)
				pt_csv.add('Description', desc_str)
				pt_csv.add('Date', date_str)
				pt_csv.add('Data URL', data_url)
				pt_csv.add('Web Page URL', bgis_url)
				pt_csv.add('Licensing', lic_str)
				pt_csv.add('Spatial Reference', sp_str)
				pt_csv.add('Web Map URL', map_url)
				pt_csv.add('Download', 'No')
				pt_csv.add('Access', 'Viewable/Contact the Province')

				pt_csv.write_dataset()
				
			print
			
		##############################################################################
		# Extract from Winnipeg's Catalogue
		
		if subpage == 'wpg_catalogue' or subpage == 'all':

			# Get the Winnipeg Catalogue URL
			search_url = self.pg_grp.get_url('winnipeg_opendata_url')
			
			ds_type = 'maps'

			# Set the parameters for the query URL
			params = collections.OrderedDict()
			if word is not None and not word == '':
				params['q'] = word
			if category is not None and not category == '':
				cat_urltag = category.get_urltags()[0]
				if not cat_urltag == 'all':
					params['category'] = cat_urltag
			if ds_type is not None and not ds_type == '':
				params['limitTo'] = ds_type
			params['sortBy'] = "alpha"

			# Build the query URL
			query_url = shared.get_post_query(search_url, params)

			# Get the soup
			soup = bsoup.get_soup(query_url)

			# Get the number of pages from page buttons at bottom of site
			res_count_div = soup.find('div', attrs={'class': 'browse2-results-title'})
			results_text = bsoup.get_text(res_count_div)
			res_lst = results_text.split(" ")

			num_results = res_lst[0]

			page_count = math.ceil(int(num_results) / 10.0)
			prev_perc = -1
			record_count = 0
			record_total = int(num_results)

			print "Number of pages: " + str(page_count)

			for page in range(0, int(page_count)):
				# Open each iteration of pages:
				params['page'] = page + 1
				page_url = shared.get_post_query(search_url, params)
				page_soup = bsoup.get_soup(page_url)

				# Get all the datasets on the current page (all datasets are in a 'div' with class 'dataset-item')
				results = page_soup.find_all('div', attrs={'class': 'browse2-result-content'})

				#print "\nPage URL: %s" % page_url
				#print "Number of results on page: " + str(len(results))

				if len(results) == 0 and record_count == 0:
					print "No records exist with the given search parameters."
					print "URL query sample: %s" % query_url
					return None

				for dataset in results:
				
					record_count += 1
					msg = "Extracting %s of approximately %s results from '%s'" % (record_count, record_total, query_url)
					shared.print_oneliner(msg)

					# Get the header of the dataset
					h2 = dataset.find('h2', attrs={'class': 'browse2-result-name'})

					# Get the link to the page
					webpage_url = shared.get_link(h2)

					# Get the soup of the dataset
					attrb = ('class', 'downloadsList')
					ds_soup = bsoup.get_soup(webpage_url)
					
					# Get the metadata from the page
					mdata_info = bsoup.get_page_metadata(ds_soup)
					
					#print "\n"
					#print webpage_url
					#for k, v in mdata_info.items():
					#	print "%s: %s" % (k, v)
					
					#if mdata_info['page_name'] == 'Map':
					
					# Get the title
					title_str = mdata_info['page_title']
					title_str = title_str.replace(' | Open Data | City of Winnipeg', '')

					# Get the description
					desc_str = mdata_info['description']

					# Get the publisher
					pub_str = bsoup.get_dl_text(ds_soup, 'Department')

					# Get the date
					date_str = ''
					date_span = ds_soup.find('span', attrs={'class': 'aboutUpdateDate'})
					if date_span is not None: date_str = bsoup.get_text(date_span)

					# Get the licence
					lic_str = bsoup.get_dl_text(ds_soup, 'Licence')

					# Set the available formats as KML, KMZ, SHP and GeoJSON
					formats = ['KML', 'KMZ', 'SHP', 'GeoJSON']
					access_str = 'Download/Web Accessible'
					download_str = 'Multiple Downloads'

					pt_csv.add('Source', 'Manitoba Municipal - Winnipeg Catalogue')
					pt_csv.add('Title', title_str)
					pt_csv.add('Type', "Vector File")
					pt_csv.add('Description', desc_str)
					pt_csv.add('Date', date_str)
					pt_csv.add('Publisher', pub_str)
					pt_csv.add('Licensing', lic_str)
					pt_csv.add('Web Page URL', webpage_url)
					pt_csv.add('Download', download_str)
					pt_csv.add('Available Formats', '|'.join(formats))
					pt_csv.add('Access', access_str)

					pt_csv.write_dataset()

				print
		##############################################################################
		# Extract from Winnipeg's Property Map/Aerial Photography & ServiceStat
		
		if subpage == 'wpg_property' or subpage == 'all':

			# Extract Property Map webpage
			propertymap_url = self.pg_grp.get_url('winnipeg_property_url')

			# Get the soup
			property_soup = bsoup.get_soup(propertymap_url, True, "legenditem")

			# Get the layers
			property_layers = property_soup.find_all('table', attrs={'class': 'legenditem'})

			prop_recs = self.process_googleapi(property_layers, "property")

			for r in prop_recs:
			
				for k, v in r.items():
					pt_csv.add(k, v)

				pt_csv.add('Source', 'Manitoba Municipal - Winnipeg Interactive Maps')
				pt_csv.add('Web Map URL', propertymap_url)
				pt_csv.add('Web Page URL', 'http://winnipeg.ca/ppd/maps.stm')
				pt_csv.add('Download', 'No')
				pt_csv.add('Access', 'Viewable/Contact the Province')

				pt_csv.write_dataset()

			# Extract the ServiceStat page
			servstat_url = self.pg_grp.get_url('servstat_url')

			# Get the soup
			attrb = ('id', 'wpgmap_legend')
			servstat_soup = bsoup.get_soup(servstat_url, True, attrb)
			
			if self.check_result(servstat_soup, servstat_url, 'ServiceStat Page'):

				# Get the legend and layers
				legend_div = servstat_soup.find('div', attrs={'id': 'wpgmap_legend'})
				servstat_layers = legend_div.find_all('a')

				stats_recs = self.process_googleapi(servstat_layers, "servstat")

				for r in stats_recs:
					for k, v in r.items():
						pt_csv.add(k, v)

					pt_csv.add('Source', 'Manitoba Municipal - Winnipeg Interactive Maps')
					pt_csv.add('Web Map URL', servstat_url)
					pt_csv.add('Download', 'No')
					pt_csv.add('Access', 'Viewable/Contact the Province')

					pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time
	
	def extract_services(self):
		''' Method to extract all Manitoba provincial map services.
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting Manitoba's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the CSV file
		csv_fn = "MapServices_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		##################################################################
		# Extract the Manitoba's ESRI REST Services

		# Get the petroleum service url
		petrol_url = self.pg_grp.get_url('petrol_url')

		self.print_log("URL: %s" % petrol_url)

		# Get a list of REST services
		petrol_rest = services.PT_REST(petrol_url)

		# Get the Petroleum service and add it to the CSV file
		petrol_data = petrol_rest.get_layers()
		for rec in petrol_data:
			for k, v in rec.items():
				pt_csv.add(k, v)

			pt_csv.add('Source', 'Manitoba Map Services')
			pt_csv.write_dataset()

		# Get a list of the services2 services
		rest_url = self.pg_grp.get_url('rest_url')
		serv_rest = services.PT_REST(rest_url)

		# Get the other service and add it to the CSV file
		serv_data = serv_rest.get_layers()
		for rec in serv_data:
			for k, v in rec.items():
				pt_csv.add(k, v)

			pt_csv.add('Source', 'Manitoba Map Services')
			pt_csv.write_dataset()

		pt_csv.close_csv()
		
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

		#print page

		ext.set_page(page)
		ext.set_params(params)
		ext.run()

	except Exception, err:
		ext.print_log('ERROR: %s\n' % str(err))
		ext.print_log(traceback.format_exc())
		ext.close_log()

if __name__ == '__main__':
	sys.exit(main())
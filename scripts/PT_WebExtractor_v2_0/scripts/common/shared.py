import os
import sys
import glob
import urllib2
import bs4
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import collections
import math
import datetime
import dateutil.parser as parser
import json
import csv
from csv import reader
import requests
import urlparse
import shutil
import ssl
import argparse
import codecs
import string
import cStringIO
import re
import xmltodict
import pprint
import traceback
import ogr
import osr
from ftplib import FTP
from BaseHTTPServer import BaseHTTPRequestHandler

from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from browsermobproxy import Server

import bsoup

class data_keys(str):
	unique = 0

	def __init__(self, val):
		super(data_keys, self).__init__(val)
		self.unique += 1
		self.my_hash = self.unique

	def __eq__(self, other):
		return False

	def __hash__(self):
		return self.my_hash

def check_page(url):
	''' Checks to see if a page can open with no errors.
	:param url: The URL of the page to load.
	:return: True if the page loads with no errors.
	'''
	
	# Open the page
	try:
		page = open_webpage(url)
	except:
		return False
	
	if page is None:
		return False
	else:
		return True
		
def clean_table(table):
	''' Fixes any issues in a table such as completing at <tr> tag with </tr>
	:param table: The input table element.
	:return: A fixed table element.
	'''

	# Clean the table first
	tr_pos = [m.start() for m in re.finditer('<tr>', str(table))]

	## print tr_pos

	table_str = str(table)

	for pos in tr_pos:
		# Get the previous tag
		end_pos = str(table)[:pos].rfind('>') + 1
		start_pos = str(table)[:pos].rfind('<')
		prev_tag = str(table)[start_pos:end_pos]

		# print prev_tag

		if not prev_tag == '<tbody>' and not prev_tag == '</tr>':
			table_str = str(table)[:end_pos] + '</tr>' + str(table)[pos:]

	return table_str

def clean_text(txt):
	''' Removes all whitespaces from txt.
	:param txt: The string in which to remove all whitespaces.
	:return: The string with no whitespaces.
	'''
	if txt is None: return ''
	# Remove next-line characters
	text_str = txt.replace("\n", " ")
	# Remove return characters
	text_str = text_str.replace("\r", " ")
	# Remove whitespace
	text_str = text_str.strip()
	# Remove extra spacing
	text_str = re.sub('[ \t]+', ' ', text_str)
	# Replace unicode with ASCII equivalent
	text_str = filter_unicode(text_str)
	#text_str = text_str.replace(u'\xa0', u' ')

	return text_str
	
def create_wkt_extents(ext, in_epsg=None, in_wkt=None):
	''' Creates the WKT extents from two points
		:param ext: A tuple or list with (north, south, east, west)
	'''
	
	#print ext
	
	if len(ext) == 4:
	
		north, south, east, west = ext
		
		if not is_float(north): return ''
		if not is_float(south): return ''
		if not is_float(east): return ''
		if not is_float(west): return ''
		
		# in_exts: [ul, ur, lr, ll]
		in_exts = [(float(west), float(north)), (float(east), float(north)), \
					(float(east), float(south)), (float(west), float(south))]
		
		#print "\nOriginal projection:"
		#print in_exts
		
		if in_epsg is not None:
			# Reproject coordinates
			srs = osr.SpatialReference()
			srs.ImportFromEPSG(in_epsg)
			
			out_exts = reproject_coords(in_exts, srs)
		else:
			if in_wkt is None:
				out_exts = in_exts
			else:
				# Reproject coordinates
				srs = osr.SpatialReference()
				srs.ImportFromWkt(in_wkt)
				
				out_exts = reproject_coords(in_exts, srs)
			
		if len(out_exts) == 0: return ''
		
		out_exts_str = [(str(pt[0]), str(pt[1])) for pt in out_exts]
	
		# Create tuples of coordinates
		ul = '(%s)' % ' '.join(out_exts_str[0])
		ur = '(%s)' % ' '.join(out_exts_str[1])
		lr = '(%s)' % ' '.join(out_exts_str[2])
		ll = '(%s)' % ' '.join(out_exts_str[3])
	else:
		print "\nWARNING: Extents not valid."
		return ''
		
	# Convert the coordinates to WKT format, 
	#	starting with upper-left and going clock-wise
	wkt_text = 'POLYGON (%s, %s, %s, %s)' % (ul, ur, lr, ll)
	
	#print wkt_text
	
	#answer = raw_input("Press enter...")
	
	return wkt_text

def epsg_to_spatref(epsg_code):
	''' Converts a EPSG code to its coordinate system name
	:param epsg_code: The EPSG code
	:return: The name of the coordinate system
	'''

	# Open the CSV of EPSG codes
	home_folder = get_home_folder()
	epsg_csv_path = os.path.join(os.sep, home_folder, 'files', 'epsg', 'coordinate_reference_system.csv')
	epsg_file = open(epsg_csv_path, 'r')
	epsg_csv = csv.reader(epsg_file)

	# Locate the EPSG in the file and return its coord_ref_sys_name if found
	for row in epsg_csv:
		if row[0] == epsg_code:
			return row[1]
			
def estimate_time(start_time, rec_count, rec_idx=10):
	''' Estimates the amount of time for an extraction process.
		:param start_time: The start time of the process.
		:param rec_count: The total number of records.
		:param rec_idx: The number of records up to the call of this method.
		:return: The estimated time as a datetime object.
	'''
	
	end_time = datetime.datetime.now()
	total_time = end_time - start_time
	total_secs = total_time.total_seconds()

	time_count = (total_secs / rec_idx) * rec_count

	mins = time_count / 60
	mins_int = int(mins)

	secs = (mins - mins_int) * 60

	print "\nTotal estimated time: %s minutes & %s seconds" % (mins_int, secs)
			
def filter_unicode(in_str, out_type=None, french=False, all=False):
	''' Replaces unicode characters with corresponding ascii characters 
	:param in_str: The input unicode string.
	'''
	
	if in_str is None: return None
	
	replace_dict = collections.OrderedDict()
	if french:
		french_dict = {u'à': 'a', u'á': 'a', u'â': 'a', u'ä': 'a',
				 u'ç': 'c', u'è': 'e', u'é': 'e', u'ê': 'e', u'ë': 'e', 
				 u'ì': 'i', u'í': 'i', u'î': 'i', u'ï': 'i', 
				 u'ò': 'o', u'ó': 'o', u'ô': 'o', u'ö': 'o',
				 u'ù': 'u', u'ú': 'u', u'û': 'u', u'ü': 'u',
				 u'À': 'A', u'Á': 'A', u'Â': 'A', u'Ä': 'A',
				 u'Ç': 'C', u'È': 'E', u'É': 'E', u'Ê': 'E', u'Ë': 'E',
				 u'Ì': 'I', u'Í': 'I', u'Î': 'I', u'Ï': 'I',
				 u'Ò': 'O', u'Ó': 'O', u'Ô': 'O', u'Ö': 'O',
				 u'Ù': 'U', u'Ú': 'U', u'Û': 'U', u'Ü': 'U'}
		replace_dict.update(french_dict)
	
	other_dict = {u'‘': "'", u'’': "'", u'“': '"', u'”': '"', u'–': '-', u'—': '-', 
				u'•': '-', u'\xa0': ' ', u'\u2011': '-', u'\u2026': '...', 
				u'\x92': "'", u'\u2122': '(TM)', u'\ufeff': '', u'\xa8': ',', 
				u'\xab': '<<', u'\xbb': '>>', u'\u0153': 'oe', 
				u'\u00B9': '(1)', u'\u00B2': '(2)', u'\u2013': '-'}
				
	replace_dict.update(other_dict)
	
	if all:
		all_dict = {u'°': '', u'©': ' copyright ', u'®': '', u'\u20ac': 'Euro'}
	
		replace_dict.update(all_dict)
	
	#print in_str in replace_dict.keys()

	out_list = []
	for l in in_str:
		if l in replace_dict.keys():
			out_l = replace_dict[l]
		else:
			out_l = l
		out_list.append(out_l)
		
	out_str = ''.join(out_list)
	
	if out_type is not None:
		out_str = type(out_type)(out_str)
	
	return out_str
	
def find_duplicates(in_rows):
	''' Finds the indices of all the duplicate entries
	'''

	dup_indices = []
	
	for idx, row in enumerate(in_rows):
	
		msg = "Finding duplicates: %s of %s lines" % (idx + 1, len(in_rows))
		print_oneliner(msg)
	
		title = row['Title']
		desc = row['Description']
		serv_url = row['Service URL']
		#print row
		downloads = row['Download']
		
		idx_lst = [idx]
		
		indices = []
		for i, x in enumerate(in_rows):
			rec_title = x['Title']
			rec_desc = x['Description']
			if rec_title == title:
				if rec_desc[:100] == desc[:100]:
					# If titles are equal and descriptions are equal
					indices.append(i)
					continue
				if rec_desc == '' or desc == '':
					# If titles are equal but one of the descriptions
					#	is blank
					recserv_url = x['Service URL']
					if recserv_url == '' or serv_url == '':
						# If one of them is not a map services, compare
						#	downloads
						rec_downloads = x['Download']
						if rec_downloads == 'Multiple Downloads' or \
							downloads == 'Multiple Downloads' or \
							rec_downloads == '' or downloads == '' or \
							rec_downloads == 'No' or downloads == 'No':
							continue
						if rec_downloads == download:
							indices.append(i)
							continue
					serv_url = get_service_url(serv_url)
					recserv_url = get_service_url(recserv_url)
					if serv_url == recserv_url:
						indices.append(i)
						continue
		
		if len(indices) > 1:
			dup_indices.append(indices)
		
	#print dup_indices
	
	print
		
	out_indices = list(set(tuple(i) for i in dup_indices))
	
	return out_indices
	
def format_date(in_date, out_format='%Y-%m-%d'):
	''' Formats a date string to a specified format or
		yyyy-mm-dd.
	'''
	
	if in_date == '': return ''
	
	try:
		dt_date = parser.parse(in_date)
	except:
		dt_date = datetime.datetime(1900, 1, 1, 0, 0)
		
	latest_date = dt_date.strftime(out_format)
	
	print latest_date
	
	return latest_date

def ftp_files(ftp, url):
	''' Gets a list of files from an FTP URL.
	:param ftp: An FTP object.
	:param url: The FTP URL which contains the files.
	:return: A list of files.
	'''

	# Using the FTP link, determine the available formats
	domain = urlparse.urljoin(url, '/')
	path = url.replace(domain, '')
	try:
		ftp.cwd('/')
		ftp.cwd(path)
		ftp_files = ftp.nlst()
		return ftp_files
	except Exception as e:
		#print traceback.format_exc()
		#print "URL: %s" % url
		print "\nError in ftp_files: %s" % str(e)
		print "%s\n" % url
		err_dict = collections.OrderedDict()
		err_dict['err'] = str(e)
		return err_dict

def get_anchor_url(anchor, root_url):
	''' Joins the link text from an anchor with its page's root URL.
	:param anchor: The anchor tag.
	:param root_url: The root URL of the page.
	:return: The full URL link.
	'''
	if anchor is None: return ''
	#print "anchor: %s" % anchor
	link = anchor['href']
	if link.find('http:') == -1 and link.find('https:') == -1:
		out_url = urlparse.urljoin(root_url, link)
	else:
		out_url = link

	return out_url

def get_arcgis_data(map_url, title_prefix=None, pre_info=None):
	''' Extracts the information from ArcGIS Online data.
	:param map_url: The ArcGIS Map URL
	:return: A dictionary containing the ArcGIS data.
	'''

	# Get the JSON format of the ArcGIS URL
	data_url = get_arcgis_url(map_url)
	
	#print data_url
	
	if isinstance(data_url, dict):
		return data_url
	
	if data_url is None: return None
	map_json = get_json(data_url)
	
	if 'err' in map_json.keys():
		map_data = collections.OrderedDict()
		if pre_info is not None: map_data.update(pre_info)
		# print "map_data: %s" % map_data
		map_data['Title'] = '(ERROR: see notes)'
		map_data['Type'] = "ArcGIS Map"
		map_data['Web Map URL'] = map_url
		map_data['Notes'] = map_json['err']

		return map_data

	if 'error' in map_json.keys():

		err_code = map_json['error']['code']
		message = map_json['error']['message']

		# Set the map_data dictionary
		map_data = collections.OrderedDict()
		if pre_info is not None: map_data.update(pre_info)
		# print "map_data: %s" % map_data
		map_data['Title'] = '(ERROR: see notes)'
		map_data['Type'] = "ArcGIS Map"
		map_data['Web Map URL'] = map_url
		map_data['Notes'] = "Error %s: %s" % (err_code, message)

		return map_data

	if 'items' in map_json.keys():
		items = map_json['items']
	else:
		items = [map_json]

	map_items = []
	for item in items:
		# Get the title
		if 'title' in item:
			title = item['title']
		else:
			title = item['name']
		if title_prefix is not None:
			title_str = '%s - %s' % (title_prefix, title)
		else:
			title_str = title

		# Get the licensing
		lic_str = ''
		if 'licenseinfo' in item: lic_str = bsoup.get_text(item['licenseInfo'])

		# Get the description
		desc_str = ''
		if 'description' in item: desc_str = bsoup.get_text(item['description'])

		# Get the map URL if applicable
		map_url = ''
		if 'url' in item: map_url = bsoup.get_text(item['url'])

		# Get the data URL
		if map_url is None or map_url == '':
			if 'viewer' in item: map_url = get_arcgis_url(data_url, 'viewer')

		# Get the overview URL
		overview_url = ''
		if 'overview' in item: overview_url = get_arcgis_url(data_url, 'overview')

		notes_str = ''
		if 'notes' in item: notes_str = item['notes']
		
		# Get keywords
		keywords = []
		if 'tags' in item: keywords += item['tags']
		if 'typeKeywords' in item: keywords += item['typeKeywords']
		keywords_str = ', '.join(keywords)
		
		ext_str = ''
		extents = item['extent']
		if len(extents) > 0:
			north = extents[1][1]
			south = extents[0][1]
			east = extents[1][0]
			west = extents[0][0]
			
			ext = (north, south, east, west)
			ext_str = create_wkt_extents(ext)

		# Set the map_data dictionary
		map_data = collections.OrderedDict()
		if pre_info is not None: map_data.update(pre_info)
		#print "map_data: %s" % map_data
		map_data['Title'] = title_str
		map_data['Description'] = desc_str
		map_data['Type'] = "ArcGIS " + str(item['type'])
		map_data['Start Date'] = translate_date(item['created'])
		map_data['Recent Date'] = translate_date(item['modified'])
		map_data['Keywords'] = keywords_str
		map_data['Extents'] = ext_str
		map_data['Licensing'] = lic_str
		#map_data['Access'] = 'Download using ESRI REST Service'
		map_data['Web Map URL'] = map_url
		map_data['Web Page URL'] = overview_url
		map_data['Data URL'] = data_url
		map_data['Notes'] = notes_str

		map_items.append(map_data)

	if len(map_items) == 1:
		return map_items[0]
	else:
		return map_items

def get_arcgis_gallery(gallery_url):
	''' Gets all the maps on a ArcGIS Gallery page.
	:param gallery_url: The ArcGIS Gallery URL.
	:return: A list of dictionaries of ArcGIS map data.
	'''

	gallery_soup = bsoup.get_soup(gallery_url, True)

	gallery_div = gallery_soup.find('div', attrs={'class': 'gallery-card-wrap'})

	# Get the <div> with class "card" to get each interactive map
	map_anchors = gallery_div.find_all('a', attrs={'class': 'card-image-wrap'})

	map_list = []

	for idx, card in enumerate(map_anchors):
		msg = "Extracting %s of %s gallery maps" % (idx, len(map_anchors))
		print_oneliner(msg)
	
		# Get the anchor link
		map_url = get_anchor_url(card, gallery_url)

		#print "Map URL: %s" % map_url
		
		#answer = raw_input("Press enter...")

		# Get the ArcGIS data
		arcgis_info = get_arcgis_data(map_url)

		if arcgis_info is None: continue

		# Add the ArcGIS data to the map list
		map_list.append(arcgis_info)

	return map_list

def get_arcgis_url(url, link_type='data'):
	''' Gets the specified ArcGIS URL from the given ArcGIS URL
	:param url: The initial ArcGIS URL.
	:param link_type: Determines the type of ArcGIS to return.
					(values: 'data', 'overview', 'webmap', 'viewer')
	:return: The specified ArcGIS URL.
	'''

	try:
		# Get the domain of the URL
		domain = urlparse.urljoin(url, '/')
		#print domain

		# if url.find('item') > -1:
			# # If the URL is already a data URL, get the ID from the basename of the URL
			# id_bname = os.path.basename(url)
			# id = id_bname.split('?')[0]
		# else:
		
		# Get the ID of the ArcGIS map from the URL
		print url
		url_split = url.split('?')
		query = url_split[1]
		params = query.split('&')

		id = ''
		for param in params:
			key = param.split('=')[0]
			value = param.split('=')[1]

			if key == 'id' or key == 'appid' or key == 'webmap' or key == 'layers':
				id = value

		if link_type == 'overview':
			out_url = "%shome/item.html?id=%s" % (domain, id)
		elif link_type == 'webmap':
			out_url = "%sapps/webappviewer/index.html?webmap=%s" % (domain, id)
		elif link_type == 'viewer':
			out_url = "%sapps/webappviewer/index.html?id=%s" % (domain, id)
		else:
			out_url = "%ssharing/rest/content/items/%s?f=pjson" % (domain, id)

		return out_url
	except:
		print "\nERROR: Not a valid ArcGIS Online URL."
		print "%s\n" % url
		print traceback.format_exc()
		err_dict = collections.OrderedDict()
		err_dict['err'] = "Not a valid ArcGIS Online URL."
		err_dict['code'] = "430"
		return err_dict

		# if url.find('rest') > -1:
		#     # Convert data URL to viewer URL
		#     # /apps/webappviewer/index.html?
		#
		#     # Get the ID from URL
		#     url_list = url.split("/")
		#     id_str = url_list[7]
		#
		#     # Remove any query parameters from the ID
		#     id_split = id_str.split('?')
		#     id = id_split[0]
		#
		#     print "ID: " + str(id)
		#
		#     webmap_url = "%sapps/webappviewer/index.html?webmap=%s" % (domain, id)
		#
		#     map_url = "%sapps/webappviewer/index.html?id=%s" % (domain, id)
		#
		#     print "\nThe ArcGIS Online webmap viewer URL: %s" % webmap_url
		#     print "\nThe ArcGIS Online viewer URL: %s" % map_url
		#
		#     return (webmap_url, map_url)
		# else:
		#     try:
		#         # Get the ID from URL
		#         url_split = url.split('?')
		#         query = url_split[1]
		#         params = query.split('&')
		#
		#         id = ''
		#         for param in params:
		#             key = param.split('=')[0]
		#             value = param.split('=')[1]
		#
		#             if key == 'id' or key == 'appid' or key == 'webmap':
		#                 id = value
		#
		#         # out_url = "%ssharing/rest/content/items/%s/data" % (domain, id)
		#         if url.find('group') > -1:
		#             out_url = "%ssharing/rest/content/groups/%s?f=pjson" % (domain, id)
		#         else:
		#             out_url = "%ssharing/rest/content/items/%s?f=pjson" % (domain, id)
		#
		#         print "\nThe ArcGIS Online data URL: %s" % out_url
		#
		#         return out_url
		#     except:
		#         print "ERROR: Not a valid ArcGIS Online URL."

def get_bracket_text(txt, bracket='(', beg=0):
	''' Gets the text between two round brackets.
	:param txt: The input text containing the brackets.
	:return: The text between the brackets.
	'''
	
	if bracket == '[':
		start_pos = txt.find('[', beg) + 1
		end_pos = txt.find(']', start_pos)
	elif bracket == '"':
		start_pos = txt.find('"', beg) + 1
		end_pos = txt.find('"', start_pos)
	else:
		start_pos = txt.find('(', beg) + 1
		end_pos = txt.find(')', start_pos)
	out_txt = txt[start_pos:end_pos]

	return out_txt

def get_data_type(url):
	''' Gets the data type based on the file extension of a URL.
	:param url: The data URL.
	:return: The data type of the URL.
	'''

	if url.find('shp') > -1 or url.find('dxf') > -1 or \
			url.find('csv') > -1 or url.find('kml') > -1 or \
			url.find('kmz') > -1 or url.find('json') > -1:
		return 'Vector Data File'
	else:
		return 'Raster Data File'

def get_download_text(formats=[], download_url='', date=''):
	''' Sets the download string and access string based on the formats.
		Ex: If no formats exist, then the download string is
			'No' and the access string is 'Contact the Province'.
			If only one format exists, then the download string is
			the download URL and access is 'Download/Web Accessible'.
			If more than one format exists, then the download string is
			'Multiple Downloads' and the access string is 'Download/Web
			Accessible'.
	:param formats: A list of the formats for the dataset.
	:param download_url: The download URL, if applicable. 
							It can either be a list or a string.
	:param date: The date, if applicable. It can either be a list or a string.
	:return: The download sting and access string (see above).
	'''
	
	if isinstance(date, list):
		# Make a list of datetime objects
		dates = [parser.parse(dt) for dt in date]
		max_date = max(dates)
		max_date = max_date.strftime('%Y-%m-%d')
		max_date = '|%s' % max_date
	else:
		if date == '':
			max_date = ''
		else:
			max_date = '|%s' % date
			
	if not isinstance(download_url, list):
		download_url = [download_url]
		
	if len(formats) == 0 and len(download_url) == 0:
		return 'No|Contact the Province%s' % max_date
	elif len(formats) == 1 or len(download_url) == 1:
		out_url = download_url[0]
		if out_url == 'http://apps.gov.bc.ca/notice/edc/faq/':
			# For BC Catalogue
			return 'No|Requires Access/Contact the Province'
		else:
			return '%s|Download/Web Accessible%s' % (out_url, max_date)
	else:
		return 'Multiple Downloads|Download/Web Accessible%s' % max_date
	
	if len(formats) == 0:
		return 'No|Contact the Province%s' % max_date
	elif len(formats) == 1:
		if isinstance(download_url, list):
			out_url = download_url[0]
		else:
			out_url = download_url
		if out_url == 'http://apps.gov.bc.ca/notice/edc/faq/':
			# For BC Catalogue
			return 'No|Requires Access/Contact the Province'
		else:
			return '%s|Download/Web Accessible%s' % (out_url, max_date)
	else:
		return 'Multiple Downloads|Download/Web Accessible%s' % max_date

def get_driver(browser='firefox', headless=True):
	''' Gets the Selenium driver based on the specified browser name.
	:param browser: The name of the browser (firefox, chrome, ie).
	:return: The Selenium driver.
	'''

	if browser.lower() == 'chrome':
		# Load the webdriver using Chrome
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--test-type")
		options.binary_location = get_home_folder() + "\\webdrivers\\chromedriver_win32"
		driver = webdriver.Chrome(chrome_options=options)
	elif browser.lower() == 'ie':
		# Load the webdriver using Internet Explorer
		ie_folder = get_home_folder() + "\\webdrivers\\IEDriverServer_x64_2.42.0\\IEDriverServer.exe"
		#print "IE Folder: %s" % ie_folder
		driver = webdriver.Ie(ie_folder)
	else:
		# Load the webdriver using headless Firefox
		firefox_folder = get_home_folder() + "\\webdrivers\\geckodriver-v0.23.0-win64\\geckodriver.exe"
		# binary = FirefoxBinary(get_home_folder() + "\\webdrivers\\geckodriver-v0.20.0-win64\\geckodriver.exe")

		options = Options()
		if headless:
			options.add_argument("--headless")
		driver = webdriver.Firefox(firefox_options=options, 
								   log_path='files\\geckodriver.log')  # , firefox_binary=binary)

	return driver

def get_ftp(url):
	''' Sets up an FTP object using URL.
	:param url: The FTP URL.
	:return: An FTP object.
	'''

	# Get the FTP domain
	if url.find("/") > -1:
		domain = urlparse.urljoin(url, '/')
		domain_base = domain.replace("ftp://", "").strip('/')
	else:
		domain_base = url
	#print domain_base

	try:
		ftp = FTP(domain_base)
		ftp.login()
		return ftp
	except Exception as e:
		print traceback.format_exc()
		print "\nError in get_ftp: %s" % str(e)
		print "%s\n" % url
		err_dict = collections.OrderedDict()
		err_dict['err'] = str(e)
		return err_dict
		
def get_header(csv_lines):
	''' Gets the header from a CSV file
	'''
	
	header = csv_lines[0].split(',')
	
	# Clean the header if from a file
	header = [h.replace(u'\ufeff', '').replace('\n', '') for h in header]
	
	return header

def get_home_folder():
	''' Gets the top folder location of the FGP_WebExtractor.
	:return: The folder location of the Web Extractor.
	'''

	top_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	return top_folder

def get_json(url, silent=True, timeout=10, attempts=1):
	''' Gets the JSON of a specified URL.
	:param url: The URL of the JSON data.
	:return: JSON formatted string.
	'''
	
	if not silent: print "\nJSON URL: %s" % url
	while attempts > 0:
		if not silent: print "\nGetting JSON, attempt #%s..." % attempts
		try:
			response = requests.get(url, timeout=timeout)
			#response = requests.request('GET', url)
			json_text = response.json()
			attempts = 0
		except requests.exceptions.Timeout:
			attempts -= 1
			if attempts == 0:
				print "\nJSON Error: Timeout occurred"
				print "%s\n" % url
				json_text = collections.OrderedDict()
				json_text['err'] = "Timeout occurred."
			else:
				if not silent: print "JSON Error: Timeout occurred."
		except:
			# html_text = open_webpage(url)
			# print html_text
			attempts = 0
			try:
				response = requests.get(url, timeout=timeout, verify=False)
				json_text = response.json()
			except Exception as e:
				print "\nError in get_json: %s" % str(e)
				print "%s\n" % url
				json_text = collections.OrderedDict()
				json_text['err'] = str(e)

	return json_text

def get_key(json_dict, key):
	''' A recursive algorithm that returns the item in a JSON text with a certain key.
	:param json_dict: A JSON dictionary.
	:param key: The key to search for.
	:return: Returns the item with the specified key
	'''

	for k, v in json_dict.iteritems():
		if k == key:
			# If the key is found, return the item
			return v
		if isinstance(v, list):
			# If v is a list, go through it
			for i in v:
				if isinstance(i, dict):
					# If the item in v list is a dictionary, send it through the get_key method
					res = get_key(i, key)
					if res is not None:
						return res
		elif isinstance(v, dict):
			# If the v is a dictionary, send it through the get_key method
			res = get_key(v, key)
			if res is not None:
				return res
				
def get_minmax_date(dates, format='%Y-%m-%d'):

	#print dates
	
	# Remove the 'T' from any date
	#split_dates = [d.split('T')[0] if 'T' in d else d for d in dates]
	split_dates = []
	for d in dates:
		if d is not None:
			if 'T' in d:
				d_val = d.split('T')[0]
			else:
				d_val = d
			split_dates.append(d_val)
		
	# Convert the dates to datetime objects
	dt_dates = []
	for date in split_dates:
		try:
			dt_date = parser.parse(date)
		except:
			dt_date = datetime.datetime(1900, 1, 1, 0, 0)
		dt_dates.append(dt_date)
		
	#if len(dt_dates) > 2:
	#	answer = raw_input("Press enter...")
		
	# Get the maximum date in the list
	latest_date = max(dt_dates)
	start_date = min(dt_dates)
	
	if latest_date.year >= 1900:
		latest_date = latest_date.strftime(format)
	else:
		latest_date = ''
		
	if start_date.year >= 1900:
		start_date = start_date.strftime(format)
	else:
		start_date = ''
	
	return start_date, latest_date

def get_link(html, url=None):
	''' Gets the link from the anchor in the HTML code
	:param html: The HTML code containing the link.
	:return: The full URL of the link
	'''

	anchors = html.find_all('a')
	if len(anchors) > 0:
		if url is None:
			link = anchors[0]['href']
		else:
			link = shared.get_anchor_url(anchors[0])
		return link
	else:
		return None

def get_network_traffic(url, attrb, delay=2, silent=True):  # attr_name, el_type='class'):
	''' Gets a list of the files loaded for a web page.
	:param url: The web page URL to load.
	:param attrb: A tuple containing (<element attribute name>, <element attribute value>)
						ex: ('class', 'esriAttribution')
	:param delay: The delay, in seconds, to wait until scraping the page.
	:return: A list of files loaded by the web page.
			JSON Ex:
			{
				log: {
					entries: [
						{
							request: {
								url: http://www.arcgis.com/
							}
						},
						{
						},
						...
					]
				}
			}

	'''

	if not silent: print "\nOpening %s..." % url

	# Set up the proxy for extracting the network traffic
	server = Server(os.path.join(os.sep, get_home_folder(), 'webdrivers', 'browsermob-proxy-2.1.4', 'bin', 'browsermob-proxy'))
	server.start()
	
	try:
		proxy = server.create_proxy()
	except Exception, e:
		print e
		err_dict = collections.OrderedDict()
		err_dict['err'] = e
		return err_dict
		
	profile = webdriver.FirefoxProfile()
	profile.set_proxy(proxy.selenium_proxy())

	# Set the options for the Firefox, mainly --headless
	options = Options()
	options.add_argument("--headless")

	# Create the driver and extract the traffic
	driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
	proxy.new_har(url, options={'captureHeaders': True})

	# print url

	driver.get(url)
	# delay = 2

	# Parse the input attrb
	#	(<element attribute name>, <element attribute value>)
	#	ex: ('class', 'esriAttribution')
	attr_name = attrb[1]
	el_type = attrb[0]

	# Create the by_val for the driver wait
	if el_type == 'id':
		by_val = By.ID
	else:
		by_val = By.CLASS_NAME

	# Create the wait
	try:
		myElem = WebDriverWait(driver, delay).until(
			EC.presence_of_element_located((by_val, attr_name)))  # 'addthis_button_compact')))
		if not silent: print "Page is ready!"
	except TimeoutException:
		print "Loading took too much time!"
	# rec_html = driver.page_source

	result = proxy.har

	server.stop()
	driver.quit()

	return result

def get_network_urls(url, attrb, delay=2):
	''' Gets a list of the files loaded for a web page.
		:param url: The web page URL to load.
		:param attrb: A tuple containing (<element attribute name>, <element attribute value>)
							ex: ('class', 'esriAttribution')
		:param delay: The delay, in seconds, to wait until scraping the page.
		:return: A list of the entries in the page's network information.
	'''

	# Get the network info for the given page
	network_info = get_network_traffic(url, attrb, delay)

	network_urls = []

	# Get the log of the network info
	log = network_info['log']
	# Get the entries of the log
	entries = log['entries']

	for entry in entries:
		# Get the request of the entry
		request = entry['request']
		# Get the URL
		url = request['url']
		# Add URL to list
		network_urls.append(url)

	return network_urls

def get_post_query(url, form_data, api_type=''):
	''' Builds a URL query string using a dictionary of parameters and values
	:param url: The base URL which the query string will be added to.
	:param form_data: A dictionary containing parameters and values for the query string.
	:return: A string of the query URL.
	'''

	params = []
	if api_type == 'ckan':
		for k, v in form_data.items():
			if not v == '':
				if k == 'q' or k == 'rows' or k == 'start':
					param_str = "%s=%s" % (k, v)
				else:
					param_str = 'fq=%s:%s' % (k, v)
				params.append(param_str)
	else:
		for k, v in form_data.items():
			if type(v) is list:
				for d in v:
					if not d == '':
						param_str = "%s=%s" % (k, d)
						params.append(param_str)
			else:
				if not v == '':
					param_str = "%s=%s" % (k, v)
					params.append(param_str)
	param_url = "&".join(params)
	query = url + "?" + param_url

	return query
	
def get_pt_abbreviation(pt):
	''' Gets the provincial/territorial 2-letter abbreviation
	'''
	
	if pt.lower() == 'alberta':
		return 'AB'
	elif pt.lower() == 'british columbia':
		return 'BC'
	elif pt.lower() == 'canada':
		return 'CA'
	elif pt.lower() == 'manitoba':
		return 'MB'
	elif pt.lower() == 'new brunswick':
		return 'NB'
	elif pt.lower().find('newfoundland') > -1 or \
		pt.lower().find('labrador') > -1:
		return 'NL'
	elif pt.lower() == 'nova scotia':
		return 'NS'
	elif pt.lower() == 'northwest territories' or pt.lower() == 'nwt':
		return 'NT'
	elif pt.lower() == 'nunavut':
		return 'NU'
	elif pt.lower() == 'ontario':
		return 'ON'
	elif pt.lower().find('edward') > -1 or pt.lower() == 'pei':
		return 'PE'
	elif pt.lower() == 'quebec':
		return 'QC'
	elif pt.lower() == 'saskatchewan':
		return 'SK'
	elif pt.lower() == 'yukon':
		return 'YT'
	else:
		return pt
		
def get_pt_folders(juris=None):
	''' Gets a list of the paths for the P/T results
	'''
	
	res_folder = get_results_folder()
	pt_folders = glob.glob(os.path.join(os.sep, res_folder, '*/'))
	
	return pt_folders
		
def get_pt_name(pt_abbrev):
	''' Gets the province name based on the 2-letter abbreviation.
	'''
	
	if pt_abbrev.lower() == 'ab':
		return 'Alberta'
	elif pt_abbrev.lower() == 'bc':
		return 'British Columbia'
	elif pt_abbrev.lower() == 'mb':
		return 'Manitoba'
	elif pt_abbrev.lower() == 'nb':
		return 'New Brunswick'
	elif pt_abbrev.lower() == 'nl':
		return 'Newfoundland & Labrador'
	elif pt_abbrev.lower() == 'ns':
		return 'Nova Scotia'
	elif pt_abbrev.lower() == 'nu':
		return 'Nunavut'
	elif pt_abbrev.lower() == 'nt':
		return 'Northwest Territories'
	elif pt_abbrev.lower() == 'on':
		return 'Ontario'
	elif pt_abbrev.lower() == 'pe':
		return 'Prince Edward Island'
	elif pt_abbrev.lower() == 'qc':
		return 'Quebec'
	elif pt_abbrev.lower() == 'sk':
		return 'Saskatchewan'
	elif pt_abbrev.lower() == 'yt' or pt_abbrev.lower() == 'yk':
		return 'Yukon'
	else:
		return pt_abbrev
		
def get_results_folder(pt=None):
	''' Gets the path of the results folder.
	'''
	
	home_folder = get_home_folder()
	res_folder = home_folder + "\\results"
	
	# Return the results folder if no province/territory mentioned
	if pt is None: return res_folder
	
	pt_folder = '%s\\%s' % (res_folder, pt)
	
	return pt_folder

def get_request(url, form_data, headers=None, silent=True):
	''' Gets a URL request with specified form_data.
	:param url: The URL for the request
	:param form_data: A dictionary of form data for the request.
	:param headers: A list of headers for the request.
	:return: A tuple containing the text of the request results and the request query URL.
	'''

	asp_query = get_post_query(url, form_data)
	
	if not silent:
		print "\nOpening:"
		print "'%s'..." % asp_query

	s = requests.session()
	r = s.post(url, headers=headers, data=form_data)
	page = requests.get(url)

	return (r.text, asp_query)
	
def get_service_url(url):
	''' Gets the base server URL
	'''

	# Get the mapserver base URL
	url_split = url.split('/')
	#print "url_split: %s" % url_split
	# Remove 'MapServer'
	url_lst = url_split[:len(url_split) - 1]
	#print "url_lst: %s" % url_lst
	# Check if the last item is an integer (date)
	#	and if so, remove it (for Alberta services only)
	if len(url_lst) == 0: return ''
	if url_lst[len(url_lst) - 1].isdigit():
		url_lst = url_lst[:len(url_lst) - 1]
	#print "url_lst: %s" % url_lst
	new_url = '/'.join(url_lst)
	
	return new_url

def get_spatialref(json_dict, sp_key=None):
	''' Locates the spatialReference item in a JSON formatted text.
	:param json_dict: The JSON dictionary.
	:param sp_key: The spatial reference key to locate.
	:return: A formatted string of the spatial reference.
				If the spatial reference contains 'wkid', then the text is
				formatted with "(WKID: <wkid>) <spatial reference>".
	'''

	# Get the spatial reference
	if sp_key is None: sp_key = 'spatialReference'

	# Locate the 'spatialReference' item in the JSON dictionary
	sp = get_key(json_dict, sp_key)

	# Format the spatial reference, depending if it is WKID of WKT
	proj_str = ""
	if sp is not None:
		if 'wkid' in sp:
			wkid = sp['wkid']
			proj = wkid_to_spatref(wkid)
			if proj is not None:
				proj_str = '(WKID: %s) %s' % (wkid, proj['Name'])
		elif 'wkt' in sp:
			proj_str = sp['wkt'].replace('"', '""')

	return proj_str

def info_to_dict(table, text_only=False):
	''' Converts a table with a list of information to a dictionary:

		Ex Table:

			Citation Information:   <- the heading
				Title:	        DP ME 002, Version 11, 2016, Nova Scotia Mineral Occurrence Database
				Originator:	    G. A. O'Reilly , G. J. Demont , J. C. Poole , B. E. Fisher
				Date:	        March 2016
				...

	:param table: The <table> element.
	:param text_only: Return only text.
	:param heading_attrb: A tuple or list containing (<element attribute name>, <element attribute value>)
							for the column <td>.
							ex: ('class', 'esriAttribution')
	:param heading_tag: The tag containing the heading.
	:return: Returns a dictionary of the items in the table.
	'''

	rows = table.find_all('tr')

	table_dict = collections.OrderedDict()

	heading_str = ''
	for row in rows:
		# Get all the columns in the table
		cols = row.find_all('td')

		# Get the heading text from the <a> with no 'href'
		a = row.find('a')
		if a is not None:
			if not a.has_attr('href'):
				heading = bsoup.get_text(a)
				if not heading == '': heading_str = heading

		# Use only columns with text
		valid_cols = [col for col in cols if not col.text.strip() == ""]

		# The number of columns has to be greater than 1 in order to have a key and value
		if len(valid_cols) > 1:
			# if heading_tag is None:
			#     # No categories necessary
			#
			#     # Get the key of the current item from the first columns text
			#     key = valid_cols[0].text
			#     # Split the key by ':'
			#     key = key.strip().strip(':')
			#     if text_only:
			#         entries = [bsoup.get_text(v) for v in valid_cols]
			#     else:
			#         entries = valid_cols
			#
			#     table_dict[key] = entries
			#
			# else:

			if not heading_str == '':
				if heading_str in table_dict.keys():
					# If the dictionary with the category already exists, get it
					entries = table_dict[heading_str]
				else:
					# If no dictionary exists, create it
					entries = collections.OrderedDict()

				# Get the key of the current item from the first columns text
				key = valid_cols[0].text
				# Split the key by ':'
				key = key.strip().strip(':')
				if text_only:
					value = [v.text.strip() for v in valid_cols]
				else:
					value = valid_cols

				# Add the item to the entries dictionary
				entries[key] = value

				# Add the entries dictionary to the table_dict
				table_dict[heading_str] = entries

	return table_dict
	
def is_float(in_str):
	try:
		float(in_str)
		return True
	except:
		return False
	
def merge_duplicates(rows, dup_tuples):

	#print dup_tuples
	#print len(dup_tuples)
	
	merged_rows = []
	for idx, indices in enumerate(dup_tuples):
	
		msg = "Merging duplicates: %s of %s rows" % (idx + 1, len(dup_tuples))
		print_oneliner(msg)
		
		merged_entry = collections.OrderedDict()
		
		# Get a list of items for the current duplicate indices
		itms = [rows[i] for i in indices]
		
		# FOR DEBUG
		# for i in itms:
			# print
			# print i
		# answer = raw_input("Press enter...")
		
		# Get the title and description from the first entry
		title_str = itms[0]['Title']
		desc_str = itms[0]['Description']
		
		# Add the title and description to the final entry
		merged_entry['Title'] = title_str
		merged_entry['Description'] = desc_str
		
		# Get a list of dates and find the latest date
		#print title_str
		dates = [r['Recent Date'] for r in itms \
					if not r['Recent Date'] == '']
		if len(dates) == 0:
			start_date = ''
			latest_date = ''
		else:
			start_date, latest_date = get_minmax_date(dates, '%Y%m%d')
		
		# Add the latest date to the final entry
		merged_entry['Recent Date'] = latest_date#.strftime('%Y%m%d')
		merged_entry['Start Date'] = start_date#.strftime('%Y%m%d')
		
		# FOR DEBUG
		# if title_str.find('Health Service Delivery Areas') > -1:
			# print [r['Recent Date'] for r in itms]
			# print "Start Date: %s" % start_date
			# print "Latest Date: %s" % latest_date
			# answer = raw_input("Press enter...")
		
		#print latest_date
		
		# Go through each other key, ignoring the ones already done
		for k in itms[0].keys():
			if k == 'Title' or k == 'Description' or k == 'Recent Date' \
				or k == 'Start Date':
				continue
			
			# Get a list of entries for the current key
			# vals = [i[k] for i in itms]
			
			vals = []
			for i in itms:
				if k in i:
					val = i[k]
					vals.append(val)
			
			#print vals
			
			# Check if any vals contain a date
			date_check = False
			for v in vals:
				check = re.search('\d{4}\d{2}\d{2}', v)
				if check is not None:
					date_check = True
					break
					
			if date_check:
				# Get a list of regular expression searches
				re_dates = [re.search('\d{4}\d{2}\d{2}', v) for v in vals]
				
				# Get the string results of the dates
				dates = [d.group(0) if d is not None else d for d in re_dates]
				
				#print dates
				
				# Get the most recent date
				start_date, recent_date = get_minmax_date(dates, '%Y%m%d')
				
				#print recent_date
				
				# Get the URL with the most recent date
				#print vals
				#print recent_date
				try:
					new_val = [url for url in vals if url.find(recent_date) > -1][0]
				except IndexError as e:
					new_val = [url for url in vals][0]
				
			else:
				new_val = ''
				for v in vals:
					if not v == '':
						new_val = v
						break
						
			merged_entry[k] = new_val
			
		merged_rows.append((indices[0], merged_entry))
		
	return merged_rows

def open_selenium_page(url, attrb, delay=2, silent=True, browser='firefox'):
	''' Opens a page using Selenium and waits until a specific element is loaded on the page.
	:param url: The URL of the page to load.
	:param attrb: A tuple containing (<element attribute name>, <element attribute value>)
					ex: ('class', 'esriAttribution')
	:param delay: The delay, in seconds, to wait until the contents is grabbed from the page.
	:param silent: If True, nothing will be printed.
	:param browser: The browser name used to open the page.
	:return: The contents of the page after the element (attrb) has been loaded.
	'''

	if not silent:
		print "\nOpening %s..." % url

	# Get the driver based on the browser name
	driver = get_driver(browser)

	# Get the URL
	try:
		driver.get(url)
	except Exception, e:
		print "\nERROR: %s" % e
		err_dict = collections.OrderedDict()
		err_dict['err'] = e
		return err_dict

	# Get the attribute and the element type
	attr_name = attrb[1]
	el_type = attrb[0]

	# Set the By value
	if el_type == 'id':
		by_val = By.ID
	else:
		by_val = By.CLASS_NAME

	# Wait for the element to load
	try:
		myElem = WebDriverWait(driver, delay).until(
			EC.presence_of_element_located((by_val, attr_name)))  # 'addthis_button_compact')))
		if not silent:
			print "Page is ready!"
	except TimeoutException:
		if not silent:
			print "Loading took too much time!"

	# Get the contents of the page
	rec_html = driver.page_source

	# Close the browser
	driver.quit()

	return rec_html

def open_selenium_wait(url, delay=2, silent=True, browser='firefox'):
	''' Opens a page using Selenium and waits explicitly for the number of seconds
		of delay.
	:param url: The URL of the page to load.
	:param delay: The delay, in seconds, to wait until the contents is grabbed from the page.
	:param silent: If True, nothing will be printed.
	:param browser: The browser name used to open the page.
	:return: The contents of the page after waiting to load.
	'''

	if not silent:
		print "\nOpening %s..." % url

	# Get the driver based on the browser name
	driver = get_driver(browser)

	# Wait for the value of delay
	driver.implicitly_wait(delay)

	# Get the URL
	driver.get(url)

	# Get the contents of the page
	rec_html = driver.page_source

	# Close the browser
	driver.quit()

	return rec_html

def open_webpage(url):
	''' Opens a web page using urllib2
	:param url: The URL of the page to open.
	:return: If an error occurs, return None, otherwise return the page's HTML contents.
	'''

	try:
		url = url.replace(' ', '%20')
		context = ssl._create_unverified_context()
		url_html = urllib2.urlopen(url, context=context)
	# except urllib2.HTTPError, e:
		# print e.code
		# # return None
		# return e.code
	# except urllib2.URLError, e:
		# print e.reason
		# return None
	# except:
	#     traceback.print_exc(file=sys.stdout)
	#     print "ERROR: '%s' does not exist." % url
	#     return None
	except Exception as e:
		#print "\nError in open_webpage: %s" % str(e)
		#print "%s\n" % url
		err_dict = collections.OrderedDict()
		err_dict['err'] = str(e)
		return err_dict

	return url_html
	
def output_json(in_json, out_fn):
	''' Outputs JSON data to a file.
	'''

	r = json.dumps(in_json)
	loaded_r = json.loads(r)

	with open(out_fn, "w") as d_file:
		json.dump(loaded_r, d_file, indent=4, sort_keys=True)
	
def parse_csv_row(in_row):
	''' Divides at quotes CSV line into a list
	'''
	
	in_row = in_row.replace(',,', ',"",')

	indices = [m.start() for m in re.finditer('","', in_row)]
	
	out_row = []
	
	#print indices
	#print len(indices)
	
	for idx, i in enumerate(indices):
		start = i + 3
		# Add the first item in the list before the start index
		if idx == 0:
			col = in_row[1:start - 3]
			out_row.append(col)
		if idx > len(indices) - 2:
			col = in_row[start:]
		else:
			end = indices[idx + 1]
			col = in_row[start:end]
			
		#col = col.replace('""', '"')
		col = col.strip('"\n')
		
		out_row.append(col)
		
	#if out_row[1].find('Compilation of In Situ Stress Data from Alberta and Northeastern') > -1:
	#	print "\n"
	#	for c in out_row:
	#		print c
	#	answer = raw_input("Press enter...")
		
	return out_row

def parse_query_url(url):
	''' Retrieves the base URL of a query string.
	:param url: The URL query string.
	:return: The base URL.
	'''

	end_pos = url.find('?')
	parse_url = url[:end_pos].split("/")

	return parse_url
	
def process_duplicates(in_rows):
	''' Finds duplicates and merges them.
	'''

	# Merge any duplicate records
	dup_tuples = find_duplicates(in_rows)
	all_dups = [x for t in dup_tuples for x in t]
	
	merged_rows = merge_duplicates(in_rows, dup_tuples)
	merged_indices = [v[0] for v in merged_rows]
	
	# Go through each item in the in_rows, ignore duplicates indices
	filtered_rows = []
	for idx, row in enumerate(in_rows):
		if idx in merged_indices:
			# If the current index is contained in the merged_rows,
			#	make the output row the merged row
			new_row = [v[1] for v in merged_rows if v[0] == idx][0]
			filtered_rows.append(new_row)
		else:
			if idx not in all_dups:
				# If the current index is not part of a duplicate,
				#	make the output row the original row
				new_row = row
				filtered_rows.append(new_row)
				
	return filtered_rows
	
def prompt_juris(juris):

	answer = 'debug'
	
	while answer == "debug":
		if juris is None:
			print '''
Available Provincial/Territorial Options (not case sensitive):
 - CA, Canada
 - AB, Alberta
 - BC, British Columbia
 - MB, Manitoba
 - NB, New Brunswick
 - NL, Newfoundland & Labrador
 - NS, Nova Scotia
 - NU, Nunavut
 - NT, Northwest Territories
 - ON, Ontario
 - PE, Prince Edward Island
 - QC, Quebec
 - SK, Saskatchewan
 - YT, Yukon'''
			answer = raw_input("Please enter a province or territory " \
								"for extraction (options above): ")
			if answer == "debug":
				print "\nEntering debug mode."
				return 'debug'
			if not answer == "":
				juris = answer.lower()
			else:
				print "\nERROR: Invalid province or territory. " \
						"Please specify a valid one from the list of options."
				print "Exiting process."
				return None
		else:
			answer = ''
			
	if juris is None: return None
			
	if juris.lower() == 'canada' or juris.lower() == 'ca':
		juris = 'Canada'
	elif juris.lower() == 'alberta' or juris.lower() == 'ab':
		juris = 'Alberta'
	elif juris.lower() == 'british columbia' or juris.lower() == 'bc':
		juris = 'BC'
	elif juris.lower() == 'manitoba' or juris.lower() == 'mb':
		juris = 'Manitoba'
	elif juris.lower() == 'new brunswick' or juris.lower() == 'nb':
		juris = 'New Brunswick'
	elif juris.lower().find('newfoundland') > -1 or juris.lower().find('labrador') > -1 or juris.lower() == 'nl':
		juris = 'NL'
	elif juris.lower() == 'nova scotia' or juris.lower() == 'ns':
		juris = 'Nova Scotia'
	elif juris.lower() == 'nunavut' or juris.lower() == 'nu':
		juris = 'Nunavut'
	elif juris.lower().find('northwest') > -1 or juris.lower() == 'nt':
		juris = 'NWT'
	elif juris.lower() == 'ontario' or juris.lower() == 'on':
		juris = 'Ontario'
	elif juris.lower().find('edward') > -1 or juris.lower() == 'pe':
		juris = 'PEI'
	elif juris.lower() == 'quebec' or juris.lower() == 'qc':
		juris = 'Quebec'
	elif juris.lower() == 'saskatchewan' or juris.lower() == 'sk':
		juris = 'Saskatchewan'
	elif juris.lower() == 'yukon' or juris.lower() == 'yt' or juris.lower() == 'yk':
		juris = 'Yukon'
	elif answer.lower() == 'help' or answer.lower().find('h') > -1:
		#parser.print_help()
		return 'help'
	else:
		if juris.lower() == 'quit' or juris.lower() == 'exit': return 'exit'
		print "\nERROR: '%s' is not a valid province or territory."
		print "Exiting process."
		return None
		
	return juris
	
def print_oneliner(msg, leading="****"):
	''' Prints the msg to the command-prompt in one line
	:param msg: The message to print.
	:return: None
	'''

	sys.stdout.write('\r')
	sys.stdout.write("%s %s %s" % (leading, msg, leading))
	sys.stdout.flush()

def query_to_dict(url):
	''' Converts a query URL string into a dictionary of its parameters and values
	:param url: The URL with the query string.
	:return: A dictionary with the parameters of the query string as keys.
	'''

	# Split the URL by '?'
	url_split = url.split('?')

	if len(url_split) > 1:
		# If the URL has a query string
		query = url_split[1]

		# The parameters are divided by '&'
		params = query.split('&')

		query_dict = collections.OrderedDict()

		for param in params:
			# Split each by '=' to get the parameter name and value
			key = param.split('=')[0]
			value = param.split('=')[1]

			query_dict[key] = value

		return query_dict
		
def reduce_text(in_text, tag_names=None):
	''' Reduces the description text to 100 characters.
	:param desc: The description text
	:param tag_names: The tag name in an HTML description with the description text.
	:return: The edited description.
	'''

	out_text = ''
	if in_text is not None and not in_text == "":
		if tag_names is not None and in_text.find("<DIV") > -1:
			desc_soup = BeautifulSoup(in_text, 'html.parser')
			tag = desc_soup.find(tag_names)
			out_text = tag.text
		elif in_text.find("<") > -1:
			desc_soup = BeautifulSoup(in_text, 'html.parser')
			out_text = bsoup.get_text(desc_soup)
		#if len(in_text) > 100:
		#	out_text = in_text[:100].replace('"', '""') + "..."

	out_text = out_text.strip()
	out_text = out_text.replace("\r\n", "; ")

	return out_text
		
def remove_duplicates(in_lst):
	''' Removes duplicates by merging them.
	'''
	
	# Merge any duplicate records
	dup_tuples = find_duplicates(in_lst)
	all_dups = [x for t in dup_tuples for x in t]
	
	merged_rows = merge_duplicates(in_lst, dup_tuples)
	merged_indices = [v[0] for v in merged_rows]
	
	# Go through each item in the in_lst, ignore duplicates indices
	final_rows = []
	for idx, row in enumerate(in_lst):
		if idx in merged_indices:
			# If the current index is contained in the merged_rows,
			#	make the output row the merged row
			new_row = [v[1] for v in merged_rows if v[0] == idx][0]
			final_rows.append(new_row)
		else:
			if idx not in all_dups:
				# If the current index is not part of a duplicate,
				#	make the output row the original row
				new_row = row
				final_rows.append(new_row)
				
	return final_rows
	
def reproject_coords(in_coords, in_srs, t_srs=None):
	
	if t_srs is None:
		t_srs = osr.SpatialReference()
		t_srs.ImportFromEPSG(4326)
	
	transform = osr.CoordinateTransformation(in_srs, t_srs)
	
	out_coords = []
	for pnt in in_coords:
		geom = ogr.Geometry(ogr.wkbPoint)
		geom.AddPoint(pnt[0], pnt[1])
		try:
			geom.Transform(transform)
		except:
			return []
		out_coords.append((geom.GetX(), geom.GetY()))
		
	return out_coords

def sort_fields(in_flds):
	''' Sorts a list of header fields in a specified order.
	:param in_flds: A list of headers for fields
	:return: A list of the sorted headers.
	'''

	fields = ['Source', 'Title', 'Description', 'Type', 'Start Date', 
			'Recent Date', 'Update Frequency', 
			'Publisher', 'Licensing', 'Available Formats', 
			'Access', 'Download', 'Spatial Reference', 
			'Data URL', 'Web Page URL', 'Web Map URL', 
			'Service', 'Service Name', 'Service URL', 
			'Metadata URL', 'Metadata Type', 'Notes']
	sort_fields = [f for f in fields if f in in_flds]
	for f in in_flds:
		if not f in sort_fields:
			sort_fields.append(f)
	return sort_fields

def soup_php(url):
	''' Soups up a PHP URL.
	:param url: The PHP URL.
	:return: A soup object.
	'''

	html_text = open_webpage(url)
	if isinstance(html_text, int): return html_text
	if isinstance(html_text, dict): return html_text
	soup = BeautifulSoup(html_text, 'html.parser')
	soup_str = str(soup)
	out_soup = BeautifulSoup(soup_str, 'html.parser')
	return out_soup

def split_upper(word):
	''' Splits a string at its capital letters
	:param word: A string with capital letters.
	:return: A string with spaces in front of every capital letter.
	'''

	# Split at capital letters
	caps = re.split('([A-Z]+[a-z]+)', word)

	# Remove white spaces and empty strings from the list
	word_list = [w.strip() for w in caps if not w == '' and not w == ' ']

	# Join the list with spaces
	out_word = ' '.join(word_list)

	return out_word

def table_to_dict(table, header_row=None, header=None, text_only=False, start_row=0):
	''' Converts a spreadsheet table to a dictionary.
	   Example Table:
		   Title       Orginator       Date
		   --------------------------------------
		   DP ME 002   G. A. O...      March 2016
		   DP ME 154   B. E. Fisher    2006
		   ...
	:param table: A soup object containing the table.
	:param header_row: The row number which contains the header info.
	:param header: A list of header values in case none exist in the table.
	:param text_only: Determines whether only to return the text of the table and not the HTML code.
	:param start_row: The row number in which to start collecting the data.
	:return: A list of rows, each containing a dictionary with the header as keys.
	'''

	#print "header_row: " + str(header_row)
	#print "header: " + str(header)
	#print "start_row: " + str(start_row)

	# Get all the rows
	rows = table.find_all('tr')

	#print "Number of rows: " + str(len(rows))

	if header is None:
		# If a list of header values is not provided, determine the header
		#   by other means

		header = []
		# Some tables contain their own header tags as <th>.
		#   Check to see if they exist.
		th = table.find_all('th')
		if th is None or len(th) == 0:
			# If no <th> tags exist, create the th list
			if header_row is not None:
				# Get the header row based on the header_row
				#   value provided

				# The starting row of the data will be just after the
				#   header row
				if start_row == 0:
					start_row = header_row + 1
				# Get the entire row of the header_row
				header_text = rows[header_row]
				# Set the th value to the header row
				th = header_text
		else:
			# Set the starting row of the data to 1
			if start_row == 0:
				start_row = 1

		if th is not None:
			# Cycle through each item in the th list
			for h in th:
				# If the <th> is a NavigableString, skip it
				if not isinstance(h, NavigableString):
					header_txt = h.text
				else:
					continue
				# Clean the header_text
				header_txt = clean_text(header_txt)
				# If the header is blank, call the column 'null'
				if not header_txt.strip() == "":
					header_str = header_txt.strip()
				else:
					header_str = 'null'
				# Add the header to the header list
				header.append(header_str.lower())

		# If the header list has duplicates,
		#   append '_1' to them
		dups = {}
		for i, val in enumerate(header):
			if val not in dups:
				# Store index of first occurrence and occurrence value
				dups[val] = [i, 1]
			else:
				# Special case for first occurrence
				if dups[val][1] == 1:
					header[dups[val][0]] += str(dups[val][1])

				# Increment occurrence value, index value doesn't matter anymore
				dups[val][1] += 1

				# Use stored occurrence value
				header[i] += str(dups[val][1])

	table_list = []

	final_rows = []
	for r_idx in range(start_row, len(rows)):
		row = rows[r_idx]

		th_cols = row.find_all('th')
		td_cols = row.find_all('td')

		row_dict = collections.OrderedDict((k, "") for k in header)

		cols = th_cols + td_cols

		#print "Number of columns: " + str(len(cols))

		key_list = row_dict.keys()

		#print "key_list: " + str(key_list)

		for pos, col in enumerate(cols):
			#print "pos: " + str(pos)
			if text_only:
				val = col.text
			else:
				val = col
			row_dict[key_list[pos]] = val

		table_list.append(row_dict)

	# print table_list

	return table_list

def translate_date(tmestmp):
	''' Converts a timestamp value to a formatted date.
	:param tmestmp: The input timestamp.
	:return: A formatted date based on the timestamp.
	'''

	if isinstance(tmestmp, str) or isinstance(tmestmp, unicode):
		tmestmp = float(tmestmp)
	
	if len(str(tmestmp)) == 13:
		# Date includes milliseconds
		fs_timestamp = tmestmp / 1000.0
	else:
		# Date doesn't include milliseconds
		fs_timestamp = tmestmp
	out_date = datetime.datetime.fromtimestamp(fs_timestamp).strftime('%Y-%m-%d %H:%M:%S')

	return out_date

def wait_page_load(driver, attr_type, attr_name, delay=10, silent=True):
	''' Implements a wait command for a selenium driver
	:param driver: The selenium drive object.
	:param attr_type: The attribute type to wait to load (By.ID or By.CLASS_NAME).
	:param attr_name: The attribute value that must be loaded before proceeding.
	:param delay: The number of seconds the driver should wait.
	:return: None
	'''
	try:
		wait_ec = EC.presence_of_element_located((attr_type, attr_name))
		myElem = WebDriverWait(driver, delay).until(wait_ec)  # 'addthis_button_compact')))
		if not silent: print "Page is ready!"
	except TimeoutException:
		print "Loading took too much time!"
	except:
		return None

def wkid_to_spatref(wkid):
	''' Converts a WKID value to a spatial reference text using two JSON files.
	:param wkid: The WKID spatial reference value.
	:return: A string of the spatial reference with the WKID in brackets.
	'''

	file_folder = os.path.join(os.sep, get_home_folder(), 'files')
	json_fn = file_folder + "\\wkid_list.json"
	json_old_fn = file_folder + "\\wkid_old_list.json"

	if not os.path.exists(json_fn):
		proj_url = "https://developers.arcgis.com/rest/services-reference/projected-coordinate-systems.htm"
		geo_url = "https://developers.arcgis.com/rest/services-reference/geographic-coordinate-systems.htm"

		# Extract the projected table
		proj_soup = soup_it_up(proj_url, True, ['id', 'afb'])
		proj_table = proj_soup.find('table', attrs={'class': 'tablexyz'})
		proj_list = table_to_dict(proj_table, text_only=True)
		# print ','.join(proj_list[0])

		# Extract the geographic table
		geo_soup = soup_it_up(geo_url, True, ['id', 'afb'])
		geo_table = geo_soup.find('table', attrs={'class': 'tablexyz'})
		geo_list = table_to_dict(geo_table, text_only=True)

		wkid_list = proj_list + geo_list

		json_data = json.dumps(wkid_list)

		# Open the JSON file
		json_f = open(json_fn, 'w')
		json_f.write(json_data)
		json_f.close()

	if not os.path.exists(json_old_fn):
		proj_url = "http://resources.esri.com/help/9.3/arcgisserver/apis/rest/pcs.html"
		geo_url = "http://resources.esri.com/help/9.3/arcgisserver/apis/rest/gcs.html"

		# Extract the projected table
		proj_soup = soup_it_up(proj_url)  # , True, ['id', 'afb'])
		proj_table = proj_soup.find('table', attrs={'class': 'detailTABLE'})
		proj_old_list = table_to_dict(proj_table, text_only=True)
		# print ','.join(proj_list[0])

		# Extract the geographic table
		geo_soup = soup_it_up(geo_url)  # , True, ['id', 'afb'])
		geo_table = geo_soup.find('table', attrs={'class': 'detailTABLE'})
		geo_old_list = table_to_dict(geo_table, text_only=True)

		wkid_old_list = proj_old_list + geo_old_list

		json_old_data = json.dumps(wkid_old_list)

		# Open the JSON file
		json_old_f = open(json_old_fn, 'w')
		json_old_f.write(json_old_data)
		json_old_f.close()

	# answer = raw_input("Press enter...")

	# Open the WKID JSON file
	json_file = open(json_fn, 'r')
	json_list = json.load(json_file)
	json_file.close()

	for wkid_dict in json_list:
		file_wkid = clean_text(wkid_dict['Well-known ID'])
		if file_wkid == wkid:
			return wkid_dict

	# Open the old WKID JSON file
	json_old_file = open(json_old_fn, 'r')
	json_old_list = json.load(json_old_file)
	json_old_file.close()

	for wkid_dict in json_old_list:
		file_wkid = clean_text(wkid_dict['Well-known ID'])
		# print "'%s'" % file_wkid
		# if file_wkid == '102100':
		#	print "'%s'" % wkid
		#	answer = raw_input("Press enter...")
		if str(file_wkid) == str(wkid):
			# answer = raw_input("Press enter...")
			return wkid_dict

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
import pprint
import traceback
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

class UTF8Recoder:
	"""
	Iterator that reads an encoded stream and reencodes the input to UTF-8
	"""

	def __init__(self, f, encoding):
		self.reader = codecs.getreader(encoding)(f)

	def __iter__(self):
		return self

	def next(self):
		return self.reader.next().encode("utf-8")


class UnicodeReader:
	"""
	A CSV reader which will iterate over lines in the CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		f = UTF8Recoder(f, encoding)
		self.reader = csv.reader(f, dialect=dialect, **kwds)

	def next(self):
		row = self.reader.next()
		return [unicode(s, "utf-8") for s in row]

	def __iter__(self):
		return self


class UnicodeWriter:
	"""
	A CSV writer which will write rows to CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		# Redirect output to a queue
		self.queue = cStringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = f
		self.encoder = codecs.getincrementalencoder(encoding)()

	def writerow(self, row):
		self.writer.writerow([s.encode("utf-8") for s in row])
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)

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
	text_str = txt.replace("\n", " ")
	text_str = text_str.replace("\r", " ")
	text_str = text_str.strip()
	text_str = re.sub('[ \t]+', ' ', text_str)
	text_str = text_str.replace(u'\xa0', u' ')

	return text_str

def edit_description(desc, tag_names=None):
	''' Reduces the description text to 100 characters.
	:param desc: The description text
	:param tag_names: The tag name in an HTML description with the description text.
	:return: The edited description.
	'''

	if desc is not None and not desc == "":
		if tag_names is not None and desc.find("<DIV") > -1:
			desc_soup = BeautifulSoup(desc, 'html.parser')
			tag = desc_soup.find(tag_names)
			desc = tag.text
		elif desc.find("<") > -1:
			desc_soup = BeautifulSoup(desc, 'html.parser')
			desc = get_text(desc_soup)
		#if len(desc) > 100:
		#	desc = desc[:100].replace('"', '""') + "..."
	else:
		desc = ""

	desc = desc.strip()
	desc = desc.replace("\r\n", "; ")

	return desc

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
			
def filter_unicode(in_str, out_type=None, french=False):
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
				u'•': '-', u'°': '', u'©': ' copyright ', u'®': '', u'\xa0': ' ', 
				u'\u2011': '-'}
	replace_dict.update(other_dict)

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

def find_parent_tag(init_element, tag_name):
	''' Finds the previous parent tag with the tag_name.
	:param soup: The soup containing the initial tag
	:param tag_name: The tag name to locate.
	:return: The tag with tag_name.
	'''

	bof = False
	current_tag = init_element

	while not bof:
		parent_tag = current_tag.parent
		if parent_tag is None:
			bof = True
			continue
		if parent_tag.name == tag_name:
			out_tag = parent_tag
			return out_tag
		current_tag = parent_tag

def find_prev_tag_containing(init_element, txt):
	''' Finds the previous sibling tag with tag_name with part of contains.
		:param soup: The soup containing the initial tag
		:param txt: Part of the tag name to locate.
		:return: The tag with tag_name.
		'''

	bof = False
	current_tag = init_element

	while not bof:
		sib_tag = current_tag.find_previous_sibling()
		if sib_tag is None:
			bof = True
			continue
		if sib_tag.name.find(txt) > -1:
			out_tag = sib_tag
			return out_tag
		current_tag = sib_tag

def find_tag_by_text(soup, text, tag_name=None):
	''' Finds a tag with exact text in a tag
	:param soup: The soup to search in.
	:param text: The text to find.
	:param tag_name: The tag to locate. Default is to search all tags in soup.
	:return: The tag containing the text.
	'''

	if tag_name is None:
		# Get all the tags on the page
		tag_list = soup.find_all()
		results = []
		for tag in tag_list:
			# Find all tags containing text
			el_text = tag.find_all(text=True, recursive=False)
			if len(el_text) > 0:
				# If both text match, add the element to the result list
				if clean_text(el_text[0]) == text:
					results.append(tag)

		return results
	else:
		# Get all elements with the tag_name
		tag_list = soup.find_all(tag_name)

		for tag in tag_list:
			# Get the element's text and clean it
			tag_text = tag.text
			tag_clean = clean_text(tag_text)
			# If both the element text and input text are equal
			if tag_clean == text:
				#print type(tag)
				#print tag
				return tag
				
def find_tag_by_id(soup, contains, tag_name=None):
	''' Finds a tag with id containing the input string.
	:param soup: The soup to search in.
	:param contains: A id string used to located the tag.
	:param tag_name: The tag to locate. Default is to search all tags in soup.
	'''
	
	if tag_name is None:
		# If no tag name is provided

		# Get all elements on the page
		tag_list = soup.find_all()
		for tag in tag_list:
			# For each tag, find all elements which have text
			element = tag.find_all(text=True, recursive=False)
			if len(element) > 0:
				tag_id = element.get('id')
				if tag_id.find(contains) > -1:
					return element
				
	else:
		# Get a list of all elements with the given tag name
		tag_list = soup.find_all(tag_name)

		# Go through each tag and compare its text to the current string in contains list
		for tag in tag_list:
			#print "tag: %s" % tag
			tag_id = tag.get('id')
			if tag_id is None: continue
			if tag_id.find(contains) > -1:
				return tag
	

def find_tags_containing(soup, contains, tag_name=None, output=None):
	''' Finds a tag with text containing a certain string
	:param soup: The soup to search in.
	:param contains: A string or list of the text to find.
	:param tag_name: The tag to locate. Default is to search all tags in soup.
	:param output: Returns a list if output = 'list'.
	:return: The tag containing the text.
	'''

	# If the contains variable is a string, convert it to a list
	if isinstance(contains, str):
		contains = [contains]

	final_tags = []

	# Go through each word in contains
	for txt in contains:
		if tag_name is None:
			# If no tag name is provided

			# Get all elements on the page
			tag_list = soup.find_all()
			for tag in tag_list:
				# For each tag, find all elements which have text
				el_text = tag.find_all(text=True, recursive=False)
				if len(el_text) > 0:
					tag_text = clean_text(el_text[0])
					tag_text = tag_text.replace("  ", " ")
					if tag_text.lower().find(txt.lower()) > -1:
						final_tags.append(tag)
		else:
			# Get a list of all elements with the given tag name
			tag_list = soup.find_all(tag_name)

			# Go through each tag and compare its text to the current string in contains list
			for tag in tag_list:
				tag_text = tag.text
				tag_clean = clean_text(tag_text)
				if tag_clean.lower().find(txt.lower()) > -1:
					final_tags.append(tag)

	if output == 'list':
		return final_tags
	else:
		if len(final_tags) > 0:
			return final_tags[0]

def find_xml_tags(xml_soup, tag_names):
	''' Searches for a tag in an XML soup, ignoring cases.
	:param xml_soup: The XML soup.
	:param txt: The text used to find the tag.
	:return: The tag containing the text (or None is no tag is found).
	'''

	results = []
	# Go through each tag in tag_names
	for tag in tag_names:
		res = xml_soup.find(tag)
		if res is None:
			res = xml_soup.find(tag.lower())
		if res is not None:
			results.append(res)

	return results

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

def get_adj_tags_by_text(soup, tag, label, contains=False, url=None):
	''' Retrieves the adjacent tags of a tag with a given text (label).
		This is used for any text in a table with the label proceeding the value.
		Ex: If a page has an entry like "Created On: 2018-07-12", the label will be
			"Created On" and the return value will be "2018-07-12".
	:param soup: The soup containing the tag with a specific label.
	:param tag: The tag name of the label element.
	:param label: The label text.
	:param contains: If true, the method will search for any tag containing the label
	:return: A list of tags adjacent to any tags with label.
	'''

	# If soup is None, return empty text
	if soup is None:
		return []

	# Find all tags with specified name
	tags = soup.find_all(tag)

	# If no tags are found
	if len(tags) == 0:
		print "\nWARNING: Cannot find '%s' element next to label '%s'." % (tag, label)
		if url is not None:
			print url
		return []

	res = []
	for t in tags:
		# Cycle through each tag
		if contains:
			# If the user specified contains as true,
			#   then use the find command for strings
			if t.text.strip().find(label) > -1:
				sib = t.find_next_sibling()
				res.append(sib)
		else:
			# If contains is false, the tag text must match the label
			if t.text.strip() == label:
				sib = t.find_next_sibling()
				res.append(sib)

	# If no results found
	if len(res) == 0:
		print "\nWARNING: Cannot find an element with text '%s'." % label
		return []

	return res

def get_adj_text_by_label(soup, tag, label, contains=False, url=None):
	''' Retrieves the adjacent text of a tag with a given text (label).
		This is used for any text in a table with the label proceeding the value.
		Ex: If a page has an entry like "Created On: 2018-07-12", the label will be
			"Created On" and the return value will be "2018-07-12".
	:param soup: The soup containing the tag with a specific label.
	:param tag: The tag name of the label element.
	:param label: The label text.
	:param contains: If true, the method will search for any tag containing the label
	:return: The adjacent text of a tag with label (the first instance found).
	'''

	# If soup is None, return empty text
	if soup is None:
		return ''

	# Find all tags with specified name
	tags = soup.find_all(tag)

	# If no tags are found
	if len(tags) == 0:
		print "\nWARNING: Cannot find '%s' element next to label '%s'." % (tag, label)
		if url is not None:
			print url
		#answer = raw_input("Press enter...")
		return ''

	res = None
	for t in tags:
		# Cycle through each tag
		t_text = get_text(t).replace(':', '')
		if contains:
			# If the user specified contains as true,
			#   then use the find command for strings
			if t_text.find(label) > -1:
				res = t
		else:

			# If contains is false, the tag text must match the label
			if t_text == label:
				res = t

	# If no results found
	if res is None:
		#print "\nWARNING: Cannot find an element with text '%s'." % label
		return ''

	# Get the text of the adjacent element
	sib = res.find_next_sibling()
	out_text = get_text(sib)

	return out_text

def get_adjacent_cell(soup, tag, value):
	''' Gets the adjacent cell (column <td>) of a given tag and value.
	:param soup: The page's soup object.
	:param tag: The input tag name of the element.
	:param value: The input text of the element.
	:return: The sibling <td> of the input tag.
	'''

	# Find the element with tag and text value
	tag_soup = soup.find(tag, text=value)
	td_found = False
	tag_parent = tag_soup.parent
	while not td_found:
		# Keep going to previous parent until <td> is found
		tag_parent = tag_parent.parent
		if tag_parent.name == 'td':
			td = tag_parent
			td_found = True
	# Get the <td> sibling
	td_sib = td.find_next_sibling('td')

	return td_sib

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
	
	#print "data_url: %s" % data_url
	
	#answer = raw_input("Press enter...")
	
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
		if 'licenseinfo' in item: lic_str = get_text(item['licenseInfo'])

		# Get the description
		desc_str = ''
		if 'description' in item: desc_str = get_text(item['description'])

		# Get the map URL if applicable
		map_url = ''
		if 'url' in item: map_url = get_text(item['url'])

		# Get the data URL
		if map_url is None or map_url == '':
			if 'viewer' in item: map_url = get_arcgis_url(data_url, 'viewer')

		# Get the overview URL
		overview_url = ''
		if 'overview' in item: overview_url = get_arcgis_url(data_url, 'overview')

		notes_str = ''
		if 'notes' in item: notes_str = item['notes']

		# Set the map_data dictionary
		map_data = collections.OrderedDict()
		if pre_info is not None: map_data.update(pre_info)
		#print "map_data: %s" % map_data
		map_data['Title'] = title_str
		map_data['Description'] = desc_str
		map_data['Type'] = "ArcGIS " + str(item['type'])
		map_data['Date'] = translate_date(item['modified'])
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

	gallery_soup = get_soup(gallery_url, True)

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

		if url.find('item') > -1:
			# If the URL is already a data URL, get the ID from the basename of the URL
			id_bname = os.path.basename(url)
			id = id_bname.split('?')[0]
		else:
			# Get the ID of the ArcGIS map from the URL
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
		err_dict = collections.OrderedDict()
		err_dict['err'] = "Not a valid ArcGIS Online URL."
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

def get_bracket_text(txt):
	''' Gets the text between two round brackets.
	:param txt: The input text containing the brackets.
	:return: The text between the brackets.
	'''

	start_pos = txt.find('(') + 1
	end_pos = txt.find(')')
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

def get_dl_text(soup, text):
	''' Finds the <dt> tage with specified text and returns its corresponding <dd> text.
	:param soup: The soup containing the <dt> tag.
	:param text: The text so search for.
	:return: The text of the corresponding <dd> of the <dt> tag.
	'''
	out_str = ''
	dt = find_tags_containing(soup, text, 'dt')
	if dt is not None:
		dd = dt.find_next_sibling('dd')
		out_str = get_text(dd)

	return out_str

def get_download_text(formats, download_url='', date=''):
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
	
	if len(formats) == 0:
		return 'No|Contact the Province%s' % max_date
	elif len(formats) == 1:
		if isinstance(download_url, list):
			return '%s|Download/Web Accessible%s' % (download_url[0], max_date)
		else:
			return '%s|Download/Web Accessible%s' % (download_url, max_date)
	else:
		return 'Multiple Downloads|Download/Web Accessible%s' % max_date

def get_driver(browser='firefox'):
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
		firefox_folder = get_home_folder() + "\\webdrivers\\geckodriver-v0.20.0-win64\\geckodriver.exe"
		#print "Firefox Folder: %s" % firefox_folder
		# binary = FirefoxBinary(get_home_folder() + "\\webdrivers\\geckodriver-v0.20.0-win64\\geckodriver.exe")

		options = Options()
		options.add_argument("--headless")
		driver = webdriver.Firefox(firefox_options=options,
								   log_path='files\\geckodriver.log')  # , firefox_binary=binary)

	return driver

def get_first_text(soup):
	''' Gets the first text on a page.
	:param soup: The soup of the page.
	:return: The first text on a page.
	'''

	if soup is not None:
		if not isinstance(soup, NavigableString):
			# Find all the elements with text
			texts = soup.find_all(text=True)

			for txt in texts:
				# Get the first element with text
				if txt is not None and not txt.strip() == "":
					text_str = clean_text(txt)

					return text_str
		else:
			# If the soup is already a string, return it
			return soup

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

def get_home_folder():
	''' Gets the top folder location of the FGP_WebExtractor.
	:return: The folder location of the Web Extractor.
	'''

	top_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	return top_folder

def get_json(url, silent=True):
	''' Gets the JSON of a specified URL.
	:param url: The URL of the JSON data.
	:return: JSON formatted string.
	'''
	
	if not silent: print "\nJSON URL: %s" % url
	try:
		response = requests.get(url, timeout=10)
		#response = requests.request('GET', url)
		json_text = response.json()
	except requests.exceptions.Timeout:
		print "\nJSON Error: Timeout occurred"
		print "%s\n" % url
		json_text = collections.OrderedDict()
		json_text['err'] = "Timeout occurred."
	except:
		# html_text = open_webpage(url)
		# print html_text
		try:
			response = requests.get(url, timeout=10, verify=False)
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

def get_link_datasets(soup, txt_vals, in_url, tag_name=None):
	''' Gets the download links from a page with text in the
		txt_vals list.
	:param soup: The soup contents containing the links.
	:param txt_vals: A list of strings that are contained in the
					link tags.
	:return: A list of dictionaries containing the resulting records.
	'''

	a_tags = find_tags_containing(soup, txt_vals, tag_name, output='list')

	datasets = []

	#print "a_tags: %s" % a_tags

	for a in a_tags:
		if a is None: continue

		if isinstance(a, list):
			a = a[0]

		#print "a: %s" % a

		rec_dict = collections.OrderedDict()

		# Get the title of the dataset
		title_str = get_text(a)
		# Get the download link
		download_url = get_anchor_url(a, in_url)
		# Get the format from the URL
		if download_url.find('.zip') > -1:
			bsname, f_ext = os.path.basename(download_url).split('.')
			bsname_split = bsname.split('_')
			formats = [bsname_split[len(bsname_split) - 1]]
		else:
			bsname, f_ext = os.path.basename(download_url).split('.')
			formats = f_ext

		download_info = get_download_text(formats, download_url)
		download_str, access_str = download_info.split('|')

		rec_dict['Title'] = title_str
		rec_dict['Download'] = download_str
		rec_dict['Access'] = access_str
		rec_dict['Available Formats'] = "|".join([f.upper() for f in formats])

		datasets.append(rec_dict)

	return datasets

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

def get_page_count(soup, element_type, attrb, sub_element, subtract=2):
	''' Gets the number of pages from a specified element on the page
	:param soup: The soup containing the element.
	:param element_type: The element name to find.
	:param attrb: The attribute name and value as tuple (or list), ex: (<attr_name>, <attr_value>)
	:param sub_element: The element type of the buttons.
	:param subtract: Number of buttons to subtract to get the highest value.
	:return: The total number of pages.
	'''

	# Get the number of pages from page buttons at bottom of site
	#print "Attribute Name: %s" % attrb[0]
	#print "Attribute Value: %s" % attrb[1]
	page_res = soup.find(element_type, attrs={attrb[0]: attrb[1]})

	#print "page_res: " + str(page_res)

	if page_res is None:
		# If no element can be found, return a page count of 1
		page_count = 1
	else:
		# Get a list of all the sub-elements (ex: <li> in the <div>)
		link_list = page_res.find_all(sub_element)
		if len(link_list) == 0:
			# If no sub-elements exist, return a page count of 1
			page_count = 1
		else:
			# Grab the link that is subtract's value from the right (default is the second-last link)
			link = link_list[len(link_list) - subtract]
			page_count = link.text
			#print page_count
			if page_count is None:
				link_href = link.a['href']
				page_pos = link_href.find('page')
				end_pos = link_href.find('&', page_pos)
				page_query = link_href[page_pos:end_pos]
				page_count = page_query.split('=')[1]

			page_count = page_count.encode('ascii', 'ignore')
			page_count = page_count.replace("page", "")
			page_count = page_count.strip()

	return int(page_count)

def get_page_metadata(soup):
	''' Gets the metadata from the web page and puts them in a dictionary.
	:param soup: The soup of the page.
	:return: A dictionary containing the names of the metadata as keys and the contents as values.
	'''

	meta_tags = soup.find_all('meta')

	meta_dict = collections.OrderedDict()
	for meta in meta_tags:
		name = ''
		if meta.has_attr('name'): name = meta['name']
		elif meta.has_attr('itemprop'): name = meta['itemprop']
		elif meta.has_attr('property'): name = meta['property']
		
		if not name == '':
			content = meta['content']
			meta_dict[name] = content

	meta_dict['page_title'] = get_text(soup.find('title'))

	return meta_dict

def get_parent(soup, tag, attr=None):
	''' Gets the parent element with the given tag and attributes, if applicable.
	:param soup: The soup of the page.
	:param tag: The tag of the parent element.
	:param attr: A specific attribute name that the parent element will have (ex: 'class').
	:return: The parent element with the given tag.
	'''

	if soup is None:
		print "WARNING: Can't get parent since child is None."
		return None

	parent = soup.parent

	if parent is None: return parent

	if attr is None:
		if not parent.name == tag:
			# If the parent element name is not the same as tag, call get_parent again
			parent = get_parent(parent, tag)
		else:
			return parent
	else:
		if not parent.name == tag and not parent.has_attr(attr):
			# If the parent element name is not the same as tag and does not have the attr, call get_parent again
			parent = get_parent(parent, tag, attr)
		else:
			return parent

	return parent

def get_post_query(url, form_data):
	''' Builds a URL query string using a dictionary of parameters and values
	:param url: The base URL which the query string will be added to.
	:param form_data: A dictionary containing parameters and values for the query string.
	:return: A string of the query URL.
	'''

	params = []
	for k, v in form_data.items():
		if type(v) is list:
			for d in v:
				param_str = "%s=%s" % (k, d)
				params.append(param_str)
		else:
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
	elif pt.lower() == 'manitoba':
		return 'MB'
	elif pt.lower() == 'new brunswick':
		return 'NB'
	elif juris.lower().find('newfoundland') > -1 or juris.lower().find('labrador') > -1:
		return 'NL'
	elif pt.lower() == 'nova scotia':
		return 'NS'
	elif pt.lower() == 'northwest territories' or pt.lower() == 'nwt':
		return 'NT'
	elif pt.lower() == 'nunavut':
		return 'NU'
	elif pt.lower() == 'ontario':
		return 'ON'
	elif juris.lower().find('edward') > -1 or pt.lower() == 'pei':
		return 'PE'
	elif pt.lower() == 'quebec':
		return 'QC'
	elif pt.lower() == 'saskatchewan':
		return 'SK'
	elif pt.lower() == 'yukon':
		return 'YT'
	else:
		return pt
		
def get_pt_folders():
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
		
def get_results_folder():
	''' Gets the path of the results folder.
	'''
	
	home_folder = get_home_folder()
	res_folder = home_folder + "\\results"
	
	return res_folder

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

def get_soup(url, selenium=False, attrb=None, delay=2, silent=True, browser='firefox'):
	''' Retrieves the BeautifulSoup object for a specified web page.
	:param url: The URL of the web page.
	:param selenium: Determines whether the page should be open using Selenium or urllib2.
	:param attrb: A tuple containing (<element attribute name>, <element attribute value>)
						ex: ('class', 'esriAttribution')
	:param delay: For Selenium, the amount of delay in seconds before retrieving the BeautifulSoup object.
	:param silent: Determines whether statements should be printed.
	:return: The BeautifulSoup object containing the web page HTML content.
	'''

	if not silent:
		print "\nGetting soup for %s" % url

	# if selenium and attrb is not None:
	if selenium:
		if attrb is None:
			# html_text = open_selenium_page(url, attrb, delay)
			html_text = open_selenium_wait(url, delay, silent=silent, browser=browser)
		else:
			html_text = open_selenium_page(url, attrb, delay, silent=silent, browser=browser)
	else:
		html_text = open_webpage(url)
		if isinstance(html_text, int):
			err_resp = BaseHTTPRequestHandler.responses[html_text]
			#err_msg = "ERROR|%s" % err_resp[1]
			err_dict = collections.OrderedDict()
			err_dict['err'] = err_resp[1]
			return err_dict

	# If the html_text is None
	if html_text is None: return None
	elif isinstance(html_text, dict): return html_text

	# Set the soup
	soup = BeautifulSoup(html_text, 'html.parser')

	return soup

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

def get_text(soup):
	''' Gets the text for a given soup and cleans it.
	:param soup: The soup containing the text.
	:return: The clean text from the soup.
	'''

	# Set the soup to a list for processing
	soup_list = []
	if isinstance(soup, bs4.element.ResultSet):
		for r in soup:
			soup_list.append(r)
	else:
		soup_list.append(soup)

	text_list = []
	for s in soup_list:
		if soup is not None:
			if isinstance(s, NavigableString):
				text_str = clean_text(s)
			elif isinstance(s, str) or isinstance(s, unicode):
				if s.find("<") > -1:
					out_soup = BeautifulSoup(s, 'html.parser')
					text = out_soup.get_text()
					text_str = clean_text(text)
				else:
					text_str = s
			else:
				text = s.get_text()
				text_str = clean_text(text)

			text_list.append(text_str)

	final_text = ' '.join(text_list)

	return final_text

def get_xml_soup(url, silent=True, selenium=False):
	''' Gets the XML BeautifulSoup object of the URL page.
	:param url: The URL of the page containing XML data.
	:param silent: If true, statements will not be printed to the output.
	:param selenium: Determines whether to use Selenium when opening the page.
	:return: A BeautifulSoup object of the page.
	'''

	if not silent:
		print "Getting XML soup for %s" % url

	try:
		if selenium:
			# If Selenium is specified, use it to open the XML page
			r = open_selenium_wait(url)
		else:
			# Open the XML page
			resp = requests.get(url)
			r = resp.text
			if len(r.splitlines()) < 3:
				# If the XML page contains less than 3 lines, open the page using Selenium
				r = open_selenium_wait(url)
	except:
		# If error occurs, open the page normally
		r = open_webpage(url)
		if isinstance(r, int): return r
		
	chk = check_page(url)
	
	if not chk: return None

	# Get the soup of the XML page
	try:
		soup = BeautifulSoup(r, 'xml')
	except TypeError, e:
		err_dict = collections.OrderedDict()
		err_dict['err'] = 'Page could not be loaded.'
		return err_dict

	if len(str(soup).splitlines()) < 3:
		# If the XML file has less than 3 lines, parse it using 'html.parser'
		soup = BeautifulSoup(r, 'html.parser')

	return soup

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
				heading = get_text(a)
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
			#         entries = [get_text(v) for v in valid_cols]
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
		print "\nError in open_webpage: %s" % str(e)
		print "%s\n" % url
		err_dict = collections.OrderedDict()
		err_dict['err'] = str(e)
		return err_dict

	return url_html

def parse_dl(dl, parsed_dl=None):
	''' Parses a <dl> list
	:param dl: The <dl> soup contents.
	:param parsed_dl: The parsed DL contents.
	:return: The parsed DL contents.
	'''

	# Get the title
	dt = dl.find('dt')
	title = dt.em.text

	# Keep parsing if necessary
	dd = dl.find('dd')
	sub_dl = dd.find('dl')
	if sub_dl is not None:
		parsed_dl[title] = parse_dl(sub_dl, parsed_dl)

	return parsed_dl

def parse_query_url(url):
	''' Retrieves the base URL of a query string.
	:param url: The URL query string.
	:return: The base URL.
	'''

	end_pos = url.find('?')
	parse_url = url[:end_pos].split("/")

	return parse_url
	
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

def sort_fields(in_flds):
	''' Sorts a list of header fields in a specified order.
	:param in_flds: A list of headers for fields
	:return: A list of the sorted headers.
	'''

	fields = ['Title', 'Service Name', 'Type', 'Description', 'Publisher',
			  'Available Formats', 'Licensing', 'Access', 'Spatial Reference',
			  'Service', 'Date', 'Metadata ISO', 'Metadata URL', 'Web Map URL',
			  'Web Page URL', 'Web Service URL', 'Download', 'Download URL', 'Notes']
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

def walk_dl(dl, results=collections.OrderedDict(), level=0):
	''' Walks through a <dl> list.
	:param dl: A soup <dl> element.
	:param results: The results of the previous recursive method.
	:param level: The current level in the list.
	:return:
	'''

	for child in dl.children:
		#print "Child type: " + str(type(child))
		if isinstance(child, Tag):
			#print "Child Tag Name: " + str(child.name)
			if child.name == 'dd':
				#answer = raw_input("DD found!!!")
				level += 1
				results = walk_dl(child, results, level)
			elif child.name == 'dl':
				#answer = raw_input("DL found!!!")
				results = walk_dl(child, results, level)
			else:
				desc = child.find_next_sibling('dd')

	return results

# NO LONGER USED:
# def get_request_with_cookies(url, asp_url, form_data, headers=None, json=False):
#     '''
#     :param url:
#     :param asp_url:
#     :param form_data:
#     :param headers:
#     :param json:
#     :return:
#     '''
#
#     # Build a URL to display
#     asp_full = urlparse.urljoin(url, asp_url)
#     asp_query = get_post_query(asp_full, form_data)
#     print "\nOpening:"
#     print "'%s'..." % asp_query
#
#     try:
#         options = Options()
#         options.add_argument("--headless")
#         driver = webdriver.Firefox(firefox_options=options)
#         driver.get(url)
#
#         # Store the cookies
#         request_cookies_browser = driver.get_cookies()
#
#         # pprint.pprint(request_cookies_browser)
#
#         # answer = raw_input("Press enter...")
#
#         # Create the requests session
#         params = {'os_username': 'username', 'os_password': 'password'}
#         s = requests.Session()
#
#         # passing the cookies generated from the browser to the session
#         c = [s.cookies.set(c['name'], c['value']) for c in request_cookies_browser]
#
#         if json:
#             resp = s.post(asp_full, headers=headers, json=form_data)  # I get a 200 status_code
#         else:
#             resp = s.post(asp_full, headers=headers, data=form_data)  # I get a 200 status_code
#
#         # passing the cookie of the response to the browser
#         dict_resp_cookies = resp.cookies.get_dict()
#         response_cookies_browser = [{'name': name, 'value': value} for name, value in dict_resp_cookies.items()]
#         c = [driver.add_cookie(c) for c in response_cookies_browser]
#
#         # the browser now contains the cookies generated from the authentication
#         driver.get(asp_full)
#
#         # rec_html = driver.page_source
#
#         driver.quit()
#
#         # print "Response URL: " + str(resp.request.url)
#
#         # print(resp.request.body)
#         # print(resp.request.headers)
#
#         return (resp.text, asp_query)
#
#     except:
#         print "Exception in user code:"
#         traceback.print_exc(file=sys.stdout)
#         if 'driver' in locals(): driver.quit()

# NO LONGER USED:
# def build_sql_statement(table_name, condition=None, html=True):
#     sql_statement = "SELECT * FROM %s" % table_name
#
#     if condition is not None and not condition == "":
#         sql_statement += " WHERE %s" % condition
#
#     if html:
#         sql_statement = sql_statement.replace(" ", "%20")
#
#     return sql_statement

# NO LONGER USED:
# def get_by_attribute(soup_list, attribute, get_val):
#     var_soup = None
#     for soup in soup_list:
#         if soup.has_attr(attribute):
#             var_soup = soup[get_val]
#
#     return var_soup

# def find_tags_containing(soup, contains, tag_name=None):
#     ''' Locates all tags with text in contains list.
#     :param soup: The soup to search in.
#     :param contains: A list of strings to locate in the soup object.
#     :return: A list of tags containing the text from list contains.
#     '''
#
#     found_tags = []
#     for txt in contains:
#         #print "txt: " + str(txt)
#         tag = get_tag_containing(soup, txt, tag_name)
#         #print "tag: " + str(tag)
#         found_tags.append(tag)
#
#     #answer = raw_input("Press enter...")
#
#     return found_tags

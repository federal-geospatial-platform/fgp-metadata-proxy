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
import xmltodict
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

import shared
		
def clean_soup(soup):
	''' Prettifies a soup object.
	:param soup: The unformatted soup object.
	:return: The prettified soup.
	'''

	clean_html = soup.prettify()
	clean_soup = BeautifulSoup(clean_html, 'html.parser')

	return clean_soup
	
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
				if shared.clean_text(el_text[0]) == text:
					results.append(tag)

		return results
	else:
		# Get all elements with the tag_name
		tag_list = soup.find_all(tag_name)

		for tag in tag_list:
			# Get the element's text and clean it
			tag_text = tag.text
			tag_clean = shared.clean_text(tag_text)
			# If both the element text and input text are equal
			if tag_clean == text:
				#print type(tag)
				#print tag
				return tag
				
def find_tag(soup, tag_name, attrs={}):
	''' Finds an element with tag_name, ignoring cases.
	'''
	
	res = soup.find(tag_name, attrs)
	
	#print "res: %s" % res
	
	if res is None:
		# Check lowercase
		res = soup.find(tag_name.lower(), attrs)
		
		#print "res: %s" % res
		
		if res is None:
			# Check uppercase
			res = soup.find(tag_name.upper(), attrs)
			
			#print "res: %s" % res
			
			if res is None:
				return None
	
	return res
				
def find_tags_by_id(soup, contains, tag_name=None):
	''' Find tags with id containing the input string.
	:param soup: The soup to search in.
	:param contains: An id string used to located the tag.
	:param tag_name: The tag to locate. Default is to search all tags in soup.
	'''
	
	out_tags = []
	
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
					out_tags.append(element)
				
	else:
		# Get a list of all elements with the given tag name
		tag_list = soup.find_all(tag_name)

		# Go through each tag and compare its text to the current string in contains list
		for tag in tag_list:
			#print "tag: %s" % tag
			tag_id = tag.get('id')
			if tag_id is None: continue
			if tag_id.find(contains) > -1:
				out_tags.append(tag)
				
	return out_tags
	

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
					tag_text = shared.clean_text(el_text[0])
					tag_text = tag_text.replace("  ", " ")
					if tag_text.lower().find(txt.lower()) > -1:
						final_tags.append(tag)
		else:
			# Get a list of all elements with the given tag name
			tag_list = soup.find_all(tag_name)

			# Go through each tag and compare its text to the current string in contains list
			for tag in tag_list:
				tag_text = tag.text
				tag_clean = shared.clean_text(tag_text)
				if tag_clean.lower().find(txt.lower()) > -1:
					final_tags.append(tag)

	if output == 'list':
		return final_tags
	else:
		if len(final_tags) > 0:
			return final_tags[0]

def find_xml_tags(xml_soup, tag_names, attrs=[], find_all=False):
	''' Searches for a tag in an XML soup, ignoring cases.
	:param xml_soup: The XML soup.
	:param txt: The text used to find the tag.
	:return: The tag containing the text (or None is no tag is found).
	'''
	
	if not isinstance(tag_names, list):
		tag_names = [tag_names]
	
	results = []
	# Go through each tag in tag_names
	for tag in tag_names:
		if len(attrs) == 0:
			#print 'xml_soup.find(%s)' % tag
			#print 'xml_soup.find(%s)' % tag.lower()
			res = xml_soup.find_all(tag)
			if len(res) == 0:
				res = xml_soup.find_all(tag.lower())
			if len(res) > 0:
				if not find_all: res = res[0]
				results.append(res)
		else:
			for a in attrs:
				res = xml_soup.find_all(tag, attrs=a)
				if len(res) == 0:
					res = xml_soup.find_all(tag.lower(), attrs=a)
				if len(res) > 0:
					if not find_all: res = res[0]
					results.append(res)

	return results
	
def find_xml_text(xml_soup, tag_name, attrs=None):
	''' Gets the text of a specified XML tag
	'''
	
	tags = [tag_name]
	if attrs is None:
		attrs = []
	else:
		attrs = [attrs]
		
	results = find_xml_tags(xml_soup, tags, attrs)
	
	if len(results) == 0: return ''
	
	res = results[0]
	res_text = get_text(res)
	
	return res_text
	
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
		print "\nWARNING: Cannot find '%s' element next to label '%s'." \
				% (tag, label)
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
		print "\nWARNING: Cannot find '%s' element next to label '%s'." \
				% (tag, label)
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
					text_str = shared.clean_text(txt)

					return text_str
		else:
			# If the soup is already a string, return it
			return soup
			
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
		download_url = shared.get_anchor_url(a, in_url)
		# Get the format from the URL
		if download_url.find('.zip') > -1:
			bname, f_ext = os.path.basename(download_url).split('.')
			bname_split = bname.split('_')
			formats = [bname_split[len(bname_split) - 1]]
		else:
			bsname, f_ext = os.path.basename(download_url).split('.')
			formats = f_ext

		download_info = shared.get_download_text(formats, download_url)
		download_str, access_str = download_info.split('|')

		rec_dict['Title'] = title_str
		rec_dict['Download'] = download_str
		rec_dict['Access'] = access_str
		rec_dict['Available Formats'] = "|".join([f.upper() for f in formats])

		datasets.append(rec_dict)

	return datasets
	
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
			html_text = shared.open_selenium_wait(url, delay, silent=silent, 
							browser=browser)
		else:
			html_text = shared.open_selenium_page(url, attrb, delay, 
							silent=silent, browser=browser)
	else:
		html_text = shared.open_webpage(url)
		#print "html_text: %s" % html_text
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
	try:
		soup = BeautifulSoup(html_text, 'html.parser')
	except:
		return None

	return soup
	
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
				text_str = shared.clean_text(s)
			elif isinstance(s, str) or isinstance(s, unicode):
				if s.find("<") > -1:
					out_soup = BeautifulSoup(s, 'html.parser')
					text = out_soup.get_text()
					text_str = shared.clean_text(text)
				else:
					text_str = s
			else:
				text = s.get_text()
				text_str = shared.clean_text(text)

			text_list.append(text_str)

	final_text = ' '.join(text_list)

	return final_text
	
def get_xml(url, silent=True, selenium=False):
	''' Gets the XML from the URL
	'''
	
	if not silent:
		print "Getting XML soup for %s" % url

	try:
		if selenium:
			# If Selenium is specified, use it to open the XML page
			resp_text = shared.open_selenium_wait(url, delay=1, silent=silent)
		else:
			# Open the XML page
			#resp = requests.get(url)
			resp = urllib2.urlopen(url)
			resp_text = resp.read()
			if len(resp_text.splitlines()) < 3:
				# If the XML page contains less than 3 lines, open the page using Selenium
				resp_text = shared.open_selenium_wait(url, delay=1, \
														silent=silent)
	except Exception, e:
		# If error occurs, open the page normally
		if not silent:
			print
			print e
		resp_text = shared.open_webpage(url)
		if isinstance(resp_text, int): return resp_text
		
	#print shared.__file__
	#for mth in dir(shared):
	#	print mth
		
	chk = shared.check_page(url)
	
	if not chk: return None
	
	return resp_text

def get_xml_soup(url, silent=True, selenium=False):
	''' Gets the XML BeautifulSoup object of the URL page.
	:param url: The URL of the page containing XML data.
	:param silent: If true, statements will not be printed to the output.
	:param selenium: Determines whether to use Selenium when opening the page.
	:return: A BeautifulSoup object of the page.
	'''
	
	resp_text = get_xml(url, silent, selenium)

	# Get the soup of the XML page
	try:
		soup = BeautifulSoup(resp_text, 'xml')
	except TypeError, e:
		err_dict = collections.OrderedDict()
		err_dict['err'] = 'Page could not be loaded.'
		return err_dict

	if len(str(soup).splitlines()) < 3:
		# If the XML file has less than 3 lines, parse it using 'html.parser'
		soup = BeautifulSoup(resp_text, 'html.parser')

	return soup
	
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
	
def xml_to_dict(xml_url, selenium=False, silent=True):
	''' Convert an XML page to JSON format
	'''
	
	xml_text = get_xml(xml_url, silent, selenium)
	
	#print "\nxml_text: %s" % xml_text
	
	if isinstance(xml_text, dict) or xml_text == '':
		return xml_text
		
	xml_dict = collections.OrderedDict()
	try:
		xml_dict = xmltodict.parse(xml_text)
	except Exception, e:
		if not silent:
			print
			print e
			print "xml_text: '%s'" % xml_text
			print "xml_url: %s" % xml_url
		return None
		#answer = raw_input("Press enter...")
	
	# FOR DEBUG
	#json_text = json.dumps(xmltodict.parse(xml_text), indent=4)
	#json_out = open('json_text.txt', 'w')
	#json_out.write(json_text)
	#json_out.close()
	
	return xml_dict
	
	
	
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
					text_str = clean_text(txt)

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
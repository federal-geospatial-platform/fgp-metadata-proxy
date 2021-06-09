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
import time
import codecs
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

# Get the shared.py
script_file = os.path.abspath(__file__)
script_folder = os.path.dirname(script_file)
province_folder = os.path.dirname(script_folder)
home_folder = os.path.dirname(province_folder)
script_folder = home_folder + "\\scripts"

sys.path.append(script_folder)
import shared
import access_rest as rest

province = 'Saskatchewan'
work_folder = 'H:\\GIS_Data\\Work\\NRCan\\FGP\\TA001\\_%s' % province

site_list = collections.OrderedDict([
				('regina', ('extract_regina()', 'http://open.regina.ca/')), 
				('saskatoon', ('extract_saskatoon()', 'http://opendata-saskatoon.cloudapp.net/DataBrowser/SaskatoonOpenDataCatalogueBeta'))])

def extract_regina():
	############################################################################
	# Extract from the Open Data site for Regina

	regina_url = site_list['regina'][1]
	
	# Get soup
	regina_soup = shared.soup_it_up(regina_url)
	categories = regina_soup.find_all('section', attrs={'class': 'tile-section'})
	
	# Create the CSV
	csv_fn = "Regina_results"
	field_names = ['Title', 'Description', 'Available Formats', 'Date', 'URL']
	my_csv = shared.MyCSV(csv_fn, regina_url, province, field_names)
	my_csv.open_csv()
	
	map_formats = ['xml', 'shp', 'kml', 'json', 'rest']
	
	records = []
	
	print "Number of categories: " + str(len(categories))
	
	for cat in categories:
		# Get the URL for the category
		link = shared.get_link(cat)
		sub_url = urlparse.urljoin(regina_url, link)
		
		h3 = cat.find('h3', attrs={'class': 'tile-label'})
		print "Category: " + str(h3.text)
		
		# Filter the formats
		for format in map_formats:
			# Build the query
			query_params = collections.OrderedDict()
			query_params['res_format'] = format.upper()
			final_url = shared.build_query_html(sub_url, query_params)
			
			# Load the sub result
			sub_soup = shared.soup_it_up(final_url)
			
			# Find out the page count
			page_count = shared.get_page_count(sub_soup, 'pagination', 'li')
			
			#print "Page Count: " + str(page_count)
			
			for page in range(0, page_count):
				# Load the current page
				if page > 0:
					page_url = "%s?page=%s" % (final_url, page + 1)
					sub_soup = shared.soup_it_up(page_url)
				
				# Open the link
				results = sub_soup.find_all('h3', attrs={'class': 'dataset-heading'})
				for res in results:
					rec_dict = collections.OrderedDict((k, "") for k in field_names)
				
					res_link = shared.get_link(res)
					res_url = urlparse.urljoin(final_url, res_link)
					
					res_soup = shared.soup_it_up(res_url)
					
					# Get the title
					div = res_soup.find('div', attrs={'class': 'module-content'})
					h1 = div.find('h1')
					title = shared.get_text(h1)
					
					# Get the description
					notes_div = div.find('div', attrs={'class': 'notes'})
					desc = shared.get_text(notes_div)
					
					# Get the available formats
					spans = div.find_all('span', attrs={'class': 'format-label'})
					#print spans
					formats = []
					for span in spans:
						format = span['data-format']
						if format == 'data':
							format = "REST"
						else:
							format = format.upper()
						formats.append(format)
					#print formats
					formats_str = '|'.join(formats)
					
					# Get the date
					date = shared.get_text_by_label(res_soup, 'th', "Last Updated")
					
					# Get the data url
					dataset_url = shared.get_text_by_label(res_soup, 'th', "Source")
					
					# ['Title', 'Description', 'Available Formats', 'Date', 'URL']
					rec_dict['Title'] = title
					rec_dict['Available Formats'] = formats_str
					rec_dict['Description'] = shared.edit_description(desc)
					rec_dict['Date'] = date
					rec_dict['URL'] = dataset_url
					
					if not rec_dict in records:
						records.append(rec_dict)
						my_csv.write_dataset(rec_dict)
						
	############################################################################
	# Extract from Regina Mapservers
	
	rest_url = "https://opengis.regina.ca/arcgis/rest/services"
	
	# csv_fn = "Regina_REST_results"
	# field_names = ['Title', 'Type', 'Description', 'URL']
	# my_csv = shared.MyCSV(csv_fn, root_url, province, header=field_names)
	# my_csv.open_csv()
	
	my_rest = rest.MyREST(rest_url)
	services = my_rest.get_services()
	
	for service in services:
		rec_dict = collections.OrderedDict((k, "") for k in field_names)
	
		rec_dict['Title'] = service['name']
		#rec_dict['Type'] = service['type']
		if 'serviceDescription' in service:
			rec_dict['Description'] = shared.edit_description(service['serviceDescription'], 'span')
		rec_dict['URL'] = service['url']
		
		my_csv.write_dataset(rec_dict)
		
	my_csv.remove_duplicates('URL')
	
	#answer = raw_input("Press enter...")
		
	my_csv.close_csv()
				
def extract_saskatoon():
	######################################################################################
	# Extract from Saskatoon's Open Catalogue

	saskatoon_url = site_list['saskatoon'][1]
	query_url = "http://opendata-saskatoon.cloudapp.net:8080/v1/SaskatoonOpenDataCatalogueBeta"

	csv_fn = "Saskatoon_2_results"
	field_names = ['Title', 'Description', 'Available Formats', 'Date', 'Metadata URL', 'Reference URL', 'URL']
	my_csv = shared.MyCSV(csv_fn, saskatoon_url, province, field_names)
	my_csv.open_csv()
	
	xml_soup = shared.get_xml_soup(query_url)
	
	colls = xml_soup.find_all('collection')
	
	# FOR DEBUGGING
	get_catalogue = False
	
	#print collections
	if get_catalogue:
		for coll in colls:
			rec_dict = collections.OrderedDict((k, "") for k in field_names)
		
			# Build query URL
			base_url = "%s/%s" % (saskatoon_url, coll['href'])
			#print base_url
			
			# Get the Soup
			coll_soup = shared.soup_it_up(base_url)
			
			#print coll_soup
			
			title = shared.get_text_by_label(coll_soup, 'td', "Dataset name")
			description = shared.get_text_by_label(coll_soup, 'td', "Description")
			date = shared.get_text_by_label(coll_soup, 'td', "Last Updated Date")
			ref_url = shared.get_text_by_label(coll_soup, 'td', "Links and references")
			mdata_url = shared.get_text_by_label(coll_soup, 'td', "Metadata Url")
			
			# Get the available formats
			form_soup = coll_soup.find('select', attrs={'id': 'eidDownloadType'})
			opts = form_soup.find_all('option')
			formats = []
			for opt in opts:
				formats.append(opt.string)
				
			formats_str = '|'.join(formats)
			
			# Wednesday, April 04, 2018
			date_obj = time.strptime(date, "%A, %B %d, %Y")
			form_date = time.strftime("%Y-%m-%d", date_obj)
			
			#print title
			#print form_date
			
			# ['Title', 'Description', 'Available Formats' 'Date', 'Metadata URL', 'Reference URL', 'URL']
			rec_dict['Title'] = title
			rec_dict['Description'] = shared.edit_description(description)
			rec_dict['Date'] = form_date
			rec_dict['URL'] = base_url
			rec_dict['Reference URL'] = ref_url
			rec_dict['Metadata URL'] = mdata_url
			rec_dict['Available Formats'] = formats_str
			
			my_csv.write_dataset(rec_dict)
		
	######################################################################################
	# Extract from Saskatoon's Address Map
	if get_catalogue:
		map_url = "https://www.arcgis.com/apps/View/index.html?appid=2199c6ba701148d58c24fcb82d4e7d8e"
		#service_url = "https://www.arcgis.com/sharing/rest/content/items/2199c6ba701148d58c24fcb82d4e7d8e"
		
		my_csv.write_line("\nSaskatoon's Address Map")
		my_csv.write_url(map_url, "Map URL")
		#my_csv.write_url(service_url, "Service URL")
		field_names = ['Title', 'Type', 'Date', 'Data URL']
		my_csv.write_header(field_names)
		
		net_traffic = shared.get_network_traffic(map_url, ('class', 'esriAttribution'))
		
		#d_f = open("json_test.txt", "w")
		#d_f.write(net_traffic)
		#d_f.close()
		
		#print net_traffic[0]
		
		log = net_traffic['log']
		entries = log['entries']
		
		json_urls = []
		
		for entry in entries:
			add_item = True
			request_url = entry['request']['url']
			if request_url.find("json") > -1 and request_url.find("items") > -1:
				# Check for a duplicate already in json_urls
				if len(json_urls) == 0:
					json_urls.append(request_url)
				for url in json_urls:
					parse_url = shared.parse_query_url(url)
					parse_request = shared.parse_query_url(request_url)
					
					if parse_url[:8] == parse_request[:8]:
						#print parse_url[:8]
						#print parse_request[:8]
						add_item = False
			
				if add_item:
					json_urls.append(request_url)
				
		print "Number of JSON requests: " + str(len(json_urls))
		
		#for request in json_urls:
		#	print request['request']['url']
		
		#soup = shared.soup_it_up(map_url)
		
		for url in json_urls:
			#json_url = url['request']['url']
			
			json_text = shared.get_json(url)
			
			rec_dict = collections.OrderedDict((k, "") for k in field_names)
			
			if 'title' in json_text: rec_dict['Title'] = json_text['title']
			if 'type' in json_text: rec_dict['Type'] = json_text['type']
			#if 'description' in json_text: rec_dict['Description'] = json_text['description']
			if 'modified' in json_text: rec_dict['Date'] = shared.translate_date(json_text['modified'])
			
			rec_dict['Data URL'] = url
			
			my_csv.write_dataset(rec_dict)
		
	######################################################################################
	# Extract from Saskatoon Zoning Address Map
	if get_catalogue:
		map_url = "https://www.arcgis.com/apps/View/index.html?appid=2ca06c6cfdef47bbbb9876a02fa1dffe"
		#service_url = "https://www.arcgis.com/sharing/rest/content/items/2ca06c6cfdef47bbbb9876a02fa1dffe"
		
		my_csv.write_line("\nSaskatoon Zoning Address Map")
		my_csv.write_url(map_url, "Map URL")
		#my_csv.write_url(service_url, "Service URL")
		field_names = ['Title', 'Type', 'Date', 'Data URL']
		my_csv.write_header(field_names)
		
		net_traffic = shared.get_network_traffic(map_url, ('class', 'esriAttribution'))
		
		#d_f = open("json_test.txt", "w")
		#d_f.write(net_traffic)
		#d_f.close()
		
		#print net_traffic[0]
		
		log = net_traffic['log']
		entries = log['entries']
		
		json_urls = []
		
		for entry in entries:
			add_item = True
			request_url = entry['request']['url']
			if request_url.find("json") > -1 and request_url.find("items") > -1:
				# Check for a duplicate already in json_urls
				if len(json_urls) == 0:
					json_urls.append(request_url)
				for url in json_urls:
					parse_url = shared.parse_query_url(url)
					parse_request = shared.parse_query_url(request_url)
					
					if parse_url[:8] == parse_request[:8]:
						#print parse_url[:8]
						#print parse_request[:8]
						add_item = False
			
				if add_item:
					json_urls.append(request_url)
				
		print "Number of JSON requests: " + str(len(json_urls))
		
		for url in json_urls:
			#json_url = url['request']['url']
			
			json_text = shared.get_json(url)
			
			rec_dict = collections.OrderedDict((k, "") for k in field_names)
			
			if 'title' in json_text: rec_dict['Title'] = json_text['title']
			if 'type' in json_text: rec_dict['Type'] = json_text['type']
			#if 'description' in json_text: rec_dict['Description'] = json_text['description']
			if 'modified' in json_text: rec_dict['Date'] = shared.translate_date(json_text['modified'])
			
			rec_dict['Data URL'] = url
			
			my_csv.write_dataset(rec_dict)
		
	######################################################################################
	# Extract from Saskatoon Snow Grading Map
	map_url = "http://apps2.saskatoon.ca/app/aSnowProgram/"
	rest_url = "http://rpbackgis2.saskatoon.ca/ArcGIS/rest/services"
	
	my_csv.write_line("\nSaskatoon Snow Grading Map")
	my_csv.write_url(map_url, "Map URL")
	my_csv.write_url(rest_url, "ArcGIS REST URL")
	field_names = ['Title', 'Type', 'Description', 'URL']
	my_csv.write_header(field_names)
	
	my_rest = rest.MyREST(rest_url)
	services = my_rest.get_services()
	
	for service in services:
		rec_dict = collections.OrderedDict((k, "") for k in field_names)
	
		rec_dict['Title'] = service['name']
		rec_dict['Type'] = service['type']
		rec_dict['Description'] = shared.edit_description(service['serviceDescription'], 'span')
		rec_dict['URL'] = service['url']
		
		my_csv.write_dataset(rec_dict)
		
	my_csv.close_csv()
	
def main():
	#city_list = ['Winnipeg', 'Brandon']

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--city", help="The city to extract: %s" % ', '.join(site_list.keys()))
	parser.add_argument("-w", "--word", help="The key word(s) to search for.")
	#parser.add_argument("-f", "--format", help="The format(s) to search for.")
	parser.add_argument("-a", "--category", help="The category to search for.")
	#parser.add_argument("-d", "--downloadable", help="Determines wheter to get only downloadable datasets.")
	#parser.add_argument("-l", "--html", help="The HTML file to scrape (only for OpenData website).")
	parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
	args = parser.parse_args()
	#print args.echo
	
	#print "province: " + str(args.province)
	#print "format: " + str(args.format)

	city = args.city
	word = args.word
	#formats = args.format
	#html = args.html
	silent = args.silent
	cat = args.category
	#downloadable = args.downloadable
	
	if city is None:
		answer = raw_input("Please enter the city you would like to extract (%s): " % ', '.join(site_list.keys()))
		if not answer == "":
			city = answer.lower()
		else:
			print "\nERROR: Please specify a city."
			print "Exiting process."
			sys.exit(1)
			
	if word is None and not silent:
		answer = raw_input("Please enter the word you would like to search: ")
		if not answer == "":
			word = answer.lower()
			
	if cat is None and not silent:
		answer = raw_input("Please enter the category you would like to search: ")
		if not answer == "":
			cat = answer.lower()
	
	if city == "all":
		for key, site in site_list.items():
			eval(site_list[key][0])
	else:
		if city in site_list.keys():
			eval(site_list[city][0])
		else:
			print "\nERROR: Invalid city '%s'. Please enter one of the following: %s" % (city, ', '.join(site_list.keys()))
			print "Exiting process."
			sys.exit(1)
	
	#geoportal_list = extract_geoportal(province)

if __name__ == '__main__':
	sys.exit(main())
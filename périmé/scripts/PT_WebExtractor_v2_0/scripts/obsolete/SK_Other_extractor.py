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
				('ducks', ('extract_ducks()', 'http://maps.ducks.ca/arcgis/rest/services')), 
				('commview', ('extract_commview()', 'http://www.communityview.ca/Catalogue'))])

def extract_commview():
	commview_url = site_list['commview'][1]
	
	soup = shared.soup_it_up(commview_url)
	
	# Create CSV file
	csv_fn = "CommunityView_results"
	field_names = ['Title', 'Available Formats', 'Map URL', 'Data URL']
	my_csv = shared.MyCSV(csv_fn, commview_url, province, field_names)
	my_csv.open_csv()
	
	# Get a list of all the anchors in the treeview at the side of the page
	ul = soup.find('ul', attrs={'class': 'treeview'})
	anchors = ul.find_all('a', attrs={'class': 'TreeRootStandard'})
	
	for anchor in anchors:
		browse_url = urlparse.urljoin(commview_url, anchor['href'])
		#print browse_url
		
		# Load the sub result
		sub_soup = shared.soup_it_up(browse_url)
		
		# Determine the number of pages in the search
		page_count = shared.get_page_count(sub_soup, 'pager', 'a')
		
		for page in range(0, page_count):
		
			# Load the current page
			if page > 0:
				page_url = "%s?page=%s" % (browse_url, page + 1)
				sub_soup = shared.soup_it_up(page_url)
		
			# Get the resource list
			resources_div = sub_soup.find('div', attrs={'class': 'ResourceList'})
			resources = sub_soup.find_all('table', attrs={'class': 'ResourceTable'})
			
			for res in resources:
				map_res = res.find('img', attrs={'alt': 'Map'})
				
				# Get the ID of the resource
				parent = res.parent
				id = parent['id'].replace("ResourceTable", "")
				
				# Get the name of the resource
				name = res.find('a', attrs={'class': "ResourceTitle"}).text
				
				if map_res is not None:
					# If the resource contains a map link, it will be included in the inventory
					rec_dict = collections.OrderedDict((k, "") for k in field_names)
					
					# Get the URLs for the data
					map_url = urlparse.urljoin(commview_url, map_res.parent['href'])
					data_url = map_url.replace("Map", "Data")
					
					#['Title', 'Available Formats', 'Map URL', 'Data URL']
					rec_dict['Title'] = name
					rec_dict['Available Formats'] = "XLS"
					rec_dict['Map URL'] = map_url
					rec_dict['Data URL'] = data_url
					
					my_csv.write_dataset(rec_dict)
				
	my_csv.close_csv()
				
def extract_ducks():
	ducks_url = site_list['ducks'][1]
	
	my_rest = rest.MyREST(ducks_url)
	services = my_rest.get_services()
	
	# Create CSV file
	csv_fn = "Ducks_results"
	field_names = ['Title', 'Type', 'Description', 'URL']
	my_csv = shared.MyCSV(csv_fn, ducks_url, province, field_names)
	my_csv.open_csv()
	
	for service in services:
		if service['name'].find("SK") > -1:
			rec_dict = collections.OrderedDict((k, "") for k in field_names)
			
			#print service
		
			rec_dict['Title'] = service['name']
			rec_dict['Type'] = service['type']
			rec_dict['Description'] = shared.edit_description(service['serviceDescription'])
			rec_dict['URL'] = service['url']
			
			my_csv.write_dataset(rec_dict)
			
	my_csv.close_csv()
	
def main():
	#city_list = ['Winnipeg', 'Brandon']

	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--tool", help="The tool to use: %s or all" % ', '.join(site_list.keys()))
	#parser.add_argument("-w", "--word", help="The key word(s) to search for.")
	#parser.add_argument("-f", "--format", help="The format(s) to search for.")
	#parser.add_argument("-a", "--category", help="The category to search for.")
	#parser.add_argument("-d", "--downloadable", help="Determines wheter to get only downloadable datasets.")
	#parser.add_argument("-l", "--html", help="The HTML file to scrape (only for OpenData website).")
	parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
	args = parser.parse_args()
	#print args.echo
	
	#print "province: " + str(args.province)
	#print "format: " + str(args.format)

	tool = args.tool
	#word = args.word
	#formats = args.format
	#html = args.html
	silent = args.silent
	#cat = args.category
	#downloadable = args.downloadable
	
	if tool is None:
		answer = raw_input("Please enter the site you would like to extract (%s): " % ', '.join(site_list.keys()))
		if not answer == "":
			tool = answer.lower()
		else:
			print "\nERROR: Please specify a site."
			print "Exiting process."
			sys.exit(1)
			
	# if word is None and not silent:
		# answer = raw_input("Please enter the word you would like to search: ")
		# if not answer == "":
			# word = answer.lower()
			
	# if cat is None and not silent:
		# answer = raw_input("Please enter the category you would like to search: ")
		# if not answer == "":
			# cat = answer.lower()
	
	if tool == "all":
		for key, site in site_list.items():
			eval(site_list[key][0])
	else:
		if tool in site_list.keys():
			eval(site_list[tool][0])
		else:
			print "\nERROR: Invalid tool '%s'. Please enter one of the following: %s" % (tool, ', '.join(site_list.keys()))
			print "Exiting process."
			sys.exit(1)
	
	#geoportal_list = extract_geoportal(province)

if __name__ == '__main__':
	sys.exit(main())
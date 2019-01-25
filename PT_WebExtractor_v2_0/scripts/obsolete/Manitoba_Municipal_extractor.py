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
import page
import recurse_ftp as rec_ftp

class Extractor:
    def __init__(self):
        ''' Initializer for the Extractor class. '''

        # Set up the initial parameters
        self.province = 'Manitoba'
        self.work_folder = 'H:\\GIS_Data\\Work\\NRCan\\FGP\\TA001\\_%s' % self.province
        self.pages = []
        self.pages = collections.OrderedDict()

        # Declare all the different types of pages
        pg = page.Page('brandon', "City of Brandon GIS Webpages")
        pg.add_page('opendata_url', 'http://opengov.brandon.ca/OpenDataService/opendata.html')
        pg.add_page('rest_url', 'https://gisapp.brandon.ca/arcgis/rest/services')
        pg.add_page('bgis_url', 'http://gis.brandon.ca/')
        self.pages['brandon'] = pg

        pg = page.Page('winnipeg', "City of Winnipeg GIS Webpages")
        pg.add_page('search_url', 'https://data.winnipeg.ca/browse')
        pg.add_page('propertymap_url', 'http://winnipeg.ca/ppd/maps_aerial.stm')
        pg.add_page('servstat_url', 'http://winnipeg.ca/Interhom/serviceStat/')
        self.pages['winnipeg'] = pg

        # Open the log file
        self.log_fn = 'Extraction_Log.txt'
        self.log_f = open(self.log_fn, 'w')

    def get_param(self, param):
        page = self.pages[self.page]
        param_val = page.get_param(param)
        return param_val

    def get_pagelist(self):
        ''' Gets a list of available page types (ex: cigg, maps, etc.).
        :return: A list of page types.
        '''
        return self.pages

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

    def set_page(self, page):
        ''' Sets the ID for the Extractor based on the given page type.
        :param page: The page type to set the ID.
        :return: None
        '''
        self.id = page

    def set_params(self, params):
        ''' Sets the parameters for the extract_opendata method
        :param params: A dictionary of parameters (keys are the method's argument names)
        :return: None
        '''
        self.method_params = params

    def print_log(self, txt):
        ''' Writes a text to the log file.
        :param txt: The string which will be written to the log file.
        :return: None
        '''
        # type: (object) -> object
        print txt
        self.log_f.write(txt + "\n")

    def close_log(self):
        ''' Closes the log file.'''
        self.log_f.close()

    def print_dict(self, in_dict):
        # dict_list = ["%s: '%s'" % (k, v) for k, v in in_dict.items()]
        dict_list = []
        for k, v in in_dict.items():
            try:
                dict_list.append("%s: '%s'" % (k, v))
                print '\t\t'.join(dict_list)
            except Exception as e:
                continue

    def process_googleapi(self, layers, lyr_type):

        records = []

        for layer in layers:
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

            title_str = shared.get_text(layer)

            # Build query URL
            # Ex: https://mapapi.winnipeg.ca/mapapi/wfs.ashx?output=json&maptypeid=2&coordinates=&g=n&featurelist=13937
            mapapi_url = "https://mapapi.winnipeg.ca/mapapi/wfs.ashx"
            srch_params = collections.OrderedDict()
            srch_params['output'] = "json"
            srch_params['maptypeid'] = "2"
            srch_params['coordinates'] = ""
            srch_params['g'] = "n"
            srch_params['featurelist'] = id

            query_url = shared.build_query_html(mapapi_url, srch_params)

            # Get soup
            json_res = shared.get_json(query_url)

            features = json_res['features']

            serv_type = features[0]['serviceType']
            if serv_type == "both": serv_type = "WMS|WFS"

            rec_dict['Title'] = title_str
            rec_dict['Type'] = serv_type.upper()
            rec_dict['Description'] = shared.edit_description(features[0]['DESCRIPTION'])
            rec_dict['Data URL'] = query_url

            records.append(rec_dict)

        return records

    def extract_brandon(self, subpage='all'):

        print "subpage: %s" % subpage

        if subpage == 'opendata' or subpage == 'all':
            #############################################################################
            # Extract from Brandon OpenData

            opendata_url = self.page.get_url('opendata_url')

            # Get soup
            soup = shared.soup_it_up(opendata_url)

            table = soup.find('table', attrs={'id': 'datasetTable'})
            rows = table.find_all('tr')

            # Create CSV file
            csv_fn = "Brandon-OpenData_results"
            my_csv = shared.MyCSV(csv_fn, self.province)
            my_csv.open_csv()

            for row in rows:
                anchor = row.find('a')

                if anchor is not None:
                    # Get the parent row
                    tr = anchor.parent.parent
                    tds = tr.find_all('td')

                    # Get the title from the first column and the format from the second column
                    title_str = shared.get_text(tds[0])
                    ds_type = shared.get_text(tds[1])

                    # Determine if the dataset is a shapefile
                    if ds_type == 'Shapefile':
                        # Get the download URL and format
                        download_url = shared.get_anchor_url(anchor, opendata_url)
                        formats = ['SHP']

                        # Get the access and download text
                        download_str, access_str = shared.get_download_text(formats, download_url)

                        my_csv.add('Title', title_str)
                        my_csv.add('Type', ds_type)
                        my_csv.add('Web Page URL', opendata_url)
                        my_csv.add('Download', download_str)
                        my_csv.add('Access', access_str)
                        my_csv.add('Available Formats', formats[0])

                        my_csv.write_dataset()

            my_csv.close_csv()

        if subpage == 'rest' or subpage == 'all':
            ##############################################################################
            # Extract from Brandon ESRI REST Service

            # Create CSV file
            csv_fn = "Brandon-Services_results"
            my_csv = shared.MyCSV(csv_fn, self.province)
            my_csv.open_csv()

            rest_url = self.page.get_url('rest_url')
            my_rest = rest.MyREST(rest_url)

            # Get the service data and add it to the CSV file
            serv_data = my_rest.get_data()
            for rec in serv_data:
                for k, v in rec.items():
                    my_csv.add(k, v)

                my_csv.write_dataset()

            my_csv.close_csv()

        if subpage == 'gis' or subpage == 'all':
            ##############################################################################

            # Create CSV file
            csv_fn = "Brandon-GIS_results"
            my_csv = shared.MyCSV(csv_fn, self.province)
            my_csv.open_csv()

            # Extract from what's left of Brandon GIS
            bgis_url = self.page.get_url('bgis_url')

            # Get the soup
            bgis_soup = shared.soup_it_up(bgis_url)

            # Locate the <section> tag with class 'mainContent'
            section = bgis_soup.find('section', attrs={'class': 'mainContent'})

            # Collect all the <li> tags in the section
            li_list = section.find_all('li')

            for li in li_list:
                # Get the map page URL
                map_a = li.find('a')
                map_url = shared.get_anchor_url(map_a, bgis_url)

                # Ignore the Google Maps since it's only a link to Google's Transit Map and
                #   not to a City of Brandon dataset
                if map_url.find('google.ca') > -1: continue
                elif map_url.find('snowmap') > -1:
                    map_url = 'https://gisapp.brandon.ca/webmaps/snowclearing/index.html'

                # Get the map soup
                map_soup = shared.soup_it_up(map_url)

                if map_url.find('arcgis') > -1:
                    # If the map is an ArcGIS Online Map
                    data_url = shared.get_arcgis_url(map_url)

                    map_json = shared.get_json(data_url)

                    title_str = map_json['title']
                    date_str = shared.translate_date(map_json['modified'])
                    desc_str = shared.edit_description(map_json['description'])
                    lic_str = shared.edit_description(map_json['licenseInfo'])
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
                    title_str = shared.get_text(title)

                    # Get the description
                    desc_str = ''
                    desc_tag = map_soup.find('meta', attrs={'name': 'description'})
                    if desc_tag is not None:
                        desc_str = desc_tag['content']

                    # Get the date
                    date_str = ''
                    date_div = map_soup.find('div', attrs={'id': 'updateDiv'})
                    if date_div is not None:
                        date_str = shared.get_text(date_div).replace('Last Updated: ', '')

                    lic_str = ''
                    sp_str = ''
                    data_url = ''

                my_csv.add('Title', title_str)
                my_csv.add('Type', map_type)
                my_csv.add('Description', desc_str)
                my_csv.add('Date', date_str)
                my_csv.add('Data URL', data_url)
                my_csv.add('Web Page URL', bgis_url)
                my_csv.add('Licensing', lic_str)
                my_csv.add('Spatial Reference', sp_str)
                my_csv.add('Web Map URL', map_url)
                my_csv.add('Download', 'No')
                my_csv.add('Access', 'Viewable/Contact the Province')

                my_csv.write_dataset()

            my_csv.close_csv()

    def extract_winnipeg(self, subpage='all', srch_word=None, category=None):

        if subpage == 'cat' or subpage == 'all':
            ##############################################################################
            # Extract from Winnipeg's Catalogue

            # Get the Winnipeg Catalogue URL
            search_url = self.page.get_url('search_url')

            # Create CSV file
            csv_fn = "Winnipeg-Catalogue_results"
            my_csv = shared.MyCSV(csv_fn, self.province)
            my_csv.open_csv()

            # Set the parameters for the query URL
            params = collections.OrderedDict()
            if srch_word is not None: params['q'] = srch_word
            if category is not None: params['limitTo'] = category
            params['sortBy'] = "alpha"

            # Build the query URL
            query_url = shared.build_query_html(search_url, params)

            # Get the soup
            soup = shared.soup_it_up(query_url)

            # Get the number of pages from page buttons at bottom of site
            res_count_div = soup.find('div', attrs={'class': 'browse2-results-title'})
            results_text = shared.get_text(res_count_div)
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
                page_url = shared.build_query_html(search_url, params)
                page_soup = shared.soup_it_up(page_url)

                # Get all the datasets on the current page (all datasets are in a 'div' with class 'dataset-item')
                results = page_soup.find_all('div', attrs={'class': 'browse2-result-content'})

                print "\nPage URL: %s" % page_url
                print "Number of results on page: " + str(len(results))

                if len(results) == 0 and record_count == 0:
                    print "No records exist with the given search parameters."
                    print "URL query sample: %s" % query_url
                    return None

                for dataset in results:

                    # Get the header of the dataset
                    h2 = dataset.find('h2', attrs={'class': 'browse2-result-name'})

                    # Get the link to the page
                    webpage_url = shared.get_link(h2)

                    # Get the soup of the dataset
                    attrb = ('class', 'downloadsList')
                    ds_soup = shared.soup_it_up(webpage_url)

                    # Get the title
                    title_str = ''
                    title = ds_soup.find('meta', attrs={'name': 'title'})
                    if title is not None:
                        title_str = shared.clean_text(title['content'])
                        title_str = title_str.replace(' | Open Data | City of Winnipeg', '')

                    # Get the description
                    desc_str = ''
                    desc = ds_soup.find('meta', attrs={'name': 'description'})
                    if desc is not None: desc_str = shared.clean_text(desc['content'])

                    # Get the publisher
                    pub_str = shared.get_dl_text(ds_soup, 'Department')

                    # Get the date
                    date_str = ''
                    date_span = ds_soup.find('span', attrs={'class': 'aboutUpdateDate'})
                    if date_span is not None: date_str = shared.get_text(date_span)

                    # Get the licence
                    lic_str = shared.get_dl_text(ds_soup, 'Licence')

                    # Set the available formats as KML, KMZ, SHP and GeoJSON
                    formats = ['KML', 'KMZ', 'SHP', 'GeoJSON']
                    access_str = 'Download/Web Accessible'
                    download_str = 'Multiple Downloads'

                    my_csv.add('Title', title_str)
                    my_csv.add('Type', "Google Map")
                    my_csv.add('Description', shared.edit_description(desc_str))
                    my_csv.add('Date', date_str)
                    my_csv.add('Publisher', pub_str)
                    my_csv.add('Licensing', lic_str)
                    my_csv.add('Web Page URL', webpage_url)
                    my_csv.add('Download', download_str)
                    my_csv.add('Available Formats', '|'.join(formats))
                    my_csv.add('Access', access_str)

                    my_csv.write_dataset()

            my_csv.close_csv()

        if subpage == 'air' or subpage == 'all':
            ##############################################################################
            # Extract from Winnipeg's Property Map/Aerial Photography & ServiceStat

            # Create CSV file
            csv_fn = "Winnipeg-Maps_results"
            my_csv = shared.MyCSV(csv_fn, self.province)
            my_csv.open_csv()

            # Extract Property Map webpage
            propertymap_url = self.page.get_url('propertymap_url')

            # Get the soup
            property_soup = shared.soup_it_up(propertymap_url, True, "legenditem")

            # Get the layers
            property_layers = property_soup.find_all('table', attrs={'class': 'legenditem'})

            prop_recs = self.process_googleapi(property_layers, "property")

            for r in prop_recs:
                for k, v in r.items():
                    my_csv.add(k, v)

                my_csv.add('Web Map URL', propertymap_url)
                my_csv.add('Web Page URL', 'http://winnipeg.ca/ppd/maps.stm')
                my_csv.add('Download', 'No')
                my_csv.add('Access', 'Viewable/Contact the Province')

                my_csv.write_dataset()

            # Extract the ServiceStat page
            servstat_url = self.page.get_url('servstat_url')

            # Get the soup
            attrb = ('id', 'wpgmap_legend')
            servstat_soup = shared.soup_it_up(servstat_url, True, attrb)

            # Get the legend and layers
            legend_div = servstat_soup.find('div', attrs={'id': 'wpgmap_legend'})
            servstat_layers = legend_div.find_all('a')

            stats_recs = self.process_googleapi(servstat_layers, "servstat")

            for r in stats_recs:
                for k, v in r.items():
                    my_csv.add(k, v)

                my_csv.add('Web Map URL', servstat_url)
                my_csv.add('Download', 'No')
                my_csv.add('Access', 'Viewable/Contact the Province')

                my_csv.write_dataset()

            my_csv.close_csv()

    def run(self):
        ''' Runs the extraction methods based on the user's input
        :return: None
        '''

        if self.id == "all":
            # Runs all page types
            for key, page in self.pages.items():
                # Get each page's key
                self.page = self.pages[key]
                # Run the appropriate method (extract_<page_key>)
                method_str = 'self.extract_%s()' % key
                print "\nRunning method: %s" % method_str
                eval(method_str)
        else:
            # Runs a specified method based on the page
            if self.id in self.pages.keys():
                self.page = self.pages[self.id]
                # Gather the list of parameters
                params_list = []
                for k, v in self.method_params.items():
                    # If the value is None, set it to all
                    if v is None: v = 'all'
                    # Get a list of arguments which are in the extract method
                    method = 'self.extract_%s' % self.id
                    method_args = inspect.getargspec(eval(method)).args
                    # If the key is not in the method's arguments list, skip it
                    if not k in method_args: continue
                    # Create the list of arguments and values for the method
                    if isinstance(v, str):
                        params_list.append('%s="%s"' % (k, v))
                    else:
                        params_list.append('%s=%s' % (k, v))
                params_str = ', '.join(params_list)
                # Run the appropriate method (extract_<page_id> with parameters for arguments)
                method_str = 'self.extract_%s(%s)' % (self.id, params_str)
                print "\nRunning method: %s" % method_str
                eval(method_str)
            else:
                print "\nERROR: Invalid page '%s'. Please enter one of the following: %s" % (
                    self.id, ', '.join(self.pages.keys()))
                print "Exiting process."
                sys.exit(1)

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
        parser.add_argument("-c", "--category", help="The category for the city sites.")
        parser.add_argument("-b", "--subpage", help="The sub-page to extract.")
        parser.add_argument("-s", "--silent", action='store_true',
                            help="If used, no extra parameters will be queried.")
        args = parser.parse_args()

        page = args.page
        params = collections.OrderedDict()
        params['subpage'] = args.subpage
        params['category'] = args.category
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

        print page
        print "Parameters: " + str(params)

        ext.set_page(page)
        ext.set_params(params)
        ext.run()

    except Exception, err:
        ext.print_log('ERROR: %s\n' % str(err))
        ext.print_log(traceback.format_exc())
        ext.close_log()

if __name__ == '__main__':
    sys.exit(main())

# def process_googleapi(layers, lyr_type, field_names, my_csv):
# 	for layer in layers:
# 		rec_dict = collections.OrderedDict((k, "") for k in field_names)
#
# 		if lyr_type == "property":
# 			element = layer.find('input')
# 			id = element.get('id')
# 			id = id.replace("chk", "")
# 		else:
# 			element = layer
# 			id = element.get('id')
# 			id = id.replace("chk-id", "")
#
# 		title = shared.get_text(layer)
#
# 		#print "Input: " + str(input)
# 		print "Title: " + str(title)
# 		print "ID: " + str(id)
#
# 		# Build query URL
# 		# Ex: https://mapapi.winnipeg.ca/mapapi/wfs.ashx?output=json&maptypeid=2&coordinates=&g=n&featurelist=13937
# 		mapapi_url = "https://mapapi.winnipeg.ca/mapapi/wfs.ashx"
# 		srch_params = collections.OrderedDict()
# 		srch_params['output'] = "json"
# 		srch_params['maptypeid'] = "2"
# 		srch_params['coordinates'] = ""
# 		srch_params['g'] = "n"
# 		srch_params['featurelist'] = id
#
# 		query_url = shared.build_query_html(mapapi_url, srch_params)
#
# 		# Get soup
# 		json_res = shared.get_json(query_url)
#
# 		#field_names = ['Title', 'Type', 'Description', 'Date', 'URL']
# 		features = json_res['features']
#
# 		rec_dict['Title'] = title
# 		rec_dict['URL'] = query_url
# 		serv_type = features[0]['serviceType']
# 		if serv_type == "both": serv_type = "WMS|WFS"
# 		rec_dict['Type'] = serv_type.upper()
# 		rec_dict['Description'] = features[0]['DESCRIPTION']
#
# 		#print json_res
#
# 		#answer = raw_input("Press enter...")
#
# 		my_csv.write_dataset(rec_dict)
#
# def extract_Brandon():
# 	##############################################################################
# 	# Extract from Brandon OpenData
#
# 	opendata_url = "http://opengov.brandon.ca/OpenDataService/opendata.html"
#
# 	# Get soup
# 	soup = shared.soup_it_up(opendata_url)
#
# 	table = soup.find('table', attrs={'id': 'datasetTable'})
# 	rows = table.find_all('tr')
#
# 	# Create CSV file
# 	csv_fn = "Brandon_results"
# 	field_names = ['Title', 'Type', 'URL']
# 	my_csv = shared.MyCSV(csv_fn, opendata_url, province, field_names)
# 	my_csv.open_csv()
#
# 	for row in rows:
# 		anchor = row.find('a')
#
# 		if anchor is not None:
# 			# Get the parent row
# 			tr = anchor.parent.parent
# 			tds = tr.find_all('td')
#
# 			title = shared.get_text(tds[0])
# 			ds_type = shared.get_text(tds[1])
#
# 			rec_dict = collections.OrderedDict((k, "") for k in field_names)
#
# 			rec_dict['Title'] = title
# 			rec_dict['Type'] = ds_type
# 			link = anchor['href']
# 			rec_dict['URL'] = urlparse.urljoin(opendata_url, link)
#
# 			my_csv.write_dataset(rec_dict)
#
# 	##############################################################################
# 	# Extract from Brandon GIS REST
# 	rest_url = "https://gisapp.brandon.ca/arcgis/rest/services"
# 	my_rest = rest.MyREST(rest_url)
#
# 	# Write the URL for Brandon GIS REST to CSV
# 	field_names = ['Title', 'Type', 'Description', 'URL']
# 	my_csv.write_line("")
# 	my_csv.write_url(rest_url, "Brandon GIS ArcGIS REST")
# 	my_csv.write_header(field_names)
#
# 	services = my_rest.get_services()
#
# 	for service in services:
# 		rec_dict = collections.OrderedDict((k, "") for k in field_names)
#
# 		rec_dict['Title'] = service['name']
# 		rec_dict['Type'] = service['type']
# 		rec_dict['Description'] = shared.edit_description(service['serviceDescription'])
# 		rec_dict['URL'] = service['url']
#
# 		my_csv.write_dataset(rec_dict)
#
# 	##############################################################################
# 	# Extract from what's left of Brandon GIS
# 	bgis_url = "http://gis.brandon.ca/"
# 	bgis_soup = shared.soup_it_up(bgis_url)
#
# 	section = bgis_soup.find('section', attrs={'class': 'mainContent'})
#
# 	li_list = section.find_all('li')
#
# 	map_list = ["Recreation", "Recycling Dropoffs", "Ward Map", "Community Map"]
#
# 	# Write the URL for Brandon GIS to CSV
# 	field_names = ['Title', 'Type', 'URL']
# 	my_csv.write_line("")
# 	my_csv.write_url(bgis_url, "Brandon GIS")
# 	my_csv.write_header(field_names)
#
# 	for li in li_list:
# 		title = shared.get_text(li)
# 		if title in map_list:
# 			rec_dict = collections.OrderedDict((k, "") for k in field_names)
#
# 			url = shared.get_link(li)
#
# 			# Extract the Webmap ID from the URL
# 			start_pos = url.find("webmap")
# 			url_list = url[start_pos:].split("=")
# 			id = url_list[1]
#
# 			arcgis_rest_url = "https://www.arcgis.com/sharing/rest/content/items"
# 			dataset_url = "%s/%s/data?f=json" % (arcgis_rest_url, id)
#
# 			ds_json = shared.get_json(dataset_url)
#
# 			if title.find("Map") == -1:
# 				title = "%s Map" % title
#
# 			rec_dict['Title'] = title
# 			rec_dict['Type'] = "ArcGIS Feature"
# 			rec_dict['URL'] = dataset_url
#
# 			my_csv.write_dataset(rec_dict)
#
# 	my_csv.close_csv()
#
#
# def extract_Winnipeg(srch_word=None, category=None):
#
# 	##############################################################################
# 	# Extract from Winnipeg's Catalogue
#
# 	# Build url
# 	search_url = "https://data.winnipeg.ca/browse"
#
# 	srch_params = collections.OrderedDict()
# 	if srch_word is not None: srch_params['q'] = srch_word
# 	if category is not None: srch_params['limitTo'] = category
# 	srch_params['sortBy'] = "alpha"
#
# 	query_url = shared.build_query_html(search_url, srch_params)
#
# 	# Get soup
# 	soup = shared.soup_it_up(query_url)
#
# 	# Get the number of pages from page buttons at bottom of site
# 	res_count_div = soup.find('div', attrs={'class': 'browse2-result-count'})
# 	results_text = shared.get_text(res_count_div)
# 	res_lst = results_text.split(" ")
#
# 	#print "Results: " + str(results_text.split(" "))
#
# 	num_results = res_lst[len(res_lst) - 2]
#
# 	# Create CSV file
# 	csv_fn = "Winnipeg_results"
# 	field_names = ['Title', 'Type', 'Description', 'Date', 'URL']
# 	my_csv = shared.MyCSV(csv_fn, query_url, province, field_names)
# 	my_csv.open_csv()
#
# 	#print "# of Results: " + str(num_results)
#
# 	#answer = raw_input("Press enter...")
#
# 	page_count = math.ceil(int(num_results) / 10.0)
# 	prev_perc = -1
# 	record_count = 0
# 	record_total = int(num_results)
#
# 	print "Number of pages: " + str(page_count)
#
# 	# Write the URL for Winnipeg Catalogue to CSV
# 	#my_csv.write_url(query_url, "Winnipeg Catalogue URL")
#
# 	for page in range(0, int(page_count)):
# 		# Open each iteration of pages:
# 		srch_params['page'] = page + 1
# 		page_url = shared.build_query_html(search_url, srch_params)
# 		page_soup = shared.soup_it_up(page_url)
#
# 		# Get all the datasets on the current page (all datasets are in a 'div' with class 'dataset-item')
# 		results = page_soup.find_all('div', attrs={'class': 'browse2-result-content'})
#
# 		print "\nPage URL: %s" % page_url
# 		print "Number of results on page: " + str(len(results))
#
# 		if len(results) == 0 and record_count == 0:
# 			print "No records exist with the given search parameters."
# 			print "URL query sample: %s" % query_url
# 			return None
#
# 		for dataset in results:
# 			rec_dict = collections.OrderedDict((k, "") for k in field_names)
#
# 			#print datasets
#
# 			# Get the header of the dataset
# 			h2 = dataset.find('h2', attrs={'class': 'browse2-result-name'})
#
# 			# Get the title of the dataset
# 			if h2 is None:
# 				print "No h2 exists in %s." % dataset.tagname
# 			else:
# 				title_str = shared.get_text(h2)
# 				rec_dict['Title'] = title_str
#
# 			# Get the link to the page
# 			link = shared.get_link(h2)
# 			rec_dict['URL'] = link
#
# 			# Set the type
# 			rec_dict['Type'] = "Interactive Map"
#
# 			# Get the description
# 			desc_div = dataset.find('div', attrs={'class': 'browse2-result-description'})
# 			desc_str = shared.get_text(desc_div)
# 			rec_dict['Description'] = shared.edit_description(desc_str)
#
# 			# Get the date
# 			date_div = dataset.find('div', attrs={'class': 'browse2-result-timestamp-value'})
# 			date_str = shared.get_text(date_div)
# 			rec_dict['Date'] = date_str
#
# 			#print rec_dict
#
# 			my_csv.write_dataset(rec_dict)
#
# 	##############################################################################
# 	# Extract from Winnipeg's Property Map/Aerial Photography & ServiceStat
#
# 	# Extract Property Map webpage
# 	propertymap_url = "http://winnipeg.ca/ppd/maps_aerial.stm"
# 	property_soup = shared.soup_it_up(propertymap_url, True, "legenditem")
# 	property_layers = property_soup.find_all('table', attrs={'class': 'legenditem'})
# 	#property_list = [('property', i) for i in property_tables]
#
# 	# Write the URL for Winnipeg's Property Map to CSV
# 	my_csv.write_line("")
# 	my_csv.write_url(propertymap_url, "Winnipeg Property Map/Aerial Photography URL")
# 	my_csv.write_header()
#
# 	process_googleapi(property_layers, "property", field_names, my_csv)
#
# 	# Extract the ServiceStat page
# 	servstat_url = "http://winnipeg.ca/Interhom/serviceStat/"
# 	servstat_soup = shared.soup_it_up(servstat_url, True, "wpgmap_legend", el_type='id')
# 	legend_div = servstat_soup.find('div', attrs={'id': 'wpgmap_legend'})
# 	servstat_layers = legend_div.find_all('a')
# 	#servstat_list = [('servstat', i) for i in anchors]
#
# 	# Write the URL for Winnipeg's ServiceStat to CSV
# 	my_csv.write_line("")
# 	my_csv.write_url(servstat_url, "Winnipeg ServiceStat URL")
# 	my_csv.write_header()
#
# 	process_googleapi(servstat_layers, "servstat", field_names, my_csv)
#
# 	##############################################################################
# 	#
#
# 	my_csv.close_csv()
#
# def main():
# 	city_list = ['Winnipeg', 'Brandon']
#
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("-c", "--city", help="The city to extract: %s" % ', '.join(city_list))
# 	parser.add_argument("-w", "--word", help="The key word(s) to search for.")
# 	#parser.add_argument("-f", "--format", help="The format(s) to search for.")
# 	parser.add_argument("-a", "--category", help="The category to search for.")
# 	#parser.add_argument("-d", "--downloadable", help="Determines wheter to get only downloadable datasets.")
# 	#parser.add_argument("-l", "--html", help="The HTML file to scrape (only for OpenData website).")
# 	parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
# 	args = parser.parse_args()
# 	#print args.echo
#
# 	#print "province: " + str(args.province)
# 	#print "format: " + str(args.format)
#
# 	city = args.city
# 	word = args.word
# 	#formats = args.format
# 	#html = args.html
# 	silent = args.silent
# 	cat = args.category
# 	#downloadable = args.downloadable
#
# 	if city is None:
# 		answer = raw_input("Please enter the city you would like to extract (%s): " % ', '.join(city_list))
# 		if not answer == "":
# 			city = answer.lower()
# 		else:
# 			print "\nERROR: Please specify a city."
# 			print "Exiting process."
# 			sys.exit(1)
#
# 	if word is None and not silent:
# 		answer = raw_input("Please enter the word you would like to search: ")
# 		if not answer == "":
# 			word = answer.lower()
#
# 	if cat is None and not silent:
# 		answer = raw_input("Please enter the category you would like to search: ")
# 		if not answer == "":
# 			cat = answer.lower()
#
# 	if city.lower() == "winnipeg":
# 		extract_Winnipeg(word, cat)
# 	elif city.lower() == "brandon":
# 		extract_Brandon()
# 	else:
# 		print "\nERROR: Invalid city '%s'. Please enter one of the following: %s" % (city, ', '.join(city_list))
# 		print "Exiting process."
# 		sys.exit(1)
#
# 	#geoportal_list = extract_geoportal(province)
#
# if __name__ == '__main__':
# 	sys.exit(main())
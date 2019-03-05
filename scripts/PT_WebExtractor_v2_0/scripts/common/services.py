import codecs
import json
import os
import sys
import urllib2
import pprint
import re
from bs4 import BeautifulSoup
import collections
from urlparse import urlparse

# Get the shared.py
# script_file = os.path.abspath(__file__)
# script_folder = os.path.dirname(script_file)
# province_folder = os.path.dirname(script_folder)
# home_folder = os.path.dirname(province_folder)
# script_folder = home_folder + "\\scripts"
#
# sys.path.append(script_folder)
import shared
import bsoup

class PT_Geocortex:
	def __init__(self, root_url, prefix=None, silent=False):
		self.root_url = root_url
		self.root_query = "%s?f=pjson" % self.root_url
		# print "#1"
		self.root_json = shared.get_json(self.root_query)
		self.prefix = prefix
		self.silent = silent
		
		self.extract_data()
		
	def extract_data(self):
	
		data_json = collections.OrderedDict()
	
		# Get a list of folders from the root
		sites_json = []
		if 'folders' in self.root_json:
			folders = self.root_json['folders']
		
			#out_services = []
			#for folder in folders:
			for folder in folders:
				# Go through each folder
				folder_path = '%s/%s' % (self.root_url, folder)
				folder_query = "%s?f=pjson" % folder_path
				folder_json = shared.get_json(folder_query)
				
				folder_info = collections.OrderedDict()
				folder_info['url'] = folder_path
				
				if 'sites' in folder_json:
					sites_json.append(folder_json['sites'])	
		
		if 'sites' in self.root_json:
			sites_json.append(self.root_json['sites'])
			
		# FOR DEBUG
		# for serv in sites_json:
		#	 print serv
		# answer = raw_input("Press enter...")
		
		sites_total = sum([len(s) for s in sites_json])
		
		# If the total number sites is 0, then the input might be a 
		#	MapService itself
		if sites_total == 0:
			sites_json.append([self.root_json])
			
			sites_total = sum([len(s) for s in sites_json])
		
		if not self.silent:
			print "Total number of sites: %s" % sites_total
			
		# Get any sites in the folder
		out_sites = []
		curr_number = 0
		for site in sites_json:
			#serv_lst = folder_json['sites']
			
			for idx, s_info in enumerate(site):
				if not self.silent:
					print "Getting %s of %s sites for '%s'" \
							% (curr_number + idx + 1, sites_total, self.root_url)
						
				# print "s_info: %s" % s_info
				
				if 'name' in s_info:
					if s_info['name'].find('Latest') > -1: continue
			
				site_data = self.get_site_data(s_info)
				
				out_sites.append(site_data)
				
			if not self.silent:
				print
			
			curr_number = curr_number + len(site)
			
		data_json['sites'] = out_sites
		
		self.all_data = data_json
		
		#self.print_data()
		
	def get_data(self):
		return self.all_data
		
	def get_layers(self):
		''' Gets all the unique layers from the services by
			merging similar layers together
		'''
		
		layers = []
		for site in self.all_data['sites']:
			# Go through each site
			#print site
			if 'services' in site:
				for serv in site['services']:
					# Go through each service
					serv_lyrs = serv['layers']
					if len(serv_lyrs) == 0:
					
						downloads = 'No'
						access = 'Viewable/Contact the Province'
					
						# Get extents
						exts_dict = serv['fullExtent']
						west = exts_dict['xmin']
						east = exts_dict['xmax']
						north = exts_dict['ymax']
						south = exts_dict['ymin']
						
						ext_lst = [north, south, east, west]
						
						wkt_text = ''
						sp = exts_dict['spatialReference']
						#answer = raw_input("Press enter...")
						if 'latestWkid' in sp:
							epsg = sp['latestWkid']
							wkt_text = shared.create_wkt_extents(ext_lst, epsg)
						elif 'wkt' in sp:
							wkt_sp = sp['wkt']
							wkt_text = shared.create_wkt_extents(ext_lst, in_wkt=wkt_sp)
							
						proj_str = shared.get_spatialref(serv)
						
						new_lyr = collections.OrderedDict()
					
						# If no layer exists, use the service as the layer
						new_lyr['Source'] = 'Map Services'
						new_lyr['Title'] = serv['displayName']
						new_lyr['Description'] = serv['description']
						#new_lyr['Publisher'] = publish_str
						new_lyr['Type'] = serv['serviceType']
						#new_lyr['Recent Date'] = date_str
						new_lyr['Extents'] = wkt_text
						#new_lyr['Keywords'] = keywords
						new_lyr['Data URL'] = '%s?f=pjson' % serv['url']
						new_lyr['Access'] = access
						new_lyr['Service'] = 'GeoCortex'
						new_lyr['Service Name'] = serv['displayName']
						new_lyr['Service URL'] = serv['url']
						#new_lyr['Available Formats'] = "|".join(formats)
						new_lyr['Spatial Reference'] = proj_str
						#new_lyr['Metadata URL'] = mdata_url
						new_lyr['Download'] = downloads
						
						layers.append(new_lyr)
					else:
						layers += serv_lyrs
			else:
				new_lyr = collections.OrderedDict()
			
				# If no layer exists, use the service as the layer
				new_lyr['Source'] = 'Map Services'
				new_lyr['Title'] = site['name']
				new_lyr['Service'] = 'GeoCortex'
				new_lyr['Service Name'] = site['name']
				new_lyr['Service URL'] = site['url']
				new_lyr['Notes'] = site['notes']
				
				layers.append(new_lyr)
		
		if not self.silent:
			print "Number of layers: %s" % len(layers)
		
		return layers
		
	def get_lyr_data(self, lyr_info, serv_info):
		''' Gets the layer data for a specified layer
		'''
	
		lyr_name = lyr_info['name']
		lyr_id = lyr_info['id']
		lyr_path = "%s/layers/%s" % (serv_info['url'], lyr_id)
		
		lyr_query = "%s?f=pjson" % lyr_path
		lyr_json = shared.get_json(lyr_query)
		
		# print lyr_query
		# with open('serv_info.json', 'w') as outfile:
			# json.dump(serv_info, outfile)
		#answer = raw_input("Press enter...")
		
		# Get the information from the site info
		# Get the downloads and access
		#formats = serv_info['formats']
		#if len(formats) == 0:
		downloads = 'No'
		access = 'Viewable/Contact the Province'
		#elif len(formats) == 1:
		#	downloads = 'Multiple Downloads'
		#	access = 'Download using ESRI REST Service'
		#else:
		#	downloads = 'Multiple Downloads'
		#	access = 'Download using GeoCortex Service'
		
		# Get the site information
		if 'name' in serv_info: serv_name = serv_info['name']
		else: serv_name = serv_info['displayName']
		
		serv_url = serv_info['url']
		#mdata_url = serv_info['metadata']
		
		# Get the keywords
		# keywords = ''
		# if 'documentInfo' in serv_info:
			# keywords = serv_info['documentInfo']['Keywords']
		
		# Get the dates
		# date_str = ''
		# if 'editingInfo' in serv_info:
			# edit_info = serv_info['editingInfo']
			# if 'lastEditDate' in edit_info:
				# date_str = edit_info['lastEditDate']
		# else:
			# # Get date from URL
			# date = re.search(r'\d{4}\d{2}\d{2}', lyr_query)
			# if date is not None:
				# date_str = date.group()[0]
				
		# xml_mdata = bsoup.xml_to_dict(mdata_url, silent=True)
		
		# startdate_str = ''
		# if 'metadata' in xml_mdata:
			# if 'Esri' in xml_mdata['metadata']:
				# esri = xml_mdata['metadata']['Esri']
				# if 'CreaDate' in esri:
					# startdate_str = esri['CreaDate']
				
		# Get publisher/author
		publish_str = ''
		if 'documentInfo' in serv_info:
			publish_str = serv_info['documentInfo']['Author']
		
		#print
		#print "Date: '%s'" % date_str
		#answer = raw_input("Press enter...")
		
		# Get extents
		exts_dict = serv_info['fullExtent']
		west = exts_dict['xmin']
		east = exts_dict['xmax']
		north = exts_dict['ymax']
		south = exts_dict['ymin']
		
		ext_lst = [north, south, east, west]
		
		wkt_text = ''
		sp = exts_dict['spatialReference']
		#answer = raw_input("Press enter...")
		if 'latestWkid' in sp:
			epsg = sp['latestWkid']
			wkt_text = shared.create_wkt_extents(ext_lst, epsg)
		elif 'wkt' in sp:
			wkt_sp = sp['wkt']
			wkt_text = shared.create_wkt_extents(ext_lst, in_wkt=wkt_sp)
		#print "\nwkt_text: %s" % wkt_text
		
		out_lyr = collections.OrderedDict()
		if lyr_json is None or 'err' in lyr_json:
			
			out_lyr['Source'] = 'Map Services'
			out_lyr['Title'] = 'ERROR (see notes)'
			out_lyr['Description'] = ''
			out_lyr['Data URL'] = lyr_query
			#out_lyr['Start Date'] = startdate_str
			#out_lyr['Recent Date'] = date_str
			out_lyr['Extents'] = wkt_text
			#out_lyr['Keywords'] = keywords
			out_lyr['Access'] = access
			out_lyr['Service'] = 'GeoCortex'
			out_lyr['Service Name'] = serv_name
			out_lyr['Service URL'] = serv_url
			#out_lyr['Metadata URL'] = mdata_url
			out_lyr['Download'] = downloads
			out_lyr['Notes'] = 'Timeout Occurred when loading this layer.'
			
			return out_lyr
		
		#out_lyr = lyr_json
		#out_lyr['url'] = lyr_path
		
		if 'error' in lyr_json:
			print "\nWARNING - Code %s: %s" % \
					(lyr_json['code'], lyr_json['message'])
			out_lyr['Source'] = 'Map Services'
			out_lyr['Title'] = 'ERROR (see notes)'
			out_lyr['Description'] = ''
			out_lyr['Data URL'] = lyr_query
			#out_lyr['Start Date'] = startdate_str
			#out_lyr['Recent Date'] = date_str
			out_lyr['Extents'] = wkt_text
			#out_lyr['Keywords'] = keywords
			out_lyr['Access'] = access
			out_lyr['Service'] = 'GeoCortex'
			out_lyr['Service Name'] = serv_name
			out_lyr['Service URL'] = serv_url
			#out_lyr['Metadata URL'] = mdata_url
			out_lyr['Download'] = downloads
			out_lyr['Notes'] = lyr_json['message']
			
			return out_lyr
		
		# Get the layer information
		title_str = lyr_json['displayName']
		if serv_name.find('.') > -1: srv_title = serv_name.split('.')[0]
		else: srv_title = serv_name
		srv_title = srv_title.replace('_', ' ')
		title_str = "%s - %s" % (srv_title, title_str)
		desc_str = lyr_json['description']
		type_str = lyr_json['type']
		
		proj_str = shared.get_spatialref(lyr_json)
		
		out_lyr['Source'] = 'Map Services'
		out_lyr['Title'] = title_str
		out_lyr['Description'] = desc_str
		#out_lyr['Publisher'] = publish_str
		out_lyr['Type'] = type_str
		#out_lyr['Recent Date'] = date_str
		out_lyr['Extents'] = wkt_text
		#out_lyr['Keywords'] = keywords
		out_lyr['Data URL'] = lyr_query
		out_lyr['Access'] = access
		out_lyr['Service'] = 'GeoCortex'
		out_lyr['Service Name'] = serv_name
		out_lyr['Service URL'] = serv_url
		#out_lyr['Available Formats'] = "|".join(formats)
		out_lyr['Spatial Reference'] = proj_str
		#out_lyr['Metadata URL'] = mdata_url
		out_lyr['Download'] = downloads
		
		return out_lyr
		
	def get_site_data(self, site_info):
		''' Gets the site data for a specified site
		'''
		
		if 'id' in site_info:
			site_name = site_info['id']
			site_path = "%s/%s" % (self.root_url, site_name)
		else:
			site_path = self.root_url
			site_name = self.root_url
		
		# Extract date from name
		site_parse = site_name.split('/')
		date = site_parse[len(site_parse) - 1]
		#print date
		#answer = raw_input("Press enter...")
		date_str = ''
		if date.isdigit():
			if len(str(int(date))) == 8:
				date_str = date
		
		site_query = "%s?f=pjson" % site_path
		site_json = shared.get_json(site_query)
		
		# print(json.dumps(site_json, indent=4, sort_keys=True))
		# answer = raw_input("Press enter...")
		
		if site_json is None:
			out_site = collections.OrderedDict()
			out_site['name'] = site_name
			out_site['notes'] = 'Timeout Occurred when loading this layer.'
			out_site['url'] = site_path
			return out_site
			
		if 'error' in site_json:
			msg = site_json['error']['message']
			print
			print msg
			out_site = collections.OrderedDict()
			out_site['name'] = site_name
			out_site['notes'] = site_json['error']['message']
			out_site['url'] = site_path
			return out_site
		
		out_site = site_json
		out_site['url'] = site_path
		# #out_site['metadata'] = "%s/info/metadata" % site_path
		out_site['name'] = site_name
		
		# Get the map service url
		map_url = "%s/map" % site_path
		map_query_url = "%s?f=pjson" % map_url
		map_json = shared.get_json(map_query_url)
		
		#print map_query_url
		#print(json.dumps(map_json, indent=4))
		#answer = raw_input("Press enter...")
		
		# Get a list of services
		services = []
		if not 'mapServices' in map_json:
			out_site['notes'] = 'No available map services.'
			return out_site
		servs = map_json['mapServices']
		for serv in servs:
			serv_json = serv
			
			#print map_query_url
			#print(json.dumps(serv_json, indent=4))
			#answer = raw_input("Press enter...")
			
			# Get the title
			serv_name = serv['displayName']
			serv_id = serv['id']
			serv_json['title'] = serv_name
			serv_json['url'] = '%s/mapservices/%s' % (map_url, serv_id)
			
			# Get the layers
			if 'layers' in serv:
				layers = []
				for idx, lyr in enumerate(serv['layers']):
					
					#print(json.dumps(lyr, indent=4))
					#answer = raw_input("Press enter...")
					
					if 'subLayerIds' in lyr:
						if len(lyr['subLayerIds']) > 0:
							continue
					
					if not self.silent:
						msg = "Getting %s of %s layers for '%s'" \
								% (idx + 1, len(serv['layers']), serv_name)
						shared.print_oneliner(msg)
				
					# Ignore group layers
					lyr_data = self.get_lyr_data(lyr, serv_json)
					
					layers.append(lyr_data)
					
				if not self.silent:
					print
					
			serv_json['layers'] = layers
			
			services.append(serv_json)
		
		out_site['services'] = services
		
		return out_site
		
			# # Get the formats
			
			# # Get the layers
			
			# #print site_json
			# formats = []
			# if 'supportedQueryFormats' in site_json:
				# query_formats = site_json['supportedQueryFormats']
			# else:
				# query_formats = ''
				
			# if 'supportedExtensions' in site_json:
				# extensions = site_json['supportedExtensions']
			# else:
				# extensions = ''
			
				# formats = query_formats.split(', ') + extensions.split(', ')
				
			# out_site['formats'] = [f for f in formats if not f == '']
			
			# layers = []
			# if 'layers' in site_json:
				# for idx, lyr in enumerate(site_json['layers']):
					# if 'subLayerIds' in lyr:
						# if lyr['subLayerIds'] is not None:
							# continue
					
					# msg = "Getting %s of %s layers for '%s'" \
							# % (idx + 1, len(site_json['layers']), site_name)
					# shared.print_oneliner(msg)
				
					# # Ignore group layers
					# lyr_data = self.get_lyr_data(lyr, out_site)
					
					# layers.append(lyr_data)
						
				# print
						
			# out_site['layers'] = layers
		
		#return out_site
		
	def print_data(self):
	
		r = json.dumps(self.all_data)
		loaded_r = json.loads(r)
	
		with open("site_test.json", "w") as d_file:
			json.dump(loaded_r, d_file, indent=4, sort_keys=True)
			
		out_f = open('dates.txt', 'w')
		for d in self.all_data['sites']:
			out_f.write('%s: %s\n' % (d['name'], d['date']))
			
		out_f.close()
			
	
		# site_data = self.get_sites()
		
		# return site_data

	# def get_site_data(self, site):
		# ''' Gets the data for the GeoCortex Services
		# :return: A list of data as dictionaries.
		# '''

		# # # Get a list of services
		# # print("\nGetting the Geocortex sites for '%s'..." % self.root_url)
		# # sites = self.get_sites()
		
		# # if sites is None: return None

		# data_list = []
		
		# if site == 'error':
			# err_dict = collections.OrderedDict()
			# err_dict['err'] = "Site could not be accessed."
			# return err_dict
	
		# # If the site contains a key with 'err', add the result
		# #   to the CSV with a note 'Service could not be loaded.'
		# if 'error' in site:
			# #print "\nsite: %s" % site
		
			# data_dict = collections.OrderedDict()

			# if self.prefix is None:
				# data_dict['Title'] = site['name']
			# else:
				# data_dict['Title'] = "%s - %s" % (self.prefix, site['name'])
			# data_dict['Type'] = "Geocortex Essentials REST API"
			# data_dict['Service URL'] = site['url']
			# if site['error']['code'] == 403:
				# data_dict['Access'] = 'Login Required/Contact the Territory'
			# data_dict['Service'] = 'Geocortex Essentials REST'
			# #data_dict['Service URL'] = self.root_url
			# data_dict['Download'] = 'No'

			# data_list.append(data_dict)

			# return data_list

		# #print site['url']

		# # Get site info
		# site_name = site['name']
		# #site_type = site['type']
		# site_url = site['url']

		# # Get the description
		# desc_str = ''
		# if 'description' in site:
			# desc_str = site['description']

		# # Load the map page to get a list of layers
		# map_url = site_url + "/map?f=pjson"
		# map_json = shared.get_json(map_url)
		
		# if map_json is None:
			# map_json = lyr
			# map_json['notes'] = 'Timeout Occurred when loading this layer.'
			# map_json['url'] = lyr_url
			# return map_json

		# # Get the layers
		# map_services = map_json['mapServices']

		# for map_serv in map_services:
			# layers = map_serv['layers']

			# for idx, lyr in enumerate(layers):
				# msg = "Getting %s of %s layers" % (idx + 1, 
						# len(layers))
				# shared.print_oneliner(msg)
			
				# data_dict = collections.OrderedDict()
				
				# lyr_name = lyr['displayName']
				# lyr_name = lyr_name.replace('_', ' ')
				# lyr_name = shared.clean_text(lyr_name)

				# # Get the title of the layer
				# if self.prefix is None:
					# title_str = lyr_name
				# else:
					# title_str = "%s - %s" % (self.prefix, lyr_name)
					
				# type_str = ''
				# if 'type' in lyr:
					# type_str = lyr['type']
					# if type_str.lower() == 'group layer' or \
						# type_str.lower() == 'grouplayer':
						# continue

				# # Get the spatial reference
				# sp_str = shared.get_spatialref(lyr)

				# # Add the results in the data_dict
				# data_dict['Source'] = 'Map Services'
				# data_dict['Title'] = title_str
				# data_dict['Description'] = desc_str
				# data_dict['Type'] = type_str
				# data_dict['Access'] = 'Contact the Province'
				# data_dict['Service Name'] = site_name
				# data_dict['Service URL'] = site_url
				# data_dict['Spatial Reference'] = sp_str
				# data_dict['Service'] = 'GeoCortex'
				# data_dict['Download'] = 'No'

				# # Write the results to the data_list
				# data_list.append(data_dict)

			# print
					
		# return data_list

	# def get_site_json(self, site_json):
		# ''' Gets the JSON for a site from a list of sites in an initial JSON page.
		# :param site_json: The initial JSON page containing a list of sites.
		# :return: The JSON of the site.
		# '''

		# # Get the site name and ID
		# site_name = site_json['displayName']
		# id = site_json['id']

		# # Add the name to the root URL to get the site URL
		# url = "%s/%s" % (self.root_url, id)

		# # Get the JSON URL of the site
		# json_url = "%s?f=pjson" % url

		# # Get the JSON
		# site_json = shared.get_json(json_url)
		# if site_json is not None:
			# # Add the URL and Name to the site JSON text
			# site_json['url'] = url
			# site_name = site_name.split("/")
			# site_json['name'] = site_name[len(site_name) - 1].replace("_", " ")

			# return site_json

	# def get_sites(self, url=None, json=None):
		# ''' Gets all the JSON text for all the sites under a Geocortex Service page
		# :param url: The root URL
		# :param json: The root JSON format
		# :return: A list of JSON formatted sites.
		# '''

		# if url is None: url = self.root_url
		# if json is None: json = self.root_json

		# sites = []
		
		# if json is None: return None
		
		# if 'err' in json or 'error' in json: return json

		# sites_json = json['sites']
		# for idx, site in enumerate(sites_json):
			# site_name = site['displayName']
			# print "Adding %s of %s sites to list" \
					# % (idx + 1, len(sites_json))
			
			# # Get the JSON data for the current service
			# json_data = self.get_site_json(site)
			
			# # Get the data of the service
			# site_data = self.get_site_data(json_data)
			
			# for site in site_data:
				# sites.append(site)

		# if 'folders' in json:
			# folders = json['folders']

			# for folder in folders:
				# sub_query = "%s/%s?f=pjson" % (url, folder)
				# sub_json = shared.get_json(sub_query)
				# if sub_json is not None:
					# sites += self.get_sites(url, sub_json)

		# return sites

class PT_REST:
	def __init__(self, root_url, prefix=None, silent=False):
		self.root_url = root_url
		self.silent = silent
		if self.root_url.find('json') > -1:
			self.root_url = self.root_url.split('?')
			#print self.root_url
			self.root_url = self.root_url[0]
			#answer = raw_input("Press enter...")
		self.root_query = "%s?f=pjson" % self.root_url
		
		self.root_json = shared.get_json(self.root_query)
		self.prefix = prefix
		self.all_data = None
		
		self.extract_data()
		
	def extract_data(self):
		data_json = collections.OrderedDict()
		
		#print self.root_json
	
		# Get a list of folders from the root
		servs_json = []
		if 'folders' in self.root_json:
			folders = self.root_json['folders']
		
			#out_services = []
			#for folder in folders:
			for folder in folders:
				# Go through each folder
				folder_path = '%s/%s' % (self.root_url, folder)
				folder_query = "%s?f=pjson" % folder_path
				folder_json = shared.get_json(folder_query)
				
				folder_info = collections.OrderedDict()
				folder_info['url'] = folder_path
				
				if 'services' in folder_json:
					servs_json.append(folder_json['services'])		
		
		if 'services' in self.root_json:
			servs_json.append(self.root_json['services'])
			
		# FOR DEBUG
		# for serv in servs_json:
		#	 print serv
		#	 answer = raw_input("Press enter...")
		
		service_total = sum([len(s) for s in servs_json])
		
		# If the total number services is 0, then the input might be a 
		#	MapService itself
		if service_total == 0:
			servs_json.append([self.root_json])
			
			service_total = sum([len(s) for s in servs_json])
		
		if not self.silent:
			print "Total number of services: %s" % service_total
			
		# Get any services in the folder
		out_services = []
		curr_number = 0
		for service in servs_json:
			#serv_lst = folder_json['services']
			
			for idx, serv in enumerate(service):
				if not self.silent:
					print "Getting %s of %s services for '%s'" \
						% (curr_number + idx + 1, service_total, self.root_url)
						
				# print "serv: %s" % serv
				
				if 'name' in serv:
					if serv['name'].find('Latest') > -1: continue
			
				serv_data = self.get_serv_data(serv)
				
				out_services.append(serv_data)
				
			if not self.silent:	
				print
			
			curr_number = curr_number + len(service)
			
		data_json['services'] = out_services
		
		self.all_data = data_json
		
		#self.print_data()
		
	# def process_data(self):
		
		# datasets = []
		# for folder in self.all_data['folders']:
			# for serv in folder['services']:
			
				# # Get the service info to add to the layer
				# serv_url = serv['url']
				# serv_name = serv['documentInfo']['Title']
				
				# mdata_url = serv['metadata']
				# query_formats = serv['supportedQueryFormats']
				# extensions = serv['supportedExtensions']
				
				# formats = query_formats.split(', ') + extensions.split(', ')
				# if len(formats) == 0:
					# downloads = 'No'
					# access = 'Viewable/Contact the Province'
				# #elif len(formats) == 1:
				# #	downloads = 'Multiple Downloads'
				# #	access = 'Download using ESRI REST Service'
				# else:
					# downloads = 'Multiple Downloads'
					# access = 'Download using ESRI REST Service'
			
				# for lyr_idx, lyr in enumerate(serv['layers']):
				
					# msg = "Extracting %s of %s layers" % \
							# (lyr_idx + 1, len(lyr))
					# shared.print_oneliner(msg)
				
					# title_str = lyr['name']
					# desc_str = lyr['description']
					# type_str = lyr['type']
					# lyr_url = lyr['url']
					
					# proj_str = shared.get_spatialref(lyr)
					
					# date_str = ''
				
					# data_dict = collections.OrderedDict()
					# # Add the results in the data_dict
					# data_dict['Source'] = 'Map Services'
					# data_dict['Title'] = title_str
					# if not desc_str == '': data_dict['Description'] = desc_str
					# data_dict['Type'] = type_str
					# if not date_str == '': data_dict['Recent Date'] = date_str
					# data_dict['Data URL'] = lyr_url
					# data_dict['Access'] = access
					# data_dict['Service'] = 'ESRI REST'
					# data_dict['Service Name'] = serv_name
					# data_dict['Service URL'] = serv_url
					# data_dict['Available Formats'] = "|".join(formats)
					# data_dict['Spatial Reference'] = proj_str
					# data_dict['Metadata URL'] = mdata_url
					# data_dict['Download'] = downloads
					
					# #print data_dict
					
					# datasets.append(data_dict)
					
					# #answer = raw_input("Press enter...")
					
				# print
				
		# return datasets
		
	def get_data(self):
		return self.all_data
		
	def get_layers(self):
		''' Gets all the unique layers from the services by
			merging similar layers together
		'''
		
		# Get a list of all layers
		layers = []
		for serv in self.all_data['services']:
			layers += serv['layers']
		
		if not self.silent:		
			print "Number of layers: %s" % len(layers)
		
		return layers
		
	def get_lyr_data(self, lyr_info, serv_info):
		''' Gets the layer data for a specified layer
		'''
	
		lyr_name = lyr_info['name']
		lyr_id = lyr_info['id']
		lyr_path = "%s/%s" % (serv_info['url'], lyr_id)
		
		lyr_query = "%s?f=pjson" % lyr_path
		#print lyr_query
		lyr_json = shared.get_json(lyr_query)
		
		#print lyr_json
		#answer = raw_input("Press enter...")
		
		# Get the information from the service info
		# Get the downloads and access
		formats = serv_info['formats']
		if len(formats) == 0:
			downloads = 'No'
			access = 'Viewable/Contact the Province'
		#elif len(formats) == 1:
		#	downloads = 'Multiple Downloads'
		#	access = 'Download using ESRI REST Service'
		else:
			downloads = 'Multiple Downloads'
			access = 'Download using ESRI REST Service'
		
		# Get the service information
		serv_name = serv_info['title']
		serv_url = serv_info['url']
		mdata_url = serv_info['metadata']
		
		# Get the keywords
		keywords = ''
		if 'documentInfo' in serv_info:
			keywords = serv_info['documentInfo']['Keywords']
		
		# Get the dates
		date_str = ''
		if 'editingInfo' in serv_info:
			edit_info = serv_info['editingInfo']
			if 'lastEditDate' in edit_info:
				date_str = edit_info['lastEditDate']
		else:
			# Get date from URL
			date = re.search(r'\d{4}\d{2}\d{2}', lyr_query)
			if date is not None:
				date_str = date.group()[0]
		
		xml_mdata = bsoup.xml_to_dict(mdata_url, silent=True)
		
		if xml_mdata is not None:
			startdate_str = ''
			if 'metadata' in xml_mdata:
				if 'Esri' in xml_mdata['metadata']:
					esri = xml_mdata['metadata']['Esri']
					if 'CreaDate' in esri:
						startdate_str = esri['CreaDate']
				
		# Get publisher/author
		publish_str = ''
		if 'documentInfo' in serv_info:
			publish_str = serv_info['documentInfo']['Author']
		
		#print
		#print "Date: '%s'" % date_str
		#answer = raw_input("Press enter...")
		
		# Get extents
		exts_dict = serv_info['fullExtent']
		west = exts_dict['xmin']
		east = exts_dict['xmax']
		north = exts_dict['ymax']
		south = exts_dict['ymin']
		
		ext_lst = [north, south, east, west]
		
		wkt_text = ''
		sp = exts_dict['spatialReference']
		#answer = raw_input("Press enter...")
		if 'latestWkid' in sp:
			epsg = sp['latestWkid']
			wkt_text = shared.create_wkt_extents(ext_lst, epsg)
		elif 'wkt' in sp:
			wkt_sp = sp['wkt']
			wkt_text = shared.create_wkt_extents(ext_lst, in_wkt=wkt_sp)
		#print "\nwkt_text: %s" % wkt_text
		
		out_lyr = collections.OrderedDict()
		if lyr_json is None or 'err' in lyr_json:
			
			out_lyr['Source'] = 'Map Services'
			out_lyr['Title'] = 'ERROR (see notes)'
			out_lyr['Description'] = ''
			out_lyr['Data URL'] = lyr_query
			out_lyr['Start Date'] = startdate_str
			out_lyr['Recent Date'] = date_str
			out_lyr['Extents'] = wkt_text
			out_lyr['Keywords'] = keywords
			out_lyr['Access'] = access
			out_lyr['Service'] = 'ESRI REST'
			out_lyr['Service Name'] = serv_name
			out_lyr['Service URL'] = serv_url
			out_lyr['Metadata URL'] = mdata_url
			out_lyr['Download'] = downloads
			out_lyr['Notes'] = 'Timeout Occurred when loading this layer.'
			
			return out_lyr
		
		#out_lyr = lyr_json
		#out_lyr['url'] = lyr_path
		
		# Get the layer information
		title_str = lyr_json['name']
		if serv_name.find('.') > -1: srv_title = serv_name.split('.')[0]
		else: srv_title = serv_name
		title_str = "%s - %s" % (srv_title, title_str)
		desc_str = lyr_json['description']
		type_str = lyr_json['type']
		
		proj_str = shared.get_spatialref(lyr_json)
		
		out_lyr['Source'] = 'Map Services'
		out_lyr['Title'] = title_str
		out_lyr['Description'] = desc_str
		out_lyr['Publisher'] = publish_str
		out_lyr['Type'] = type_str
		out_lyr['Recent Date'] = date_str
		out_lyr['Extents'] = wkt_text
		out_lyr['Keywords'] = keywords
		out_lyr['Data URL'] = lyr_query
		out_lyr['Access'] = access
		out_lyr['Service'] = 'ESRI REST'
		out_lyr['Service Name'] = serv_name
		out_lyr['Service URL'] = serv_url
		out_lyr['Available Formats'] = "|".join(formats)
		out_lyr['Spatial Reference'] = proj_str
		out_lyr['Metadata URL'] = mdata_url
		out_lyr['Download'] = downloads
		
		return out_lyr
		
	def get_serv_data(self, serv_info):
		''' Gets the service data for a specified service
		'''
		
		if 'type' in serv_info and 'name' in serv_info:
			serv_type = serv_info['type']
			serv_name = serv_info['name']
			serv_path = "%s/%s/%s" % (self.root_url, serv_name, serv_type)
		else:
			serv_path = self.root_url
			serv_name = self.root_url
		
		# Extract date from name
		serv_parse = serv_name.split('/')
		date = serv_parse[len(serv_parse) - 1]
		#print date
		#answer = raw_input("Press enter...")
		date_str = ''
		if date.isdigit():
			if len(str(int(date))) == 8:
				date_str = date
		
		serv_query = "%s?f=pjson" % serv_path
		serv_json = shared.get_json(serv_query)
		
		if serv_json is None:
			out_serv = collections.OrderedDict()
			out_serv['notes'] = 'Timeout Occurred when loading this layer.'
			out_serv['url'] = lyr_path
			return out_lyr
		
		out_serv = serv_json
		out_serv['url'] = serv_path
		out_serv['metadata'] = "%s/info/metadata" % serv_path
		out_serv['name'] = serv_name
		if 'date' not in out_serv:
			# If 'date' not in out_serv, check in metadata
			mdata_date = ''
			mdata_xml = bsoup.get_xml_soup(out_serv['metadata'])
			if not isinstance(mdata_xml, dict): 
				#print mdata_xml
				mdata = mdata_xml.find('metadata')
				if mdata is not None:
					esri = mdata.find('Esri')
					if esri is not None:
						mdata_date = bsoup.get_text(esri.find('CreaDate'))
			if mdata_date == '':
				out_serv['date'] = date_str
			else:
				out_serv['date'] = mdata_date
		else:
			if not date_str == '':
				out_serv['date'] = date_str
		if 'documentInfo' in serv_json:
			out_serv['title'] = serv_json['documentInfo']['Title']
		else:
			out_serv['title'] = serv_name
			
		if out_serv['title'] == '':
			# Get the service name from the URL
			url_split = serv_path.split('/')
			out_serv['title'] = url_split[len(url_split) - 2].replace('_', ' ')
			
			#print out_serv['title']
			#answer = raw_input("Press enter...")
		
		# if out_serv['title'] == 'cha': #serv_name.find('cha') > -1:
			# print "date: '%s'" % date_str
			# print "out_serv['date']: '%s'" % out_serv['date']
			# answer = raw_input("Press enter...")
		
		#print serv_json
		formats = []
		if 'supportedQueryFormats' in serv_json:
			query_formats = serv_json['supportedQueryFormats']
		else:
			query_formats = ''
			
		if 'supportedExtensions' in serv_json:
			extensions = serv_json['supportedExtensions']
		else:
			extensions = ''
		
			formats = query_formats.split(', ') + extensions.split(', ')
			
		out_serv['formats'] = [f for f in formats if not f == '']
		
		layers = []
		if 'layers' in serv_json:
			for idx, lyr in enumerate(serv_json['layers']):
				if 'subLayerIds' in lyr:
					if lyr['subLayerIds'] is not None:
						continue
				
				if not self.silent:
					msg = "Getting %s of %s layers for '%s'" \
							% (idx + 1, len(serv_json['layers']), serv_name)
					shared.print_oneliner(msg)
			
				# Ignore group layers
				lyr_data = self.get_lyr_data(lyr, out_serv)
				
				layers.append(lyr_data)
			
			if not self.silent:
				print
					
		out_serv['layers'] = layers
		
		return out_serv
		
	def get_root_json(self):
		''' Gets the home JSON dictionary of the REST service.
		:return: The JSON dictionary of the home page of the REST service.
		'''
		return self.root_json
		
	def print_data(self):
	
		r = json.dumps(self.all_data)
		loaded_r = json.loads(r)
	
		with open("serv_test.json", "w") as d_file:
			json.dump(loaded_r, d_file, indent=4, sort_keys=True)
			
		out_f = open('dates.txt', 'w')
		for d in self.all_data['services']:
			out_f.write('%s: %s\n' % (d['name'], d['date']))
			
		out_f.close()
	
class PT_WMS:
	def __init__(self, wms_url, silent=False):
		self.root_url = wms_url
		self.silent = silent
		#self.xml_soup = bsoup.get_xml_soup(self.root_url, selenium=True)
		#self.xml_dict = bsoup.xml_to_dict(self.root_url, selenium=True)
		self.xml_dict = bsoup.xml_to_dict(self.root_url)
		
		# FOR DEBUG ONLY
		out_fn = 'wms_test.txt'
		if self.root_url.find('tools.pacificclimate.org') > -1 and \
			not os.path.exists(out_fn):
			print "Creating '%s'..." % out_fn
			out_json = json.dumps(self.xml_dict)
			out_f = open(out_fn, 'w')
			json.dump(out_json, out_f, indent=4)
			out_f.close()
		
		self.all_data = collections.OrderedDict()
		
		self.extract_data()
		
	def get_layers(self, in_lyr, lyrs=[], title=''):
	
		# If the current layer is a group layer, go into its sub-layers
		if 'Layer' in in_lyr:
			lyr_title = in_lyr['Title']
			if not lyr_title == self.serv_name:
				if title == '':
					full_title = lyr_title
				else:
					full_title = '%s|%s' % (title, lyr_title)
			else:
				full_title = ''
			if isinstance(in_lyr['Layer'], list):
				cur_lyrs = in_lyr['Layer']
			else:
				cur_lyrs = [in_lyr['Layer']]
			
			for lyr in cur_lyrs:
				lyr['Parent Title'] = full_title
				lyrs = self.get_layers(lyr, lyrs, full_title)
		else:
			lyrs.append(in_lyr)
			
		return lyrs
		
		# print level
		# level += 1
		
		# if isinstance(in_lyr, list):
			# for lyr in in_lyr:
				# if '@queryable' in lyr or '@opaque' in lyr:
					# lyrs.append(lyr)
			
				# if 'Layer' in lyr:
					# lyrs = self.get_layer(lyr['Layer'], lyrs, level=level)
		# else:
			# if '@queryable' in in_lyr or '@opaque' in in_lyr:
				# lyrs.append(in_lyr)
		
			# if 'Layer' in in_lyr:
				# lyrs = self.get_layer(in_lyr['Layer'], lyrs, level=level)

		# return lyrs
		
	def extract_data(self):
	
		if self.xml_dict is None:
			print "\nWARNING: WMS '%s' could not be opened." % self.root_url
			print "Please check the 'err_log.csv' file in the province/territory results folder."
			self.write_error(self.root_url, 'WMS', 'Page could not be opened.')
			return None
			
		if not self.silent:
			print "\nExtracting data for '%s'" % self.root_url
		
		if 'ows:ExceptionReport' in self.xml_dict.keys() or \
			'err' in self.xml_dict.keys() or \
			'ServiceExceptionReport' in self.xml_dict.keys():
			return None
		
		# Get the service info
		if 'WMT_MS_Capabilities' in self.xml_dict.keys():
			wms_capab = self.xml_dict['WMT_MS_Capabilities']
		else:
			wms_capab = self.xml_dict['WMS_Capabilities']
		service_info = wms_capab['Service']

		# Get the type of service
		#serv_type = bsoup.find_xml_text(self.xml_soup, 'Name')
		serv_type = service_info['Name']

		# Get the service name
		#serv_name = bsoup.find_xml_text(self.xml_soup, 'Title')
		self.serv_name = service_info['Title']
		
		
		# Get the description name
		#serv_desc = bsoup.find_xml_text(self.xml_soup, 'Abstract')
		serv_desc = ''
		if 'Abstract' in service_info:
			serv_desc = service_info['Abstract']

		# Get the publisher
		#pub_str = bsoup.find_xml_text(self.xml_soup, 'ContactOrganization')
		pub_str = service_info['ContactInformation']['ContactPersonPrimary']\
					['ContactOrganization']
		
		# Get the keywords of the service
		keywords = ''
		if 'KeywordList' in service_info:
			keywords = service_info['KeywordList']['Keyword']
			
		if isinstance(keywords, list):
			keywords = ', '.join(keywords)
			
		#print keywords
			
		# Get the date if applicable
		date = ''
		if '@updateSequence' in wms_capab:
			date = wms_capab['@updateSequence']
		if date == '0': date = ''
		
		# Add the data to the self.all_data
		self.all_data['type'] = serv_type
		self.all_data['name'] = self.serv_name
		self.all_data['description'] = serv_desc
		self.all_data['date'] = date
		self.all_data['publisher'] = pub_str
		self.all_data['keywords'] = keywords

		# To get the layer information, get the 'Capability' item
		capability = wms_capab['Capability']

		# Get all the layers
		#layers = bsoup.find_xml_tags(self.xml_soup, ['Layer'], attrs, True)[0]
		
		layers = self.get_layers(capability['Layer'], [])
		
		out_lyrs = []
		lyr_idx = 0
		if len(layers) > 0:
			for lyr_idx, lyr in enumerate(layers):
				#print bsoup.get_text(lyr.find('name'))
				
				if not self.silent:
					msg = "Adding layer %s of %s layers to CSV inventory" % \
							(lyr_idx + 1, len(layers))
					shared.print_oneliner(msg)
				
				data_dict = collections.OrderedDict()

				title = lyr['Title']
				title_str = '%s|%s' % (lyr['Parent Title'], title)
				
				desc_str = serv_desc
				#print "\nDescription: %s" % desc_str
				if 'Abstract' in lyr:
					desc_str = lyr['Abstract']
					#print "Description: %s" % desc_str
				
				#if self.root_url.find('tools.pacificclimate.org') > -1:
				#	answer = raw_input("Press enter...")
				
				# Get the extents
				if 'EX_GeographicBoundingBox' in lyr:
					exts_dict = lyr['EX_GeographicBoundingBox']
					west = exts_dict['westBoundLongitude']
					east = exts_dict['eastBoundLongitude']
					north = exts_dict['southBoundLatitude']
					south = exts_dict['northBoundLatitude']
				elif 'LatLonBoundingBox' in lyr:
					exts_dict = lyr['LatLonBoundingBox']
					west = exts_dict['@minx']
					east = exts_dict['@maxx']
					north = exts_dict['@maxy']
					south = exts_dict['@miny'] 
				
				ext_lst = [north, south, east, west]
				wkt_text = shared.create_wkt_extents(ext_lst)
				
				# FOR DEBUG ONLY
				# if title_str.lower().find('black and white') > -1:
					# print "\nTitle: %s" % title_str
					# if title_str.find('/') > -1:
						# fn_title = title_str.split('/')[1]
					# else:
						# fn_title = title_str
					# with open('%s.json' % fn_title, 'w') as fp:
						# json.dump(capability, fp)
					# print "Number of layers: %s" % len(layers)
					#answer = raw_input("Press enter...")
					
				# Add all values to the CSV file object
				#data_dict['Source'] = 'BC Map Services'
				data_dict['Title'] = title_str
				data_dict['Description'] = desc_str
				data_dict['Start Date'] = date
				data_dict['Publisher'] = pub_str
				data_dict['Keywords'] = keywords
				data_dict['Extents'] = wkt_text
				data_dict['Spatial Reference'] = 'Multiple'
				data_dict['Type'] = 'WMS'
				data_dict['Service'] = serv_type
				data_dict['Service Name'] = self.serv_name
				data_dict['Service URL'] = self.root_url
				data_dict['Download'] = 'No'
				data_dict['Access'] = 'Contact the Province'
				
				out_lyrs.append(data_dict)
			
			if not self.silent:	
				print
			
		self.all_data['layers'] = out_lyrs
		
		# out_lyrs = []
		# if len(layers) > 0:
			# for lyr_idx, lyr in enumerate(layers):
				# #print bsoup.get_text(lyr.find('name'))
				
				# msg = "Adding layer %s of %s layers to CSV inventory" % (lyr_idx + 1, len(layers))
				# shared.print_oneliner(msg)
				
				# data_dict = collections.OrderedDict()

				# title_str = bsoup.find_xml_text(lyr, 'Title')
				
				# desc_str = bsoup.find_xml_text(lyr, 'Abstract')
				
				# # Get the extents
				# exts = bsoup.find_xml_tags(lyr, ['EX_GeographicBoundingBox'])
				
				# print exts
				
				# #if len(exts) > 0:
				# west = bsoup.find_xml_text(exts[0], 'westBoundLongitude')
				# east = bsoup.find_xml_text(exts[0], 'eastBoundLongitude')
				# south = bsoup.find_xml_text(exts[0], 'southBoundLatitude')
				# north = bsoup.find_xml_text(exts[0], 'northBoundLatitude')
				
				# ext_lst = [north, south, east, west]
				# wkt_text = shared.create_wkt_extents(ext_lst)
					
				# # Add all values to the CSV file object
				# #data_dict['Source'] = 'BC Map Services'
				# data_dict['Title'] = title_str
				# data_dict['Description'] = serv_desc
				# data_dict['Publisher'] = pub_str
				# data_dict['Extents'] = wkt_text
				# data_dict['Spatial Reference'] = 'Multiple'
				# data_dict['Type'] = 'WMS'
				# data_dict['Service'] = serv_type
				# data_dict['Service Name'] = serv_name
				# data_dict['Service URL'] = self.root_url
				# data_dict['Download'] = 'No'
				# data_dict['Access'] = 'Contact the Province'
				
				# out_lyrs.append(data_dict)
				
			# print
			
		# self.all_data['layers'] = out_lyrs
				
	def get_data(self):
		return self.all_data
		
	# def get_layers(self):
		# ''' Gets all the unique layers from the services by
			# merging similar layers together
		# '''
		
		# # Get a list of all layers
		# layers = []
		# #for serv in self.all_data['services']:
		# #	layers += serv['layers']
			
		# print "Number of layers: %s" % len(layers)
		
		# return layers			

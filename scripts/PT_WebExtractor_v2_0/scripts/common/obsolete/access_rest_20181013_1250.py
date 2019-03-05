import codecs
import json
import os
import sys
import urllib2
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

class MyGeocortex:
	def __init__(self, root_url, prefix=None):
		self.root_url = root_url
		self.root_query = "%s?f=pjson" % self.root_url
		# print "#1"
		self.root_json = shared.get_json(self.root_query)
		self.prefix = prefix

	def get_data(self):
		''' Gets the data for the GeoCortex Services
		:return: A list of data as dictionaries.
		'''

		# Get a list of services
		print("\nGetting the Geocortex sites for '%s'..." % self.root_url)
		sites = self.get_sites()
		
		if sites is None: return None

		data_list = []

		# Cycle through each service
		print("\nGetting the data for Geocortex sites for '%s'..." \
				% self.root_url)
		for site_idx, site in enumerate(sites):
		
			print "Getting site %s of %s for '%s'" % (site_idx + 1, 
					len(sites), self.root_url)
			
			if site == 'error':
				err_dict = collections.OrderedDict()
				err_dict['err'] = "Site could not be accessed."
				return err_dict
		
			# If the site contains a key with 'err', add the result
			#   to the CSV with a note 'Service could not be loaded.'
			if 'error' in site:
				#print "\nsite: %s" % site
			
				data_dict = collections.OrderedDict()

				if self.prefix is None:
					data_dict['Title'] = site['name']
				else:
					data_dict['Title'] = "%s - %s" % (self.prefix, site['name'])
				data_dict['Type'] = "Geocortex Essentials REST API"
				data_dict['Web Service URL'] = site['url']
				if site['error']['code'] == 403:
					data_dict['Access'] = 'Login Required/Contact the Territory'
				data_dict['Service'] = 'Geocortex Essentials REST'
				data_dict['Service URL'] = self.root_url
				data_dict['Download'] = 'No'

				data_list.append(data_dict)

				continue

			#print site['url']

			# Get site info
			site_name = site['name']
			#site_type = site['type']
			site_url = site['url']

			# Get the description
			desc_str = site['description']

			# Load the map page to get a list of layers
			map_url = site_url + "/map?f=pjson"
			map_json = shared.get_json(map_url)

			# Get the layers
			map_services = map_json['mapServices']

			for map_serv in map_services:
				layers = map_serv['layers']

				for idx, lyr in enumerate(layers):
					msg = "Getting %s of %s layers" % (idx + 1, 
							len(layers))
					shared.print_oneliner(msg)
				
					data_dict = collections.OrderedDict()
					
					lyr_name = lyr['displayName']
					lyr_name = lyr_name.replace('_', ' ')
					lyr_name = shared.clean_text(lyr_name)

					# Get the title of the layer
					if self.prefix is None:
						title_str = lyr_name
					else:
						title_str = "%s - %s" % (self.prefix, lyr_name)

					# Get the spatial reference
					sp_str = shared.get_spatialref(lyr)

					type_str = lyr['type']

					# Add the results in the data_dict
					data_dict['Title'] = title_str
					data_dict['Description'] = desc_str
					data_dict['Type'] = type_str
					data_dict['Service URL'] = site_url
					data_dict['Access'] = 'Contact the Province'
					data_dict['Service Name'] = site_name
					data_dict['Service URL'] = site_url
					data_dict['Spatial Reference'] = sp_str
					data_dict['Service'] = 'GeoCortex'
					data_dict['Download'] = 'No'

					# Write the results to the data_list
					data_list.append(data_dict)

					continue

				print
					
		return data_list

	def get_site_json(self, site_json):
		''' Gets the JSON for a site from a list of sites in an initial JSON page.
		:param site_json: The initial JSON page containing a list of sites.
		:return: The JSON of the site.
		'''

		#print "site_json: %s" % site_json
		#answer = raw_input("Press enter...")

		# Get the site name and ID
		site_name = site_json['displayName']
		id = site_json['id']

		# Add the name to the root URL to get the site URL
		url = "%s/%s" % (self.root_url, id)

		# Get the JSON URL of the site
		json_url = "%s?f=pjson" % url

		# Get the JSON
		site_json = shared.get_json(json_url)
		if site_json is not None:
			# Add the URL and Name to the site JSON text
			site_json['url'] = url
			site_name = site_name.split("/")
			site_json['name'] = site_name[len(site_name) - 1].replace("_", " ")

			return site_json

	def get_sites(self, url=None, json=None):
		''' Gets all the JSON text for all the sites under a Geocortex Service page
		:param url: The root URL
		:param json: The root JSON format
		:return: A list of JSON formatted sites.
		'''

		if url is None: url = self.root_url
		if json is None: json = self.root_json

		sites = []
		
		if json is None: return None
		
		if 'err' in json or 'error' in json: return json

		sites_json = json['sites']
		for idx, site in enumerate(sites_json):
			site_name = site_json['displayName']
			print "Adding %s of %s sites to list for '%s'" \
					% (idx + 1, len(sites_json), site_name)
		
			sites.append(self.get_site_json(site))
			
		print

		if 'folders' in json:
			folders = json['folders']

			for folder in folders:
				sub_query = "%s/%s?f=pjson" % (url, folder)
				sub_json = shared.get_json(sub_query)
				if sub_json is not None:
					sites += self.get_sites(url, sub_json)

		return sites

class MyREST:
	def __init__(self, root_url, prefix=None):
		self.root_url = root_url
		self.root_query = "%s?f=pjson" % self.root_url
		self.root_json = shared.get_json(self.root_query)
		self.prefix = prefix
		
	def get_service_data(self, service):
					
		data_list = []

		# If the service contains a key with 'err', add the result
		#   to the CSV with a note 'Service could not be loaded.'
		if isinstance(service, str):
			data_dict = collections.OrderedDict()
			
			#print "service: %s" % service

			if self.prefix is None:
				data_dict['Title'] = service['name']
			else:
				data_dict['Title'] = "%s - %s" % (self.prefix, service['name'])
			data_dict['Service Name'] = service['name']
			data_dict['Service URL'] = service['url']
			data_dict['Notes'] = 'Service could not be loaded.'

			data_list.append(data_dict)

			return data_list
		else:
			if 'err' in service:
				data_dict = collections.OrderedDict()

				if self.prefix is None:
					data_dict['Title'] = service['name']
				else:
					data_dict['Title'] = "%s - %s" % (self.prefix, service['name'])
				data_dict['Service Name'] = service['name']
				data_dict['Service URL'] = service['url']
				data_dict['Notes'] = 'Service could not be loaded.'

				data_list.append(data_dict)

				return data_list

		serv_name = service['name']
		serv_name = serv_name.replace('_', ' ')
		serv_name = shared.clean_text(serv_name)

		if serv_name.find("Latest") == -1:

			# The latest service is the same as the most recent
			#	dated service so it doesn't need to be included

			serv_type = service['type']
			serv_url = service['url']

			# Get the metadata
			mdata_url = "%s/info/metadata" % serv_url

			mdata_info = self.get_metadata(mdata_url)

			# If the service is a standard map server, the following
			#   formats can be extract
			if serv_type.lower() == 'mapserver':
				formats = ['KMZ', 'LYR', 'NMF', 'AMF']
				downloads = 'Multiple Downloads'
				access = 'Download/Web Accessible'
			elif serv_type.lower() == 'imageserver':
				formats = ['KMZ', 'LYR']
				downloads = 'Multiple Downloads'
				access = 'Download using ESRI REST Service'
			else:
				formats = ''
				downloads = 'No'
				access = 'Viewable/Contact the Province'

			# Get the author/publisher
			#author_str = ''
			#if 'documentInfo' in service:
			#    doc_info = service['documentInfo']
			#
			#    if 'Author' in doc_info:
			#        author_str = doc_info['Author']

			# Extract date from name
			serv_parse = serv_url.split('/')
			date = serv_parse[len(serv_parse) - 2]
			date_str = ''
			if date_str.isdigit():
				if len(str(int(date))) == 8:
					date_str = date

			# Get the spatial reference
			proj_str = shared.get_spatialref(service)

			if 'layers' not in service:
				# If the service has no layers, include instead the service
				#   in the CSV

				data_dict = collections.OrderedDict()

				# Set the info from the metadata
				if mdata_info is not None:
					for k, v in mdata_info.items():
						data_dict[k] = v

				# Get the title
				if self.prefix is None:
					title_str = serv_name
				else:
					title_str = "%s - %s" % (self.prefix, serv_name)

				# Get the description
				desc_str = ''
				if 'description' in service:
					desc_str = service['description']

				if desc_str == '':
					if 'serviceDescription' in service:
						desc_str = service['serviceDescription']

				desc_str = shared.edit_description(desc_str, 'span')

				# Get the spatial reference
				if proj_str == '':
					proj_str = shared.get_spatialref(service)

				# Add the results in the data_dict
				data_dict['Title'] = title_str
				if not desc_str == '': data_dict['Description'] = desc_str
				data_dict['Type'] = serv_type
				if not date_str == '': data_dict['Date'] = date_str
				data_dict['Service URL'] = serv_url
				data_dict['Access'] = access
				data_dict['Service Name'] = serv_name
				data_dict['Available Formats'] = "|".join(formats)
				data_dict['Spatial Reference'] = proj_str
				if mdata_info is not None: data_dict['Metadata URL'] = mdata_url
				data_dict['Service'] = 'ESRI REST'
				data_dict['Download'] = downloads

				# Write the results to the data_list
				data_list.append(data_dict)

				return data_list

			layers = service['layers']
			for idx, lyr in enumerate(layers):
			
				msg = "Getting layer %s of %s for '%s'" \
						% (idx + 1, len(layers), self.root_url)
				shared.print_oneliner(msg)

				data_dict = collections.OrderedDict()

				# Set the info from the metadata
				if mdata_info is not None:
					for k, v in mdata_info.items():
						data_dict[k] = v
				
				if 'err' in lyr.keys():
					data_list.append(data_dict)
					continue

				# Get the layer ID
				lyr_id = lyr['id']

				# Get the layer URL
				if 'url' in lyr:
					lyr_url = lyr['url']
				else:
					lyr_url = "%s/%s" % (serv_url, lyr_id)

				lyr_json = shared.get_json(lyr_url + "?f=pjson")

				if lyr_json is None:
					lyr_json = lyr
					lyr_json['notes'] = 'Timeout Occurred when loading this layer.'
					lyr_json['url'] = lyr_url

				# Get the title string
				if 'name' in lyr_json:
					lyr_name = lyr_json['name']
					lyr_name = lyr_name.replace('_', ' ')
					lyr_name = shared.clean_text(lyr_name)
					title_str = shared.split_upper(lyr_name)
				else:
					title_str = shared.split_upper(serv_name)
				
				# Get the parent layer name, if applicable
				if 'parentLayer' in lyr_json and lyr_json['parentLayer'] is not None:
					#print lyr_json
					parent_name = lyr_json['parentLayer']['name']
					title_str = "%s: %s" % (parent_name, title_str)
					
				if self.prefix is not None:
					title_str = "%s - %s" % (self.prefix, title_str)	

				# Get the service type
				lyr_type = ''
				if 'type' in lyr_json:
					lyr_type = lyr_json['type']

				# Get the description
				desc_str = ''
				if 'description' in lyr_json:
					desc_str = lyr_json['description']
					desc_str = shared.edit_description(desc_str, 'span')

				# Get the spatial reference
				if proj_str == '':
					proj_str = shared.get_spatialref(service)

				# Add the results in the data_dict
				data_dict['Title'] = title_str
				if not desc_str == '': data_dict['Description'] = desc_str
				data_dict['Type'] = lyr_type
				if not date_str == '': data_dict['Date'] = date_str
				data_dict['Service URL'] = serv_url
				data_dict['Data URL'] = lyr_url
				data_dict['Access'] = access
				data_dict['Service Name'] = serv_name
				data_dict['Available Formats'] = "|".join(formats)
				data_dict['Spatial Reference'] = proj_str
				data_dict['Service'] = 'ESRI REST'
				if mdata_info is not None: data_dict['Metadata URL'] = mdata_url
				data_dict['Download'] = downloads

				# Write the results to the data_list
				data_list.append(data_dict)
	
			print
			
		return data_list

	def get_data(self):
		''' Gets the data for the ESRI REST Services
		:return: A list of data as dictionaries.
		'''

		# Get a list of services
		print("\nDetermining the number of ArcGIS REST services for '%s'..." \
				% self.root_url)
				
		serv_data = self.get_services()
		
		return serv_data

	def get_metadata(self, mdata_url):
		''' Gets the metadata for a specific service.
		:param service: The service to extract the metadata from.
		:return: A dictionary of the metadata.
		'''

		# Get the XML metadata
		mdata_xml = bsoup.get_xml_soup(mdata_url)
		
		if mdata_xml is None:
			print "Metadata '%s' page could not be loaded." % mdata_url
			return None

		if mdata_xml.find('html') is not None: return None

		mdata_dict = collections.OrderedDict()

		# Get the description, if applicable
		abstract = mdata_xml.find('idAbs')
		if abstract is not None: mdata_dict['Description'] = shared.edit_description(abstract.text)

		# Get the date, if applicable
		date = mdata_xml.find('CreaDate')
		if date is not None: mdata_dict['Date'] = bsoup.get_text(date)

		# Get the publisher, if applicable
		publisher = mdata_xml.find('idCredit')
		if publisher is not None: mdata_dict['Publisher'] = bsoup.get_text(publisher)

		return mdata_dict

	def get_root_json(self):
		''' Gets the home JSON dictionary of the REST service.
		:return: The JSON dictionary of the home page of the REST service.
		'''
		return self.root_json

	def get_service_json(self, url, serv_json=None):
		''' Gets the map service in JSON format.
		:param url: The home URL of the ESRI REST Service.
		:param serv_json: The JSON of the ESRI REST Service.
		:return: The service in JSON format.
		'''

		# If the serv_json is not specified, use the self.root_json
		if serv_json is None: serv_json = self.root_json

		# Get the basename of the service name
		serv_bn = serv_json['name']

		# Parse the service basename into the date, service name
		#  Ex: ABWRET-Relative_Wetland_Value_Estimator_By_Section/20150710
		date = ''
		if serv_bn.find("/") > -1:
			serv_name = serv_bn.split("/")[1]
			if serv_name.isdigit():
				date = serv_bn.split("/")[1]
				serv_name = serv_bn.split("/")[0]
		else:
			serv_name = serv_bn

		# Build the service URL JSON link
		serv_type = serv_json['type']
		if date == '':
			serv_url = "%s/%s/%s" % (url, serv_name, serv_type)
		else:
			serv_url = "%s/%s/%s" % (url, date, serv_type)
		json_url = "%s?f=pjson" % serv_url
		#print json_url
		serv_json = shared.get_json(json_url)

		# If the serv_json is None, the URL is broken
		if serv_json is None:
			err_dict = collections.OrderedDict()
			err_dict['name'] = serv_name
			err_dict['url'] = json_url
			err_dict['err'] = 'Error accessing server.'

			return err_dict
			
		if 'err' in serv_json.keys():
			err_dict = collections.OrderedDict()
			err_dict['name'] = serv_name
			err_dict['url'] = json_url
			err_dict['err'] = serv_json['err']

			return err_dict

		# Add some extra information to the service JSON
		serv_json['url'] = serv_url
		serv_name = serv_name.split("/")
		serv_json['name'] = serv_name[len(serv_name) - 1].replace("_", " ")
		serv_json['type'] = serv_type

		# Get the layer JSONs of the service
		#print serv_json
		if 'layers' in serv_json:
			layers = serv_json['layers']
			out_layers = []
			for idx, lyr in enumerate(layers):
				msg = "Adding %s of %s layers to list" \
							% (idx + 1, len(layers))
				shared.print_oneliner(msg)
			
				#print "Layer Info:"
				#print lyr
				# Get the layer ID
				id = lyr['id']
				# Get the layer URL
				lyr_url = "%s/%s" % (serv_json['url'], id)
				# Get the layer JSON
				lyr_json_url = lyr_url + "?f=pjson"
				#print lyr_json_url
				lyr_json = shared.get_json(lyr_json_url)

				if lyr_json is None:
					lyr_json = lyr
					lyr_json['notes'] = 'Timeout Occurred when loading this layer.'
					lyr_json['url'] = lyr_url
				else:
					lyr_json['url'] = lyr_url

				out_layers.append(lyr_json)

			print
			
			serv_json['layers'] = out_layers

		return serv_json

	def get_services(self, url=None, json=None):
		''' Gets all the services in a mapservice.
		:param url: The mapservice URL.
		:param json: The JSON text.
		:return: A list of JSON services.
		'''

		# Set the variables
		if url is None: url = self.root_url
		if json is None:
			if self.root_json is None:
				#err_msg = "ERROR|No JSON available."
				err_dict = collections.OrderedDict()
				err_dict['err'] = err_msg
				print("\n%s" % err_msg)
				return err_dict
			else:
				json = self.root_json

		services = []
		
		if 'services' not in json and url.find('MapServer') > -1:
			json['name'] = url.split('/')[6].replace("_", ' ')
			json['type'] = url.split('/')[7]
			json['url'] = url
			serv_data = self.get_service_data(json)
			services.append(serv_data)
			return services
			
		if 'err' in json: return json
		
		# Get the list of services from the server JSON
		servs_json = json['services']
		#print "services: " + str(servs_json)

		# Go through each service and add it to the services list
		for idx, serv in enumerate(servs_json):
			serv_name = serv['name']
			if serv_name.find('Latest') > -1: continue
			print "Adding %s of %s services to list for '%s'" \
					% (idx + 1, len(servs_json), serv_name)
			
			json_data = self.get_service_json(url, serv)
			serv_data = self.get_service_data(json_data)
			services.append(serv_data)
			
		# Cycle through all subfolders and call this function for any services
		#   which are found
		if 'folders' in json:
			folders = json['folders']

			if folders is not None:
				num_folders = len(folders)
				if num_folders > 0:
					print "Number of folders under '%s': %s" % (url, len(folders))
			
				for folder in folders:
					sub_url = '%s/%s' % (url, folder)
					sub_query = "%s/%s?f=pjson" % (url, folder)
					sub_json = shared.get_json(sub_query)
					services += self.get_services(sub_url, sub_json)

		return services

		# # If there are no services in the JSON, add it to the service list
		# if 'services' not in json and url.find('MapServer') > -1:
			# json['name'] = url.split('/')[6].replace("_", ' ')
			# json['type'] = url.split('/')[7]
			# json['url'] = url
			# services.append(json)
			# return services
			
		# if 'err' in json: return json

		
			
		# print

		# #print "number of services: " + str(len(services))

		# # Cycle through all subfolders and call this function for any services
		# #   which are found
		# if 'folders' in json:
			# folders = json['folders']

			# if folders is not None:
				# num_folders = len(folders)
				# if num_folders > 0:
					# print "Number of folders under '%s': %s" % (url, len(folders))
			
				# for folder in folders:
					# sub_url = '%s/%s' % (url, folder)
					# sub_query = "%s/%s?f=pjson" % (url, folder)
					# sub_json = shared.get_json(sub_query)
					# services += self.get_services(sub_url, sub_json)

		# return services
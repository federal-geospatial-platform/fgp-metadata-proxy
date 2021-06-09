import os
import sys
import urllib2
from bs4 import BeautifulSoup
import collections
import math
import csv
import json
import codecs
import re
import urlparse
import time
import datetime
import inspect
import argparse
import traceback

import Main_Extractor as main_ext

from common import shared
from common import bsoup
#from common import access_rest as rest
from common import services
#from common import page_group
from common import recurse_ftp as rec_ftp
from common import spreadsheet as sh

class PT_Extractor(main_ext.Extractor):
	''' The Extractor class contains all the tools and methods to extract geospatial datasets
			from the various web pages and services from British Columbia.
	'''

	def __init__(self):
		''' Initializer for the Extractor class. '''

		# Set the province
		self.province = 'BC'
		
		# Initialize the Main Extractor to use its variables
		main_ext.Extractor.__init__(self)
		
		# Create the page groups dictionary
		self.page_groups = []

		####################################################################
		# Create Catalogue page group
		
		cat_grp = main_ext.PageGroup('catalogue', "Open Data Catalogue")
		
		# Add arguments and options
		cat_grp.add_arg('word', title='Search Word')
		ds_arg = cat_grp.add_arg('ds_type', title='Dataset Type')
		ds_arg.add_opt('Dataset', ['dataset'], ['Dataset'])
		ds_arg.add_opt('Geographic Dataset', ['geographic'], ['Geographic'])
		ds_arg.add_opt('Application', ['application'], ['Application'])
		ds_arg.add_opt('Web Service/API', ['webservice', 'ws'], ['WebService'])
		
		# Add URLs
		cat_grp.add_url('catal_url', 'https://catalogue.data.gov.bc.ca/dataset')
		cat_grp.add_url('api_url', 'https://catalogue.data.gov.bc.ca/api/3')
		
		# Add to Extractor's page group list
		self.page_groups.append(cat_grp)
		
		
		####################################################################
		# Create ArcGIS Maps page group

		arc_grp = main_ext.PageGroup('arcgismaps', "ArcGIS Maps")
		
		# No arguments to add
		
		# Add URLs
		#arc_grp.add_url('group_url', 'https://governmentofbc.maps.arcgis.com/home/group.html?id=cf5aab3d795d41e282ceab3d6630bd43')
		arc_grp.add_url('gobc_url', 'https://governmentofbc.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=desc&sortField=modified')
		arc_grp.add_url('bcgov03_url', 'http://bcgov03.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title')
		
		# Add to Extractor's page group list
		self.page_groups.append(arc_grp)
		
		
		####################################################################
		# Create Environmental Interactive Maps page group

		# env_grp = main_ext.PageGroup('enviro_maps', "Environmental Interactive Maps")
		
		# # No arguments to add
		
		# # Add URLs
		# #env_grp.add_url('parks_url', ['http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=5859423305973444492',
		# #                         'http://www.env.gov.bc.ca/bcparks/explore'])
		# env_grp.add_url('parks_url', 'http://www.env.gov.bc.ca/bcparks/explore/map.html')
		# env_grp.add_url('ground_url', 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html')
		# #env_grp.add_url('soil_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/air-land-water/land/soil/soil-information-finder')
		# #env_grp.add_url('drought_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/drought-flooding-dikes-dams/drought-information')
		# #env_grp.add_url('flood_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/drought-flooding-dikes-dams/river-forecast-centre/current-water-levels-and-flood-forecast-modeling')
		# #env_grp.add_url('grmap_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells/aquifers/groundwater-observation-well-network/groundwater-level-data-interactive-map')
		# env_grp.add_url('water_url',
				   # 'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/real-time-water-data-reporting')
		# #env_grp.add_url('snow_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/snow-survey-data/automated-snow-weather-station-data')
		# env_grp.add_url('cdc_url',
				   # 'https://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/conservation-data-centre/explore-cdc-data/known-locations-of-species-and-ecosystems-at-risk/cdc-imap-theme')
		# env_grp.add_url('frog_url',
				   # 'http://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/wildlife/wildlife-conservation/amphibians-reptiles/frogwatching')
		# #env_grp.add_url('surface_url',
		# #           'http://www2.gov.bc.ca/gov/content/environment/research-monitoring-reporting/monitoring/tools-databases/surface-water-monitoring-sites')
		# env_grp.add_url('ecocat_url', 'https://www2.gov.bc.ca/gov/content/environment/research-monitoring-reporting/libraries-publication-catalogues/ecocat')
		# env_grp.add_url('forest_url', 'http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna')
		# env_grp.add_url('bcwater_url', 'http://www.bcwatertool.ca')
		# env_grp.add_url('climate_url', 'http://www.pacificclimate.org/data')
		# env_grp.add_url('eao_url', 'http://www.projects.eao.gov.bc.ca')
		
		# # Add to Extractor's page group list
		# self.page_groups.append(env_grp)
		
		
		####################################################################
		# Create FTP site page group

		ftp_grp = main_ext.PageGroup('ftp', "FTP datasets")
		
		# No arguments to add
		
		# Add URLs
		ftp_grp.add_url('ftp_url', 'ftp.geobc.gov.bc.ca')
		
		# Add to Extractor's page group list
		self.page_groups.append(ftp_grp)
		
		
		####################################################################
		# Create Interactive Maps page group
		
		maps_grp = main_ext.PageGroup('maps', "BC's Interactive Maps")
		
		# No arguments to add
		
		# Add URLs
		maps_grp.add_url('parks_url', 'http://www.env.gov.bc.ca/bcparks/explore/map.html')
		maps_grp.add_url('ground_url', 'http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html')
		maps_grp.add_url('water_url',
				   'http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/real-time-water-data-reporting')
		maps_grp.add_url('cdc_url',
				   'https://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/conservation-data-centre/explore-cdc-data/known-locations-of-species-and-ecosystems-at-risk/cdc-imap-theme')
		maps_grp.add_url('frog_url',
				   'http://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/wildlife/wildlife-conservation/amphibians-reptiles/frogwatching')
		maps_grp.add_url('ecocat_url', 'https://www2.gov.bc.ca/gov/content/environment/research-monitoring-reporting/libraries-publication-catalogues/ecocat')
		maps_grp.add_url('forest_url', 'http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna')
		maps_grp.add_url('bcwater_url', 'http://www.bcwatertool.ca')
		maps_grp.add_url('climate_url', 'http://www.pacificclimate.org/data')
		maps_grp.add_url('eao_url', 'http://www.projects.eao.gov.bc.ca')
		maps_grp.add_url('meat_url',
				   'https://www2.gov.bc.ca/gov/content/industry/agriculture-seafood/food-safety/meat-inspection-licensing')
		maps_grp.add_url('product_url',
				   'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/forest-inventory/site-productivity/provincial-site-productivity-layer')
		maps_grp.add_url('seedlot_url',
				   'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedlot-aou')
		maps_grp.add_url('seedmap_url',
				   'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedmap')
		maps_grp.add_url('iapp_url',
				   'https://www.for.gov.bc.ca/hra/plants/application.htm')
		maps_grp.add_url('mineral_url',
				   'http://www.mtonline.gov.bc.ca/mtov/home.do')
		maps_grp.add_url('stops_url',
				   'http://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/traveller-information/stop-of-interest')
		maps_grp.add_url('traffic_url',
				   'http://www.th.gov.bc.ca/trafficData/')
		maps_grp.add_url('elections_url', 'http://elections.bc.ca/resources/maps')
		maps_grp.add_url('franco_url',
				   'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/office-of-the-premier/intergovernmental-relations-secretariat/francophone')
		maps_grp.add_url('health_url', 'http://communityhealth.phsa.ca/Home/HealthAtlas')
		maps_grp.add_url('fish_url', 'http://www.bccdc.ca/health-info/food-your-health/fish-shellfish/processing-plants')
		maps_grp.add_url('child_url',
				   'http://www2.gov.bc.ca/gov/content/family-social-supports/data-monitoring-quality-assurance/find-services-for-children-teens-families')
		maps_grp.add_url('geonames_url',
				   'http://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/historic-places/geographical-names')
		maps_grp.add_url('rec_url', ['http://www2.gov.bc.ca/gov/content/sports-culture/recreation/camping-hiking/sites-trails',
				   'http://www.sitesandtrailsbc.ca'])
		maps_grp.add_url('mapplace_url', 'http://webmap.em.gov.bc.ca/mapplace/minpot/ex_maps.asp')
		maps_grp.add_url('harbour_url', 'http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=4758954260021402554')
		maps_grp.add_url('databc_url',
				   'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder')
		
		# Add to Extractor's page group list
		self.page_groups.append(maps_grp)
		
		
		# ####################################################################
		# # Create Industry Interactive maps page group

		# ind_grp = main_ext.PageGroup('industry_maps', "British Columbia's Industry Maps")
		
		# # No arguments to add
		
		# # Add URLs
		# ind_grp.add_url('meat_url',
				   # 'https://www2.gov.bc.ca/gov/content/industry/agriculture-seafood/food-safety/meat-inspection-licensing')
		# ind_grp.add_url('product_url',
				   # 'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/forest-inventory/site-productivity/provincial-site-productivity-layer')
		# ind_grp.add_url('seedlot_url',
				   # 'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedlot-aou')
		# ind_grp.add_url('seedmap_url',
				   # 'https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedmap')
		# ind_grp.add_url('iapp_url',
				   # 'https://www.for.gov.bc.ca/hra/plants/application.htm')
		# ind_grp.add_url('mineral_url',
				   # 'http://www.mtonline.gov.bc.ca/mtov/home.do')
				   
		# # Add to Extractor's page group list
		# self.page_groups.append(ind_grp)
		
		
		####################################################################
		# Create Map Services page group

		srv_grp = main_ext.PageGroup('services', "Map Services")
		
		# Add arguments
		sb_arg = srv_grp.add_arg('subpage', 'all', debug=True)
		sb_arg.add_opt('ArcGIS REST Service', ['rest'])
		sb_arg.add_opt('WMS', ['wms'])
		
		# Add URLs
		srv_grp.add_url('rest_urls', ['https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services',
								 'http://maps.gov.bc.ca/arcserver/rest/services'])
		srv_grp.add_url('wms_urls', ['http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?service=wms&request=getcapabilities&version=1.3.0',
								'http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?wms_landsat?service=wms&request=getcapabilities&version=1.3.0',
								'https://openmaps.gov.bc.ca/lzt/ows?service=wms&version=1.1.1&request=getcapabilities', 
								'https://tools.pacificclimate.org/ncWMS-PCIC/wms?REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.1.1', 
								'https://maps.gov.bc.ca/arcgis/services/province/roads/MapServer/WMSServer?request=GetCapabilities&service=WMS'])
		
		# Add to Extractor's page group list
		self.page_groups.append(srv_grp)
		
		
		####################################################################
		# Create Transportation Interactive Maps page group

		# trans_grp = main_ext.PageGroup('transpo_maps', "Transportation Maps")
		
		# # No arguments to add
		
		# # Add URLs
		# trans_grp.add_url('stops_url',
				   # 'http://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/traveller-information/stop-of-interest')
		# trans_grp.add_url('traffic_url',
				   # 'http://www.th.gov.bc.ca/trafficData/')
		
		# # Add to Extractor's page group list
		# self.page_groups.append(trans_grp)
		
		
		####################################################################
		# Create Other Interactive Maps page group

		# other_grp = main_ext.PageGroup('misc_maps', "Other Interactive Maps")
		
		# # No arguments to add
		
		# # Add URLs
		# other_grp.add_url('elections_url', 'http://elections.bc.ca/resources/maps')
		# other_grp.add_url('franco_url',
				   # 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/office-of-the-premier/intergovernmental-relations-secretariat/francophone')
		# other_grp.add_url('health_url', 'http://communityhealth.phsa.ca/Home/HealthAtlas')
		# other_grp.add_url('fish_url', 'http://www.bccdc.ca/health-info/food-your-health/fish-shellfish/processing-plants')
		# #other_grp.add_url('data_url', 'http://www2.gov.bc.ca/gov/content/data/geographic-data-services')
		# #other_grp.add_url('child_url',
		# #           'http://www2.gov.bc.ca/gov/content/family-social-supports/caring-for-young-children/child-care/search-for-child-care')
		# other_grp.add_url('child_url',
				   # 'http://www2.gov.bc.ca/gov/content/family-social-supports/data-monitoring-quality-assurance/find-services-for-children-teens-families')
		# other_grp.add_url('geonames_url',
				   # 'http://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/historic-places/geographical-names')
		# #other_grp.add_url('wildfire_url', 'http://www2.gov.bc.ca/gov/content/safety/wildfire-status')
		# #other_grp.add_url('wildfire_url', 'http://www2.gov.bc.ca/gov/content/safety/wildfire-status/wildfire-situation')
		# #other_grp.add_url('rec_url', ['http://www2.gov.bc.ca/gov/content/sports-culture/recreation/camping-hiking/sites-trails',
		# #               'http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=5140114829009675607'])
		# other_grp.add_url('rec_url', ['http://www2.gov.bc.ca/gov/content/sports-culture/recreation/camping-hiking/sites-trails',
				   # 'http://www.sitesandtrailsbc.ca'])
		# other_grp.add_url('mapplace_url', 'http://webmap.em.gov.bc.ca/mapplace/minpot/ex_maps.asp')
		# other_grp.add_url('harbour_url', 'http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=4758954260021402554')
		# other_grp.add_url('databc_url',
				   # 'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder')
		
		# # Add to Extractor's page group list
		# self.page_groups.append(other_grp)
		
		
		####################################################################
		# Create Webpages page group

		web_grp = main_ext.PageGroup('webpages', "Webpages with Geospatial Data")
		
		# No arguments to add
		
		# Add URLs
		web_grp.add_url('discovery_url', 'http://www.frontcounterbc.gov.bc.ca/mapping')
		web_grp.add_url('ortho_url',
				   'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/orthophotos/orthophoto-viewer')
		web_grp.add_url('air_url',
				   'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/air-photos/air-photo-viewer')
		web_grp.add_url('mascot_url',
				   'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/georeferencing/survey-control-operations')
		web_grp.add_url('geocoder_url',
				   'https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder')
		
		# Add to Extractor's page group list
		self.page_groups.append(web_grp)
		
		# FOR DEBUG:
		# for pg in self.page_groups:
			# print "Page ID: %s" % pg.get_id()
			# for arg in pg.get_args():
				# print "\targ_name: %s" % arg.get_name()
				# for opt in arg.get_opts():
					# print "\t\topt_name: %s" % opt.get_name()
		# answer = raw_input("Press enter...")
		

	###################################################################################################################
		
	def get_catalogue_extents(self, in_json):
		''' Gets the extents of a dataset from the BC Catalogue
		'''
		
		#print "Getting extents..."
		
		#print in_json
		
		#answer = raw_input("Press enter...")
		
		# Get the coordinates
		if not 'west_bound_longitude' in in_json:
			#print "No west bound coordinate in dataset."
			return ''
		west = in_json['west_bound_longitude']
		
		if not 'east_bound_longitude' in in_json:
			#print "No east bound coordinate in dataset."
			return ''
		east = in_json['east_bound_longitude']
		
		if not 'north_bound_latitude' in in_json:
			#print "No north bound coordinate in dataset."
			return ''
		north = in_json['north_bound_latitude']
		
		if not 'south_bound_latitude' in in_json:
			#print "No south bound coordinate in dataset."
			return ''
		south = in_json['south_bound_latitude']
		
		ext = [north, south, east, west]
		wkt_text = shared.create_wkt_extents(ext)
		
		#print wkt_text
		
		#answer = raw_input("Press enter...")
		
		return wkt_text

	###################################################################################################################

	def extract_arcgismaps(self):
		''' Extracts all ArcGIS maps on governmentofbc.maps.arcgis.com
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		if self.xl:
			pt_xl = sh.PT_XL(self, write_only=True, replace_ws=True)
		else:
			# Create the Maps CSV file
			csv_fn = "ArcGISMaps_results"
			pt_csv = sh.PT_CSV(csv_fn, self)
			pt_csv.open_csv()
		
		self.print_title("Extracting BC's ArcGIS maps")

		# Get the URL list
		url_list = self.pg_grp.get_url_list()

		for url_idx, url in enumerate(url_list):
		
			#msg = "Extracting ArcGIS map %s of %s maps" % (url_idx, len(url_list))
			#shared.print_oneliner(msg)
			
			print "Gallery URL: %s" % url

			gallery_soup = bsoup.get_soup(url, True)
			
			# Check if gallery_soup can be opened
			if not self.check_result(gallery_soup, url, 'ArcGIS Map', 'ArcGIS map could not be opened.'): continue

			gallery_div = gallery_soup.find('div', attrs={'class': 'gallery-card-wrap'})

			# Get the <div> with class "card" to get each interactive map
			map_anchors = gallery_div.find_all('a', attrs={'class': 'card-image-wrap'})

			#print len(map_anchors)

			for idx, card in enumerate(map_anchors):
				map_url = shared.get_anchor_url(card, url)

				msg = "Extracting %s of %s ArcGIS maps" % (idx + 1, len(map_anchors))
				shared.print_oneliner(msg)
				
				# Get the ArcGIS data
				arcgis_info = shared.get_arcgis_data(map_url)
				
				if 'code' in arcgis_info and arcgis_info['code'] == "430":
					sib_div = card.find_next_sibling('div', class_='card-content')
					item_a = sib_div.find('a')
					item_url = shared.get_anchor_url(item_a, url)
					
					#print item_url
					
					# Get the ArcGIS data
					arcgis_info = shared.get_arcgis_data(item_url)
					
					#print arcgis_info
					
					#answer = raw_input("Press enter...")

				# Check if arcgis_info can be opened
				err_txt = 'ArcGIS map could not be opened.'
				if not self.check_result(arcgis_info, map_url, 
										'ArcGIS Map', err_txt):
					continue

				# Add the ArcGIS data to the CSV
				for k, v in arcgis_info.items():
					pt_csv.add(k, v)

				# Add all values to the CSV file
				pt_csv.add('Source', 'BC ArcGIS Maps')
				pt_csv.add('Access', 'Viewable/Map Service')
				pt_csv.add('Download', 'No')
				pt_csv.add('Web Map URL', map_url)

				pt_csv.write_dataset()
				
			print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_catalogue(self): #, word=None, ds_type=None):
		''' Method to extract all geospatial data from the BC Open Data Catalogue.
			:param word: The word which will be used to query the catalogue.
		'''

		# Extract the BC Open Data Catalogue

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting from BC's Catalogue")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time
		
		# Get the parameters
		word = self.get_arg_val('word')
		ds_type = self.get_arg_val('ds_type')
		if ds_type.lower() == 'webservice':
			ds_type = 'WebService'
		else:
			ds_type = ds_type.title()

		# Create the Maps CSV file
		csv_fn = "Catalogue_%s_results" % ds_type
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Extraction of the BC Open Data Catalogue is done using their API
		# However, the API doesn't seem to have a way to get groups
		# so extraction will first start with the Catalogue web page

		catal_url = self.pg_grp.get_url('catal_url')
		api_url = self.pg_grp.get_url('api_url')

		# Build the query URL for the catalogue
		params = collections.OrderedDict()
		if word is not None and not word == '':
			params['q'] = word
		if ds_type is not None and not ds_type == '':
			params['type'] = ds_type
		query_url = shared.get_post_query(catal_url, params)

		# Get the query soup
		res_soup = bsoup.get_soup(query_url)
		
		# Check if res_soup can be opened
		err_txt = 'Catalogue query page could not be opened.'
		if not self.check_result(res_soup, query_url, 
								'Catalogue Query Page', err_txt):
			return None

		# Get the page count
		page_count = bsoup.get_page_count(res_soup, 'div', ['class', 
											'pagination'], 'li')

		# Used for displaying the percentage of records during processing
		prev_perc = -1
		record_count = 0
		special_chr = ""
		#record_total = page_count * 20

		time_count = 0.0

		#print "Page count: %s" % page_count
		
		# Get the total number of results from the page
		h2 = res_soup.find('h2', id='record-count')
		res_str = bsoup.get_text(h2)
		reg = re.findall('\d+(?:,\d+)?', res_str)
		rec_total = reg[0]
	
		# Set the current record
		record = 0
		geo_count = 0
		for page in range(0, page_count):
		#for page in range(0, 3):
		
			# Open each iteration of pages:
			if special_chr == "":
				# Some of the search entries can include "&" character
				#	but if an error is returned, use the "?" character instead
				try:
					page_url = "%s&page=%s" % (query_url, page + 1)
					special_chr = "&"
				except:
					page_url = "%s?page=%s" % (query_url, page + 1)
					special_chr = "?"
			else:
				page_url = "%s%spage=%s" % (query_url, special_chr, page + 1)

			# Create the soup object of the current page
			page_soup = bsoup.get_soup(page_url, silent=True)
			
			# If page_soup is None
			err_txt = 'Catalogue page could not be opened.'
			if not self.check_result(page_soup, query_url, 
									'Catalogue Page', err_txt):
				return None

			# Get all the results of the page
			results = page_soup.find_all('div', attrs={'class': 'dataset-content'})

			# Let the user know if there are no records
			if len(results) == 0 and record_count == 0:
				print "No records exist with the given search parameters."
				print "URL query sample: %s" % query_url
				return None

			# Cycle through each result
			for res in results:
				record += 1
				msg = "Extracting %s of approximately %s results from '%s'" \
						% (record, rec_total, query_url)
				shared.print_oneliner(msg)
			
				# Get the link and the dataset name for the API
				h3 = res.find('h3', attrs={'class': 'dataset-heading'})
				res_a = h3.a
				links = res_a['href'].split('/')
				ds_name = links[len(links) - 1]

				#print "Dataset name: %s" % ds_name

				# Get the dataset JSON text
				ds_api_url = "%s/action/package_show?id=%s" % (api_url, ds_name)
				ds_cat_url = "%s/%s" % (catal_url, ds_name)
				ds_json = shared.get_json(ds_api_url)
				
				# If ds_json is None
				if not self.check_result(ds_json, query_url, 
										'Catalogue JSON Results'):
					continue

				# For DEBUG
				#print
				#print ds_api_url
				#print ds_cat_url
				
				try:
					# Get the result JSON
					ds_res = ds_json['result']

					# FOR DEBUG ONLY
					#f = open('%s.json' % ds_name, 'w')
					#f.write(json.dumps(ds_json, indent=4, sort_keys=True))
					#f.close()

					# Get the title
					title_str = ds_res['title']

					# Get the description
					desc_str = ''
					if 'purpose' in ds_res.keys(): 
						desc_str = ds_res['purpose']

					if 'notes' in ds_res.keys():
						if desc_str == '':
							desc_str = ds_res['notes']
						else:
							desc_str = "%s|%s" % (ds_res['notes'], desc_str)

					# Get the date
					date_str = ds_res['record_last_modified']

					# Get the publisher
					org = ds_res['organization']
					pub_str = org['full_title']

					# Get the type
					result_type = ''
					if 'type' in ds_res.keys(): result_type = ds_res['type']

					# Get the licence
					lic_str = ds_res['license_title']

					# Get the web page URL
					webpage_url = ''
					if 'more_info' in ds_res.keys():
						more_info = ds_res['more_info']
						webpage_url = more_info[0]['link']
						if webpage_url.find('.pdf') > -1 and \
							len(more_info) > 1:
							webpage_url = more_info[1]['link']

					# Get the projection
					sp_str = shared.get_key(ds_res, 'projection_name')

					# Get the resources
					resources = ds_res['resources']
					
					# Get keywords
					keyword_lst = []
					tags = ds_res['tags']
					for tag in tags:
						keyword_lst.append(tag['display_name'])
					keywords = ', '.join(keyword_lst)
					
					#print "keywords: '%s'" % keywords
					#answer = raw_input("Press enter...")

					downloads = []
					formats = []
					service_url = ''
					service_type = ''
					map_url = ''
					created_dates = []
					latest_dates = []
					extents = ''
					for r in resources:
						# Get the format
						format = r['format']
						
						#print "\nFormat: %s" % r['format']
						#print "URL: %s" % r['url']
						#answer = raw_input("Press enter...")
						
						#print "\nFormat: %s" % format
						#answer = raw_input("Press enter...")

						res_url = r['url']
						
						if format == 'wms':
							if res_url.find('GetCapabilities') == -1 and \
								res_url.find('arcgis') == -1:
								res_url += 'request=GetCapabilities&service=WMS'
							service_url = res_url
							service_type = 'WMS'
							
							if res_url.find('arcgis') > -1:
								# Open the ArcGIS REST page
								arc_info = shared.get_arcgis_data(res_url)
								
								extents = arc_info['Extents']
								#keywords = arc_info['Keywords']
							else:
								# Open the WMS link to get more info
								wms = services.PT_WMS(res_url)
								wms_info = wms.get_data()
								
								if 'layers' in wms_info:
									lyr = wms_info['layers'][0]
								
									extents = lyr['Extents']
									#keywords = lyr['Keywords']
						elif format == 'arcgis_rest':
							service_url = res_url
							service_type = 'ArcGIS REST'
						
							# Open the ArcGIS REST page
							arc_rest = services.PT_REST(res_url)
							rest_info = arc_rest.get_data()
							
							# for serv in rest_info['services']:
								# for k, v in serv.items():
									# print "%s: %s" % (k, v)
							# answer = raw_input("Press enter...")
							
							if 'layers' in rest_info['services'][0]:
								layers = rest_info['services'][0]['layers']
								
								if len(layers) > 0:
									lyr = layers[0]
								
									# print
									# print res_url
									# print "lyr['Extents']: %s" % lyr['Extents']
									# answer = raw_input("Press enter...")
								
									if extents == '': extents = lyr['Extents']
									#if keywords == '': keywords = lyr['Keywords']
							
							#print rest_info
							#answer = raw_input("Press enter...")
						elif format == 'other' or format == '':
							if result_type == 'Application':
								map_url = res_url
						
						if not res_url == '':
							downloads.append(res_url)
							formats.append(format.upper())
								
						# Get the dates
						if 'created' in r:
							created_dates.append(r['created'])
							
						#if 'last_modified' in r:
						#	latest_dates.append(r['last_modified'])
							
					startdate_str, _ = shared.get_minmax_date(created_dates)
					#_, max_date = shared.get_minmax_date(latest_dates)
					
					#print "\nStart date: %s" % min_date
					#print "Recent date: %s" % date_str
					
					#answer = raw_input("Press enter...")
								
					# Get unique formats
					formats = list(set(formats))

					# Get tags to determine the type of dataset
					if 'tags' in ds_res.keys():
						tags = ds_res['tags']
						tag_list = [tag['display_name'] for tag in tags]

						if 'interactive map' in tag_list:
							result_type = 'Interactive Map'
							if 'ArcGIS Online' in tag_list:
								result_type = 'ArcGIS Online Map'

					download_info = shared.get_download_text(formats, downloads)
					download_str, access_str = download_info.split('|')
					
					mdata_type = ''
					if 'metadata_standard_name' in ds_res:
						mdata_type = ds_res['metadata_standard_name']
					
					# Get the coordinates
					if extents == '':
						extents = self.get_catalogue_extents(ds_res)
					
					geo_formats = ['WMS', 'ARCGIS_REST', 'KML', 'KMZ', \
									'GEOJSON', 'SHP', 'ARCVIEW SHAPE', \
									'ESRI FILE GEODATABASE', \
									'GEODATABASE_FILE', 'E00', 'GEORSS', \
									'SHAPE', 'FGDB']
									
					
					# print
					# print "Extents: %s" % extents
					# print "Geo Formats: %s" % geo_formats
					# print "Formats: %s" % formats
					# print any(l in formats for l in geo_formats)
					# answer = raw_input("Press enter...")
					
					# Check if geospatial data
					if extents == '' and \
						not any(l in formats for l in geo_formats):
						continue

					if map_url.find('arcgis') > -1:
						result_type = 'ArcGIS Online Map'

						# Add all values to the CSV file object
						pre_info = collections.OrderedDict()
						pre_info['Source'] = 'BC Data Catalogue'
						pre_info['Title'] = title_str
						pre_info['Description'] = desc_str
						pre_info['Type'] = result_type
						pre_info['Start Date'] = startdate_str
						pre_info['Recent Date'] = date_str
						pre_info['Keywords'] = keywords
						pre_info['Licensing'] = lic_str
						pre_info['Download'] = download_str
						pre_info['Access'] = access_str
						pre_info['Publisher'] = pub_str
						pre_info['Extents'] = extents
						pre_info['Web Page URL'] = webpage_url
						pre_info['Web Map URL'] = map_url
						pre_info['Spatial Reference'] = sp_str
						pre_info['Service URL'] = service_url
						pre_info['Service'] = service_type
						pre_info['Available Formats'] = '|'.join(formats)
						pre_info['Metadata URL'] = ds_cat_url
						pre_info['Metadata Type'] = mdata_type
						pre_info['Data URL'] = ds_api_url

						# Get the ArcGIS data
						arcgis_info = shared.get_arcgis_data(map_url, 
															pre_info=pre_info)
						
						if 'err' in arcgis_info:
							arcgis_info = collections.OrderedDict()
							# print "map_data: %s" % map_data
							arcgis_info['Title'] = '(ERROR: see notes)'
							arcgis_info['Type'] = "ArcGIS Map"
							arcgis_info['Web Map URL'] = map_url
							arcgis_info['Notes'] = map_json['err']
						
						# If ds_json is None
						err_txt = 'ArcGIS map could not be opened.'
						if not self.check_result(ds_json, query_url, 
												'ArcGIS Map', err_txt):
							continue

						# Add the ArcGIS data to the CSV
						for k, v in arcgis_info.items():
							pt_csv.add(k, v)

					else:

						# Add all values to the CSV file object
						pt_csv.add('Source', 'BC Data Catalogue')
						pt_csv.add('Title', title_str)
						pt_csv.add('Description', desc_str)
						pt_csv.add('Type', result_type)
						pt_csv.add('Keywords', keywords)
						pt_csv.add('Start Date', startdate_str)
						pt_csv.add('Recent Date', date_str)
						pt_csv.add('Licensing', lic_str)
						pt_csv.add('Download', download_str)
						pt_csv.add('Access', access_str)
						pt_csv.add('Publisher', pub_str)
						pt_csv.add('Extents', extents)
						pt_csv.add('Web Page URL', webpage_url)
						pt_csv.add('Web Map URL', map_url)
						pt_csv.add('Spatial Reference', sp_str)
						pt_csv.add('Service URL', service_url)
						pt_csv.add('Service', service_type)
						pt_csv.add('Available Formats', '|'.join(formats))
						pt_csv.add('Metadata URL', ds_cat_url)
						pt_csv.add('Metadata Type', mdata_type)
						pt_csv.add('Data URL', ds_api_url)
					# FOR DEBUG ONLY
					#pt_csv.add('Restrictions', access_method)

					#pt_csv.add('Access', access)
					#pt_csv.add('Service URL', serv_url)
					#pt_csv.add('Service Name', serv_name)
					#pt_csv.add('Service', serv_type)
					#pt_csv.add('Type', dtype)
					#pt_csv.add('Web Map URL', webmap_url)
					#pt_csv.add('Download', download_str)
					#pt_csv.add('Metadata URL', mdata_url)
					#pt_csv.add('Metadata Type', mdata_type)
					#pt_csv.add('Available Formats', format_str)
					#pt_csv.add('Spatial Reference', sp)

					# Write the dataset to the CSV file
					geo_count += 1
					pt_csv.write_dataset()

					#answer = raw_input("Press enter...")
				except:
					print traceback.format_exc()
					f = open('files\\errors\\%s_error.json' % ds_name, 'w')
					f.write("ERROR: %s\n\n" % traceback.format_exc())
					f.write(json.dumps(ds_json, indent=4, sort_keys=True))
					f.close()
					answer = raw_input("Press enter...")

			print
			
		print "\nA total of %s geospatial datasets saved to CSV file." % geo_count
					
		pt_csv.close_csv()
		#serv_csv.close_csv()
		#docs_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction extraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_enviro_maps(self):
		''' Extracts British Columbia's environmental interactive maps
		:return: None
		'''

		# self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the Maps CSV file
		# csv_fn = "Maps_Environmental_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		self.print_title("Extracting BC's Environmental interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		#######################################################################################
		# Get the Parks Map

		# # Get the parks page URL
		webpage_url = self.pg_grp.get_url('parks_url')
		webpage_soup = bsoup.get_soup(webpage_url)
		
		# Check if webpage_soup can be opened
		err_txt = 'Parks map page results could not be opened.'
		if self.check_result(webpage_soup, webpage_url, 'Parks Map', err_txt):
			#
			# # Get the map soup
			# map_url = self.pg_grp.get_url('parks_url')[0]
			# map_soup = bsoup.get_soup(map_url, True, ['id', 'about-text'])
			#
			# # Get the title of the map
			# title_str = bsoup.get_text(webpage_soup.find('title'))
			
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)

			#print "Title: '%s'" % title_str

			# Get the description
			# about_div = map_soup.find('div', attrs={'id': 'about-text'})
			#f = codecs.open('about.html', mode='w', encoding='utf-8')
			#f.write(unicode(map_soup))
			#f.close()
			# desc_str = shared.edit_description(bsoup.get_text(about_div))

			# Get the link to the full map page
			map_a = bsoup.find_tags_containing(webpage_soup, 'full screen', 'a')
			map_url = shared.get_anchor_url(map_a, webpage_url)

			# Get the information from the metadata of the page
			map_mdata = bsoup.get_page_metadata(webpage_soup)

			# Get the info from the metadata
			title_str = map_mdata['title']
			desc_str = map_mdata['Description']
			pub_str = map_mdata['DCTERMS.publisher']

			#print "Description: '%s'" % desc_str

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Google Interactive Map')
			self.pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Page URL', webpage_url)
			self.pt_csv.add('Web Map URL', map_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Long-term Trends in Groundwater Levels

		# Get the groundwater soup
		ground_url = self.pg_grp.get_url('ground_url')
		ground_soup = bsoup.get_soup(ground_url)
		
		# If ground_soup is None
		if self.check_result(ground_soup, ground_url, 'Long-term Trends in Groundwater Levels'):
			# Get the title
			#title_str = bsoup.get_text(ground_soup.title)
			
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)

			# Get the description
			#desc_str = bsoup.get_text(ground_soup.find('meta', attrs={'name': 'description'})['content'])

			# Get the page metadata
			page_mdata = bsoup.get_page_metadata(ground_soup)

			title_str = page_mdata['page_title']
			startdate_str = page_mdata['dcterms.created']
			date_str = page_mdata['dcterms.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['dcterms.publisher']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Type', 'Google Interactive Map')
			self.pt_csv.add('Spatial Reference', 'WGS 84 Web Mercator')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', ground_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Real-time Water Data

		# Get the water soup
		water_url = self.pg_grp.get_url('water_url')
		water_soup = bsoup.get_soup(water_url)
		
		# If page_soup can be opened
		if self.check_result(water_soup, water_url, 'Real-time Water Data'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = water_soup.find('a', attrs={'class': 'alert-link'})
			map_url = shared.get_anchor_url(map_a, water_url)

			# Most info about the map can be taken from the web page's metadata

			page_mdata = bsoup.get_page_metadata(water_soup)

			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.creator']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', water_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the CDC iMap

		# Get the CDC soup
		cdc_url = self.pg_grp.get_url('cdc_url')
		cdc_soup = bsoup.get_soup(cdc_url)
		
		# If page_soup can be opened
		if self.check_result(cdc_soup, cdc_url, 'CDC iMap'):
			
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(cdc_soup, 'Launch CDC iMap', 'a')
			#print "map_a: %s" % map_a
			map_url = shared.get_anchor_url(map_a, cdc_url)

			page_mdata = bsoup.get_page_metadata(cdc_soup)

			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.creator']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Page URL', cdc_url)
			self.pt_csv.add('Web Map URL', map_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Frogwatching

		# Get the frogwatching soup
		frog_url = self.pg_grp.get_url('frog_url')
		frog_soup = bsoup.get_soup(frog_url)
		
		# If page_soup can be opened
		if self.check_result(frog_soup, frog_url, 'Frogwatching'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(frog_soup, 'BC Frogwatch Atlas', 'a')

			map_url = shared.get_anchor_url(map_a, frog_url)

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(frog_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.creator']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', frog_url)
			self.pt_csv.add('Notes', 'Requires Silverlight and only works in Internet Explorer.')

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the EcoCat

		# Get the EcoCat soup
		ecocat_url = self.pg_grp.get_url('ecocat_url')
		ecocat_soup = bsoup.get_soup(ecocat_url)
		
		# If ecocat_soup can be opened
		if self.check_result(ecocat_soup, ecocat_url, 'EcoCat'):
			
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# # Get the title
			# title_td = ecocat_soup.find('td', attrs={'class': 'programHeadingHome'})
			# title_str = bsoup.get_text(title_td)
			#
			# # Get the description
			# form = ecocat_soup.find('form', attrs={'name': 'searchForm'})
			# desc_str = bsoup.get_text(form)

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(ecocat_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Get the search page URL
			search_a = bsoup.find_tags_containing(ecocat_soup, 'Public access to EcoCat', 'a')
			search_url = shared.get_anchor_url(search_a, ecocat_url)
			search_soup = bsoup.get_soup(search_url + "/public/welcome.do")
			
			if search_soup is None:
				print "\nWARNING: EcoCat search results '%s' could not be opened." % ecocat_url
				print "Please check the 'err_log.csv' file in the province/territory results folder."
				self.write_error(ecocat_url, 'EcoCat Search Results', 'Page could not be opened.')
			else:
				# Get the map URL from the search page
				map_a = bsoup.find_tags_containing(search_soup, 'Search for Reports using a map', 'a')
				map_jslink = map_a['href']
				start_pos = map_jslink.find('(') + 1
				end_pos = map_jslink.find(')')
				map_url = map_jslink[start_pos:end_pos].replace("'", "")

				# Add all values to the CSV file object
				self.pt_csv.add('Source', 'BC Interactive Maps')
				self.pt_csv.add('Title', title_str)
				self.pt_csv.add('Description', desc_str)
				self.pt_csv.add('Start Date', startdate_str)
				self.pt_csv.add('Recent Date', date_str)
				self.pt_csv.add('Publisher', pub_str)
				self.pt_csv.add('Keywords', keywords)
				self.pt_csv.add('Type', 'Interactive Map')
				self.pt_csv.add('Download', 'No')
				self.pt_csv.add('Access', 'Viewable/Contact the Province')
				self.pt_csv.add('Web Map URL', map_url)
				self.pt_csv.add('Web Page URL', ecocat_url)
				self.pt_csv.add('Notes', 'Requires Silverlight and only works in Internet Explorer.')

				self.pt_csv.write_dataset()

		#######################################################################################
		# Get the ClimateBC/WNA/NA

		# Get the climateBC soup
		forest_url = self.pg_grp.get_url('forest_url')
		forest_soup = bsoup.get_soup(forest_url)
		
		# If forest_soup can be opened
		if self.check_result(forest_soup, forest_url, 'ClimateBC/WNA/NA'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			strong_list = bsoup.find_tags_containing(forest_soup, 'Web-based version', 'strong', output='list')

			for strong in strong_list:

				# # Get the title from the previous <h1> of the parent of strong
				# p_parent = strong.parent
				# title_h1 = p_parent.find_previous_sibling('h1')
				# title_str = bsoup.get_text(title_h1)

				# Get the map URL
				sib_a = strong.find_next_sibling('a')
				map_url = shared.get_anchor_url(sib_a, forest_url)
				
				# Get the title from the previous <h1> tag
				p = strong.parent
				h1 = bsoup.find_prev_tag_containing(p, 'h1')
				title_str = bsoup.get_text(h1)

				# Get the information from the metadata of the map page
				map_soup = bsoup.get_soup(map_url)
				
				if not self.check_result(map_soup, map_url, '%s Map' % title_str):
					desc_str = ''
					
					note_str = 'Page could not be loaded.'
				else:
					# Get the page's metadata
					map_mdata = bsoup.get_page_metadata(map_soup)

					# Get the title
					title_str = bsoup.get_text(map_soup.find('title'))
					title_str = title_str.replace("_", " ")

					# Get the description
					desc_str = map_mdata['description']
					
					# Get keywords
					keywords = map_mdata['keywords']
					
					note_str = ''

				#print "Title: %s" % title_str
				#print "Description: %s" % desc_str

				# Add all values to the CSV file object
				self.pt_csv.add('Source', 'BC Interactive Maps')
				self.pt_csv.add('Title', title_str)
				self.pt_csv.add('Description', desc_str)
				self.pt_csv.add('Keywords', keywords)
				self.pt_csv.add('Type', 'Interactive Map')
				self.pt_csv.add('Download', 'No')
				self.pt_csv.add('Access', 'Viewable/Contact the Province')
				self.pt_csv.add('Web Map URL', map_url)
				self.pt_csv.add('Web Page URL', forest_url)
				self.pt_csv.add('Notes', note_str)

				self.pt_csv.write_dataset()

		#######################################################################################
		# Get the BC Water Tool Maps

		# Get the BC Water Tools soup
		bcwater_url = self.pg_grp.get_url('bcwater_url')
		bcwater_soup = bsoup.get_soup(bcwater_url)
		
		# If bcwater_soup can be opened
		if self.check_result(bcwater_soup, bcwater_url, 'BC Water Tool Maps'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
			
			# To get the keywords, open the gov.bc.ca page with link to Water Tools
			init_url = 'https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools'
			init_soup = bsoup.get_soup(init_url)
			init_mdata = bsoup.get_page_metadata(init_soup)
			keywords = init_mdata['keywords']
		
			# Get all the DIVs for each map
			map_divs = bcwater_soup.find_all('div', attrs={'class': 'project primary-text'})

			for map in map_divs:
				# Get the title
				title_div = map.find('div', attrs={'class': 'project-title headline'})
				title_str = bsoup.get_text(title_div)

				# Get the description
				desc_div = map.find('div', attrs={'class': 'project-description'})
				desc_str = bsoup.get_text(desc_div)

				# Get the map URL
				action_div = map.find('div', attrs={'class': 'project-actions'})
				map_a = action_div.a
				map_url = shared.get_anchor_url(map_a, bcwater_url)

				# Add all values to the CSV file object
				self.pt_csv.add('Source', 'BC Interactive Maps')
				self.pt_csv.add('Title', title_str)
				self.pt_csv.add('Description', desc_str)
				self.pt_csv.add('Keywords', keywords)
				self.pt_csv.add('Type', 'Interactive Map')
				self.pt_csv.add('Download', 'No')
				self.pt_csv.add('Access', 'Viewable/Contact the Province')
				self.pt_csv.add('Web Map URL', map_url)
				self.pt_csv.add('Web Page URL', bcwater_url)

				self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Pacific Climate Impacts Consortium Data Portal

		# Get the BC Water Tools soup
		climate_url = self.pg_grp.get_url('climate_url')
		climate_soup = bsoup.get_soup(climate_url)
		
		# If climate_soup can be opened
		if self.check_result(climate_soup, climate_url, 'Pacific Climate Impacts Consortium Data Portal'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			subsections = climate_soup.find_all('div', attrs={'class': 'subsection'})
			for section in subsections:
				# Get the title
				h2 = section.h2
				title_str = bsoup.get_text(h2)

				# Get the description
				desc_p = h2.find_next_sibling('p')
				desc_str = bsoup.get_text(desc_p)

				# Open section's page
				sect_url = shared.get_anchor_url(h2.a, climate_url)
				sect_soup = bsoup.get_soup(sect_url)
				
				if sect_soup is None:
					print "\nWARNING: Pacific Climate Impacts Consortium Data Portal section's page '%s' could not be opened." % sect_url
					print "Please check the 'err_log.csv' file in the province/territory results folder."
					self.write_error(sect_url, 'Pacific Climate Impacts Consortium Data Portal Section', 'Page could not be opened.')
					
					map_url = ''
				else:
					# Get the map URL from the section's page
					map_a = bsoup.find_tags_containing(sect_soup, 'Access and download', 'a')
					map_url = shared.get_anchor_url(map_a, sect_url)

				# Add all values to the CSV file object
				self.pt_csv.add('Source', 'BC Interactive Maps')
				self.pt_csv.add('Title', title_str)
				self.pt_csv.add('Description', desc_str)
				self.pt_csv.add('Type', 'Interactive Map')
				self.pt_csv.add('Download', 'No')
				self.pt_csv.add('Access', 'Viewable/Contact the Province')
				self.pt_csv.add('Web Map URL', map_url)
				self.pt_csv.add('Web Page URL', climate_url)

				self.pt_csv.write_dataset()

		#######################################################################################
		# Get the BC Environmental Assessment Office

		# Get the BC Water Tools soup
		eao_url = self.pg_grp.get_url('eao_url')
		eao_soup = bsoup.get_soup(eao_url, True)
		
		# If eao_soup can be opened
		if self.check_result(eao_soup, eao_url, 'BC Environmental Assessment Office'):
		
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the title from the <h1> tag
			h1 = eao_soup.find('h1')
			title_str = bsoup.get_text(h1)

			# Get the description
			desc_p = h1.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Find span with text 'View Map'
			span = bsoup.find_tags_containing(eao_soup, 'View Map', 'span')
			map_a = span.parent
			map_url = shared.get_anchor_url(map_a, eao_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', eao_url)

			self.pt_csv.write_dataset()
			
		print
		
		#pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction extraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_ftp(self):
		''' Extract the FTP datasets
		:return: None
		'''

		ftp_domain = self.pg_grp.get_url('ftp_url')

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the CSV file
		csv_fn = "FTP_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		# Get a list of directories
		dir_list = []
		dir_list.append('/pub/')
		dir_list.append('/sections/')
		
		self.print_title("Extracting FTP files from '%s'" % ftp_domain)
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Get a list of files on the FTP site
		ftp_files = []
		header = ['date', 'time', 'type', 'filename']
		#print "dir_list: %s" % dir_list
		for idx, dr in enumerate(dir_list):
			msg = "Adding FTP folder %s of %s folders" % (idx, len(dir_list))
			shared.print_oneliner(msg)
		
			# Get the FTP object for the current folder
			ftp = rec_ftp.RecFTP(ftp_domain, dr, header, self.debug)

			# Get a list of files under the current folder
			ftp_list = ftp.get_file_list()
			
			#print ftp_list

			# Add the files to the overall ftp_files list
			if isinstance(ftp_list, list):
				ftp_files += ftp_list
			else:
				ftp_files.append(ftp_list)
			
		print
		
		#print "ftp_files: %s" % ftp_files

		for f_idx, f in enumerate(ftp_files):
			#print f
			
			msg = "Extracting file %s of %s FTP files from '%s'" % (f_idx, len(ftp_files), ftp_domain)
			shared.print_oneliner(msg)

			#print "f: '%s'" % f
			
			if isinstance(f, dict) and 'err' in f:
				#print f
				pt_csv.add('Source', 'BC FTP')
				pt_csv.add('Title', 'ERROR: see notes')
				#pt_csv.add('Type', ds_type)
				#pt_csv.add('Download', f)
				pt_csv.add('Data URL', f['url'])
				#pt_csv.add('Access', 'Download/Accessible FTP')
				#pt_csv.add('Available Formats', ext.upper())
				pt_csv.add('Notes', f['err'])

				pt_csv.write_dataset()
				
				continue
			
			folder = os.path.dirname(f)
			basename = os.path.basename(f)
			if basename.find('.') == -1: continue
			title_str = basename.split('.')[0]
			#print "\n%s" % basename
			ext = basename.split('.')[1]

			pt_csv.add('Source', 'BC FTP')
			pt_csv.add('Title', title_str)
			#pt_csv.add('Type', ds_type)
			pt_csv.add('Download', f)
			pt_csv.add('Data URL', folder)
			pt_csv.add('Access', 'Download/Accessible FTP')
			pt_csv.add('Available Formats', ext.upper())

			pt_csv.write_dataset()
			
		print

		# Go through each file
		# ftp_dict = collections.OrderedDict()
		# for f in ftp_files:
		#     dir_key = f[0]
		#     print "dir_key: %s" % dir_key
		#     if dir_key in ftp_dict.keys():
		#         cur_list = ftp_dict[dir_key]
		#         cur_list.append(f[1])
		#         ftp_dict[dir_key] = cur_list
		#     else:
		#         new_list = []
		#         new_list.append(f[1])
		#         ftp_dict[dir_key] = new_list
		#
		# answer = raw_input("Press enter...")
		#
		# final_dict = collections.OrderedDict()
		# for k, v in ftp_dict.items():
		#     tmp_dict = collections.OrderedDict()
		#     for i in v:
		#         key_val = i.split('.')[0]
		#         if key_val in tmp_dict.keys():
		#             cur_list = tmp_dict[key_val]
		#             cur_list.append(i)
		#             tmp_dict[key_val] = cur_list
		#         else:
		#             new_list = []
		#             new_list.append(i)
		#             tmp_dict[key_val] = new_list
		#     final_dict[k] = tmp_dict

		# out_f = open('ftp_test.txt', 'w')
		# for k, v in final_dict.items():
		#    out_f.write('%s: %s\n' % (k, v))
		# out_f.close()

		# for folder, files in final_dict.items():
		#     print "folder: %s" % folder
		#     print "files: %s" % files
		#
		#     for key, f in files.items():
		#
		#         if len(f) > 1:
		#             formats = []
		#             for fle in f:
		#                 format = fle.split('.')[1]
		#                 formats.append(format.upper())
		#             download = 'Multiple Downloads'
		#             ds_type = 'Vector File'
		#         else:
		#             fle = f[0]
		#             formats = [fle.split('.')[1].upper()]
		#             download = '%s/%s' % (folder, fle)
		#             if fle.find('.tif') > -1:
		#                 ds_type = 'Raster File'
		#             else:
		#                 ds_type = 'Vector File'
		#
		#         pt_csv.add('Title', key.replace("_", " "))
		#         pt_csv.add('Type', ds_type)
		#         pt_csv.add('Download', download)
		#         pt_csv.add('FTP URL', folder)
		#         pt_csv.add('Access', 'Download/Accessible FTP')
		#         pt_csv.add('Available Formats', '|'.join(formats))
		#
		#         pt_csv.write_dataset()

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_industry_maps(self):

		''' Extracts British Columbia's industry interactive maps
			:return: None
			'''

		# self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the Maps CSV file
		# csv_fn = "Maps_Industry_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		self.print_title("Extracting BC's Industry interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		#######################################################################################
		# Get the Meat Inspection & Licensing

		meat_url = self.pg_grp.get_url('meat_url')
		meat_soup = bsoup.get_soup(meat_url)
		
		# Check if meat_soup can be opened
		if self.check_result(meat_soup, meat_url, 'Meat Inspection & Licensing'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get metadata info
			page_mdata = bsoup.get_page_metadata(meat_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Get the map link from the sidebar
			sidebar_div = meat_soup.find('div', attrs={'class': 'contentPageRightColumn'})
			map_a = bsoup.find_tags_containing(sidebar_div, 'Find a provincially licensed', 'a')
			map_url = shared.get_anchor_url(map_a, meat_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', meat_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Provincial Site Productivity Layer map and Hectares BC map

		product_url = self.pg_grp.get_url('product_url')
		product_soup = bsoup.get_soup(product_url)
		
		# Check if meat_soup can be opened
		if self.check_result(product_soup, product_url, 'Provincial Site Productivity Layer Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get metadata info
			page_mdata = bsoup.get_page_metadata(product_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Get map link
			main_div = product_soup.find('div', attrs={'id': 'main-content'})
			body_div = main_div.find('div', attrs={'id': 'body'})
			h2 = bsoup.find_tags_containing(body_div, 'Access to the Database & PDF Maps Catalogue', 'h2')
			ul_sib = h2.find_next_sibling('ul')
			map_a = ul_sib.find('a')
			map_url = shared.get_anchor_url(map_a, product_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', product_url)

			self.pt_csv.write_dataset()

			# Get the Hectares BC map on the same page
			
			#print "\n%s" % product_url

			hec_h2 = bsoup.find_tags_containing(body_div, 'Hectares BC Website')

			# Get description
			desc_p = hec_h2.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			#map_span = bsoup.find_tags_containing(body_div, 'Access Hectares BC', 'span')
			map_a = desc_p.a
			#map_a = map_span.parent

			map_url = shared.get_anchor_url(map_a, product_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', 'Hectares BC')
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', product_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Seedlot Area of Use map

		seedlot_url = self.pg_grp.get_url('seedlot_url')
		seedlot_soup = bsoup.get_soup(seedlot_url)
		
		if self.check_result(seedlot_soup, seedlot_url, 'Seedlot Area of Use Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the main-content <div>
			main_div = seedlot_soup.find('div', attrs={'id': 'main-content'})

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(seedlot_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Get the map link
			intro_div = main_div.find('div', attrs={'id': 'introduction'})
			p_list = intro_div.find_all('p')
			map_a = p_list[2].a
			map_url = shared.get_anchor_url(map_a, product_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', product_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the SeedMap

		seedmap_url = self.pg_grp.get_url('seedmap_url')
		seedmap_soup = bsoup.get_soup(seedmap_url)
		
		if self.check_result(seedmap_soup, seedmap_url, 'SeedMap'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get metadata info
			page_mdata = bsoup.get_page_metadata(seedmap_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Get the map link from the sidebar
			sidebar_div = seedmap_soup.find('div', attrs={'class': 'contentPageRightColumn'})
			map_a = bsoup.find_tags_containing(sidebar_div, 'Launch the SeedMap Application', 'a')
			map_url = shared.get_anchor_url(map_a, seedmap_url)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', seedmap_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Invasive Alien Plant Program map

		iapp_url = self.pg_grp.get_url('iapp_url')
		iapp_soup = bsoup.get_soup(iapp_url)
		
		if self.check_result(iapp_soup, iapp_url, 'Invasive Alien Plant Program Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get metadata info
			page_mdata = bsoup.get_page_metadata(iapp_soup)
			title_str = page_mdata['title']
			date_str = page_mdata['DC.date']
			desc_str = page_mdata['description']
			pub_str = page_mdata['DC.publisher']

			# Get the map link
			map_a = bsoup.find_tags_containing(iapp_soup, 'IAPP Map Display', 'a')
			map_url = map_a['href']

			# print "Title: %s" % title_str
			# print "Recent Date: %s" % date_str
			# print "Description: %s" % desc_str
			# print "Publisher: %s" % pub_str
			# print "Map URL: %s" % map_url
			# print "IAPP URL: %s" % iapp_url

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', iapp_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Mineral Titles maps

		mineral_url = self.pg_grp.get_url('mineral_url')
		mineral_soup = bsoup.get_soup(mineral_url)  # , True, attrb=['class', 'journal-content-article'])
		
		if self.check_result(mineral_soup, mineral_url, 'Mineral Titles Maps'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			strong_mapviewer = bsoup.find_tags_containing(mineral_soup, 'Map Viewer', 'strong')

			for strong in strong_mapviewer:
				# Get the parent of the <strong>
				p = strong.parent
				# Get the title from the p text
				title = bsoup.get_text(p)
				# Get the remaining anchor siblings
				a_list = p.find_next_siblings('a')

				# print "Number of anchors: %s" % len(a_list)
				# print "a_list: %s" % a_list
				# print "title: %s" % title

				for a in a_list:
					# Get the map link
					js_link = a['href']
					link = shared.get_bracket_text(js_link)
					map_url = urlparse.urljoin(mineral_url, link.replace("'", ""))

					# Determine the title suffix
					if link.find('=M') > -1 or link.find('min') > -1:
						title_str = "%s - Mineral Map" % title
					elif link.find('=P') > -1 or link.find('pla') > -1:
						title_str = "%s - Placer Map" % title
					elif link.find('=C') > -1 or link.find('coal') > -1:
						title_str = "%s - Coal Map" % title

					# print map_url

					# Add all values to the CSV file object
					self.pt_csv.add('Source', 'BC Interactive Maps')
					self.pt_csv.add('Title', title_str)
					self.pt_csv.add('Type', 'Interactive Map')
					self.pt_csv.add('Download', 'No')
					self.pt_csv.add('Access', 'Viewable/Contact the Province')
					self.pt_csv.add('Web Map URL', map_url)
					self.pt_csv.add('Web Page URL', mineral_url)

					self.pt_csv.write_dataset()
					
		print

		#pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time
		
	def extract_maps(self):
		''' Extracts all BC's Interactive Maps
		:return: None
		'''
		
		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# Create the Maps CSV file
		csv_fn = "Interactive_Maps_results"
		self.pt_csv = sh.PT_CSV(csv_fn, self)
		self.pt_csv.open_csv()
		
		# Extract the Environmental Maps
		self.extract_enviro_maps()
		
		# Extract the Industry Maps
		self.extract_industry_maps()
		
		# Extract the Transportation Maps
		self.extract_transpo_maps()
		
		# Extract the rest
		self.extract_misc_maps()
		
		# Close CSV file
		self.pt_csv.close_csv()

	def extract_misc_maps(self):
		''' Extracts British Columbia's other maps
		:return: None
		'''

		# self.print_log("\nExtracting from %s" % self.pg_grp.get_title())

		# # Create the Maps CSV file
		# csv_fn = "Maps_Misc_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		self.print_title("Extracting BC's other interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		#######################################################################################
		# Get the Elections BC map

		elections_url = self.pg_grp.get_url('elections_url')
		elections_soup = bsoup.get_soup(elections_url)
		
		if self.check_result(elections_soup, elections_url, 'Elections BC Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(elections_soup, 'Electoral District Explorer', 'a')
			map_url = map_a['href']

			map_soup = bsoup.get_soup(map_url, True, ['class', 'content'], 45)
			
			if map_soup is None:
				print "\nWARNING: Elections BC map page '%s' could not be opened." % map_url
				print "Please check the 'err_log.csv' file in the province/territory results folder."
				self.write_error(map_url, 'Elections BC Map', 'Page could not be opened.')
				
				title_str = ''
				desc_str = ''
				
				notes_str = 'Map page could not be loaded.'
			else:
				# Get the map's title
				title_str = bsoup.get_text(map_soup.find('title'))

				# Get the map's description
				content_div = map_soup.find('div', attrs={'class': 'content'})
				desc_str = bsoup.get_text(content_div.p)
				
				notes_str = ''

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', elections_url)
			self.pt_csv.add('Notes', notes_str)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Francophone Services map

		franco_url = self.pg_grp.get_url('franco_url')
		franco_soup = bsoup.get_soup(franco_url)
		
		if self.check_result(franco_soup, franco_url, 'Francophone Services Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(franco_soup, 'interactive map', 'a')
			map_url = map_a['href']

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(franco_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', franco_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the BC Community Health Atlas

		health_url = self.pg_grp.get_url('health_url')
		health_soup = bsoup.get_soup(health_url)
		
		if self.check_result(health_soup, health_url, 'BC Community Health Atlas'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the title
			h1 = bsoup.find_tags_containing(health_soup, 'BC Community Health Atlas', 'h1')
			title_str = bsoup.get_text(h1)

			#print title_str

			# Get the description
			desc_p = h1.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Get the map URL
			map_a = bsoup.find_tags_containing(desc_p, \
							'BC Community Health Atlas', 'a')
			map_url = map_a['href']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', health_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Fish Processing Plants map

		fish_url = self.pg_grp.get_url('fish_url')
		fish_soup = bsoup.get_soup(fish_url)
		
		if self.check_result(fish_soup, fish_url, 'Fish Processing Plants Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the title
			title_str = bsoup.get_text(fish_soup.find('h1', attrs={'class': 'page-title'}))

			# Get the description
			main_content = fish_soup.find('main', attrs={'class': 'content-body'})
			desc_p = main_content.find('p')
			desc_str = bsoup.get_text(desc_p)

			# Get the map URL
			map_a = main_content.find('a', attrs={'title': 'Map of BC Fish Processing Plants'})
			map_url = map_a['href']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', health_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Child Development & Family Support Services map

		child_url = self.pg_grp.get_url('child_url')
		child_soup = bsoup.get_soup(child_url)
		
		if self.check_result(child_soup, child_url, 'Child Development & Family Support Services Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(child_soup, 'Family Support Services', 'a')
			map_url = map_a['href']

			# Get the map soup
			map_soup = bsoup.get_soup(map_url, True, ['class', 'banner-title'])

			# Get the title
			title_str = bsoup.get_text(map_a)

			# Get the description
			#about_div = map_soup.find('div', attrs={'id': 'about-text'})
			#about_p = about_div.p
			##print title_div
			##print about_p
			##answer = raw_input("Press enter...")
			##desc_str = bsoup.get_text(about_p)
			#desc_str = 'Welcome to the Early Years Services Map. This map shows the locations and contact ' \
			#           'information for a variety of early years programs and services in BC. Early years programs ' \
			#           'include a range of early childhood development and family support services which help to ' \
			#           'promote the healthy growth and development of young children (0-6 years).'
			desc_str = bsoup.get_text(map_a.find_next_sibling())
			
			# Get the metadata of the main page to get the keywords
			child_mdata = bsoup.get_page_metadata(child_soup)
			keywords = child_mdata['keywords']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', child_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Geographical Names map

		geonames_url = self.pg_grp.get_url('geonames_url')
		geonames_soup = bsoup.get_soup(geonames_url)
		
		if self.check_result(geonames_soup, geonames_url, 'Geographical Names Main Page'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map URL
			map_a = bsoup.find_tags_containing(geonames_soup, 'Launch Application:', 'a')
			map_url = map_a['href']

			# Get the map soup
			map_soup = bsoup.get_soup(map_url)
			
			if map_soup is None:
				print "\nWARNING: Geographical Names map '%s' could not be opened." % map_url
				print "Please check the 'err_log.csv' file in the province/territory results folder."
				self.write_error(map_url, 'Geographical Names Map', 'Page could not be opened.')
				
				body_div = geonames_soup.find('div', attrs={'id': 'body'})
				title_h2 = body_div.find('h2')
				title_str = bsoup.get_text(title_h2)
				
				desc_p = title_h2.find_next_sibling('p')
				desc_str = bsoup.get_text(desc_p)
			else:
				# Get the title from the map page's title
				title_str = bsoup.get_text(map_soup.find('title'))

				# Get the description
				welcome_div = map_soup.find('div', attrs={'class': 'welcome'})
				p_list = welcome_div.find_all('p')
				desc_p = p_list[1]
				desc_str = bsoup.get_text(desc_p)
				
			# Get the metadata of the main page to get the keywords
			geonames_mdata = bsoup.get_page_metadata(geonames_soup)
			keywords = geonames_mdata['keywords']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', geonames_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Recreation Sites and Trails map

		rec_url = self.pg_grp.get_url('rec_url')[0]
		map_url = self.pg_grp.get_url('rec_url')[1]

		# Get the main page soup
		rec_soup = bsoup.get_soup(rec_url)

		# Get the map page soup
		map_soup = bsoup.get_soup(map_url)
		
		if self.check_result(map_soup, map_url, 'Recreation Sites and Trails Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the metadata of the page
			map_mdata = bsoup.get_page_metadata(map_soup)

			# Get the title and description
			title_str = map_mdata['page_title']
			desc_str = map_mdata['description']
			keywords = map_mdata['keywords']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', rec_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the MapPlace maps

		mapplace_url = self.pg_grp.get_url('mapplace_url')
		mapplace_soup = bsoup.get_soup(mapplace_url, True)
		
		if self.check_result(mapplace_soup, mapplace_url, 'MapPlace Maps'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			tables = mapplace_soup.find_all('table')

			#for table in tables:
			table = tables[4]

			table_rows = shared.table_to_dict(table, 0)

			#print "Table Rows:"

			for row in table_rows:
				# Get the title
				title_str = bsoup.get_text(row['available maps'])

				# Get the description
				desc_str = bsoup.get_text(row['general description'])

				# Get the map URL
				#print row['available maps']
				map_a = row['available maps'].a
				map_url = shared.get_anchor_url(map_a, mapplace_url)

				# Add all values to the CSV file object
				self.pt_csv.add('Source', 'BC Interactive Maps')
				self.pt_csv.add('Title', title_str)
				self.pt_csv.add('Description', desc_str)
				self.pt_csv.add('Type', 'Interactive Map')
				self.pt_csv.add('Download', 'No')
				self.pt_csv.add('Access', 'Viewable/Contact the Province')
				self.pt_csv.add('Web Map URL', map_url)
				self.pt_csv.add('Web Page URL', mapplace_url)

				self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Safe Harbour map

		harbour_url = self.pg_grp.get_url('harbour_url')
		harbour_soup = bsoup.get_soup(harbour_url, True, ['id', 'about-text'], delay=20)
		
		if self.check_result(harbour_soup, harbour_url, 'Safe Harbour Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the title from the map page's title
			#print harbour_soup.title
			title_str = ''
			title = harbour_soup.find('title')
			if title is not None: title_str = bsoup.get_text(title)
			
			if title_str == '': title_str = 'Safe Harbour Map'

			# Get the description
			about_div = harbour_soup.find('div', attrs={'id': 'about-text'})
			about_p = about_div.p
			if about_p is not None:
				desc_str = bsoup.get_text(about_div.p)
			else:
				desc_str = 'Safe Harbour: Respect for All creates opportunities for storefront businesses, ' \
					   'institutions, agencies, and entire municipalities to celebrate our differences, ' \
					   'helping to create safer, more welcoming communities that support diversity and ' \
					   'reject discrimination.'

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', harbour_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the DataBC Address Viewer

		databc_url = self.pg_grp.get_url('databc_url')
		databc_soup = bsoup.get_soup(databc_url)
		
		if self.check_result(databc_soup, databc_url, 'DataBC Address Viewer'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Find the map link
			map_a = bsoup.find_tags_containing(databc_soup, 'Launch Location Services', 'a')
			map_url = map_a['href']
			map_soup = bsoup.get_soup(map_url)

			# Get the title
			title_str = bsoup.get_text(map_soup.find('title'))

			mdata = bsoup.get_page_metadata(databc_soup)
			desc_str = mdata['description']
			
			keywords = mdata['keywords']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', databc_url)

			self.pt_csv.write_dataset()
			
		print

		#pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_services(self): #, subpage='all'):
		''' Extract all services for British Columbia
		:param subpage: The type of service to extract (for debug mode only).
		:return: None
		'''
		
		# Get the parameters
		subpage = self.get_arg_val('subpage')

		# NOTE: subpage is for debugging only
		if subpage is None: subpage = 'all'
		#subpage = 'all'

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		self.print_title("Extracting BC's map services")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		# Create the Maps CSV file
		csv_fn = "Services_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()

		if subpage == 'rest' or subpage == 'all':

			#######################################################################################
			# Get the ArcGIS REST Services

			rest_urls = self.pg_grp.get_url('rest_urls')

			if rest_urls is not None:
				for url in rest_urls:
				
					print "\nExtracting ArcGIS REST services for '%s'..." % url
					
					# Get a list of REST services
					rest_serv = services.PT_REST(url)

					# Get the service and add it to the CSV file
					lyr_info = rest_serv.get_layers()
					
					if not self.check_result(lyr_info, url, 'ArcGIS REST Map'): continue
					
					filter_rows = shared.process_duplicates(lyr_info)
					
					#print "\nAdding data from ArcGIS REST service for '%s' to CSV inventory..." % url
					for index, rec in enumerate(filter_rows):
						shared.print_oneliner("Adding %s of %s to CSV inventory" \
												% (index + 1, len(filter_rows)))
						for k, v in rec.items():
							pt_csv.add(k, v)
						
						pt_csv.add('Source', 'BC Map Services')
						pt_csv.write_dataset()
					
					print

		#######################################################################################
		# Get the WMS maps

		if subpage == 'wms' or subpage == 'all':

			wms_urls = self.pg_grp.get_url('wms_urls')
			
			for w in wms_urls:
				print w
			#answer = raw_input("Press enter...")

			for index, url in enumerate(wms_urls):
				print "Extracting layers from WMS '%s'..." % url
				
				wms = services.PT_WMS(url)
				
				ds_info = wms.get_data()
				
				#print ds_info
				
				print "Number of layers: %s" % len(ds_info['layers'])
				
				for idx, lyr in enumerate(ds_info['layers']):
					shared.print_oneliner("Adding %s of %s to CSV inventory" \
										% (idx + 1, len(ds_info['layers'])))
					for k, v in lyr.items():
						pt_csv.add(k, v)
				
					pt_csv.add('Source', 'BC Map Services')
					pt_csv.add('Publisher', ds_info['publisher'])
					pt_csv.write_dataset()
					
				print
					
				continue
			
				# xml_soup = bsoup.get_xml_soup(url)
				
				# if xml_soup is None:
					# print "\nWARNING: WMS '%s' could not be opened." % url
					# print "Please check the 'err_log.csv' file in the province/territory results folder."
					# self.write_error(url, 'WMS', 'Page could not be opened.')
					# continue

				# # Get the service info

				# # Get the type of service
				# serv_type = bsoup.get_text(xml_soup.find('name'))
				# if serv_type == '':
					# serv_type = bsoup.get_text(xml_soup.find('Name'))

				# # Get the service name
				# service_name = bsoup.get_text(xml_soup.find('title'))
				# if service_name == '':
					# service_name = bsoup.get_text(xml_soup.find('Title'))

				# # Get the description name
				# desc_str = bsoup.get_text(xml_soup.find('abstract'))
				# if desc_str == '':
					# desc_str = bsoup.get_text(xml_soup.find('Abstract'))

				# # Get the publisher
				# pub_str = bsoup.get_text(xml_soup.find('contactorganization'))
				# if pub_str == '':
					# pub_str = bsoup.get_text(xml_soup.find('ContactOrganization'))

				# #print "Number of layers: %s" % len(xml_soup.find_all('layer'))

				# # Get all the layers
				# layers = xml_soup.find_all('layer', attrs={'queryable': '1'})
				
				# print url
				# print "Number of layers: %s" % len(layers)
				
				# answer = raw_input("Press enter...")

				# if len(layers) > 0:
					# for lyr_idx, lyr in enumerate(layers):
						# #print bsoup.get_text(lyr.find('name'))
						
						# msg = "Adding layer %s of %s layers to CSV inventory" % (lyr_idx + 1, len(layers))
						# shared.print_oneliner(msg)

						# title_str = bsoup.get_text(lyr.find('name'))

						# # Add all values to the CSV file object
						# pt_csv.add('Source', 'BC Map Services')
						# pt_csv.add('Title', title_str)
						# pt_csv.add('Description', desc_str)
						# pt_csv.add('Publisher', pub_str)
						# pt_csv.add('Spatial Reference', 'Multiple')
						# pt_csv.add('Type', 'WMS')
						# pt_csv.add('Service', serv_type)
						# pt_csv.add('Service Name', service_name)
						# pt_csv.add('Service URL', url)
						# pt_csv.add('Download', 'No')
						# pt_csv.add('Access', 'Contact the Province')

						# pt_csv.write_dataset()
					# print
				# else:
					# layers = xml_soup.find_all('Layer', attrs={'opaque': '1'})
					# for lyr_idx, lyr in enumerate(layers):
						# #print bsoup.get_text(lyr.find('Title'))
						
						# msg = "Adding layer %s of %s layers to CSV inventory" % (lyr_idx + 1, len(layers))
						# shared.print_oneliner(msg)

						# title_str = bsoup.get_text(lyr.find('Title'))

						# # Add all values to the CSV file object
						# pt_csv.add('Source', 'BC Map Services')
						# pt_csv.add('Title', title_str)
						# pt_csv.add('Description', desc_str)
						# pt_csv.add('Publisher', pub_str)
						# pt_csv.add('Type', 'WMS')
						# pt_csv.add('Spatial Reference', 'Multiple')
						# pt_csv.add('Service Name', service_name)
						# pt_csv.add('Service URL', url)
						# pt_csv.add('Download', 'No')
						# pt_csv.add('Access', 'Contact the Province')

						# pt_csv.write_dataset()
					# print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_transpo_maps(self):
		''' Extracts British Columbia's transportation interactive maps
		:return: None
		'''

		# self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# # Create the Maps CSV file
		# csv_fn = "Maps_Transpo_results"
		# pt_csv = sh.PT_CSV(csv_fn, self)
		# pt_csv.open_csv()
		
		cur_page = 0
		page_count = self.pg_grp.get_page_count()
		
		self.print_title("Extracting BC's transportation interactive maps")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		#######################################################################################
		# Get the Stops of Interest map

		stops_url = self.pg_grp.get_url('stops_url')
		stops_soup = bsoup.get_soup(stops_url)
		
		if self.check_result(stops_soup, stops_url, 'Stops of Interest Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Get the map link from the sidebar
			map_img = stops_soup.find('img', attrs={'alt': 'Stop of Interest Signs Map'})
			map_a = map_img.parent
			map_url = map_a['href']

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(stops_soup)
			title_str = page_mdata['title']
			startdate_str = page_mdata['DCTERMS.created']
			date_str = page_mdata['DCTERMS.modified']
			desc_str = page_mdata['description']
			keywords = page_mdata['keywords']
			pub_str = page_mdata['DCTERMS.publisher']

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Keywords', keywords)
			self.pt_csv.add('Start Date', startdate_str)
			self.pt_csv.add('Recent Date', date_str)
			self.pt_csv.add('Publisher', pub_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', stops_url)

			self.pt_csv.write_dataset()

		#######################################################################################
		# Get the Traffic Data maps

		traffic_url = self.pg_grp.get_url('traffic_url')
		traffic_soup = bsoup.get_soup(traffic_url)
		
		if self.check_result(traffic_soup, traffic_url, 'Traffic Data Map'):
			# Print the status
			cur_page += 1
			msg = "Extracting web map %s of %s maps" % (cur_page, page_count)
			shared.print_oneliner(msg)
		
			# Set the title
			title_str = 'Traffic Data Map'

			#f = codecs.open('traffic.html', mode='w', encoding='utf-8')
			#f.write(unicode(traffic_soup))
			#f.close()

			# Get the corecontent <div>
			#print traffic_soup
			#core_div = traffic_soup.find('div', attrs={'id', 'mainbodycontainer'})

			#print core_div

			#h1 = bsoup.find_tags_containing(traffic_soup, 'Traffic Data Program', 'h1')
			h1 = traffic_soup.find('h1', attrs={'class': 'heading sizable'})
			core_div = h1.parent

			# Get the map link
			map_a = core_div.find('a')
			map_url = map_a['href']

			# Get the description
			h3 = core_div.find('h3')
			desc_p = h3.find_next_sibling('p')
			desc_str = bsoup.get_text(desc_p)

			# Add all values to the CSV file object
			self.pt_csv.add('Source', 'BC Interactive Maps')
			self.pt_csv.add('Title', title_str)
			self.pt_csv.add('Description', desc_str)
			self.pt_csv.add('Type', 'Interactive Map')
			self.pt_csv.add('Download', 'No')
			self.pt_csv.add('Access', 'Viewable/Contact the Province')
			self.pt_csv.add('Web Map URL', map_url)
			self.pt_csv.add('Web Page URL', traffic_url)

			self.pt_csv.write_dataset()

		#pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

	def extract_webpages(self):
		''' Extracts British Columbia's webpages with geospatial downloadable data
		:return: None
		'''

		self.print_log("\nExtracting from %s" % self.pg_grp.get_title())
		
		# Create the Maps CSV file
		csv_fn = "Webpages_results"
		pt_csv = sh.PT_CSV(csv_fn, self)
		pt_csv.open_csv()
		
		page_count = self.pg_grp.get_page_count()
		
		self.print_title("Extracting BC's web pages")
		
		start_time = datetime.datetime.now()
		print "Process started at: %s" % start_time

		url_list = self.pg_grp.get_url_list()

		for idx, url in enumerate(url_list):
			msg = "Extracting web page %s of %s pages" % (idx + 1, url)
			shared.print_oneliner(msg)
		
			soup = bsoup.get_soup(url)
				
			if not self.check_result(soup, url): continue

			# Get metadata info
			page_mdata = bsoup.get_page_metadata(soup)

			# Get the title
			if 'title' in page_mdata.keys():
				title_str = page_mdata['title']
			else:
				title_str = page_mdata['page_title']

			# Get the date
			if 'DCTERMS.modified' in page_mdata.keys():
				date_str = page_mdata['DCTERMS.modified']
			else:
				date_str = page_mdata['dc.date.modified']
				
			# Get the date
			if 'DCTERMS.keywords' in page_mdata.keys():
				keywords = page_mdata['DCTERMS.keywords']
			elif 'dc.keywords' in page_mdata.keys():
				keywords = page_mdata['dc.keywords']
			else:
				keywords = page_mdata['keywords']
				
			# Get the date
			if 'DCTERMS.created' in page_mdata.keys():
				startdate_str = page_mdata['DCTERMS.created']
			else:
				startdate_str = page_mdata['dc.date.created']

			# Get the description
			desc_str = page_mdata['description']

			# Get the publisher
			if 'DCTERMS.publisher' in page_mdata.keys():
				pub_str = page_mdata['DCTERMS.publisher']
			else:
				pub_str = page_mdata['dc.publisher']

			# Get a list of all anchors and locate the one with link containing '.kml'
			download_str = ''
			a_list = soup.find_all('a')
			for a in a_list:
				if a.has_attr('href'):
					if a['href'].find('.kml') > -1 or a['href'].find('.kmz') > -1:
						download_str = a['href']

			# Add all values to the CSV file object
			pt_csv.add('Source', 'BC Web Pages')
			pt_csv.add('Title', title_str)
			pt_csv.add('Description', desc_str)
			pt_csv.add('Start Date', startdate_str)
			pt_csv.add('Keywords', keywords)
			pt_csv.add('Recent Date', date_str)
			pt_csv.add('Publisher', pub_str)
			pt_csv.add('Type', 'File')
			pt_csv.add('Download', download_str)
			pt_csv.add('Access', 'Download/Web Accessible')
			pt_csv.add('Web Page URL', url)

			pt_csv.write_dataset()
			
		print

		pt_csv.close_csv()
		
		# Print ending time
		end_time = datetime.datetime.now()
		print "\nExtraction complete at %s." % end_time
		tot_time = end_time - start_time
		print "It took %s to complete." % tot_time

def main():
	#tool_list = ['REST', 'OpenData', 'GeoDiscover']

	ext = Extractor()

	try:
		pages = ext.get_pagelist()

		parser = argparse.ArgumentParser()
		parser.add_argument("-p", "--page", help="The page to extract: %s or all" % ', '.join(pages.keys()))
		parser.add_argument("-w", "--word", help="The key word(s) to search for.")
		parser.add_argument("-f", "--format", help="The format(s) to search for.")
		parser.add_argument("-s", "--silent", action='store_true', help="If used, no extra parameters will be queried.")
		args = parser.parse_args()
		# print args.echo

		# print "province: " + str(args.province)
		# print "format: " + str(args.format)

		page = args.page
		word = args.word
		formats = args.format
		silent = args.silent

		if page is None:
			answer = raw_input("Please enter the page you would like to use (%s or all): " % ', '.join(pages.keys()))
			if not answer == "":
				page = answer.lower()
			else:
				print "\nERROR: Please specify a tool."
				print "Exiting process."
				sys.exit(1)

		page = page.lower()

		print page

		ext.set_page(page)
		ext.run()

	except Exception, err:
		ext.print_log('ERROR: %s\n' % str(err))
		ext.print_log(traceback.format_exc())
		ext.close_log()


if __name__ == '__main__':
	sys.exit(main())

# -*- coding: utf-8 -*-
# =================================================================
#
# Author: Kevin Ballantyne <kevin.ballantyne@canada.ca>
# Date Created: February 6, 2019
#
# =================================================================

import os
import sys
import json
import collections
import re
import glob
import traceback
import requests
from owslib.csw import CatalogueServiceWeb
from owslib.util import http_post

from pycsw import __version__ as pycsw_version
from pycsw.server import Csw

#sys.path.append('C:\\FGP\\Development\\PT_WebExtractor\\scripts')

#print(sys.path)

#from common import shared

def run(xml_fn=None):

	port = '8000'
	
	#pycsw_url = 'http://localhost:%s/catalogue/csw' % port
	
	pycsw_url = 'http://localhost:%s/csw' % port
	
	if xml_fn is None or xml_fn == '':
		#local_csw = CatalogueServiceWeb('http://localhost:%s/catalogue/csw' % port)
		
		local_csw = CatalogueServiceWeb('http://localhost:%s/csw' % port)
		
		#fgp_csw = CatalogueServiceWeb('https://test.gcgeo.gc.ca/geonetwork/srv/eng/csw')
		
		in_folder = 'C:\\pycsw-2.2.0\\tests\\keballan\\XML_Importer\\xml_kevin2'
		
		xml_files = glob.glob('%s\\*.xml' % in_folder)
	else:
		if os.path.isdir(xml_fn):
			xml_files = glob.glob('%s\\*.xml' % xml_fn)
		else:
			xml_files = [xml_fn]
	
	for x in xml_files:
		# Try harvesting
		#local_csw.harvest('file:///%s' % x, 'http://www.isotc211.org/2005/gmd')
		
		# Try transaction
		xml_f = open(x)
		#local_csw.transaction(ttype='insert', typename='gmd:MD_Metadata', record=xml_f.read())
		print("Inserting '%s'" % x)
		xml_str = xml_f.read()
		print(http_post(url=pycsw_url, request=xml_str, timeout=30))

def main():

	try:
		# answer = raw_input("Please enter the number of results to import [all]: ")
		
		# if answer == '' or answer.lower().find('a') > -1 or answer.lower() == 'all':
			# total = None
		# else:
			# total = int(answer)
		
		xml_fn = None
		if len(sys.argv) > 1:
			xml_fn = sys.argv[1]
	
		run(xml_fn)
	except:
		print(traceback.format_exc())

if __name__ == '__main__':
	sys.exit(main())

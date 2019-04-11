import os
import sys
import traceback
import requests
from owslib.csw import CatalogueServiceWeb
from owslib.util import http_post
import xml.etree.ElementTree as ET
import collections

from common import pycsw_func

def run():

	answer = raw_input("This will delete every record in the database. Do you want to continue? [y/n]: ")
	
	if answer.lower().find('y') > -1:

		port = '8000'
		
		#pycsw_url = 'http://localhost:%s/catalogue/csw' % port
		
		pycsw_url = 'http://localhost:%s/csw' % port
		local_csw = CatalogueServiceWeb(pycsw_url)
		
		xml_str = '''<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service="CSW" version="2.0.2" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd">
	<csw:Delete>
		<csw:Constraint version="1.1.0">
			<ogc:Filter>
				<ogc:PropertyIsLike escapeChar="\" singleChar="?" wildCard="*">
					<ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
					<ogc:Literal>*</ogc:Literal>
				</ogc:PropertyIsLike>
			</ogc:Filter>
		</csw:Constraint>
	</csw:Delete>
</csw:Transaction>
'''
	
		response = http_post(url=pycsw_url, request=xml_str, timeout=30)
		
		print response
		
		resp_xml = ET.fromstring(response)
		
		# Convert response to dictionary
		resp_dict = collections.OrderedDict()
		for child in resp_xml.iter('*'):
			#print dir(child)
			#print child.text
			txt = child.text
			if txt:
				resp_dict[child.tag.split('}', 1)[1]] = child.text
			
		print("\nResponse:")
		for k, v in resp_dict.items():
			print('%s: %s' % (k, v))
			
def main():

	try:
		run()
	except:
		print(traceback.format_exc())

if __name__ == '__main__':
	sys.exit(main())
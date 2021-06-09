import os
import sys
import traceback
import requests
from owslib.csw import CatalogueServiceWeb
from owslib.util import http_post
import collections
import xml.etree.ElementTree as ET

from common import pycsw_func

def run():

	answer = input("This will delete every record in the database. Do you want to continue? [y/n]: ")
	
	if answer.lower().find('y') > -1:

		port = '8000'
		
		#pycsw_url = 'http://localhost:%s/catalogue/csw' % port
		
		pycsw_url = 'http://localhost:%s/csw' % port
		local_csw = CatalogueServiceWeb(pycsw_url)
		
		#local_csw.transaction(ttype='delete', typename='gmd:MD_Metadata')
		
		# Get the total number of records
		get_post = '''<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords
    service="CSW"
    version="2.0.2"
    resultType="results"
    outputFormat="application/xml"
    outputSchema="http://www.opengis.net/cat/csw/2.0.2"
    xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"
    xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xmlns:gml="http://www.opengis.net/gml"
    xmlns:ows="http://www.opengis.net/ows"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <csw:Query typeNames="csw:Record">
        <csw:ElementSetName typeNames="gmd:MD_Metadata">full</csw:ElementSetName>
        <csw:Constraint version="1.1.0">
            <Filter
                xmlns="http://www.opengis.net/ogc"
                xmlns:gml="http://www.opengis.net/gml">
                <PropertyIsLike wildCard="*" singleChar="_" escapeChar="\"> 
                    <PropertyName>csw:AnyText</PropertyName> 
                    <Literal>*</Literal> 
               </PropertyIsLike> 
            </Filter>
        </csw:Constraint>
    </csw:Query>
</csw:GetRecords>'''

		get_response = http_post(url=pycsw_url, request=get_post, timeout=30)
		
		rec_total = 0
		res_xml = ET.fromstring(get_response)
		children = res_xml.getchildren()
		for child in children:
			tag_name = child.tag
			if tag_name.find('SearchResults') > -1:
				rec_total = child.get('numberOfRecordsMatched')
		
		for t in range(1, int(rec_total), 100):
			local_csw.getrecords2(maxrecords=10000)
			all_res = local_csw.records
			
			# Build the xml list
			filter_xml = ''
			for r in all_res:
				filter_xml += '''
					<ogc:PropertyIsLike escapeChar="\" singleChar="?" wildCard="*">
						<ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
						<ogc:Literal>%s</ogc:Literal>
					</ogc:PropertyIsLike>
				''' % r
			
			xml_str = '''<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service="CSW" version="2.0.2" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd">
		<csw:Delete>
			<csw:Constraint version="1.1.0">
				<ogc:Filter>
					<ogc:Or>
						%s
					</ogc:Or>
				</ogc:Filter>
			</csw:Constraint>
		</csw:Delete>
	</csw:Transaction>
	''' % filter_xml

			response = http_post(url=pycsw_url, request=xml_str, timeout=30)
				
			pycsw_func.print_response(response)
		
		# for rec in all_res:
			# xml_str = '''<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service="CSW" version="2.0.2" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd">
	# <csw:Delete>
		# <csw:Constraint version="1.1.0">
			# <ogc:Filter>
				# <ogc:PropertyIsLike escapeChar="\" singleChar="?" wildCard="*">
					# <ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
					# <ogc:Literal>%s</ogc:Literal>
				# </ogc:PropertyIsLike>
			# </ogc:Filter>
		# </csw:Constraint>
	# </csw:Delete>
# </csw:Transaction>
# ''' % rec
	
			# response = http_post(url=pycsw_url, request=xml_str, timeout=30)
			
			# pycsw_func.print_response(response)
			
		# xml_str = '''<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service="CSW" version="2.0.2" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd">
	# <csw:Delete>
		# <csw:Constraint version="1.1.0">
		  # <ogc:Filter>
			# <ogc:PropertyIsLike wildCard="%" singleChar="." escapeChar="\">
			  # <ogc:PropertyName>dc:identifier</ogc:PropertyName>
			  # <ogc:Literal>%</ogc:Literal>
			# </ogc:PropertyIsLike>
		  # </ogc:Filter>
		# </csw:Constraint>
	# </csw:Delete>
# </csw:Transaction>'''

		# response = http_post(url=pycsw_url, request=xml_str, timeout=30)
		
		# pycsw_func.print_response(response)
			
def main():

	try:
		run()
	except:
		print(traceback.format_exc())

if __name__ == '__main__':
	sys.exit(main())
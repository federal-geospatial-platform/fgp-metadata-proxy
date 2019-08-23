import os
import sys
import xml.etree.ElementTree as ET
import collections

def add_transaction_tags(in_xml, trans_type='insert'):

	if trans_type == 'insert':
		out_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction xmlns="http://www.opengis.net/cat/csw/2.0.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0.2" service="CSW" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd                        http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20070417/gmd/metadataEntity.xsd">
	<Insert>
		%s
	</Insert>
</Transaction>''' % in_xml.decode("utf-8").strip("'")
	elif trans_type == 'update':
		out_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction xmlns="http://www.opengis.net/cat/csw/2.0.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0.2" service="CSW" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd                        http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20070417/gmd/metadataEntity.xsd">
	<Update>
		%s
	</Update>
</Transaction>''' % in_xml.decode("utf-8").strip("'")

	return out_xml

def print_response(response):

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
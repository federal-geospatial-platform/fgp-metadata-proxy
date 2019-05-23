import fme
import fmeobjects
import urllib2
import requests

# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def processFeature(feature):
    pass

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class FeatureProcessor(object):
    
    def __init__(self):
        pass
        
        self.csw_url = fme.macroValues['CSW_URL']
        
    def input(self,feature):
        self.xml_str = feature.getAttribute('_xml_output')
        self.xml_str = self.xml_str.encode('utf-8')
        
        request_str = self.post_xml()
        
        feature.setAttribute('insert_response', request_str)
        
        self.pyoutput(feature)
        
    def post_xml(self):
        headers = {'Content-Type': 'text/xml; charset=utf-8'} # set what your server accepts
        
        return requests.post(self.csw_url, data=self.xml_str, headers=headers).text
        
    def close(self):
        pass
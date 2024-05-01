import fme
import fmeobjects
import requests
import urllib3
import urllib.parse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import sys
from Python.FME_utils import FME_utils

try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names
HTTP_CALL_ERROR = "_http_call_error"
RESPONSE_BODY = "_response_body"
STATUS_CODE = "_status_code"
STATUS_CODE_DESCRIPTION = "_status_code_description"
URL_SOCRATA = "_url_socrata"

# FME attribute value

#Define Socrata attribute
ID = "id"

# Define http return code
HTTP_OK = 200


# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class ManageHttpCall(object):
    """This class enables the call to Socrata GeoHub servers and the creation of FME features with Socrata information.
    
    To extract all the information the Socrata reader makes a first http call to extract all the IDs then a second 
    http call is done to extract the information of each ID.  The information is finally stored in FME attributes.      
    """

    def __init__(self):
        """Constructor of the class.
        
        Creates the logger to log information in FME log.
        """
        
        self.logger = fmeobjects.FMELogFile()
        """Read the JSON metadata record from the secondary DCAT server and output the JSON in FME feature.
        
        Parameters
        ----------
         feature FME Feature object
            The FME feature to process
            
        Returns
        -------
        None
        """
        
    def read_socrata(self, feature):
        """Read the JSON metadata record from the Socrata server and output the JSON in FME feature.
        
        In order to read the metadata record a first http call is done to extract all the identifiers (id)
        then a second Socrata read is done to read the fulle content of each id.
        
        Parameters
        ----------
         feature FME Feature object
            The FME feature to process
            
        Returns
        -------
        None
        """
        
        # Create a session to be used to make http request
        session = FME_utils.create_session()
        
        url_socrata_views = self.url_socrata + "/api/views"
    
        # Get the header of the web service
        response = FME_utils.make_http_call(self, feature, session, url_socrata_views,timeout=30)
   
        # Extarct information
        json_response = response.json()
        
        for item in json_response:
            try:
                id = item[ID]
                url_socrata_id = self.url_socrata + "/api/views/{0}".format(id)
                # Get the response of the web service
                response_id = FME_utils.make_http_call(self, feature, session, url_socrata_id)
                # Extarct information
                json_response_id = response_id.json()
                str_json_dataset = json.dumps(json_response_id)
                lst_key_val_att = [(ID, id), 
                                   (STATUS_CODE, HTTP_OK), 
                                   (RESPONSE_BODY, str_json_dataset)]
                # Oiutput FME feature
                FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
            except KeyError:
                # Badly formed JSON document
                self.logger.logMessageString ('JSON file has no "id" entry: {}'.format(json.dumps(item)), fmeobjects.FME_ERROR)
    
    def input(self,feature):
        """Main routine call be the FME software
        
        Manage the reading of Socrata server for all the records
        
        Parameters
        ----------
        feature: FME Feature object 
            FME Feature to process
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        # Extract the attribute of url Socrata
        self.url_socrata = FME_utils.feature_get_attribute(feature, URL_SOCRATA)
        
        # Read the Socrata server
        self.read_socrata(feature)
                    
    def close(self):
        """Unused method"""
        pass

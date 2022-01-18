import fme
import fmeobjects
import requests
import urllib3
import urllib.parse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import sys
from FME_utils import FME_utils

try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names
ID = "_id"
DCAT_P_IDENTIFIER = "DCAT_P_identifier"
DCAT_S_SLUG_ID = "DCAT_S_slug_id_"
HTTP_CALL_ERROR = "_http_call_error"
RESPONSE_BODY_P = "_response_body_P"
RESPONSE_BODY_S = "_response_body_S"
ROOT_URL = "_root_url"
STATUS_CODE = "_status_code"
STATUS_CODE_DESCRIPTION = "_status_code_description"
TYPE_REQUETE = "_type_requete"

# FME attribute value
DCAT_PRIMARY = "DCAT-PRIMARY"
DCAT_SECONDARY = "DCAT-SECONDARY"
DCAT_ID_UNKNOWN = "DCAT_id_unknown"
SLUG_ID_UNKNOWN = "SLUG_id_unknown"

# Define http return code
HTTP_OK = 200

# Define SK_GEOHUB_SECONDARY call
SK_GEOHUB_SECONDARY = "https://geohub.saskatchewan.ca/api/v3/datasets?filter[owner]=Saskatchewan.Government&page[number]=1&page[size]=25"

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class ManageHttpCall(object):
    """This class enables the call to DCAT GeoHub servers and the creation of FME features with DCAT information.
    
    To extract all the information the DCAT reader must read into a primary and a secondary server.
    The results from the DCAT servers are stored in the FME Feature attributes (*_response_body_P* and _response_body_S).
    For each FME Feaure the result from the DCAT reading is stored in the FME Feature attribute *_status_code* and the 
    description of the result code in the attribute *_status_code_attribute*.
      
    """

    def __init__(self):
        """Constructor of the class.
        
        Creates the logger to log information in FME log.
        """
        
        self.logger = fmeobjects.FMELogFile()
        
    def read_secondary_json(self, feature):
        """Read the JSON metadata record from the secondary DCAT server and output the JSON in FME feature.
        
        Parameters
        ----------
         feature FME Feature object
            The FME feature to process
            
        Returns
        -------
        None
        """
        
        # Convert special character in URL (ex.: white space for "%20")
        str_http = urllib.parse.quote(SK_GEOHUB_SECONDARY, safe="/:&?.=")
        
        # Create a session to be used to make http request
        session = FME_utils.create_session()
    
        while str_http is not None:
            # Get the header of the web service
            response = FME_utils.make_http_call(self, feature, session, str_http)
        
            # Extarct information
            json_response = response.json()
            datasets = json_response["data"]
            # Output the FME feature with in attribute the JSON file
            for json_dataset in datasets:
                try:
                    slug_id = json_dataset["attributes"]["slug"]
                except KeyError:
                    slug_id = SLUG_ID_UNKNOWN
                str_json_dataset = json.dumps(json_dataset)
                lst_key_val_att = [(DCAT_S_SLUG_ID, slug_id), 
                                   (STATUS_CODE, HTTP_OK), 
                                   (RESPONSE_BODY_S, str_json_dataset)]
                FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
            
            # Check for the next request to read
            try:
                str_http = json_response["links"]["next"]
            except KeyError:
                # When the key is missing it's the end of the search
                str_http = None
        
        return
            
    def read_primary_json(self, feature):
        """Read the JSON metadata record from the primary DCAT server and output the JSON in FME feature.
        
        Parameters
        ----------
         feature FME Feature object
            The FME feature to process
            
        Returns
        -------
        None
        """
        
        str_http = self.root_url
        
        # Create a session to be used to make http request
        session = FME_utils.create_session()
    
        # Get the header of the web service
        response = FME_utils.make_http_call(self, feature, session, str_http)
        
        # Extarct information
        json_response = response.json()
        datasets = json_response["dataset"]
        # Output the FME feature with in attribute the JSON file
        for json_dataset in datasets:
            try:
                id = json_dataset["identifier"]
                if "datasets/" in id:
                   splitter = "datasets/"
                else:
                   splitter = "maps/"
                txt_split = id.split(splitter)
                if len(txt_split) == 2:
                   dcat_id = txt_split[1]
                else:
                   dcat_id = DCAT_ID_UNKNOWN  # Unable to extract the ID
            except KeyError:
                   dcat_id = DCAT_ID_UNKNOWN  # Unable to extract the ID
            str_json_dataset = json.dumps(json_dataset)
            lst_key_val_att = [(DCAT_P_IDENTIFIER, dcat_id), 
                               (STATUS_CODE, HTTP_OK), 
                               (RESPONSE_BODY_P, str_json_dataset)]
                               
            FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
    
    def input(self,feature):
        """Main routine call be the FME software
        
        Manage the reading of CKAN server for all or by id (one record only)
        
        Parameters
        ----------
        feature: FME Feature object 
            FME Feature to process
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()

        # Extract feature attributes
        self.root_url = feature.getAttribute(ROOT_URL)
        self.root_url = FME_utils.feature_get_attribute(feature, ROOT_URL)
        
        # Extract the type of request
        self.type_requete = feature.getAttribute(TYPE_REQUETE)
        self.type_requete = FME_utils.feature_get_attribute(feature, TYPE_REQUETE)
                    
        # Execute the requested type of request
        if self.type_requete == DCAT_PRIMARY:
            self.read_primary_json(feature)  # Extract from primary server
        elif self.type_requete == DCAT_SECONDARY:
            self.read_secondary_json(feature)  # Extract from secondary server
        else:
            pass
            
 
    def close(self):
        """Unused method"""
        pass

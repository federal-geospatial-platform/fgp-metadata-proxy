import fme
import fmeobjects
import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import sys

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names
ID = "_id"
OPEN_MAP_FILTER = "_OpenMapsFilter"
HTTP_CALL_ERROR = "_http_call_error"
ROOT_URL = "root_url"
TYPE_REQUETE = "_type_requete"

# FME request
CKAN_ALL_RECORDS = "CKAN-AllRecords"
CKAN_BY_ID = "CKAN-ByID"
CSW_ALL_RECORDS = "CSW-AllRecords"
CSW_BY_ID = "CSW-ByID"

MAX_RECORD_READ = 50

# Define JSON keyword
RESULT = "result"
RESULTS = "results"

HTTP_ADDRESS_CKAN = "{0}/package_search?start={1}&rows={2}{3}"
    

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class ManageHttpCall(object):
    def __init__(self):
        
        self.logger = fmeobjects.FMELogFile()
        
    def make_http_call(self, feature, session, str_http):
    
        try:
            response = session.get(str_http, verify=False, timeout=10)
            self.logger.logMessageString("HTTP call: {0}".format(str_http), 
                                         fmeobjects.FME_INFORM)
        except Exception as err:
            # Mange the case where an error occured during the reading of the CKAN server
            self.logger.logMessageString("HTTP call error: {0}".format(err), 
                                         fmeobjects.FME_ERROR)
            feature.setAttribute (HTTP_CALL_ERROR, "True")
            self.pyoutput(feature)  # Send a feature to the Terminator
            sys.exit(1)

        return response
    
    def create_session(self, http_address):
        """This method creates a http session.
        
        Parameters
        ----------
        http_address: str
            The http address used to create a session
            
        Returns
        -------
        Session
            Session to use to make http requests
        """
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1.0,
                        status_forcelist=[ 500, 502, 503, 504 ])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        return session
    
    def read_ckan_records(self, feature, session, first_id, number_to_read):
        """This method reads the requested records from a CKAN web site.
        
        Parameters
        ----------
        from: int
            Record number of the first record to read
        number_to_read: int
            Number of record to read in the CKAN web site
            
        Returns
        -------
        List
            List of CKAN JSON records
        """    
        
        head = first_id
        last_id = first_id + number_to_read - 1
        while head <= last_id:
            if last_id - head + 1 >= MAX_RECORD_READ:
                read_size = MAX_RECORD_READ
            else:
               read_size = last_id - head + 1
            
            # Form the HTTP call 
            str_http_read = HTTP_ADDRESS_CKAN.format(self.root_url, head, read_size, self.open_map_filter)
            response = self.make_http_call(feature, session, str_http_read)  # Read the CKAN server
            head += read_size
            try:
                json_response = response.json()
                result = json_response[RESULT]
                results = result[RESULTS]
            except Exception as err:
                # Mange the case where the JSON is not well formed
                self.logger.logMessageString("JSON response is not well formed: {0}".format(err), 
                                             fmeobjects.FME_ERROR)
                feature.setAttribute (HTTP_CALL_ERROR, "True")
                self.pyoutput(feature)  # Send a feature for the Terminator
                sys.exit(1)
            
            
            
            # Output the FME feature with in attribute the JSON file
            for json_result in results:
                str_json_result = json.dumps(json_result)
                cloned_feature = feature.clone()
                cloned_feature.setAttribute("_response_body", str_json_result)
                self.pyoutput(cloned_feature)
            
    def read_ckan_all(self, feature):
        """This method read one record from the CKAN web site
    
        Parameters
        ----------
        feature: FME FeatureProcessor
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        str_http = HTTP_ADDRESS_CKAN.format(self.root_url, 0, 1, self.open_map_filter)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
    
        # Get the header of the web service
        response = self.make_http_call(feature, session, str_http)
        self.logger.logMessageString("HTTP call: {0}".format(str_http), fmeobjects.FME_INFORM)
      
        json_response = response.json()
        result = json_response["result"]
        count = int(result["count"])

        self.read_ckan_records(feature, session, 0, count)
    
    def read_ckan_one_id(self, feature):
        """This method read one  record from the CKAN web site
    
        Parameters
        ----------
        feature: FME FeatureProcessor
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        str_http = HTTP_ADDRESS_CKAN.format(self.root_url, 0, 1, self.open_map_filter)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
        
        id = feature.getAttribute(ID)
    
        # read the requested record
        self.read_ckan_records(feature, session, id, 1)
    
    def input(self,feature):
    
#        web_pdb.set_trace()
        # Extract the target URL
        self.root_url = feature.getAttribute(ROOT_URL)
        
        # Extract the open map filter
        self.open_map_filter = feature.getAttribute(OPEN_MAP_FILTER)
        if self.open_map_filter is None or self.open_map_filter == "":
            self.open_map_filter = ""
        else:
            self.open_map_filter = "&" + self.open_map_filter  # & is for a web parameter
            
        # Extract the type of reuqest
        type_requete = feature.getAttribute(TYPE_REQUETE)
            
        # Execute the request
        if type_requete == CKAN_ALL_RECORDS:
            self.read_ckan_all(feature)
        elif type_requete == CKAN_BY_ID:
            self.open_map_filter = ""  # Reset open map filter
            self.read_ckan_one_id(feature)
 
    def close(self):
        pass

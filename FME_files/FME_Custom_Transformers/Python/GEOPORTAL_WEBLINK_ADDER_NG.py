#
# Ce fichier contient le ccode python appelé le Custom Transformer
# GEOPORTAL_WEBLINK_ADDER_NG

import fme
import fmeobjects
import requests
from Python.FME_utils import CsvKeyValuePair
from Python.FME_utils import FME_utils

# Constants

# FME attribute name


# FME published parameter as attributes
HTTP_STATUS_CODE = "_http_status_code"
ORDER = "_order"
URL_VALIDATION = "_url_validation"
WEBLINK_WILDCARD = "_weblink_wildcard"

# FME attribute value
HTTP_OK = "200"
YES = "yes"

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

class FeatureProcessor(object):
    """This class implement the design pattern: *Processing Composite Data*"""
    
    def __init__(self):
        """This constructor method created a dictionary and a list to store the features."""
       
        self.csv_features = {}  # Create a dictionary to load the CSV features
        self.meta_features = []  # Create list to load the metadata features
        
        # Create logger for loggin into FME
        self.logger = fmeobjects.FMELogFile()
        
        # Use one session that will be used by all http head reuqest to save time
        self.session = FME_utils.create_session()  # Create an http session
        
    def input(self,feature):
        """Load the incoming features.
        
        The features from the CSV (_order=1) are stored in a dictionary according to the unique 
        format name. The  metadata features (_order=2) or stored in a list.
        
        Parameters
        ----------
        feature: FmeFeature object
            Feature object to process
        
        Returns
        -------
        None
        """
   
        order = feature.getAttribute(ORDER)
        if order == 1:
            # Read the attributes from the CSV features into a dictionary
            default_key = feature.getAttribute("default_key")
            default_value = feature.getAttribute("default_value")
            self.csv_features[default_key] = default_value # Add a new item in the dictionary
        else:
            # Load the metadata features
            self.meta_features.append(feature)
                    
    def _add_resources(self, feature, test_url):
        """Add the key value pair of the CSV into an extra resources{} list.
        
        Key-Value pair are added as is except if the key is URL than the web link 
        is added as the value of the URL
        
        Parameters
        ----------
        feature: FmeFeature
            Feature object to process
        test_url: String
            The URL address to add
        
        Returns
        -------
        None
        """
    
        # Count the number of ressouces{} in the attribute list
        max_index = FME_utils.max_index_attribute_list(feature, "resources{}")
        max_index += 1  # Add one ressources
        
        for key, value in self.csv_features.items():
            if key == "url":
                # Update the value if the key is "url"
                value = test_url
             
            # Add attribute to the FME feature
            resources_name = "resources{%d}.%s"%(max_index, key)  # Set the attribute name
            feature.setAttribute(resources_name, value)  # Set the attribute
            
        return
    
    def close(self):
        """Map the requested attribute.
        
        The following tasks are performed:
        
         - Extract the url to test (attribute test_url)
         - Extract the flag for the URL validation
         - Build the http to validate
         - Add an extra resource at the end of the ressources{} list with the
           values from the CSV file and change the value of the URL with the 
           url used to test the link
           
        """         
        
#        web_pdb.set_trace()
        # Extract the URL for testing
        try:
            url_value = self.csv_features["url"]
        except KeyError:
            url_value = ""  # In case the url entry is missing
        
        # Loop over each FME features
        for feature in self.meta_features:
        
            # Check if URL validation is requested
            bool_url_validation = FME_utils.test_attribute_value(feature, URL_VALIDATION, YES, False)
            
            # Extract the suffix to build the http requested
            suffix = feature.getAttribute("_weblink_wildcard")
            if url_value == "":
                # test url is empty
                test_url = suffix
            else:
                # Test url is not empty
                test_url = url_value + "/" + suffix  # Build the http request

            if bool_url_validation:
                # Test if the url link is responding with a http head call (faster than get)
                response = self.session.head(test_url, verify=False, timeout=10, 
                                             allow_redirects=True)
                status_code = str(response.status_code)
                self.logger.logMessageString("Status code: {0};  HTTP request head:   {1}"
                                             .format(status_code, test_url), fmeobjects.FME_INFORM)
            else:
                # Do not test if the link is valid and simulate a valid request
                status_code = HTTP_OK
            
            # Set the status code attribute
            feature.setAttribute(HTTP_STATUS_CODE, status_code)    
            if status_code == HTTP_OK:
                # Add the key-value pairs contained in the CSV in the ressources{} list
                self._add_resources(feature, test_url)
                
            
                    
            # Output the feature to FME after processing all the attributes
            self.pyoutput(feature)
                
        return
                
            
            
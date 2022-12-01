import re
import requests
import sys, os
import traceback
import urllib3
import yaml
import urllib.request
import lxml
from ftplib import FTP, FTP_TLS
from typing import NamedTuple
from urllib.parse import urlparse
from urllib.parse import unquote
from urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.error

try:
    import fme
    import fmeobjects
except:
    pass
    


try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass


# FME attribute name
STATUS_CODE = "_status_code"
STATUS_CODE_DESCRIPTION = "_status_code_description"

# Define HTTP OK return code
HTTP_OK = 200  # Satus OK
HTTP_MOVED = 301  # Status moved permanetly
HTTP_REDIRECTION = 302  # URL redirection

# The general timeout used by the http requests
TIMEOUT = 5

class CsvKeyValuePair(NamedTuple):
    """Class containing one row from a CSV defining a key-Value pair.
    
    Attributes:
    
    key : str
        Key name of a Key-Value pair
    value : str
        Value name of a Key-Value pair
    """
    
    key: str
    value: str
    
    
class CsvMetaDataFormatMapper(NamedTuple):
    """Class containing one row from the CSV used by METADATA_VALUE_MAPPER_NG.
    
    Attributes:
    
    original_value : str
        Original value that can be found in the metadata record
    real_value : str
        Name that replace the original value
    resource_type_en : str
        Name of the English resource
    resource_type_fr : str
        Name of the French resource
        
    """
    original_value: str
    real_value: str 
    resource_type_en: str 
    resource_type_fr: str

class CsvMetaDataValueMapper(NamedTuple):
    """Class containing one row from the CSV used by METADATA_VALUE_MAPPER_NG.
    
    Attributes:
    
    original_value : str
        Original value that can be found in the metadata record
    value_english : str
        English value that replace the original value
    value_french : str
        French value that replace the original value
    code_value : str
        Code value for this value
    """
    
    original_value: str
    value_english: str
    value_french: str
    code_value: str
    
  
class CsvGeoSpatialValidation(NamedTuple):
    """Class containing one row from the CSV GeoSpatialValidation.
    
    Attributes:
    
    fgp_publish : str
        Flag (oui/non) indicating if this format is published in the FGP
    format : str
        Name of the format
    spatial_type : str
        Spatial type code
    """
    
    fgp_publish: str
    format: str
    spatial_type: str

class FME_utils:
    
    @staticmethod
    def extract_url_html(url_to_read):
        """This method reads the html source code from a website.
        
        The method will also pass the html source code into BeautifulSoup
        in order to correct badly (when possible) badly formed html source code.
        
        Parameters
        ----------
        url_to_read : str
            URL address to read.
        
        Returns
        -------
        str
            The html source code read from the url.
        """
        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        try:
            logger.logMessageString("HTTP call: {0}".format(url_to_read), fmeobjects.FME_INFORM)
            httprequest = urllib.request.Request(url_to_read, headers={"Accept": "text/html",'User-Agent': 'Mozilla/5.0'})
            response=urllib.request.urlopen(httprequest)
            html_str = response.read()
        except:
            logger.logMessageString("Unable to read the URL: {}".format(url_to_read), fmeobjects.FME_ERROR)  
            raise Exception
            

        try:
            # First try to parse the html code with html.parser
            soup = BeautifulSoup(html_str, "html.parser")
            xhtml_str = soup.prettify()
        except:
            try:
                # Second try to parse the html with lxml
                soup = BeautifulSoup(html_str, "lxml")
                xhtml_str = soup.prettify()
            except:
                logger.logMessageString("Unable to parse the html source code from: {}".format(url_to_read), fmeobjects.FME_ERROR)
                xhtml_str = ""
                
        return xhtml_str
    
    @staticmethod
    def extract_attribute_list(feature, att_name):
        """This method extracts a subset of the attributes of a feature.
        
        If the the attribute name to extract is not an FME list (ex.: value) than only one 
        attribute is extracted.
        
        If the attribute name to extract is a list (ex.: ressources{}.name) than all the
        attributes of the list is extrated.
        
        The method returns a list of tuple one tuple for each attribute to extract. The 
        tuple is composed of 2 values the first is the complete attribute name: 
        ex.: value for none list attribute or ressources{1}.name for list attribute.  The 
        seconde value of the list is the index value: None for non list attribute or "1" for 
        ressources{1}.name for list attribute.
        
        Parameters
        ----------
        feature : FME Feature
            FME feature to process
        att_name : str
            The name of the attribute to extract
        
        Returns
        -------
        list
            A list of FME attribute.  
        """

        #web_pdb.set_trace()
        atts = []
        feature_atts = feature.getAllAttributeNames()  # Extract all attribute names
        logger = fmeobjects.FMELogFile()
        regex_list = "\{\d+\}"
        regex_index = "\d+"

        if att_name.find("{}") != -1:
            if att_name.endswith("{}"):
                # Search for all the attributes of a list (ex.: resources{})
                att_name = "^" + att_name
            else:
                # Search for specific attributes of a list (ex.: resources{}.name)
                att_name = "^" + att_name + "$"
            regex_search = att_name.replace("{}", regex_list)
            for feature_att in feature_atts:
                att_lst = re.match(regex_search , feature_att)  # Check if attribute name is present
                if att_lst is not None:
                    index_lst = re.findall(regex_list, att_lst[0])  # Extract the index with "{}"
                    if len(index_lst) == 1:
                        index = re.findall(regex_index, index_lst[0])  # Extract the index number
                        if len(index) == 1:
                            if index[0].isdigit():  #Validate index is a number
                                atts.append((int(index[0]), feature_att))
                            else:
                                logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
                        else:
                            logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
                    else:
                        logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
        else:
            # The attribute to search is not a list
            for feature_att in feature_atts:
                if att_name == feature_att:
                    atts.append((None, att_name))
                    break
        # Sort the list indexes as FME getAllAttributeNames break the order of the list
        atts.sort()

        return atts
        
    @staticmethod
    def max_index_attribute_list(feature, list_name):
        """This method returns the maximum index number of an attribute list.
        
        This method only works with a FME attribute list and returns the maximum index
        for an attribute list even if there is hole in the list it will return the
        maximum index number. So for the list name: att{} if the feature has the following
        attribute: att{0}.name and att{3}.value. The method will return 3. If there is no
        list, the returned value is -1.
        
        Parameters
        ----------
        feature : FME Feature
            FME feature to process
        list_name : str
            The name of the list to search including the "{}" characters (ex.: "att{}")
        
        Returns
        -------
        Int
            Maximum index number in the list.  
        """

#        web_pdb.set_trace()
        count = -1
        feature_atts = feature.getAllAttributeNames()  # Extract all attribute names
        logger = fmeobjects.FMELogFile()
        regex_list = "\{\d+\}"
        regex_index = "\d+"

        att_name = list_name
        if att_name.find("{}") != -1:
            # The attribute to search is a list
            att_name = "^" + att_name  # Regular expression exact match
            regex_search = att_name.replace("{}", regex_list)
            for feature_att in feature_atts:
                att_lst = re.match(regex_search , feature_att)  # Check if attribute name is present
                if att_lst is not None:
                    index_lst = re.findall(regex_list, att_lst[0])  # Extract the index with "{}"
                    if len(index_lst) == 1:
                        index = re.findall(regex_index, index_lst[0])  # Extract the index number
                        if len(index) == 1:
                            if index[0].isdigit():  #Validate index is a number
                                if int(index[0]) > count:
                                    count = int(index[0])
                            else:
                                logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
                        else:
                            logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
                    else:
                        logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
        else:
            # The attribute to search is not a list
            logger.logMessageString("Not valid list name: {}".format(att_name), fmeobjects.FME_WARN)

        return count

    @staticmethod
    def repair_attribute_list(feature, att_list_name, default_att_name=None):
        """This method repairs a list by creating the missing attribute in a list.
        
        For example if the list resources{} contains the following attributes:
        
          - resources{0}.a
          - resources{1}.a
          - resources{1}.b
          - resources{3}.a
          
        This method will create with empty values the following missing attribute:
        
          - resources{0}.b
          - resources{2}.a
          - resources{2}.b
          - resources{3}.b
        
        Parameters
        ----------
        feature: FME feature
            FME feature to process
        att_list_name: list
            Name of the attribute to extract (ex: values{})
        default_att_name: list
            List of attribute that will be added to the feature even if none is present
            
        Returns
        -------
        None
        """

        # Managing mutable default values
        if default_att_name is None:
            att_names = []
        else:
            att_names = list(default_att_name)
        max_index = -1
        regex_list = "\{\d+\}"
        regex_index = "\d+"
        logger = fmeobjects.FMELogFile()
        
    #    web_pdb.set_trace()
        if att_list_name.find("{}") != -1:    
            # Extract only the attribute to process
            attributes = FME_utils.extract_attribute_list(feature, att_list_name)
            
            for index, attribute in attributes:
                if index > max_index:
                    max_index = index  # Set the maximum index number
                    
                # Build the list of names (after the dot; ex: att{99}.name)
                att_split = attribute.split(".")
                att_name = att_split[1]
                if att_name not in att_names:
                   att_names.append(att_name)  # Update the list
                   
            # Repair the missing attributes names in the attribute list
            for index in range(max_index+1):
                for att_name in att_names:
                    attribute = att_list_name.replace('{}', '{%i}') + '.' + att_name
                    attribute = attribute%index  # Add the index number 
                    if not feature.getAttribute(attribute):
                        feature.setAttribute(attribute, '')
                        
            # Validate reparation
            attributes = FME_utils.extract_attribute_list(feature, att_list_name)
            if len(attributes) == (max_index+1) * len(att_names):
                # Reparation works
                pass
            else:
                logger.logMessageString("Internal error: {}".format(att_list_name), fmeobjects.FME_ERROR)
                        
        else:
            logger.logMessageString("Not a valid attribute list: {}".format(att_list_name), fmeobjects.FME_WARN)    

        return

    @staticmethod
    def load_yaml_document(yaml_str_document):
        """ This method loads a YMAL document from a string.
        
        Parameters
        ----------
        str_yaml : str
            String containing a YAML document
            
        Returns
        -------
        dict
            YAML structure in dictionnaries
            
        Raises
        ------
        Exception 
            If the YAML is not well formed
        """
        
        try:
            # Load the YMAL directives into python dictionnaries
            yaml_document = yaml.safe_load(yaml_str_document)
        except Exception:
            traceback.print_exc()
            raise Exception("Error loading YAML document: \n{}".format(yaml_str_document))

        return yaml_document
        
    @staticmethod
    def create_set_of_word(str_words, separator = " ", lower = True):
        """Create a set of words from a string of words.
        
        A set will remove duplicate words
        
        Parameters
        ----------
        str_words : str
            A string of words
        separator : str
            A character that delimits word in a string (default is space " ")
        lower: bool
            If set to True the result will be transformed in lower case; If flase no action is taken
            
        Returns
        -------
        Set
            A set of word
        """
        
        word_lst = str_words.split(separator)
        if lower:
            word_lst = [word.lower() for word in word_lst]
             
        # Create the set of words    
        word_set = set(word_lst)
         
        return word_set
        
    @staticmethod
    def feature_get_attribute(feature, attribute_key, error_if_none=False):
        """Read an attribute from a FME feature.
        
        Parameters
        ----------
        feature : FME Feature object
            The FME feature used to read the attribute
        attribute_key : String
            Name of the attribute to read
        error_if_none : Bool
            True: Raise exception if the FME attribute is missing; 
            False: write emtpty string if attribute is missing
        
        Returns
        -------
        String
            Value of the attribute read
        """
        
        attribute_value = feature.getAttribute(attribute_key)
        if attribute_value is None:
            if error_if_none:
                raise Exception ("Error.  Attribute: {} is missing)".format(attribute_key))
            else:
                attribute_value = ""
            
        return attribute_value 

    @staticmethod
    def make_http_call(fme_self, feature, session, str_http, output_fme=True):
        """This method makes an http call and manage the request response.
        
        If the response from the http request is not 200 (OK); an entry is made in the logger
        and an FME feature is outputted with the status code and the description.
        
        Parameters
        ----------
        fme_self : FME session object
            FME session object the "self"
        feature : FME Feature object
            FME feature used to output a feature
        session : Session object
            Used to make the http call
        str_http : str
            Http string used for the http call
        output_fme : Bool
            True: output an FME feature; False: do not output an FME feature
        
        Returns
        -------
        Request object
            Result from the get request
        """
    
        #web_pdb.set_trace()
        try:
            fme_self.logger.logMessageString("HTTP call: {0}".format(str_http), 
                                         fmeobjects.FME_INFORM)
            response = session.get(str_http, verify=False, timeout=10,  allow_redirects=True)
            status_code = response.status_code
            description = requests.status_codes._codes[status_code][0]
            
            # Manage if an FME feature need to be outputted
            if status_code != HTTP_OK and output_fme:
                lst_key_val_att = [(STATUS_CODE, "Status code: {0}: {1}".format(status_code, description)),
                                   (STATUS_CODE_DESCRIPTION, description)]
                FME_utils.pyoutput_feature(fme_self, feature, lst_key_val_att, clone=True) 
        except KeyError as err:
        #except Exception as err:
            # Manage the case where an error occured during the reading of the CKAN server
            fme_self.logger.logMessageString("HTTP call error: {0}".format(err), 
                                         fmeobjects.FME_ERROR)
            lst_key_val_att = [(STATUS_CODE, "500"),
                               (STATUS_CODE_DESCRIPTION, requests.status_codes._codes[500][0])]
            FME_utils.pyoutput_feature(fme_self, feature, lst_key_val_att, clone=True)
            sys.exit(0)

        return response
            
    @staticmethod    
    def create_session():
        """This method creates an http session.
        
        Parameters
        ----------
        None
            
        Returns
        -------
        Session
            Session to be uses to make the http requests
        """
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1.0,
                        status_forcelist=[ 500, 502, 503, 504 ])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        return session
        
    @staticmethod
    def pyoutput_feature(fme_self, feature, lst_key_value_att, clone=False):
        """Set attributes to the FME feature and output he feature through the FME pyoutput
        
        Parameters
        ----------
        me_self : FME session object
            FME session object the "self"
        feature : FME Feature object
            FME feature used to output a feature
        lst_key_value_att : List of tuple
            Each tuple contains 2 values: first the name of the key; second the value of the attribute
        clone : Bool
            True: Clone the feature before output it; 
            False: do not clone feature before outputit.
        
        Returns
        -------
        None
        """
    
        if clone:
            feature_out = feature.clone()
        else:
            feature_out = feature
            
        for key_att, value_att in lst_key_value_att:
            feature_out.setAttribute(key_att, value_att)
            
        # Output FME feature
        fme_self.pyoutput(feature_out)      
        
        return
        
    @staticmethod
    def convert_unix_time(feature, in_att_name, out_att_name='itemModif', out_format='%Y-%m-%d %H:%M:%S'):
        """ This method unix time to a specified format.
        
        Parameters
        ----------
        feature : FME Feature object
            The FME feature used to read the attribute
        in_att_name : str
            The name of the FME attribute to convert.
        out_att_name : str
            The name of the FME attribute you want the conversion to be done.
        out_format : str
            String containing the wanted output format for the date.
            
        Returns
        -------
        str
            A string representing the time in the specified format.
            
        """
        #web_pdb.set_trace()
        
        #Managing empty attributes
        if not feature.getAttribute(in_att_name):
            pass
        
        else:
            #Get the attribute value
            att_value = feature.getAttribute(in_att_name)
            
            #Converting the attribute value to string
            att_value_str = str(att_value)
            
            #Converting the length adjusted attribute value to integer
            att_value_cut = int(att_value_str[0:10:1])


            feature.setAttribute(out_att_name, datetime.fromtimestamp(att_value_cut).strftime(out_format))
            
        return
        
    @staticmethod
    def test_attribute_value(feature, att_name, target_value, check_case):
        """Test if a feature has a specific atttribute and a specific attribute value.
        
        Parameters
        ----------
        feature : FMEFeature
            Feature object containing the attribute to test_attribute
        att_name : String
            Attribute name to test
        target_value : str
            Value to test
        check_case : Bool
            Flag for the string case. True: Check the string case; False: string 
            case is not important
            
        Returns
        -------
        Bool
            True: The attribute is present and the value is good; 
            False: The attribute is not there or the value is different
        """
        
        att_value = FME_utils.feature_get_attribute(feature, att_name, True)
        
        if check_case:
            # Nothing to do
            pass
        else:
            # Adjust the case
            target_value = target_value.lower()
            att_value = att_value.lower()
        
        if att_value == target_value:
            match = True
        else:
            match = False
            
        return match    

    @staticmethod
    def remove_mailto(feature, in_att_name, out_att_name="", remove_in_att=False, separator=":"):
        """Removes the first part of an attribute string where it is not part of the email address
        
        Parameters
        ----------
        feature : FMEFeature
            Feature object containing the attribute to transform
        in_att_name : str
            The name of the FME attribute containing the email Address
        out_att_name : str
            The name of the FME attribute you want the transformation to be saved to.
            if this parameter is nor specified the transformation will be applied the attribute source
        separator : str
            String for the separator
        remove_in_att : Boolean
            When True and out_att_name is specified the source attribute is removed from the feature
        
        Returns
        -------
        None
        """

        try:
            splitted_mail = feature.getAttribute(in_att_name).split(separator)[1]
        except:
            pass
        else:
            if out_att_name=="":
                feature.setAttribute(in_att_name,splitted_mail.strip())
            else:
                feature.setAttribute(out_att_name,splitted_mail.strip())
                if remove_in_att:
                    feature.removeAttribute(in_att_name)
        
    @staticmethod
    def go_url(url):
        """
        Verifies if the provided url is valid and responds to a request, whether it's a http or ftp url.
        
        Parameters
        ----------
        url: String
            The current url to check.
        
        Returns
        -------
        None
        """

        # Depending if checking a ftp or http url
        if url.lower().startswith("ftp"):
            result = FME_utils.ftp_check_url(url)

        else:
            result = FME_utils.http_check_url(url)

        # If found
        if result["found"]:
            # If redirects happened
            if "redirects" in result and len(result["redirects"]) > 0:
                print("Found! | " + result["url"] + " --> " + ' --> '.join(result["redirects"]))

            else:
                print("Found! | " + result["url"])

        else:
            print("Not found | " + result["url"])

    @staticmethod
    def http_check_url(url):
        """
        Checks if the http url responds to a request.
        
        Parameters
        ----------
        url : String
            The current url to check
        
        Returns
        -------
        Dictionary
            A dictionary with "found", "url" and "redirects" properties.
        """

        redirects = []
        url_redir = None
        found_flag = FME_utils._http_check_url_rec(url, redirects)

        # Return information
        return {
            "found": found_flag,
            "url": url,
            "redirects": redirects
        }

    @staticmethod
    def _http_check_url_rec(url, redirects):
        """
        Checks if the url responds to a request and recursively follows redirections when any. The redirects used are added to the redirects parameter to be provided back to the caller.
        
        Parameters
        ----------
        url : String
            The current url to check
        redirects : List
            The total redirect urls processed
            
        Returns
        -------
        Boolean
            True if the url responded successfully (200 response); False otherwise
        """

        # Do the request using HEAD method
        r = FME_utils.http_check_url_request_head(url)

        # If a 200
        if r is not None and r.status_code == 200:
            return True

        elif r is not None and (r.status_code == 301 or r.status_code == 302 or r.status_code == 303 or r.status_code == 307 or r.status_code == 308):
            # Handle the redirects
            return FME_utils._http_check_url_rec_handle_redir(r, redirects)

        elif r is not None and (r.status_code == 400 or r.status_code == 405):
            # Do the request using OPTIONS method
            r = FME_utils.http_check_url_request_options(url)

            if r is not None and r.status_code == 200:
                return True

            elif r is not None and (r.status_code == 301 or r.status_code == 302 or r.status_code == 303 or r.status_code == 307 or r.status_code == 308):
                # Handle the redirects
                return FME_utils._http_check_url_rec_handle_redir(r, redirects)

        # Couldn't
        return False

    @staticmethod
    def http_check_url_request_head(url):
        """
        Makes a call on the provided url using the HEAD method.
        
        Parameters
        ----------
        url : String
            The current url to check
        
        Returns
        -------
        Request object
            The request object when successfully got a response of any kind or None when the request failed.
        """

        try:
            # Requests the head of the url
            r = requests.head(url, timeout=TIMEOUT)
            r.close()
            return r

        except Exception as err:
            return None

    @staticmethod
    def http_get_url_mime_type(url):
        """
        Makes a requests on the header of the url address to extract the MIME-type.
        
        If the MIME-type is absent and the status code of the URL reuest is valid, a get request is done 
        on the URL address and it validates if the URL content starts with '<!DOCTYPE html>' the MIME-type
        is set to 'text/html'.
        
        The method will set the MIME-type to None if it cannot determine the MIME-type of the URL.
        
        Parameters
        ----------
        url : String
            The current url to check
        
        Returns
        -------
        mime_type String
            The MIME-type of the URL address or None if the MIME-type cannot be determined
        """
        
        content_type = None  # Set default value
        logger = fmeobjects.FMELogFile()  # Create a logger
        
        try:
            # Suppress warning
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            
            # Make a head request to get only the header (not the content)
            response = requests.head(url, timeout=TIMEOUT, verify=False)
            status_code = response.status_code
            text = "HTTP call -- Status code: {0}; URL {1}".format(status_code, url)
            logger.logMessageString(text, fmeobjects.FME_INFORM)
            
            headers = response.headers
            content_type = headers.get("content-type")                
            if content_type is None:
                # If content-type is empty try to read the data and check if it's an HTML document
                headers = {"Range": "bytes=0-25"}  # Request a range if server can handle it (faster)
                request = requests.get(url,headers=headers, timeout=TIMEOUT, verify=False)
                text = request.text
                if '<!DOCTYPE html' in text[0:20]:
                    content_type = "text/html"
                else:
                    # Not an HTML document.
                    pass

        except:
            # An error has occured nothing to do 
            pass
            
        return content_type
        
    
    @staticmethod
    def http_check_url_request_options(url):
        """
        Makes a call on the provided url using the OPTIONS method.
        
        Parameters
        ----------
        url : String
            The current url to check
            
        Returns
        -------
        Request object or None
            The request object when successfully got a response of any kind or None when the request failed.
        """
        #web_pdb.set_trace()
        try:
            # Requests the head of the url
            r = requests.options(url, timeout=TIMEOUT, verify=False, allow_redirects=True)
            r.close()
            return r

        except Exception as err:
            return None

    @staticmethod
    def _http_check_url_rec_handle_redir(r, redirects):
        """
        Handles the request being redirected in order to loop back in the recursion with the redirected url.
        
        Parameters
        ----------
        r : String
            The current request that got a redirected status.
        redirects : List
            The total redirect urls processed.
            
        Returns
        -------
        Boolean
            True if the url responded successfully (200 response); False otherwise.
        """

        # If Location is in the headers
        if "Location" in r.headers:
            url_redir = r.headers["Location"]
            redirects.append(url_redir)

            # Loop back in the recursion
            return FME_utils._http_check_url_rec(url_redir, redirects)

        return False

    @staticmethod
    def ftp_check_url(url):
        """
        Parses the given url to retrieve the base directory and the directory/file to check for existence.\\
        A connection using TLS is tried first and if it fails a connection without TLS is attempted.
        Prints Found or Not Found with the tested url.
        
        Parameters
        ----------
        url : String
            The current url to check.
        
        Returns
        -------
        Dicstionary
            A dictionary with "found", "url" properties.
        """

        # Parse the url to get the base path and ignoring the extremities "/"
        o = urlparse(url)
        directories = o.path.strip('/').split('/')
        base_path = "/".join(directories[:-1])
        dir_file_name = directories[-1:][0]

        # Decode back to regular text (as urlparse also encodes the path)
        base_path = unquote(base_path)
        dir_file_name = unquote(dir_file_name)

        found_flag = False
        try:
            # Try with TLS
            with FTP_TLS(o.netloc) as ftp:
                found_flag = FME_utils.ftp_check_file_dir_exists(ftp, base_path, dir_file_name)

        except Exception as e:
            #print("FTP connection with TLS failed, trying without TLS")
            try:
                # Try without TLS
                with FTP(o.netloc) as ftp:
                    found_flag = FME_utils.ftp_check_file_dir_exists(ftp, base_path, dir_file_name)

            except Exception as e:
                print("Failed", e)

        # If found a file
        return {
            "found": found_flag,
            "url": url
        }

    @staticmethod
    def ftp_check_file_dir_exists(ftp, base_path, dir_file_name):
        """
        Uses the given ftp instance connection to browse to the base_path and check the existance of either a directory or a file name.
        
        Parameters
        ----------
        ftp : String
            The current ftp (ftplib) instance.
        base_path : String
            The base path to browse into.
        dir_file_name : String
            The name of the directory or the file to search for.
        
        Returns
        -------
        Boolean 
           True when found; False otherwise
        """

        ftp.encoding = "utf-8" # To support accented characters
        ftp.login()
        ftp.cwd(base_path)
        
        # List the files/directories
        filelist = ftp.nlst()

        # Return True if item is in the list
        return dir_file_name in filelist


def main():
    """
    Main function used when called without any parameters to run a couple test cases.
    """

    # Good tough examples:
    # - (with spaces and accents in url): "ftp://transfert.mern.gouv.qc.ca/public/diffusion/RGQ/Documentation/BDAT(FTP)/Index_Nord du 53e parallèle.pdf"
    # - (with redirection(s)): "http://rds.ca" (2 sequentional redirects!) or "https://www.donneesquebec.ca/recherche/fr/dataset/6d080ad9-3823-4bfd-8c61-32594f11bc83" (real case)
    # - (HEAD not working (error 400, use OPTIONS) "https://data.princeedwardisland.ca/api/views/4bk3-u3rm/rows.rdf?accessType=DOWNLOAD"
    # - (HEAD not working (error 405, use OPTIONS) "https://data.princeedwardisland.ca/api/geospatial/u8pp-dvp4?method=export&format=GeoJSON"
    # - (invalid SSL certificate): "https://jaymze.org/proglang/windows/unofficial_Guide_URL_File_Format_.pdf"

    url = ["ftp://transfert.mern.gouv.qc.ca/public/diffusion/RGQ/Documentation/BDAT(FTP)/Index_Nord du 53e parallèle.pdf",
           "https://jaymze.org/proglang/windows/unofficial_Guide_URL_File_Format_.pdf",
           "http://rds.ca",
           "https://www.donneesquebec.ca/recherche/fr/dataset/6d080ad9-3823-4bfd-8c61-32594f11bc83",
           "https://gnb.socrata.com/datasets/rzzg-85tb",
           "http://www.gov.pe.ca/photos/original/1900_forest.MIF.zip",
           "https://www.gov.pe.ca/photos/original/Wetlands09.DXF.zip",
           "https://www.gov.pe.ca/photos/original/wildlife2011.SHP.zip",
           "https://data.princeedwardisland.ca/api/geospatial/4zg3-he2k?method=export&format=GeoJSON",
           "https://data.princeedwardisland.ca/api/geospatial/4zg3-he2k?method=export&format=KML",
           "https://data.princeedwardisland.ca/api/geospatial/4zg3-he2k?method=export&format=KMZ",
           "https://data.princeedwardisland.ca/api/geospatial/4zg3-he2k?method=export&format=Shapefile",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.csv?accessType=DOWNLOAD",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.csv?accessType=DOWNLOAD&bom=true&format=true",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.rdf?accessType=DOWNLOAD",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.rss?accessType=DOWNLOAD",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.tsv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B",
           "https://data.princeedwardisland.ca/api/views/2ig2-djcy/rows.xml?accessType=DOWNLOAD",
           "https://data.princeedwardisland.ca/api/views/cgzy-bim6/files/689546cd-afbe-45f4-ae04-cb41a5c82c6a?download=true&filename=PEI%20Groundwater%20Well%20Information%20Mar2021.xlsx",
           "https://data.princeedwardisland.ca/datasets/2arv-as4n",
           "https://data.princeedwardisland.ca/datasets/y58z-nyfh",
           "https://data.princeedwardisland.ca/datasets/yhvv-wi8v"]

    # If url is a list of urls
    if isinstance(url, list):
        for u in url:
            FME_utils.go_url(u)

    else:
        FME_utils.go_url(url)

# Start the url check
#main()
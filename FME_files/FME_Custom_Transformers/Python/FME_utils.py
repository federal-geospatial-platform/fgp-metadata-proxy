import re
import fmeobjects
import yaml
import traceback
from typing import NamedTuple
import requests
import sys
import urllib3
import urllib.parse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime
import fme


try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass


# FME attribute name
STATUS_CODE = "_status_code"
STATUS_CODE_DESCRIPTION = "_status_code_description"

# Define HTTP OK return code
HTTP_OK = 200

class CsvKeyValuePair(NamedTuple):
    """Class containing one row from a CSV defining a key-Value pair.
    
    Attributes:
    
    key: str
        Key name of a Key-Value pair
    value: str
        Value name of a Key-Value pair
    """
    
    key: str
    value: str
    
    
class CsvMetaDataFormatMapper(NamedTuple):
    """Class containing one row from the CSV used by METADATA_VALUE_MAPPER_NG.
    
    Attributes:
    
    original_value: str
        Original value that can be found in the metadata record
    real_value: str
        Name that replace the original value
    resource_type_en: str
        Name of the English resource
    resource_type_fr: str
        Name of the French resource
        
    """
    original_value: str
    real_value: str 
    resource_type_en: str 
    resource_type_fr: str

class CsvMetaDataValueMapper(NamedTuple):
    """Class containing one row from the CSV used by METADATA_VALUE_MAPPER_NG.
    
    Attributes:
    
    original_value: str
        Original value that can be found in the metadata record
    value_english: str
        English value that replace the original value
    value_french: str
        French value that replace the original value
    code_valueL str
        Code value for this value
    """
    
    original_value: str
    value_english: str
    value_french: str
    code_value: str
    
  
class CsvGeoSpatialValidation(NamedTuple):
    """Class containing one row from the CSV GeoSpatialValidation.
    
    Attributes:
    
    fgp_publish: str
        Flag (oui/non) indicating if this format is published in the FGP
    format: str
        Name of the format
    spatial_type: str
        Spatial type code
    """
    
    fgp_publish: str
    format: str
    spatial_type: str

class FME_utils:
    
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
        feature: FME Feature
            FME feature to process
        att_name: str
            The name of the attribute to extract
        
        Returns
        -------
        list
            A list of FME attribute.  
        """

#        web_pdb.set_trace()
        atts = []
        feature_atts = feature.getAllAttributeNames()  # Extract all attribute names
        logger = fmeobjects.FMELogFile()
        regex_list = "\{\d+\}"
        regex_index = "\d+"

        if att_name.find("{}") != -1:
            # The attribute to search is a list
            att_name = "^" + att_name + "$"  # Regular expression exact match
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
        feature: FME Feature
            FME feature to process
        list_name: str
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
        str_yaml: str
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
        str_words: str
            A string of words
        separator: str
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
        feature FME Feature object
            The FME feature used to read the attribute
        attribute_key String
            Name of the attribute to read
        error_if_none Bool
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
        fme_self: FME session object
            FME session object the "self"
        feature: FME Feature object
            FME feature used to output a feature
        session: Session object
            Used to make the http call
        str_http: str
            Http string used for the http call
        output_fme: Bool
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
        me_self: FME session object
            FME session object the "self"
        feature FME Feature object
            FME feature used to output a feature
        lst_key_value_att List of tuples
            Each tuple contains 2 values: first the name of the key; second the value of the attribute
        clone Bool
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
        feature FME Feature object
            The FME feature used to read the attribute
        
        in_att_name: str
            The name of the FME attribute to convert.
            
        out_att_name: str
            The name of the FME attribute you want the conversion to be done.
        
        out_format: str
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
        feature FMEFeature
            Feature object containing the attribute to test_attribute
        att_name String
            Attribute name to test
        target_value
            Value to test
        check_case Bool
            Flag for the string case. True: Check the string case; False: string 
            case is not important
            
        Returns
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
        feature FMEFeature
            Feature object containing the attribute to transform

        in_att_name str
            The name of the FME attribute containing the email Address

        out_att_name: str
            The name of the FME attribute you want the transformation to be saved to.
            if this parameter is nor specified the transformation will be applied the attribute source
        
        separator str
            String for the separator

        remove_in_att
            When True and out_att_name is specified the source attribute is removed from the feature

        action:
            Replaces the attribute for the second part of itself after the separator
        """

        if not feature.getAttribute(in_att_name):
            pass
        else:
            splitted_mail = feature.getAttribute(in_att_name).split(separator)
            if out_att_name=="":
                feature.setAttribute(in_att_name,splitted_mail[1])
            else:
                feature.setAttribute(out_att_name,splitted_mail[1])
                if remove_in_att:
                    feature.removeAttribute(in_att_name)
        

#
# Ce fichier contient le code python appelé le Custom Transformer
# GEO_NON_GEO_SELECTOR

import fme
import fmeobjects
from Python.FME_utils import FME_utils
from Python.FME_utils import CsvGeoSpatialValidation
from typing import NamedTuple

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass
    
# FME Attribute names
ORDER = "_order"
YAML_STR = "_yaml_str"

RESOURCE_FORMAT = "resources{}.format"

# Name of the attribute containing the publish parameter
KEYWORD_SEARCH = "_keyword_search"
LIST_SEARCH_ATTRIBUTE = "_list_search_attribute"

# CSV column name
FORMAT = "format"
FGP_PUBLISH = "fgp_publish"
SPATIAL_TYPE = 'spatial_type'

# YAML directives
SEARCH_TYPE = "search_type"
NOT_FOUND = "not_found"
DOMAIN = "domain"

# YAML keyword
CONTAINS = "contains"
EQUALS = "equals"
IF_NULL_OVERWRITE = "if_null_overwrite"
LOOKUP_TABLE_FORMAT = "lookup_table_format"
LOG = "log"
NO_LOG = "no_log"
NO_OVERWRITE = "no_overwrite"
OVERWRITE = "overwrite"

# Geo none geo FME attributes
GEO_NONE_GEO_STATUS = "_geo_none_geo_status"
GEO = "geo"
NONE_GEO = "none_geo"
FORMAT_UNKNOWN = "format_unknown"
LOG_ERROR = "log_error"
NOT_FOUND_ERR_MSG = "_not_found_err_msg"
FORMAT = "format"

def copy_attributes_in_resources(feature):
    """Copy the attributes notes, titles and id in the attribute resources list.
    
    Parameters
    ----------
    feature: FMEObject
       The FME feature to processs
       
    Returns
    -------
    None
    """
    
    # Extract the original attribute
#        web_pdb.set_trace()
    id = FME_utils.feature_get_attribute(feature, "id", False)
    notes = FME_utils.feature_get_attribute(feature, "notes", False)
    title = FME_utils.feature_get_attribute(feature, "title", False)
    
    # extract the number of resources
    max_index_resources = FME_utils.max_index_attribute_list(feature, "resources{}")
    
    # For each resources add the attribute
    for i in range(max_index_resources+1):
        feature.setAttribute("resources{%d}.orig_id"%i, id)
        feature.setAttribute("resources{%d}.notes"%i, notes)
        feature.setAttribute("resources{%d}.title"%i, title)
        
    return 

def lower_resources_format(feature):
    """This method puts in lower case the content of the attribute resources{}.format
    
    Parameters
    ----------
    feature FMEObject
        the FME feature to process
        
    Returns
    -------
    None
    
    """
    
    # Loop over each attribute
    for dummy, att_name in FME_utils.extract_attribute_list(feature, "resources{}.format"):
        value = feature.getAttribute(att_name)
        value = value.lower()
        feature.setAttribute(att_name, value)
        
    return

class GeoNoneGeoSelector(object):
    def __init__(self):
        """Creates some instance variables before processing the FME features.
        
        Parameters
        ----------
        None
        
        Returns
        =======
        None
        """
    
        self.csv_features ={}
        
    def _load_csv_feature(self, feature):
        """ Load a feature from the CSV lookup table
        
        Parameters
        ----------
        feature: FME Feature object
            Feature containing the attributes to read
            
        Returns
        -------
        None
        """
        # Load the information from the CSV feature in a dictionary
#        web_pdb.set_trace()
        format = feature.getAttribute(FORMAT)
        fgp_publish = feature.getAttribute(FGP_PUBLISH)
        spatial_type = feature.getAttribute(SPATIAL_TYPE)
        csv_row = CsvGeoSpatialValidation(fgp_publish, format, spatial_type)
        self.csv_features[format] = csv_row  # Insert into the CSV dictionnary
        
        return
    
    def _validate_value_domain(self, value, domain):
        """Validates if a string value is contained in a list of strings.
        
        An exception is raised when the string is not contained in the list of strings
        
        Parameters
        ----------
        value: String
            The value to check
        domain: List of String
            List of string used to make the domain validation
            
        Returns
        -------
        None
        
        Exceptions
        ----------
        Exception Exception
            Raised when the value is not in the domain
        """
    
        if value in domain:
            # Structure valid
            pass
        else:
            raise Exception ("Structure of the YAML is invalid: {}".format(value))
            
        return
    
    
    def _load_yaml_document(self, feature):
        """Load the YAML document and validate the values of the document
        
        Parameters
        ----------
        Feature: FME feature object
            Feature containing in attribute the YAML document
            
        Returns
        -------
        None
        """
        
#        web_pdb.set_trace()
        yaml_str_document = feature.getAttribute(YAML_STR)  # extract YAML document in string
        self.yaml_document = FME_utils.load_yaml_document(yaml_str_document)
        
        # Validate the content of the YAML document
        for fme_att, value in self.yaml_document.items():
            # Validate YAML"domain" directive
            if DOMAIN in value and SPATIAL_TYPE in value and \
               NOT_FOUND in value and SEARCH_TYPE in value:
               
                domain = value[DOMAIN]        
                if domain == LOOKUP_TABLE_FORMAT or isinstance(domain, list):
                   # Structure valid
                   pass
                else:
                    raise Exception ("Structure of the YAML is invalid: {}".format(domain))
            
                # Validate SPATIAL_TYPE
                self._validate_value_domain(value[SPATIAL_TYPE], [OVERWRITE, IF_NULL_OVERWRITE, NO_OVERWRITE] )
                    
                # Validate NOT_FOUND
                self._validate_value_domain(value[NOT_FOUND], [LOG, NO_LOG] )
                    
                # Validate SEARCH_TYPE
                self._validate_value_domain(value[SEARCH_TYPE], [EQUALS, CONTAINS] )
                
                # Validate invalid cross directives: Domain list and OVERWRITE or IF_NULL_OVERWRITE
                if  isinstance(domain, list) and value[SPATIAL_TYPE] in [OVERWRITE, IF_NULL_OVERWRITE]:
                    #  Cannot overwrite the spatial type when the domain is a list 
                    raise Exception ("Invalid YAML. Spatial type OVERWRITE or IF_NULL_OVERWRITE invalid when the domain is a list")
                
                # Validate invalid cross directives: None FME list attribute and OVERWRITE or IF_NULL_OVERWRITE
                if "{}" not in fme_att:
                    if value[SPATIAL_TYPE] in [OVERWRITE, IF_NULL_OVERWRITE]:
                        # Cannot set SPATIAL_TYPE for none list attribute
                        raise Exception ("Invalid YAML. Spatial type OVERWRITE or IF_NULL_OVERWRITE invalid when the attribute is not a list")                                                  
            else:
                # Error Unknown directives           
                raise Exception ("Structure of the YAML is invalid: unknown directive {}".format(value))

        return
        
    def _create_domain(self, directives):
        """Extract the domain of possible values to test
        
        The method returns a set to enable intersection operation
        
        Parameters
        ----------
        directives: Dictionary
            Contain the YMAL directives 
            
        Returns
        -------
        Set
            Values of the DOMAIN directives in the YAML
        """
        
        # Extract the domain values to check
        domain = directives[DOMAIN]
        if domain == LOOKUP_TABLE_FORMAT:
            # Extract the format values from the CSV and create a set
            domain_lst = [item.format for item in self.csv_features.values()]
        else:
            # Create a set from the list of domain values
            domain_lst = [item.lower() for item in domain]  # Lower case
            
        return domain_lst
    
    def _output_feature(self, feature, geo, not_found_err):
        """Add some attributes to the FME feature and output the FME feature.
        
        Parameters
        ----------
        feature: FME Feature object
            The FME feature to process
        geo: Bool
            True: The metadata is geosptial
            False: The metadata is not geospatial
        not_found_err: List of tuple
            The first element of the tuple contains the name of the atribute; the second element contains the value of the attribute
  
        """
    
        if geo:
            # Output geopspatial feature#
            feature.setAttribute(GEO_NONE_GEO_STATUS, GEO)
            self.pyoutput(feature)
                
        else:
            # Output none geospatial feature 
            feature.setAttribute(GEO_NONE_GEO_STATUS, NONE_GEO)
            self.pyoutput(feature)
                
        if len(not_found_err) != 0:
            # Clone feature and output to LOG_ERROR
            for att_name, att_value in not_found_err:
                cloned_feature = feature.clone()
                cloned_feature.setAttribute(GEO_NONE_GEO_STATUS, LOG_ERROR)
                not_found_err_msg = "Attribute name: {} value: {} has no match \n".format(att_name, att_value)
                cloned_feature.setAttribute(NOT_FOUND_ERR_MSG, not_found_err_msg)
                cloned_feature.setAttribute(FORMAT, att_value)
                self.pyoutput(cloned_feature)
    
    def _process_feature(self, feature):
        """Process each FME feature according to the directives in the YAML document.
        
        Parameters
        ----------
        feature: FME Feature object
            The FME feature to process
            
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        # Process each entry in the YAML
        geo = False
        not_found_err = []
        for fme_att, directives in self.yaml_document.items():
            # Extract the list of attributes to process
            attributes = FME_utils.extract_attribute_list(feature, fme_att)
            
            # Loop over each attribute to process it
            for index, att_name in attributes:
                found = False
                att_value = feature.getAttributeAsType(att_name, fmeobjects.FME_ATTR_STRING)
                att_value = att_value.lower()
               
                # Extract the value(s) to search. Create a set to enable set intersection
                if directives[SEARCH_TYPE] == EQUALS:
                    att_value_set = set([att_value])
                else:
                    # Extract the words from the attribute and create a set (words are separated by " ")
                    att_value_set = FME_utils.create_set_of_word(att_value, separator = " ", lower = True)
                   
                # Create the domain values to validate
                domain_lst = self._create_domain(directives)
                # Check if value exist in domain list
                domain_match = [domain for domain in domain_lst if domain in att_value]
                if len(domain_match) >= 1:
                    # Match found
                    found = True
                    value = domain_match[0]  # Extract the element from the intersection
                    if directives[DOMAIN] in [LOOKUP_TABLE_FORMAT]:
                        # Validate that fgp_publish == oui in the CSV file
                        csv_feature = self.csv_features[value]
                        if csv_feature.fgp_publish == 'oui':
                            # We have a geospatial feature
                            geo = geo or True
                    else:
                        geo = geo or True
                        
                # Manage SPATIAL_type directives when the FME attribute is found
                if found:                
                    if directives[SPATIAL_TYPE] == NO_OVERWRITE:
                        # Nothing to do...
                        pass
                    else:
                        # Set the value of the spatial type
                        parts = fme_att.split("{")
                        spatial_type_name = parts[0] + "{%i}.spatial_type"%index
                        spatial_type_value = feature.getAttribute(spatial_type_name)
                        
                        if directives[SPATIAL_TYPE] == OVERWRITE or \
                           (directives[SPATIAL_TYPE] == IF_NULL_OVERWRITE and spatial_type_value in [None,""]):
                            # Add the spatial type
                            feature.setAttribute(spatial_type_name, csv_feature.spatial_type)
                        
                # Manage the LOG directive when the FME attribute is not found
                if not found:
                    if directives[NOT_FOUND] == LOG:
                        # Add the item not found
                        not_found_err.append((att_name, att_value))
                
        self._output_feature(feature, geo, not_found_err)
        
        return

    def input(self,feature):
        """Process the incoming FME features.
        
        Parameters
        ----------
        feature FME Feature object
            The incoming FME feature to process
        
        Returns
        -------
        None
        """
            
        order = feature.getAttribute(ORDER)
        if order == 1:
            self._load_csv_feature(feature)
            
        elif order == 2:
            self._load_yaml_document(feature)
        
        elif order == 3:
            self._process_feature(feature)
        else:
             raise Exception ("ERROR Unknown value for _order: {}".format(order))

            # Process the feature
    
    def close(self):
        """No action needs to be done when all the FME features have been processed.
        """
        pass
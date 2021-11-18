import fme
import fmeobjects

from FME_utils import FME_utils
from FME_utils import CsvGeoSpatialValidation

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

class GeoNoneGeoSelector(object):
    """This class is used by the custom transfomer GEO_NON_GEO_SELECTOR in a PythonCaller in order 
    to sort the record between geospatial and none geospatial records. This class is reading 
    YAML files that contains the directives to sort the records
    """
    
    def __init__(self):
        """Constructor call before any FME features are passed
        """
    
        self.csv_features ={}
        self.logger = fmeobjects.FMELogFile()
        
    def _load_csv_feature(self, feature):
        """ Load the YAML directuves.
        """
        # Load the information from the CSV feature in a dictionary
#        web_pdb.set_trace()
        format = feature.getAttribute(FORMAT)
        fgp_publish = feature.getAttribute(FGP_PUBLISH)
        spatial_type = feature.getAttribute(SPATIAL_TYPE)
        csv_row = CsvGeoSpatialValidation(fgp_publish, format, spatial_type)
        self.csv_features[format] = csv_row  # Insert into the CSV dictionnary
    
    def _validate_value_domain(self, value, domain):
        """Check if a value is in a list and raise an error if not
        """
    
        if value in domain:
            # Structure valid
            pass
        else:
            raise Exception ("Structure of the YAML is invalid: {}".format(value))
    
    
    def _load_yaml_document(self, feature):
        """Load the YAML document
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
        
        """
        
        # Extract the domain values to check
        domain = directives[DOMAIN]
        if domain == LOOKUP_TABLE_FORMAT:
            # Extract the format values from the CSV and create a set
            domain_lst = [item.format for item in self.csv_features.values()]
            domain_set = set(domain_lst)
        else:
            # Create a set from the list of domain values
            domain_lst = [item.lower() for item in domain]  # Lower case
            domain_set = set(domain_lst)
            
        return domain_set
    
    def _output_feature(self, feature, geo, not_found_err):
        """Output the feature to FME.
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
        """Process each FME feature
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
                att_value = feature.getAttribute(att_name)
                att_value = att_value.lower()
               
                # Extract the value(s) to search. Create a set to enable set intersection
                if directives[SEARCH_TYPE] == EQUALS:
                    att_value_set = set([att_value])
                else:
                    # Extract the words from the attribute and create a set (words are separated by " ")
                    att_value_set = FME_utils.create_set_of_word(att_value, separator = " ", lower = True)
                   
                # Create the domain values to validate
                domain_set = self._create_domain(directives)
                domain_intersection = att_value_set.intersection(domain_set)  # Set intersection
                if len(domain_intersection) == 1:
                    # Match found
                    found = True
                    value = list(domain_intersection)[0]  # Extract the element from the intersection
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
                            self.logger.logMessageString("Added attribute: {} Value: ".format(spatial_type_name, 
                                                          csv_feature.spatial_type), fmeobjects.FME_INFORM)
                        
                # Manage the LOG directive when the FME attribute is not found
                if not found:
                    if directives[NOT_FOUND] == LOG:
                        # Add the item not found
                        not_found_err.append((att_name, att_value))
                
        self._output_feature(feature, geo, not_found_err)
        
        return

    def input(self,feature):
        """Input of all FME features.
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
        """Method call when all the festures are passed
        """
        
        pass
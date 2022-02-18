#
# Ce fichier contient le ccode python appelé le Custom Transformer
# METADATA_FORMAT_MAPPER_NG

import fme
import fmeobjects
from Python.FME_utils import CsvMetaDataFormatMapper
from Python.FME_utils import FME_utils

# Constants

# FME attribute name
##CODE_VALUE = "code_value"
ORDER = "_order"
ORIGINAL_VALUE = "original_value"
REAL_VALUE = "real_value"
REAL_VALUE_ENGLISH = "resource_type_en"
REAL_VALUE_FRENCH = "resource_type_fr"
RESOURCE_TYPE_EN = "resource_type_en"
RESOURCE_TYPE_FR = "resource_type_fr"

# FME published parameter as attributes
ERROR_NOT_MAPPED = "error_not_mapped"
REAL_VALUE_REFRESH = "real_value_refresh"
RES_TYPE_EN_REFRESH = "res_type_en_refresh"
RES_TYPE_FR_REFRESH = "res_type_fr_refresh"

# FME attribute value
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
       
        self.csv_features = {}  # Create dictionary to load the CSV features
        self.meta_features = []  # Create list to load the metadata features

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
            original_value = (feature.getAttribute(ORIGINAL_VALUE)).lower()
            real_value = feature.getAttribute(REAL_VALUE)
            resource_type_en = feature.getAttribute(RESOURCE_TYPE_EN)
            resource_type_fr = feature.getAttribute(RESOURCE_TYPE_FR)
            csv_row = CsvMetaDataFormatMapper(original_value, real_value, resource_type_en, 
                                              resource_type_fr)
            self.csv_features[original_value] = csv_row  # Insert into the CSV dictionnary        
        else:
            # Load the metadata features
            self.meta_features.append(feature)
                    
    def close(self):
        """Map the requested attribute.
        
        The following tasks are performed:
        
         - Extract boolean information on how to map values;
         - Extract the value of the attribute or attribute list to map
         - Map the values according to which value to map (Feanch value, 
           English value, code value)
         - Append the error to the mapping_errors{}.error attribute list
         - Output the FME feature
           
        """         
        
#        web_pdb.set_trace()
        # Process all the features
        for feature in self.meta_features:
            self.mapping_errors = []  # Reset the list that contains the errors
            # Extract attribute value to process
            att_2_map=feature.getAttribute('att_2_map')
            
            # Extract the status of the published parameters (passed through attributes)
            bool_real_value_refresh = FME_utils.test_attribute_value(feature, REAL_VALUE_REFRESH, YES, False)
            bool_res_type_en_refresh = FME_utils.test_attribute_value(feature, RES_TYPE_EN_REFRESH, YES, False)
            bool_res_type_fr_refresh = FME_utils.test_attribute_value(feature, RES_TYPE_FR_REFRESH, YES, False)
            bool_error_not_mapped = FME_utils.test_attribute_value(feature, ERROR_NOT_MAPPED, YES, False)
         
            # Extract the attributes name to process.  Can be a list or a single attribute
            index_attributes = FME_utils.extract_attribute_list(feature, att_2_map)
        
            if index_attributes:
                # Loop over the attributes
                for index, att_name in index_attributes:
                    # Extract the attribute to process
                    att_value = FME_utils.feature_get_attribute(feature, att_name, False)
                    att_value = att_value.lower().rstrip(" ").lstrip(" ")
                    
                    # Extract the row from CSV dictionary
                    try:
                        csv_row = self.csv_features[att_value]
                        # Map the value according to the requirements
                        if bool_real_value_refresh:
                            feature.setAttribute(att_name, csv_row.real_value)
                        if bool_res_type_en_refresh:
                            feature.setAttribute(att_name+'_resourceType_en', csv_row.resource_type_en)
                        if bool_res_type_fr_refresh:
                            feature.setAttribute(att_name+'_resourceType_fr', csv_row.resource_type_fr)
                    except KeyError:
                        # Value not found in the dictionary. Add the error in the list
                        str_error = ("Unable to map value: {0} for attribute: {1}.".format(att_value,att_name))
                        self.mapping_errors.append(str_error)
            else:
                # The requested attribute is not found
                str_error = ('The requested attribute to map (ATT_TO_MAP): {} is not present on the FME feature.'.format(att_2_map))
                self.mapping_errors.append(str_error)
                    
            # Append the errors in the FME error attribute
            if bool_error_not_mapped:
                # Mapping errors are registered in FME attribute
                if self.mapping_errors:
                    # Extract the number of existing error
                    err_count = FME_utils.max_index_attribute_list(feature, "mapping_errors{}.error")
                    err_count += 1
                    for i, mapping_error in enumerate(self.mapping_errors):
                        # Append the error to the existing list of error
                        feature.setAttribute("mapping_errors{%d}.error"%(i+err_count), mapping_error)
                else:
                    # Mapping error list empty ===> Nothing to do
                    pass
            else:
                # Mapping error are not registered in FME attribute
                pass
                    
            # Output the feature to FME after processing all the attributes
            self.pyoutput(feature)
                
        return
                
def reset_format_no_value(feature):
    """Reset the resources{}.format list.

    If the the resources{}.format is equal to "no_data" set the value to ""
    
    Parameters
    ----------
    feature: FMEObject
        Feature object to process
        
    Returns
    -------
    None
    """
    
    # Extract all the resources{}.format
    ind_resources_formats = FME_utils.extract_attribute_list(feature, 'resources{}.format')
    
    # Loop over all the resources{}.format
    for ind, resources_format in ind_resources_formats:
        value = feature.getAttribute(resources_format)
        if value == "no_value":
            # Reset the format value
            feature.setAttribute(resources_format,"")
            
    return

#
# Ce fichier contient le ccode python appelé le Custom Transformer
# GEOSPATIAL_DATA_VALIDATOR_NG

import fme
import fmeobjects
from Python.FME_utils import CsvMetaDataValueMapper
from Python.FME_utils import FME_utils

# Constants

# FME attribute name
CODE_VALUE = "code_value"
ORDER = "_order"
ORIGINAL_VALUE = "original_value"
REAL_VALUE_ENGLISH = "real_value_english"
REAL_VALUE_FRENCH = "real_value_french"

# FME published parameter as attributes
CODE_REFRESH = "code_refresh"
ENGLISH_REFRESH = "english_refresh"
ERROR_NOT_MAPPED = "error_not_mapped"
FRENCH_REFRESH = "french_refresh"

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
            value_english=feature.getAttribute(REAL_VALUE_ENGLISH)
            value_french=feature.getAttribute(REAL_VALUE_FRENCH)
            code_value=feature.getAttribute(CODE_VALUE)
            csv_row = CsvMetaDataValueMapper(original_value, value_english, value_french, code_value)
            self.csv_features[original_value] = csv_row  # Insert into the CSV dictionnary        
        else:
            # Load the metadata features
            self.meta_features.append(feature)
                    
    def close(self):
        """Map the requested attribute.
        
        The following tasks are performed:
        
         - ...
           
        """         
        
#        web_pdb.set_trace()
        # Process all the features
        for feature in self.meta_features:
            self.mapping_errors = []  # Reset the list that contains the errors
            # Extract attribute value to process
            att_2_map=feature.getAttribute('att_2_map')
            
            # Extract the status of the value mapping published parameters (through attributes)
            bool_english_refresh = FME_utils.test_attribute_value(feature, ENGLISH_REFRESH, YES, False)
            bool_french_refresh = FME_utils.test_attribute_value(feature, FRENCH_REFRESH, YES, False)
            bool_code_refresh = FME_utils.test_attribute_value(feature, CODE_REFRESH, YES, False)
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
                        if bool_english_refresh:
                            feature.setAttribute(att_name, csv_row.value_english)
                        if bool_french_refresh:
                            feature.setAttribute(att_name+"_fr", csv_row.value_french)
                        if bool_code_refresh:
                            feature.setAttribute(att_name+"_code", csv_row.code_value)
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
                    index_mapping_error = FME_utils.extract_attribute_list(feature, "mapping_errors{}.error")
                    if len(index_mapping_error) >= 1:
                        # Extract the value of the last index which can be different from the lenght of the list index_att_error
                        err_count = index_mapping_error[-1][0] + 1
                    else:
                        err_count = 0
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
                
            
            
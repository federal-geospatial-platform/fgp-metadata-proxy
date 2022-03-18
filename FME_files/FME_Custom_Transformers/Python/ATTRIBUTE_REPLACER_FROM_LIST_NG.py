#
# Ce fichier contient le ccode python appelé le Custom Transformer
# ATTRIBUTE_REPLACER_FROM_LIST_NG

import fme
import fmeobjects

# Constants
ORDER = "_order"
ORIGINAL_VALUE = "original_value"

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
                
            
class FeatureProcessor(object):
    """This class implement the design pattern: *Processing Composite Data*"""
    
    def __init__(self):
        """This constructor method created two lists to store the key values and the features."""
       
        self.csv_items = []  # Create list to load the CSV features
        self.features = []  # Create list to load the metadata features

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
            self.csv_items.append(feature.getAttribute(ORIGINAL_VALUE))
        else:
            self.features.append(feature)

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
        
        # Process all the features
        for feature in self.features:

            # Extract attribute values to compare for each feature 
            # _list2search=feature.getAttribute(FME_MacroValues['SEARCH_LIST'])
            list_name = feature.getAttribute('_SEARCH_LIST')
            _list2search = feature.getAttribute(list_name)
            # _list2search=feature.getAttribute('tags{}')
            
            found=False
            # for each element from the csv file 
            for keyword in self.csv_items:
                # Look for the first match in the list
                for item in _list2search:
                    if item == keyword:
                        found=True
                        break
                if found:
                  feature.setAttribute('$(ATT_TO_REPLACE)', keyword)
                  break
            self.pyoutput(feature)
            

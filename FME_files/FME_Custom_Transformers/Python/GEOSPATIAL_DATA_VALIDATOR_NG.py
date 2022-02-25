#
# Ce fichier contient le ccode python appelé le Custom Transformer
# GEOSPATIAL_DATA_VALIDATOR_NG

import fme
import fmeobjects
from Python.FME_utils import CsvGeoSpatialValidation
from Python.FME_utils import FME_utils

# Constants

# FME attribute name
FGP_PUBLISH = "fgp_publish"
FORMAT = "format"
KEYWORD_SEARCH = "keyword_search"
LIST_SEARCH_ATTRIBUTE = "list_search_attribute"
RECORD_TYPE = "_record_type"
SPATIAL_TYPE = "spatial_type"

# FME attribute value
OUI = "oui"

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
   
        order = feature.getAttribute('_order')
        if order == 1:
            # Read the attributes from the CSV features into a dictionary
            format = feature.getAttribute(FORMAT)
            fgp_publish = feature.getAttribute(FGP_PUBLISH)
            spatial_type = feature.getAttribute(SPATIAL_TYPE)
            csv_row = CsvGeoSpatialValidation(fgp_publish, format, spatial_type)
            self.csv_features[format] = csv_row  # Insert into the CSV dictionnary        
        elif order == 2:
            # Load the keyword search and search attribute list
            keyword_search = FME_utils.feature_get_attribute(feature, KEYWORD_SEARCH, True)
            self.keyword_search_lst = keyword_search.split("|")
            self.list_search_attribute = FME_utils.feature_get_attribute(feature, LIST_SEARCH_ATTRIBUTE, True)
        else:
            # Load the metadata features
            self.meta_features.append(feature)
        
    def _copy_attributes_in_resources(self, feature):
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
    
    def close(self):
        """Determine if the metadata feature is geospatial or non-geospatial.
        
        The following tasks are performed:
        
         - For each resources{}.format, it extracts from the csv file the 
           the format, the fgp_publish and the spatial_type.  The spatial_type
           is added as attribute to the feature
         - If the format cannot be match in the CSV; the ID and the format 
           are outputtted through the port UNKNOWN_FORMAT
         - To determine if a record is geospatial, the fgp_publish value 
           matching the format must be equal to "oui" or the metadata record
           must have an attribute fgp_publish with the value to "oui"; if 
           one of these conditions are not met the metadata record is consedered
           to be none geospatial
           
        """         
        
#        web_pdb.set_trace()
        for feature in self.meta_features:
            geo_record = False  # Flag reset
            err_format_features = []  # Reset error format list
            
            # Copy some attributes in the atrribute list resources
            self._copy_attributes_in_resources(feature)
            
            # Loop over each resources{}.format
            index_attributes = FME_utils.extract_attribute_list(feature, "resources{}.format")
            for ind, attribute in index_attributes:
                format = FME_utils.feature_get_attribute(feature, attribute, False)
                format = format.lower()
                feature.setAttribute(attribute, format)  # Rewrite the format attribute in lower case0
                try:
                    # Extract the format information
                    csv_row = self.csv_features[format]
                    # Assign the values from the CSV spatial_type to the feature
                    feature.setAttribute("resources{%d}.spatial_type"%ind, csv_row.spatial_type)                    
                    # Check if the format is published
                    if csv_row.fgp_publish == OUI:
                        geo_record = True
                    else:
                        # Check if the feature has a fgg_publish attribute set to OUI
                        if FME_utils.extract_attribute_list(feature, "resources{%d}.fgp_publish"%ind) == OUI:
                            # It is a geospatial record
                            geo_record = True
                          
                except KeyError:
                    # The format is unknown (not in the dictionary). Feature to be output in error format port
                    feature_clone = feature.clone()
                    feature_clone.setAttribute(FORMAT, format)
                    err_format_features.append(feature_clone)
                    
            if not geo_record:
                # Check if some keyword are present in the list search attribute; if so make it Geo Spatial
                index_attributes = FME_utils.extract_attribute_list(feature, self.list_search_attribute)
                for ind, attribute in index_attributes:
                    attribute_value = feature.getAttribute(attribute)  # Extract the attribute value             
                    if attribute_value in self.keyword_search_lst:  # Check if present in the list of key words
                        geo_record = True
                        break  # Do not need to process the others...
                        
            if not geo_record:
                # check if one attribute resources{}.fgp_publish == "oui"; if so make it a Geo Spatial
                index_attributes = FME_utils.extract_attribute_list(feature, "resources{}.fgp_publish")
                for ind, attribute in index_attributes:
                    attribute_value = feature.getAttribute(attribute)  # Extract the attribute value             
                    if attribute_value == OUI:  # Check if present in the list of key words
                        geo_record = True
                        break  # Do not need to process the others...
                        
            # Output the FME features with the good record type
            if len(err_format_features) >= 1:
                # Format Error.  Loop over each feature (one feature can have more than format error) 
                for err_format_feature in err_format_features:
                    err_format_feature.setAttribute(RECORD_TYPE, "ERROR_FORMAT")
                    self.pyoutput(err_format_feature)  # Ouput the feature
            else:
                if geo_record:
                    # Geo Spatial feature
                    feature.setAttribute(RECORD_TYPE, "GEO_SPATIAL")
                else:
                    # None Geo Spatial feature
                    feature.setAttribute(RECORD_TYPE, "NONE_GEO_SPATIAL")
                # Output the feature
                self.pyoutput(feature)  # Ouput the feature
#
# Ce fichier contient le ccode python appelé le Custom Transformer
# GEO_NON_GEO_SELECTOR

import fme
import fmeobjects
import FME_utils
from typing import NamedTuple

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass
    
ORDER = "_order"

RESOURCE_FORMAT = "resources{}.format"

# Name of the attribute containing the publish parameter
KEYWORD_SEARCH = "_keyword_search"
LIST_SEARCH_ATTRIBUTE = "_list_search_attribute"

# CSV column name
FORMAT = "format"
FGP_PUBLISH = "fgp_publish"
SPATIAL_TYPE = 'spatial_type'

FORMAT_UNKNOWN_VALUE = "_format_unknown_value"

# Geo none geo attributes
GEO_NONE_GEO_STATUS = "_geo_none_geo_status"
GEO = "geo"
NONE_GEO = "none_geo"
FORMAT_UNKNOWN = "format_unknown"

class CsvColumn(NamedTuple):
    """Class containing the features from the CSV
    """
    fgp_publish: str
    format: str
    spatial_type: str


class GeoNoneGeoSelector(object):
    def __init__(self):
    
        self.csv_features ={}
        self.geo = []
        self.none_geo = []
        self.format_unknown = []
        
    def input(self,feature):
            
        if feature.getAttribute(ORDER) == 1:
            # Load the information from the CSV feature in a dictionary
#            web_pdb.set_trace()
            format = feature.getAttribute(FORMAT)
            fgp_publish = feature.getAttribute(FGP_PUBLISH)
            spatial_type = feature.getAttribute(SPATIAL_TYPE)
            csv_row = CsvColumn(fgp_publish, format, spatial_type)
            self.csv_features[format] = csv_row  # Insert into the CSV dictionnary
            
        else:
            # Process the feature
        
            # Extract the KEYWORD_SEARCH and SEARCH_ATTRIBUTE (Published parameter)
            keyword_search =  feature.getAttribute(KEYWORD_SEARCH)
            search_atts =  feature.getAttribute(LIST_SEARCH_ATTRIBUTE)
            lst_search_atts = search_atts.split("|")
            
            # Check the ressources{}.format
#            web_pdb.set_trace()
            processed = False
            attributes = FME_utils.extract_attribute_list(feature, RESOURCE_FORMAT)  # Extract the attribute name
            for index, attribute in attributes:  # Loop over each attribute name
                format_value = feature.getAttribute(attribute)
                if format_value in self.csv_features:
                    # Known format; extract spatial type
                    csv_feature = self.csv_features[format_value]
                    att_spatial_type = attribute.replace(".format", ".spatial_type")
                    feature.setAttribute(att_spatial_type, csv_feature.spatial_type)
                    if csv_feature.fgp_publish == "oui":
                       processed = True
                else:
                    # Identify unknown format
                    cloned = feature.clone()
                    cloned.setAttribute(FORMAT_UNKNOWN_VALUE, format_value)
                    self.format_unknown.append(cloned)
                    
            if processed:
                self.geo.append(feature)
                                
            else:      
                web_pdb.set_trace()
                # Verify in the KEYWORD_SEARCH
                processed = False
                attributes = FME_utils.extract_attribute_list(feature, keyword_search)
                for index, attribute_name in attributes:
                    value = feature.getAttribute(attribute_name)
                    if value in lst_search_atts:
                        processed = True
                        break

                if processed:
                    self.geo.append(feature)  # It's a geo feature
                else:
                    self.none_geo.append(feature)  # It's not a geo feature
            
    def close(self):
        # Output the feature
        
        for feature in self.geo:
            feature.setAttribute(GEO_NONE_GEO_STATUS, GEO)
            self.pyoutput(feature)
            
        for feature in self.none_geo:
            feature.setAttribute(GEO_NONE_GEO_STATUS, NONE_GEO)
            self.pyoutput(feature)
            
        for feature in self.format_unknown:
            feature.setAttribute(GEO_NONE_GEO_STATUS, FORMAT_UNKNOWN)
            self.pyoutput(feature)
            
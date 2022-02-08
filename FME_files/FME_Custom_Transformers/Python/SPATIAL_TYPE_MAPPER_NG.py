#
# Ce fichier contient le ccode python appelé le Custom Transformer
# SPATIAL_TYPE_MAPPER_NG


import fme
import fmeobjects
from collections import Counter
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass


# FME attribute name
SPATIAL_REPRESENTAIOTN_TYPE = "spatial_representation_type"
RESOURCES_SPATIAL_TYPE = "resources{}.spatial_type"


def set_spatial_representation(feature):
    """This method sets the spatial representation based of the resources{}.spatial_type.
    
    The FME attribute resources{}.spatial_type can take one of the following values
    
     - <empty value>
     - a-grid
     - b-vector
     - c-textTable
     
     The method count the number of occurences of each value except the <empty-value> or "" 
     value. It will set the spatial representation to the value that has the most count. 
     In case of  equality the a-grid has priority over b-vector and the latter has 
     priority over c-textTable.  For the spatial representation we remove the "a-", 
     "b-" or "c-" and only keep "grid", "vector" or "textTable" that is set in the 
     FME attribute spatial_representation_type.
    
    Parameters
    ----------
    feature: FmeFeature object
        Feature object to process
        
    Returns
    -------
    None
    """
    
#    web_pdb.set_trace()
    spatial_types = []
    
    # Extract all the attribute spatial_type from the list 
    resources_spatial_types = FME_utils.extract_attribute_list(feature, RESOURCES_SPATIAL_TYPE)
    for dummy, att_spatial_type in resources_spatial_types:
        value_spatial_type = feature.getAttribute(att_spatial_type)
        if value_spatial_type is not None and value_spatial_type != "":
            value_spatial_type = feature.getAttribute(att_spatial_type)
            spatial_types.append(value_spatial_type)
            
    # Count the number of spatial for each distinct spatial type
    count_spatial_type = Counter(spatial_types)
    
    # Order the counted spatial type from the most to the least
    ordered_spatial_type = count_spatial_type.most_common()
    
    # Extract the count of the maximum spatial type
    max_count = ordered_spatial_type[0][1]
    
    # Extract all the spatial type that have the same max count
    similar_spatial_type = [spatial_type[0] for spatial_type in ordered_spatial_type 
                                                if spatial_type[1]==max_count]
    
    # Sort on the spatial_type alphabetically
    similar_spatial_type.sort()
    spatial_representation_type = similar_spatial_type[0]  # Extract the first element of the list
    spatial_representation_type = spatial_representation_type[2:]  # Extrat from the third charcater to the remaining of the string
    
    # Set the output attribute 
    feature.setAttribute(SPATIAL_REPRESENTAIOTN_TYPE, spatial_representation_type)
                
    return

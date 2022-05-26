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
ATT_DEFAULT_KEY = "default_key"
ATT_DEFAULT_VALUE = "default_value"

class DefaultAttributeMapper(object):
    def __init__(self):
        """Creates some instance variables before processing the FME features.
        
        Parameters
        ----------
        None
        
        Returns
        =======
        None
        """
    
        self.csv_features = []
        self.features = []

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
            self.csv_features.append(feature)
            
        elif order == 2:
            self.features.append(feature)
        
        else:
             raise Exception ("ERROR Unknown value for _order: {}".format(order))
    
    def close(self):
        """Add the default values to each features.
        """
        
        #web_pdb.set_trace()
        # Loop over each feature
        for feature in self.features:
        
            # Loop over each feature of the CSV
            for csv_feature in self.csv_features:
                default_key = FME_utils.feature_get_attribute(csv_feature, ATT_DEFAULT_KEY)
                default_value = FME_utils.feature_get_attribute(csv_feature, ATT_DEFAULT_VALUE)
                if "{}" in default_key:
                    pos = default_key.find("}")
                    sub_default_key = default_key[0:pos+1]
                    nbr_index = FME_utils.max_index_attribute_list(feature, sub_default_key)
                    for index in range(nbr_index+1):
                        default_key = default_key.replace("{}", "{%i}")
                        feature.setAttribute(default_key %index, default_value)
                else:
                    feature.setAttribute(default_key, default_value)
            
            self.pyoutput(feature)
            
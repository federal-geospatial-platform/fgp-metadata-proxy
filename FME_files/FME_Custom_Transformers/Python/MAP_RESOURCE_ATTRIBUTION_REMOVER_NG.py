#
# Ce fichier contient le ccode python appelé le Custom Transformer
# LOOKUP_TABLE_READER_NG


import fme
import fmeobjects
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

#
#
#-SetUrlResources-------------------------------------------------------------
#
# Constant for the YAML directives

# Constant

# FME Attribute
ORDER = "_order"
URL = "url"

class SetUrlResources(object):
    """Template Class Interface:
    When using this class, make sure its name is set as the value of the 'Class
    to Process Features' transformer parameter.
    
    This class will update the FME attribute resource{} list by adding 2 attributes
    if the resources{x}.url attribute is contained in the list of URL read from 
    the CSV file.    
    """

    def __init__(self):
        """Define the variables needed to load and store the incoming features.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        # Create instance attribute needed for the processing
        self.features = []  # List to accumulate the features
        self.csv_url = []  # List to accumulate the CSV records
        
        return
    
    def input(self, feature):
        """This method stores the incoming FME features.
        
        Parameters
        ----------
        feature: FmeFeature object
            Feature to process
        
        Returns
        -------
        None
        """
        
#        web_pdb.set_trace()
        order = FME_utils.feature_get_attribute(feature, ORDER, True)
        
        if order == 1:
            # Extract URL and load it
            url_value = FME_utils.feature_get_attribute(feature, URL, True)
            self.csv_url.append(url_value)
        else:
            # Load metadata records
            self.features.append(feature)
            
        return

    def close(self):
        """This method updates the FME attribute ressources{}.url list.
        
        The attribute will be updated if the url is present in the CSV URL file.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
#        web_pdb.set_trace()  # Breakpoint
        # Process all the stored featured
        
        for feature in self.features:
            # Process all the FME attribute resources{}.url
            for ind, fme_attribute in FME_utils.extract_attribute_list(feature, "resources{}.url"):
                value_url = FME_utils.feature_get_attribute(feature, fme_attribute, True)
                if value_url in self.csv_url:
                    feature.setAttribute("resources{%d}.xlink_role"%(ind),"")
                    feature.setAttribute("resources{%d}.protocol"%(ind),'HTTPS')
                    
            self.pyoutput(feature)

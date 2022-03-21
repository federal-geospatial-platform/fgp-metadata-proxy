#
# Ce fichier contient le ccode python appelé le Custom Transformer
# ATTRIBUTE_REPLACER_FROM_LIST_NG

import fme
import fmeobjects

# Constants
ORDER = "_order"
ORIGINAL_VALUE = "original_value"

class FeatureProcessor(object):

    def __init__(self):
        """This constructor method created two lists to store the key values and the features."""
       
        self.csv_items = []  # Create list to load the CSV features
        self.features = []  # Create list to load the metadata features

    def input(self,feature):
        """Load the incoming features.
        
        The keywords from the CSV (_order=1) are stored in a list 
        The features (_order=2) are stored in a list.
        
        Parameters
        ----------

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
        
         - Extract the list of values to search into;
         - Use the keywords list to search sequencially a match in the values list
         - When a match is found, it replaces the attribute specified
         - If there is not match, then Append the error to the mapping_errors{}.error attribute list
         - Output the FME feature
           
        """         
        
        # Process all the features
        for feature in self.features:

            # Extract attribute values to compare for each feature 
            # _list2search=feature.getAttribute(FME_MacroValues['SEARCH_LIST'])
            #list_name = feature.getAttribute('_SEARCH_LIST')
            #_list2search = feature.getAttribute(list_name)
            _list2search=feature.getAttribute('tags{}')
            
            found=False
            # for each element from the csv file 
            for keyword in self.csv_items:
                # Look for a match in the list
                for item in _list2search:
                    if item.lower() == keyword.lower():
                        found=True
                        break
                if found:
                  feature.setAttribute($(ATT_TO_REPLACE), keyword)
                  break
            self.pyoutput(feature)
            

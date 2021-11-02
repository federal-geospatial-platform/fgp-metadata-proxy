#
# Ce fichier contient le ccode python appelé le Custom Transformer
# GEO_NON_GEO_SELECTOR

import fme
import fmeobjects
import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass
    
ORDER = "_order"
FORMAT = "format"
FGP_PUBLISH = "fgp_publish"
KEYWORD_SEARCH = "_keyword_search"
LIST_SEARCH_ATTRIBUTE = "_list_search_attribute"

class GeoNoneGeoSelector(object):
    def __init__(self):
    
#        web_pdb.set_trace()
        self.csv_features =[]
        self.geo = []
        self.parameter_read = False
#        self.key_word_search = FME_MacroValues['KEYWORD_SEARCH']
#        search_att = FME_MacroValues['LIST_SEARCH_ATTRIBUTE']
#        self.lst_search_atts = search_att.split(",")
        
        
    def input(self,feature):
            
#        web_pdb.set_trace()
        if feature.getAttribute(ORDER) == 1:
            # Load CSV feature in the list
            self.csv_features.append(feature)
            
        else:
            # Process the feature
            web_pdb.set_trace()
            if not self.parameter_read:
                self.keyword_search =  feature.getAttribute(KEYWORD_SEARCH)
                tt = self.keyword_search
                search_atts =  feature.getAttribute(LIST_SEARCH_ATTRIBUTE)
                self.lst_search_atts = search_atts.split(",")
                self.parameter_read = True
                
            format_feature = feature.getAttribute(FORMAT)
            for csv_feature in self.csv_features:
               found = False
               format_csv = csv_feature.getAttribute(FORMAT)
               if format_feature == format_csv:
                  fgp_publish = csv_feature.getAttribute(FGP_PUBLISH)
                  if fgp_publish == "oui":
                      self.geo.append(feature)
                      found = True
                  break
                  
            web_pdb.set_trace()
            if not found:
                # Verify in the KEYWORD_SEARCH
                a = self.keyword_search
                b = self.lst_search_atts
                attributes = FME_utils.extract_attribute_list(feature, self.keyword_search)
                for index, attribute_name in attributes:
                    value = feature.getAttribute(attribute_name)
                    if value in self.lst_search_atts:
                        self.geo.append(feature) 
                        break                              
        self.pyoutput(feature)
        
    def close(self):
        pass
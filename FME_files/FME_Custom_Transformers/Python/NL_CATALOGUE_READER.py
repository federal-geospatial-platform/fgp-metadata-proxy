import fme
import fmeobjects
from bs4 import BeautifulSoup
from datetime import datetime
from Python.FME_utils import FME_utils


try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names

ATT_URL_DETAIL = "_html_p_div{}.a.href"
ATT_URL_ROOT = "_url_root"
ATT_URL_SECONDARY_1 = "_html_p_div{}.a.href"
ATT_URL_SECONDARY_2 = "_html_p_div{}.br.a.href"
ATT_URL_DATASET_GEO = "_url_dataset_geo"
ATT_URL_ERR = "_url_error"
ATT_URL_DATASET_NON_GEO = "_url_dataset_non_geo"
ATT_HTML_GEO_FULL = "_html_geo_full"
ATT_HTML_NON_GEO_FULL = "_html_non_geo_full"
ATT_HTML_DETAIL = "_html_detail"



def catalogue_reader_primary(feature):
    """This method reads the pimary catalogue of Newfoundland and Labrador
    
    Parameters
    ----------
    feature : FME Feature
        FME feature to process
    
    Returns
    -------
    None
    """
    
#    web_pdb.set_trace()
    # Read the geo datasets
    url_dataset_geo = FME_utils.feature_get_attribute(feature, ATT_URL_DATASET_GEO)
    if url_dataset_geo != "":
        # Read the url
        try:
            xhtml = FME_utils.extract_url_html(url_dataset_geo)
            feature.setAttribute(ATT_HTML_GEO_FULL, xhtml)
        except:
            feature.setAttribute(ATT_URL_ERR, url_dataset_geo)
            
    # Read the non geo datasets
    url_dataset_non_geo = FME_utils.feature_get_attribute(feature, ATT_URL_DATASET_NON_GEO)
    if url_dataset_non_geo != "":
        # Read the url
        try:
            xhtml = FME_utils.extract_url_html(url_dataset_non_geo)
            feature.setAttribute(ATT_HTML_NON_GEO_FULL, xhtml)
        except:
            feature.setAttribute(ATT_URL_ERR, url_dataset_non_geo)
        
    return
    
class CatalogueReaderSecondary(object):
    """This class reads the html code of each datasets.
    
    Reading of the NL datasets.
    
    For NL there is no API to extract the information in JSON and/or XML like format.
    So we must read all the HTML code and perform HTML tag extraction to get the metadata.
    The *Requests* is not working properly so we implemented the standard library urllib.request
    to read the HTML code (used in the method FME_utils.extract_url_html)
    
    """

    def __init__(self):
        """Constructor of the method.
        
        Creates an empy self.feature to prevent a crash when there is no feature to process
        
        Parameters
        ----------
        None
    
        Returns
        -------
        None
        """
        self.feature = None
        
    def input(self, feature):
        """Stores the incoming attribute.
        
        Parameters
        ----------
        feature : FME Feature object 
            FME Feature to process
            
        Returns
        -------
        None
        """
    
        self.feature = feature
        
    def close(self):
        """Read  the HTML code for each dataset.
        
        Parameters
        ----------
        None
            
        Returns
        -------
        None
        """

#        web_pdb.set_trace()
        # Prevent a crash when there is no feature to process
        if self.feature is None:
            return
            
        url_root_nl = FME_utils.feature_get_attribute(self.feature, ATT_URL_ROOT, True)
    
        # Address of the dataset are stored in 2 different ways
        att_secondary_1 = FME_utils.extract_attribute_list(self.feature, ATT_URL_SECONDARY_1)
        att_secondary_2 = FME_utils.extract_attribute_list(self.feature, ATT_URL_SECONDARY_2)

        att_web_suffix_lst = att_secondary_1 + att_secondary_2
        
        for dummy, att_web_suffix in att_web_suffix_lst:
            web_suffix = FME_utils.feature_get_attribute(self.feature, att_web_suffix)
            web_url = url_root_nl + web_suffix
            feature_cloned = self.feature.clone()
            try:
                xhtml = FME_utils.extract_url_html(web_url)
                feature_cloned.setAttribute(ATT_HTML_DETAIL, xhtml)  # Set the HTML code
            except:
                # Error occured during the url reading
                feature_cloned.setAttribute(ATT_URL_ERR, web_url)  # Set an error code
            
            self.pyoutput(feature_cloned)

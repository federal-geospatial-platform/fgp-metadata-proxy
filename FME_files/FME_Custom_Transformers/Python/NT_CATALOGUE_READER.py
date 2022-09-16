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

ROOT_URL = "https://www.geomatics.gov.nt.ca/"
ATT_HTML_CODE = "_html_code"
ATT_URL_ERR = "url_error"
ATT_CATEGORY = "_category"
WMS = "WMS"
YES = "Yes"
NO = "No"

class CatalogueReader(object):

    def __init__(self):
        pass
    def input(self,feature):

        self.in_feature = feature
    
    def _read_catalogue(self, category_name, catalogue_status, catalogue_url):
    
        status = self.in_feature.getAttribute(catalogue_status)
        if status == YES:
            url_datasets = self.in_feature.getAttribute(catalogue_url)
            tag = 'title="Go to page {0}"'
            current_page = 1
            
            url_datasets += "?page={0}"
            
            next_page = True
            
            while next_page:
                
                cloned_feature = self.in_feature.clone()
                cloned_feature.setAttribute(ATT_CATEGORY, category_name)
                url_to_read = url_datasets.format(current_page-1)
                
                # Read the url
                try:
                    xhtml = FME_utils.extract_url_html(url_to_read)
                    cloned_feature.setAttribute(ATT_HTML_CODE, xhtml)
                except:
                    cloned_feature.setAttribute(ATT_URL_ERR, url_to_read)
            
                self.pyoutput(cloned_feature)
                
                target_tag = tag.format(current_page+1)
                if xhtml.find(target_tag) != -1:
                    current_page += 1
                else:
                    # A "next page" is not found so there is no more page to read...
                    next_page = False
        
        return
    
    def close(self):
        """This method reads the pimary catalogue of Newfoundland and Labrador
        
        Parameters
        ----------
        feature : FME Feature
            FME feature to process
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        category_name = "Data"
        category_status = "_data_status"
        category_url = "_data_url"
        self._read_catalogue(category_name, category_status, category_url)

        category_name = "Maps"
        category_status = "_maps_status"
        category_url = "_maps_url"
        self._read_catalogue(category_name, category_status, category_url)

        category_name = "WMS"
        category_status = "_wms_status"
        category_url = "_wms_url"
        self._read_catalogue(category_name, category_status, category_url)
        
        category_name = "Reports"
        category_status = "_reports_status"
        category_url = "_reports_url"
        self._read_catalogue(category_name, category_status, category_url)
        
        category_name = "Documents"
        category_status = "_documents_status"
        category_url = "_documents_url"
        self._read_catalogue(category_name, category_status, category_url)
        
        category_name = "Map Viewers"
        category_status = "_map_viewers_status"
        category_url = "_map_viewers_url"
        self._read_catalogue(category_name, category_status, category_url)
                    
        return
        
def trim_text(text):
    """This method remove extra spaces and carriage return to a text.
    
    Parameters
    ----------
    text : str
        Text to process
        
    Returns:
    --------
    String
        Text with white spaces removed
    """
    return text
    if text is not None:
        text = text.replace("\n", "")
        text = text.strip()
    
    return text

class ExtractWms(object):

    """Class used to extract WMS metadata from the NWT open web site"""

    def __init__(self):
        self.in_feature = []
    
    def input(self,feature):
        self.in_feature.append(feature)

    def close(self):

        """This extracts the metadata from the flatten XHTML and creates FME attributes and FME lists.
        
        Parameters
        ----------
        feature : FME Feature
            The feature to process
            
        Returns:
        --------
        None
        """

        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(30):
                start_row = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.class" %ind)
                print ("*** Start row", ind, start_row)
                if start_row is not None:
                    # Find and extract the title of the dataset 
                    att_title = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a" %ind)
                    att_title = trim_text(att_title)
                    if att_title is not None:
                        # Create a new feature for this new title
                        new_feature = feature.clone()
                        new_feature.setAttribute("title", att_title) # Add the title
                                        
                        res = 0
                        for ind1 in range(10):
                            # Find and extract the resources of the dataset
                            att_key = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div.div.a" %(ind, ind1))
                            att_value = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div.div.a.href" %(ind, ind1))
                            att_key = trim_text(att_key)
                            att_value = trim_text(att_value)    
                            if att_key == "Metadata (REST Service)":
                                new_feature.setAttribute("resources{%i}.url" %(res), att_value)
                                new_feature.setAttribute("resources{%i}.format" %(res), "METADATA ESRI REST")
                                new_feature.setAttribute("resources{%i}.name" %(res), att_title)
                                res += 1
                            elif att_key == "OGC WMS Link":
                                new_feature.setAttribute("resources{%i}.url" %(res), att_value)
                                new_feature.setAttribute("resources{%i}.format" %(res), "WMS")
                                new_feature.setAttribute("resources{%i}.name" %(res), att_title)
                                res += 1
                            elif att_key == "Google Earth (kmz file)":
                                new_feature.setAttribute("resources{%i}.url" %(res), att_value)
                                new_feature.setAttribute("resources{%i}.format" %(res), "KMZ")
                                new_feature.setAttribute("resources{%i}.name" %(res), att_title)
                                res += 1
                            elif att_key == "ArcGIS.com (Rest Service)":
                                new_feature.setAttribute("resources{%i}.url" %(res), att_value)
                                new_feature.setAttribute("resources{%i}.format" %(res), "ESRI REST")
                                new_feature.setAttribute("resources{%i}.name" %(res), att_title)
                                res += 1
                            elif att_key == "ArcGIS Map (lyr file)":
                                new_feature.setAttribute("resources{%i}.url" %(res), att_value)
                                new_feature.setAttribute("resources{%i}.format" %(res), "LYR")
                                new_feature.setAttribute("resources{%i}.name" %(res), att_title)
                                res += 1
                        
                        for ind1 in range(10):
                            att_key = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{0}" %(ind, ind1))
                            att_key = trim_text(att_key)
                            if att_key == "Description:":
                                att_value = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.p" %(ind, ind1))
                            else:
                                att_value = feature.getAttribute("_html_p_main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            att_value = trim_text(att_value)
                            if att_key == "Description:":
                                new_feature.setAttribute("description", att_value)
                            elif att_key == "Resource Category:":
                                new_feature.setAttribute("resource_category", att_value)
                            elif att_key == "Type of resource:":
                                new_feature.setAttribute("resource_type", att_value)
                            elif att_key == "Data Category :":
                                new_feature.setAttribute("data category", att_value)
                           
                    self.pyoutput(new_feature)
                    
class ExtractMapViewers(object):

    """Class used to extract Map Viewers metadata from the NWT open web site"""

    def __init__(self):
        self.in_feature = []
    
    def input(self,feature):
        self.in_feature.append(feature)

    def close(self):

        """This extracts the metadata from the flatten XHTML and creates FME attributes and FME lists.
        
        Parameters
        ----------
        feature : FME Feature
            The feature to process
            
        Returns:
        --------
        None
        """

        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(30):
                # Find and extract the title of the dataset 
                att_title = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a" %ind)
                add_tile = None
                att_title = trim_text(att_title)
                if att_title is not None:
                    # Create a new feature for this new title
                    new_feature = feature.clone()
                    new_feature.setAttribute("title", att_title) # Add the title
                    
                    # Extract one ressource
                    ressource_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a.href" %ind)
                    ressource_value = ROOT_URL + ressource_value
                    new_feature.setAttribute("resources{0}.url", ressource_value)
                    new_feature.setAttribute("resources{0}.format", "ESRI REST")
                    new_feature.setAttribute("resources{0}.name", att_title)
                    
                    for ind1 in range(10):
                        att_key = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{0}" %(ind, ind1))
                        att_key = trim_text(att_key)
                        if att_key == "Description:":
                            att_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.p{0}" %(ind, ind1))
                        else:
                            att_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                        att_value = trim_text(att_value)
                        if att_key == "Description:":
                            new_feature.setAttribute("description", att_value)
                        elif att_key == "Resource Category:":
                            new_feature.setAttribute("resource_category", att_value)
                        elif att_key == "Type of resource:":
                            new_feature.setAttribute("resource_type", att_value)
                        elif att_key == "Data Category :":
                            new_feature.setAttribute("data_category", att_value)

                    self.pyoutput(new_feature)
                        
class ExtractReports(object):

    """Class used to extract Reports metadata from the NWT open web site"""

    def __init__(self):
        self.in_feature = []
    
    def input(self,feature):
        self.in_feature.append(feature)

    def close(self):

        """This extracts the metadata from the flatten XHTML and creates FME attributes and FME lists.
        
        Parameters
        ----------
        feature : FME Feature
            The feature to process
            
        Returns:
        --------
        None
        """

        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(30):
                # Find and extract the title of the dataset 
                att_title = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a" %ind)
                add_tile = None
                att_title = trim_text(att_title)
                if att_title is not None:
                    # Create a new feature for this new title
                    new_feature = feature.clone()
                    new_feature.setAttribute("title", att_title) # Add the title
                    
                    # Extract one ressource
                    ressource_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a.href" %ind)
                    ressource_value = ROOT_URL + ressource_value
                    new_feature.setAttribute("resources{0}.url", ressource_value)
                    new_feature.setAttribute("resources{0}.format", "PDF")
                    new_feature.setAttribute("resources{0}.name", att_title)
                    
                    for ind1 in range(10):
                        att_key = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{0}" %(ind, ind1))
                        att_key = trim_text(att_key)
                        if att_key == "Description:":
                            att_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.p" %(ind, ind1))
                        else:
                            att_value = feature.getAttribute("_html_p_div{1}.div.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                        att_value = trim_text(att_value)
                        if att_key == "Description:":
                            new_feature.setAttribute("description", att_value)
                        elif att_key == "Resource Category:":
                            new_feature.setAttribute("resource_category", att_value)
                        elif att_key == "Type of resource:":
                            new_feature.setAttribute("resource_type", att_value)
                        elif att_key == "Data Category :":
                            new_feature.setAttribute("data_category", att_value)

                    self.pyoutput(new_feature)

class ExtractMaps(object):

    """Class used to extract Maps metadata from the NWT open web site"""

    def __init__(self):
        self.in_feature = []
    
    def input(self,feature):
        self.in_feature.append(feature)

    def close(self):

        """This extracts the metadata from the flatten XHTML and creates FME attributes and FME lists.
        
        Parameters
        ----------
        feature : FME Feature
            The feature to process
            
        Returns:
        --------
        None
        """

        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(30):
                # Find and extract the title of the dataset 
                att_title = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a" %ind)
                add_tile = None
                att_title = trim_text(att_title)
                if att_title is not None:
                    # Create a new feature for this new title
                    new_feature = feature.clone()
                    new_feature.setAttribute("title", att_title) # Add the title
                    
                    # Extract one ressource
                    ressource_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a.href" %ind)
                    ressource_value = ROOT_URL + ressource_value
                    new_feature.setAttribute("resources{0}.url", ressource_value)
                    new_feature.setAttribute("resources{0}.format", "PDF")
                    new_feature.setAttribute("resources{0}.name", att_title)
                    
                    for ind1 in range(10):
                        att_key = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{0}" %(ind, ind1))
                        att_key = trim_text(att_key)
                        if att_key == "Description:":
                            att_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.p" %(ind, ind1))
                            new_feature.setAttribute("description", att_value)
                        elif att_key == "Publication date:":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.span" %(ind, ind1))                              
                            new_feature.setAttribute("publication_date", att_value)
                        elif att_key == "Type of resource:":
                            att_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("resource_type", att_value)
                        elif att_key == "Data Category :":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("data_category", att_value)
                        elif att_key == "Resource Category:":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("resource_categgory", att_value)

                    self.pyoutput(new_feature)
                        
class ExtractData(object):

    def __init__(self):
        self.in_feature = []
    
    def input(self,feature):
        self.in_feature.append(feature)

    def close(self):

        """This method extracts the NWT metadata category: Data.
        
        Parameters
        ----------
        None
            
        Returns:
        --------
        None
        """

        #web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(30):
                # Find and extract the title of the dataset 
                att_title = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a" %ind)
                add_tile = None
                att_title = trim_text(att_title)
                if att_title is not None:
                    # Create a new feature for this new title
                    new_feature = feature.clone()
                    new_feature.setAttribute("title", att_title) # Add the title
                    # Extract one ressource
                    ressource_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{0}.div.div.div.div.div.div.div.span.h3.a.href" %ind)
                    ressource_value = ROOT_URL + ressource_value
                    new_feature.setAttribute("resources{0}.url", ressource_value)
                    new_feature.setAttribute("resources{0}.format", "PDF")
                    new_feature.setAttribute("resources{0}.name", att_title)
                    for ind1 in range(10):
                        att_key = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{0}" %(ind, ind1))
                        att_key = trim_text(att_key)
                        if att_key == "Description:":
                            att_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.p" %(ind, ind1))
                            new_feature.setAttribute("description", att_value)
                        elif att_key == "Publication date:":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div.span" %(ind, ind1))                              
                            new_feature.setAttribute("publication_date", att_value)
                        elif att_key == "Type of resource:":
                            att_value = feature.getAttribute("_html_p_div.div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("resource_type", att_value)
                        elif att_key == "Data Category :":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("data_category", att_value)
                        elif att_key == "Resource Category:":
                            att_value = feature.getAttribute("_html_p_div{4}.main.div.div{1}.div{0}.div{%i}.div.span.div.div{1}.div{%i}.div{1}.div" %(ind, ind1))
                            new_feature.setAttribute("resource_category", att_value)

                    self.pyoutput(new_feature)
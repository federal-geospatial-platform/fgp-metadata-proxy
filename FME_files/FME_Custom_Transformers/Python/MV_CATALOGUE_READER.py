import fme
import fmeobjects
import re
from bs4 import BeautifulSoup
from datetime import datetime, date
from Python.FME_utils import FME_utils


try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names

ATT_URL_DETAIL = "_html_p_div{}.a.href"
ATT_URL_DATASET_GEO = "_url_dataset_geo"
ATT_URL_DATASET_NON_GEO = "_url_dataset_non_geo"
ATT_URL_ERR = "_url_error"
ATT_URL_ROOT = "_url_root"
ATT_URL_SECONDARY_1 = "_html_p_div{}.a.href"
ATT_URL_SECONDARY_2 = "_html_p_div{}.br.a.href"
ATT_HTML_GEO_FULL = "_html_geo_full"
ATT_HTML_NON_GEO_FULL = "_html_non_geo_full"
ATT_HTML_DETAIL = "_html_detail"
ATT_URL_METADATA = "url_metadata"



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
    
    web_pdb.set_trace()
    # Read the geo datasets
    url_dataset_geo = FME_utils.feature_get_attribute(feature, ATT_URL_DATASET_GEO)
    if url_dataset_geo != "":
        # Read the url

        try:
            xhtml = FME_utils.extract_url_html(url_dataset_geo)

            soup = BeautifulSoup(xhtml, "html.parser")
            xhtml_lst = soup.find_all('tbody')
            for xhtml in xhtml_lst:
                xhtml_str = xhtml.prettify()
                cloned_feature = feature.clone()
                cloned_feature.setAttribute(ATT_HTML_GEO_FULL, xhtml_str)
                self.pyoutput.cloned_feature

        except:
            feature.setAttribute(ATT_URL_ERR, url_dataset_geo)
            
#    # Read the non geo datasets
#    url_dataset_non_geo = FME_utils.feature_get_attribute(feature, ATT_URL_DATASET_NON_GEO)
#    if url_dataset_non_geo != "":
#        # Read the url
#        try:
#            xhtml = FME_utils.extract_url_html(url_dataset_non_geo)
#            feature.setAttribute(ATT_HTML_NON_GEO_FULL, xhtml)
#        except:
#            feature.setAttribute(ATT_URL_ERR, url_dataset_non_geo)
        
    return
    
class CatalogueReaderMacValley(object):
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

        # web_pdb.set_trace()
        # Read the geo datasets
        url_dataset_geo = FME_utils.feature_get_attribute(self.feature, ATT_URL_DATASET_GEO)
        if url_dataset_geo != "":
            # Read the url

            try:
                xhtml = FME_utils.extract_url_html(url_dataset_geo)

                soup = BeautifulSoup(xhtml, "html.parser")
                xhtml_lst = soup.find_all('tbody')
                for xhtml in xhtml_lst:
                    xhtml_str = xhtml.prettify()
                    cloned_feature = self.feature.clone()
                    cloned_feature.setAttribute(ATT_HTML_GEO_FULL, xhtml_str)
                    self.pyoutput(cloned_feature)

            except:
                self.feature.setAttribute(ATT_URL_ERR, url_dataset_geo)
                self.pyoutput(self.feature)


class MackenzieValleySecondary(object):
    """Class used to extract information for each document from the Mackenzie Valley web site"""

    def __init__(self):
        self.in_feature = []

    def input(self, feature):
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

        def _del_attributes():
            for attrib in feature_cloned.getAllAttributeNames():
                if attrib.startswith('_html_p_'):
                    feature_cloned.removeAttribute(attrib)

        # web_pdb.set_trace()
        logger = fmeobjects.FMELogFile()
        for feature in self.in_feature:
            # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
            for ind in range(999):
                company = feature.getAttribute("_html_p_tr{%i}.td{0}" % ind)
                project = feature.getAttribute("_html_p_tr{%i}.td{1}.a" % ind)
                code = feature.getAttribute("_html_p_tr{%i}.td{2}" % ind)
                year = feature.getAttribute("_html_p_tr{%i}.td{3}.span" % ind)
                url_suffix = feature.getAttribute("_html_p_tr{%i}.td{1}.a.href" % ind)
                if company is None and project is None and code is None and year is None and url_suffix is None:
                    break
                feature_cloned = feature.clone()
                feature_cloned.setAttribute('mv_company', company)
                feature_cloned.setAttribute('mv_project', project)
                feature_cloned.setAttribute('mv_code', code)
                feature_cloned.setAttribute('mv_year', year)
                feature_cloned.setAttribute('mv_url_suffix', url_suffix)

                _del_attributes()

                url_mv = feature_cloned.getAttribute('_url_root')
                url_detail = url_mv + url_suffix

                xhtml = FME_utils.extract_url_html(url_detail)
                feature_cloned.setAttribute('_html_detail', xhtml)

                soup = BeautifulSoup(xhtml, "html.parser")
                xhtml_lst = soup.find_all('tbody')
                logger = fmeobjects.FMELogFile()
                try:
                    feature_cloned.setAttribute('_html_desc', xhtml_lst[0].prettify())
                except:
                    logger.logMessageString("No details found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)

                try:
                    feature_cloned.setAttribute('_html_ref1', xhtml_lst[1].prettify())
                except:
                    logger.logMessageString("No references found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)

                try:
                    feature_cloned.setAttribute('_html_ref2', xhtml_lst[2].prettify())
                except:
                    logger.logMessageString("No references found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)

                xhtml_lst = soup.find_all(attrs = {"class": "field field-name-field-body field-type-text-long field-label-hidden clearfix"})
                try:
                    feature_cloned.setAttribute('_html_def', xhtml_lst[0].prettify())
                except:
                    logger.logMessageString("No description found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)

                self.pyoutput(feature_cloned)

def MackenzieValleyDetail(feature):

    logger = fmeobjects.FMELogFile()

    # web_pdb.set_trace()
    for i in range(4):
        code = feature.getAttribute("_html_pd_tr{%i}.th" %i)
        if code is None:
            break
        if "type" in code.lower():
            type = feature.getAttribute("_html_pd_tr{%i}.td" %i)
            feature.setAttribute('type', type)
        elif "status" in code.lower():
            status = feature.getAttribute("_html_pd_tr{%i}.td" %i)
            feature.setAttribute('status', status)
        elif "contact" in code.lower():
            contact = feature.getAttribute("_html_pd_tr{%i}.td.a" %i)
            email_str = feature.getAttribute("_html_pd_tr{%i}.td.a.href" %i)
            email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})')
            email_match = re.findall(email_pattern, email_str)
            feature.setAttribute('contact', contact)
            feature.setAttribute('email', email_match[0])
        else:
            pass

    # web_pdb.set_trace()
    url_root = feature.getAttribute(ATT_URL_ROOT)
    ind = 0
    for html_prefix in ("_html_ref1_", "_html_ref2_"):
        for i in range(9999):
            att = html_prefix+"tr{%i}.td{0}.a" %i
            title = feature.getAttribute(att)
            title = feature.getAttribute (html_prefix+"tr{%i}.td{0}.a" %i)
            link = feature.getAttribute (html_prefix+"tr{%i}.td{0}.a.href" %i)
            date = feature.getAttribute (html_prefix+"tr{%i}.td{1}" %i)
            if title is None and link is None and date is None:
                break
            if title is None: title = ""
            if link is None:
                title = ""
            else:
                link = url_root + link
            if date is None: title = ""
            feature.setAttribute("ref{%i}.title" %i, title)
            feature.setAttribute("ref{%i}.link" %i, link)
            feature.setAttribute("ref{%i}.date" %i, date)
            i += 1

    description = feature.getAttribute("_html_pdef_p")
    if description is None:
        description = ""
    feature.setAttribute("description", description)

    return
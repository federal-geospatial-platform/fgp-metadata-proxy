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
ATT_HTML_GEO_FULL = "_html_geo_full"


class CatalogueReaderMacValley(object):
    """This class reads the html code of each datasets.
    
    Reading of the Mavckenzy Valley datasets.
    
    For Mackenzy Valley there is no API to extract the information in JSON and/or XML like format.
    So we must read all the HTML code and perform HTML tag extraction to get the metadata.
    
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
        """Read  the HTML code for the MV web site. Break into different FME feature for <tbody> tag
        in the XML dcument.
        
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
                    # Create a FME feature for each <tbody> tag.
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
            """This routine deletes all the attributes that starts with a predefined prefix."""

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
                try:
                    feature_cloned.setAttribute('_html_desc', xhtml_lst[0].prettify())
                except:
                    logger.logMessageString("No details found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)


                # web_pdb.set_trace()
                xhtml_lst = soup.find_all(attrs = {"class": "field field-name-field-body field-type-text-long field-label-hidden clearfix"})
                try:
                    description = str(xhtml_lst[0].p.string)
                    feature_cloned.setAttribute("mv_description", description)
                except:
                    logger.logMessageString("No description found in HTML code in URL {0}".format(url_detail), fmeobjects.FME_WARN)
                    feature_cloned.setAttribute("mv_description", "")

                pos = xhtml.find("Total Documents (")
                pos_start = xhtml[pos:].find('"')
                pos_end = xhtml[pos+pos_start+1:].find('"')
                if pos != -1 and pos_start != -1 and pos_end != -1:
                    # Extract the list of document
                    try:
                        txt_start = pos+pos_start+1
                        url_doc_suffix = xhtml[txt_start:txt_start+pos_end]
                        url_doc_all = url_mv + url_doc_suffix
                        xhtml = FME_utils.extract_url_html(url_doc_all)

                        soup = BeautifulSoup(xhtml, "html.parser")
                        soup_lst = soup.find_all(attrs={"class": "views-row"})

                        i = 0
                        for item in soup_lst:

                            # web_pdb.set_trace()
                            titre = str(item.h3.a.string)
                            url_doc = str(item.h3.a['href'])

                            items = item.find_all(attrs={"class": "views-field views-field-file-size"})
                            doc_size = str(items[0].span.string)

                            items = item.find_all(attrs={"class": "views-field views-field-date-received"})
                            sub_items = items[0].find_all(attrs={"class": "field-content"})
                            date_recu = str(sub_items[0].string)

                            items = item.find_all(attrs={"class": "views-field views-field-document-date"})
                            sub_items = items[0].find_all(attrs={"class": "field-content"})
                            date_doc = str(sub_items[0].string)

                            items = item.find_all(attrs={"class": "views-field views-field-originator"})
                            sub_items = items[0].find_all(attrs={"class": "field-content"})
                            originator = str(sub_items[0].string)

                            # web_pdb.set_trace()
                            items = item.find_all(attrs={"class": "views-field views-field-document-stage-name"})
                            sub_items = items[0].find_all(attrs={"class": "field-content"})
                            doc_name = str(sub_items[0].string)

                            feature_cloned.setAttribute('mv_ref{%i}.titre' %i, titre)
                            feature_cloned.setAttribute('mv_ref{%i}.url' %i, url_mv + url_doc)
                            feature_cloned.setAttribute('mv_ref{%i}.doc_size' %i, doc_size)
                            feature_cloned.setAttribute('mv_ref{%i}.date_recu' %i, date_recu)
                            feature_cloned.setAttribute('mv_ref{%i}.date_doc' %i, date_doc)
                            feature_cloned.setAttribute('mv_ref{%i}.originator' %i, originator)
                            feature_cloned.setAttribute('mv_ref{%i}.doc_name' %i, doc_name)
                            i += 1

                    except:
                        logger.logMessageString("Unable to extract the  content of the URL {0}".format(url_doc_suffix),
                                                fmeobjects.FME_WARN)
                else:
                    # Unable to locate the URL suffix of the documentation
                    logger.logMessageString("Unable to find the URL of the documents {0}".format(url_doc_suffix),
                                            fmeobjects.FME_WARN)


                # Extract the project date range
                # web_pdb.set_trace()
                try:
                    url_date = url_mv + url_suffix + "/timeline"
                    xhtml = FME_utils.extract_url_html(url_date)
                    feature_cloned.setAttribute('_html_timeline', xhtml)

                    soup = BeautifulSoup(xhtml, "html.parser")
                    start_lst = soup.find_all(attrs={"class": "date-display-start"})
                    end_lst = soup.find_all(attrs={"class": "date-display-end"})
                    try:
                        feature_cloned.setAttribute("mv_date_start", str(start_lst[0].string))
                        feature_cloned.setAttribute('mv_date_end', str(end_lst[0].string))
                    except:
                        logger.logMessageString("No date range found in HTML code in URL {0}".format(url_date),
                                                fmeobjects.FME_WARN)
                except:
                    feature_cloned.setAttribute('_html_timeline', "<empty>")

                self.pyoutput(feature_cloned)

def MackenzieValleyDetail(feature):
    """This routine sets different FME attributes from the flatten XML documents.

        Parameters
        ----------
        feature : FME Feature
                The feature to process

        Returns:
        --------
        None
        """

    def _set_min_max_date():
        # If nodate are present this module extract the min max date from the date in the references

        # Check if start date and end date exist
        date_start = feature.getAttribute("mv_date_start")
        date_end = feature.getAttribute('mv_date_end')

        if date_start is None and date_end is None:
            # The start and end dates do not exist
            ind = FME_utils.max_index_attribute_list(feature, "mv_ref{}.date_doc")
            date_lst = []
            # Loop over the reference to extract the dates
            for i in range(ind):
                date_doc = feature.getAttribute("mv_ref{%i}.date_doc" % i)
                date_doc = date_doc.replace("\n", "")  # remove all \n (return)
                date_doc = date_doc.strip()  # Remove starting and ending whitespaces

                try:
                    date = datetime.strptime(date_doc, "%b %d, %Y")  # Convert string date to object date
                    date_lst.append(date)
                except:
                    pass

            if len(date_lst) >= 1:
                # Extract the min date, max date and set the attributes
                date_start = min(date_lst)
                date_end = max(date_lst)
                feature.setAttribute("mv_date_start", date_start.strftime("%b %d, %Y"))
                feature.setAttribute("mv_date_end", date_end.strftime("%b %d, %Y"))

    def _set_lat_lon():
        # Set the latitute and longitude

        html = feature.getAttribute("_html_detail")  # Get the flattend xml code
        try:
            lat_lon_start = html.find("deltas")
            lat_lon_end = html[lat_lon_start:].find("}") + lat_lon_start
            lat_lon_str = '{"' + html[lat_lon_start:lat_lon_end] + "}}}"
            lat_lon_dict = eval(lat_lon_str)  # Transform the string into a dictionary
            lat = float(lat_lon_dict["deltas"]["d_0"]["lat"])  # extract the lat
            lon = float(lat_lon_dict["deltas"]["d_0"]["lng"])  # Extract the lon
        except:
            # Any error during lat/lon extraction will reset the lat/lon to 0.
            lat = 0.
            lon = 0.

        # Set the FME attributes
        feature.setAttribute("mv_lat", lat)
        feature.setAttribute("mv_lon", lon)

    def _set_contact_info():
        # Extract different information from the flatten XML code

        for i in range(4):
            code = feature.getAttribute("_html_pd_tr{%i}.th" % i)
            if code is None:
                break
            if "type" in code.lower():
                type = feature.getAttribute("_html_pd_tr{%i}.td" % i)
                feature.setAttribute('mv_type', type)
            elif "status" in code.lower():
                status = feature.getAttribute("_html_pd_tr{%i}.td" % i)
                feature.setAttribute('mv_status', status)
            elif "contact" in code.lower():
                contact = feature.getAttribute("_html_pd_tr{%i}.td.a" % i)
                email_str = feature.getAttribute("_html_pd_tr{%i}.td.a.href" % i)
                email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})')
                email_match = re.findall(email_pattern, email_str)
                feature.setAttribute('mv_contact', contact)
                feature.setAttribute('mv_email', email_match[0])
            else:
                pass

    logger = fmeobjects.FMELogFile()

    # web_pdb.set_trace()
    # Set contact information
    _set_contact_info()

    # Set the lat/lon
    _set_lat_lon()

    # Set the start end date (if missing)
    _set_min_max_date()

    return
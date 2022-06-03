import fme
import fmeobjects
#from bs4 import BeautifulSoup
#from datetime import datetime
from Python.FME_utils import FME_utils


try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names

ATT_URL_ROOT = "_url_root"


            
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

def extract_html_tags(feature):
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
    ind = 0
    # Loop over the flatten XHTML document in order to extract specific tags into FME attribute
    while ind != -1:
        tag = feature.getAttribute("_html_s_body.div{2}.div.dl.dt{%i}.strong" %ind)
        if tag is None:
            # Reading of attributes is terminated
            ind = -1
        else:
            tag = trim_text(tag)
            att_fme = None
            if tag == "Title:":
                att_fme = "title"
                
            elif tag == "Type:":
                att_fme = "type"
                
            elif tag == "Creator:":
                att_fme = "sector"
                
            elif tag == "Contact Email:":
                att_fme = "contacts{0}.email"
                
            elif tag == "Geographical Coverage:":
                att_fme = "geographical_coverage"
                
            elif tag == "Description:":
                att_fme = "note"
                
            elif tag == "Contributor:":
                att_fme = "contributor"
                
            elif tag == "Publisher:":
                att_fme = "publisher"
                
            elif tag == "Temporal Coverage:":
                att_fme = "data_collection_start_date"
                
            elif tag == "Released Date:":
                att_fme = "record_create_date"
                
            elif tag == "Modified Date:":
                att_fme = "record_published_date"
                
            elif tag == "Rights:":
                att_fme = "license_id"
            else:
                pass
                          
            if att_fme is not None:
                att_value = FME_utils.feature_get_attribute(feature, "_html_s_body.div{2}.div.dl.dd{%i}" %ind)
                feature.setAttribute(att_fme, att_value)
            else:
                # Log unknown tag found in the HTML code
                log_text = "Found unknown tag within HTML code: {0}".format(tag)
                logger.logMessageString(log_text, fmeobjects.FME_WARN)
            
            ind += 1
    
    # Extract the topics
    ind = 0
    while ind != -1:
        topic = feature.getAttribute("_html_s_body.div{2}.div.div{0}.ul.li{%i}.a" %ind)
        topic = trim_text(topic)
        if topic is None:
            # Reading of attributes is terminated
            ind = -1
        else:   
            feature.setAttribute("tags{%i}.display_name" %ind, topic)
            ind += 1
            
    # Extract the resources
    ind_tag = 1
    url_root = feature.getAttribute(ATT_URL_ROOT)
    while ind_tag != -1:
        name = feature.getAttribute("_html_s_body.div{2}.div.div{1}.table.tr{%i}.td{0}" %ind_tag)
        file_format = feature.getAttribute("_html_s_body.div{2}.div.div{1}.table.tr{%i}.td{2}" %ind_tag)
        url_ref = feature.getAttribute("_html_s_body.div{2}.div.div{1}.table.tr{%i}.td{5}.a.href" %ind_tag)
        if file_format is None or url_ref is None or name is None:
            # Reading of attributes is terminated
            ind_tag = -1
        else:
            ind_res = ind_tag - 1
            url_ref = url_root + url_ref
            name = trim_text(name)
            feature.setAttribute("resources{%i}.name" %ind_res, name)
            file_format = trim_text(file_format)
            feature.setAttribute("resources{%i}.format" %ind_res, file_format)
            url_ref = trim_text(url_ref)
            feature.setAttribute("resources{%i}.url" %ind_res, url_ref)
            ind_tag += 1
            
    return

import re
import fmeobjects

def extract_attribute_list(feature, att_name):

    """This method extracts a subset of the attribute of a feature.
    
    If the the attribute name to extract is not a list (ex.: value) than only one 
    attribute is extracted.
    
    If the attribute name to extract is a list (ex.: ressources{}.name) than all the
    attributes of the list is extrated.
    
    The method returns a list of tuple one tuplee for each attribute to extract. The 
    tuple is composed of 2 values the first is the complete attribute name: 
    ex.: value for none list attribute or ressources{1}.name for list attribute.  The 
    seconde value of the list is the index value: None for non list attribute or "1" for 
    essources{1}.name for list attribute.
    
    :param: feature: FME feature to process
    :param: att_name: The name of the attribute to extract
    """

    atts = []
    feature_atts = feature.getAllAttributeNames()  # Extract all attribute names
    logger = fmeobjects.FMELogFile()
    regex_list = "\{\d+\}"
    regex_index = "\d+"

    if att_name.find("{}") != -1:
        # The attribute to search is a list
        regex_search = att_name.replace("{}", regex_list)
        for feature_att in feature_atts:
            list_index = re.findall(regex_search , feature_att)  # Check if attribute name is present
            if len(list_index) == 1:
                index = re.findall(regex_index, list_index[0])  # Extract the index value
                if len(index) == 1:
                    if index[0].isdigit():  #Validate index is a number
                        atts.append((int(index[0]), feature_att))
                    else:
                        logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
                else:
                    logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
    else:
        # The attribute to search is not a list
        for feature_att in feature_atts:
            if att_name == feature_att:
                atts.append((None, att_name))
                break

    return atts

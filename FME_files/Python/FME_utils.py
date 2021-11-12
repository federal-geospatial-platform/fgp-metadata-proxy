import re
import fmeobjects
import yaml
import traceback

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

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

def repair_attribute_list(feature, att_list_name, default_att_name=[]):

    """This method repairs a list by creating the missing attribute in a list.
    
    For example if the list resources{} contains the following attributes
      - resources{0}.a
      - resources{1}.a
      - resources{1}.b
      - resources{3}.a
    This method will create with empty values the following missing attribute:
      - resources{0}.b
      - resources{2}.a
      - resources{2}.b
      - resources{3}.b
    
    :param: feature: FME feature to process
    :param: att_list_name: Name of the attribute to extract (ex: values{})
    :parama: default_att_name: ...
    """
    
    att_names = default_att_name
    max_index = -1
    regex_list = "\{\d+\}"
    regex_index = "\d+"
    logger = fmeobjects.FMELogFile()
    
#    web_pdb.set_trace()
    if att_list_name.find("{}") != -1:    
        # Extract only the attribute to process
        attributes = extract_attribute_list(feature, att_list_name)
        
        for index, attribute in attributes:
            if index > max_index:
                max_index = index  # Set the maximum index number
                
            # Build the list of names (after the dot; ex: att{99}.name)
            att_split = attribute.split(".")
            att_name = att_split[1]
            if att_name not in att_names:
               att_names.append(att_name)  # Update the list
               
        # Repair the missing attributes names in the attribute list
        for index in range(max_index+1):
            for att_name in att_names:
                attribute = att_list_name.replace('{}', '{%i}') + '.' + att_name
                attribute = attribute%index  # Add the index number 
                if not feature.getAttribute(attribute):
                    feature.setAttribute(attribute, '')
                    
        # Validate reparation
        attributes = extract_attribute_list(feature, att_list_name)
        if len(attributes) == (max_index+1) * len(att_names):
            # Reparation works
            pass
        else:
            logger.logMessageString("Internal error: {}".format(att_list_name), fmeobjects.FME_ERROR)
                    
    else:
        logger.logMessageString("Not a valid attribute list: {}".format(att_list_name), fmeobjects.FME_WARN)    
            
    return

def load_yaml_document(yaml_str_document):
    """ This method loads a YMAL document from a string.
    
    :param: str_yaml: String containing a YAML document
    
    """
    
    try:
        # Load the YMAL directives into python dictionnaries
        yaml_document = yaml.safe_load(yaml_str_document)
    except Exception:
        traceback.print_exc()
        raise Exception("Error loading YAML document: \n{}".format(yaml_str_document))

    return yaml_document
        
    
    
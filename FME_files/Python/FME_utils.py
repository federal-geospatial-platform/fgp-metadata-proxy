import re
import fmeobjects
import yaml
import traceback
from typing import NamedTuple


try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

class CsvGeoSpatialValidation(NamedTuple):
    """Class containing one row from the CSV GeoSpatialValidation.
    
    Attributes
    ----------
    fgp_publish: str
        Flag (oui/non) indicating if this format is published in the FGP
    format: str
        Name of the format
    spatial_type: str
        Spatial type code
    """
    
    fgp_publish: str
    format: str
    spatial_type: str

class FME_utils:

    @staticmethod
    def extract_attribute_list(feature, att_name):
        """This method extracts a subset of the attributes of a feature.
        
        If the the attribute name to extract is not an FME list (ex.: value) than only one 
        attribute is extracted.
        
        If the attribute name to extract is a list (ex.: ressources{}.name) than all the
        attributes of the list is extrated.
        
        The method returns a list of tuple one tuplee for each attribute to extract. The 
        tuple is composed of 2 values the first is the complete attribute name: 
        ex.: value for none list attribute or ressources{1}.name for list attribute.  The 
        seconde value of the list is the index value: None for non list attribute or "1" for 
        ressources{1}.name for list attribute.
        
        Parameters
        ----------
        feature: FME Feature
            FME feature to process
        att_name: str
            The name of the attribute to extract
        
        Returns
        -------
        list
            a list of FME attribute
        """

#        web_pdb.set_trace()
        atts = []
        feature_atts = feature.getAllAttributeNames()  # Extract all attribute names
        logger = fmeobjects.FMELogFile()
        regex_list = "\{\d+\}"
        regex_index = "\d+"

        if att_name.find("{}") != -1:
            # The attribute to search is a list
            att_name = "^" + att_name + "$"  # Regular expression exact match
            regex_search = att_name.replace("{}", regex_list)
            for feature_att in feature_atts:
                att_lst = re.match(regex_search , feature_att)  # Check if attribute name is present
                if att_lst is not None:
                    index_lst = re.findall(regex_list, att_lst[0])  # Extract the index with "{}"
                    if len(index_lst) == 1:
                        index = re.findall(regex_index, index_lst[0])  # Extract the index number
                        if len(index) == 1:
                            if index[0].isdigit():  #Validate index is a number
                                atts.append((int(index[0]), feature_att))
                            else:
                                logger.logMessageString("List is not valid: {}".format(feature_att), fmeobjects.FME_WARN)
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
        # Sort the list indexes as FME getAllAttributeNames break the order of the list
        atts.sort()

        return atts

    @staticmethod
    def repair_attribute_list(feature, att_list_name, default_att_name=None):
        """This method repairs a list by creating the missing attribute in a list.
        
        For example if the list resources{} contains the following attributes:
        
          - resources{0}.a
          - resources{1}.a
          - resources{1}.b
          - resources{3}.a
          
        This method will create with empty values the following missing attribute:
        
          - resources{0}.b
          - resources{2}.a
          - resources{2}.b
          - resources{3}.b
        
        Parameters
        ----------
        feature: FME feature
            FME feature to process
        att_list_name: list
            Name of the attribute to extract (ex: values{})
        default_att_name: list
            List of attribute that will be added to the feature even if none is present
            
        Returns
        -------
        None
        """

        # Managing mutable default values
        if default_att_name is None:
            att_names = []
        else:
            att_names = list(default_att_name)
        max_index = -1
        regex_list = "\{\d+\}"
        regex_index = "\d+"
        logger = fmeobjects.FMELogFile()
        
    #    web_pdb.set_trace()
        if att_list_name.find("{}") != -1:    
            # Extract only the attribute to process
            attributes = FME_utils.extract_attribute_list(feature, att_list_name)
            
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
            attributes = FME_utils.extract_attribute_list(feature, att_list_name)
            if len(attributes) == (max_index+1) * len(att_names):
                # Reparation works
                pass
            else:
                logger.logMessageString("Internal error: {}".format(att_list_name), fmeobjects.FME_ERROR)
                        
        else:
            logger.logMessageString("Not a valid attribute list: {}".format(att_list_name), fmeobjects.FME_WARN)    

        return

    @staticmethod
    def load_yaml_document(yaml_str_document):
        """ This method loads a YMAL document from a string.
        
        Parameters
        ----------
        str_yaml: str
            String containing a YAML document
            
        Returns
        -------
        dict
            YAML structure in dictionnaries
            
        Raises
        ------
        Exception 
            If the YAML is not well formed
        """
        
        try:
            # Load the YMAL directives into python dictionnaries
            yaml_document = yaml.safe_load(yaml_str_document)
        except Exception:
            traceback.print_exc()
            raise Exception("Error loading YAML document: \n{}".format(yaml_str_document))

        return yaml_document
        
    @staticmethod
    def create_set_of_word(str_words, separator = " ", lower = True):
        """Create a set of words from a string of words.
        
        A set will remove duplicate words
        
        Parameters
        ----------
        str_words: str
            A string of words
        separator: str
            A character that delimits word in a string (default is space " ")
        lower: bool
            If set to True the result will be transformed in lower case; If flase no action is taken
            
        Returns
        -------
        Set
            A set of word
        """
        
        word_lst = str_words.split(separator)
        if lower:
            word_lst = [word.lower() for word in word_lst]
             
        # Create the set of words    
        word_set = set(word_lst)
         
        return word_set
        
    
    
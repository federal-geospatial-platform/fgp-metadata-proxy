#
# Ce fichier contient le ccode python appelé le Custom Transformer
# LOOKUP_TABLE_READER_NG


import fme
import fmeobjects
import os
import yaml
import traceback
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

#
#-check_file_present-----------------------------------------------------------
#
def check_file_present(feature):
# This method checks if a file is present in the shared or the province directory
    
#    web_pdb.set_trace()
    # Manage if execution is done locally or on FME Server
    if r'fmeserver' in feature.getAttribute('_fme_home').lower():
        spacer=r'/'
    else:
        spacer="\\"
    
    # Extract some attributes
    csv_path = feature.getAttribute('_csv_path')
    file_name = feature.getAttribute('_feature_type')
    pt = feature.getAttribute('_pt')
    
    file_error = ""
    
    # Create the root file name for the shared and the province specific file to read
    root_shared = '%s%s%s%s%s'%(csv_path, spacer, 'SHARED', spacer, file_name)
    root_path = '%s%s%s%s%s'%(csv_path,spacer, pt, spacer, file_name)
    
    # Add the file extension
    file_shared = root_shared + ".csv"
    file_path = root_path +  ".csv"
    yaml_shared = root_shared + ".yaml"
    yaml_path = root_path + ".yaml"
    
    # Check if the file and the yaml are in the province path directory
    if os.path.exists(file_path) and os.path.exists(yaml_path):
        file2read = file_path
        yaml2read = yaml_path
    else:
        # Check if the file and the yaml are present in the shared  
        if os.path.exists(file_shared) and os.path.exists(yaml_shared):
            file2read = file_shared
            yaml2read = yaml_shared
        else:
            # Set error
            file_error = "Lookup table and/or yaml are missing"
            file2read = ""
            yaml2read = ""
    
    # Set the FME attribute
    feature.setAttribute("_file2read", file2read)
    feature.setAttribute("_yaml2read", yaml2read)
    feature.setAttribute("_file_error", file_error)
#
#
#-LoadValidateYaml-------------------------------------------------------------
#
# Constant for the YAML directives
CHECK_DOMAIN = "CHECK_DOMAIN"
CREATE_KEY_VALUE = "CREATE_KEY_VALUE"
CSV_COLUMNS = "CSV_COLUMNS"
NO_DUPLICATE = "NO_DUPLICATE"
# List of directives
LST_DIRECTIVES = [CSV_COLUMNS, CREATE_KEY_VALUE, NO_DUPLICATE, CHECK_DOMAIN]

CSV_ERROR = "_csv_error"  # Name of the FME attribute containing the FME errors
CSV_DIRECTIVES = "_csv_directives"  # Name of the FME attribute containing the YAML
TEXT_LINE_DATA = "text_line_data"

# Contstant for the record type
FEATURE = 'feature'
SCHEMA = 'schema'
YMAL = 'yaml'
RECORD_TYPE = "_record_type"

# Constant for the actions in the Y
EXPLODE = "explode"
LOWER = "lower"
NO_NULL = "no_null"
TRIM = "trim"
UPPER = "upper"
# List of actions
LST_ACTION = [LOWER, UPPER, TRIM, EXPLODE, NO_NULL]

class LoadValidateYaml(object):
    """Template Class Interface:
    When using this class, make sure its name is set as the value of the 'Class
    to Process Features' transformer parameter.
    """

    def __init__(self):
        """Base constructor for class members."""
        
        # Create instance attribute needed for the processing
        self.features = []  # List to accumulate the features
        self.directive_errors = ""  # Contains the errors found
        pass
        
    def _process_yaml(self):
        
        # Read the CSV YMAL directives from the attribute
        str_csv_directives = self.yaml.getAttribute(TEXT_LINE_DATA)
        try:
            # Load the YMAL directives into python dictionnaries
            dict_directives = yaml.safe_load(str_csv_directives)
        except Exception:
            traceback.print_exc()
            self.directive_errors = "Error schema"
            return
    
        # Load the name of the column from the schema feature        
        csv_column_names = []
        lst_attributes = FME_utils.extract_attribute_list(self.schema, 'attribute{}.name')
        for index, attribute in lst_attributes:
            column_name = self.schema.getAttribute(attribute)
            csv_column_names.append(column_name)
            
        # Validate the content and form of the YAML CSV directives
        lst_directives = dict_directives.keys()
        for directive in lst_directives:
            if directive not in LST_DIRECTIVES:
               self.directive_errors += "ERROR`Unknown YMAL directives: " + str(directive) + "\n"
        if self.directive_errors != "":
           # There is an error do not continue
           return
        
        # Validate the content of the CSV_COLUMNS section in the YAML
        csv_directives = dict_directives[CSV_COLUMNS]
        if csv_directives is not None:
            for column_name, lst_actions in csv_directives.items():
                if isinstance(lst_actions, list):
                    if column_name not in csv_column_names:
                        self.directive_errors += "ERROR: YAML column name in CSV_COLUMNS do not match CSV: {} \n".format(str(column_name))
                    for action in lst_actions:
                        if action not in LST_ACTION:
                            self.directive_errors += "ERROR: YAML action is not known. Column: {}; Action: {} \n".format(str(column_name), str(action))
                else:
                    # Must be a list 
                    self.directive_errors += "ERROR: YAML actions must be a list []. Column: {} \n".format(str(column_name))
                
        # Validate the content of the CREATE_KEY_VALUE section in the YAML
        csv_directives = dict_directives[CREATE_KEY_VALUE]
        if csv_directives is not None:
            for key, value in csv_directives.items():
                if key not in csv_column_names or value not in csv_column_names:
                    self.directive_errors += "ERROR: YAML (Key,value) names unknown: {}, {} \n".format(str(key), str(value))
        else:
            # CREATE_KEY_VALUE is empty: no problem
            pass
                
        # Validate the content of the NO_DUPLICATE section in the YAML
        csv_directives = dict_directives[NO_DUPLICATE]
        if csv_directives is not None:
            for dummy, lst_column_names in csv_directives.items():
                if isinstance(lst_column_names, list):
                    # Loop over the list to validate the content
                    for column_name in lst_column_names:
                        # Check that each column_name is valid
                        if column_name not in csv_column_names:
                            self.directive_errors += "ERROR: YAML NO_DUPLICATE Unknown column names: {} \n".format(str(column_name))
                else:
                    # Duplicate columns must be a list
                    self.directive_errors += "ERROR: YAML NO_DUPLICATE must be a list. Column name: {} \n".format(str(lst_column_names))
        else:
            # NO_DUPLICATE is empty: no problem
            pass
            
        # Validate the content of the CHECK_DOMAIN section in the YAML
        csv_directives = dict_directives[CHECK_DOMAIN]
        if csv_directives is not None:
            for column_name, lst_domain in csv_directives.items():
                if isinstance(lst_domain, list):
                    if column_name not in csv_column_names:
                        self.directive_errors += "ERROR: YAML column name in CHECK_DOMAIN do not match CSV: {} \n".format(str(column_name))
                else:
                    # Must be a list 
                    self.directive_errors += "ERROR: YAML actions must be a list []. Column: {} \n".format(str(column_name))    

        return dict_directives
        
    
    def _process_no_duplicate(self, dict_no_duplicate):
        
        # Create new attribute from a key/value pair
        for dummy, column_names in dict_no_duplicate.items():
            dict_no_duplicate = {}
            key_values = []
            for feature in self.features:
                for column_name in column_names:
                    column_value = feature.getAttribute(column_name)
                    key_values.append(column_value)
                if column_value in dict_no_duplicate.keys():
                    # Duplicate value found
                    self.directive_errors += "Column: {0}: Duplicate keys \n".format(str(column_name))
                else:
                    dict_no_duplicate[column_value] = "dummy"

    def _process_create_key_value(self, dict_key_value):
        
        # Create new attribute from a key/value pair
        for key_column, value_column in dict_key_value.items():
            for feature in self.features:
                key = feature.getAttribute(key_column)
                value = feature.getAttribute(value_column)
                feature.setAttribute(key, value)

    def _process_check_domain(self, dict_check_domain):
        
        # Check the domain of the columns
        for key_column, lst_domains in dict_check_domain.items():
            for feature in self.features:
                value = feature.getAttribute(key_column)
                if value not in lst_domains:
                    # Domain is not valid
                    self.directive_errors += "Column: {0}: value: {1}: Invalid domain \n".format(str(key_column), str(value))
                
    
    def _process_csv_columns(self, dict_csv_columns):
        
        
        # Process the EXPLODE action first that duplicate features
        for column_name, action_list in dict_csv_columns.items():
            if EXPLODE in action_list:
                # Loop over each features
                for feature in self.features:
                    # Explode the feature if the attribute contains values separated by coma ","
                    att_value = feature.getAttribute(column_name)
                    if att_value is not None:
                        explode_values = att_value.split(";")
                        if len(explode_values) >=2:
                            feature_to_clone = feature.clone()
                            # Explode the attribute list into different features
                            for index, explode_value in enumerate(explode_values):
                                if index == 0:
                                    # No need to duplicate the first feature
                                    pass
                                else:
                                    # Duplicate the feature and append the feature to the list
                                    feature = feature_to_clone.clone()
                                    self.features.append(feature)
                                # Set the new attribute value
                                feature.setAttribute(column_name, explode_value)
                        else:
                            # The list contains only one value nothing to explode 
                            pass
                            
        for feature in self.features:
            for column_name, action_list in dict_csv_columns.items():                
                att_value = feature.getAttribute(column_name)
                if att_value is not None and isinstance(att_value, str):                                    
                    # Check if lower case is requested
                    if LOWER in action_list:
                        att_value = att_value.lower()
                        
                    # Check if upper case is requested
                    if UPPER in action_list:
                        att_value = att_value.upper()
                        
                    # Check if trimming is requested
                    if TRIM in action_list:
                        att_value = att_value.strip()
                        
                # Check if NO_NULL checking is requested
                if NO_NULL in action_list:
                    if att_value is None or att_value == "":
                        self.directive_errors += "Column: {0}: No null error \n".format(column_name)
                
                # Update edited field
                feature.setAttribute(column_name, att_value)

        return
    
    def input(self, feature):
        """This method is called for each FME Feature entering the 
        PythonCaller. If knowledge of all input Features is not required for 
        processing, then the processed Feature can be emitted from this method 
        through self.pyoutput(). Otherwise, the input FME Feature should be 
        cached to a list class member and processed in the close() method.

        :param fmeobjects.FMEFeature feature: FME Feature entering the transformer.
        """
        
        record_type = feature.getAttribute(RECORD_TYPE)
        if record_type == FEATURE:
            # Accumulate the feature for further processing
            self.features.append(feature)
        elif record_type == SCHEMA:
            # Accumulate the schema for furture processing
            self.schema = feature
        else:
            # Accumulate the YMAL for future processing
            self.yaml = feature

    def close(self):
        """This method is called once all the FME Features have been processedfrom input().
        """
        
#        web_pdb.set_trace()  # Breakpoint
        # Read and validate the schema record
        dict_directives = self._process_yaml()
        if self.directive_errors != "":
            # Schema is invalid set the attribute and output the schema
            self.yaml.setAttribute(CSV_ERROR, self.directive_errors)
            self.pyoutput(self.yaml)
            
        else:
            
            # Only process the CSV if the schema is valid
            # Process the CSV_COLUMNS directives
            if CSV_COLUMNS in dict_directives:
                dict_csv_columns = dict_directives[CSV_COLUMNS]
                if dict_csv_columns is not None:
                    self._process_csv_columns(dict_csv_columns)
                else:
                    # CSV_COLUMNS is empty: No problem
                    pass
                
            # Process the CREATE_VALUE_PAIR directives
            if CREATE_KEY_VALUE in dict_directives:
                dict_key_value = dict_directives[CREATE_KEY_VALUE]
                if dict_key_value is not None:
                    self._process_create_key_value(dict_key_value)
                else:
                    # CREATE_KEY_VALUE is empty: No problem
                    pass
            
            # Process the NO_DUPLICATE directives
            if NO_DUPLICATE in dict_directives:
                dict_no_duplicate = dict_directives[NO_DUPLICATE]
                if dict_no_duplicate is not None:
                    self._process_no_duplicate(dict_no_duplicate)
                else:
                    # NO_DUPLICATE is empty: No problem
                    pass
                    
            # Process the CHECK_DOMAIN directives
            if CHECK_DOMAIN in dict_directives:
                dict_check_domain = dict_directives[CHECK_DOMAIN]
                if dict_check_domain is not None:
                    self._process_check_domain(dict_check_domain)
                else:
                    # check_domain is empty: No problem
                    pass
                  
            # Output the features
            for feature in self.features:
                # Add the variable containing the errors
                feature.setAttribute(CSV_ERROR, self.directive_errors)
                self.pyoutput(feature)

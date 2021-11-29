LOOKUP_TABLES_READER_NG
=======================

Documentation du Custom Transformer FME
#######################################

Description 
· This custom Transformer allow the user to set a specified value for one or many attributes into a FME feature (attributes can be simple list i.e. with only one index). It can either overwrite the attribute value or set a specified value if the attribute is Null. The value can be set as text or as another attribute value from the same FME feature. In the case where the specified attribute is a list, the custom Transformer repairs it (it assures there is no missing index into the list). Attributes to process and actions to do are contained into input YAML directives. 
Input Ports 
· DATA_INPUT : A FME feature. 
Output Ports 
· OUTPUT : The FME feature for witch attributes have been modified according the YAML directives. 
Parameters 
· IN_YAML_TEXT: YAML directives to determine the attribute and the action to be done on the FME feature. See the section Content of the YAML directives below for a description of the YAML directives. 
Content of the YAML directives 
The YAML directives are used by the custom transformer to decide the attribute to process and the process itself. Below is an example of YAML directives. Notice that there is 6 attributes, each of them has 2 keywords values: action and attr2set . 
notes: 
    action: attribute_not_null 
    attr2set: title 
iso_topic{}.: 
    action: attribute_not_null 
    attr2set: default_iso_topic 
publisher: 
    action: text_overwrite 
    attr2set: NRCan 
description: 
    action: text_not_null 
    attr2set: Description PGF 
maintainer: 
    action: attribute_overwrite 
    attr2set: description 
tags{}.name: 
    action: attribute_not_null 
    attr2set: default_tags_display_name 
Description of the YAML directives 
The first part of the YAML is the name of the FME attribute on which we want to do an action, it can be a list with a specific attribute to access (e.g. iso_topic{}.topic_value ) or just a list (e.g. iso_topic{}. ). Note that if the FME feature being processed does not contain the specific attribute of the list you want to access, it will not be process. For example, if you want to do text_not_null on every feature for the list iso_topic {}.,you need to specify the specific attribute of the list (topic_value) so that all feature will be affected, even those not containing iso_topic{}.topic_value. 
When referring to a list, it is important to write it with the following 3 characters "{}.". It can also be a single attribute (e.g. description ). 
Following the FME attribute to process, there are 2 keywords: action and attr2set . The keyword action defines the action to do with the attribute it relates to, 4 options are available. The keyword attr2set , defines either the attribute name or a text literal depending of the action selected. If the action name contains attribute , then it sets the value of the specified attribute. If the action name contains text then it sets the text written. 
action : 
- attribute_not_null: This option verify if the attribute value is Null , if yes it sets the value of the attribute specified by the attr2set keyword. 
- attribute_overwrite: This option overwrite the attribute value by setting the value of the attribute specified by the attr2set keyword. 
- text_not_null: This option verify if the attribute value is Null , if yes it sets the text written into the attr2set keyword. 
- text_overwrite: This option overwrite the attribute value, it sets the text written into the attr2set keyword. 
attr2set: 
-attribute_not_null and attribute_overwrite: Sets the attribute value specified. 
- text_not_null and text_overwrite: Sets the literal text written. 
New attributes or list: 
If the list or the attribute written into the YAML does not exist, it will be created. Lists will be set with an index {0}. Note that attributes or lists are processed in the YAML from top to bottom. Therefore, you can use in lower attributes in the YAML, the attributes values that have been sets higher in the YAML.   
Documentation du code LOOKUP_TABLES_READER.py
#############################################
   
.. autosummary::
   LOOKUP_TABLES_READER_NG.check_file_present
   LOOKUP_TABLES_READER_NG.LoadValidateYaml
 
.. automodule:: LOOKUP_TABLES_READER_NG
   :members:
   :special-members: __init__
   :show-inheritance:
    

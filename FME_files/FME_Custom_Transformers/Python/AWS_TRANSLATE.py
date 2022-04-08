#
# Ce fichier contient le ccode python appelé le Custom Transformer AWS_TRANSLATE

import time
import fme
import fmeobjects
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass
    
try:
    import boto3
except:
    # No access to boto3
    pass

# FME attribute name
TRANSLATION_STATUS = '_translation_status'

# Constant
EN = "en"
FR = "fr"
ENGLISH_TO_FRENCH = "English-->French"
MAX_ITERATION = 5
SLEEP_TIME = 1
YES = "YES"

def aws_translate(aws_activation, inText, inlang, outlang):
    """This translates string using AWS translation service.
        
    Parameters
    ----------
    aws_activate : Boolean
        Flag to activate the AWS translation. True: Translate the attributes;
        False do not translate the strings
    inText: String
        String to translate
    inLang: String
        Language of the input string to translate. Can take 2 values: en or fr
    outLang: String
        Language of the translated string. Can take 2 values: en or fr
        
    Returns
    -------
    String
        Translated string
    
    """

    if inText == "":
        # Empty string nothing to translate
        result = ""
    else:
        if aws_activation:
            try:
                translate = boto3.client('translate', 'ca-central-1', use_ssl=True)
                result = translate.translate_text(Text=inText,SourceLanguageCode=inlang, TargetLanguageCode=outlang).get('TranslatedText')
                result = result.replace(' ', ' ')  # Replace the Non-breaking space which we replace by a space char to prevent loading problems in TBS portal
            except:
                logger = fmeobjects.FMELogFile()
                logger.logMessageString("Unable to access AWS translate", fmeobjects.FME_WARN)
                logger.logMessageString("String to translate: {}".format(inText), fmeobjects.FME_WARN)
                raise
        else:
            # AWS translation is not activated
            result = "Translation of " +  inText
        
    return result


def aws_guess_translation(att_value_in_lang):
    """
    """
    # Message à imprimer dans le log si on change la direction de la traduction pour un attribut
    print ("log: Correction de la traduction. Changement de la langue pour @Value(name) @Value(name_fr)")
    raise


def get_translation_direction(feature, aws_activation, att_name, translation_mode):
    """This method validates the direction of the translation.
        
    Parameters
    ----------
    feature : FmeFeature object
        Feature object to process
    aws_activate : Boolean
        Flag to activate the AWS translation. True: Translate the attributes;
        False do not translate the strings
    att_name : String
    translation_mode : String
        Flag to indicate the type of translation. Can take two values:
        English-->French for an English to French tranlation; French-->English for a French to English translation
        
    Returns
    -------
    Tuple
        Tuple of 2 strings. First string input language; second string output language.
        If both string are equal no translation is needed and the value is the value of
        the input language.
    
    """
    
    if translation_mode == ENGLISH_TO_FRENCH:
        in_lang = EN
        out_lang = FR
    else:
        in_lang = FR
        out_lang = EN
        
    att_value_in_lang = FME_utils.feature_get_attribute(feature, att_name)
    att_name_out_lang = att_name + "_" + out_lang
    att_value_out_lang = FME_utils.feature_get_attribute(feature, att_name_out_lang)
    
    if att_value_in_lang != "" and att_value_out_lang != "":
        if att_value_in_lang == att_value_out_lang:
            # Same text value... try to guess the language
            if aws_activation:
                in_lang, out_lang = aws_guess_translation(att_value_in_lang)
        else:
             # Text already translated nothing to translate
             out_lang = in_lang
            
    return in_lang, out_lang
    

def manage_translation(feature, lst_att_2_translate, aws_activation, translation_mode):
    """This method iterates a list of FME attributes to trasnlate.
        
    Parameters
    ----------
    feature : FmeFeature object
        Feature object to process
    lst_att_2_translate : List
        List of FME attributes to translate
    aws_activate : Boolean
        Flag to activate the AWS translation. True: Translate the attributes;
        False do not translate the strings
    translation_mode: String
        Flag to indicate the type of translation. Can take two values:
        English-->French for an English to French tranlation; French-->English for a French to English translation
        
    Returns
    -------
    Boolean
        True: The translation was successful; False the translation was in error
    
    """
    
#    web_pdb.set_trace()
    translation_done = True
    # Loop over each attribute name of the list
    for att_2_translate in lst_att_2_translate:
        lst_att_name_index = FME_utils.extract_attribute_list(feature, att_2_translate)
        for (index, att_to_translate) in lst_att_name_index:
            text_to_translate = feature.getAttribute(att_to_translate)
            if text_to_translate is None:
                # Attribute is missing nothing to translate
                pass
            else:
                try:
                    in_lang, out_lang =  get_translation_direction(feature, aws_activation, att_to_translate, 
                                                                   translation_mode)
                    if in_lang != out_lang:
                        text_translated = aws_translate(aws_activation, text_to_translate, in_lang, out_lang)
                        # Set the out language attribute
                        att_name_out_lang = att_to_translate + "_" + out_lang
                        feature.setAttribute(att_name_out_lang, text_translated)
                    else:
                        # String already translate. Nothing to do
                        pass
                    # Set a new in language attribute
                    att_name_in_lang = att_to_translate + "_" + in_lang
                    feature.setAttribute(att_name_in_lang, text_to_translate)
                except:
                    translation_done = False
                    break
        else:
            continue  # Go to next iteration of the outer loops
        
        # Something went wrong before; exit for..loop
        break 
    
    return translation_done
        
def process_feature(feature):
    """This method translate string using AWS translate tools.
    
    The FME attributes to translate are stored in the FME attribute: *_attr2translate*
    The FME list to translate are stored in the FME attribute: *_attr2translate*.
    The translation mode in contained in the attribute: _mode. If mode equals: English-->French
    An english to Frech is done if the value equals: French-->English a French to English 
    translation is done.
    The FME attribute _aws_activation contains the translation flag. If set to Yes the translation is done; 
    if set to No the translation is not done.
    
    Parameters
    ----------
    feature: FmeFeature object
        Feature object to process
        
    Returns
    -------
    None
    
    """
    
#    web_pdb.set_trace()
    # Extract some FME attributes
    att_names = feature.getAttribute('_attr2translate')
    list_names = feature.getAttribute('_attrlist2translate')
    aws_activation = FME_utils.test_attribute_value(feature, "_aws_activation", YES, False)
    translation_mode = feature.getAttribute('_mode')
    
    # Trasform CSV string into list
    att_names = att_names.replace(" ", "")  # Remove any whitespace in the string
    list_names = list_names.replace(" ", "")  # Remove any whitespace in the string
    att_2_translate = att_names + "," + list_names
    lst_att_2_translate = att_2_translate.split(",")  # Split names into a list of names
    
    # Manage special case if first element is empty
    if lst_att_2_translate[0] == "":
       del lst_att_2_translate[0]
       
    # Manage special case if last element is empty
    if lst_att_2_translate[-1] == "":
       del lst_att_2_translate[-1]
        
    translation_done = False
    logger = fmeobjects.FMELogFile()
    nbr_iteration = 0

    # Loop until translation done or maximum iteration reached
    while not translation_done and nbr_iteration < MAX_ITERATION:              
        translation_done = manage_translation (feature, lst_att_2_translate, aws_activation, 
                                               translation_mode)
        if not translation_done:
            # There was an error during translation wait and retry translation
            nbr_iteration += 1
            logger.logMessageString("Iteration: {} (AWS Problem)".format(nbr_iteration), fmeobjects.FME_INFORM)
            time.sleep(SLEEP_TIME)  # Sleep before next iteration
    
    if translation_done:
        # Translation was done correctly
        feature.setAttribute(TRANSLATION_STATUS, 0)
    else:
        # Translation was problematic
        logger.logMessageString("Unable to fully translate all the attributes", fmeobjects.FME_ERROR)
        feature.setAttribute(TRANSLATION_STATUS, 1)
    
    return

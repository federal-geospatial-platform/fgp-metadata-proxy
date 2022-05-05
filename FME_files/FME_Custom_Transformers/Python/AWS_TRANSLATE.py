#
# Ce fichier contient le ccode python appelé le Custom Transformer AWS_TRANSLATE
#
import time
import json
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
AWS_REGION = 'ca-central-1'
EN = "en"
FR = "fr"
ENGLISH_TO_FRENCH = "English-->French"
MAX_ITERATION = 5
SLEEP_TIME = 1
YES = "YES"

class AwsTranslationErr(Exception):
    """Exception error raised during AWS translation error"""
    pass

def aws_translate(aws_activation, inText, inlang, outlang):
    """This translates string using AWS translation service.
        
    Parameters
    ----------
    aws_activation : Boolean
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
        
    Raises
    ------
    AwsTranlationError
        When the AWS translation fails
    
    """

    if inText == "":
        # Empty string nothing to translate
        result = ""
    else:
        if aws_activation:
            try:
                translate = boto3.client('translate', AWS_REGION, use_ssl=True)
                result = translate.translate_text(Text=inText,SourceLanguageCode=inlang, TargetLanguageCode=outlang).get('TranslatedText')
                result = result.replace(' ', ' ')  # Replace the Non-breaking space which we replace by a space char to prevent loading problems in TBS portal
            except:
                logger = fmeobjects.FMELogFile()
                logger.logMessageString("Unable to access AWS translate", fmeobjects.FME_WARN)
                logger.logMessageString("String to translate: {}".format(inText), fmeobjects.FME_WARN)
                raise AwsTranslationErr
        else:
            # AWS translation is not activated
            result = "Translation of " +  inText
        
    return result


def aws_guess_translation(aws_activation, text_to_guess, in_lang, out_lang):
    """This method guesses using AWS translate tools which language the text is.
    
    Note: Result is always either: "fr" or "en"
    
    Parameters
    ----------
    aws_activation : Boolean
        Flag to activate the AWS translation. True: Translate the attributes;
        False do not translate the strings
    att_name_in_lang : String
        Name of the attribute to translate
    text_to_guess : String
        Text used to guess the language
    in_lang : String
        Requested input language
    out_lang : String
        Requested output language
        
    Returns
    -------
    Tuple
        Tuple of 2 strings. First string input language; second string output language as
        guessed by AWS translate tools.
    """
    
    # Set initial scores
    score_en = 0.0
    score_fr = 0.0

    if aws_activation:
        try:
            # Request language guessing
            comprehend = boto3.client(service_name='comprehend', region_name=AWS_REGION)
            json_response = comprehend.detect_dominant_language(Text = text_to_guess)
            
            # Loop over the guessed languages
            languages = json_response.get("Languages")
            if languages is not None:
                for language in languages:
                    code = language.get("LanguageCode")
                    score = language.get("Score")
                    if code == EN:
                        score_en = score
                    if code == FR:
                        score_fr = score
            else:
                # No language was guessed
                pass
        except:
            # There was a problem during language guessing...
            raise AwsTranslationErr
    else:
        # AWS langugage guessing is not activated
        logger = fmeobjects.FMELogFile()
        text_log = 'AWS is not activated. Cannot guess the language of the string "{0}"'.format(text_to_guess)
        logger.logMessageString(text_log, fmeobjects.FME_WARN)
        
    # Identifiy the language with the most probability
    if score_en > score_fr:
        in_out_lang = (EN, FR)  # English to French translation
    elif score_fr > score_en:
        in_out_lang = (FR, EN)  # French to English translation
    else:
        in_out_lang = (in_lang, out_lang)  # Even probability.  Take original translation direction
        
    return in_out_lang

def translate_attribute(feature, aws_activation, att_name, translation_mode):
    """This method translates the attribute text value.
        
    Parameters
    ----------
    feature : FmeFeature object
        Feature object to process
    aws_activate : Boolean
        Flag to activate the AWS translation. True: Translate the attributes;
        False do not translate the strings
    att_name : String
        Attribute name to translate
    translation_mode : String
        Flag to indicate the type of translation. Can take two values:
        English-->French for an English to French tranlation; French-->English for a French to English translation
    
    Returns
    -------
    None
    
    """
    
    if translation_mode == ENGLISH_TO_FRENCH:
        in_lang = EN
        out_lang = FR
    else:
        in_lang = FR
        out_lang = EN
        
    logger = fmeobjects.FMELogFile()
    id = FME_utils.feature_get_attribute(feature, "id")

    att_name_in_lang = att_name + "_" + in_lang
    att_value_in_lang = FME_utils.feature_get_attribute(feature, att_name_in_lang)
    att_name_out_lang = att_name + "_" + out_lang
    att_value_out_lang = FME_utils.feature_get_attribute(feature, att_name_out_lang)

    if att_value_out_lang == "":
        # The output attribute is empty
        # Translate the text
        att_value_out_lang = aws_translate(aws_activation, att_value_in_lang, in_lang, out_lang)
        if att_value_in_lang == att_value_out_lang:
            # The text to translate and the translated text are the same.  Translation direction is reversed
            log_text = 'ID: {0} - {1} ==> {2} translation of "{3}" returns same text. Attribute name: "{4}" ' + \
                       'Translation is reversed {5} ==> {6}.'
            log_text = log_text.format(id, in_lang.upper(), out_lang.upper(), att_value_in_lang, 
                                       att_name_in_lang, out_lang.upper(), in_lang.upper())
            logger.logMessageString(log_text, fmeobjects.FME_WARN)
            # Reverse the translation direction 
            att_value_out_lang = aws_translate(aws_activation, att_value_in_lang, out_lang, in_lang)
            # Reverse the output in_lang and out_lang attribute
            feature.setAttribute(att_name_in_lang, att_value_out_lang)
            feature.setAttribute(att_name_out_lang, att_value_in_lang)
        else:
            # Write the translation 
            feature.setAttribute(att_name_out_lang, att_value_out_lang)
    elif att_value_in_lang != att_value_out_lang:
        # Value are different. Attribute text value already translated nothing to do
        pass
    elif att_value_in_lang == att_value_out_lang:
        # Attribute value EN and FR are the same... try to guess the language and translate after
        in_lang, out_lang = aws_guess_translation(aws_activation, att_value_in_lang,
                                                  in_lang, out_lang)
        log_text = 'ID: {0} - Original attribute value of "{1}" and "{2}" are the same. ' + \
                   'AWS language guessing is now proposing: {3} ==> {4}'
        log_text = log_text.format(id, att_name_in_lang, att_name_out_lang, in_lang, out_lang)
        logger.logMessageString(log_text, fmeobjects.FME_WARN)
        # Reverse in and out attribute name
        att_name_in_lang, att_name_out_lang = att_name_out_lang, att_name_in_lang
        att_value_out_lang = aws_translate(aws_activation, att_value_in_lang, in_lang, out_lang)
        feature.setAttribute(att_name_out_lang, att_value_out_lang)   
                
    return
    
def set_en_fr_attributes(feature, att_name_to_translate, text_to_translate, translation_mode):
    """Set the attribute suffix of the attribute to translate depending on the translation direction.
    
    If the translation direction is en ==> fr, the suffix "_en" is added to the attribute to translate.
    If the translation direction is fr ==> en, the suffix "_fr" is added to the attribute to translate.
    If the attribute (including the suffix) to create exists and their attribute values are different then 
    it's problematic and the attribute value with the suffix is replaced by the original attribute name 
    to translate.
    
    Parameters
    ----------
    feature : FmeFeature object
        Feature object to process
    att_name_to_translate : String
        Name of the attribute to translate
    text_to_translate: String
        Text string to translate
    translation_mode : String
        Flag to indicate the type of translation. Can take two values:
        English-->French for an English to French tranlation; French-->English for a French to English translation
    """
    
#    web_pdb.set_trace()
    if translation_mode == ENGLISH_TO_FRENCH:
        in_lang_att_name = att_name_to_translate + "_" + EN
    else:
        in_lang_att_name = att_name_to_translate + "_" + FR
        
    in_lang_att_value = feature.getAttribute(in_lang_att_name)
    if in_lang_att_value is None or in_lang_att_value == "":
        # Replace no attribute with attribute to translate
        feature.setAttribute(in_lang_att_name, text_to_translate)
    else:
        if in_lang_att_value != text_to_translate:
            # Resolving discrepency between attribute to translate and destination attribute
            id = FME_utils.feature_get_attribute(feature, "id")
            log_text = 'ID: {0} - Attribute: "{1}" and "{2}" should have same content. "{3}" attribute will be used'
            log_text = log_text.format(id, att_name_to_translate, in_lang_att_name, att_name_to_translate)
            logger = fmeobjects.FMELogFile()
            logger.logMessageString(log_text, fmeobjects.FME_WARN)
            # Overwrite the attribute with the original value
            feature.setAttribute(in_lang_att_name, text_to_translate)
        else:
            # Both attribute value are the same.  Nothing to do
            pass

    return

def manage_translation(feature, lst_att_2_translate, aws_activation, translation_mode):
    """This method iterates the list of FME attributes to translate.
        
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
        for (index, att_name_to_translate) in lst_att_name_index:
            text_to_translate = feature.getAttribute(att_name_to_translate)
            if text_to_translate is None:
                # Attribute is missing nothing to translate
                pass
            else:
                try:
                    pass
                    set_en_fr_attributes(feature, att_name_to_translate, text_to_translate, translation_mode)
                    translate_attribute(feature, aws_activation, att_name_to_translate, translation_mode)
                except AwsTranslationErr:
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
    The FME list to translate are stored in the FME attribute: *_attrlist2translate*.
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

import fme
import fmeobjects
from lxml import etree
import json

# Template Function interface
def processFeature(feature):
    pass

# Template Class Interface
class FeatureProcessor(object):
    
    def __init__(self):
        self.namespaces = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "srv": "http://www.isotc211.org/2005/srv",
            "gco": "http://www.isotc211.org/2005/gco",
            "gmx": "http://www.isotc211.org/2005/gmx",
            "xlink": "http://www.w3.org/1999/xlink",
            "gts": "http://www.isotc211.org/2005/gts",
            "gfc": "http://www.isotc211.org/2005/gfc",
            "gmi": "http://www.isotc211.org/2005/gmi",
            "gsr": "http://www.isotc211.org/2005/gsr",
            "gss": "http://www.isotc211.org/2005/gss",
            "gml": "http://www.opengis.net/gml/3.2",
            "geonet": "http://www.fao.org/geonetwork",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "err": "http://www.w3.org/2005/xqt-errors"
        }

    def adjust_xpath_based_on_language(self, language_code, xpath):
        if language_code not in ["eng", "fra"]:
            raise ValueError(f"Invalid language code in the XML (gmd:language): {language_code}")
        
        if language_code == "eng":
            english_xpath = f"{xpath}/gco:CharacterString/text()"
            french_xpath = f"{xpath}/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']/text()"
        else:
            english_xpath = f"{xpath}/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#eng']/text()"
            french_xpath = f"{xpath}/gco:CharacterString/text()"
        
        return english_xpath, french_xpath

    def handle_xpath(self, root, xpath, namespaces):
        try:
            result = root.xpath(xpath, namespaces=namespaces)
            if not result:
                raise ValueError(f"No match found for XPath: {xpath}")
            return result
        except etree.XPathError as e:
            raise ValueError(f"XPath error: {str(e)}")           

    def extract_transfer_options(self, root, transfer_options_xpath, namespaces, language_code):
        """
        Extract specific fields from transferOptions in an XML document.
        
        :param root: The root of the XML document.
        :param transfer_options_xpath: The XPath expression to locate transferOptions elements.
        :param namespaces: The namespace mapping for XPath.
        :param language_code: The language code ('eng' or 'fra') to determine the default language.
        :return: A list of dictionaries containing the extracted fields.
        """
        
        try:
            # Find all transferOptions elements based on the provided XPath
            transfer_options_elements = root.xpath(transfer_options_xpath, namespaces=namespaces)
        except etree.XPathError as e:
            raise ValueError(f"XPath error in transfer options extraction: {str(e)}")
        
        # Initialize a list to store the results
        result = []
        
        # Loop over each transferOptions element
        for transfer_option in transfer_options_elements:
            # Initialize a dictionary to store the extracted fields for the current transferOptions
            transfer_option_data = {
                'url': None,
                'name_translated_en': None,
                'name_translated_fr': None,
                'language_en': None,
                'resource_type_en': None,
                'format_en': None,
                'language_fr': None,
                'resource_type_fr': None,
                'format_fr': None
            }
            
            # Extract the URL
            try:
                url_element = transfer_option.xpath('.//gmd:CI_OnlineResource/gmd:linkage/gmd:URL', namespaces=namespaces)
                if url_element:
                    transfer_option_data['url'] = url_element[0].text
            except IndexError as e:
                IndexError(f"Warning: URL element missing in transferOptions. {str(e)}")
            
            try:            
                # Extract the translated names based on language
                english_xpath, french_xpath = self.adjust_xpath_based_on_language(language_code, './/gmd:CI_OnlineResource/gmd:name')
                
                name_translated_en_element = transfer_option.xpath(english_xpath, namespaces=namespaces)
                name_translated_fr_element = transfer_option.xpath(french_xpath, namespaces=namespaces)
                
                if name_translated_en_element:
                    transfer_option_data['name_translated_en'] = name_translated_en_element[0]
                
                if name_translated_fr_element:
                    transfer_option_data['name_translated_fr'] = name_translated_fr_element[0]
                
            except Exception as e:
                ValueError(f"Error extracting translated names based on language: {str(e)}")

            
            # Extract the resource type and format
            #description_element = transfer_option.xpath('.//gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString', namespaces=namespaces)
            try:
                english_description_element, french_description_element = self.adjust_xpath_based_on_language(language_code, './/gmd:CI_OnlineResource/gmd:description')
                
                if english_description_element:
                    english_description_element = transfer_option.xpath(english_description_element, namespaces=namespaces)[0]
                    parts = english_description_element.split(';')
                    if len(parts) >= 2:
                        transfer_option_data['resource_type_en'] = parts[0]
                        transfer_option_data['format_en'] = parts[1]
                        transfer_option_data['language_en'] = parts[2]
                if french_description_element:
                    french_description_element = transfer_option.xpath(french_description_element, namespaces=namespaces)[0]
                    parts = french_description_element.split(';')
                    if len(parts) >= 2:
                        transfer_option_data['resource_type_fr'] = parts[0]
                        transfer_option_data['format_fr'] = parts[1]
                        transfer_option_data['language_fr'] = parts[2]            
            except Exception as e:
                ValueError(f"Error extracting resource type or format: {str(e)}")
            
            # Append the collected data to the result list
            result.append(transfer_option_data)
        
        return result

    def input(self, feature):
        errors = []

        try:
            # Define your XML document as a string
            xml_string = feature.getAttribute("HNAP_MD")
            if not xml_string:
                raise ValueError("Problème de lecture de l'attribut HNAP_MD")
            
            # Remove the XML declaration from the XML string
            xml_string_no_declaration = xml_string.split("\n", 1)[1] if "\n" in xml_string else xml_string
            # Parse the XML string without the declaration
            root = etree.fromstring(xml_string_no_declaration)
            
            # Extract language code
            language_codes = root.xpath("/gmd:MD_Metadata/gmd:language/gco:CharacterString/text()", namespaces=self.namespaces)
            if not language_codes:
                raise ValueError("Missing language code in the XML")
            language_code = language_codes[0].split(";")[0]
            
            # Validate the language code
            if language_code not in ["eng", "fra"]:
                raise ValueError(f"Invalid language code: {language_code}. Must be 'eng' or 'fra'.")

            attributes = zip(
                feature.getAttribute('item{}.AttributeName'), 
                feature.getAttribute('item{}.AttributesNb'), 
                feature.getAttribute('item{}.Bilingue'), 
                feature.getAttribute('item{}.Xpath'),
                feature.getAttribute('item{}.NestedPath')
            )
            
            lists, singles, duals, nested, lists_singles, resources = [], [], [], [], [], []
            
            
            for name, count, bilingual, xpath, nestedpath in attributes:
                # Validate count
                if count not in ['Simple', 'Liste', 'Resources']:
                    errors.append(f"Invalid value for count for attribute '{name}': {count}")
                # Validate bilingual
                if bilingual not in ['Yes', 'No']:
                    errors.append(f"Invalid value for bilingual for attribute '{name}': {bilingual}")
                # Validate name
                if not isinstance(name, str):
                    errors.append(f"Attribute name must be a string for attribute '{name}'")
                
                if not nestedpath and count == 'Liste':
                    (lists if bilingual == 'Yes' else lists_singles).append((name, xpath))
                elif not nestedpath and count == 'Simple':
                    (duals if bilingual == 'Yes' else singles).append((name, xpath))
                elif not nestedpath and count == 'Resources':
                    resources.append((name, xpath))
                elif nestedpath:
                    nested.append((name, xpath, nestedpath))
            
            
            for name, xpath in singles:
                try:
                    value_single = self.handle_xpath(root, xpath, self.namespaces)
                    feature.setAttribute(name, value_single[0])
                except ValueError as e:
                    errors.append(f"{name}: {str(e)}")

            for name, xpath in duals:
                try:
                    english_xpath, french_xpath = self.adjust_xpath_based_on_language(language_code, xpath)
                    english_values = self.handle_xpath(root, english_xpath, self.namespaces)
                    french_values = self.handle_xpath(root, french_xpath, self.namespaces)
                    feature.setAttribute(f"{name}_en", english_values[0])
                    feature.setAttribute(f"{name}_fr", french_values[0])
                except ValueError as e:
                    errors.append(f"{name}: {str(e)}")

            for name, xpath in lists:
                try:
                    english_xpath, french_xpath = self.adjust_xpath_based_on_language(language_code, xpath)
                    english_values = self.handle_xpath(root, english_xpath, self.namespaces)
                    french_values = self.handle_xpath(root, french_xpath, self.namespaces)
                    feature.setAttribute(f"{name}_en", english_values)
                    feature.setAttribute(f"{name}_fr", french_values)
                except ValueError as e:
                    errors.append(f"{name}: {str(e)}")

                    
            for name, xpath, nestedpath in nested:
                nested_values = []
                nestedpath = nestedpath.strip('[]')
                try:
                    value_1 = self.handle_xpath(root, xpath, self.namespaces)
                    for path in [elem.strip() for elem in nestedpath.split(',')]:
                        nested_values.append(self.handle_xpath(root, path, self.namespaces))
                    #merged_list = [a + ";" + b for a, b in zip(value_1, nested_values)]
                    nested_values.append(value_1)
                    feature.setAttribute(name, [', '.join(item) for item in zip(*nested_values)])
                except ValueError as e:
                    errors.append(f"{name}: {str(e)}")

            for name, xpath in lists_singles:
                try:
                    value_single = self.handle_xpath(root, xpath, self.namespaces)
                    feature.setAttribute(name, value_single)
                except ValueError as e:
                    errors.append(f"{name}: {str(e)}")
                    
            for name, xpath in resources:
                try:
                    valeurs_resources = self.extract_transfer_options(root, xpath, self.namespaces, language_code)
                            
                    for index, elem in enumerate(valeurs_resources):
                        _index = str(index)
                        for key, value in elem.items():
                            feature.setAttribute(f"resources{{" + _index + f"}}.{key}", f"{value}")
                  
                except ValueError as e:
                    # Handle other ValueErrors
                    errors.append(f"{name}: {str(e)}")

            # Set the attribute with all collected errors at the end
            if errors:
                feature.setAttribute("xpath_errors", errors)

        except (etree.XMLSyntaxError, ValueError) as e:
            feature.setAttribute("parsing_error", f"Parsing error: {str(e)} \n")
        
        self.pyoutput(feature)

    def close(self):
        pass

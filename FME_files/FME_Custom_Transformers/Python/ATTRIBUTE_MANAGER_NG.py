import fme
import fmeobjects
import yaml
from Python.FME_utils import FME_utils


#Définissons les constantes qui constituent l'ensemble des actions possibles.
ATTR_NOT_NULL = 'attribute_not_null'
ATTR_OVERWRITE = 'attribute_overwrite'
TXT_NOT_NULL = 'text_not_null'
TXT_OVERWRITE = 'text_overwrite'
#Définissons le séparateur à utiliser pour identifier une liste dans notre YAML
LIST_SEPARATOR_IDENTIFIER = '{}.' #À utiliser pour identifier la liste dans notre YAML
REPLACEMENT_LIST_SEPARATOR = '{0}.' #À utiliser pour créer au moins un élément dans une liste qui n'existe pas
LIST_SEPARATOR_BRACKET = '{}' #À utiliser pour combiner avec le nom d'un attribut pour l'identifier comme liste


# List des actions
LST_ACTION = [ATTR_NOT_NULL, ATTR_OVERWRITE, TXT_NOT_NULL, TXT_OVERWRITE]

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class AttributeManagerNG(object):
    """This class is used by the ATTRIBUTE_MANAGER_NG custom transformer in a PythonCaller in order to
    to manage attribute values. It can overwrite any attribute (including list) or set a specific attribute value for null attributes.
    This class is reading YAML directives received as input from the costum transformer.
    
    Notes
    -----
    Python modules:
        - yaml
        - FME_utils
    """

    def __init__(self):
        """Constructor call before any FME features are passed
        """
    
        self.mapping = {}
   
    def input(self, feature):
        """Process each FME features. Actions to be done on attributes are specified into the costum transformer YAML directives.
        More informations are available into the ATTRIBUTE_MANAGER_NG costum transformer.
        
        Example, the following actions can be done on attributes:
        
        -attribute_not_null
        -attribute_overwrite
        -text_not_null
        -text_overwrite
        
        Parameters
        ----------
        feature: FME feature
            FME feature to process
        
        Returns
        -------
        feature: FME feature
            FME feature who's attributes have been processed according to the yaml directives.
        
        """
        
        #Vérification de la valeur de l'attribut _ordre = 1 afin de lire le YAML
        if feature.getAttribute('_order') == 1:
            self.mapping = FME_utils.load_yaml_document(feature.getAttribute('in_yaml'))
            for key in self.mapping.keys():
                try:
                    #Validation des actions
                    temp_action = self.mapping[key]['action']
                    
                    if temp_action not in LST_ACTION:
                        raise ValueError("L'action choisie doit être parmis les 4 choix")
                    #Validation de attr2set 
                    temp_attr2set = self.mapping[key]['attr2set']
                    if temp_attr2set is not None:
                        #Tout est beau
                        pass
                        
                    else:
                        raise ValueError("Vérifier que le YAML est bien structuré")
                 
                except:
                    raise
            pass
        
        #Vérification de la valeur de l'attribut _ordre = 2 afin de process le YAML
        if feature.getAttribute('_order') == 2:
            for key in self.mapping.keys():

                #Définissons une switch pour la variable replace_key:
                replace_key_switch = False
                              
                #Établissons quels attributs de notre YAML sont des listes en vérifiant le séparateur LIST_SEPARATOR_IDENTIFIER
                sep = key.split(LIST_SEPARATOR_IDENTIFIER)
                if len(sep) > 1:
                    if len(sep[1]):
                        #default_att_name devient la valeur de l'élément de la liste à forcer 
                        default_att_name = [sep[1]]
                    else:
                        #Définissons la variable default_att_name à None
                        default_att_name = None
                        pass
                    #Réparation de la liste pour l'attribut en spécifié
                    FME_utils.repair_attribute_list(feature, sep[0] + LIST_SEPARATOR_BRACKET, default_att_name)
                else:
                    pass
                    
                #Si on confirme que c'est une liste en vérifiant le patron suivant --> LIST_SEPARATOR_IDENTIFIER et qu'elle n'existe pas dans le feature alors on ajoute l'index 0 à la liste pour créer l'attribut
                if feature.getAttribute(key) is None and key.find(LIST_SEPARATOR_IDENTIFIER) != -1:
                    replace_key = key.replace(LIST_SEPARATOR_IDENTIFIER, REPLACEMENT_LIST_SEPARATOR)
                    replace_key_switch = True
                else:
                    pass  

                #Extraction du l'action
                action = self.mapping[key]['action']
                #Extraction de l'attribut
                attr = self.mapping[key]['attr2set']
                
                #Ajustons le dictionnaire d'attribut pour lui faire considérer les listes
                extr_att_list = FME_utils.extract_attribute_list(feature, key)

                #Gérons une liste non présente dans le feature pour lui créer l'indice .{0}
                if not replace_key_switch:
                    #Création d'un dictionaire d'attribut
                    dict_attr = {key: self.mapping[key]['attr2set']}
                elif replace_key_switch:
                    #Création d'un dictionaire d'attribut avec la nouvelle clée qui est une liste d'indice 0 --> {0}.
                    dict_attr = {replace_key: self.mapping[key]['attr2set']}
                    key = replace_key
                
                #Initialisation dictionnaire vide pour y inclure les listes d'attributs
                dict_attr_updated = {}
                
                #Validation de l'attribut
                if not extr_att_list:
                    #  L'attribut n'existe pas
                    dict_attr_updated = dict_attr
                    pass
                    
                elif len(extr_att_list) == 1:
                    #L'attribut n'est pas une liste
                    dict_attr_updated = dict_attr
                    pass
                
                else :
                    #On a une liste de tuple alors on boucle dedans
                    for elem in extr_att_list:
                        dict_attr_updated.update({elem[1]: dict_attr[key]})
                        
                #Validation de l'action NOT_NULL
                if action == ATTR_NOT_NULL or action == TXT_NOT_NULL:
                    #On boucle dans notre dictionnaire ajusté
                    for attr in dict_attr_updated.keys():
                        #Vérification que l'attribut n'existe pas (important pour les listes d'attribut)
                        if not feature.getAttribute(attr):
                            #On met une valeur associée à un attribut déjà existant
                            if action == ATTR_NOT_NULL:
                                feature.setAttribute(attr, feature.getAttribute(dict_attr_updated[attr]))
                            #On met une valeur texte
                            if action == TXT_NOT_NULL:
                                feature.setAttribute(attr, dict_attr_updated[attr])                           
                
                
                #Validation de l'action OVERWRITE
                if action == ATTR_OVERWRITE or action == TXT_OVERWRITE:
                    #On boucle dans notre dictionnaire ajusté
                    for attr in dict_attr_updated.keys():
                        #On met une valeur associée à un attribut déjà existant
                        if action == ATTR_OVERWRITE:   
                            feature.setAttribute(attr, feature.getAttribute(dict_attr_updated[attr]))
                        #On met une valeur texte
                        if action == TXT_OVERWRITE:
                            feature.setAttribute(attr, dict_attr_updated[attr])  
        
            self.pyoutput(feature)
        
        #Si l'attribut _ordre n'a pas de valeur ou n'est pas présent, alors on ne fait rien    
        else:
            pass
            
    def close(self):
        """Method call when all the festures are passed, not used.
        """
        
        pass
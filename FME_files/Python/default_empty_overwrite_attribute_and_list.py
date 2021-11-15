import fme
import fmeobjects
import yaml
from FME_utils import *


#Définissons les constantes qui constituent l'ensemble des actions possibles.
ATTR_NOT_NULL = 'attribute_not_null'
ATTR_OVERWRITE = 'attribute_overwrite'
TXT_NOT_NULL = 'text_not_null'
TXT_OVERWRITE = 'text_overwrite'

# List des actions
LST_ACTION = [ATTR_NOT_NULL, ATTR_OVERWRITE, TXT_NOT_NULL, TXT_OVERWRITE]

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class FeatureProcessor(object):

    def __init__(self):
    
        self.mapping = {}
   
    def input(self, feature):
        #Vérification de la valeur de l'attribut _ordre = 1 afin de lire le YAML
        if feature.getAttribute('_order') == 1:
            self.mapping = load_yaml_document(feature.getAttribute('in_yaml'))
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

                #Définissons un switch pour la variable replace_key:
                replace_key_switch = False
                              
                #Établissons quels attributs de notre YAML sont des listes en vérifiant le séparateur '{}.'
                sep = key.split('{}.')
                if len(sep) > 1:                  
                    #Réparation de la liste pour l'attribut en spécifié
                    repaired_list = repair_attribute_list(feature, sep[0])
                else:
                    pass
                    
                #Si on confirme que c'est une liste en vérifiant le patron suivant --> {}. et qu'elle n'existe pas dans le feature alors on ajoute l'index 0 à la liste pour créer l'attribut
                if feature.getAttribute(key) is None and key.find('{}.') != -1:
                    replace_key = key.replace('{}.', '{0}.')
                    replace_key_switch = True
                else:
                    pass  

                #Extraction du l'action
                action = self.mapping[key]['action']
                #Extraction de l'attribut
                attr = self.mapping[key]['attr2set']
                
                #Ajustons le dictionnaire d'attribut pour lui faire considérer les listes
                extr_att_list = extract_attribute_list(feature, key)

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
        pass
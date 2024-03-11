#from Python.METADATA_DELTA_FINDER_GEN import FeatureProcessor
import fme
import fmeobjects
import yaml
from Python.FME_utils import FME_utils
import hashlib
import re
import json

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

 
class FeatureProcessor(object):


    def __init__(self):
    
        self.mapping = {}   #dictionnary containing the yaml content new and ref attributes to compare and their corresponding attribute names
        self.DictFeatureNew={}
        self.DictFeatureRef={}

    def input(self, feature):
        
        #Chargement du fichier yaml en config. Si non chargé
        if not self.mapping:
            self.mapping = FME_utils.load_yaml_document(open(feature.getAttribute('_yaml_file'), "r").read())
            
            if 'id' not in self.mapping.keys():
                #C'est une erreur
                feature.setAttribute('error',r"Il n'y a pas d'ID de défini dans le yaml")
                self.pyoutput(feature)
        
        #Extraction du type de source (new ou ref)
        source_type=feature.getAttribute('_source')
        
        #Création des dictionnaires dans lesquels ont va ajouter  les valeurs hashées et brute pour la comparaison
        feature_dict_hash={}
        feature_dict_value={}
        
        #Parcourir le yaml pour créer les hash
        for keys in self.mapping.keys():
         try: 
            
            #Extraction du nom générique de l'attribut servant à décrire ce qu'on comparre 
            nom_eva=self.mapping[keys]['attr_name']
            
            
            #Extraction du nom de l'attribut en fonction de la référence/nouveau
            if source_type=='ref':
                nom_att=self.mapping[keys]['attr_ref']
            else:
                nom_att=self.mapping[keys]['attr_new']
            
           
            # Si un | est présent dans le nom de l'attribut (uniquement dans du new), cela
            # veut dire qu'on doit concatener N attributs pour avoir la même valeur que dans la référence.
            if '|' in nom_att:
                #Extraire le séparateur utilisé pour concatener
                sep=self.mapping[keys]['separator']
                
                #Vérifier si on concatène des attributs réguliers ou des listes
                #Lorsque c'est une liste, chaque élément de la concaténation doit être une liste
                #et toute les listes doivent être de la même longueur.
                if '{}' in nom_att:
                    
                    #Gestion des attributs selon les listes
                    #Création d'un dictionnaire pour stoker chaque liste
                    dict_cont_list={}
                    
                    #Variable conservant la longueur de la/les listes
                    global_len=0
                    
                    
                    index=0
                    #Créer un dictionnaire avec les listes de valeurs pour chaque atts
                    for atts in nom_att.split('|'):
                        #Vérifier que chaque sous-item est une liste
                        if '{}' not in atts:
                            
                            feature.setAttribute('error',r"On ne peut concatener une liste  avec des attributs réguliers. L'attribut %s du yaml est en erreur"%(nom_eva))
                            self.pyoutput(feature) 
                            
                        else:
                            #Extraire la longueur de chaque liste et vérifier qu'elle est la même pour chaque liste
                            if global_len==0:
                                global_len=len(feature.getAttribute(atts))
                            elif global_len != len(feature.getAttribute(atts)):
                                    feature.setAttribute('error',r"Les listes concaténées doivent être de même longueur.L'attribut %s du yaml est en erreur"%(nom_eva))
                                    self.pyoutput(feature) 
                                    
                            
                            
                            dict_cont_list[index]=feature.getAttribute(atts)
                            #Incrémenter le compteur
                            index+=1
                   
                    #Définir la variable Value (liste) dans laquel on viendra storer le résultat de la concaténation de chaque item du dictionnaire, groupé par position de liste similaire
                    # E.G. ('A1,B1,C1')('A2,B2,C2')....
                    value=[]
                    
                    # Boucler pour chaque index de liste
                    for i in range(global_len):
                        temp=''
                        #Concaténer pour chaque dans l'ordre 1,2,3....
                        
                            
                        for keys in list(dict_cont_list.keys()):
                            if temp:
                                temp='%s%s%s'%(temp,sep,dict_cont_list[keys][i])
                            else:
                                temp=dict_cont_list[keys][i]
                        
                        value.append(temp)
                      
                
                #Lorsqu'il n'y a pas de liste dans la concaténation
                else:
                
                    value=''
                    #Parcourir chaque attribut, extraction de la valeur et concaténation avec l'espaceur choisi
                    for atts in nom_att.split('|'):
                                       
                        temp=feature.getAttribute(atts)
                        if value:
                            value='%s%s%s'%(value,sep,temp)
                        else:
                            value=temp
                            
             
            #À voir si on peut remplacer.           
            #value=value.replace('<space>',' ')
            
            
            
            else:
                value=feature.getAttribute(nom_att)
            
            
            

            #Définition de la variable id si l'attribut validé à l'ID
            if nom_eva=='id':
                id=value
            
            #Si absence de valeur, on défini value à une constante
            if value:
                pass
            else:
                value='METADATA_DELTA_FINDER_NO_VALUE'

            #Si c'est une liste, on concatène le tout sans espaceur.
            if isinstance(value, list):

                
                listToStr = ''.join([str(elem) for i,elem in enumerate(value)])
                
                value=listToStr
            
                      
            
            
            #Création d'une Hashing key à partir de la valeur extraite            
            value_hash=hashlib.sha256(value.encode('utf-8')).hexdigest()
            
                
            #Stockage de la valeur brute et de la clé de hashage pour attribut comparé dans les dictionnaires respectifs
            #Dictionnaire de hashage
            feature_dict_hash[nom_eva]=value_hash
            #Dictionnaire de valeur brute
            feature_dict_value[nom_eva]=value
         except:
             feature.setAttribute('error',r"Erreur de création de la clé.L'attribut %s du yaml est en erreur. L'erreur est survenue sur l'entité %s" %(nom_eva,str(feature.getAttribute('id'))))
             self.pyoutput(feature) 
        #Transfère en attribut des dictionnaires (hash et brute) sur la feature pour utilisation dans le close
        feature.setAttribute('feature_dict_hash',str(feature_dict_hash))
        feature.setAttribute('feature_dict_value',str(feature_dict_value))
        
        
        #Transfère des features dans les dictionnaires de feature (new ou ref), la clé étant l'identifiant
        if source_type=='ref':
            self.DictFeatureRef[id]=feature
        else:
            self.DictFeatureNew[id]=feature
  
        
        
        
    def close(self):
         
            
            
            
        #Parcourir le dictionnaires des nouvelles métadonnées pour identifier les insert / update(ou no change) 
        #en comparant les clés du dictionnaire des nouvelles features avec celles de référence. Si la clé new n'est pas dans 
        #dans le dictionnaire de référence, c'est un INSERT. Quand on a un match de clés, on doit comparer le contenu pour identifier 
        #si c'est un no change ou un update.
        for nf_keys in self.DictFeatureNew.keys():
            
            #Extraction de la feature (new)  contenue dans le dictionnaire des nouvelles métadonnées
            feature_new=self.DictFeatureNew[nf_keys]
            
            
            #Déterminer si l'identifiant (la feature) existe dans la métadonnées référence
            if nf_keys in self.DictFeatureRef.keys():
                
                # On a un match entre le new et le ref. On doit comparer les clés de hashage pour déterminé Update/No Chant
                
                feature_ref=self.DictFeatureRef[nf_keys]
                
                #Extraction de la clé de hashage de la nouvelle feature
                hash_detail_new=feature_new.getAttribute('feature_dict_hash')
                #Extraction de la clé de hashage de la feature de référence
                hash_detail_ref=feature_ref.getAttribute('feature_dict_hash')
                
                
                if hash_detail_new != hash_detail_ref:
                    #Les clés de hashahge sont différentes, on est en mode Update
                    
                    #Supprimer l'attribut contenant le clé de hashage sur la nouvelle feature. Attribut non utile 
                    #à cette étape du traitement 
                    feature_new.removeAttribute('feature_dict_hash')
                    #Définition du PyCSW Transaction à update
                    feature_new.setAttribute('PyCSW_Transaction','Update')
                    
                    #Comparer en détail les clés de hashage pour identifier les différences
                    new = set(eval(hash_detail_new).items())
                    ref = set(eval(hash_detail_ref).items())
                    diff_hash=new ^ ref
      
                    #Extraction les dictionnaires de valeurs brutes pour identifier les valeurs d'origine pour chaque keys
                    dict_value_new=eval(feature_new.getAttribute('feature_dict_value'))
                    dict_value_ref=eval(feature_ref.getAttribute('feature_dict_value'))
                
                    
                    #Parcourrir la listes de différence et extraire les valeurs new et ref correspondant aux attributs 
                    
                    #Liste servant à stoker les différences
                    att_diff={}
                    for items in diff_hash:
                        
                        #uniquement si l'item n'est pas dans le dictionnaire
                        if items[0] not in att_diff.keys():
                            
                            #Création d'un dictionnaire temporaire pour stoker les valeurs new et ref associées à l'attribut
                            dict_temp={}
                            dict_temp['new']=dict_value_new[items[0]]
                            dict_temp['ref']=dict_value_ref[items[0]]
                            #Ajout dans le dictionnaire des différences le dictionnaire temporaire
                            att_diff[items[0]]=dict_temp
                            
                    #Transfert en attribut sur la feature du dictionnaire des différences
                    feature_new.setAttribute('_diff_detil',str(att_diff))
                    
                    
                else:
                    #Les 2 hash détaillés sont identiques, on ressort en No Change
                    feature_new.setAttribute('PyCSW_Transaction','No change')
            
            else:
                #La feature n'existe pas, on doit définir une transaction à Insert
                
                feature_new.setAttribute('PyCSW_Transaction','Insert')
            
            #On fait ressortir la nouvelle feature avec la bonne transaction
            self.pyoutput(feature_new)
   

        #On boucle à l'inverse dans les références pour identifier les feature de référence n'étant plus dans les new
        for rf_keys in self.DictFeatureRef.keys():
            
            #Vérifier si la clé existe dans les news
            if rf_keys not in self.DictFeatureNew.keys():
                #La métadonnée de référence a été supprimée, on la fait ressortir avec le PyCSW_Transaction à delete
                feature_del=self.DictFeatureRef[rf_keys]
                feature_del.setAttribute('PyCSW_Transaction','Delete')
                
                self.pyoutput(feature_del)
               
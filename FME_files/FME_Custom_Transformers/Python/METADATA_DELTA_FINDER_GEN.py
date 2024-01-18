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
        if not self.mapping:
            self.mapping = FME_utils.load_yaml_document(open(feature.getAttribute('_yaml_file'), "r").read())
            
            if 'id' not in self.mapping.keys():
                raise
        
        source_type=feature.getAttribute('_source')
        
        feature_dict_hash={}
        
        #Parcourir le yaml pour créer les hash
        for keys in self.mapping.keys():
            
            #Extraction du nom générique de l'attribut
            nom_eva=self.mapping[keys]['attr_name']
            
            
            #Extraction du nom de l'attribut en fonction de la référence/nouveau
            if source_type=='ref':
                nom_att=self.mapping[keys]['attr_ref']
            else:
                nom_att=self.mapping[keys]['attr_new']
                               
            
            value=feature.getAttribute(nom_att)
            
            
            
            
            if nom_eva=='id':
                id=value
            
            if value:
                pass
            else:
                value='METADATA_DELTA_FINDER_NO_VALUE'

            if isinstance(value, list):
                
                
                listToStr = ''.join([str(elem) for i,elem in enumerate(value)])
                
                value=listToStr
                
                
            
            
            
            value_hash=hashlib.sha256(value.encode('utf-8')).hexdigest()
            
                

            feature_dict_hash[nom_eva]=value_hash
            
        feature.setAttribute('feature_dict_hash',str(feature_dict_hash))
        
        if source_type=='ref':
            self.DictFeatureRef[id]=feature
        else:
            self.DictFeatureNew[id]=feature
        
    def close(self):
        
        
        
        #Boucler à partir des nouvelles métadonnées pour identifier les insert / update(ou no change)
        for nf_keys in self.DictFeatureNew.keys():
            
            #Extraction de la feature (new)  contenue dans le dictionnaire des nouvelles métadonnées
            feature_new=self.DictFeatureNew[nf_keys]
            
            
            #Déterminer si l'identifiant (la feature) existe dans la métadonnées référence
            if nf_keys in self.DictFeatureRef.keys():
                
                
                feature_ref=self.DictFeatureRef[nf_keys]
                
                #Hash global new
                hash_detail_new=feature_new.getAttribute('feature_dict_hash')
                #Hash global ref
                hash_detail_ref=feature_ref.getAttribute('feature_dict_hash')
                
                
                if hash_detail_new != hash_detail_ref:
                    # Faire ressortir la feature new avec la transaction Update ainsi que les 2 hash pour trouver la différence
                    feature_new.removeAttribute('feature_dict_hash')
                    feature_new.setAttribute('PyCSW_Transaction','Update')
                    feature_new.setAttribute('_hash_detail_new',hash_detail_new)
                    feature_new.setAttribute('_hash_detail_ref',hash_detail_ref)
                    
                    
                    set1 = set(eval(hash_detail_new).items())
                    
                    
                    set2 = set(eval(hash_detail_ref).items())
                    diff_hash=set1 ^ set2
                    
                    feature_new.setAttribute('_diff_hash',str(diff_hash))
                    
                    
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
                
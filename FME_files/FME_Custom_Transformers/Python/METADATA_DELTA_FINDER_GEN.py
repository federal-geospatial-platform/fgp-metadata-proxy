import fme
import fmeobjects
import yaml
from Python.FME_utils import FME_utils
import hashlib
import re
try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

 
class FeatureProcessor(object):


    def __init__(self):
    
        self.mapping = {}   #dictionnary containing the yaml content new and ref attributes to compare and their corresponding attribute names
        self.dict_ref_globalhash = {}  #dictionnary containing the global hash for ref metadata (key = id)
        self.dict_new_globalhash = {}  #dictionnary containing the global hash for new metadata (key = id)
        self.dict_ref_att = {}  #dictionnary containing the hash value for each attributes in the yaml file for ref metadata (key = id)
        self.dict_new_att = {}  #dictionnary containing the hash value for each attributes in the yaml file for new metadata (key = id)
        self.listatt_name = []  #list containing the yaml attributes names 
        self.listatt_diff = []  #list with the attributes names for which the hash value for each attributes is different between new and ref        
        self.all_att_names_ref = []   #list with all attributes names for ref attributes
        self.all_att_names_new = []   #list with all attributes names for new attributes
        self.featureList = []
        self.logger = fmeobjects.FMELogFile()
        
    
    def create_hash_key(self,feature,uuid,attr_ref_or_new,dict_globalhash,dict_att):
        #Create global_hash for each metadata for all attributes and a dictionary with the attribute names + hash key for each metadata (will be applied to new and ref)
        #web_pdb.set_trace()
        id=uuid
        _hash_ref_or_new=''   #global hash 
        dict_att[id]={}    #create dict_att with key=id  
        for key in self.mapping.keys():  #for each attributes of the yaml file:
               
            #attribute extraction
            attr = feature.getAttribute(self.mapping[key][attr_ref_or_new])  #attribute value
            attr_name = self.mapping[key][attr_ref_or_new] #attribute name for ref or new            
            attr_name_yaml = self.mapping[key]['attr_name'] #attribute name in the yaml file

            
            #Check if attr_name is in the list of names for all attributes (ref or new); else terminate the programm
            if attr_ref_or_new=='attr_ref':
                list_all_att_names=self.all_att_names_ref

            if attr_ref_or_new=='attr_new':
                list_all_att_names=self.all_att_names_new

            if attr_name not in list_all_att_names:
                self.logger.logMessageString(" ERROR: attribute: {0} (yaml_name:  {1}) does not exists. Revise attribute name in the yaml file.".format(attr_name,attr_name_yaml), fmeobjects.FME_FATAL)
                raise   #terminate the programm

            
            #apply actions to each attribute to ensure a correct comparison
            if attr_name in list_all_att_names and attr is None: #if attribute is in the self.all_att_names_ref/self.all_att_names_new lists and is None, change to 'NULL'    
                attr = 'NULL' 
            
            if '{}' in attr_name:  #if attribute is a list
               attr_sort = sorted(attr, key=str.casefold)  #sort attribute
               attr_update = ''.join([str(x) for x in attr_sort])  #then join all attributes
            else:
               attr_update = attr    
                  
            
            attr_update2 = str(attr_update).strip().lower().replace('\t',' ').replace('\n',' ').replace('\r',' ')
            if 'bound_l' in attr_name_yaml:            ##############à modifier, trouver une manière plus flexible d'identifier les coordonnées####################
              attr_update3=str(round(float(attr_update2),6))
            else:
              attr_update3=attr_update2           ################à modifier; nommer d'une autre manière que attr_update2 et attr_update3##############################
            #Create hashkey for each attribute                   
            att_hash=hashlib.sha256(attr_update3.encode('utf-8')).hexdigest()
            _hash_ref_or_new += att_hash #Create global hashkey by concatenating all attribute's hashkeys
            dict_globalhash[id]={'hash':_hash_ref_or_new} #add the global hashkey to the dictionary for each metadata (key = id)
            dict_att[id].update({attr_name_yaml:att_hash}) #append all attribute names (in the yaml file) with their hashkey values in a dictionary (key = id)
   
    def input(self, feature):
        
        #read yaml file and extract new and ref attributes names and values in dictionary sel.mapping
        if feature.getAttribute('_order') == 1: 
            self.mapping = FME_utils.load_yaml_document(feature.getAttribute('in_yaml'))
            for key in self.mapping.keys():
                attr_name_yaml = self.mapping[key]['attr_name']
                self.listatt_name.append(attr_name_yaml) #create a list with the yaml attribute names

        #get all attribute names for new attributes
        if feature.getAttribute('_order') == 2:
            self.all_att_names_new = []
            max_index=FME_utils.max_index_attribute_list(feature,'list_all_attribute_names{}')
            for j in range(max_index+1):
                att=feature.getAttribute('list_all_attribute_names{%i}'%(j)) 
                if att not in self.all_att_names_new:
                    self.all_att_names_new.append(att)

        #get all attribute names sor ref attributes
        if feature.getAttribute('_order') == 3:
            self.all_att_names_ref = []
            max_index=FME_utils.max_index_attribute_list(feature,'list_all_attribute_names{}')
            for j in range(max_index+1):
                att=feature.getAttribute('list_all_attribute_names{%i}'%(j)) 
                if att not in self.all_att_names_ref:
                    self.all_att_names_ref.append(att)
            
        #apply create_hash_key() for ref attributes       
        if feature.getAttribute('_order') == 4:
            
            self.create_hash_key(feature,
            uuid=feature.getAttribute(feature.getAttribute('id_ref')),  #id_ref is an attribute created in AttributeCreator_10
            attr_ref_or_new='attr_ref',
            dict_att=self.dict_ref_att,
            dict_globalhash=self.dict_ref_globalhash)

        #apply create_hash_key() for new attributes      
        if feature.getAttribute('_order') == 5:
        
            self.create_hash_key(feature,
            uuid=feature.getAttribute(feature.getAttribute('id_new')),  #id_new is an attribute created in AttributeCreator_11
            attr_ref_or_new='attr_new',
            dict_att=self.dict_new_att,
            dict_globalhash=self.dict_new_globalhash)
            self.featureList.append(feature) #to access new attributes in the def close

        else:
            pass
   
    
    def close(self):
    #check if id is present in both ref and new metadata (else delta=insert or delete); and if it is the case if the global hashkey is the same (delta=no change) or not (delta=update)        
      for key in self.dict_ref_globalhash:    #key = id
         if key not in self.dict_new_globalhash:   #if id in ref is not in new, delta (PYCSW_Transaction) = delete
           newFeature_delete = fmeobjects.FMEFeature()
           newFeature_delete.setAttribute('id',key)
           newFeature_delete.setAttribute('PyCSW_Transaction','Delete')
           self.pyoutput(newFeature_delete)  
           
      for newFeature in self.featureList:  #new attributes
         
        id = newFeature.getAttribute(newFeature.getAttribute('id_new')) #changer pour la valeur du nom de l'attribut 'id' new dans le yaml
        if id in self.dict_ref_globalhash: #if id of new attribute present in ref globalhash dictionnary (update or no change)
            if self.dict_new_globalhash[id]['hash']==self.dict_ref_globalhash[id]['hash']:
                newFeature.setAttribute('PyCSW_Transaction','No change') #if global hash are the same: no change
            else:
                newFeature.setAttribute('PyCSW_Transaction','Update') #if global hash are not the same: update
                self.listatt_diff = []
                for i in self.listatt_name: #if delta=update, log the attributes that are different between ref and new metadata
                     if self.dict_new_att[id][i] != self.dict_ref_att[id][i]:
                      if i not in self.listatt_diff:
                       self.listatt_diff.append(i)
                newFeature.setAttribute('delta_attr',self.listatt_diff)  #add an attribute (delta_attr) with a list of the different attributes between ref and new 
                self.logger.logMessageString(" METADATA_DELTA_FINDER_NG attributes updated: {0}; for id  {1}".format(newFeature.getAttribute('delta_attr'),id), fmeobjects.FME_INFORM)
                
        else:   # id is not present in ref metadata, delta=insert
            newFeature.setAttribute('PyCSW_Transaction','Insert')       
        
        
        self.pyoutput(newFeature)
import requests
import fme
import fmeobjects
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass
    
# FME attribute
FORMAT = "format"
MIME_TYPE = "mime_type"
ORDER = "_order"
ORIGINAL_VALUE = "original_value"
URL_VALIDATION = "_url_validation"
UNKNOWN_MIME_TYPE = "_unknown_mime_type"

# Attribute content
OTHER = "other"

# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter

class FeatureProcessor(object):

    def __init__(self):
        """Contructor of the class.
        
        Create the necessary list and dictionary
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
    
        self.fme_features = []  # Create a list to load FME features
        self.csv_format = {}  # Create a dictionary to load CSV formats
        self.csv_mime_types = {}  # Create a dictionary to load CSV features
        
        return
        
    def input(self, feature):
        """Method called for each FME feature.
        
        The method places each feature in the corresponding data structure depending 
        on the order attribute
        
        Parameters
        ----------
        feature : FME_Feature
            Feature to process
        
        Returns
        -------
        None
        """
    
        order = feature.getAttribute(ORDER)
        if order == 1:
            # Load the format
            original_value = feature.getAttribute(ORIGINAL_VALUE)
            original_value = original_value.lower()
            if original_value not in self.csv_format:
                # Add the key in the dictionary
                self.csv_format[original_value] = None  # Only the key value is important
            else:
                # Key is already in the dictionary
                pass
        elif order == 2:
            # Load the CSV MIME-type
            mime_type = feature.getAttribute(MIME_TYPE)
            url_format = feature.getAttribute(FORMAT)
            self.csv_mime_types[mime_type] = url_format
        else:
            # Load the FME feature
            self.fme_features.append(feature)
            
        return
            
    def close(self):
        """Method call once all the feature are read.
        
        The method processes each FME feature to determine the format.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        for fme_feature in self.fme_features:
            # Process the format of the feature
            self.process_feature(fme_feature)
            
            # Output the FME feature to FME 
            self.pyoutput(fme_feature)
            
        return


    def process_feature(self, feature):
        """This method add a format to ressources with empty format.
        
        This method is analysing the content of the url to determine the format.
        It searches for substring (ex.: service=wms) or extensions (ex.: .shp).
        
        If the format is still unknown, it extracts the format from the MIME-type of
        the HTTP URL call.
        
        Parameters
        ----------
        feature: FME feature
            FME feature to process
        
        Returns
        -------
        None
        
        """

#        web_pdb.set_trace()
        # Extract the number of resources on the features
        nbr_resources = FME_utils.max_index_attribute_list(feature, "resources{}")
        
        for i in range(nbr_resources+1):
            # Extract attribute
            format=feature.getAttribute('resources{%d}.format'%(i))
            url=feature.getAttribute('resources{%d}.url'%(i))
            url_validation = feature.getAttribute(URL_VALIDATION)
            url_original = url
            new_format = format
            
            if not url:
                # resources{i}.url is empty
                new_format = 'other'
            else:
                if not format:  # resources{i}.format is empty
                    # Try to guess the format based on the content of the url
                    if r'service=wms' in url.lower():
                        new_format='WMS'
                    elif r'mapserver' in url.lower() or r'featureserver' in url.lower(): 
                        new_format='ESRI REST'
                    elif  '.'  not in url.split(r'/')[-1]:
                        new_format='other'
                    else:
                        url=url.replace('_','.')
                        url=url.replace('-','.')
                        trim=False
                        try:
                            if url.endswith('.zip'):
                                # Remove the .zip to find the real format
                                # Like Shape in this example: blablabla.shp.zip
                                trim=True
                                url=url.replace('.zip','')
                            
                            if len(url.split(r'/')[-1].split('.'))>1:
                                if len(url.split(r'/')[-1].split('.')[-1])<5:
                                    new_format=url.split(r'/')[-1].split('.')[-1]
                                else:
                                    new_format='other'  # Fallback format value
                            else:
                                new_format='other'  # Fallback format value
                            
                            if trim:
                                try:
                                    int(new_format)
                                    new_format='zip'
                                except:
                                    pass
                                    
                            # Validate if the extracted format is a valid format
                            if new_format.lower() not in self.csv_format:
                                # Unknown format. Set value to default: "other"
                                new_format = OTHER
                
                        except:
                            # In case of any error assign format "other"
                            new_format='other'  # Fallback format value
                            
                if new_format == "other":
                    # Try to guess the format
                    if url_original.endswith(".zip"):
                        # Set format to zip
                        new_format = "zip"  
                    else:
                        # Extract the format using the MIME-type of the url request
                        if url_validation.lower() == "yes":
                            # Try to guess the format using the MIME-type of the url address
                            mime_type = FME_utils.http_get_url_mime_type(url_original)
                            if mime_type != None:
                                try:
                                    new_format = self.csv_mime_types[mime_type]
                                except KeyError:
                                    new_format = OTHER
                                    feature.setAttribute(UNKNOWN_MIME_TYPE, mime_type)
                                    
                            else:
                                # Log an error
                                new_format = OTHER
                        else:
                            # Do not extract the mime type with an http request (validation is no)
                            pass
                else:
                    # No other format are tested 
                    pass

                # Set the format
                feature.setAttribute('resources{%d}.format'%(i),new_format)

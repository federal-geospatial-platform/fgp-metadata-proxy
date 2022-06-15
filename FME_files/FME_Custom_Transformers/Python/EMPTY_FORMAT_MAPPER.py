import fme
import fmeobjects
from Python.FME_utils import FME_utils

try:
    import web_pdb
except:
    # No problem if the package is not avalaible
    pass

# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def process_feature(feature):
    """This method add a format to ressources with empty format.
    
    This method is analysing the content of the url to determine the format.
    It searches for substring (ex.: service=wms) or extensions (ex.: .shp)
    
    Parameters
    ----------
    feature: FME feature
        FME feature to process
    
    Returns
    -------
    None
    
    """

#    web_pdb.set_trace()
    # Extract the number of resources on the features
    nbr_resources = FME_utils.max_index_attribute_list(feature, "resources{}")
    
    for i in range(nbr_resources+1):
        format=feature.getAttribute('resources{%d}.format'%(i))
        url=feature.getAttribute('resources{%d}.url'%(i))
        
        if not format:  # resources{i}.format is empty
            if not url:  # resources{i}.url is empty
                new_format='other'
            else:
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
            
                    except:
                        # In case of any error assign format "other"
                        new_format='other'  # Fallback format value
                    
            feature.setAttribute('resources{%d}.format'%(i),new_format)

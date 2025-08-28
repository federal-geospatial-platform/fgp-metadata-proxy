import fme
import fmeobjects
import re
from html.parser import HTMLParser


#Defining attribute to skip name
ATTR_TO_SKIP = '_attr_to_skip'

# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter

class HTMLFilter(HTMLParser):
    """Class that serves as the basis for parsing text files formatted in HTML (`More informations: <https://docs.python.org/3/library/html.parser.html>`_)
    
    Notes
    -----
    text : str
        Class variable needed to parse the html string.
    """
    
    text = ""

    
    def handle_data(self, data):
        """This method is called to process arbitrary data (e.g. text nodes and the content of <script>...</script> and <style>...</style>).
    
        Parameters
        ----------
        data: str
            The data to process
        
        Returns
        -------
        self.text: str
            The parsed data
        """
        
        self.text += data


def processFeature(feature):
    """Cleans all string attributes by performing the followin tasks: 

        - Remove html directive (ex.: `<p>bla bla bla <\p>`) so that the string contains only plain text	
        - Replace special character (carriage return, line feed, tab) by white spaces
        - Replace curly braces {} by parenthesis
        - Removing front and trailing white spaces
        - Replace multiple white spaces by only one white space
    
    Parameters
    ----------
    feature: FME feature
        FME feature to process
    
    Returns
    -------
    feature: FME feature
        FME feature who's attributes have been processed accordingly
    
    """  
    
    try:
        # Extract list of all attributes
        list_att=feature.getAllAttributeNames()
        # Extract attribute to skip
        attr_to_skip = feature.getAttribute(ATTR_TO_SKIP)
        
        # Loop over each attribute
        for atts in list_att:
            val_temp=feature.getAttribute(atts)
             
            # Only process String attributes 
            if isinstance(val_temp, str):
                
                # Remove the html directives from a string
                f = HTMLFilter()
                f.feed(val_temp)                
                val=f.text
                
                if not val:
                    #remplacer par la valeur original si le texte est strippé
                    val=val_temp
                
                # Skip attribute specified
                if atts == attr_to_skip:
                    
                    val=val.replace('{','(')
                    val=val.replace('}',')')
                    val=val.replace('&amp;','&')
                
                    # Strip front and trailing white spaces
                    val=val.lstrip(' ')
                    val=val.rstrip(' ')
                
                    # Replace series of white spaces by only one white space and set attribute
                    feature.setAttribute(atts,re.sub(r' +', ' ',val))
                    continue
                    
                # Reaplace some special characters by white space
                val=val.replace('\n',' ') # Line feed
                val=val.replace('\r',' ') # Carriage return
                val=val.replace('\t',' ') # Tab character
                val=val.replace('{','(')
                val=val.replace('}',')')
                val=val.replace('&amp;','&')
                
                # Strip front and trailing white spaces
                val=val.lstrip(' ')
                val=val.rstrip(' ')
                
                # Replace series of white spaces by only one white space and set attribute
                feature.setAttribute(atts,re.sub(r' +', ' ',val))

    except:
        pass

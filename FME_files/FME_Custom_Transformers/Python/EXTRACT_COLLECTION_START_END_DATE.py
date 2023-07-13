import fme
import fmeobjects
import re
from dateutil.parser import parse
import datetime

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class collection_end_start_date_extractor(object):
    """
        Cette classe python permet d'extraire l'étendu temporel à partir d'expression régulière
        Quand c'est une date contenant juste une année, on ajout -01-01 lorsque date début et -12-31 quand fin
        
        Notes
        -----
        Liste des expressions régulières:
        
        1. ^[1-2][0-9][0-9][0-9]$  --> 2001
        
        1.b	^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$  --> 2001-12-18
        
        2. ^[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]$  --> 2001-2002
        
        3. ^[1-2][0-9][0-9][0-9] - [1-2][0-9][0-9][0-9]$  --> 2001 - 2002
        
        4. ^[1-2][0-9][0-9][0-9] to [1-2][0-9][0-9][0-9]$ --> 2002 to 2020
        
        5. ^[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]/[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]$ --> 2017-2018/2019-2020 
        
        6. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]$ --> 2012-09/2020-06
        
        6.b ^[1-2][0-9][0-9][0-9]-[0-1][0-9] - [1-2][0-9][0-9][0-9]-[0-1][0-9]$ --> 2012-09 - 2020-06
        
        7. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] to [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$ --> 2018-04-01 to 2021-06-24
        
        8. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$ --> 2018-04-01/2021-06-24
        
        9. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] to present$ -->2000-01-01 to present
        
        10. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/present$ --> 2000-01-01/present
        
        11. ^[1-2][0-9][0-9][0-9]-present$ -->  2000-present or 2000 - present
        
        12. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]; [1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]$ -->2012-09/2016-06; 2018-09/2019-06
        
        13. ^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9], [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$ --> 1995-01-01, 2000-01-01/2006-12-31
        
        14. ^([1-2][0-9][0-9][0-9],)+$ ==> 2001,2002,2003 ...
        
        15. ^[A-Z,a-z]* [1-2][0-9][0-9][0-9]$ ===> March 2010
        
        16. ^[A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9]$ ===> March 31, 2010
        
        17. ^[A-Z,a-z]* [1-2][0-9][0-9][0-9] - [A-Z,a-z]* [1-2][0-9][0-9][0-9]$ ====> March 2020 - April 2021
        
        18. ^[A-Z,a-z]* [1-2][0-9][0-9][0-9] to [A-Z,a-z]* [1-2][0-9][0-9][0-9]$ ====> March 2020 to April 2021
        
        19. ^[A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9] - [A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9]$ ====> March 31, 2020 to April 15, 2021
        
    """    
    
    
    def __init__(self):
        """Constructor call before any FME features are passed
        """    
        self.dict={}
    def input(self,feature):
        """Process each FME features.
        """
        
        #Extraction de l'ordre
        if int(feature.getAttribute('_ordre'))==1:
            #On est dans la configuration, ajout dans le dictionnaire
            ori=feature.getAttribute('source_date_extent')
            start_date=feature.getAttribute('data_collection_start_date')
            end_date=feature.getAttribute('data_collection_end_date')
            
            self.dict[ori]={'start_date':start_date,'end_date':end_date}
        
        else:
            date_extent=str(feature.getAttribute('_date_to_process'))
        
            if date_extent in self.dict.keys():
              start_date=self.dict[date_extent]['start_date']
              end_date=self.dict[date_extent]['end_date']
            else:
                date_extent_copy=date_extent
                #Définir une de liste de chaine de caracètre à remplacer
                remplacement_string=[[' through ',r'/'],[' onward',''],[' and on',''],[' and ',r'-'],[' census','']]
                date_extent=date_extent.lower()
                for elem in remplacement_string:
                    date_extent=date_extent.replace(elem[0],elem[1])

                start_date=''
                end_date=''
                
                if date_extent:
                                    
                    # 1. De type 2000
                    if re.match('^[1-2][0-9][0-9][0-9]$',date_extent):
                        start_date=date_extent
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]$',date_extent):
                        start_date=date_extent
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent
                    
                    # 1.a De type 2000/
                    elif re.match('^[1-2][0-9][0-9][0-9]/$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                    
                    # 1.b De type 2000/01
                    elif re.match('^[1-2][0-9][0-9][0-9]/[0-1][0-9]$',date_extent):
                        start_date=date_extent	
                    
                    # 1.c De type 2000/01/06
                    elif re.match('^[1-2][0-9][0-9][0-9]/[0-1][0-9]/[0-1][0-9]$',date_extent):
                        start_date=date_extent	
                    
                    # 2. De type 1999-2000
                    elif re.match('^[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]$',date_extent):
                        start_date=date_extent.split('-')[0]
                        end_date=date_extent.split('-')[1]
                    
                    # 2.b De type 1999/2000
                    elif re.match('^[1-2][0-9][0-9][0-9]/[1-2][0-9][0-9][0-9]$',date_extent):
                        
                        start_date=date_extent.split('/')[0]
                        end_date=date_extent.split('/')[1]
                    
                    # 2.c De type 1999 / 2000
                    elif re.match('^[1-2][0-9][0-9][0-9] / [1-2][0-9][0-9][0-9]$',date_extent):
                        
                        start_date=date_extent.split(' / ')[0]
                        end_date=date_extent.split(' / ')[1]
                    
                    
                    # 3. De type 1999 - 2000
                    elif re.match('^[1-2][0-9][0-9][0-9] - [1-2][0-9][0-9][0-9]$',date_extent):
                        
                        start_date=date_extent.split(' - ')[0]
                        end_date=date_extent.split(' - ')[1]
                    
                    # 4.  De type 2002 to 2020
                    elif re.match('^[1-2][0-9][0-9][0-9] to [1-2][0-9][0-9][0-9]$',date_extent):                
                        start_date=date_extent.split(' to ')[0]
                        end_date=date_extent.split(' to ')[1]
                    
                    # 5. De type 2017-2018/2019-2020    
                    elif re.match('^[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]/[1-2][0-9][0-9][0-9]-[1-2][0-9][0-9][0-9]$',date_extent):
                        start_date=date_extent.split(r'-')[0]
                        end_date=date_extent.split(r'-')[-1]
                    
                    # 6. De type 2012-09/2020-06
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                        end_date=date_extent.split(r'/')[1]
                    
                    # 6.b De type 2012-09 - 2020-06
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9] - [1-2][0-9][0-9][0-9]-[0-1][0-9]$',date_extent):
                        start_date=date_extent.split(r' - ')[0]
                        end_date=date_extent.split(r' - ')[1]
                    
                    #7. De type 2018-04-01 to 2021-06-24
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] to [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent.split(r' to ')[0]
                        end_date=date_extent.split(r' to ')[1]
                    
                    #8. De type 2018-04-01/2021-06-24
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                        end_date=date_extent.split(r'/')[1]

                    #8.a De type 2018-04-01 / 2021-06-24
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] / [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent.split(r' / ')[0]
                        end_date=date_extent.split(r' / ')[1]

                    #8.b De type 2018-04-01 au 2021-06-24
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] au [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent.split(r' au ')[0]
                        end_date=date_extent.split(r' au ')[1]
                    
                    #9.  De type 2000-01-01 to present
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9] to present$',date_extent):
                        start_date=date_extent.replace(' to present','')
                    
                    #10. De type 2000-01-01/present
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/present$',date_extent):
                        start_date=date_extent.split(r'/')[0]

                    #10.b De type 2000-01/
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]/$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                    
                    #10.b De type 2000-01-01/
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                    
                    #11.  De type 2000-present
                    elif re.match('^[1-2][0-9][0-9][0-9]\s*-\s*present$',date_extent):
                        start_date=date_extent.split('-')[0]
                    
                    #12. De type 2012-09/2016-06; 2018-09/2019-06
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]; [1-2][0-9][0-9][0-9]-[0-1][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]$',date_extent):
                        start_date=date_extent.split(r'/')[0]
                        end_date=date_extent.split(r'/')[2]
                    
                    #13. De type 1995-01-01, 2000-01-01/2006-12-31
                    elif re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9], [1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]/[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$',date_extent):
                        start_date=date_extent.split(r',')[0]
                        end_date=date_extent.split(r'/')[1]
                    
                    #14. De type 2010, 2015, 2017, 2019
                   
                    elif re.match('^([1-2][0-9][0-9][0-9],)+',date_extent):
                        start_date=date_extent.split(r',')[0]
                        end_date=date_extent.split(r',')[-1]
                    
                    #15 de Type March 2020
                    elif  re.match('^[A-Z,a-z]* [1-2][0-9][0-9][0-9]$',date_extent):
                        try:
                            datem = datetime.datetime.strptime(date_extent, "%B %Y")
                            start_date = datem.strftime("%Y-%m-%d")
                        except ValueError:
                            feature.setAttribute('unmatched_date_extent',date_extent)
                        
                    #16 De type March 31, 2020
                    elif  re.match('^[A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9]$',date_extent):
                        try:
                            datem = datetime.datetime.strptime(date_extent, "%B %d, %Y")
                            start_date = datem.strftime("%Y-%m-%d")
                        except ValueError:
                            feature.setAttribute('unmatched_date_extent',date_extent)
                        
                    #17 de Type March 2020 - April 2021
                    elif  re.match('^[A-Z,a-z]* [1-2][0-9][0-9][0-9] - [A-Z,a-z]* [1-2][0-9][0-9][0-9]$',date_extent):
                        try:
                            date_split = date_extent.split(' - ')
                            datem = datetime.datetime.strptime(date_split[0], "%B %Y")
                            start_date = datem.strftime("%Y-%m-%d")
                            datem = datetime.datetime.strptime(date_split[1], "%B %Y")
                            end_date = datem.strftime("%Y-%m-%d")
                        except ValueError:
                            feature.setAttribute('unmatched_date_extent',date_extent)
                        
                    #18 de Type March 2020 to April 2021
                    elif  re.match('^[A-Z,a-z]* [1-2][0-9][0-9][0-9] to [A-Z,a-z]* [1-2][0-9][0-9][0-9]$',date_extent):
                        try:
                            date_split = date_extent.split(' to ')
                            datem = datetime.datetime.strptime(date_split[0], "%B %Y")
                            start_date = datem.strftime("%Y-%m-%d")
                            datem = datetime.datetime.strptime(date_split[1], "%B %Y")
                            end_date = datem.strftime("%Y-%m-%d")
                        except ValueError:
                            feature.setAttribute('unmatched_date_extent',date_extent)
                        
                    #19 de Type March 31, 2020 - April 15, 2021
                    elif  re.match('^[A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9] - [A-Z,a-z]* ([1-9]|[0-3][0-9]), [1-2][0-9][0-9][0-9]$',date_extent):
                        try:
                            date_split = date_extent.split(' - ')
                            datem = datetime.datetime.strptime(date_split[0], "%B %d, %Y")
                            start_date = datem.strftime("%Y-%m-%d")
                            datem = datetime.datetime.strptime(date_split[1], "%B %d, %Y")
                            end_date = datem.strftime("%Y-%m-%d")
                        except ValueError:
                            feature.setAttribute('unmatched_date_extent',date_extent)
                    
                    else:
                        
                        feature.setAttribute('unmatched_date_extent',date_extent)
                    
                else:
                    start_date='0001-01-01'
                
                
            
            start_date=start_date.rstrip(' ').lstrip(' ')
            
            #Validation de la date
            try:
                parse(start_date)
            except:
                feature.setAttribute('unmatched_date_extent',date_extent_copy)
                
            if end_date:
                try:
                    parse(end_date)
                except:
                    feature.setAttribute('unmatched_date_extent',date_extent_copy)
                       
            if re.match('^[1-2][0-9][0-9][0-9]$',start_date):
               start_date='%s-01-01'%(start_date)
            
            if re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]$',start_date):
               start_date='%s-01'%(start_date)
            if end_date:
               end_date=end_date.rstrip(' ').lstrip(' ')
               if re.match('^[1-2][0-9][0-9][0-9]$',end_date):
                  end_date='%s-12-31'%(end_date)
               if re.match('^[1-2][0-9][0-9][0-9]-[0-1][0-9]$',end_date):
                   if re.match('01|03|05|07|08|10|12$',end_date):
                       
                       end_date='%s-31'%(end_date)
                   elif re.match('02$',end_date):
                       end_date='%s-28'%(end_date)
                   else:
                       
                       end_date='%s-30'%(end_date)

            feature.setAttribute('data_collection_start_date',start_date)
            feature.setAttribute('data_collection_end_date',end_date)
            
            self.pyoutput(feature)
        
    def close(self):
        """Method call when all the festures are passed, not used.
        """
        pass
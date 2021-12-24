import fme
import fmeobjects
import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json
import sys
import xml.etree.ElementTree as ElementTree
from io import StringIO

try:
    import web_pdb  # Web debug tool
except:
    # No problem if the package is not avalaible
    pass

# Define FME attribute names
CSW_CONSTRAINT = "_csw_constraint"
CSW_CONSTRAINT_LANGUAGE = "_csw_constraint_language"
#CSW_FILTER = "_csw_filter"
CSW_LIST_NAME = '_csw_list_name'
CSW_ID = "_id"
CSW_OUTPUT_SCHEMA = "_csw_output_schema"
#CSW_SEARCH_CRITERIA = "_csw_search_criteria"
CSW_TYPENAMES = "_csw_typenames"
CSW_TYPENAMES_COPY = "_csw_typenames_copy"
CSW_VERSION = "_csw_version"
ID = "_id"
HTTP_CALL_ERROR = "_http_call_error"
OPEN_MAP_FILTER = "_OpenMapsFilter"
RESPONSE_BODY = "_response_body"
ROOT_URL = "root_url"
STATUS_CODE = "_status_code"
STATUS_CODE_DESCRIPTION = "_status_code_description"
TYPE_REQUETE = "_type_requete"

# FME request
CKAN_ALL_RECORDS = "CKAN-AllRecords"
CKAN_BY_ID = "CKAN-ByID"
CSW_ALL_RECORDS = "CSW-AllRecords"
CSW_BY_ID = "CSW-ByID"

# Define the maximum number of records that can be read at one time
MAX_RECORD_READ = 50

# Define JSON keyword
RESULT = "result"
RESULTS = "results"

# Define CKAN CKAN call
HTTP_CKAN_ALL = "{0}/package_search?start={1}&rows={2}{3}"
HTTP_CKAN_BY_ID = "{0}/package_show?id={1}"

# Define CSW call
#@Value(root_url)request=GetRecords&service=CSW&version=@Value(csw_version)&elementSetName=full@Value(csw_typenames)@Value(csw_filter)@Value(csw_search_criteria)
HTTP_CSW_HEADER = "{0}request=GetRecords&service=CSW&elementSetName=full&version={1}{2}{3}{4}"  # version csw_typenames, csw_filter, csw_search_criteria
#@Value(root_url)request=GetRecords&service=CSW&version=@Value(csw_version)&elementSetName=full&resultType=results&startPosition=@Value(debut)&maxRecords=10&outputSchema=@Value(csw_schema)@Value(csw_filter)@Value(csw_typenames)@Value(csw_search_criteria)
HTTP_CSW_RECORDS = "{0}request=GetRecords&service=CSW&version={1}&elementSetName=full&resultType=results&startPosition={2}&maxRecords={3}&outputSchema={4}{5}{6}{7}"

#@Value(root_url)request=GetRecordById&service=CSW&version=@Value(csw_version)&elementSetName=full&id=@Value(_id)&outputSchema=@Value(csw_schema)@Value(csw_typenames)@Value(csw_filter)
HTTP_CSW_BY_ID = "{0}request=GetRecordById&service=CSW&version={1}&elementSetName=full&id={2}&outputSchema={3}{4}{5}"
# Define http return code
HTTP_OK = 200

HTTP_CSW_REQUEST = "{0}&service=CSW&elementSetName=full"
#header = version csw_typenames csw_filter csw_search_criteria
    

# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class ManageHttpCall(object):
    """This class enables the call to CKAN servers and the creation of FME features with CKAN information.
    
    The results from the CKAN servers are stored in the FME Feature attribute (*_response_body*).
    For each FME Feaure the result from the CKAN reading and the JSON transformation is stored in the 
    FME Feature attribute *_status_code* and the description of the result code in the attribute
    *_status_code_attribute*.
    
    CKAN server extraction options:
    
      - to read only one record from the CKAN server write the UUID of the record to read in the 
    FME Feature attribute *_id*; 
      - to read all the records leave the FME attribute '_id' empty.
      - to read specific records use the CKAN filter, write the CKAN filter in the FME Feature attribute *_OpenMapsFilter*;
      the format of the CKAN Filter is: *fq=collection:federated* where *fq* is a keyword of the CKAN http get
      request; *collection* is a keyword of the JSON record and *federated* is the requested value.    
    """

    def __init__(self):
        """Constructor of the class.
        
        Creates the logger to log information in FME log.
        """
        
        self.logger = fmeobjects.FMELogFile()
        
    def output_fme_error(self, feature, status_code, description):
        """Output an FME feature and set status code and description.
        
        Parameters
        ----------
        feature: FME Feature object
            FME feature to process
        status_code: int
            Status code of the http request
        description: str
            Literal description of the status code
            
        Returns
        -------
        None
        """
    
        feature_cloned = feature.clone()  # Do not use the original feature
        feature_cloned.setAttribute(STATUS_CODE, status_code)
        feature_cloned.setAttribute(STATUS_CODE_DESCRIPTION, description)
        self.pyoutput(feature_cloned)
        
        return
    
    def make_http_call(self, feature, session, str_http, output_fme=True):
        """This method makes an http call and manage the request response.
        
        If the response from the http request is not 200 (OK); an entry is made in the logger
        and an FME feature is outputted with the status code and the description
        
        Parameters
        ----------
        feature: FME Feature object
            FME feature to process
        session: Session object
            Used to make the http call
        str_http: str
            Http string used for the http call
        output_fme: Bool
            True: output an FME feature; False: do not output an FME feature
        
        Returns
        -------
        Request object
            Result from the get request
        """
    
        try:
            self.logger.logMessageString("HTTP call: {0}".format(str_http), 
                                         fmeobjects.FME_INFORM)
            response = session.get(str_http, verify=False, timeout=10)
            status_code = response.status_code
            description = requests.status_codes._codes[status_code][0]
            
            # Manage if an FME feature need to be outputted
            if status_code != HTTP_OK and output_fme:
                self.output_fme_error(feature, status_code, description)
                self.logger.logMessageString("Status code: {0}: {1}".format(status_code, description), 
                                             fmeobjects.FME_INFORM)    
        except Exception as err:
            # Manage the case where an error occured during the reading of the CKAN server
            self.logger.logMessageString("HTTP call error: {0}".format(err), 
                                         fmeobjects.FME_ERROR)
            self.output_fme_error(feature, "500", requests.status_codes._codes[500][0])
            sys.exit(0)

        return response
    
    def create_session(self, http_address):
        """This method creates an http session.
        
        Parameters
        ----------
        http_address: str
            The http address used to create a session
            
        Returns
        -------
        Session
            Session to use to make http requests
        """
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1.0,
                        status_forcelist=[ 500, 502, 503, 504 ])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        return session
    
    def read_ckan_records(self, feature, session, first_id, number_to_read):
        """This method reads the requested records from a CKAN web site and output FME Feature.
        
        Parameters
        ----------
         feature: FME Feature object
            FME feature to process
        session: Session object
            Use to make the http call
        first_id: int
            Position of the first id to read
        number_to_read: int
            Number of record to read in the CKAN web site
            
        Returns
        -------
        None
        """    
        
        head = first_id
        last_id = first_id + number_to_read - 1
        # Read the CKAN server by batch of MAX_REACORD_READ
        while head <= last_id:
            if last_id - head + 1 >= MAX_RECORD_READ:
                read_size = MAX_RECORD_READ
            else:
               read_size = last_id - head + 1
            
            # Form the HTTP call 
            str_http = HTTP_CKAN_ALL.format(self.root_url, head, read_size, self.open_map_filter)
            response = self.make_http_call(feature, session, str_http, True)  # Read the CKAN server
            
            if response.status_code == HTTP_OK:
                head += read_size
                try:
                    json_response = response.json()
                    result = json_response[RESULT]
                    results = result[RESULTS]
                except Exception as err:
                    # Mange the case where the JSON is not well formed
                    self.logger.logMessageString("JSON document is not well formed: {0}".format(err), 
                                                 fmeobjects.FME_ERROR)
                    self.output_fme_error(feature, "600", "JSON document is not well formed")
                    sys.exit(0)
                
                # Output the FME feature with in attribute the JSON file
                for json_result in results:
                    str_json_result = json.dumps(json_result)
                    feature_cloned = feature.clone()
                    feature_cloned.setAttribute(STATUS_CODE, HTTP_OK)
                    feature_cloned.setAttribute(RESPONSE_BODY, str_json_result)
                    self.pyoutput(feature_cloned)
            else:
                # Nothing to do if there is an error
                pass
                
        return
        
    def build_csw_request(self, root_url, csw_output_schema="", csw_request="",
                          csw_typenames="", csw_version="", csw_id="",
                          csw_constraint="", csw_start_position="", csw_max_records="",
                          csw_constraint_language="", csw_result_type=""):
                          
        def add_param_key_value(param_key, param_value):
                   
            if param_value != "":
                param_key_value = "&" + param_key + "=" + param_value
            else:
                param_key_value = ""
            
            return param_key_value
                         
        http_csw_request = HTTP_CSW_REQUEST.format(root_url)
        
        http_csw_request += add_param_key_value("request", csw_request)
        http_csw_request += add_param_key_value("id", csw_id)
        http_csw_request += add_param_key_value("resultType", csw_result_type)
        http_csw_request += add_param_key_value("startPosition", csw_start_position)
        http_csw_request += add_param_key_value("maxRecords", csw_max_records)
        http_csw_request += add_param_key_value("outputSchema", csw_output_schema)
        http_csw_request += add_param_key_value("version", csw_version)
        http_csw_request += add_param_key_value("typeNames", csw_typenames)
        http_csw_request += add_param_key_value("constraintLanguage", csw_constraint_language)
        http_csw_request += add_param_key_value("constraint", csw_constraint)
        
        return http_csw_request           
        
    def calculate_start_max_record(self, nbr_records):
    
        nbr_loops = nbr_records//MAX_RECORD_READ
        remaining = nbr_records%MAX_RECORD_READ
        
        lst_start_max = [(i*MAX_RECORD_READ, MAX_RECORD_READ) for i in range(nbr_loops)]
        
        if remaining != 0:
           lst_start_max.append((nbr_loops*MAX_RECORD_READ, remaining))
           
        if len(lst_start_max) == 0:
            lst_start_max = [(0,0)]

        return lst_start_max
    
    def read_csw_records(self, feature, session, first_id, number_to_read):
        """This method reads the requested records from a CKAN web site and output FME Feature.
        
        Parameters
        ----------
         feature: FME Feature object
            FME feature to process
        session: Session object
            Use to make the http call
        first_id: int
            Position of the first id to read
        number_to_read: int
            Number of record to read in the CKAN web site
            
        Returns
        -------
        None
        """    
        
        web_pdb.set_trace()
        
        lst_start_max = self.calculate_start_max_record(number_to_read)
#        head = first_id
#        last_id = first_id + number_to_read - 1
        # Read the CKAN server by batch of MAX_REACORD_READ
        for head, read_size in lst_start_max:
#        while head <= last_id:
#            if last_id - head + 1 >= MAX_RECORD_READ:
#                read_size = MAX_RECORD_READ
#            else:
#               read_size = last_id - head + 1
            
            # Form the HTTP call
            
            str_http = self.build_csw_request(root_url=self.root_url,
                                              csw_request="GetRecords",
                                              csw_version=self.csw_version,
                                              csw_start_position=str(head+1), 
                                              csw_max_records=str(read_size),
                                              csw_result_type="results",
                                              csw_output_schema=self.csw_output_schema,
                                              csw_typenames=self.csw_typenames, 
                                              csw_constraint_language=self.csw_constraint_language, 
                                              csw_constraint=self.csw_constraint)
            
            response = self.make_http_call(feature, session, str_http, True)  # Read the CKAN server
            if response.status_code == HTTP_OK:
                str_xml = self.extract_xml_response(response)
#                head += read_size
                feature_cloned = feature.clone()
                feature_cloned.setAttribute(STATUS_CODE, HTTP_OK)
                feature_cloned.setAttribute(RESPONSE_BODY, str_xml)
                self.pyoutput(feature_cloned)
            else:
                # Nothing to do if there is an error
                pass
                
        return
            
    def read_ckan_all(self, feature):
        """This method read one record from the CKAN web site
    
        Parameters
        ----------
        feature: FME Feature object
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        # Build the HTTP request
        str_http = HTTP_CKAN_ALL.format(self.root_url, 0, 1, self.open_map_filter)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
    
        # Get the header of the web service
        response = self.make_http_call(feature, session, str_http)
        self.logger.logMessageString("HTTP call: {0}".format(str_http), fmeobjects.FME_INFORM)
      
        # Extract the information from the JSON document
        json_response = response.json()
        result = json_response["result"]
        count = int(result["count"])

        self.read_ckan_records(feature, session, 0, count)
        
    def extract_xml_response(self, response):
        """
        """
        
        # Extract the information from the XML document
        xml_str = response.content.decode("utf-8")  # Convert to utf-8
        xml_str = xml_str.strip()  # Strip whitespaces
        
        return xml_str
        
    
    def read_csw_all(self, feature):
        """This method read one record from the CKAN web site
    
        Parameters
        ----------
        feature: FME Feature object
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        web_pdb.set_trace()
        
        #HTTP_CSW_REQUEST = "{0}request=GetRecords&service=CSW&elementSetName=full&resultType=results"
        #header = version csw_typenames csw_filter csw_search_criteria
        
        a = self.csw_constraint_language
        str_http = self.build_csw_request(root_url=self.root_url,
                                          csw_request="GetRecords",
                                          csw_version=self.csw_version, 
                                          csw_typenames=self.csw_typenames, 
                                          csw_constraint_language=self.csw_constraint_language, 
                                          csw_constraint=self.csw_constraint)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
    
        # Get the header of the web service
        response = self.make_http_call(feature, session, str_http)
        self.logger.logMessageString("HTTP call: {0}".format(str_http), fmeobjects.FME_INFORM)
      
        # Extract the information from the XML document
        xml_str = self.extract_xml_response(response)
        
        # Extract the name spaces
        my_namespaces = dict([node for _, node in ElementTree.iterparse(StringIO(xml_str), events=['start-ns'])])
        elem_tree = ElementTree.fromstring(xml_str)  # Read the xml string
        el = elem_tree.find('.//csw:SearchResults', my_namespaces)
        count = int(el.attrib['numberOfRecordsMatched'])
        

        self.read_csw_records(feature, session, 0, count)
    
    def read_ckan_by_id(self, feature):
        """This method read one  record from the CKAN server.
    
        Parameters
        ----------
        feature: FME Feature object
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        # Extract the UUID 
        id = feature.getAttribute(ID)
        
        # Build the http request
        str_http = HTTP_CKAN_BY_ID.format(self.root_url, id)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
        
        # Make the http call
        response = self.make_http_call(feature, session, str_http)
        
        if response.status_code == HTTP_OK:
                str_xml = self.extract_xml_response(response)
                head += read_size
                feature_cloned = feature.clone()
                feature_cloned.setAttribute(STATUS_CODE, HTTP_OK)
                feature_cloned.setAttribute(RESPONSE_BODY, str_xml)
                self.pyoutput(feature_cloned)
        else:
            # Nothing to do if there is an error
            pass
            
        return
        
    def read_csw_by_id(self, feature):
        """This method read one  record from the CSW server.
    
        Parameters
        ----------
        feature: FME Feature object
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
        # Extract the UUID 
        id = feature.getAttribute(ID)
        
        str_http = self.build_csw_request(root_url=self.root_url,
                                          csw_request="GetRecordById",
                                          csw_id=self.csw_id,
                                          csw_version=self.csw_version,
                                          csw_result_type="results",
                                          csw_output_schema=self.csw_output_schema,
                                          csw_typenames=self.csw_typenames, 
                                          csw_constraint_language=self.csw_constraint_language, 
                                          csw_constraint=self.csw_constraint)
        
        # Build the http request
        #@Value(root_url)request=GetRecordById&service=CSW&version=@Value(csw_version)&elementSetName=full&id=@Value(_id)&outputSchema=@Value(csw_schema)@Value(csw_typenames)@Value(csw_filter)
        #HTTP_CSW_BY_ID = "{0}request=GetRecordById&service=CSW&version={1}&elementSetName=full&id={2}&outputSchema={3}{4}{5}"
#        str_http = HTTP_CSW_BY_ID.format(self.root_url, self.csw_version, id, self.csw_schema, 
#                                         self.csw_typenames, self.csw_filter)
        
        # Create a session to be used to make http request
        session = self.create_session(str_http)
        
        # Make the http call
        response = self.make_http_call(feature, session, str_http)
        
        if response.status_code == HTTP_OK:
            xml_str = self.extract_xml_response(response)
            try:
                my_namespaces = dict([node for _, node in ElementTree.iterparse(StringIO(xml_str), events=['start-ns'])])
                elem_tree = ElementTree.fromstring(xml_str)  # Read the xml string
                xml_node_to_search = self.csw_typenames
#                xml_node_to_search = './/csw:SearchResults/{0}'.format(self.node_to_search)
                xml_results = elem_tree.findall(xml_node_to_search, my_namespaces)
            except Exception as err:
                # Mange the case where the XML is not well formed
                self.logger.logMessageString("XML document is not well formed: {0}".format(err), 
                                             fmeobjects.FME_ERROR)
                self.output_fme_error(feature, "600", "XML document is not well formed")
                sys.exit(0)
            
            # Output the FME feature with in attribute the JSON file
#
            for xml_result in xml_results:          
                str_xml_result = ElementTree.tostring(xml_result).decode()
                feature_cloned = feature.clone()
                feature_cloned.setAttribute(STATUS_CODE, HTTP_OK)
                feature_cloned.setAttribute(RESPONSE_BODY, str_xml_result)
                self.pyoutput(feature_cloned)
        else:
            # Nothing to do if there is an error
            pass
            
        return
        
    def feature_get_attribute(self, feature, attribute_key, error_if_none=False):
    
        attribute_value = feature.getAttribute(attribute_key)
        if attribute_value is None:
            if error_if_none:
                raise Exception ("Error.  Attribute: {} is missing)".format(attribute_key))
            else:
                attribute_value = ""
            
        return attribute_value
    
    def input(self,feature):
        """Main routine call be the FME software
        
        Manage the reading of CKAN server for all or by id (one record only)
        
        Parameters
        ----------
        feature: FME Feature object 
            FME Feature to process
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        # Extract the target URL
        self.root_url = feature.getAttribute(ROOT_URL)
        
        # Extract the type of reuqest
        type_requete = feature.getAttribute(TYPE_REQUETE)
        
        # Extract the open map filter
        self.open_map_filter = feature.getAttribute(OPEN_MAP_FILTER)
        if self.open_map_filter is None or self.open_map_filter == "":
            self.open_map_filter = ""
        else:
            self.open_map_filter = "&" + self.open_map_filter  # & is for a web parameter
            
        # Extract the CSW parameters stored in attribure
        self.csw_typenames = self.feature_get_attribute(feature, CSW_TYPENAMES, True)
        self.csw_id = self.feature_get_attribute(feature, CSW_ID, True)
        self.csw_version = self.feature_get_attribute(feature, CSW_VERSION, True)
        self.csw_output_schema = self.feature_get_attribute(feature, CSW_OUTPUT_SCHEMA, True)
        self.csw_list_name = self.feature_get_attribute(feature, CSW_LIST_NAME, True)
        self.csw_constraint_language = self.feature_get_attribute(feature, CSW_CONSTRAINT_LANGUAGE, True)
        self.csw_constraint = self.feature_get_attribute(feature, CSW_CONSTRAINT, True)
                    
        # Execute the requested type of request
        if type_requete == CKAN_ALL_RECORDS:
            self.read_ckan_all(feature)
        elif type_requete == CKAN_BY_ID:
            self.read_ckan_by_id(feature)
        elif type_requete == CSW_ALL_RECORDS:
            self.read_csw_all(feature)
        else:
            self.read_csw_by_id(feature)
 
    def close(self):
        """Unused method"""
        pass

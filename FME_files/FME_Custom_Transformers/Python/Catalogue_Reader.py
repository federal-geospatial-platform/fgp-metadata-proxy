import fme
import fmeobjects
import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from Python.FME_utils import FME_utils
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
CSW_LIST_NAME = '_csw_list_name'
CSW_ID = "_id"
CSW_OUTPUT_SCHEMA = "_csw_output_schema"
CSW_TYPENAMES = "_csw_typenames"
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

# Define CKAN call
HTTP_CKAN_ALL = "{0}/package_search?start={1}&rows={2}{3}"
HTTP_CKAN_BY_ID = "{0}/package_show?id={1}"

# Define http return code
HTTP_OK = 200

# Define CSW call
HTTP_CSW_REQUEST = "{0}&service=CSW&elementSetName=full"   

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
    
      - to read only one record from the CKAN server write the UUID of the record to read \
      in the FME Feature attribute *_id*; 
      - to read all the records leave the FME attribute '_id' empty
      - to read specific records use the CKAN filter, write the CKAN filter in the FME Feature \
      attribute *_OpenMapsFilter*; the format of the CKAN Filter is: *fq=collection:federated* \
      where *fq* is a keyword of the CKAN http get request; *collection* is a keyword of the \
      JSON record and *federated* is the requested value.
      
    """

    def __init__(self):
        """Constructor of the class.
        
        Creates the logger to log information in FME log.
        """
        
        self.logger = fmeobjects.FMELogFile()
        
    def build_csw_request(self, root_url, csw_output_schema="", csw_request="",
                          csw_typenames="", csw_version="", csw_id="",
                          csw_constraint="", csw_start_position="", csw_max_records="",
                          csw_constraint_language="", csw_result_type=""):
        """This method build an http CSW request.
        
        Parameters
        ----------
        root_url: string
            The url of the request
        csw_output_schema: string
            The target output schema
        csw_request: string
            The CSW type of request
        csw_typenames: string
            The type name of the request
        csw_version: string
            The version numver of the CSW
        csw_id: string
            The id of the string to search
        csw_constraint: string
            The constraint to use
        csw_start_position: string
            The start position to read
        csw_max_records: string
            The number of record to read
        csw_constraint_language: string
            The constraint language
        csw_result_type: string
            The type of result
            
        Returns
        -------
        String
            Valid http CSW ewuqest 
        """
                          
        def _add_param_key_value(param_key, param_value):
            """Add a parameter to the http request.
            """
                   
            if param_value != "":
                param_key_value = "&" + param_key + "=" + param_value
            else:
                param_key_value = ""
            
            return param_key_value
                         
        http_csw_request = HTTP_CSW_REQUEST.format(root_url)
        
        http_csw_request += _add_param_key_value("request", csw_request)
        http_csw_request += _add_param_key_value("id", csw_id)
        http_csw_request += _add_param_key_value("resultType", csw_result_type)
        http_csw_request += _add_param_key_value("startPosition", csw_start_position)
        http_csw_request += _add_param_key_value("maxRecords", csw_max_records)
        http_csw_request += _add_param_key_value("outputSchema", csw_output_schema)
        http_csw_request += _add_param_key_value("version", csw_version)
        http_csw_request += _add_param_key_value("typeNames", csw_typenames)
        http_csw_request += _add_param_key_value("constraintLanguage", csw_constraint_language)
        http_csw_request += _add_param_key_value("constraint", csw_constraint)
        
        return http_csw_request           
        
    def calculate_start_max_record(self, nbr_records):
        """This method calculates the number and the start position of the records to read for each iteration.
        
        Parameters
        ----------
        nbr_records: int
            Total number of records to read
            
        Returns
        -------
        List of tuple (int,int)
            For each tuple, the first value is the position to read; the second value, 
            the number of record to read. If there is no record to read it returns an empty list []
        """
    
        if nbr_records == 0:
           # There is no records to read
           lst_start_max = []
        
        else:
            # There is one or more record to read        
            nbr_loops = nbr_records//MAX_RECORD_READ
            remaining = nbr_records%MAX_RECORD_READ
            
            lst_start_max = [(i*MAX_RECORD_READ, MAX_RECORD_READ) for i in range(nbr_loops)]
            
            if remaining != 0:
               lst_start_max.append((nbr_loops*MAX_RECORD_READ, remaining))
               
            if len(lst_start_max) == 0:
                lst_start_max = [(0,0)]

        return lst_start_max
            
    def extract_xml_response(self, response):
        """Convert to UTF-8 and strip leading and ending white spaces.
        
        Parameters
        ----------
        response: String
            String to process
            
        Returns
        -------
        String
            The string without trailing and ending whitespaces
        """
        
        # Extract the information from the XML document
        xml_str = response.content.decode("utf-8")  # Convert to utf-8
        xml_str = xml_str.strip()  # Strip whitespaces
        
        return xml_str

    def read_csw_records(self, feature, session, first_id, number_to_read):
        """This method reads the requested records from a CSW web site and output FME Feature.
        
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
        
#        web_pdb.set_trace()
        lst_start_max = self.calculate_start_max_record(number_to_read)
        # Read the CSW server by batch of MAX_REACORD_READ
        for head, read_size in lst_start_max:
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
            
            response = FME_utils.make_http_call(self, feature, session, str_http, True)  # Read the CSW server
            if response.status_code == HTTP_OK:
                xml_str = self.extract_xml_response(response)
                # Output the FME feature with an attribute containing the XML document
                lst_key_val_att = [(STATUS_CODE, HTTP_OK), 
                                   (RESPONSE_BODY, xml_str)]
                FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
                
        return
    
    def read_csw(self, feature):
        """This method read one record from the CKAN web site
    
        Parameters
        ----------
        feature: FME Feature object
            The Fme feature to process
        
        Returns
        -------
        None
        """
    
#        web_pdb.set_trace()
        # Build the HTTP request
        if self.type_requete == CSW_ALL_RECORDS:
            # Read ALL CSW records
            str_http = self.build_csw_request(root_url=self.root_url,
                                              csw_request="GetRecords",
                                              csw_version=self.csw_version, 
                                              csw_typenames=self.csw_typenames, 
                                              csw_constraint_language=self.csw_constraint_language, 
                                              csw_constraint=self.csw_constraint)
        else:
            # Read By ID record
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
        
        # Create a session to be used to make http request
        session = FME_utils.create_session()
    
        # Get the header of the web service
        response = FME_utils.make_http_call(self, feature, session, str_http, True)
      
        # Extract the information from the XML document
        xml_str = self.extract_xml_response(response)
        
        if response.status_code == HTTP_OK:
            if self.type_requete == CSW_ALL_RECORDS:  # Read ALL CSW records
                my_namespaces = dict([node for _, node in ElementTree.iterparse(StringIO(xml_str), events=['start-ns'])])
                elem_tree = ElementTree.fromstring(xml_str)  # Read the xml string
                el = elem_tree.find('.//csw:SearchResults', my_namespaces)
                count = int(el.attrib['numberOfRecordsMatched'])  # Extract number of record
                self.read_csw_records(feature, session, 0, count)  # Read all records
            else:  # Read By ID record
                # Output the FME feature with an attribute containing the XML document
                lst_key_val_att = [(STATUS_CODE, HTTP_OK), 
                                   (RESPONSE_BODY, xml_str)]
                FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
    
    def read_ckan_all_records(self, feature, session, first_id, number_to_read):
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
        
        lst_start_max = self.calculate_start_max_record(number_to_read)
        # Read the CKAN server by batch of MAX_REACORD_READ
        for head, read_size in lst_start_max:
            # Form the HTTP call 
            str_http = HTTP_CKAN_ALL.format(self.root_url, head, read_size, self.open_map_filter)
            response = FME_utils.make_http_call(self, feature, session, str_http, True)  # Read the CKAN server
            
            if response.status_code == HTTP_OK:
                try:
                    json_response = response.json()
                    result = json_response[RESULT]
                    results = result[RESULTS]
                except Exception as err:
                    # Mange the case where the JSON is not well formed
                    self.logger.logMessageString("JSON document is not well formed: {0}".format(err), 
                                                 fmeobjects.FME_ERROR)
                    lst_key_val_att = [(STATUS_CODE, "600"),
                                       (STATUS_CODE_DESCRIPTION, "JSON document is not well formed")]
                    FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
                    sys.exit(0)
                
                # Output the FME feature with in attribute the JSON file
                for json_result in results:
                    str_json_result = json.dumps(json_result)
                    lst_key_val_att = [(STATUS_CODE, HTTP_OK), 
                                       (RESPONSE_BODY, str_json_result)]
                    FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)

                
        return

    def read_ckan(self, feature):
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
        if self.type_requete == CKAN_ALL_RECORDS:
            # All Records
            str_http = HTTP_CKAN_ALL.format(self.root_url, 0, 1, self.open_map_filter)
        else:
            # By ID
            id = feature.getAttribute(ID)
            str_http = HTTP_CKAN_BY_ID.format(self.root_url, id)
        
        # Create a session to be used to make http request
        session = FME_utils.create_session()
    
        # Get the header of the web service
        response = FME_utils.make_http_call(self, feature, session, str_http)
        
        if self.type_requete == CKAN_ALL_RECORDS:
            # Extarct information
            json_response = response.json()
            result = json_response["result"]
            count = int(result["count"])
            # Read all CKAN records from the server
            self.read_ckan_all_records(feature, session, 0, count)
        else:
            # Extract and output information
            if response.status_code == HTTP_OK:
                str_json = self.extract_xml_response(response)
                lst_key_val_att = [(STATUS_CODE, HTTP_OK), 
                                   (RESPONSE_BODY, str_json)]
                FME_utils.pyoutput_feature(self, feature, lst_key_val_att, clone=True)
    
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
        self.type_requete = feature.getAttribute(TYPE_REQUETE)
        
        # Extract the open map filter
        self.open_map_filter = feature.getAttribute(OPEN_MAP_FILTER)
        if self.open_map_filter is None or self.open_map_filter == "":
            self.open_map_filter = ""
        else:
            self.open_map_filter = "&" + self.open_map_filter  # & is for a web parameter
            
        # Extract the CSW parameters stored in attribure
        self.csw_typenames = FME_utils.feature_get_attribute(feature, CSW_TYPENAMES, True)
        self.csw_id = FME_utils.feature_get_attribute(feature, CSW_ID, True)
        self.csw_version = FME_utils.feature_get_attribute(feature, CSW_VERSION, True)
        self.csw_output_schema = FME_utils.feature_get_attribute(feature, CSW_OUTPUT_SCHEMA, True)
        self.csw_list_name = FME_utils.feature_get_attribute(feature, CSW_LIST_NAME, True)
        self.csw_constraint_language = FME_utils.feature_get_attribute(feature, CSW_CONSTRAINT_LANGUAGE, True)
        self.csw_constraint = FME_utils.feature_get_attribute(feature, CSW_CONSTRAINT, True)
                    
        # Execute the requested type of request
        if self.type_requete in [CKAN_ALL_RECORDS, CKAN_BY_ID]:
            self.read_ckan(feature)
        elif self.type_requete in [CSW_ALL_RECORDS, CSW_BY_ID]:
            self.read_csw(feature)
        else:
            pass
 
    def close(self):
        """Mandatory but unused method
        """
        
        pass

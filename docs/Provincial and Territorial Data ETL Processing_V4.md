
Provincial and Territorial Extraction, Transformation and Loading Processes
==========

- [Table of Contents](#table-of-contents)
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes)
  - [Overview](#overview)
    - [Workspaces](#workspaces)
	- [Custom Transformers](#custom-transformers)
	- [XML Templates](#xml-templates)
  - [Workspaces](#workspaces-1)
  - [Custom Transformers Detail](#custom-transformers-detail)	
   
# Provincial and Territorial Extraction, Transformation and Loading Processes

## Overview

### Workspaces

Open data extraction, transformation and loading processes utilize one of two different FME Workspaces for each Canadian province or territory, the workspace utilized will be dependent on whether th ETL process is being utilized for Federal Geospatial Platform (FGP) geospatial data or the FGP along with the Treasury Board Secretariat (TBS) non-geospatial data:

-   **(p-t_abbreviation)_FGP_XML_BUILDER.fmw:** These workspaces extract, transform and load a complete geospatial dataset to an empty Catalogue Service for the Web (CSW), exclusively for the FGP.  The data output result are XML files.  They also output error logs in .XLS format, to allow for updating of lookup table data, troubleshooting errors, or for information only.  These workspaces have a placeholder output for future non-geospatial data for the TBS.

These workspaces are segmented into bookmarks,common to each workspace, with each bookmark containing a series of transformers that may differ from workspace to workspace.  Each of these bookmarks represent a stage in the ETL process:

-  **ETL PROCESS INITIATION:** Starts the process and sets date/time for process reports.
-  **DATA EXTRACTION:** Reads the API and exposes required attributes.  Filters geo/non-geo data when attribute testing allows for selection.
-  **P/T SPECIFIC TRANSFORMATIONS:** Contains custom transformers that are specific to a province or territory due to the unique nature of the metadata and cannot be addressed with a universal transformer.
-  **PRE METADATA MAPPING TRANSFORMATIONS:** Contains universal custom transformers that require processing prior to metadata mapping.
-  **SPATIAL DATA TYPE MANAGEMENT:** Will perform one or more of the following tasks; Validates geospatial data and maps spatial data types.  Filters geo/non-geo data when it can’t be completed in the DATA EXTRACTION process. 
-  **METADATA MAPPING:** Contains universal custom transformers that utilize lookup tables to map data types to HNAP standards.
-  **POST METADATA MAPPING TRANSFORMATIONS:** Contains universal custom transformers to fine tune and customize metadata prior to publishing.
-  **PUBLISHING MANAGMENT:** Contains universal custom transformers that determine the URL of the PyCSW Repository, and compares existing repository data with the current run time data to identify records that are new, obsolete or updated.
-  **LANGUAGE_TRANSLATION:** Universal custom transformer that leverages the AWS translation service to translate specific data items to English or French as required.  Due to the fees required of the AWS, there is an option to bypass the translation service and enter proxy items in the required data fields for testing purposes by turning off the ACTIVATE_TRANSLATION published parameter.
-  **XML CREATION & PUBLISHING:** Inserts processed data into a series of XML templates that are assembled into a single XML file for each data record, then published to PyCSW repository.  Outputs a copy of each XML file to a local folder and filters records that failed to publish.
For development/testing, the PyCSW repository can be bypassed to write XML to a local folder only by selecting the LOCAL_WRITER option in published parameters.
-  **METADATA OUTPUT:** Local repository locations to write XML files.  These can be used to validate XML files in the schematron.

-  **(p-t_abbreviation)_FGP-TBS_XML-JSON_BUILDER.fmw:**  These workspaces extract, transform and load a complete geospatial dataset to an empty Catalogue Service for the Web (CSW), as XML files for the FGP, and filter non-geospatial data output as JSON files for the TBS.  They also output error logs in .XLS format, to allow for updating of lookup table data, troubleshooting errors, or for information only. 

These workspaces are segmented into bookmarks,common to each workspace (exception for nongeospatial data), with each bookmark containing a series of transformers that may differ from workspace to workspace.  Each of these bookmarks represent a stage in the ETL process:

-  **ETL PROCESS INITIATION:** Starts the process and sets date/time for process reports.
-  **DATA EXTRACTION:** Reads the API and exposes required attributes.  Filters geo/non-geo data when attribute testing allows for selection.
-  **P/T SPECIFIC TRANSFORMATIONS:** Contains custom transformers that are specific to a province or territory due to the unique nature of the metadata and cannot be addressed with a universal transformer.
-  **PRE METADATA MAPPING TRANSFORMATIONS:** Contains universal custom transformers that require processing prior to metadata mapping.
-  **SPATIAL DATA TYPE MANAGEMENT:** Will perform one or more of the following tasks; Validates geospatial data and maps spatial data types.  Filters geo/non-geo data when it can’t be completed in the DATA EXTRACTION process. 
-  **PRE METADATA MAPPING TRANFORMATIONS - NONGEO:** Contains universal custom transformers that require processing prior to metadata mapping.
-  **METADATA MAPPING - NONGEO:** Contains universal custom transformers that utilize lookup tables to map data types to HNAP standards.
-  **POST METADATA MAPPING TRANSFORMATIONS - NONGEO:** Contains universal custom transformers to fine tune and customize metadata prior to publishing.
-  **METADATA MAPPING:** Contains universal custom transformers that utilize lookup tables to map data types to HNAP standards.
-  **POST METADATA MAPPING TRANSFORMATIONS:** Contains universal custom transformers to fine tune and customize metadata prior to publishing.
-  **PUBLISHING MANAGMENT:** Contains universal custom transformers that determine the URL of the PyCSW Repository, and compares existing repository data with the current run time data to identify records that are new, obsolete or updated.
-  **LANGUAGE_TRANSLATION:** Universal custom transformer that leverages the AWS translation service to translate specific data items to English or French as required.  Due to the fees required of the AWS, there is an option to bypass the translation service and enter proxy items in the required data fields for testing purposes by turning off the ACTIVATE_TRANSLATION published parameter.
-  **LANGUAGE_TRANSLATION - NONGEO:** Universal custom transformer that leverages the AWS translation service to translate specific data items to English or French as required.  Due to the fees required of the AWS, there is an option to bypass the translation service and enter proxy items in the required data fields for testing purposes by turning off the ACTIVATE_TRANSLATION published parameter.
-  **XML CREATION & PUBLISHING:** Inserts processed data into a series of XML templates that are assembled into a single XML file for each data record, then published to PyCSW repository.  Outputs a copy of each XML file to a local folder and filters records that failed to publish.
For development/testing, the PyCSW repository can be bypassed to write XML to a local folder only by selecting the LOCAL_WRITER option in published parameters.
-  **JSON CREATION:** Inserts processed data into a series of JSON templates that are assembled into a single JSON file for each data record, to be written to a local folder.
-  **METADATA OUTPUT:** Local repository locations to write XML files.  These can be used to validate XML files in the schematron.
-  **METADATA OUTPUT - NONGEO:** Local repository location to write JSON files.  

All FME Workspaces can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces)

A process flow chart showing the interconnectivity of the process can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/docs/P-T_FGP-TBS_XML-JSON_BUILDER_WORKSPACE_PROCESS_FLOW_STANDARD_v2.docx)

### Custom Transformers

The extensive transformers required for metadata ETL have been aggregated into a series of custom transformers, each defining a key step in the ETL process.  These transformers can be broken down into two types:

-  **Provincial/Territorial Specific Transformers:** These are exclusive to a provincial or territorial ETL process due to the unique nature of a data schema.
-  **Universal Transformers:** These contain processes that are universal to any workspace.

All FME custom transformers can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Custom_Transformers)

### XML Templates

The workspaces utilize eleven individual XML templates representing specific sections of an HNAP compliant document, that are bracketed by closing and ending tags,  that ultimately compile extracted data into a single document.  Ten of these are sub-templates that are inserted into specific locations of the main, or root, document.  Multiple instances of sub-templates can be inserted into the root document or other sub-templates to accommodate multiple instances of a metadata item. 

-   **GMD_CITEDRESPONSIBLEPARTY.xml:** This XML file is a sub-template and is framed by the **gmd:citedResponsibleParty** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
	- gmd:onlineResource
    - gmd:role

-   **GMD_CONTACT.xml:** This XML file is is a sub-template and is framed by the **gmd:contact** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
	- gmd:onlineResource
    - gmd:role

-   **GMD_DISTRIBUTIONFORMAT.xml:** This XML file is a sub-template and is framed by the **gmd:distributionFormat** tags.  Extracted data populates the following metadata item:
    - gmd:MD_Format
  
-   **GMD_DISTRIBUTOR.xml:** This XML file is a sub-template and is framed by the **gmd:distributor** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
	- gmd:onlineResource
    - gmd:role
  
-   **GMD_KEYWORDS.xml:** This XML file is a sub-template and is framed by the **gmd:keyword** tags.  Extracted data populates the following metadata item:
    - gmd:keyword
  
-   **GMD_MDMETADATA.xml:** This XML file is the root template and is framed by the **gmd:MD_Metadata** tags.  Extracted data populates the following metadata items:
    - gmd:fileIdentifier
    - GMD_CONTACT.xml sub-template
    - gmd:dateStamp (modified date)
    - gmd:metadataStandardVersion
    - GMD_REFERENCESYSTEMINFO.xml sub-template
    - gmd:title
    - gmd:date (publication date)
    - gmd:date (creation date)
    - GMD_CITEDRESPONSIBLEPARTY.xml sub-template
    - gmd:abstract
    - gmd:status
    - GMD_RESOURCEMAINTENANCE.xml sub-template
    - gmd:graphicOverview
    - GMD_KEYWORDS.xml sub-template
	- gmd:useLimitation
    - gmd:spatialRepresentationType
    - GMD_TOPICCATEGORY.xml sub-template
    - gmd:extent
      - gmd:temporalElement
	  - gmd:geographicElement
    - GMD_DISTRIBUTIONFORMAT.xml sub-template
    - GMD_DISTRIBUTOR.xml sub-template
    - GMD_TRANSFEROPTIONS.xml sub-template
  
-   **GMD_REFERENCESYSTEMINFO.xml:** This XML file is a sub-template and is framed by the **gmd:referenceSystemInfo** tags.  Extracted data populates the following metadata item:
    - gmd:referenceSystemInfo
  
-   **GMD_RESOURCEMAINTENANCE.xml:** This XML file is a sub-template and is framed by the **gmd:resourceMaintenance** tags.  Extracted data populates the following metadata item:
    - gmd:resourceMaintenance
  
-   **GMD_TOPICCATEGORY.xml:** This XML file is a sub-template and is framed by the **gmd:topicCategory** tags.  Extracted data populates the following metadata item:
    - gmd:topicCategory
  
-   **GMD_TRANSFEROPTIONS.xml:** This XML file is a sub-template and is framed by the **gmd:transferOptions** tags.  Extracted data populates the following metadata item:
    - gmd:linkage
    - gmd:protocol
    - gmd:name
    - gmd:description
  
All XML templates can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/XML_TEMPLATES)

## Workspaces

### Alberta (AB_FGP_XML_BUILDER)

#### Overview

ETL (extract, transformation and loading) workspace created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using two data sources:

-   **Alberta Open Data Catalogue**: Alberta ISO 19115 compliant data is extracted by exposing data from CKAN API [Alberta's Open Data Catalogue](https://open.alberta.ca/opendata), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. 

-  **Alberta Geodiscover Portal**:  A secondary data source is utilized to extract web map services (WMS) or ESRI REST services through XML files that are extracted from Alberta Open Data Catalogue.

Attributes required to meet mandatory requirements for individual XML (Extensible Markup Language) files are extracted from both the exposed JSON file and XML files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces use a series of custom transformers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  There is a placeholder for non-geo output but currently there is no processing for non-geo data.  Note that non-geo and geo filtering occurs at the DATA EXTRACTION bookmark.  

The Alberta Metadata FME Workspace can be found here:

-   [Alberta FME Workspace](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces/StandardizedWorkspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### AB_FGP_XML_BUILDER Contents

The AB_FGP_XML_BUILDER workspace utilizes the following sequence of bookmarks.  Custom transformer contents are indicated where they exist.

-   ETL PROCESS INITIATION
-   DATA EXTRACTION
    - Catalogue Reader
	- LICENSE_FILTER
	- DEFAULT_ATTRIBUTE_MAPPER
	- AB_DATA_READER
	- AB_GEODISCOVER_RESOURCE_EXTRACTOR
	- ATTRIBUTE_VALUE_TEXT_CLEANER
	- GEOPORTAL_WEBLINK_ADDER
-   P/T SPECIFIC TRANSFORMATIONS
    - AB_RESOURCES_FORMATTER
	- AB_MISSING_ATTRIBUTE_MANAGER
-   PRE METADATA MAPPING TRANSFORMATIONS
    - EMPTY_FORMAT_MAPPER
	- FORMAT_VALIDATOR
	- UPDATE_TO_PROGRESS_MAPPER
	- EMAIL_FORMAT_TESTER
-   SPATIAL_DATA_TYPE_MANAGEMENT
    - GEOSPATIAL_DATA_VALIDATOR
	- SPATIAL_TYPE_MAPPER
-   METADATA_MAPPING: The attribute value to be mapped is indicated
    - METADATA_VALUE_MAPPER_1: resource{}.name
	- METADATA_VALUE_MAPPER_2: resource_update_cycle
	- METADATA_VALUE_MAPPER_3: progress_code
	- METADATA_VALUE_MAPPER_4: spatial_representation_type
	- METADATA_VALUE_MAPPER_5: spatialref{}.projection_name
	- METADATA_VALUE_MAPPER_6: spatialref{}.projection_system
	- METADATA_VALUE_MAPPER_7: iso_topic{}.topic_value
	- METADATA_VALUE_MAPPER_8: contacts{}.country
	- METADATA_VALUE_MAPPER_9: contacts{}.email
	- METADATA_FORMAT_MAPPER: resources{}.format
	- METADATA_VALUE_MAPPER_ERROR_MANAGER
-   POST_METADATA_MAPPING_TRANSFORMATIONS
    - MORE_INFO_MANAGER
	- REMOVE_BROKEN_URL_WMS_ESRI_REST
	- DUPLICATE_SERVICE_REMOVER
	- GMD_SECTION_DATA_EXTRACTION
-   PUBLISHING MANAGEMENT
    - PYCSW_URL_MAPPER
	- METADATA_DELTA_FINDER
-   LANGUAGE TRANSLATION
    - AWS_TRANSLATE
-   XML_CREATION & PUBLISHING
    - XML_PUBLISHER
-   METADATA_OUTPUT

### British Columbia (BC_FGP_XML_BUILDER)

#### Overview

British Columbia open data is exposed through a CKAN API:

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation) file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  There is a placeholder for non-geo output but currently there is no processing for non-geo data.  Note that non-geo and geo filtering occurs at the DATA EXTRACTION bookmark.  

The British Columbia Metadata FME Workspace can be found here:

-   [British Columbia FME Workspace](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces/StandardizedWorkspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### BC_FGP_XML_BUILDER Contents

The BC_FGP_XML_BUILDER workspace utilizes the following sequence of bookmarks.  Custom transformer contents are indicated where they exist.

-   ETL PROCESS INITIATION
-   DATA EXTRACTION
    - Catalogue Reader
	- LICENSE_FILTER
	- DEFAULT_ATTRIBUTE_MAPPER
	- BC_DATA_READER
	- GEOPORTAL_WEBLINK_ADDER
-   P/T SPECIFIC TRANSFORMATIONS
    - BC_GEOWAREHOUSE_URL_BUILDER
	- BC_WMS_FORMATTER
	- BC_RESOURCE_NAME_CORRECTION
-   PRE METADATA MAPPING TRANSFORMATIONS
	- FORMAT_VALIDATOR
	- TOPIC_PARSER
-   SPATIAL_DATA_TYPE_MANAGEMENT
    - GEOSPATIAL_DATA_VALIDATOR
	- SPATIAL_TYPE_MAPPER
-   METADATA_MAPPING: The attribute value to be mapped is indicated
    - METADATA_VALUE_MAPPER_1: iso_topic{}.topic_value
	- METADATA_VALUE_MAPPER_2: contacts{}.role
	- METADATA_VALUE_MAPPER_3: resources{}resource_update_cycle
	- METADATA_VALUE_MAPPER_4: progress_code
	- METADATA_VALUE_MAPPER_5: spatial_representation_type
	- METADATA_VALUE_MAPPER_6: resources{}.projection_name
	- METADATA_FORMAT_MAPPER: resources{}.format
	- METADATA_VALUE_MAPPER_ERROR_MANAGER
-   POST_METADATA_MAPPING_TRANSFORMATIONS
    - EMAIL_FORMAT_TESTER
	- TEMPORAL_EXTENTS_MAPPER
	- RESOURCE_NAME_UNDERSCORE_REMOVER
	- MORE_INFO_MANAGER
	- REMOVE_BROKEN_URL_WMS_ESRI_REST
	- WMS_REST_LANGUAGE_FORMATTER
	- DUPLICATE_SERVICE_REMOVER
	- GMD_SECTION_DATA_EXTRACTION
	- URL_HTTPS_MAKER
-   PUBLISHING MANAGEMENT
    - PYCSW_URL_MAPPER
	- METADATA_DELTA_FINDER
-   LANGUAGE TRANSLATION
    - AWS_TRANSLATE
-   XML_CREATION & PUBLISHING
    - XML_PUBLISHER
-   METADATA_OUTPUT

### Manitoba

### New Brunswick

### Newfoundland and Labrador

### Nova Scotia

### Nunavut

### Ontario (ON_FGP-TBS_XML_JSON_BUILDER)

#### Overview

ETL (extract, transformation and loading) workspace created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using two data sources:

-   **Ontario Open Data Catalogue**: Ontario ISO 19115 compliant data is extracted by exposing data from CKAN API [Ontario's Open Data Catalogue](https://data.ontario.ca/en/api/3/action), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. 

-  **Ontario Geohub Portal**:  A secondary data source is utilized to extract web map services (WMS) or ESRI REST services through XML files that are extracted from Ontario Open Data Catalogue.

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation) file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  There is also a provision to process non-geo data for the TBS that outputs to a local folder. Note that non-geo and geo filtering occurs at the SPATIAL DATA TYPE MANAGEMENT bookmark.  

The Ontario Metadata FME Workspace can be found here:

-   [Ontario FME Workspace](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces/StandardizedWorkspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### ON_FGP-TBS_XML_JSON_BUILDER Contents

The ON_FGP-TBS_XML_JSON_BUILDER workspace utilizes the following sequence of bookmarks.  Custom transformer contents are indicated where they exist.

-   ETL PROCESS INITIATION
-   DATA EXTRACTION
    - Catalogue Reader
	- ATTRIBUTE_VALUE_TEXT_CLEANER
	- LICENSE_FILTER
	- ON_GEOHUB_RESOURCE_EXTRACTOR
	- DEFAULT_ATTRIBUTE_MAPPER
	- ON_DATA_READER
	- GEOPORTAL_WEBLINK_ADDER
-   P/T SPECIFIC TRANSFORMATIONS
    - ON_TRANSFER_LANG_MAPPER
	- ON_DATE_FORMATTER
-   PRE METADATA MAPPING TRANSFORMATIONS
	- RESOURCES_VALIDATOR
-   SPATIAL_DATA_TYPE_MANAGEMENT
    - GEOSPATIAL_DATA_VALIDATOR
	- SPATIAL_TYPE_MAPPER
	- MANUAL_GEOSPATIAL_SETTER
-   METADATA_MAPPING: The attribute value to be mapped is indicated
    - METADATA_VALUE_MAPPER_1: contacts{}.role
	- METADATA_VALUE_MAPPER_2: update_frequency
	- METADATA_VALUE_MAPPER_3: progress_code
	- METADATA_VALUE_MAPPER_4: spatial_representation_type
	- METADATA_FORMAT_MAPPER: resources{}.format
	- METADATA_VALUE_MAPPER_ERROR_MANAGER
-   POST METADATA MAPPING TRANSFORMATIONS
	- RESOURCE_NAME_UNDERSCORE_REMOVER
	- MORE_INFO_MANAGER
	- REMOVE_BROKEN_URL_WMS_ESRI_REST
	- WMS_REST_LANGUAGE_FORMATTER
	- DUPLICATE_SERVICE_REMOVER
	- GMD_SECTION_DATA_EXTRACTION
-   PRE METADATA MAPPING TRANSFORMATIONS - NONGEO
	- ON_DATE_FORMATTER
	- RESOURCES_VALIDATOR
-   METADATA_MAPPING - NONGEO
	- METADATA_VALUE_MAPPER_5: UpdateFrequency_TBS
	- METADATA_FORMAT_MAPPER_2: Format_TBS
	- METADATA_VALUE_MAPPER_ONE2MANY_1: TBS_Subject_temp{}.display_name
	- METADATA_VALUE_MAPPER_ONE2MANY_2: TBS_Topic_temp{}.display_name
	- METADATA_VALUE_MAPPER_ERROR_MANAGER_2
-   POST_METADATA_MAPPING_TRANSFORMATIONS - NONGEO
    - TBS_DEFAULT_KEYWORD_TOPIC_SUBJECT
	- RESOURCE_NAME_UNDERSCORE_REMOVER_2
-   PUBLISHING MANAGEMENT
    - PYCSW_URL_MAPPER
	- METADATA_DELTA_FINDER_1 (geospatial data)
	- METADATA_DELTA_FINDER_2 (non-geospatial data)
-   LANGUAGE TRANSLATION
    - AWS_TRANSLATE
-   XML_CREATION & PUBLISHING
    - XML_PUBLISHER
-   METADATA OUTPUT
-   LANGUAGE TRANSLATION - NONGEO
	- AWS_TRANLSATE_2: translates nongeo English to French resource{}.name
	- AWS_TRANSLATE_3: translates nongeo French to English resource{}.name
	- AWS_TRANSLATE_4: translates nongeo English to French notes, title and keyword attributes
-   JSON CREATION
	- JSON_PUBLISHER
-   METADATA OUTPUT - NONGEO

### Prince Edward Island

### Québec (QC_FGP-TBS_XML_JSON_BUILDER)

#### Overview

ETL (extract, transformation and loading) workspace created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from the following source:

-   **Québec Open Data Catalogue**: Québec ISO 19115 compliant data is extracted by exposing data from CKAN API [Québec's Open Data Catalogue](https://www.donneesquebec.ca/recherche/api/action), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. 

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation) file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  There is also a provision to process non-geo data for the TBS that outputs to a local folder. Note that non-geo and geo filtering occurs at the SPATIAL DATA TYPE MANAGEMENT bookmark.  

The Québec Metadata FME Workspace can be found here:

-   [Québec FME Workspace](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces/StandardizedWorkspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### QC_FGP-TBS_XML_JSON_BUILDER Contents

The QC_FGP-TBS_XML_JSON_BUILDER workspace utilizes the following sequence of bookmarks.  Custom transformer contents are indicated where they exist.

-   ETL PROCESS INITIATION
-   DATA EXTRACTION
    - Catalogue Reader
	- ATTRIBUTE_VALUE_TEXT_CLEANER
	- LICENSE_FILTER
	- DEFAULT_ATTRIBUTE_MAPPER
	- QC_DATA_READER
	- GEOPORTAL_WEBLINK_ADDER
-   P/T SPECIFIC TRANSFORMATIONS
  	- QC_DATE_FORMATTER
	- QC_SECTOR_MAPPER_AND_FILTER
	- QC_PROJECTION_GEOEXTENTS_EXTRACTOR
-   PRE METADATA MAPPING TRANSFORMATIONS
	- GEO_EXTENTS_MAPPER
	- RESOURCES_VALIDATOR
	- FORMAT_VALIDATOR
	- EMAIL_FORMAT_TESTER
-   SPATIAL_DATA_TYPE_MANAGEMENT
    - GEOSPATIAL_DATA_VALIDATOR
	- SPATIAL_TYPE_MAPPER
-   METADATA_MAPPING: The attribute value to be mapped is indicated
    - METADATA_VALUE_MAPPER_1: update_frequency
	- METADATA_VALUE_MAPPER_2: progress_code
	- METADATA_VALUE_MAPPER_3: spatial_representation_type
	- METADATA_FORMAT_MAPPER: resources{}.format
	- METADATA_VALUE_MAPPER_ERROR_MANAGER
-   POST METADATA MAPPING TRANSFORMATIONS
	- QC_WMS_URL_SETTER
	- RESOURCE_NAME_UNDERSCORE_REMOVER
	- MORE_INFO_MANAGER
	- REMOVE_BROKEN_URL_WMS_ESRI_REST
	- WMS_REST_LANGUAGE_FORMATTER
	- DUPLICATE_SERVICE_REMOVER
	- GMD_SECTION_DATA_EXTRACTION
	- URL_CHARACTER_ENCODER
	- MAP_RESOURCE_ATTRIBUTE_REMOVER
-   TRANSFORMATIONS - NONGEO
	- QC_TBS_ATTRIBUTE_VALUE_MAPPER
-   PUBLISHING MANAGEMENT
    - PYCSW_URL_MAPPER
	- METADATA_DELTA_FINDER_1 (geospatial data)
	- METADATA_DELTA_FINDER_2 (non-geospatial data)
-   LANGUAGE TRANSLATION
    - AWS_TRANSLATE
-   XML CREATION & PUBLISHING
    - XML_PUBLISHER
-   METADATA_OUTPUT
-   JSON CREATION
	- JSON_PUBLISHER
-   METADATA_OUTPUT - NONGEO

### Saskatchewan

### Yukon (YT_FGP_XML_BUILDER)

#### Overview

ETL (extract, transformation and loading) workspace created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using three data sources:

-   **Yukon Open Data Catalogue**: Alberta ISO 19115 compliant data is extracted by exposing data from DKAN API [Yukon's Open Data Catalogue](https://open.yukon.ca/api/3/action), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. 

-  **Yukon Geology Portal**:  A secondary data source is utilized to extract geological spatial data.

-  **Yukon Geoweb Portal**:  A secondary data source is utilized to extract addtional spatial data.

Attributes required to meet mandatory requirements for individual XML (Extensible Markup Language) files are extracted from both the exposed JSON file and XML files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces use a series of custom transformers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  There is a placeholder for non-geo output but currently there is no processing for non-geo data.  Note that non-geo and geo filtering occurs at the DATA EXTRACTION bookmark.  The intitial catalogue extraction from the DKAN portal, where other workspaces use the universal Catalogue_Reader transformer, utilizes the YT_CATALOGUE_READER due to the unique nature of the Yukon API.

The Yukon Metadata FME Workspace can be found here:

-   [Yukon FME Workspace](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces/StandardizedWorkspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### YT_FGP_XML_BUILDER Contents

The YT_FGP_XML_BUILDER workspace utilizes the following sequence of bookmarks.  Custom transformer contents are indicated where they exist.

-   ETL PROCESS INITIATION
-   DATA EXTRACTION
    - YT_CATALOGUE_READER
	- LICENSE_FILTER
	- DEFAULT_ATTRIBUTE_MAPPER
	- YT_DATA_READER
	- YT_GEOLOGY_DATA_EXTRACTOR
	- YT_GEOWEB_EXTRACTOR
	- GEOPORTAL_WEBLINK_ADDER
-   P/T SPECIFIC TRANSFORMATIONS
    - YT_DATE_FORMATTER
	- YT_MISSING_ATTRIBUTE_MANAGER
	- YT_CONTACTS_MERGER
-   PRE METADATA MAPPING TRANSFORMATIONS
    - EMPTY_FORMAT_MAPPER
	- URL_HTTPS_MAKER
	- FORMAT_VALIDATOR
	- EMAIL_FORMAT_TESTER
-   SPATIAL_DATA_TYPE_MANAGEMENT
    - GEOSPATIAL_DATA_VALIDATOR
	- SPATIAL_TYPE_MAPPER
	- MANUAL_GEOSPATIAL_SETTER
-   METADATA_MAPPING: The attribute value to be mapped is indicated
    - METADATA_VALUE_MAPPER_1: contacts{}.role
	- METADATA_VALUE_MAPPER_2: spatial_representation_type
	- METADATA_VALUE_MAPPER_3: progress_code
	- METADATA_VALUE_MAPPER_4: spatialref_projection_name
	- METADATA_VALUE_MAPPER_5: resource_update_cycle
	- METADATA_VALUE_MAPPER_6: contacts{}.email
	- METADATA_FORMAT_MAPPER: resources{}.format
	- METADATA_VALUE_MAPPER_ERROR_MANAGER
-   POST_METADATA_MAPPING_TRANSFORMATIONS
    - RESOURCE_NAME_UNDERSCORE_REMOVER
	- MORE_INFO_MANAGER
	- REMOVE_BROKEN_URL_WMS_ESRI_REST
	- WMS_REST_LANGUAGE_FORMATTER
	- DUPLICATE_SERVICE_REMOVER
	- AMPERSAND_CHARACTER_REFERENCE_REMOVER
	- GMD_SECTION_DATA_EXTRACTION
-   PUBLISHING MANAGEMENT
    - PYCSW_URL_MAPPER
	- METADATA_DELTA_FINDER
-   LANGUAGE TRANSLATION
    - AWS_TRANSLATE
-   XML_CREATION & PUBLISHING
    - XML_PUBLISHER
-   METADATA_OUTPUT

## Custom Transformers Detail

-   AB_DATA_READER
-   AB_GEODISCOVER_RESOURCE 
-   AB_GEODISCOVER_RESOURCE_EXTRACTOR
-   AB_MISSING_ATTRIBUTE_MANAGER
-   AMPERSAND_CHARACTER_REFERENCE_REMOVER
-   ATTRIBUTE_VALUE_TEXT_CLEANER
-   AWS_TRANSLATE
-   BC_DATA_READER
-   BC_GEOWAREHOUSE_URL_BUILDER
-   BC_RESOURCE_NAME_CORRECTION
-   BC_WMS_FORMATTER
-   Catalogue_Reader
-   DEFAULT_ATTRIBUTE_MAPPER
-   DUPLICATE_SERVICE_REMOVER
-   EMAIL_FORMAT_TESTER
-   EMPTY_FORMAT_MAPPER
-   FORMAT_VALIDATOR
-   GEO_EXTENTS_MAPPER
-   GEOPORTAL_WEBLINK_ADDER
-   GEOSPATIAL_DATA_VALIDATOR
-   GMD_SECTION_DATA_EXTRACTION
-   JSON_PUBLISHER
-   LICENSE_FILTER
-   LOOKUP_TABLES_READER
-   MANUAL_GEOSPATIAL_SETTER
-   MAP_RESOURCE_ATTRIBUTION_REMOVER
-   METADATA_DELTA_FINDER
-   METADATA_VALUE_MAPPER_ERROR_MANAGER
-   METADATA_VALUE_MAPPER_ONE2MANY
-   MORE_INFO_MANAGER
-   NB_ADVANCED_VIEW_RESOURCE_MAPPER
-   NB_AttachementManager
-   NB_ATTRIBUTE_MANAGER
-   NB_BoundingBoxExtractor
-   NB_ESRIMAPPER
-   NB_FRENCH_TAG_SEPARATOR
-   NB_FrenchEnglishTitlesDescSeparator
-   NB_HrefResourcesExtractor
-	NB_ISOTOPIC_ASSIGNER
-   NB_MetadataMerger
-   NB_ORGANZATION_MAPPER
-   NB_RESOURCE_TYPE_FILTER
-   NB_TAGS_MANAGER
-   ON_DATA_READER
-   ON_DATE_FORMATTER
-   ON_GEOHUB_RESOURCE_EXTRACTOR
-   ON_KEYWORD_RENAMER
-   ON_TRANSFER_LANG_MAPPER
-   PYCSW_URL_MAPPER
-   QC_ATTRIBUTE_MAPPER
-   QC_DATA_READER
-   QC_DATE_FORMATTER
-   QC_MISSING_EMAIL_SETTER
-   QC_PROJECTION_GEOEXTENTS_EXTRACTOR
-   QC_SECTOR_MAPPER_AND_FILTER
-   QC_TBS_ATTRIBUTE_VALUE_MAPPER
-   QC_WMS_URL_SETTER
-   REVOVE_BROKEN_URL_WMS_ESRI_REST
-   RESOURCE_NAME_UNDERSCORE_REMOVER
-   RESOURCES_VALIDATOR
-   SOCRATA_READER
-   SOCRATA_RESOURCE_MAPPER
-   SocrataAPICaller
-   SocrataDateTimeConverter
-   SocrataHashIDGenerator
-   SocrataReader
-   SPATIAL_TYPE_MAPPER
-   TBS_DEFAULT_KEYWORD_TOPIC_SUBJECT
-   TEMPORAT_EXTENTS_MAPPER
-   TOPIC_PARSER
-   UNIQUE_ID_GENERATOR
-   UPDATE_TO_PROGRESS_MAPPER
-   URL_CHARACTER_ENCODER
-   URL_HTTPS_MAKER
-   UUID_4_FORMATTER
-   WMS_REST_LANGUAGE_FORMATTER
-   XML_PUBLISHER
-   YT_CATALOGUE_READER
-   YT_CONTACTS_MERGER
-   YT_DATA_READEER
-   YT_DATE_FORMATTER
-   YT_GEOLOGY_DATA_EXTRACTOR
-   YT_GEOWEB_EXTRACTOR
-   YT_MISSING_ATTRIBUTE_MANAGER
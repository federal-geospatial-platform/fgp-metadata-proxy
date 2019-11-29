
Provincial and Territorial Extraction, Transformation and Loading Processes
==========

- [Table of Contents](#table-of-contents)
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes)
  - [Overview](#overview)
    - [Workspaces](#workspaces)
	- [Custom Transformers](#custom-transformers)
	- [XML Templates](#xml-templates)
	- [Other PyCSW Tools](#other-pycsw-tools)
  - [Workspaces](#workspaces-1)
  - [Alberta](#alberta)
    - [Overview](#overview-1)
    - [AB_CREATE Workspace Detail](#ab_create-workspace-detail)
	  - [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate)
	  - [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper)
      - [AB_MISSING_ATTRIBUTE_MAPPER](#ab_missing_attribute_mapper)
	  - [AB_WMS_FORMATTER](#ab_wms_formatter)
	  - [AWS_TRANSLATE](#aws_translate)
	  - [AB_TRANSLATION_CORRECTION](#ab_translation_correction)
      - [TEMPORAL_EXTENTS_MAPPER](#temporal_extents_mapper)
	  - [AB_RESOURCE_LIST_MANAGER](#ab_resource_list_manager)
	  - [METADATA_VALUE_MAPPER](#metadata_value_mapper)
	  - [METADATA_FORMAT_MAPPER](#metadata_format_mapper)
      - [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator)
	  - [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction)
	  - [MORE_INFO_MAPPER](#more_info_mapper)
	  - [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest)
      - [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter)
      - [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover)
      - [XML_PUBLISHER](#xml_publisher)
	  - [NOTIFY_CREATE](#notify_create)
	- [AB_UPDATE Workspace Detail](#ab_update-workspace-detail)
	  - [AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate)
	  - [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-1)
      - [AB_MISSING_ATTRIBUTE_MAPPER](#ab_missing_attribute_mapper-1)
	  - [AB_WMS_FORMATTER](#ab_wms_formatter-1)
	  - [AWS_TRANSLATE](#aws_translate-1)
	  - [AB_TRANSLATION_CORRECTION](#ab_translation_correction-1)
      - [TEMPORAL_EXTENTS_MAPPER](#temporal_extents_mapper-1)
	  - [AB_RESOURCE_LIST_MANAGER](#ab_resource_list_manager-1)
	  - [METADATA_VALUE_MAPPER](#metadata_value_mapper-1)
	  - [METADATA_FORMAT_MAPPER](#metadata_format_mapper-1)
      - [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-1)
	  - [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-1)
	  - [MORE_INFO_MAPPER](#more_info_mapper-1)
	  - [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-1)
      - [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-1)
      - [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-1)
      - [XML_PUBLISHER](#xml_publisher-1)
	  - [NOTIFY_UPDATE](#notify_update)
  - [British Columbia](#british-columbia)
    - [Overview](#overview-2) 
	- [BC_CREATE Workspace Detail](#bc_create-workspace-detail)
	  - [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate)
	  - [BC_GEOWAREHOUSE_URL_BUILDER](#bc_geowarehouse_url_builder)
	  - [BC_WMS_FORMATTER](#bc_wms_formatter)
	  - [BC_RESOURCE_NAME_CORRECTION](#bc_resource_name_correction)
	  - [AWS_TRANSLATE](#aws_translate-2)
	  - [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-2)
	  - [TOPIC_PARSER](#topic_parser)
	  - [METADATA_VALUE_MAPPER](#metadata_value_mapper-2)
	  - [METADATA_FORMAT_MAPPER](#metadata_format_mapper-2)
	  - [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-2)
	  - [MORE_INFO_MANAGER](#more_info_manager-2)
	  - [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-2)
	  - [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-2)
	  - [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-2)
	  - [XML_PUBLISHER](#xml_publisher-2)
	  - [NOTIFY_CREATE](#notify_create-1)
	- [BC_UPDATE Workspace Detail](#bc_update-workspace-detail)
	  - [BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate)
	  - [BC_GEOWAREHOUSE_URL_BUILDER](#bc_geowarehouse_url_builder-1)
	  - [BC_WMS_FORMATTER](#bc_wms_formatter-1)
	  - [BC_RESOURCE_NAME_CORRECTION](#bc_resource_name_correction-1)
	  - [AWS_TRANSLATE](#aws_translate-3)
	  - [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-3)
	  - [TOPIC_PARSER](#topic_parser-1)
	  - [METADATA_VALUE_MAPPER](#metadata_value_mapper-3)
	  - [METADATA_FORMAT_MAPPER](#metadata_format_mapper-3)
	  - [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-3)
	  - [MORE_INFO_MANAGER](#more_info_manager-3)
	  - [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-3)
	  - [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-3)
	  - [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-3)
	  - [XML_PUBLISHER](#xml_publisher-3)
	  - [NOTIFY_UPDATE](#notify_update-1)
  - [Manitoba](#manitoba)
  - [New Brunswick](#new-brunswick)
  - [Newfoundland and Labrador](#newfoundland-and-labrador)
  - [Nova Scotia](#nova-scotia)
  - [Nunavut](#nunavut)
  - [Ontario](#ontario)
  - [Prince Edward Island](#prince-edward-island)
  - [Québec](#québec)
  - [Saskatchewan](#saskatchewan)
  - [Yukon](#yukon)
  - [Custom Transformers Detail](#custom-transformers-detail)
    - [Universal Transformers](#universal-transformers)
	  - [AWS_TRANSLATE](#aws_translate-4)
	  - [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-4)
	  - [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-4)
	  - [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-4)
	  - [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-4)
	  - [METADATA_FORMAT_MAPPER](#metadata_format_mapper-4)
	  - [METADATA_VALUE_MAPPER](#metadata_value_mapper-4)
	  - [MORE_INFO_MANAGER](#more_info_manager-4)
      - [NOTIFY_CREATE](#notify_create-2)
      - [NOTIFY_UPDATE](#notify_update-2)	
      - [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-4)
	  - [TEMPORAL_EXTENTS_MAPPER](#temporal_extents_mapper-4)
	  - [TOPIC_PARSER](#topic_parser-2)
	  - [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-4)
	  - [XML_PUBLISHER](#xml_publisher-4)
    - [Provincial and Territorial Specific Transformers](#provincial-and-territorial-specific-transformers)
	  - [Alberta](#alberta-1)
	    - [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate-1)
        - [AB_MISSING_ATTRIBUTE_MAPPER](#ab_missing_attribute_mapper-2)
        - [AB_TRANSLATION_CORRECTION](#ab_translation_correction-2)
		- [AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate-1)
		- [AB_WMS_FORMATTER](#ab_wms_formatter-2)
	  - [British Columbia](#british-columbia-1)
	    - [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate-1)
        - [BC_GEOWAREHOUSE_URL_BUILDER](#bc_geowarehouse_url_builder-2)
        - [BC_RESOURCE_NAME_CORRECTION](#bc_resource_name_correction-2)
		- [BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate-1)
        - [BC_WMS_FORMATTER](#bc_wms_formatter-2)		
   
# Provincial and Territorial Extraction, Transformation and Loading Processes

## Overview

### Workspaces

Open data extraction, transformation and loading processes utilize two different FME Workspaces for each Canadian province or territory:

-   **(p-t_abbreviation_)__CREATE__(_version_number).fmw:** The CREATE workspaces are for extracting, transforming and loading a complete dataset to an empty Catalogue Service for the Web (CSW).  Its intended use is for initial creation of a CSW, or in the event an entire CSW needs to be reloaded.  This can be run manually from FME Server.
-  **(p-t_abbreviation_)__UPDATE__(_version_number).fmw:**  The UPDATE workspaces filter, extract, transform and load new or updated data records to the CSW.  It also reads all existing data records already in the CSW and deletes any records no longer found in the source data.  These workspaces run on a daily schedule on the FME Server.

All FME Workspaces can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces)

### Custom Transformers

The extensive transformers required for metadata ETL have been aggregated into a series of custom transformers, each defining a key step in the ETL process.  These transformers can be broken down into three types:

-   **Workspace Exclusive Transformers:** These are exclusive to either a single provincial/territorial CREATE or UPDATE workspace.
-  **Provincial/Territorial Exclusive Transformers:** These are exclusive to a provincial or territorial ETL process, but can be used in that province/territory's CREATE or UPDATE transformers.
-  **Universal Transformers:** These contain processes that are universal to any workspace.

All FME custom transformers can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Custom_Transformers)

### XML Templates

The workspaces utilize eleven individual XML templates representing specific sections of an HNAP compliant document, that are bracketed by closing and ending tags,  that ultimately compile extracted data into a single document.  Ten of these are sub-templates that are inserted into specific locations of the main, or root, document.  Multiple instances of sub-templates can be inserted into the root document or other sub-templates to accommodate multiple instances of a metadata item. 

-   **GMD_CITEDRESPONSIBLEPARTY.xml:** This XML file is a sub-template and is framed by the **gmd:citedResponsibleParty** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
    - gmd:role
    - GMD_ONLINE_RESOURCES.xml sub-template

-   **GMD_CONTACT.xml:** This XML file is is a sub-template and is framed by the **gmd:contact** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
    - gmd:role
    - GMD_ONLINE_RESOURCES.xml sub-template

-   **GMD_DISTRIBUTIONFORMAT.xml:** This XML file is a sub-template and is framed by the **gmd:distributionFormat** tags.  Extracted data populates the following metadata item:
    - gmd:MD_Format
  
-   **GMD_DISTRIBUTOR.xml:** This XML file is a sub-template and is framed by the **gmd:distributor** tags.  Extracted data populates the following metadata items:
    - gmd:individualName
    - gmd:organisationName
    - gmd:positionName
    - gmd:contactInfo
    - gmd:role
    - GMD_ONLINE_RESOURCES.xml sub-template
  
-   **GMD_KEYWORDS.xml:** This XML file is a sub-template and is framed by the **gmd:keyword** tags.  Extracted data populates the following metadata item:
    - gmd:keyword
  
-   **GMD_MDMETADATA.xml:** This XML file is the root template and is framed by the **gmd:MD_Metadata** tags.  Extracted data populates the following metadata items:
    - gmd:fileIdentifier
    - GMD_CONTACT.xml sub-template
    - gmd:timeStamp
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
    - gmd:spatialRepresentationType
    - GMD_TOPICCATEGORY.xml sub-template
    - gmd:extent
      - gmd:temporalElement
	  - gmd:geographicElement
    - GMD_DISTRIBUTIONFORMAT.xml sub-template
    - GMD_DISTRIBUTOR.xml sub-template
    - GMD_TRANSFEROPTIONS.xml sub-template
  
-   **GMD_ONLINERESOURCE.xml:** This XML file is a sub-template and is framed by the **gmd:onlineResource** tags.  Extracted data populates the following metadata item:
    - gmd:onlineResource
  
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

### Other PyCSW Tools

-   **EMPTY CSW Python Scripts:** These are intended for admin purposes only in the event a CSW has to be cleared of all data.  These scripts run manually and must be executed prior to running a CREATE workspace.  It will clear 1000 records at a time from the CSW and will have to be run multiple times if the CSW count exceeds 1000.

All EMPTY CSW Python scripts can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/scripts/Empty_PyCSW_Scripts)

## Workspaces

### Alberta

#### Overview

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using two approaches:

-   **Alberta Open Data Catalogue**: Alberta ISO 19115 compliant data is extracted by exposing data from CKAN API [Alberta's Open Data Catalogue](https://open.alberta.ca/opendata), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. The approach going through the Open Data Catalog first is required as the unique ID's from the Open Data are required due to inconsistencies in the unique ID's used in the subsequently exposed XML files.

-  **Alberta Geospatial Catalog**:  A small amount of ISO 19139 compliant data using exclusively ESRI REST services is unavailable in the Alberta Open Data Catalog and is exposed directly from [Alberta Geospatial Catalogue](https://geodiscover.alberta.ca/geoportal).  The unique ID naming conventions are accurate with this data subset that allows for direct extraction.  The remainder of ISO 19139 data not exposing ESRI REST services that is found in the Alberta geospatial catalogue has been found to be largely incomplete and unusable.  

Attributes required to meet mandatory requirements for individual XML (Extensible Markup Language) files are extracted from both the exposed JSON file and XML files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces use a series of custom transformers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key-v2.xlsx)

The Alberta Metadata FME Workspaces can be found here:

-   [Alberta FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### AB_CREATE Workspace Detail

The AB_CREATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate-1)

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-4)

Sets default attribute values specific to AB data that are universal to every data record.

##### [AB_MISSING_ATTRIBUTE_MAPPER](#ab_missing_attribute_mapper-2)

Adds default values to missing values.  

##### [AB_WMS_FORMATTER](#ab_wms_formatter-2)

Creates MapViewer compliant WMS url's.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [AB_TRANSLATION_CORRECTION](#ab_translation_correction-2)

Corrects common GIS terms found in resources{}.name attributes that have been literally translated to incorrect French values in the AWS Translate tool and reverts them back to their correct GIS terms.

##### [TEMPORAL_EXTENTS_MAPPER](#temporal_extents_mapper-4)

Formats and maps data collection start and end dates.  Sets start dates to 0001-01-01 and end dates to no value where missing.

##### [AB_RESOURCE_LIST_MANAGER](#ab_resource_list_manager-2)

Tests if the dataset resources{} list items have values for name, url and format and if not, the item is filtered out due to insufficient information for publishing. 

##### [METADATA_VALUE_MAPPER](#metadata_value_mapper-4)

There are multiple instances of the METADATA_VALUE_MAPPER in the workspace to correct values to valid English values and to add the valid French equivalents and RI_CODES where applicable.  It can be utilized for multiple metadata items by accessing custom look up tables applicable to specific items.  The multiple instances of the tool are mapped to the following individual look-up tables:

  - Codespace
  - Keyword
  - ProgressStatusAttributeMapper
  - RoleAttributeMapper
  - SpatialReferenceMapper
  - SpatialRepresentationAttributeMapper
  - UpdateCycleAttributeMapper

##### [METADATA_FORMAT_MAPPER](#metadata_format_mapper-4)

The METADATA_FORMAT_MAPPER corrects known incorrect variations of data format values to HNAP compliant format values, and adds the correct English and French Resource Type values by accessing the FormatAttributeMapper lookup table.

##### [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-4)

Creates an FFS file of data item values that cannot be mapped to a valid value due to undocumented data entry errors missing from the look-up table.  

##### [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-4)

Creates lists and removes duplicates for distribution formats, projections, update cycles and more_info.

##### [MORE_INFO_MAPPER](#more_info_mapper-4)

Tests the more_info{}.link list for valid attribute values and filters them out where missing.

##### [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-4)

Tests WMS/ESRI_REST resource URL's and removes them where broken.

##### [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-4)

Formats WMS and ESRI REST resources to add French versions and formats French and English versions with valid supporting attributes.

##### [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-4)

Removes duplicate WMS or ESRI REST resources where they exist, that would otherwise invalidate the dataset.

##### [XML_PUBLISHER](#xml_publisher-4)

Extracts and maps attributes to values required by the XML root template or sub-templates, compiles the templates to a single XML file, and publishes the XML to the PyCSW, or to a local folder.

##### [NOTIFY_CREATE](#notify_create-2)

E-mails processing results to administrator.

#### AB_UPDATE Workspace Detail

The AB_UPDATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate-1)

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against Alberta API's for obsolete data.  Deletes records from CSW that are no longer found in Alberta open data.  

##### [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-4)

Sets default attribute values specific to AB data that are universal to every data record.

##### [AB_MISSING_ATTRIBUTE_MAPPER](#ab_missing_attribute_mapper-2)

Adds default values to missing values.  

##### [AB_WMS_FORMATTER](#ab_wms_formatter-2)

Creates MapViewer compliant WMS url's.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [AB_TRANSLATION_CORRECTION](#ab_translation_correction-2)

Corrects common GIS terms found in resources{}.name attributes that have been literally translated to incorrect French values in the AWS Translate tool and reverts them back to their correct GIS terms.

##### [TEMPORAL_EXTENTS_MAPPER](#temporal_extents_mapper-4)

Formats and maps data collection start and end dates.  Sets start dates to 0001-01-01 and end dates to no value where missing.

##### [AB_RESOURCE_LIST_MANAGER](#ab_resource_list_manager-2)

Tests if the dataset resources{} list items have values for name, url and format and if not, the item is filtered out due to insufficient information for publishing. 

##### [METADATA_VALUE_MAPPER](#metadata_value_mapper-4)

There are multiple instances of the METADATA_VALUE_MAPPER in the workspace to correct values to valid English values and to add the valid French equivalents and RI_CODES where applicable.  It can be utilized for multiple metadata items by accessing custom look up tables applicable to specific items.  The multiple instances of the tool are mapped to the following individual look-up tables:

  - Codespace
  - Keyword
  - ProgressStatusAttributeMapper
  - RoleAttributeMapper
  - SpatialReferenceMapper
  - SpatialRepresentationAttributeMapper
  - UpdateCycleAttributeMapper

##### [METADATA_FORMAT_MAPPER](#metadata_format_mapper-4)

The METADATA_FORMAT_MAPPER corrects known incorrect variations of data format values to HNAP compliant format values, and adds the correct English and French Resource Type values by accessing the FormatAttributeMapper lookup table.

##### [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-4)

Creates an FFS file of data item values that cannot be mapped in the METADATA_FORMAT_MAPPER or METADATA_VALUE_MAPPER to a valid value due to undocumented data entry errors missing from the look-up table. 

##### [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-4)

Creates lists and removes duplicates for distribution formats, projections, update cycles and more_info.

##### [MORE_INFO_MAPPER](#more_info_mapper-4)

Tests the more_info{}.link list for valid attribute values and filters them out where missing.

##### [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-4)

Tests WMS/ESRI_REST resource URL's and removes them where broken.

##### [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-4)

Formats WMS and ESRI REST resources to add French versions and formats French and English versions with valid supporting attributes.

##### [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-4)

Removes duplicate WMS or ESRI REST resources where they exist, that would otherwise invalidate the dataset.

##### [XML_PUBLISHER](#xml_publisher-4)

Extracts and maps attributes to values required by the XML root template or sub-templates, compiles the templates to a single XML file, and publishes the XML to the PyCSW, or to a local folder.

##### [NOTIFY_UPDATE](#notify_update-2)

E-mails processing results to administrator.

### British Columbia

#### Overview

British Columbia open data is exposed through a CKAN API:

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation) file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key-v2.xlsx)

The British Columbia Metadata FME Workspaces can be found here:

-   [British Columbia FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_files/FME_Workspaces)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### BC_CREATE Workspace Detail

The BC_CREATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate-1)

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### [BC_GEOWAREHOUSE_URL_BUILDER](#bc_geowarehouse_url_builder-2)

Builds URL for BC Geowarehouse download links that are not readily available in the BC API but can be concatenated from other existing data.

##### [BC_WMS_FORMATTER](#bc_wms_formatter-2)

Builds URL for WMS links that are not readily available in the required French/English formats in the BC API but can be concatenated from other existing data.

##### [BC_RESOURCE_NAME_CORRECTION](#bc_resource_name_correction-2)

Substitutes resource name with dataset title when resource name is missing.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-4)

Sets default attibute values specific to BC data that are universal to every data record.

##### [TEMPORAL_EXTENTS_MAPPER](temporal_extents_mapper_4)

Formats and maps data collection start and end dates.  Sets start dates to 0001-01-01 and end dates to no value where missing.

##### [TOPIC_PARSER](#topic-parser-2)

Parses topics into individual attributes when multiple topics appear as comma separated values.

##### [METADATA_VALUE_MAPPER](#metadata_value_mapper-4)

There are multiple instances of the METADATA_VALUE_MAPPER in the workspace to correct values to valid English values and to add the valid French equivalents and RI_CODES where applicable.  It can be utilized for multiple metadata items by accessing custom look up tables applicable to specific items.  The multiple instances of the tool are mapped to the following individual look-up tables:

  - Keyword
  - ProgressStatusAttributeMapper
  - RoleAttributeMapper
  - SpatialReferenceMapper
  - SpatialRepresentationAttributeMapper
  - UpdateCycleAttributeMapper
  
##### [METADATA_FORMAT_MAPPER](#metadata_format_mapper-4)

The METADATA_FORMAT_MAPPER corrects known incorrect variations of data format values to HNAP compliant format values, and adds the correct English and French Resource Type values by accessing the FormatAttributeMapper lookup table.

##### [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-4)

Creates an FFS file of data item values that cannot be mapped in the METADATA_FORMAT_MAPPER or METADATA_VALUE_MAPPER to a valid value due to undocumented data entry errors missing from the look-up table. 

##### [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-4)

Creates lists and removes duplicates for distribution formats, projections, update cycles and more_info.

##### [MORE_INFO_MANAGER](#more_info_manager-4)

Tests the more_info{}.link list for valid attribute values and filters them out where missing.

##### [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-4)

Tests WMS/ESRI_REST resource URL's and removes them where broken.

##### [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-4)

Formats WMS and ESRI REST resources to add French versions and formats French and English versions with valid supporting attributes.

##### [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-4)

Removes duplicate WMS or ESRI REST resources where they exist, that would otherwise invalidate the dataset.

##### [XML_PUBLISHER](#xml_publisher-4)

Extracts and maps attributes to values required by the XML root template or sub-templates, compiles the templates to a single XML file, and publishes the XML to the PyCSW, or to a local folder.

##### [NOTIFY_CREATE](#notify_create-2)

E-mails processing results to administrator.

#### BC_UPDATE Workspace Detail

The BC_UPDATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate-1)

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against British Columbia's API for obsolete data.  Deletes records from CSW that are no longer found in British Columbia open data.  

##### [BC_GEOWAREHOUSE_URL_BUILDER](#bc_geowarehouse_url_builder-2)

Builds URL for BC Geowarehouse download links that are not readily available in the BC API but can be concatenated from other existing data.

##### [BC_WMS_FORMATTER](#bc_wms_formatter-2)

Builds URL for WMS links that are not readily available in the required French/English formats in the BC API but can be concatenated from other existing data.

##### [BC_RESOURCE_NAME_CORRECTION](#bc_resource_name_correction-1)

Substitutes resource name with dataset title when resource name is missing.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [DEFAULT_ATTRIBUTE_MAPPER](#default_attribute_mapper-4)

Sets default attribute values specific to BC data that are universal to every data record.

##### [TEMPORAL_EXTENTS_MAPPER](temporal_extents_mapper_4)

Formats and maps data collection start and end dates.  Sets start dates to 0001-01-01 and end dates to no value where missing.

##### [TOPIC_PARSER](#topic-parser-2)

Parses topics into individual attributes when multiple topics appear as comma separated values.

##### [METADATA_VALUE_MAPPER](#metadata_value_mapper-4)

There are multiple instances of the METADATA_VALUE_MAPPER in the workspace to correct values to valid English values and to add the valid French equivalents and RI_CODES where applicable.  It can be utilized for multiple metadata items by accessing custom look up tables applicable to specific items.  The multiple instances of the tool are mapped to the following individual look-up tables:

  - Keyword
  - ProgressStatusAttributeMapper
  - RoleAttributeMapper
  - SpatialReferenceMapper
  - SpatialRepresentationAttributeMapper
  - UpdateCycleAttributeMapper
  
##### [METADATA_FORMAT_MAPPER](#metadata_format_mapper-4)

The METADATA_FORMAT_MAPPER corrects known incorrect variations of data format values to HNAP compliant format values, and adds the correct English and French Resource Type values by accessing the FormatAttributeMapper lookup table.

##### [MAPPING_ERROR_LIST_CREATOR](#mapping_error_list_creator-4)

Creates an FFS file of data item values that cannot be mapped in the METADATA_FORMAT_MAPPER or METADATA_VALUE_MAPPER to a valid value due to undocumented data entry errors missing from the look-up table. 

##### [GMD_SECTION_DATA_EXTRACTION](#gmd_section_data_extraction-4)

Creates lists and removes duplicates for distribution formats, projections, update cycles and more_info.

##### [MORE_INFO_MANAGER](#more_info_manager-4)

Tests the more_info{}.link list for valid attribute values and filters them out where missing.

##### [REMOVE_BROKEN_URL_WMS_ESRI_REST](#remove_broken_url_wms_esri_rest-4)

Tests WMS/ESRI_REST resource URL's and removes them where broken.

##### [WMS_REST_LANGUAGE_FORMATTER](#wms_rest_language_formatter-4)

Formats WMS and ESRI REST resources to add French versions and formats French and English versions with valid supporting attributes.

##### [DUPLICATE_SERVICE_REMOVER](#duplicate_service_remover-4)

Removes duplicate WMS or ESRI REST resources where they exist, that would otherwise invalidate the dataset.

##### [XML_PUBLISHER](#xml_publisher-4)

Extracts and maps attributes to values required by the XML root template or sub-templates, compiles the templates to a single XML file, and publishes the XML to the PyCSW, or to a local folder.

##### [NOTIFY_UPDATE](#notify_update-2)

E-mails processing results to administrator.

## Manitoba

## New Brunswick

## Newfoundland and Labrador

## Nova Scotia

## Nunavut

## Ontario

## Prince Edward Island

## Québec

## Saskatchewan

## Yukon

## Custom Transformers Detail

### Universal Transformers

#### AWS_TRANSLATE

This transformer is designed to function in all data ETL activities and translates the following attributes from English to French using the Amazon Web Services language translation API:

- title
- notes
- sector
- tags{}.display_name (list attribute)
- resources{}.name (list attribute)

The results are achieved by performing the following tasks:

- Removes failure causing excess whitespace from all attribute values to be translated via Python script.
- Tests for strings over 5000 bytes and reduces strings in excess to under 5000 bytes (5000 bytes is maximum permitted per attribute by AWS Translate)
- Posts attributes and list attributes to be translated to the AWS API using Python script.
- Creates French version of the attributes and list attributes from the returned translated value.
- Removes UTF8 Character code returned from translated results.
- Removes out-of-scope attributes.

#### DEFAULT_ATTRIBUTE_MAPPER

This custom transformer merges an Excel file containing default attribute values common to each dataset by performing the following tasks:

- Each default_key attribute is turned into an individual attribute.
- Default attributes are then merged with each dataset.

#### DUPLICATE_SERVICE_REMOVER		
	
Manages duplicate WMS or ESRI REST resources where they exist, that would otherwise prevent validation of the dataset when loaded to the FGP.  Duplicate services are given the resources{}.format value of 'other'.  The results are achieved through the following tasks:

- Create histogram{} list from resources{}.protocol list to extract attribute value counts from each data set.  
- Searches histogram{}.value list for OGC:WMS
- Searches histogram{}.value list for ESRI REST: Map Service
- ListIndexer obtains number of OGC:WMS services
- List indexer obtains number of ESRI REST services
- Tests for OGC:WMS or ESRI REST services in excess of two.
- The data stream is split into two.
  - Data stream 1 contains OGC:WMS or ESRI REST services.
    - Data stream 1 generates unique id '_uuid' for later FeatureMerger.
	- Data stream 1 is split into two.
	  - Data stream 1a retains only the resources{} list and _uuid attribute.
	    - resources{} list is exploded to its individual attributes.
	    - xlink_role attribute is tested for a value.
	    - xlink_role attributes with values have a DuplicateFilter applied with consideration to _uuid, protocol and xlink_role attribute duplicates.
		  - The first value found is output via the unique port to the ListBuilder transformer.
		  - Any duplicates found are output the duplicate port and have their format attribute updated to 'other' and are sent to the ListBuilder transformer.
	    - xlink_role attributes without a value are sent to directly to the ListBuilder transformer.  
        - Data stream 1a is sent to the Supplier port of the FeatureMerger transformer.
	  - Data stream 1b retains all attributes except resources{} list attribute.
	    - Date stream 1b is sent to the Requestor port of the FeatureMerger transformer.
	- Data streams 1a and 1b are rejoined in the FeatureMerger on the _uuid attribute.
	- Out of scope attributes are removed from data stream 1.
	- Data stream 1 is sent to the transformer output.
  - Data stream 2 does not contain OGC:WMS nor ESRI REST Services.
    - Data stream 2 is sent directly to the transformer output.

#### GMD_SECTION_DATA_EXTRACTION

Creates lists of data items and removes duplicates for the GMD templates by performing the following tasks: 

- Copies resources{}.format list to new list distributionList{}.format.
- Removes duplicates from distributionList{}.format for inclusion in the GMD_DISTRIBUTIONFORMAT sub-template.
- Copies resources{}.projection_name to new list projectionList{}.projection_name.
- Removes duplicates from projectionList{}.projection_name for inclusion in the GMD_REFERENCESYSTEMINFO sub-template.
- Copies resources{}.resource_update_cycle to new list updateList{}.resource_update_cycle.
- Removes duplicates from updateList{}.resource_update_cycle for inclusion in the GMD_RESOURCEMAINTENANCE sub-template.
- Removes duplicates from more_info{}.link list for inclusion in the GMD_ONLINERESOURCE sub-template.

#### MAPPING_ERROR_LIST_CREATOR

Creates an FFS file of data item values that cannot be mapped to a valid value due to undocumented data entry errors missing from the look-up table.  Allows administrators to update the look-up table to document the missing value and re-run workspace.  These results are achieved by performing the following tasks:

- Counts the number of mapping errors found following processing of METADATA_VALUE _MAPPER or METADATA_FORMAT_MAPPER.
- Tests for error count > 0.
- Removes all attributes except mapping_errors{}.error.
- Explodes mapping_errors{} list to write individual attributes to FFS file.

#### METADATA_FORMAT_MAPPER

Corrects data format values of to valid data format values and to add associated Resource Type attributes in French and English.  Results are achieved by performing the following tasks:

- When loaded to the workspace, the user can select the following data conversion functions to be on or off by selecting yes/no options in the following published parameters:
  - ERROR_NOT_MAPPED: enables mapping of data item values that cannot be found in the lookup tables.
  - REAL_VALUE_REFRESH: enables updating of data format values.
  - RES_TYPE_FR_REFRESH: enables updating of French Resource Type values.
  - RES_TYPE_EN_REFRESH: enables updating of English Resource Type values.
- Tests for 'original_value' attribute in look-up tables and terminates translation if missing.
- Tests for REAL_VALUE_REFRESH, RES_TYPE_FR_REFRESH and RES_TYPE_EN_REFRESH options.
- Sets look-up table attributes as priority over incoming dataset attributes.
- Assigns look-up table attributes to list attributes via Python scripting.

#### METADATA_VALUE_MAPPER

Corrects values to valid English values and adds the valid French equivalents and RI_CODES where applicable.  It can be utilized for multiple metadata items by accessing custom look up tables specific to the data item by performing the following tasks:

- When loaded to the workspace, the user can select the following data conversion functions to be on or off by selecting yes/no options in the following published parameters:
  - ERROR_NOT_MAPPED: enables mapping of data item values that cannot be found in the lookup tables.
  - ENGLISH_REFRESH: enables updating of English attribute values.
  - FRENCH_REFRESH: enables updating of French attribute values.
  - CODE_REFRESH: enables updating of RI_CODE values.
- Tests for 'original_value' attribute in look-up tables and terminates data translation if missing.
- Tests for ENGLISH_REFRESH, FRENCH_REFRESH and CODE_REFRESH options.
- Sets look-up table attributes as priority over incoming dataset attributes.
- Assigns look-up table attributes to list attributes via Python scripting.

#### MORE_INFO_MANAGER

This transformer tests the more_info{}.link list for valid attribute values and filters them out where missing by performing the following tasks:

- Creates a _uuid attribute using the UUIDGenerator.
- Splits the data stream into two:
  - Stream 1 retains only the _uuid and more_info{} list.
    - more_info{}.link list is exploded into individual 'link' attributes.  
	- link attributes with no value are filtered out.
	- 'protocol' attribute is created with hard coded value 'https'
	- data stream sent to 'Supplier' input of FeatureMerger transformer.
  - Stream 2 retains all other data except the more_info{} list.
    - Stream 2 is sent to the 'Requestor' port of the FeatureMerger transformer.
- Feature Merger transformer merges stream 1 and 2 using the _uuid as the join attribute, then recreates the more_info{} list adding the link and protocol attributes.
- Out-of-scope attributes are removed.

#### NOTIFY_CREATE

This transformer is designed to function in all CREATE workspaces and creates an email message of ETL results for system administrators.

##### Insert Records Notification

This section performs the following tasks:
- Gets count of inserted records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### NOTIFY_UPDATE

This transformer is designed to function in all UPDATE workspaces and creates an email message of ETL results for system administrators.

##### Insert Records Notification

This section performs the following tasks:
- Gets count of inserted records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

##### Update Records Notification

This section performs the following tasks:
- Gets count of updated records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

##### Records Deleted Notification

This section performs the following tasks:

- Gets count of records that were deleted from the PyCSW
- Creates a message string with the overall results of the data deletion.

##### Notification Compiler and eMailer

This section performs the following tasks:
- Gets the current date and time.
- Concatenates insert records or no records to insert notification strings, update records or no records to update notification strings, number of obsolete records deleted, plus date and time into one message string.
- Emails the message string to an administrator.

#### REMOVE_BROKEN_URL_WMS_ESRI_REST

This transformer tests all WMS and ESRI REST URL's for connectivity and removes them where the URL is broken.  These results are achieved by performing the following tasks:

- Creates unique ID '_uuid' for each dataset using the UUIDGenerator.
- Splits the data stream into two:
  - Stream 1 retains only the _uuid and resources{} list.
    - Resources{} list are exploded into individual attributes.
	- 'format' attribute is tested for WMS or ESRI REST services.
	- Stream 1 is split into two:
	  - Stream 1a sends 'format' attributes with WMS or ESRI REST values to the HTTP Caller
	    - HTTP Caller performs a 'GET' function on each WMS or ESRI REST URL.  Functioning URL's will receive a response and be sent to the output port.  Non-functioning URL's will be filtered out.  
		- Out of scope attributes are removed.
		- Stream 1a is sent to ListBuilder transformer.
	  - Stream 1b sends format attributes that do not have WMS or ESRI REST values to the List Builder transformer
	- Stream 1a and 1b are remerged at the ListBuilder transformer, and the resources{} list is rebuilt from the exploded attributes.
	- Stream 1 is sent to the FeatureMerger transformer.
  - Stream 2 removes the resources{} attribute list.
  - Stream 2 is sent to the FeatureMerger.
- Streams 1 & 2 are joined on the _uuid attribute.
- Out of scope attributes are removed.
- Datasets are tested to ensure at least one URL remains after testing or they are filtered out.

#### TEMPORAL_EXTENTS_MAPPER

The temporal extents and date format refiner tests and inserts required values where missing, and formats date by performing the following tasks:

- Extracts the resources{}.data_collection_start_date list attribute.
- Sorts the resources{}.data_collection_start_date list attributes in ascending order to find the earliest date.
- If no start date exists in the data set, a data_collection_start_date attribute is created with the default value 0001-01-01.
- Keeps the earliest start date if available and removes all other dates using a list indexer and bulk attribute remover.
- Creates a single non-list data_collection_start_date attribute to represent the dataset.
- Sorts the resources{}.data_collection_end_date list attributes in descending order to find the latest date.
- If no end date exists in the data set, a data_collection_end_date attribute is created with no value (this field can be empty).
- Keeps the latest end date if available and removes all other dates using a list indexer and bulk attribute remover.
- Creates a single non-list data_collection_end_date attribute to represent the dataset.
- Converts dates to ISO yyyy-mm-dd format.

#### TOPIC_PARSER

Parses topics into individual attributes when multiple topics appear as comma separated values and adds a default value where missing, by performing the following tasks:

- Sets delimiter type (ie: comma) for delimiter separated values.
- Tests all iso_topic_string attributes for valid topic values.
- Creates iso_topic_string with default value of 'geoscientificInformation' where missing.
- Python script parses delimiter (ie: comma) separated iso_topic attributes (ie: iso_topic_string = economy,society,geoscientificInformation) into individual list attributes (ie: iso_topic{0}.topic_string = economy, iso_topic{1}.topic_string = society, iso_topic{2}.topic_string = geoscientificInformation) and converts non comma separated attributes (ie: iso_topic_string = geoscientificInformation) to individual list attributes (ie: iso_topic{0}.topic_string = geoscientificInformation).

#### WMS_REST_LANGUAGE_FORMATTER

This transformer creates default values in the resources{} list required for the GMD_TRANSFEROPTIONS XML sub-template, and creates an additional list entry that is required for French WMS and ESRI REST format types.  These results are achieved by performing the following tasks:

- Creates unique ID '_uuid' for each dataset using the UUIDGenerator.
- Splits the data stream into two:
  - Stream 1 retains only the _uuid and resources{} list.
    - resources{} list is exploded into individual attributes.
	- The SSL protocol for each URL attribute are tested for 'http' or 'https'.  'protocol' attribute is created with the value 'HTTP' or 'HTTPS' for insertion into the GMD_TRANSFEROPTIONS sub-template.
	- 'xlink_role' attribute is created for insertion into the GMD_TRANSFEROPTIONS sub-template.
	- Attributes 'transfer_option_description_language' with value 'eng' and 'transfer_option_description_language_other_lang' with value 'fra' are created.
	- '_element_index' attribute is removed.
	- Exposes 'id' attribute from exploded resources{} list.
	- ListBuilder transformer recreates resources{} list containing stream 1 attributes that were previously exploded and new attributes.
	- Data stream 1 is sent to FEATURE_MERGER_1 transformer.
  - Data stream 2 retains all attributes except resources{} list attribute.
    -  Data stream 2 sent to FEATURE_MERGER_1 transformer.
- Data streams 1 & 2 are joined on the _uuid attribute.
- The data stream is again split into two:
  - Data stream 3 retains only the _uuid and resources{} list.
    - resources{} list is exploded into individual attributes.
	- The AttributeFilter transformer splits Stream 3 into three data streams:
	  - Data stream 3a includes all resource data with 'WMS' as the format value and splits them to two AttributeCreator transformers.
	    - AttributeCreator_3 creates French attribute values, overriding previously created definitions:
		  - 'xlink_role' with the value of 'urn:xml:lang:fra-CAN'
		  - 'transfer_option_description_language_other_lang' with the value of 'fra'
		  - 'transfer_option_description_language' with the value of 'fra'
		- AttributeCreator_2 creates English attribute values:
		  - 'xlink_role' with the value of 'urn:xml:lang:eng-CAN'
		  - 'transfer_option_description_language_other_lang' with the value of 'eng'
		  - 'transfer_option_description_language' with the value of 'eng'
		- AttributeCreator_3 and AttributeCreator_4 are both sent to Attribute_Creator_8 transformer.
	    - AttributeCreator_8 creates 'protocol' with value of 'OGC:WMS'
		- Data stream 3a sent to AttributeExposer_4 transformer.
	  - Data stream 3b includes all resources data with 'ESRI REST' as the format value and splits them to two AttributeCreator transformers.
	    - AttributeCreator_7 creates French attribute values, overriding previously created definitions:
		  - 'xlink_role' with the value of 'urn:xml:lang:fra-CAN'
		  - 'transfer_option_description_language_other_lang' with the value of 'fra'
		  - 'transfer_option_description_language' with the value of 'fra' 
		- AttributeCreator_6 creates English attribute values:
		  - 'xlink_role' with the value of 'urn:xml:lang:eng-CAN'
		  - 'transfer_option_description_language_other_lang' with the value of 'eng'
		  - 'transfer_option_description_language' with the value of 'eng'
	    - AttributeCreator_6 and AttributeCreator_7 are both sent to Attribute_Creator_9 transformer.
	    - AttributeCreator_9 creates 'protocol' with value of 'ESRI REST: Map Service'
		- Data stream 3b sent to AttributeExposer_4 transformer.
      - Data stream 3c includes all resource data with neither 'WMS' nor 'ESRI REST' as the format value.
	    - Data stream 3c sent to AttributeExposer_4 transformer.
	- Data streams 3a, 3b and 3c are merged as Stream 3 at the AttributeExposer_4 transformer, where 'id' attribute is exposed.
    - ListBuilder transformer recreates resources{} list containing stream 3 attributes that were previously exploded.
	- Data stream 3 sent to FEATURE_MERGER_2 transformer.
  - Data stream 4 retains all attributes except resources{} list attribute.
    - Data stream 4 sent to FEATURE_MERGER_2 transformer.
- Data streams 3 & 4 are joined on the _uuid attribute.
- Out of scope attributes are removed.
- New attributes created in this transformer are exposed.
- ListSorter sorts resources{} list alphabetically by resources{}.format items.

#### XML_PUBLISHER

Extracts and maps attributes to values required by the XML root template or sub-templates, compiles the templates to a single XML file, and publishes the XML to the PyCSW, or to a local folder.  

##### ATTRIBUTE LOOKUP TABLE PROCESSING

An .xls config file maps the extracted metadata values to the HNAP attributes required by the root template and sub-templates.  The lookup table contains the following attributes:

- **HNAP_ATTRIBUTES:** This is a list of attribute keys that are used by the root template and sub-templates.  All metadata attribute keys are converted to these attributes.  This data row does not allow duplicate keys.
- **FEATURE_ATTRIBUTES:** This is a list of all attributes extracted from the metadata.  It allows for stand-alone attributes and list attributes, and can be varied from workspace to workspace.  This data row does not allow duplicate keys.
- **METADATA_SECTION:** This is a list of the metadata sections, that reflect the root template and sub-templates, to which each HNAP_ATTRIBUTE is directed.  Some attributes may apply to multiple metadata sections and in these cases the METADATA_SECTION fields can contain multiple values and are separated by a semi-colon.  This list can also contain duplicate values as more than one attribute can be mapped to a metadata section.

The attribute config file is processed through the following tasks:

- From the lookup table, the METADATA_SECTION attribute  for HNAP_ATTRIBUTES found in multiple metadata sections is split into one attribute per METADATA_SECTION creating METADATA_SECTION{} list, using the AttributeSplitter transformer.
- METADATA_SECTION{} list is exploded to its individual parts using a ListExploder transformer.
- A StringSearcher transformer searches the lookup table for FEATURE_ATTRIBUTES that are list attributes.
- AttributeSplitter transformer splits list attributes using {} delimiter and creates _list{} list attribute from results.
- AttributeCreator extracts _list{0} attribute creating list_name attribute that is original FEATURE_ATTRIBUTE list name.
  - These lists are tested for duplication in METADATA_SECTIONS and an error is thrown in the transformer when found.
- List attributes and non-list attributes have out of scope attributes removed.
- ListBuilder builds _list{} list attributes from FEATURE_ATTRIBUTES, HNAP_ATTRIBUTES and list_name, grouped by METADATA_SECTION attributes.
-  '_order' attribute with value of 1 is created.
- ListElementCounter retrieves _list{} element count for each METADATA_SECTION.
- ListSearcher searches for _list{}.listname attribute in each METADATA_SECTION.
- _list_index from all _list{}.listname attributes is extracted.
- The results are sent to the XML CREATION section.

##### METADATA PREPROCESSING

- Exposes all metadata attributes.
- Python script removes all whitespace.
-  '_order' attribute with value of 2 is created.
- The results are sent to the XML CREATION section.

##### XML CREATION

- Sorter transformer receives data from the ATTRIBUTE LOOKUP TABLE PROCESSING and METADATA PREPROCESSING section.  The data is sorted by the '_order' attribute, so giving priority to the lookup table.
- The data stream is split so all attributes, except 'method', enter a PythonCaller.
  - In the PythonCaller, the Python script utilizes attribute names and list attribute names created by the config file to convert metadata attribute keys to the HNAP_ATTRIBUTE Keys created from the config file.  The HNAP_ATTRIBUTE keys are consumed by the XML Templates used to build the metadata XML file.
  - HNAP_ATTRIBUTE keys are exposed.
  - AttributeFilter filters metadata according to METADATA_SECTION attribute and throws error if METADATA_SECTION is missing.
  - XMLTemplater compiles metadata root template with sub-templates to output single XML metadata file as '_xml_raw' attribute.
  - Results are sent to FeatureMerger.
- 'method' attribute stream is not part of the metadata, but is preserved to be used to set the XML creation method.
  - All data is removed from this stream, except 'method' and 'id'
  - Results are sent to FeatureMerger.
- FeatureMerger merges metadata attribute stream with method attribute stream.
- 'master_id' attribute is renamed to 'id'.
- Creates methodSelect attribute from selection in METHOD_SELECT published parameter.
- Tests if methodSelect is 'Auto'.  Note: If 'Auto' is selected then no changes is made to the value of the method attribute.  This would be utilized in an 'UPDATE' workspace as the 'Insert' or 'Update' method values are previously created in 'UPDATE' transformers based on new data (Insert) or updated data (Update).
- If methodSelect is not set to 'Auto', then method attribute assumes other methodSelect values; 'Insert', 'Update' or 'Local'.
- AttributeFilter filters datasets according to their 'method' value.
  - 'Local': Creates '_xml_data' attribute by copying '_xml_raw' attribute.  
  - 'Insert': Creates '_xml_data' attribute by concatenating PyCSW Insert headers and footers with '_xml_raw' attribute.
  - 'Update': Creates '_xml_data' attribute by concatenating PyCSW Update headers and footers with '_xml_raw' attribute.
- A second XMLTemplater receives all datasets, adds header for '_xml_data' attribute and outputs as '_xml_data_header'
- XMLFormatter cleans up XML '_xml_data_header' and outputs XML as 'text_line_data' attribute.
- XMLValidator validates the syntax of 'text_line_data' attribute.
- AttributeFilter filters datasets according to method attribute.
  - 'Local': Writes 'text_line_data' attribute for each data set to individual XML files directly to LOCAL transformer output.
  - 'Insert': Sends 'text_line_data' attribute for each new data set to PyCSW_POST transformer.
    - PyCSW_POST transformer uses Python script to insert each new data record to the Catalog Service for the Web.  Each insertion attempt receives a response as to the success or failure of the post in the form of 'insert_response' attribute.
	- 'insert_response' attribute is exposed.
	- Tester transformer evaluates the 'insert_response' attribute for success or failure.
	  - Successful insertions are output via the PASSED port and sent to the INSERT_PASSED transformer output port.
	  - Failed insertions are output via the FAILED port and sent to the INSERT_FAILED transformer output port.
  - 'Update': Sends 'text_line_data' attribute for each updated data set to PyCSW_POST transformer.
    - PyCSW_POST transformer uses Python script to insert each updated data record to the Catalog Service for the Web.  Each update attempt receives a response as to the success or failure of the post in the form of 'insert_response' attribute.
	- 'insert_response' attribute is exposed.
	- Tester transformer evaluates the 'insert_response' attribute for success or failure.
	  - Successful updates are output via the PASSED port and sent to the UPDATE_PASSED transformer output port.
	  - Failed updates are output via the FAILED port and sent to the UPDATE_FAILED transformer output port.
	
### Provincial and Territorial Specific Transformers

#### Alberta

##### AB_CREATE_PRETRANSLATE

This transformer is designed to function exclusively in the AB_CREATE workspace.  It queries the Alberta open data API and the Alberta geospatial API, and filters the returned data by performing the following tasks:

###### Alberta Open Data Query Loop Creation 

This section uses FME transformers to create a repetitive query loop for the Alberta Data API as the API will only return 1000 records per query, less than that of the BC database.  
It is set at default to perform 20 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://open.alberta.ca/api/3/action/package_search?start=@Value(start_feature)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 20000 records, and, at the time of writing, there are approximately 17,000 open data records in Alberta open data.

###### Alberta Open Data Query

This section sends each concatentated query instance using a GET http method to the Alberta Open Data API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes and values from the JSON string based on a JSON query.

In the event of a connection failure to the API, the process is terminated and an email is generated and sent to the system admin.

###### Alberta Open Data Attribute Management

Specific resource URL's exposed in the Alberta API link to a geospatial CSW, where the second resource URL in each data record is an XML file defining a catalog service record.

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Tests resource URL domains exposed by the JSON query that contain 'geospatial' in their value, and filters out other records.
- Filters out duplicate datasets that Alberta has already republished from NRCan.
- Tests second resource URL for internal Alberta CSW domain (oxpgdaws01.env.gov.ab.ca:8080) in URL string.  This second resource URL is always an XML file that defines CSW record.
- Tests second resource URL for public domain string used for XML CSW queries.
- Replaces internal Alberta CSW domain string snippet in second resource URL with publicly accessible domain string snippet (https://geodiscover.alberta.ca)
- Filters out second resource URL that are not links to Alberta geospatial by testing for absence of 'csw' in URL string.
- Gets XML file from edited second resource URL.
- Breaksdown attribute fields in retreived XML document.
- Extracts attribute keys/values from XML document using the following XQuery expression:
  - [Alberta Open Data X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-OpenData-XQuery.xml)
- Exposes required extracted attributes from X-Query and earlier JSON query.
- Adds additional required attributes not available in extracted data
- Creates shell values of attributes required for universal CSW Insert transformer
- Formats all date fields to ISO yyyy-mm-dd
- Copies selected attributes to act as proxies for other required values in XML output template.
- Renames indexed and other specific attributes to match XML template.
- Outputs to Date/Time Testing.

##### Query Creation for Alberta Geospatial API

All ISO 19139 formatted geospatial data is extracted through the Alberta Geospatial Portal.  The query is created in this section.

This section performs the following functions:

- Concatenates API query URL and number of rows to query.  Number of rows is set in published parameter ISO_19139_QUERY_ITERATIONS and has a default value of 2000.
  - Default Query: https://geodiscover.alberta.ca/geoportal/rest/find/document?max=2000
- In the event of a connection failure to the API, the process is terminated and an email is generated and sent to the system admin.
- Sends query string to API and returns list of unique ID's.
- Exposes the unique ID query string from the returned XML file.
- Extracts unique ID query string.
- Extracts unique ID.
- Call to API to extract XML using unique ID query string.
- Tests for ISO 19139 formatted XML files by eliminating files with MD_Metadata tag.

##### Alberta Geospatial Attribute Management 

Currently, only ESRI REST services are extracted from the ISO 19139 formatted files accessed in this process.  Other datasets in this format have inadequate information to complete an HNAP compliant dataset

This section performs the following functions:

- Extracts required attributes from XML strings returned in the previous process through the following XQuery Expression:
  - [Alberta Geospatial Data X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-GeospatialData-XQuery.xml)
- Exposes extracted attributes.
- Tests for ESRI REST services by searching for 'MapServer' in URL string.
- Calculates string length in publish date attribute.
- Tests for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts publish date from yyyymmdd format to yyyy-mm-dd format.
- Tests that create date has a value.
- Where missing, sets create date to publish date.
- Converts create date from yyyymmdd format to yyyy-mm-dd format.
- Tests that record modified date has a value.
- Where missing, sets records modified date to publish date.
- Converts record modified date from yyyymmdd format to yyyy-mm-dd format.
- Tests that data collection start date has a value.
- Where missing, sets data collection start date to 00010101.
- Calculates string length in data collection start date attribute.
- Tests for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts data collection start date from yyyymmdd format to yyyy-mm-dd format.
- Tests that data collection end date has a value.
- Calculates string length of data collection end dates that have a value.  **NOTE:** Data collection end dates with no value are left blank. 
- Tests data collection end dates for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts data collection end date from yyyymmdd format to yyyy-mm-dd format.
- Adds additional global attributes not available in extracted data.
- Changes unique ID values to required lower case.
- Outputs to Date/Time Testing.

###### Date/Time Testing

This section exists primarily for debugging purposes and can test creation date for records that backdated to a specific number of days or months.  Its default setting for normal 
operation is 0, which nullifies the test.  All data extracted from the Alberta Open Data API stream and the Alberta Geospatial Data API stream converges here.

###### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not found, a generic name, 
'AB Data Link' is inserted to the resource name attribute.

###### Excess Attribute Removal

This section performs the following tasks:

- Removes out of scope attributes.
- Output is directed to the AWS_TRANSLATE transformer.

##### AB_MISSING_ATTRIBUTE_MAPPER

This transformer adds default values to attribute values with known data gaps.  The results are achieved through the following tasks:

- AttributeExposer exposes all attributes utilized by this transformer.
- AttributeRenamer renames 'id' attribute to '_uuid' to avoid conflict with 'id' value in exploded lists.
- Data stream is split and sent to the Role Refiner section.

###### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  

- Data stream 1 processes role attributes.
  - AttributeKeeper retains only _uuid, default_role_value and contacts{} attributes.
  - ListExploder explodes contacts{} list.
  - Tester tests 'role' attribute is an HNAP conforming value.
  - For non-conforming values, AttributeCreator sets role to default_role_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.
  - Results are sent to Supplier port of FeatureMerger.
- Data stream 2 carries all metadata
  - AttributeRemover removes contacts[] list attribute.
-  FeatureMerger merges attributes from refined role attributes to the metadata, and recreates contacts{} list attributes.

###### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'asNeeded'.  

- Data stream 1 processes update cycle attributes.
  - AttributeKeeper retains only _uuid, default_update_value and resources{} attributes.
  - ListExploder explodes resources{} list.
  - Tester tests 'resource_update_cycle' attribute is an HNAP conforming value.
  - For non-conforming values, AttributeCreator sets role to default_update_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.
  - Results are sent to Supplier port of FeatureMerger.
- Data stream 2 carries all metadata
  - AttributeRemover removes results[] list attribute.
-  FeatureMerger merges attributes from refined update cycle attributes to the metadata, and recreates resources{} list attributes.

###### Spatial Representation Type Refiner

This section tests that Spatial Representation Type values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  

- Tester tests spatial_representation_type attribute is an HNAP conforming value
- For non-conforming values, AttributeCreator sets spatial_representation_type to default_spatial_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.

###### Progress Code Refiner

This section tests that Progress code values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'onGoing'.  

- Tester tests progress_code attribute is an HNAP conforming value.
- For non-conforming values, AttributeCreator sets progress_code to default_progress_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.
  
###### Projection Code Refiner

This section tests for projection name value and sets default value where missing.

- Tester tests projectionList{0}.projection_name attribute is an HNAP conforming value.
- For non-conforming values, AttributeCreator sets projectionList{0}.projection_name to default_reference_code_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.

###### Reference System Codespace Refiner

This section tests for reference system codespace value and sets default value where missing.

- Tester tests reference_system attribute has a value.
- For non-conforming values, AttributeCreator sets reference_system to default_reference_space_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.

###### Reference System Version Refiner

This section tests for reference system codespace value and sets default value where missing.

- Tester tests reference_system_version attribute has a value.
- For non-conforming values, AttributeCreator sets reference_system_version to default_reference_version_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.

###### Topic Category Refiner

This section substitutes a default value where items in iso_topic{}.topic_value list are nonconforming or missing.  List duplicates are removed.

- Data stream 1 processes iso_topic{}.topic_value attributes.
  - AttributeKeeper retains only _uuid, default_topic_value and iso_topic{}.topic_value attributes.
  - ListExploder explodes iso_topic{}.topic_value list.
  - Tester tests topic_value attribute is an HNAP conforming value.
  - For non-conforming values, AttributeCreator sets role to default_topic_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.
  - Results are sent to ListBuilder to rebuild iso_topic{} list.
  - DuplicateRemover removes duplicates from iso_topic{} list.
- Data stream 2 carries all metadata
  - AttributeRemover removes iso_topic[] list attribute.
-  FeatureMerger merges attributes from refined update cycle attributes to the metadata, and recreates resources{} list attributes.
- AttributeRemover removes out-of-scope attributes.

###### HTML/XML Refiner

All resources{}.format attributes in Alberta data have the value of HTML for index 0, and XML for index 1, with the exception of ESRI REST formats that are extracted from ISO 19139 data, that are at index 0, and are followed by no successive indices.  This section tests resources{0}.format = HTML and resources{1}.format = XML, and assigns those values where not found, except where resources{0}.format = ESRI REST.

- Tester tests resources{0}.format is not HTML nor ESRI REST
- For non-conforming values, AttributeCreator sets resources{0}.format = HTML.
- Tester tests resources{0}.format is not ESRI REST and resources{1}.format is not XML.
- For non-conforming values, AttributeCreator sets resources{1}.format = XML.

###### ZIP Link Creator

On Alberta's open data site, ISO 19115 data with only two resources{} items per dataset (HTML and XML) also has access to a ZIP file download resource.  This section creates a zip file download link in conditions where the third URL has no value and the first URL is not an ESRI REST link.

- Tester creates a zip file download link in conditions where the third URL has no value and the first URL is not an ESRI REST link.
- For items meeting this criteria, AttributeCreator sets resources{2}.url = zip_link (zip_link attribute extracted in the CREATE/UPDATE extraction processes).

###### Tag Creator 

This section tests at least one tag value exists, and creates a default tag where missing.

- Tester tests tags{0}.display_name has a value.
- For missing values, AttributeCreator sets tags{0}.display_name to default_tag_value attribute, extracted from lookup table in the DEFAULT_ATTRIBUTE_MAPPER transformer.

###### Attribute Cleanup

- AttributeRenamer reverts '_uuid' attribute back to 'id'.
- AttributeRemover removes out-of-scope attributes.

##### AB_TRANSLATION_CORRECTION

This transformer corrects common GIS terms found in resources{}.name attributes that have been literally translated to incorrect French values in the AWS Translate tool and reverts them back to their correct GIS terms.

- For each identified error, a PythonCaller executes a Python script to revert the incorrect value to its original value.  The following errors are addressed:
  - 'REPOSE-TOI' is reverted to 'REST'.
  - 'CHUT' is reverted to 'SHP'.

##### AB_UPDATE_PRETRANSLATE

This custom transformer is the first stage of daily extraction of new or updated data from the AB Data API, and inserting to the CSW.  It also identifies obsolete records for removal from the CSW.  It is intended to run as a component of the 'AB_Update' workspace.

The transformer performs the following functions:

###### CSW UUID Reader

This section extracts the unique ID's from all data records currently loaded to the CSW by performing the following tasks:

- Creates attribute required to perform CSW search with XML file (Alberta)
- Loads the Get Records XML template.
- Formats Get Records XML template.
- Validates the Get Records XML template.
- Posts XML to PyCSW using Python script and returns XML with dataset summary.
- Exposes the unique ID elements from the returned XML file.
- Extracts string snippet from the unique ID element.
- Outputs to the Obsolete Records Removal section.

###### Alberta Open Data Query Loop Creation 

This section uses FME transformers to create a repetitive query loop for the Alberta Data API as the API will only return 1000 records per query, less than that of the BC database.  
It is set at default to perform 20 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://open.alberta.ca/api/3/action/package_search?start=@Value(start_feature)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 20000 records, and, at the time of writing, there are approximately 17,000 open data records in Alberta open data.

###### Alberta Open Data Query

This section sends each concatentated query instance using a GET http method to the Alberta Opend Data API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes and values from the JSON string based on a JSON query.

In the event of a connection failure to the API, the process is terminated and an email is generated and sent to the system admin.

###### Alberta Open Data Attribute Management

Specific resource URL's exposed in the Alberta API link to a geospatial CSW, where the second resource URL in each data record is an XML file defining a catalog service record.

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Tests resource URL domains exposed by the JSON query that contain 'geospatial' in their value, and filters out other records.
- Filters out duplicate datasets that Alberta has already republished from NRCan.
- Tests second resource URL for internal Alberta CSW domain (oxpgdaws01.env.gov.ab.ca:8080) in URL string.  This second resource URL is always an XML file that defines CSW record.
- Tests second resource URL for public domain string used for XML CSW queries.
- Replaces internal Alberta CSW domain string snippet in second resource URL with publicly accessible domain string snippet (https://geodiscover.alberta.ca)
- Filters out second resource URL that are not links to Alberta geospatial by testing for absence of 'csw' in URL string.
- Gets XML file from edited second resource URL.
- Breaksdown attribute fields in retreived XML document.
- Extracts attribute keys/values from XML document using the following XQuery expression:
  - [Alberta Open Data X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-OpenData-XQuery.xml)
- Exposes required extracted attributes from X-Query and earlier JSON query.
- Adds additional required attributes not available in extracted data
- Creates shell values of attributes required for universal CSW Insert transformer
- Formats all date fields to ISO yyyy-mm-dd
- Copies selected attributes to act as proxies for other required values in XML output template.
- Renames indexed and other specific attributes to match XML template.
- Outputs to the following sections:
  - Obsolete Records Removal
  - New/Updated Records Filter

##### Query Creation for Alberta Geospatial API

All ISO 19139 formatted geospatial data is extracted through the Alberta Geospatial Portal.  The query is created in this section.

This section performs the following functions:

- Concatenates API query URL and number of rows to query.  Number of rows is set in published parameter ISO_19139_QUERY_ITERATIONS and has a default value of 2000.
  - Default Query: https://geodiscover.alberta.ca/geoportal/rest/find/document?max=2000
- In the event of a connection failure to the API, the process is terminated and an email is generated and sent to the system admin.
- Sends query string to API and returns list of unique ID's.
- Exposes the unique ID query string from the returned XML file.
- Extracts unique ID query string.
- Extracts unique ID.
- Call to API to extract XML using unique ID query string.
- Tests for ISO 19139 formatted XML files by eliminating files with MD_Metadata tag.

##### Alberta Geospatial Attribute Management 

Currently, only ESRI REST services are extracted from the ISO 19139 accessed in this process data.  Other datasets in this format have inadequate information to complete an HNAP compliant dataset

This section performs the following functions:

- Extracts required attributes from XML strings returned in the previous process through the following XQuery Expression:
  - [Alberta Geospatial Data X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-GeospatialData-XQuery.xml)
- Exposes extracted attributes.
- Tests for ESRI REST services by searching for 'MapServer' in URL string.
- Calculates string length in publish date attribute.
- Tests for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts publish date from yyyymmdd format to yyyy-mm-dd format.
- Tests that create date has a value.
- Where missing, sets create date to publish date.
- Converts create date from yyyymmdd format to yyyy-mm-dd format.
- Tests that record modified date has a value.
- Where missing, sets records modified date to publish date.
- Converts record modified date from yyyymmdd format to yyyy-mm-dd format.
- Tests that data collection start date has a value.
- Where missing, sets data collection start date to 00010101.
- Calculates string length in data collection start date attribute.
- Tests for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts data collection start date from yyyymmdd format to yyyy-mm-dd format.
- Tests that data collection end date has a value.
- Calculates string length of data collection end dates that have a value.  **NOTE:** Data collection end dates with no value are left blank. 
- Tests data collection end dates for string length = 4, which is indicative of the year only.
- Adds '0101' to complete date strings that have year only.
- Converts data collection end date from yyyymmdd format to yyyy-mm-dd format.
- Adds additional global attributes not available in extracted data.
- Changes unique ID values to required lower case.
- Outputs to the following sections:
  - Obsolete Records Removal
  - New/Updated Records Filter
  
###### Obsolete Records Removal

This section removes obsolete data records by performing the following tasks:

- Inputs all data output from CSW UUID Reader, Alberta Open Data Attribute Management and Alberta Geospatial Attribute Management.
- Retains only the UUID from each data input and removes all other attributes.
- Merges unique ID's from the CSW with unique ID's from the current data search.
- Loads the Delete Records XML template for each CSW Data Record not found in the current data search.
- Formats Delete Records XML's.
- Validates Delete Records XML's.
- Posts Delete Records XML for each UUID in the CSW not found in the current data search, removing the obsolete record.
- Outputs the NO_DELETED_RECORDS_COUNT and DELETED_RECORDS_COUNT to NOTIFY_UPDATE transformer.

###### New/Updated Records Filter

This section performs the following tasks:

- Extracts current date.
- Calculates time since last time tool processed.  Default setting is 1 day and is accessed in published parameter TIME_FILTER_DAYS.
- Tests for new records by comparing record_publish_date attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute with value 'Insert' for all new records.
- After new records are filtered, tests remainder for updated records by comparing record_last_modified attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute 'Update' for all updated records.
- Outputs the TOTAL_RECORDS_COUNT, NEW_RECORDS_COUNT and UPDATED_RECORDS_COUNT to the NOTIFY_UPDATE transformer.
- Data is output to the Resource Name Tester section.

###### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not found, a generic name, 
'AB Data Link' is inserted to the resource name attribute.

###### Excess Attribute Removal

This section performs the following tasks:

- Removes out of scope attributes.
- Output is directed to the AWS_TRANSLATE transformer.

##### AB_WMS_FORMATTER

There are two categories of WMS found in Alberta datasets.  One individual WMS maintained by the Ministry of Energy and over twenty maintained by the Ministry of Agriculture.  This transformer edits the utilized URL's for the WMS to support compliancy to the FGP Map Viewer.

######  Ministry of Energy WMS

This section manages one unique WMS and compiles the URL string to HNAP requirements through the following steps:

- Tester tests resources{2}.format and resources{2}.url for the unique WMS.
- Found results enter StringSearcher that uses RegEx to extract object_name from resources{2}.url
- object_name not matched is output to another StringSearcher to extract object_name attribute via RegEx query.
- A final StringSeracher uses RegEx to refine URL for resources{2}.url.
- AttributeExposer exposes object_name attribute for WMS url concatenation.
- Data sent to PythonCaller.

###### Ministry of Agriculture WMS

- Results not found in previous Tester are split in two data streams.
  - Data stream 1 sent to AttributeKeeper
    - AttributeKeeper retains resources{}.format and resources{}.url.
	- Tester tests resources{3}.url for WMS services.
	- StringConcatenator concatenates resources{3}.url with GetCapabilities query:
	  - Example: resources{3}.url?service=WMS&request=GetCapabilities
	- HTTPCaller uses concatenated URL to extract capabilities from the WMS.
	- Extract_Results extracts attribute keys/values from XML document using XQuery, pairing titles and layer numbers by creating list attributes wms{}.xtitle and wms{}.object_name.
	- AttributeExposer exposes extracted attributes.
	- AttributeKeeper retains wms{} list only.
	- ListExploder explodes wms{} list.
	- AttributeExposer exposes values from exploded list.
	- Data sent to Supplier port on FeatureMerger.
  - Data stream 2 sent to Requestor port on FeatureMerger.
- FeatureMerger merges extracted wms{} list values with datasets using title and xtitle attributes.
- Data sent to PythonCaller.

###### PythonCaller

Contains Python script to concatenate URL string for WMS services.

#### British Columbia

##### BC_CREATE_PRETRANSLATE

This transformer is designed to function exclusively in the BC_CREATE workspace.  It queries the British Columbia open data API and filters the returned data by performing the following tasks:

###### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.   The results are achieved through the following tasks:

- AttributeCreator sets the number of loops required to query BC Data.  Default setting is 10 and is accessed in published parameter LOOP_ITERATIONS.
- CLONER repeats the number of loops required to query BC Data until the default setting in LOOP_ITERATIONS published parameter is reached.
- StringConcatenator concatenates each query string sent to the BC Data API.  The number of loop attributes set in the CLONER are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:
  - https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   
  - **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME.
The current default settings will return a total of 10000 records, and, as of November 2019, there are less than 3000 open data records in BC open data.

###### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  The results are achieved through the following tasks:

- HTTPCaller sends the query string to BC Data API and returns response as a JSON string.
  - In the event of a connection failure to the BC Data API, an email is sent to the administrator and the program is terminated.
- JSON_FRAGMENTER extracts attributes and values from the JSON string.

###### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not geographic.
- Filters out records that are not Open Government License - British Columbia.
- ISO_DATE_FORMATTER formats all date fields to ISO yyyy-mm-dd.
- Filters out duplicate datasets that BC has already republished from NRCan.

###### Date/Time Testing

This section exists primarily for debugging purposes and can test creation dates for records backdated to a specific number of days or months.  Its default setting for normal operation is 0, which nullifies the test.  The results are achieved through the following tasks:

- DateTimeStamper extracts current date.
- PAST_DATE_CALCULATOR calculates past dates. Default setting for normal operation is 0 days/0 months and can be reset in published parameters TIME_FILTER_DAYS and TIME_FILTER_MONTHS.
- FME_DATE_FORMATTER converts record_publish_date attribute to FME format for testing.
- Tests for new records by comparing record_publish_date attribute against time calculated in PAST_DATE_CALCULATOR.  
- ISO_DATE_FORMATTER converts record_publish_date back to ISO yyyy-mm-dd format for publishing.

###### Attribute Cleanup

- Python script places resource{}.description in resource{}.name where resource{}.name is missing.
- 'method' attribute with value 'Insert' is created to facilitate correct XML Formatting for later PyCSW insertion.
- Removes out-of-scope attributes from datasets.
- Sets all null or empty attributes as 'missing'.

##### BC_GEOWAREHOUSE_URL_BUILDER

The URL links for BC Data located in the BC Geowarehouse are not readily available from the BC API.  This transformer recreates the BC Geowarehouse URL format by concatenting several available attributes with hardcoded values.  The results are achieved by performing the following tasks:

- AttributeExposer exposes the attributes required by this transformer.
- AttributeRenamer renames  'id' attribute to '_uuid' to avoid being overwritten by resources{}.id after this list attribute is exploded.  Dataset is split into two data streams at the output port.
  - Data stream 1 separates resources{} list attributes from all other attributes.
    - Renames 'name' attribute to 'service_name' to avoid being overwritten by resources{}.name after this list attribute is exploded.  
	- AttributeKeeper retains 'service_name' '_uuid' and 'resources{}' attributes and discards all others.
	- LIST_EXPLODER explodes resources{} list attributes to non-list attributes.
	- AttributeExposer exposes required exploded attributes.
	- Tester tests 'name' attribute for BC Geowarehouse Custom Download.
	- AttributeCreator recreates resources{}.url attribute at extracted _element_index position from concatenated values.  
	- AttributeRemover removes out-of-scope attributes.
	- Data stream is sent to the Supplier port of the FeatureMerger.
  - Data stream 2 is sent to the Requestor port of the FeatureMerger.
- FeatureMerger merges data streams on _uuid attribute.
- AttributeRenamer reverts '_uuid' attribute to 'id'.

##### BC_RESOURCE_NAME_CORRECTION

This transformer sets the value of the resources{}.name attribute with the resources{}.description value when missing.  For all WMS services, it performs a getCapabilities to extract the Layer.Title and overwrites the resources{}.name value with Layer.Title.  The results are achieved by performing the following tasks:

- AttributeExposer exposes all attributes required by the transformer.
- PythonCaller executes a Python script that sets the value of the resources{}.name attribute with the resources{}.description value when missing.
- UUIDGenerator creates a temporary unique ID to rejoin data streams after processing.  The data stream is split into two at the Output port.
  - Data stream 1 ListExploder explodes the resources{} list.
    - The exploded format attribute tests for 'wms' value.
	- HTTPCaller uses the url attribute to perform GetCapabilities request on the data set.
	- XMLFlattener extracts Layer.Title attribute from the XML response.
	- Layer.Title attribute is exposed by AttributeExposer.
	- AttributeKeeper retains required attributes only.
	- AttributeCreator overwrites resources{}.name attribute with wms layer name retrieved from getCapabilities query.
	- AttributeRemove removes out-of-scope attributes, retaining only resources{}.name and the unique id.
	- Data stream 1 sent to Supplier port of FeatureMerger.
  - Data stream 2 sent to Requestor port of FeatureMerger.
- FeatureMerger merges resources{}.name attribute with datasets joined on unique id.
- Unique id is removed.
	
##### BC_UPDATE_PRETRANSLATE

This custom transformer is the first stage of scheduled extraction of new or updated data from the BC Data API, and inserting to the CSW.  It also identifies obsolete records for removal from the CSW.  It is intended to run as a component of the 'BC_UPDATE' workspace.

This transformer performs the following tasks:

###### CSW UUID Reader

This section extracts the unique ID's from all data records currently loaded to the CSW by performing the following tasks:

- AttributeCreator creates attribute required to perform CSW search with XML file (Columbia).
- XMLTemplater loads the Get Records XML template.
- XMLFormatter formats Get Records XML template.
- XMLValidator validates the Get Records XML template.
- PyCSW_POST posts XML to PyCSW using Python script and returns XML with dataset summary.
- XMLFragmenter exposes the unique ID elements from the returned XML file.
- StringSearcher extracts string snippet from the unique ID element.
- Outputs to the Obsolete Records Removal section.

###### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.  It is set at default to perform 10 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

###### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  The results are achieved through the following tasks:

- HTTPCaller sends the query string to BC Data API and returns response as a JSON string.
  - In the event of a connection failure to the BC Data API, an email is sent to the administrator and the program is terminated.
- JSON_FRAGMENTER extracts attributes and values from the JSON string.

###### Obsolete Records Removal

This section removes obsolete data records by performing the following tasks:

- AttributeExposer exposes unique ID from the current data search.  Data stream is split into two.
- One data stream is sent to AttributeKeeper retains only the UUID from each data input and removes all other attributes, the other data stream retains all attributes and is sent to the Attribute Management section.
- FEATURE_MERGER merges unique ID's from the CSW with unique ID's from the current data search.
- XMLTemplater Loads the Delete Records XML template for each CSW Data Record not found in the current data search.
- XMLFormatter formats Delete Records XML's.
- XMLValidator validates Delete Records XML's.
- PyCSW_POST posts Delete Records XML for each UUID in the CSW not found in the current data search, removing the obsolete record.
- Outputs the the NO_DELETED_RECORDS_COUNT and DELETED_RECORDS_COUNT to NOTIFY_UPDATE transformer.

###### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not geographic.
- Filters out records that are not Open Government License - British Columbia.
- ISO_DATE_FORMATTER formats all date fields to ISO yyyy-mm-dd.
- Filters out duplicate datasets that BC has already republished from NRCan.

###### New/Updated Records Filter

This section performs the following tasks:

- Extracts current date.
- Calculates time since last time tool processed.  Default setting is 1 day and is accessed in published parameter TIME_FILTER_DAYS.
- Tests for new records by comparing record_publish_date attribute against time calculated in DateTimeCalculator.
- Creates 'method' attribute with value 'Insert' is created for all new records to facilitate correct XML Formatting for later PyCSW insertion.
- After new records are filtered, tests remainder for updated records by comparing record_last_modified attribute against time calculated in DateTimeCalculator.
- Creates 'method' attribute 'Update' for all updated records to facilitate correct XML Formatting for later PyCSW insertion.
- Outputs the TOTAL_RECORDS_COUNT, NEW_RECORDS_COUNT and UPDATED_RECORDS_COUNT to the NOTIFY_UPDATE transformer.
- Data is output to the Attribute Cleanup section.

###### Attribute Cleanup

This section performs the following tasks:

- Python script places resources{}.description in resources{}.name where resources{}.name is missing.
- Removes out-of-scope attributes from datasets.
- Sets all null or empty attributes as 'missing'.
- Data is directed to the transformer OUTPUT port.

##### BC_WMS_FORMATTER

This transformer concatenates the url for all wms format URL's to a valid URL string for the map viewer.  The results are achieved by performing the following tasks:

- AttributeExposer exposes the required attributes for concatenation.
- PythonCaller executes a Python script to overwrite WMS url with concactenated attribute and hardcoded values:
  - Example: Attribute: resources{0}.url: https://openmaps.gov.bc.ca/geo/pub/WHSE_ADMIN_BOUNDARIES.ADM_NR_AREAS_SPG/ows?service=WMS&request=GetCapabilities
                       + Hardcoded value: &layers=pub:
				+ Attribute: object_name: WHSE_ADMIN_BOUNDARIES.ADM_NR_AREAS_SP
				       + Hardcoded value: &legend_format=image/png&feature_info_type=text/plain
					              RESULT: https://openmaps.gov.bc.ca/geo/pub/WHSE_ADMIN_BOUNDARIES.ADM_NR_AREAS_SPG/ows?service=WMS&request=GetCapabilities&layers=pub:WHSE_ADMIN_BOUNDARIES.ADM_NR_AREAS_SP&legend_format=image/png&feature_info_type=text/plain
				

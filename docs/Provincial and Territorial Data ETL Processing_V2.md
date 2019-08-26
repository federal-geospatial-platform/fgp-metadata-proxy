
Provincial and Territorial Extraction, Transformation and Loading Processes
==========

- [Table of Contents](#table-of-contents)
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes)
  - [Oveview](#overview)
    - [Workspaces](#workspaces)
	- [Custom Transformers](#custom-transformers)
	- [XML Templates](#xml-templates)
	- [Other PyCSW Tools](#other-pycsw-tools)
  - [Workspaces](#workspaces-1)
  - [Alberta](#alberta)
    - [Overview](#overview-1)
    - [AB_CREATE Workspace Detail](#ab_create-workspace-detail)
	  - [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate)
	  - [AB_POSTTRANSLATE_1](#ab_posttranslate_1)
	  - [AB_POSTTRANSLATE_2](#ab_posttranslate_2)
	  - [POSTTRANSLATE_3](#posttranslate_3)
	  - [AB_POSTTRANSLATE_4](#ab_posttranslate_4)
	  - [CSW_INSERT](#csw_insert)
	  - [NOTIFY_CREATE](#notify_create)
	- [AB_UPDATE Workspace Detail](#ab_update-workspace-detail)
	  -[AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate-1)
	  - [AB_POSTTRANSLATE_1](#ab_posttranslate_1-1)
	  - [AB_POSTTRANSLATE_2](#ab_posttranslate_2-1)
	  - [POSTTRANSLATE_3](#posttranslate_3-1)
	  - [AB_POSTTRANSLATE_4](#ab_posttranslate_4-1)
	  - [CSW_INSERT](#csw_insert-1)
	  - [CSW_UPDATE](#csw_update)
	  - [NOTIFY_UPDATE](#notify_update)
  - [British Columbia](#british-columbia)
    - [Overview](#overview-2) 
	- [BC_CREATE Workspace Detail](#bc_create-workspace-detail)
	  - [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate-2)
	  - [BC_POSTRANSLATE_1](#bc_posttranslate_1)
	  - [BC_POSTRANSLATE_2](#bc_posttranslate_2)
	  - [POSTTRANSLATE_3](#posttranslate_3-2)
	  - [BC_POSTRANSLATE_4](#bc_posttranslate_4)
	  - [CSW_INSERT](#csw_insert-2)
	  - [NOTIFY_CREATE](#notify_create-1)
	- [BC_UPDATE Workspace Detail](#bc_update-workspace-detail)
	  -[BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate-3)
	  - [BC_POSTRANSLATE_1](#bc_posttranslate_1-1)
	  - [BC_POSTRANSLATE_2](#bc_posttranslate_2-1)
	  - [POSTTRANSLATE_3](#posttranslate_3-3)
	  - [BC_POSTRANSLATE_4](#bc_posttranslate_4-1)
	  - [CSW_INSERT](#csw_insert-3)
	  - [CSW_UPDATE](#csw_update-1)
	  - [NOTIFY_UPDATE](#notify_update-1)
  - [Custom Transformers Detail](#custom-transformers-detail)
    - [Universal Transformers](#universal-transformers)
	  - [AWS_TRANSLATE](#aws_translate-4)
	  - [CSW_INSERT](#csw_insert-4)
	  - [CSW_UPDATE](#csw_update-2)
      - [NOTIFY_CREATE](#notify_create-2)
      - [NOTIFY_UPDATE](#notify_update-2)	
      - [POSTTRANSLATE_3](#posttranslate_3-4)	
    - [Provincial/Territorial Specific Transformers](#provincial/territorial-specific-transformers)
	  - [Alberta](#alberta-1)
	    - [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate-1)
		- [AB_POSTTRANSLATE_1](#ab_posttranslate_1-2)
		- [AB_POSTTRANSLATE_2](#ab_posttranslate_2-2)
		- [AB_POSTTRANSLATE_4](#ab_posttranslate_4-2)
		- [AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate-1)
	  - [British Columbia](#british-columbia-1)
	    - [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate-1)
		- [BC_POSTTRANSLATE_1](#bc_posttranslate_1-2)
		- [BC_POSTTRANSLATE_2](#bc_posttranslate_2-2)
		- [BC_POSTTRANSLATE_4](#bc_posttranslate_4-2)
		- [BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate-1)	  
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
   
# Provincial and Territorial Extraction, Transformation and Loading Processes

## Overview

### Workspaces

Open data extraction, transformation and loading processes utilize two different FME Workspaces for each Canadian province or territory:

-   **(p-t_abbreviation_)__CREATE__(_version_number).fmw:** The CREATE workspaces are for extracting, transforming and loading a complete dataset to an empty Catalogue Service for the Web (CSW).  Its intended use is for initial creation of a CSW, or in the event an entire CSW needs to be reloaded.  This can be run manually from FME Server.
-  **(p-t_abbreviation_)__UPDATE__(_version_number).fmw:**  The UPDATE workspaces filter, extract, transform and load new or updated data records to the CSW.  It also reads all existing data records already in the CSW and deletes any records no longer found in the source data.  These workspaces run on a daily schedule on the FME Server.

All FME Workspaces can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/FME_Workspaces)

### Custom Transformers

The extensive transformers required for metadata ETL have been aggregated into a series of custom transformers, each defining a key step in the ETL process.  These transformers can be broken down into three types:

-   **Workspace Exclusive Transformers:** These are exclusive to either a single provincial/territorial CREATE or UPDATE workspace.
-  **Provincial/Territorial Exclusive Transformers:** These are exclusive to a provincial or territorial ETL process, but can be used in that province/territory's CREATE or UPDATE transformers.
-  **Universal Transformers:** These contain processes that are universal to any workspace.

All FME custom transformers can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/FME_Custom_Transformers)

### XML Templates

The workspaces utilize 104 XML templates to retreive, load and delete data from the PyCSW.

-   **FGP_GetRecords.xml:** This XML file posts a request to the PyCSW and retrieves the unique ID from every data records contained therein.

-  **FGP_DeleteById.xml:** Following the extraction of unique ID"s from the PyCSW and validation of the unique ID's against unique ID's retreived from an agency's API, this XML file removes obsolete records by their unique ID by posting to the PyCSW.  

-  **FGP_XML_Insert_Template_(number).xml:**  There are 51 'insert' XML document templates that are denoted by 'Insert' tags at the beginning and end of the document, the number of distribution formats and the number of transfer options.  Data analysis has shown that there are no more than six distribution formats and no more than eleven transfer options in any given dataset.  The number at the end of the file name is indicative of the number of transfer options, followed by number of distribution formats.  The numbering is indexed, beginning at '0', where 0 indicates a count of 1.  For example, FGP_XML_Insert_Template_1-0.xml indicates the template can accommodate 2 transfer options and 1 distribution format, and FGP_XML_Insert_Template_10-3.xml indicates the template can accommodate 11 transfer options and 4 distribution formats.

-  **FGP_XML_Update_Template_(number).xml:**  There are 51 'update' XML document templates that are denoted by 'Update' tags at the beginning and end of the document, the number of distribution formats and the number of transfer options.  Data analysis has shown that there are no more than six distribution formats and no more than eleven transfer options in any given dataset.  The number at the end of the file name is indicative of the number of transfer options, followed by number of distribution formats.  The numbering is indexed, beginning at '0', where 0 indicates a count of 1.  For example, FGP_XML_Update_Template_1-0.xml indicates the template can accommodate 2 transfer options and 1 distribution format, and FGP_XML_Update_Template_10-3.xml indicates the template can accommodate 11 transfer options and 4 distribution formats.

All XML templates can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/XML_Templates)

### Other PyCSW Tools

-   **EMPTY CSW Python Scripts:** These are intended for admin purposes only in the event a CSW has to be cleared of all data.  These scripts run manually and must be executed prior to running a CREATE workspace.  It will clear 1000 records at a time from the CSW and will have to be run multiple times if the CSW count exceeds 1000.

All EMPTY CSW Python scripts can be found [here](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/scripts/Empty_PyCSW_Scripts)

## Workspaces

### Alberta

#### Overview

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using two approaches:

-   **Alberta Open Data Catalogue**: Alberta ISO 19115 compliant data is extracted by exposing data from CKAN API [Alberta's Open Data Catalogue](https://open.alberta.ca/opendata), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. The approach going through the Open Data Catalog first is required as the unique ID's from the Open Data are required due to inconsistencies in the unique ID's used in the subsequently exposed XML files.

-  **Alberta Geospatial Catalog**:  A small amount of ISO 19139 compliant data using exclusively ESRI REST services is unavailable in the Alberta Open Data Catalog and is exposed directly from [Alberta Geospatial Catalogue](https://geodiscover.alberta.ca/geoportal).  The unique ID naming conventions are accurate with this data subset which allows for direct extraction.  The remainder of ISO 19139 data not exposing ESRI REST services that is found in the Alberta geospatial catalogue has been found to be largely incomplete and unusable.  

Attributes required to meet mandatory requirements for individual XML (Extensible Markup Language) files are extracted from both the exposed JSON file and XML files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces use a series of custom transformers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx)

The Alberta Metadata FME Workspaces can be found here:

-   [Alberta FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/FME_Workspaces/AB)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### AB_CREATE Workspace Detail

The AB_CREATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate-1)

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [AB_POSTTRANSLATE_1](#ab_posttranslate_1-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [AB_POSTTRANSLATE_2](#ab_posttranslate_2-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [POSTTRANSLATE_3](#posttranslate_3-4)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [AB_POSTTRANSLATE_4](#ab_posttranslate_4-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [CSW_INSERT](#csw_insert-4)

Selects appropriate XML insert template and posts XML to the CSW.

##### [NOTIFY_CREATE](#notify_create-2)

E-mails processing results to administrator.

#### AB_UPDATE Workspace Detail

The AB_UPDATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate-1)

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against Alberta API's for obsolete data.  Deletes records from CSW that are no longer found in Alberta open data.  

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [AB_POSTTRANSLATE_1](#ab_posttranslate_1-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [AB_POSTTRANSLATE_2](#ab_posttranslate_2-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [POSTTRANSLATE_3](#posttranslate_3-4)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [AB_POSTTRANSLATE_4](#ab_posttranslate_4-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [CSW_INSERT](#csw_insert-4)

Selects appropriate XML insert template for all new datasets and posts XML to the CSW.

##### [CSW_UPDATE](#csw_update-2)

Selects appropriate XML update template for all updated datasets and posts XML to the CSW.

##### [NOTIFY_UPDATE](#notify_update-2)

E-mails processing results to administrator.

### British Columbia

#### Overview

British Columbia open data is exposed through a CKAN API:

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation) file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx)

The British Columbia Metadata FME Workspaces can be found here:

-   [British Columbia FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/FME_Workspaces/BC)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### BC_CREATE Workspace Detail

The BC_CREATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [BC_CREATE_PRETRANSLATE](#bc_create_pretranslate-1)

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [BC_POSTTRANSLATE_1](#bc_posttranslate_1-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [BC_POSTTRANSLATE_2](#bc_posttranslate_2-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [POSTTRANSLATE_3](#posttranslate_3-4)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [BC_POSTTRANSLATE_4](#bc_posttranslate_4-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [CSW_INSERT](#csw_insert-4)

Selects appropriate XML insert template and posts XML to the CSW.

##### [NOTIFY_CREATE](#notify_create-2)

E-mails processing results to administrator.

#### BC_UPDATE Workspace Detail

The BC_UPDATE workspace utilizes the following sequence of custom transformers.  Note that transformer names are hyperlinked to view detail:

##### [BC_UPDATE_PRETRANSLATE](#bc_update_pretranslate-1)

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against British Columbia's API for obsolete data.  Deletes records from CSW that are no longer found in British Columbia open data.  

##### [AWS_TRANSLATE](#aws_translate-4)

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### [BC_POSTTRANSLATE_1](#bc_posttranslate_1-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [BC_POSTTRANSLATE_2](#bc_posttranslate_2-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [POSTTRANSLATE_3](#posttranslate_3-4)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [BC_POSTTRANSLATE_4](#bc_posttranslate_4-2)

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### [CSW_INSERT](#csw_insert-4)

Selects appropriate XML insert template for all new datasets and posts XML to the CSW.

##### [CSW_UPDATE](#csw_update-2)

Selects appropriate XML update template for all updated datasets and posts XML to the CSW.

##### [NOTIFY_UPDATE](#notify_update-2)

E-mails processing results to administrator.

## Custom Transformers Detail

### Universal Transformers

#### AWS_TRANSLATE

This transformer is designed to function in all data ETL activities and translates the following attributes from English to French using the Amazon Web Services language translation API:

- title
- notes
- sector
- all exposed tags attributes (maximum 9)
- all exposed resource_name attributes (maximum 6)

This section operates using the following steps:

- Removes failure causing excess whitespace from all attribute values to be translated.
- Posts attribute to be translated to the AWS API using Python script.
- Creates French version of the attribute from the returned translated value.
- Removes UTF8 Character code returned from translated results.

#### CSW_INSERT

This transformer is designed to function in all data ETL activities for all new data records and performs the following tasks:

- Tests for the number of transfer options and distribution formats, and filters the datasets according to their number.
- Selects the appropriate XML insert template based on the results of the previous test.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### CSW_UPDATE

This transformer is designed to function in all data ETL activities for all updated data records and performs the following tasks:

- Tests for the number of transfer options and distribution formats, and filters the datasets according to their number.
- Selects the appropriate XML update template based on the results of the previous test.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### NOTIFY_CREATE

This transformer is designed to function in all CREATE workspaces and creates an email message of ETL results for system administrators.

##### Insert Records Notification

This section performs the following tasks:
- Gets count of inserted records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

##### Notification Compliler and eMailer

This section performs the following tasks:
- Gets the current data and time.
- Concatenates insert records or no records to insert notifcation strings, update records or no records to update notification strings, plus date and time into one message string
- Emails the message string to an adminstrator.

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

##### Notification Compliler and eMailer

This section performs the following tasks:
- Gets the current data and time.
- Concatenates insert records or no records to insert notifcation strings, update records or no records to update notification strings, number of obsolete records deleted, plus date and time into one message string.
- Emails the message string to an adminstrator.

#### POSTTRANSLATE_3

This transformer is designed to function in all workspaces and removes duplicates of distribution format items by performing the following tasks:
- Copies all resource_format attributes into list attributes.
- Removes all list attribute duplicates.
- Renames remaining list attributes to distribution_format attributes

### Provincial/Territorial Specific Transformers

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

This section sends each concatentated query instance using a GET http method to the Alberta Opend Data API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

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
- Tests data collection end dates for string length = 4, which is indicative of the year only **NOTE: Data collection end dates with no value are left blank. 
- Adds '0101' to complete date strings that have year only.
- Converts data collection end date from yyyymmdd format to yyyy-mm-dd format.
- Adds additional global attributes not available in extracted data.
- Changes unique ID values to required lower case.
- Outputs to Date/Time Testing.

###### Date/Time Testing

This section exists primarily for debugging purposes and can test for records that were created backdated to a specific number of days or months.  It's default setting for normal 
operation is 0, which nullifies the test.  All data extracted from the Alberta Open Data API stream and the Alberta Geospatial Data API stream converges here.

###### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not found, a generic name, 
'AB Data Link' is inserted to the resource name attribute.

###### Excess Attribute Removal

This section performs the following tasks:

- Removes out of scope attributes.
- Output is directed to the AWS_TRANSLATE transformer.

##### AB_POSTTRANSLATE_1

This custom transformer is the first stage following the AWS Translate custom transformer.  It enhances Alberta datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'AB_Create' and 'AB_Update' workspaces.  Input is received from the AWS_TRANSLATE transformer.

This transformer performs the following tasks:

###### Temporal Extents Refiner

Tests and inserts required values where missing, and formats date.

###### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  

###### Second Contact Test

This section tests for a second contact as required by the XML template.  If the second contact is missing, it is replaced with the first contact.

###### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'asNeeded'.  The corresponding RI_Code is then applied.

###### Spatial Representation Type Refiner

This section tests that Spatial Representation Type values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  The corresponding RI_Code and French language translation is then applied.

###### Progress Code Refiner

This section tests that Progress code values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'onGoing'.  The corresponding RI_Code and French language translation is then applied.  

The transformer outputs to AB_POSTTRANSLATE_2 transformer.

##### AB_POSTTRANSLATE_2

This custom transformer is the second stage following the AWS Translate custom transformer.  It enhances Alberta datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'AB_Create' and 'AB_Update' workspaces.

This transformer performs the following functions:

###### File Format Refiner

There are up to six transfer options (data links) available in Alberta datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis 
of all Alberta data has identified all the potential incorrect variations of required file format names (i.e.: 'uri' should be 'HTML', 'REST' should be 'ESRI REST').  There are a number 
of data formats that are not a variation of any valid data type.  This section tests for these valid formats found in Alberta datasets and renames them to the valid option 
'other' accordingly.

List of validated file formats can be found here:

-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

###### ZIP Link Creator

This section creates a zip file download link where conditions where the third URL has no value and the first URL is not an ESRI REST link

The transfomer outputs to POSTTRANSLATE_3 transfomer.

##### AB_POSTTRANSLATE_4

This custom transformer is the fourth stage following the AWS Translate custom transformer.  It enhances Alberta datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'AB_Create' and 'AB_Update' workspaces.

This transformer performs the following functions:

###### Keyword Attributor

Alberta datasets have a maximum of nine keyword values, and XML templates are formatted to accommodate nine keyword values.  Not all datasets utilize nine keyword values and the 
FGP harvester will reject the XML file if any of the keyword values are NULL.  This section tests each keyword attribute, English and French, for NULL values, and substitutes a 
generic value accordingly.   

  **English Generic Keyword Values:**

  - Geomatics
  - Open Data
  - Open Government
  - AB Data
  - Open Source
  - Public Data
  - Government Data
  - Alberta Data
  - Government of Alberta

  **French Generic Keyword Values:**

  - Géomatique
  - Données ouvertes
  - Gouvernement ouvert
  - Données AB
  - Source ourverte
  - Données publiques
  - Données gouvernementales
  - Données de l'Alberta
  - Gouvernement de l'Alberta
  
###### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

###### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to six in Alberta datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

###### ESRI REST Formatter

Most datasets from Alberta have an HTML link as the first resource_url.  There are a small number that have ESRI REST as the first resource_url.  This tests for the ESRI REST as the first resource_url.

For ESRI REST formatted URL, this transformer creates the  second url and associated attributes required by the FGP for ESRI REST distribution formats.

Features not processed in this section are directed to the WMS Formatter.  Processed features bypass the WMS Formatter and are directed to the Distribution Formatter.

###### WMS Formatter

This section tests resource_format attributes (there are up to six in Alberta datasets) in transferOptions for 'WMS' value, that require an additional French WMS format for each 
English format as a transferOption to facilitate links to the web mapping service.  This section will insert a French WMS formatted transferOption immediately following the English 
WMS transferOption, and move subsequent transferOptions down the sequence accordingly by reassiging the attribute index numbers.  

This section assigns all WMS requirements to each English and French transferOption: 

- xlink:role 
- protocol
- locale
- language
- name
- URL
- format 

###### Distribution Version Formatter

This section creates distribution format versions for all WMS formats as this is the default for Alberta WMS.  Other distribution format versions are not provided.  Data from the WMS Formatter and the ESRI REST Formtter converge here.

###### INSERT/UPDATE Test

This section tests if the POST method has been determined to be 'INSERT' or 'UPDATE'

Transformer output is then directed to the CSW_INSERT transformer for all INSERT workspaces, and for all UPDATE workspaces, directed to either the CSW_INSERT or CSW_UPDATE transformers.

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
- Exposes the unique ID elements from the returned XML file,
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

This section sends each concatentated query instance using a GET http method to the Alberta Opend Data API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

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
- Tests data collection end dates for string length = 4, which is indicative of the year only **NOTE: Data collection end dates with no value are left blank. 
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
- Outputs the the NO_DELETED_RECORDS_COUNT and DELETED_RECORDS_COUNT to NOTIFY_UPDATE transformer.

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

#### British Columbia

##### BC_CREATE_PRETRANSLATE

This transformer is designed to function exclusively in the BC_CREATE workspace.  It queries the British Columbia open data API and filters the returned data by performing the following tasks:

###### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.  It is set
at default to perform 10 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

###### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

###### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not Open Government License - British Columbia.
- Filters out data records that are password access only.
- Adds additional required attributes not available in extracted data
- Renames attributes that have index array to attribute name format that can be read by the XML templater.
- Formats all date fields to ISO yyyy-mm-dd
- Filters out duplicate datasets that BC has already republished from NRCan.

###### Date/Time Testing

This section exists primarily for debugging purposes and can test for records that were created backdated to a specific number of days or months.  It's default setting for normal 
operation is 0, which nullifies the test.

###### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not found, a generic name, 
'BC Data Link' is inserted to the resource name attribute.

###### Excess Attribute Removal

This section performs the following tasks:

- Removes out of scope attributes.
- Output is directed to the AWS_TRANSLATE transformer.

##### BC_POSTTRANSLATE_1

This custom transformer is the first stage following the AWS Translate custom transformer.  It enhances British Columbia datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'BC_Create' and 'BC_Update' workspaces.

This transformer performs the following functions:

###### Temporal Extents Creator

This section tests for required temporal extents (data collection start and end dates) and corrects if necessary by performing the following tasks:

- Tests if data_collection_start_date is present
- Sets data collection start date to 0001-01-01 if missing
- Formats data_collection_start_date to ISO yyyy-mm-dd format if present.
- Tests if data_collection_end_date is present.
- Formats data_collection_end_date to ISO yyyy-mm-dd format if present.
- **NOTE**: data_collection_end_date is not a mandatory value and no action is taken if data is absent.

###### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  
All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  
A list of all RI Codes, including RI Role Codes, can be found here:

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

###### Second Contact Testing

Contact fields in XML templates cannot be incomplete.  Every data record has at least one contact.  The XML template allows for two.  This section tests if second contact exists 
in data record, then substitutes all second contact associated values with first contact values if second contact is missing.

  **Substituted values:**

  - contact name
  - contact email
  - contact role
  - contact role french
  - RI role code
  
###### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revises them to default 'asNeeded'.  The corresponding RI_Code 
is then applied to all values.

This transformer outputs to the BC_POSTTRANSLATE_2 transformer.

##### BC_POSTTRANSLATE_2

This custom transformer is the second stage following the AWS Translate custom transformer.  It enhances British Columbia datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'BC_Create' and 'BC_Update' workspaces.

###### File Format Refiner

There are up to ten transfer options (data links) available in BC datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis of all BC data
has identified all the potential incorrect variations of required file format names (i.e.: 'kmz' should be 'KMZ', 'Esri File Geodatabase' should be 'FGDB/GDB').  This section tests for all
the variations found in BC datasets and corrects them to conforming values where required.

List of validated file formats can be found here:

-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

This transformer outputs to the POSTTRANSLATE_3 transformer.

##### BC_POSTTRANSLATE_4

This custom transformer is the fourth stage following the AWS Translate custom transformer.  It enhances British Columbia datasets post translation to ensure conformity to ISO 19115 HNAP standards.  It can run in both the 'BC_Create' and 'BC_Update' workspaces.

This transformer performs the following tasks:

###### Keyword Attributor

Some BC datasets have been found to have over one hundred keyword values (or tags as they are named when returned by the JSON query).  In order to make this portion of the data more 
manageable, the XML templates have been formatted to allow for nine keywords only, which is aligned with the maximum of nine keywords that are returned with Alberta datasets.  The FGP 
harvester will reject the XML file if any of the keyword values are NULL.  This section tests each tag attribute, English and French, for NULL values, and substitutes a 
generic value accordingly.   

  **English Generic Keyword Values:**

  - Geomatics
  - Open Data
  - Open Government
  - BC Data
  - Open Source
  - Public Data
  - Government Data
  - British Columbia Data
  - Government of British Columbia

  **French Generic Keyword Values:**

  - Géomatique
  - Données ouvertes
  - Gouvernement ouvert
  - Données de la C.-B.
  - Source ourverte
  - Données publiques
  - Données gouvernementales
  - Données de la Colombie-Britannique
  - Gouvernement de la Colombie-Britannique

###### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

###### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to ten in BC datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

###### WMS Formatter

This section tests resource_format attributes (there are up to ten in BC datasets) in transferOptions for 'WMS' value, that require an additional French WMS format for each English format 
as a transferOption to facilitate links to the web mapping service.  This section will insert a French WMS formatted transferOption immediately following the English WMS transferOption, 
and move subsequent transferOptions down the sequence accordingly by reassiging the attribute index numbers.  

This section assigns all WMS requirements to each English and French transferOption: 

- xlink:role 
- protocol
- locale
- language
- name
- URL
- format

**NOTE:** The FGP harvester will only accept one WMS transfer option each for English and French.  If the source data contains more than one WMS transfer option prior to the 
addition of the French transfer option, it will exceed the maximum and the record will be rejected.  As of the time of this writing, three BC datasets exceed the maximum WMS transfer 
options allowed.

###### Distribution Version Formatter

This section creates distribution format versions for all WMS formats as this is the default for Alberta WMS.  Other distribution format versions are not provided.  Data from the WMS Formatter and the ESRI REST Formtter converge here.

###### INSERT/UPDATE Test

This section tests if the POST method has been determined to be 'INSERT' or 'UPDATE'

Transformer output is then directed to the CSW_INSERT transformer for all INSERT workspaces, and for all UPDATE workspaces, directed to either the CSW_INSERT or CSW_UPDATE transformers.

##### BC_UPDATE_PRETRANSLATE

This custom transformer is the first stage of daily extraction of new or updated data from the BC Data API, and inserting to the CSW.  It also identifies obsolete records for removal from the CSW.  It is intended to run as a component of the 'BC_Update' workspace.

This transformer performs the following tasks:

###### CSW UUID Reader

This section extracts the unique ID's from all data records currently loaded to the CSW by performing the following tasks:

- Creates attribute required to perform CSW search with XML file (Columbia)
- Loads the Get Records XML template.
- Formats Get Records XML template.
- Validates the Get Records XML template.
- Posts XML to PyCSW using Python script and returns XML with dataset summary.
- Exposes the unique ID elements from the returned XML file,
- Extracts string snippet from the unique ID element.
- Outputs to the Obsolete Records Removal section.

###### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.  It is set
at default to perform 10 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

###### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query.

###### Obsolete Records Removal

This section removes obsolete data records by performing the following tasks:

- Inputs all data output from CSW UUID Reader and data query.
- Retains only the UUID from each data input and removes all other attributes.
- Merges unique ID's from the CSW with unique ID's from the current data search.
- Loads the Delete Records XML template for each CSW Data Record not found in the current data search.
- Formats Delete Records XML's.
- Validates Delete Records XML's.
- Posts Delete Records XML for each UUID in the CSW not found in the current data search, removing the obsolete record.
- Outputs the the NO_DELETED_RECORDS_COUNT and DELETED_RECORDS_COUNT to NOTIFY_UPDATE transformer.

###### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not Open Government License - British Columbia.
- Filter out records that are not Geographic.
- Filters out data records that are password access only.
- Creates global attributes specific to British Columbia data.
- Renames attributes that have index array to attribute name format that can be read by the XML templater.
- Formats all date fields to ISO yyyy-mm-dd
- Filters out duplicate datasets that BC has already republished from NRCan.

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
'BC Data Link' is inserted to the resource name attribute.

###### Excess Attribute Removal

This section performs the following tasks:

- Removes out of scope attributes.
- Output is directed to the AWS_TRANSLATE transformer.

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
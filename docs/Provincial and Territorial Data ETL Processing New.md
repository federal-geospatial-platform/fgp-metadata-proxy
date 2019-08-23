
Provincial and Territorial Extraction, Transformation and Loading Processes
==========

- [Table of Contents](#table-of-contents)
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes)
  - [Oveview](#overview)
    - [Workspaces](#workspaces)
	- [Custom Transformers](#custom-transformers)
	- [XML Templates](#xml-templates)
	- [Other PyCSW Tools](#other-pycsw-tools)
  - [Alberta](#alberta)
    - [Overview](#overview-1)
    - [AB_CREATE Workspace Detail](#ab_create-workspace-detail)
	  - [AB_CREATE_PRETRANSLATE](#ab_create_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate)
	  - [AB_POSTRANSLATE_1](#ab_posttranslate_1)
	  - [AB_POSTRANSLATE_2](#ab_posttranslate_2)
	  - [POSTTRANSLATE_3](#posttranslate_3)
	  - [AB_POSTRANSLATE_4](#ab_posttranslate_4)
	  - [CSW_INSERT](#csw_insert)
	  - [NOTIFY_CREATE](#notify_create)
	- [AB_UPDATE Workspace Detail](#ab_update-workspace-detail)
	  -[AB_UPDATE_PRETRANSLATE](#ab_update_pretranslate)
	  - [AWS_TRANSLATE](#aws_translate-1)
	  - [AB_POSTRANSLATE_1](#ab_posttranslate_1-1)
	  - [AB_POSTRANSLATE_2](#ab_posttranslate_2-1)
	  - [POSTTRANSLATE_3](#posttranslate_3-1)
	  - [AB_POSTRANSLATE_4](#ab_posttranslate_4-1)
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
	  - [POSTTRANSLATE_3](#posttranslate_3-1)
	  - [BC_POSTRANSLATE_4](#bc_posttranslate_4-1)
	  - [CSW_INSERT](#csw_insert-3)
	  - [CSW_UPDATE](#csw_update-1)
	  - [NOTIFY_UPDATE](#notify_update)
	  - [Data Clear](#data-clear)
	  - [Query Loop Creation](#query-loop-creation)
	  - [Data Query](#data-query)
	  - [Attribute Management](#attribute-management)
	  - [Date/Time Testing](#datetime-testing)
	  - [Resource Name Tester](#resource-name-tester)
	  - [DeepL Translation](#deepl-translation)
	  - [Temporal Extents Creator](#temporal-extents-creator)
	  - [Role Refiner](#role-refiner)
	  - [Second Contact Testing](#second-contact-testing)
	  - [Update Cycle Refiner](#update-cycle-refiner)
	  - [Spatial Representation Type Refiner](#spatial-representation-type-refiner)
	  - [Progress Code Refiner](#progress-code-refiner)
	  - [File Format Refiner](#file-format-refiner)
	  - [Keyword Attributor](#keyword-attributor)
	  - [SSL Protocol Test - Online Resource](#ssl-protocol-test---online-resource)
	  - [SSL Protocol Test - Transfer Options](#ssl-protocol-test---transfer-options)
	  - [WMS Formatter](#wms-formatter)
	  - [PyCSW Record Insert](#pycsw-record-insert)
	  - [Local Directory Writers](#local-directory-writers)
	  - [Insert Records Notification](#insert-records-notification)
	  - [Notification Compiler and eMailer](#notification-compiler-and-emailer)
    - [AB_Data_NewAndUpdatedRecords](#ab_data_newandupdatedrecords)
	  - [Query Loop Creation](#query-loop-creation-1)
	  - [Data Query](#data-query-1)
	  - [Attribute Management](#attribute-management-1)
	  - [Date/Time Testing](#datetime-testing-1)
	  - [No Records to Insert/Update Notification](#no-records-to-insertupdate-notification)
	  - [Resource Name Tester](#resource-name-tester-1)
	  - [DeepL Translation](#deepl-translation-1)
	  - [Temporal Extents Creator](#temporal-extents-creator-1)
	  - [Role Refiner](#role-refiner-1)
	  - [Second Contact Testing](#second-contact-testing-1)
	  - [Update Cycle Refiner](#update-cycle-refiner-1)
	  - [Spatial Representation Type Refiner](#spatial-representation-type-refiner-1)
	  - [Progress Code Refiner](#progress-code-refiner-1)
	  - [File Format Refiner](#file-format-refiner-1)
	  - [Keyword Attributor](#keyword-attributor-1)
	  - [SSL Protocol Test - Online Resource](#ssl-protocol-test---online-resource-1)
	  - [SSL Protocol Test - Transfer Options](#ssl-protocol-test---transfer-options-1)
	  - [WMS Formatter](#wms-formatter-1)
	  - [Insert/Update Filter](#insertupdate-filter)
	  - [PyCSW Record Insert](#pycsw-record-insert-1)
	  - [PyCSW Record Update](#pycsw-record-update)
	  - [Local Directory Writers](#local-directory-writers-1)
	  - [Insert Records Notification](#insert-records-notification-1)
	  - [Update Records Notification](#update-records-notification)
	  - [Notification Compiler and eMailer](#notification-compiler-and-emailer-1)
  - [British Columbia](#british-columbia-1)
    - [Overview](#overview-3)
    - [BC_Data_AllRecords Workspace/BC_Data_ClearCSW Detail](#bc_data_allrecords-workspacebc_data_clearcsw-detail)
	  - [Data Clear](#data-clear-1)
	  - [Query Loop Creation](#query-loop-creation-2)
	  - [Data Query](#data-query-2)
	  - [Attribute Management](#attribute-management-2)
	  - [Date/Time Testing](#datetime-testing-2)
	  - [Resource Name Tester](#resource-name-tester-2)
	  - [DeepL Translation](#deepl-translation-2)
	  - [Temporal Extents Creator](#temporal-extents-creator-2)
	  - [Role Refiner](#role-refiner-2)
	  - [Second Contact Testing](#second-contact-testing-2)
	  - [Update Cycle Refiner](#update-cycle-refiner-2)
	  - [File Format Refiner](#file-format-refiner-2)
	  - [Keyword Attributor](#keyword-attributor-2)
	  - [SSL Protocol Test - Online Resource](#ssl-protocol-test---online-resource-2)
	  - [SSL Protocol Test - Transfer Options](#ssl-protocol-test---transfer-options-2)
	  - [WMS Formatter](#wms-formatter-2)
	  - [PyCSW Record Insert](#pycsw-record-insert-2)
	  - [Local Directory Writers](#local-directory-writers-2)
	  - [Insert Records Notification](#insert-records-notification-2)
	  - [Notification Compiler and eMailer](#notification-compiler-and-emailer-2)
    - [BC_Data_NewAndUpdatedRecords](#bc_data_newandupdatedrecords)
	  - [Data Query](#data-query-3)
	  - [Attribute Management](#attribute-management-3)
	  - [Date/Time Testing](#datetime-testing-3)
	  - [No Records to Insert/Update Notification](#no-records-to-insertupdate-notification-1)
	  - [Resource Name Tester](#resource-name-tester-3)
	  - [DeepL Translation](#deepl-translation-3)
	  - [Temporal Extents Creator](#temporal-extents-creator-3)
	  - [Role Refiner](#role-refiner-3)
	  - [Second Contact Testing](#second-contact-testing-3)
	  - [Update Cycle Refiner](#update-cycle-refiner-3)
	  - [File Format Refiner](#file-format-refiner-3)
	  - [Keyword Attributor](#keyword-attributor-3)
	  - [SSL Protocol Test - Online Resource](#ssl-protocol-test---online-resource-3)
	  - [SSL Protocol Test - Transfer Options](#ssl-protocol-test---transfer-options-3)
	  - [WMS Formatter](#wms-formatter-3)
	  - [Insert/Update Filter](#insertupdate-filter-1)
	  - [PyCSW Record Insert](#pycsw-record-insert-3)
	  - [PyCSW Record Update](#pycsw-record-update-1)
	  - [Local Directory Writers](#local-directory-writers-3)
	  - [Insert Records Notification](#insert-records-notification-3)
	  - [Update Records Notification](#update-records-notification-1)
	  - [Notification Compiler and eMailer](#notification-compiler-and-emailer-1)
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

-   **(p-t_abbreviation)_CREATE_(version_number).fmw:** The CREATE workspaces are for extracting, tranforming and loading a complete dataset to an empty Catalogue Service for the Web (CSW).  Its intended use is for initial creation of a CSW, or in the event an entire CSW needs to be reloaded.  This can be run manually from FME Server.
-  **(p-t_abbreviation)_UPDATE_(version_number).fmw:**  The UPDATE workspaces filter, extract, transform and load new or updated data records to the CSW.  It also reads all existing data records already in the CSW and deletes any records no longer found in the source data.  Theses workspaces run on a daily schedule on the FME Server.

### Custom Transformers

The extensive transformers required for metadata ETL have been aggregated into a series of custom transformers, each defining a key step in the ETL process.  These transformers can be broken down into three types:

-   **Workspace Exclusive Transformers:** These are exclusive to either a single provincial/territorial CREATE or UPDATE workspace.
-  **Provincial/Territorial Exclusive Transformers:** These are exclusive to a provincial or territorial ETL process, but can be used in that province/territory's CREATE or UPDATE transformers.
-  **Universal Transformers:** These contain processes that are universal to any workspace.

### XML Templates

The workspaces utilize 104 XML templates to retreive, load and delete data from the PyCSW.

-   **FGP_GetRecords.xml:** This XML file posts a request to the PyCSW and retrieves the unique ID from every data records contained therein.

-  **FGP_DeleteById.xml:** Following the extraction of unique ID"s from the PyCSW and validation of the unique ID's against unique ID's retreived from an agency's API, this XML file removes obsolete records by their unique ID by posting to the PyCSW.  

-  **FGP_XML_Insert_Template_(number).xml:**  There are 51 'insert' XML document templates that are denoted by 'Insert' tags at the beginning and end of the document, the number of distribution formats and the number of transfer options.  Data analysis has shown that there are no more than six distribution formats and no more than eleven transfer options in any given dataset.  The number at the end of the file name is indicative of the number of transfer options, followed by number of distribtion formats.  The numbering is indexed, beginning at '0', where 0 indicates a count of 1.  For example, FGP_XML_Insert_Template_1-0.xml indicates the template can accommodate 2 transfer options and 1 distribtion format, and FGP_XML_Insert_Template_10-3.xml indicates the template can accommodate 11 transfer options and 4 distribution formats.

-  **FGP_XML_Update_Template_(number).xml:**  There are 51 'update' XML document templates that are denoted by 'Update' tags at the beginning and end of the document, the number of distribution formats and the number of transfer options.  Data analysis has shown that there are no more than six distribution formats and no more than eleven transfer options in any given dataset.  The number at the end of the file name is indicative of the number of transfer options, followed by number of distribtion formats.  The numbering is indexed, beginning at '0', where 0 indicates a count of 1.  For example, FGP_XML_Insert_Template_1-0.xml indicates the template can accommodate 2 transfer options and 1 distribtion format, and FGP_XML_Insert_Template_10-3.xml indicates the template can accommodate 11 transfer options and 4 distribution formats.

### Other PyCSW Tools

-   **EMPTY CSW Python Scripts:** These are intended for admin purposes only in the event a CSW has to be cleared of all data.  These scripts run manually and must be executed prior to running a CREATE workspace.  It will clear 1000 records at a time from the CSW and will have to be run multiple times if the CSW count exceeds 1000.

## Workspaces

### Alberta

#### Overview

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes using two approaches:

--   **Alberta Open Data Catalogue**: Alberta ISO 19115 compliant data is extracted by exposing data from CKAN API [Alberta's Open Data Catalogue](https://open.alberta.ca/opendata), extracting a JSON (Javascript Object Notation) file, and subsequently, via the JSON file, an XML file in Geospatial Catalog. The approach going through the Open Data Catalog first is required as the unique ID's from the Open Data are required due to inconsistencies in the unique ID's used in the subsequently exposed XML files.

--  **Alberta Geospatial Catalog**:  A small amount of ISO 19139 compliant data using exclusively ESRI REST services is unavailable in the Alberta Open Data Catalog and is exposed directly from [Alberta Geospatial Catalogue](https://geodiscover.alberta.ca/geoportal).  The unique ID naming conventions are accurate with this data subset which allows for direct extraction.  The remainder of ISO 19139 data not exposing ESRI REST services that is found in the Alberta geospatial catalogue has been found to be largely incomplete and unusable.  

Attributes required to meet mandatory requirements for individual XML (Extensible Markup Language) files are extracted from both the exposed JSON file and XML files, each representing and defining a unique dataset, that are published to a CSW (Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces use a series of custom transformers appropriately placed to address attribute deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx)

The Alberta Metadata FME Workspaces can be found here:

-   [Alberta FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/FME_Workspaces/AB)

- **NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

#### AB_CREATE Workspace Detail

The AB_CREATE workspace utilizes the following sequence of custom transformers:

##### AB_CREATE_PRETRANSLATE

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### AWS_TRANSLATE

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### AB_POSTTRANSLATE_1

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### AB_POSTTRANSLATE_2

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### POSTTRANSLATE_3

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### AB_POSTTRANSLATE_4

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### CSW_INSERT

Selects appropriate XML insert template and posts XML to the CSW.

##### NOTIFY_CREATE

E-mails processing results to administrator.

#### AB_UPDATE Workspace Detail

The AB_UPDATE workspace utilizes the following sequence of custom transformers:

##### AB_UPDATE_PRETRANSLATE

Queries both the Alberta open government portal API and the Alberta geospatial API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against Alberta API's for obsolete data.  Deletes records from CSW that are no longer found in Alberta open data.  

##### AWS_TRANSLATE

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### AB_POSTTRANSLATE_1

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### AB_POSTTRANSLATE_2

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### POSTTRANSLATE_3

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### AB_POSTTRANSLATE_4

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### CSW_INSERT

Selects appropriate XML insert template for all new datasets and posts XML to the CSW.

##### CSW_UPDATE

Selects appropriate XML update template for all updated datasets and posts XML to the CSW.

##### NOTIFY_UPDATE

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

The BC_CREATE workspace utilizes the following sequence of custom transformers:

##### BC_CREATE_PRETRANSLATE

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data.  It also contains a date filter for admin testing purposes only.

##### AWS_TRANSLATE

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### BC_POSTTRANSLATE_1

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### BC_POSTTRANSLATE_2

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### POSTTRANSLATE_3

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### BC_POSTTRANSLATE_4

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### CSW_INSERT

Selects appropriate XML insert template and posts XML to the CSW.

##### NOTIFY_CREATE

E-mails processing results to administrator.

#### BC_UPDATE Workspace Detail

The BC_UPDATE workspace utilizes the following sequence of custom transformers:

##### BC_UPDATE_PRETRANSLATE

Queries the British Columbia open government portal API, exposes returned attributes and filters data by open, geospatial data and date.  Tests for revised data and new data records.  Reads unique ID's from the existing CSW dataset and tests against British Columbia's API for obsolete data.  Deletes records from CSW that are no longer found in British Columbia open data.  

##### AWS_TRANSLATE

Sends extracted English text attributes, that require French equivalents, to Amazon Web Service Translate, returns French translation and creates new attributes from the translation. 

##### BC_POSTTRANSLATE_1

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### BC_POSTTRANSLATE_2

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### POSTTRANSLATE_3

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### BC_POSTTRANSLATE_4

Performs post translation transformations to ensure conformity to ISO 19115 HNAP requirements.

##### CSW_INSERT

Selects appropriate XML insert template for all new datasets and posts XML to the CSW.

##### CSW_UPDATE

Selects appropriate XML update template for all updated datasets and posts XML to the CSW.

##### NOTIFY_UPDATE

E-mails processing results to administrator.

#### Data Clear

This section clears the CSW completely, and if utilizing the option to write all XML output to a local directory, clears the directory.  It utilizes the following steps:

-   **Workspace Runner:** This workspace runner initiates the AB_Data_ClearCSW workspace containing a custom transformer built on a loop.  The workspace runner is required to allow the loops 
to complete before initiating the rest of the processes in this tool.  
The custom transformer (Clear_PyCSW) is located in the FME Transformers folder and must be copied to any new FME environments in order for this tool to load.  Any edits required to this tool 
are performed by opening up the transformer itself in its home directory using FME Desktop.  
The loop is required because the sqlLite database which hosts the data for the CSW is limited in the number of records it can delete at a time.  This tool will delete the number of records 
that is set in the maxrecords property in default.cfg stored in the pycsw-2.2.0 directory.  The default setting for maxrecords is 100.  The default setting for number of loop iterations 
for this tool is 100, which allows for deletion of a maximum of 10000 records in the CSW database.  

-  **Clear XML_Results directory:** A system caller is used to clear the XML_Results directory.  This directory is not mandatory for the CSW, but creates local copies of XML files that were 
successfully published to the CSW.  Used primarily in development and could be disabled in a production environment by disabling the writers found in the Local Directory Writers bookmark. 

-  **Clear XML Failed directory:** A system caller is used to clear the XML_Failed directory.  This directory is not mandatory for the CSW, but creates local copies of XML files that 
failed to publish to the CSW.  Used primarily in development and could be disabled in a production environment by disabling the writers found in the Local Directory Writers bookmark.

#### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the Alberta Data API as the API will only return 1000 records per query, less than that of the BC database.  
It is set at default to perform 20 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://open.alberta.ca/api/3/action/package_search?start=@Value(start_feature)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 20000 records, and, at the time of writing, there are approximately 17,000 open data records in Alberta open data.

#### Data Query

This section sends each concatentated query instance using a GET http method to the Alberta API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

#### Attribute Management

Specific resource URL's exposed in the Alberta API link to a geospatial CSW, where the second resource URL in each data record is an XML file defining a catalog service record.

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Tests resource URL domains exposed by the JSON query that contain 'geospatial' in their value, and filters out other records.
- Filters out duplicate datasets that BC has already republished from NRCan.
- Tests second resource URL for internal Alberta CSW domain (oxpgdaws01.env.gov.ab.ca:8080) in URL string.  This second resource URL is always an XML file that defines CSW record.
- Tests second resource URL for public domain string used for XML CSW queries.
- Replaces internal Alberta CSW domain string snippet in second resource URL with publicly accessible domain string snippet (https://geodiscover.alberta.ca)
- Filters out second resource URL that are not links to Alberta geospatial by testing for absence of 'csw' in URL string.
- Gets XML file from edited second resource URL.
- Breaksdown attribute fields in retreived XML document.
- Extracts attribute keys/values from XML document using the following XQuery expression:
  - [Alberta X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-XQuery.xml)
- Exposes required extracted attributes from X-Query and earlier JSON query.
- Copies selected attributes to act as proxies for other required values in XML output template.
- Renames indexed and other specific attributes to match XML template

#### Date/Time Testing

This section exists primarily for debugging purposes and can test for records that were created backdated to a specific number of days or months.  It's default setting for normal 
operation is 0, which nullifies the test.

#### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not find, a generic name, 
'AB Data Link' is inserted to the resource name attribute.

#### DeepL Translation

This section translates the following attributes from English to French using the DeepL language translation API:

- title
- notes
- sector
- all exposed tags attributes (maximum 9)
- all exposed resource_name attributes (maximum 6)

This section operates using the following steps:

- Removes failure causing excess whitespace from all attribute values to be translated.
- Concatenates query string to send to the DeepL API:
  - https://api.deepl.com/v2/translate?auth_key=$(DEEPL_KEY)&text=@Value(title)&source_lang=EN&target_lang=FR&split_sentences=1&preserve_formatting=1
  - **NOTE:** 'DEEPL_KEY' variable in concatenated value is the authorization key for DeepL API and is stored as a published parameter in FME, 'title' is the variable to be translated.
- Sends query string to the DeepL API.
- Substitutes the attribute value with hard coded error message in French in the event of translation failure.
- Parses the JSON string returned from the query to expose translated value.
- Creates French version of the attribute from translated value.
- Removes UTF8 Character code returned from translated results.

#### Temporal Extents Creator

This section tests for required temporal extents (data collection start and end dates) and creates default extents where missing.  The default temporal extents are set as follows:

- **data_collection_start_date:** 20 years prior to date data was processed by FME workspace.
- **data_collection_end_date:** the date data was processed by FME workspace.

#### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  
All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  
A list of all RI Codes, including RI Role Codes, can be found here:

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Second Contact Testing

Contact fields in XML templates cannot be incomplete.  Every data record has at least one contact.  The XML template allows for two.  This section tests if second contact exists 
in data record, then substitutes all second contact associated values with first contact values if second contact is missing.

  **Substituted values:**

  - contact name
  - contact email
  - contact role
  - contact role french
  - RI role code

#### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revises them to default 'asNeeded'.  The corresponding RI_Code 
is then applied to all values.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Spatial Representation Type Refiner

This section tests that Spatial Representation Type values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  The corresponding RI_Code 
and French language translation is then applied.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Progress Code Refiner

This section tests that Progress code values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  The corresponding RI_Code 
and French language translation is then applied.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### File Format Refiner

There are up to ten transfer options (data links) available in Alberta datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis 
of all Alberta data has identified all the potential incorrect variations of required file format names (i.e.: 'uri' should be 'HTML', 'REST' should be 'ESRI REST').  There are a number 
of data formats that are not a variation of any valid data type.  This section tests for these valid formats found in Alberta datasets and renames them to the valid option 
'other' accordingly.

List of validated file formats can be found here:

-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

#### Keyword Attributor

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

#### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

#### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to six in Alberta datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

#### WMS Formatter

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

#### PyCSW Record Insert

Alberta datasets contain has a minimum of two and a maximum of six transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially 
six transfer options in each dataset (two to seven), requiring six templates.  

The XML insert templates can be found here:

-   [Alberta XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/AB/AB_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### Local Directory Writers

This section outputs each XML file to a local directory, sorted by succesful load or failure.  It is disabled by default but can be enabled if debugging of errors is required.

#### Insert Records Notification

This section performs the following tasks:

- Gets count of records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Notification Compliler and eMailer

This section performs the following tasks:

- Gets the current date and time.
- Concatenates insert records notifcation string plus date and time into one message string
- Emails the message string to an adminstrator.

### AB_Data_NewAndUpdatedRecords

#### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the Alberta Data API as the API will only return 1000 records per query, less than that of the BC database.  
It is set at default to perform 20 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://open.alberta.ca/api/3/action/package_search?start=@Value(start_feature)&rows=$(QUERY_ITERATIONS) 
  
- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME.
  
The current default settings will return a total of 20000 records, and, at the time of writing, there are approximately 17,000 open data records in Alberta open data.

#### Data Query

This section sends each concatentated query instance using a GET http method to the Alberta API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

#### Attribute Management

Specific resource URL's exposed in the Alberta API link to a geospatial CSW, where the second resource URL in each data record is an XML defining a catalog service record.

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Tests resource URL domains exposed by the JSON query that contain 'geospatial' in their value, and filters out other records.
- Filters out duplicate datasets that BC has already republished from NRCan.
- Tests second resource URL for internal Alberta CSW domain (oxpgdaws01.env.gov.ab.ca:8080) in URL string.  This second resource URL is always an XML file that defines CSW record.
- Tests second resource URL for public domain string used for XML CSW queries.
- Replaces internal Alberta CSW domain string snippet in second resource URL with publicly accessible domain string snippet (https://geodiscover.alberta.ca)
- Filters out second resource URL that are not links to Alberta geospatial by testing for absence of 'csw' in URL string.
- Gets XML file from edited second resource URL.
- Breaksdown attribute fields in retreived XML document.
- Extracts attribute keys/values from XML document using the following XQuery expression:
  - [Alberta X-Query](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/Alberta-XQuery.xml)
- Exposes required extracted attributes from X-Query and earlier JSON query.
- Copies selected attributes to act as proxies for other required values in XML output template.
- Renames indexed and other specific attributes to match XML template

#### Date/Time Testing

This section performs the following tasks:

- Extracts current date.
- Calculates time since last time tool processed.  Default setting is 1 day and is accessed in published parameter TIME_FILTER_DAYS.
- Tests for new records by comparing record_publish_date attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute with value 'Insert' for all new records.
- After new records are filtered, tests remainder for updated records by comparing record_last_modified attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute 'Update' for all updated records.

#### No Records to Insert/Update Notification

- Verifies number of records that are to be inserted or updated.
- Concatenates message string for notification if there are no records to be inserted and/or updated.

#### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not find, a generic name, 
'AB Data Link' is inserted to the resource name attribute.

#### DeepL Translation

This section translates the following attributes from English to French using the DeepL language translation API:

- title
- notes
- sector
- all exposed tags attributes (maximum 9)
- all exposed resource_name attributes (maximum 6)

This section operates using the following steps:

- Removes failure causing excess whitespace from all attribute values to be translated.
- Concatenates query string to send to the DeepL API:
  - https://api.deepl.com/v2/translate?auth_key=$(DEEPL_KEY)&text=@Value(title)&source_lang=EN&target_lang=FR&split_sentences=1&preserve_formatting=1
  - **NOTE:** 'DEEPL_KEY' variable in concatenated value is the authorization key for DeepL API and is stored as a published parameter in FME, 'title' is the variable to be translated.
- Sends query string to the DeepL API.
- Substitutes the attribute value with hard coded error message in French in the event of translation failure.
- Parses the JSON string returned from the query to expose translated value.
- Creates French version of the attribute from translated value.
- Removes UTF8 Character code returned from translated results.

#### Temporal Extents Creator

This section tests for required temporal extents (data collection start and end dates) and creates default extents where missing.  The default temporal extents are set as follows:

- **data_collection_start_date:** 20 years prior to date data was processed by FME workspace.
- **data_collection_end_date:** the date data was processed by FME workspace.

#### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  
All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  
A list of all RI Codes, including RI Role Codes, can be found here:

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Second Contact Testing

Contact fields in XML templates cannot be incomplete.  Every data record has at least one contact.  The XML template allows for two.  This section tests if second contact exists 
in data record, then substitutes all second contact associated values with first contact values if second contact is missing.

  **Substituted values:**

  - contact name
  - contact email
  - contact role
  - contact role french
  - RI role code

#### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revises them to default 'asNeeded'.  The corresponding RI_Code 
is then applied to all values.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Spatial Representation Type Refiner

This section tests that Spatial Representation Type values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  The corresponding RI_Code 
and French language translation is then applied.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Progress Code Refiner

This section tests that Progress code values conform to HNAP requirements, and where nonconforming or missing, revise them to default 'vector'.  The corresponding RI_Code 
and French language translation is then applied.

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### File Format Refiner

There are up to ten transfer options (data links) available in Alberta datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis 
of all Alberta data has identified all the potential incorrect variations of required file format names (i.e.: 'uri' should be 'HTML', 'REST' should be 'ESRI REST').  There are a number 
of data formats that are not a variation of any valid data type.  This section tests for these valid formats found in Alberta datasets and renames them to the valid option 
'other' accordingly.

List of validated file formats can be found here:

-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

#### Keyword Attributor

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

#### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

#### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to six in Alberta datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

#### WMS Formatter

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

#### Insert/Update Filter

This section tests the 'Method' attribute applied in the New/Updated Records Filter section for 'Insert' or 'Update' values, and directs the dataset accordingly to the PyCSW Insert
or PyCSW UPDATE section of the workspace.

#### PyCSW Record Insert

Alberta datasets contain has a minimum of two and a maximum of six transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially 
six transfer options in each dataset (two to seven), requiring six templates.  

The XML insert templates can be found here:

-   [Alberta XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/AB/AB_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### PyCSW Record Update

Alberta datasets contain has a minimum of two and a maximum of six transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially 
six transfer options in each dataset (two to seven), requiring six templates.  

The XML update templates can be found here:

-   [Alberta XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/AB/AB_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- laces the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### Local Directory Writers

This section outputs each XML inserted or updated file to a local directory, sorted by succesful load or failure.  It is disabled by default but can be enabled 
if debugging of errors is required.

#### Insert Records Notification

This section performs the following tasks:
- Gets count of inserted records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Update Records Notification

This section performs the following tasks:
- Gets count of updated records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Notification Compliler and eMailer

This section performs the following tasks:
- Gets the current data and time.
- Concatenates insert records or no records to insert notifcation strings, update records or no records to update notification strings, plus date and time into one message string
- Emails the message string to an adminstrator.

## British Columbia

### Overview

British Columbia open data is exposed through a CKAN API:

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

ETL (extract, transformation and loading) workspaces created in Safe Software's Feature Manipulation Engine (FME) are used to extract and parse specific attributes from a JSON (Javascript Object Notation)
file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW 
(Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The FME workspaces have handlers appropriately placed to address attribute 
deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx)

There are three FME workspaces created to process BC Metadata:

-   **BC_Data_AllRecords_(revision_number).fmw:**  This FME workspace is for resetting and reloading the CSW.  It clears all data from the CSW and local directories (if they exist), extracts,
processes and reloads CSW and local directories with all current data.  It is intended for adminisrative use only.  It is dependent on another workspace (BC_Data_ClearCSW) that is initiated 
from a workspace runner.
-  **BC_Data_ClearCSW_(revision_number).fmw:** This FME workspace is initiated by the BC_Data_AllRecords workspace.  Once initiated it is set to complete its entire run before the initiating workspace 
can proceed any further.  This separation of workspaces is required to prevent loading and deletion of data simultaneously.
-  **BC_Data_NewAndUpdatedRecords_(revision_number).fmw:**: This FME workspace uses the same data extraction and transformation methods as BC_Data_AllRecords workspace, but is for daily 
extraction of new or updated data from the BC Data API, and inserting to the CSW.  It is intended to run on FME Server on a once daily schedule.

The BC Metadata FME Workspaces can be found here:

-   [BC FME Workspaces](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/BC/BC_FME_Workspaces)

**NOTE:** The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

### BC_Data_AllRecords Workspace/BC_Data_ClearCSW Detail

#### Data Clear

This section clears the CSW completely, and if utilizing the option to write all XML output to a local directory, clears the directory.  It utilizes the following steps:

-   **Workspace Runner:** This workspace runner initiates the BC_Data_ClearCSW workspace containing a custom transformer built on a loop.  The workspace runner is required to allow the loops 
to complete before initiating the rest of the processes in this tool.  
The custom transformer (Clear_PyCSW) is located in the FME Transformers folder and must be copied to any new FME environments in order for this tool to load.  Any edits required to this tool 
are performed by opening up the transformer itself in its home directory using FME Desktop.  
The loop is required because the sqlLite database which hosts the data for the CSW is limited in the number of records it can delete at a time.  This tool will delete the number of records 
that is set in the maxrecords property in default.cfg stored in the pycsw-2.2.0 directory.  The default setting for maxrecords is 100.  The default setting for number of loop iterations 
for this tool is 100, which allows for deletion of a maximum of 10000 records in the CSW database.  

-  **Clear XML_Results directory:** A system caller is used to clear the XML_Results directory.  This directory is not mandatory for the CSW, but creates local copies of XML files that were 
successfully published to the CSW.  Used primarily in development and could be disabled in a production environment by disabling the writers found in the Local Directory Writers bookmark. 

-  **Clear XML Failed directory:** A system caller is used to clear the XML_Failed directory.  This directory is not mandatory for the CSW, but creates local copies of XML files that 
failed to publish to the CSW.  Used primarily in development and could be disabled in a production environment by disabling the writers found in the Local Directory Writers bookmark.

#### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.  It is set
at default to perform 10 query loops.  
These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME
  
The current default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

#### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

#### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not Geographic.
- Filters out records that are not Open Data.
- Renames attributes that have index array to attribute name format that can be read by the XML templater.
- Filters out duplicate datasets that BC has already republished from NRCan.

#### Date/Time Testing

This section exists primarily for debugging purposes and can test for records that were created backdated to a specific number of days or months.  It's default setting for normal 
operation is 0, which nullifies the test.

#### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not find, a generic name, 
'BC Data Link' is inserted to the resource name attribute.

#### DeepL Translation

This section translates the following attributes from English to French using the DeepL language translation API:

- title
- notes
- sector
- all exposed tags attributes (maximum 9)
- all exposed resource_name attributes (maximum 10)

This section operates using the following steps:

- Removes failure causing excess whitespace from all attribute values to be translated.
- Concatenates query string to send to the DeepL API:
  - https://api.deepl.com/v2/translate?auth_key=$(DEEPL_KEY)&text=@Value(title)&source_lang=EN&target_lang=FR&split_sentences=1&preserve_formatting=1
  - **NOTE:** 'DEEPL_KEY' variable in concatenated value is the authorization key for DeepL API and is stored as a published parameter in FME, 'title' is the variable to be translated.
- Sends query string to the DeepL API.
- Substitutes the attribute value with hard coded error message in French in the event of translation failure.
- Parses the JSON string returned from the query to expose translated value.
- Creates French version of the attribute from translated value.
- Removes UTF8 Character code returned from translated results.

#### Temporal Extents Creator

This section tests for required temporal extents (data collection start and end dates) and creates default extents where missing.  The default temporal extents are set as follows:

- **data_collection_start_date:** 20 years prior to date data was processed by FME workspace.
- **data_collection_end_date:** the date data was processed by FME workspace.

#### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  
All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  
A list of all RI Codes, including RI Role Codes, can be found here:

-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Second Contact Testing

Contact fields in XML templates cannot be incomplete.  Every data record has at least one contact.  The XML template allows for two.  This section tests if second contact exists 
in data record, then substitutes all second contact associated values with first contact values if second contact is missing.

  **Substituted values:**

  - contact name
  - contact email
  - contact role
  - contact role french
  - RI role code

#### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revises them to default 'asNeeded'.  The corresponding RI_Code 
is then applied to all values.

#### File Format Refiner

There are up to ten transfer options (data links) available in BC datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis of all BC data
has identified all the potential incorrect variations of required file format names (i.e.: 'kmz' should be 'KMZ', 'Esri File Geodatabase' should be 'FGDB/GDB').  This section tests for all
the variations found in BC datasets and corrects them to conforming values where required.

List of validated file formats can be found here:

-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

#### Keyword Attributor

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

#### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

#### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to ten in BC datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

#### WMS Formatter

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

#### PyCSW Record Insert

BC datasets contain a maximum of ten transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially eleven transfer options in
each dataset, requiring eleven templates.  

The XML insert templates can be found here:

-   [BC XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/BC/BC_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### Local Directory Writers

This section outputs each XML file to a local directory, sorted by succesful load or failure.  It is disabled by default but can be enabled if debugging of errors is required.

#### Insert Records Notification

This section performs the following tasks:

- Gets count of records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Notification Compliler and eMailer

This section performs the following tasks:

- Gets the current date and time.
- Concatenates insert records notifcation string plus date and time into one message string
- Emails the message string to an adminstrator.

### BC_Data_NewAndUpdatedRecords

#### Query Loop Creation

This section uses FME transformers to create a repetitive query loop for the BC Data API as the API will only return 1000 records per query, less than that of the BC database.  It is set
at default to perform 10 query loops.  

These loop attributes are concatenated to a query string that updates to a new query starting point ('start_feature' variable) following the completion of each loop:

- https://catalogue.data.gov.bc.ca/api/3/action/package_search?start=@Value(**start_feature**)&rows=$(QUERY_ITERATIONS)   

- **NOTE:** 'QUERY_ITERATIONS' variable in concatenated value is the number of query loops and is stored as a published parameter in FME.
  
The current default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

#### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the response as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

#### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not Geographic.
- Filters out records that are not Open Data.
- Renames attributes that have index array to attribute name format that can be read by the XML templater.
- Filters out duplicate datasets that BC has already republished from NRCan.

#### Date/Time Testing

This section performs the following tasks:

- Extracts current date.
- Calculates time since last time tool processed.  Default setting is 1 day and is accessed in published parameter TIME_FILTER_DAYS.
- Tests for new records by comparing record_publish_date attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute with value 'Insert' for all new records.
- After new records are filtered, tests remainder for updated records by comparing record_last_modified attribute against time calculated in DateTimeCalculator.
- Creates 'Method' attribute 'Update' for all updated records.

#### No Records to Insert/Update Notification

- Verifies number of records that are to be inserted or updated.
- Concatenates message string for notification if there are no records to be inserted and/or updated.

#### Resource Name Tester

This section tests for a resource URL and verifies that each resource URL has a corresponding resource name.  If a corresponding resource name is not find, a generic name, 
'BC Data Link' is inserted to the resource name attribute.

#### DeepL Translation

This section translates the following attributes from English to French using the DeepL language translation API:

- title
- notes
- sector
- all exposed tags attributes (maximum 9)
- all exposed resource_name attributes (maximum 10)

This section operates using the following steps:

- Removes failure causing excess whitespace from all attribute values to be translated.
- Concatenates query string to send to the DeepL API:
  - https://api.deepl.com/v2/translate?auth_key=$(DEEPL_KEY)&text=@Value(title)&source_lang=EN&target_lang=FR&split_sentences=1&preserve_formatting=1
  - **NOTE:** 'DEEPL_KEY' variable in concatenated value is the authorization key for DeepL API and is stored as a published parameter in FME, 'title' is the variable to be translated.
- Sends query string to the DeepL API.
- Substitutes the attribute value with hard coded error message in French in the event of translation failure.
- Parses the JSON string returned from the query to expose translated value.
- Creates French version of the attribute from translated value.
- Removes UTF8 Character code returned from translated results.

#### Temporal Extents Creator

This section tests for required temporal extents (data collection start and end dates) and creates default extents where missing.  The default temporal extents are set as follows:
- **data_collection_start_date:** 20 years prior to date data was processed by FME workspace.
- **data_collection_end_date:** the date data was processed by FME workspace.

#### Role Refiner

This section tests that extracted role names are conforming to HNAP role code requirements.  Nonconforming or missing role names are set to pointOfContact as default.  
All role names have their corresponding French role names with their appropriate role code (IE: RI_414) applied to the dataset.  
A list of all RI Codes, including RI Role Codes, can be found here:
-   [RI Code Master List](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/RI_List.xlsx)

#### Second Contact Testing

Contact fields in XML templates cannot be incomplete.  Every data record has at least one contact.  The XML template allows for two.  This section tests if second contact exists 
in data record, then substitutes all second contact associated values with first contact values if second contact is missing.

  **Substituted values:**

  - contact name
  - contact email
  - contact role
  - contact role french
  - RI role code

#### Update Cycle Refiner

This section tests that Maintenance Frequency values conform to HNAP requirements, and where nonconforming or missing, revises them to default 'asNeeded'.  The corresponding RI_Code 
is then applied to all values.

#### File Format Refiner

There are up to ten transfer options (data links) available in BC datasets.  The file format of each transfer option has a specific validation requirement in the FGP.  Data analysis of all BC data
has identified all the potential incorrect variations of required file format names (i.e.: 'kmz' should be 'KMZ', 'Esri File Geodatabase' should be 'FGDB/GDB').  This section tests for all
the variations found in BC datasets and corrects them to conforming values where required.
List of validated file formats can be found here:
-   [Validated File Formats](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/VALIDATED_FILE_FORMATS.xlsx)

#### Keyword Attributor

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

#### SSL Protocol Test - Online Resource

This section tests the SSL protocol on the 'more_info.link_0' URL in CI_OnlineResource that are not contained in transferOptions and assigns 'HTTPS' or 'HTTP' to the protocol value.

#### SSL Protocol Test - Transfer Options

This section tests the SSL protocol in all 'resource_url' attributes (there are up to ten in BC datasets) in CI_OnlineResource that are contained in transferOptions and assigns 
'HTTPS' or 'HTTP' to the protocol value.

#### WMS Formatter

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

#### Insert/Update Filter

This section tests the 'Method' attribute applied in the New/Updated Records Filter section for 'Insert' or 'Update' values, and directs the dataset accordingly to the PyCSW Insert
or PyCSW UPDATE section of the workspace.

#### PyCSW Record INSERT

BC datasets contain a maximum of ten transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially eleven transfer options in
each dataset, requiring eleven templates.  

The XML insert templates can be found here:

-   [BC XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/BC/BC_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### PyCSW Record UPDATE

BC datasets contain a mimimum of one and a maximum of ten transfer options.  The WMS Formatter in this workspace will add an additional transfer option, so there are potentially eleven 
transfer options ineach dataset, requiring eleven templates.  

The XML update templates can be found here:

-   [BC XML Templates](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/tree/master/FME_fmw_files_and_templates/BC/BC_XML_Templates)

This section performs the following tasks:

- Tests for the number of transfer options and filters the datasets according to their number.
- Places the extracted attributes for each dataset in the XML template.
- Cleans up the XML document with the XML format tool.
- Validates the XML syntax.
- Posts each XML document to the PyCSW using the following Python script:
  - [PyCSW Post](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/scripts/PyCSW_Post.py)
- Tests each record for successful load or failure to the PyCSW

#### Local Directory Writers

This section outputs each XML inserted or updated file to a local directory, sorted by succesful load or failure.  It is disabled by default but can be enabled 
if debugging of errors is required.

#### Insert Records Notification

This section performs the following tasks:
- Gets count of inserted records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Update Records Notification

This section performs the following tasks:
- Gets count of updated records that successfully loaded or failed to load to the PyCSW.
- Creates a message string with the overall results of the data translation.

#### Notification Compliler and eMailer

This section performs the following tasks:
- Gets the current data and time.
- Concatenates insert records or no records to insert notifcation strings, update records or no records to update notification strings, plus date and time into one message string
- Emails the message string to an adminstrator.

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
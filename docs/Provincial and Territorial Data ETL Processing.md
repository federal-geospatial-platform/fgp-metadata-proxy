
Provincial and Territorial Extraction, Transformation and Loading Processes
==========
# Table of Contents
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes-1)
  - [Alberta](#alberta)
  - [British Columbia](#british-columbia)
    - [Overview](#overview)
	- [BC_Data_AllRecords Workspace Detail](#bc_data_allrecords-detail)
	- [Data Clear](#data-clear)
	- [Query Loop Creation](#query-loop-creation)
	- [Data Query](#data-query)
	- [Attribute Management](#attribute-management)
	- [Date/Time Testing](date/time-testing)
  - [Manitoba](#manitoba)
  - [New Brunswick](#new-brunswick)
  - [Newfoundland and Labrador](#newfoundland-and-labrador)
  - [Northwest Territories](#northwest-territories)
  - [Nova Scotia](#nova-scotia)
  - [Nunavut](#nunavut)
  - [Ontario](#ontario)
  - [Prince Edward Island](#prince-edward-island)
  - [Québec](#québec)
  - [Saskatchewan](#saskatchewan)
  - [Yukon](#yukon)
   
# Provincial and Territorial Extraction, Transformation and Loading Processes

## Alberta

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

Note: The CSW is a type built on Python scripting and may be referred to throughout this document as **PyCSW**.

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
at default to perform 10 query loops.  These loop attributes are concatenated to a query string that updates to a new query starting point following the completion of each loop.  The current
default settings will return a total of 10000 records, and, at the time of writing, there are less than 3000 open data records in BC open data.

#### Data Query

This section sends each concatentated query instance using a GET http method to the BC API, and returns the repsone as a JSON string.  A JSON fragmenter is used to extracts attributes 
and values from the JSON string based on a JSON query

#### Attribute Management

This section performs the following functions:

- Exposes specific attributes returned from the JSON query.  See [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx) file for details.
- Filters out records that are not Geographic.
- Renames attributes that have index array to attribute name format that can be read by the XML templater.
- Filters out duplicate datasets that BC has already republished from NRCan.

#### Date/Time Testing

This section exists primarily for debugging purposes and can test for records that were created backdated to a specific number of days or months.  It's default setting for normal 
operation is 0, which nullifies the test.








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
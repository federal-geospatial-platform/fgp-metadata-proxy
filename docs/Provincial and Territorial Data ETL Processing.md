
Provincial and Territorial Extraction, Transformation and Loading Processes
==========
# Table of Contents
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes-1)
  - [Alberta](#alberta)
  - [British Columbia](#british-columbia)
    - [Overview](#overview)
	- [BC_Data_AllRecords Detail](#bc_data_allrecords-detail)
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

### BC_Data_AllRecords Detail


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
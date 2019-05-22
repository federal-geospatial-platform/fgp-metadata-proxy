
Provincial and Territorial Extraction, Transformation and Loading Processes
==========
# Table of Contents
- [Provincial and Territorial Extraction, Transformation and Loading Processes](#provincial-and-territorial-extraction-transformation-and-loading-processes-1)
  - [Alberta] (#alberta)
  - [British Columbia](#british-columbia)
    - [Overview](#overview)
  - [Manitoba] (#manitoba)
  - [New Brunswick] (#new-brunswick)
  - [Newfoundland and Labrador] (#newfoundland-and-labrador)
  - [Northwest Territories] (#northwest-territories)
  - [Nova Scotia] (#nova-scotia)
  - [Nunavut] (#nunavut)
  - [Ontario] (#ontario)
  - [Prince Edward Island] (#prince-edward-island)
  - [Québec] (#quebec)
  - [Saskatchewan] (#saskatchewan)
  - [Yukon] (#yukon)
   
# Provincial and Territorial Extraction, Transformation and Loading Processes

## Alberta

## British Columbia

### Overview

British Columbia open data is exposed through a CKAN API:

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

An ETL (extract, transformation and loading) tool created in Safe Software's Feature Manipulation Engine (FME) is used to extract and parse specific attributes from a JSON (Javascript Object Notation)
file that are required to meet mandatory requirements for individual XML (Extensible Markup Language) files, each representing and defining a unique dataset, that are published to a CSW 
(Catalogue Service for the Web) and subsequently harvested from the CSW by the Federal Geospatial Platform (FGP).  The ETL tool has handlers appropriately placed to address attribute 
deficiencies that are either missing or have formats incompatible to FGP requirements.  

A detailed list of all attributes processed by FME for insertion to the XML files can be found here:

-   [FGP Attribute to XML Key](https://github.com/federal-geospatial-platform/fgp-metadata-proxy/blob/master/docs/FGP_Attribute-XML_Key.xlsx)

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
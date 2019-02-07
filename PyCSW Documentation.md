# pycsw 2.2.0 Documentation

## Index

* [Installation & Setup](#installation--setup)
  * [Download and Unzip](#download-and-unzip)
  * [Setup Python](#setup-python)
    * [Dependencies](#dependencies)
    * [Setup pycsw for Python](#setup-pycsw-for-python)
* [Running The Server](#running-the-server)
  * [Using WSGI](#using-wsgi)
* [Requests](#request)
  * [GetCapabilities](#getcapabilities)
    * [Description](#description)
    * [GET Request Example](#get-request-example)
  * [DescribeRecord](#describerecord)
    * [Description](#description-1)
    * [Required Parameters](#required-parameters)
    * [GET Request Example](#get-request-example-1)
  * [GetRecords](#getrecords)
    * [Description](#description-2)
    * [Required Parameters](#required-parameters-1)
    * [Optional Parameters](#optional-parameters)
    * [Output Schema](#setup-python)
    * [GET Request Example](#get-request-example-2)
    * [POST Request Example](#post-request-example)
  * [GetRecordById](#getrecordbyid)
    * [Required Parameters](#required-parameters-2)
    * [Optional Parameters](#optional-parameters-1)
    * [GET Request Example](#get-request-example-3)
  * [Transaction](#transaction)
    * [POST Dublin Core Example](#post-dublin-core-example)
    * [POST ISO 19139/19115 Example](#post-iso-19139-19115-example)

## Installation & Setup

### Download and Unzip

1.	Download the pycsw zip file from https://download.osgeo.org/pycsw/pycsw-2.2.0.zip
2.	Unzip the file to a preferred location (in this case C:\pycsw-2.2.0)

### Setup Python

NOTE: Make sure Python is installed before going through the next steps. To check if Python is installed, type ```python``` in a command prompt. If the error ```'python' is not recognized as an internal or external command, operable program or batch file.``` occurs, either Python is not installed or the Python installation location is not in the PATH Environment Variable.

### Dependencies

pycsw 2.2.0 requires the following Python package:
*	lxml v3.6.2
*	SQLAlchemy v1.2.16
*	pyproj v1.9.5.1
*	Shapely v1.5.17
*	OWSLib v0.16.0
*	six v1.10.0
*	xmltodict v0.10.2
*	geolinks v0.2.0

pycsw 2.2.0 only works with these specific versions. Any early or later packages will cause an error when running pycsw.

Each package can be installed using pip. In a command prompt, enter ```pip install <package>==<version>``` (lxml example: ```pip install lxml==3.6.2```)

### Setup pycsw for Python

1.	Open a Command Prompt window.
2.	Change the drive to C by typing ```C:```
3.	Navigate to C:\pycsw-2.2.0 by typing ```cd pycsw-2.2.0```
4.	To build the setup, type ```python setup.py build```
5.	To install, type ```python setup.py install```

## RUNNING THE SERVER

### Using WSGI

Web Server Gateway Interface (WSGI) can be used to run the pycsw server. In a command prompt, enter ```python pycsw/wsgi.py``` in the pycsw-2.2.0 folder.

## REQUESTS

All requests require the following parameters:

| Parameter | Description | Valid Options |
| --------- | ----------- | ------------- |
| service | | CSW |
| version | The version number of the CSW service. | 2.0.2 |

### GetCapabilities

#### Description

The GetCapabilities request retrieves the service metadata from the server in XML format. The GetCapabilities request contains no required parameters.

#### GET Request Example

http://localhost:8000/csw?service=CSW&version=2.0.2&request=GetCapabilities

### DescribeRecord

#### Description

The DescribeRecord request provides access to the elements of the information model supported by the service.

#### Required Parameters

The following parameters are required for DescribeRecord requests:

| Parameter | Description | Valid Options |
| --------- | ----------- | ------------- |
| outputFormat | | application/json<br>application/xml |
| schemaLanguage | | http://www.w3.org/2001/XMLSchema<br>http://www.w3.org/TR/xmlschema-1/<br>http://www.w3.org/XML/Schema |
| typeName | | csw:Record<br>gmd:MD_Metadata |

#### GET Request Example

http://localhost:8000/geonetwork/srv/eng/csw?request=DescribeRecord&service=CSW&version=2.0.2&outputFormat=application/xml&schemaLanguage=http://www.w3.org/XML/Schema

### GetRecords

#### Description

The GetRecords request allows the user to query the catalogue metadata records using an optional filter in either CQL text or OCG filter XML.

#### Required Parameters

The following parameters are required for GetRecords requests:

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>Parameter Description</th>
            <th>Options</th>
	    <th>Description</th>
        </tr>
    </thead>
    <tbody>
	<!-- First row -->
        <tr>
            <td rowspan=2>CONSTRAINTLANGUAGE</td>
            <td rowspan=2>The CONSTRAINTLANGUAGE is used to specify the predicate language being used.</td>
            <td>CQL_TEXT</td>
	    <td>CQL (Common Query Language) is a query language created by the OGC for the Catalogue Web Services specification. Unlike the XML-based Filter Encoding language, CQL is written using a familiar text-based syntax. It is thus more readable and better-suited for manual authoring.</td>
        </tr>
        <tr>
	    <td>FILTER</td>
            <td>Filter is (usually) an OGC filter which is expressed in XML and is more suited for machines to write.</td>
        </tr>
	<!-- 2nd row -->
        <tr>
            <td rowspan=3>ElementSetName</td>
            <td rowspan=3>Specifies a named, predefined set of metadata record elements from each source record that should be presented in the response to the operation.</td>
            <td>brief</td>
	    <td>Returns the least amount of detail.</td>
        </tr>
        <tr>
	    <td>full</td>
            <td>Represents all the metadata record elements.</td>
        </tr>
	<tr>
	    <td>summary</td>
            <td></td>
        </tr>
	<!-- 3rd row -->
	<tr>
            <td rowspan=3>ElementSetName</td>
            <td rowspan=3>Specifies a named, predefined set of metadata record elements from each source record that should be presented in the response to the operation.</td>
            <td>brief</td>
	    <td>Returns the least amount of detail.</td>
        </tr>
        <tr>
	    <td>full</td>
            <td>Represents all the metadata record elements.</td>
        </tr>
	<tr>
	    <td>summary</td>
            <td></td>
        </tr>
	<!-- 4th row -->
	<tr>
            <td rowspan=3>outputFormat</td>
            <td rowspan=3>Document format for output.</td>
            <td>application/atom+xml</td>
	    <td></td>
        </tr>
        <tr>
	    <td>application/json</td>
            <td></td>
        </tr>
	<tr>
	    <td>application/xml</td>
            <td></td>
        </tr>
	<!-- 5th row -->
	<tr>
            <td rowspan=3>typeNames</td>
            <td rowspan=3>The typeNames parameter is a list of one or more names of queryable entities in the catalogue's information model that may be constrained in the predicate of the query.</td>
            <td>csw30:Record</td>
	    <td></td>
        </tr>
        <tr>
	    <td>csw:Record</td>
            <td></td>
        </tr>
	<tr>
	    <td>gmd:MD_Metadata</td>
            <td></td>
        </tr>
	<!-- 6th row -->
	<tr>
            <td rowspan=3>resultType</td>
            <td rowspan=3></td>
            <td>hits</td>
	    <td></td>
        </tr>
        <tr>
	    <td>results</td>
            <td></td>
        </tr>
	<tr>
	    <td>validate</td>
            <td></td>
        </tr>
    </tbody>
</table>	
    
#### Optional Parameters

These are some useful optional parameters for the GetRecords request:

| Parameter | Parameter Description | Options |
| --------- | --------------------- | ------- | 
| startPosition | Specifies the record position the search results should start. | Any integer above 0 |
| maxRecords | Specifies the maximum number of records should be returned. | Any integer above 0 |
| Constraint | Specifies the filter for the query. | A filter either in CQL language or a Filter XML, depending on the CONSTRAINTLANGUAGE parameter. |
| outputSchema | Specifies the URI for the schema to return the record. | (see section on [Output Schema](#output-schema) below) |

For a complete list of GetRecords parameters, visit http://reference1.mapinfo.com/software/spectrum/lim/8_0/services/Spatial/source/Services/csw/postget/postgetgetrecords.html

#### Output Schema

The outputSchema parameter uses a URI that specifies the schema to use for returning the results.
The following schemas are available for pycsw servers:

http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/
http://www.interlis.ch/INTERLIS2.3
http://www.isotc211.org/2005/gmd
http://www.opengis.net/cat/csw/3.0
http://www.opengis.net/cat/csw/csdgm
http://www.w3.org/2005/Atom

The following schemas are available for the FGP CSW server:

http://www.opengis.net/cat/csw/2.0.2
http://www.isotc211.org/2005/gmd
http://www.ec.gc.ca/napec
http://www.ec.gc.ca/ECDMP/schemas/MonitoringSite/1-0-0

#### GET Request Examples

The following request retrieves the first 10 records in the service:

http://localhost:8000/csw?service=CSW&version=2.0.2&request=GetRecords&CONSTRAINTLANGUAGE=CQL_TEXT&ElementSetName=full&outputFormat=application/xml&typeNames=gmd:MD_Metadata&resultType=results

The following request returns any records containing the word ‘Lorem’ (using constraint with CQL csw:AnyText like ‘%Lorem%’):

http://localhost:8000/csw?service=CSW&version=2.0.2&request=GetRecords&CONSTRAINTLANGUAGE=CQL_TEXT&ElementSetName=full&outputFormat=application/xml&typeNames=gmd:MD_Metadata&resultType=results&Constraint=csw:AnyText%20like%20%27%Lorem%%27&constraint_language_version=1.1.0

#### POST Request Example

This example sends a POST request to get any record containing ‘Lorem’:

**URL**: ```http://localhost:8000/csw```<br>
**Content-type**: ```application/xml```<br>
**POST Data**:
```<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords
    service="CSW"
    version="2.0.2"
    resultType="results"
    outputFormat="application/xml"
    outputSchema="http://www.opengis.net/cat/csw/2.0.2"
    xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"
    xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xmlns:gml="http://www.opengis.net/gml"
    xmlns:ows="http://www.opengis.net/ows"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <csw:Query typeNames="csw:Record">
        <csw:ElementSetName typeNames="gmd:MD_Metadata">full
  </csw:ElementSetName>
        <csw:Constraint version="1.1.0">
            <Filter
                xmlns="http://www.opengis.net/ogc"
                xmlns:gml="http://www.opengis.net/gml">
                <PropertyIsEqualTo>
                    <PropertyName>csw:AnyText</PropertyName>
                    <Literal>Lorem</Literal>
                </PropertyIsEqualTo>
            </Filter>
        </csw:Constraint>
    </csw:Query>
</csw:GetRecords>
```

For more Filter examples, visit http://reference1.mapinfo.com/software/spectrum/lim/8_0/services/Spatial/source/Services/csw/filters/filterexamples.html

### GetRecordById

The GetRecordById returns a record based on a given identifier.

#### Required Parameters

The following parameters are required for GetRecordById requests:

| Parameter | Parameter Description | Options |
| --------- | --------------------- | ------- |
| id | URI identifier of one or more records to return. | Identifiers separated by commas. |

#### Optional Parameters



These are some useful optional parameters for the GetRecordById request:

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>Parameter Description</th>
            <th>Options</th>
	    <th>Description</th>
        </tr>
    </thead>
    <tbody>
	<!-- First row -->
        <tr>
            <td rowspan=3>ElementSetName</td>
            <td rowspan=3>Specifies a named, predefined set of metadata record elements from each source record that should be presented in the response to the operation.</td>
            <td>brief</td>
	    <td>Returns the least amount of detail.</td>
        </tr>
        <tr>
	    <td>full</td>
            <td>Represents all the metadata record elements.</td>
        </tr>
	<tr>
	    <td>summary</td>
            <td></td>
        </tr>
	<!-- 2nd row -->
	<tr>
            <td rowspan=3>outputFormat</td>
            <td rowspan=3>Document format for output.</td>
            <td>application/atom+xml</td>
	    <td></td>
        </tr>
        <tr>
	    <td>application/json</td>
            <td></td>
        </tr>
	<tr>
	    <td>application/xml</td>
            <td></td>
        </tr>
	<!-- 3rd row -->
	<tr>
            <td>outputSchema</td>
            <td>Specifies the URI for the schema to return the record.</td>
	    <td>see section on <a href="#output-schema">Output Schema</a> above</td>
	    <td></td>
        </tr>
    </tbody>
</table>

#### GET Request Example

The following request returns the full results for the record with identifier 0b229ec0-da50-4b29-88da-49c85a5944e2:
http://localhost:8000/csw?service=CSW&version=2.0.2&request=GetRecordById&ElementSetName=full&id=0b229ec0-da50-4b29-88da-49c85a5944e2

### Transaction

The Transaction request allows the user to create, modify and delete catalog records.

NOTE: To perform Transactions in pycsw, set the ‘transactions’ property under the [manager] section in the configuration file to ‘true’.

#### POST Dublin Core Example

This example adds a new record into the catalog using Dublin Core XML tags:

**URL**: ```http://localhost:8000/csw```<br>
**Content-type**: ```application/xml```<br>
**POST Data**:
```<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
  <csw:Insert typeName="csw:Record">
    <csw:Record xmlns:ows="http://www.opengis.net/ows"
        xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dct="http://purl.org/dc/terms/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <dc:contributor>Susan J. Green</dc:contributor>
          <dc:contributor>Bill Dowedoff</dc:contributor>
          <dc:coverage>-139.5, 60.0, -113.5, 48.0</dc:coverage>
          <dc:creator>Heritage</dc:creator>
          <dc:date>2017-01-26</dc:date>
          <dc:description>Simple Dublin Core generation
    </dc:description>
          <dc:format>application/xml</dc:format>
          <dc:identifier>dublin-core</dc:identifier>
          <dc:language>en</dc:language>
          <dc:publisher>CERN</dc:publisher>
          <dc:relation>Invenio Software</dc:relation>
          <dc:rights>MIT</dc:rights>
          <dc:source>Python</dc:source>
          <dc:title>Historic Trails of British Columbia</dc:title>
          <dc:type>Software</dc:type>
    </csw:Record>
  </csw:Insert>
</csw:Transaction>
```

For more Transaction examples, visit http://reference1.mapinfo.com/software/spectrum/lim/8_0/services/Spatial/source/Services/csw/postget/postgettransaction.html

#### POST ISO 19139/19115 Example

The following example uses ISO 19139/19115 XML tags to insert a record into the pycsw (most sub-tags have been removed due to the number of elements in the ISO XML):

**URL**: ```http://localhost:8000/csw```<br>
**Content-type**: ```application/xml```<br>
**POST Data**:
```<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
  <csw:Insert>
    <gmd:MD_Metadata xmlns:gmd="http://www.isotc211.org/2005/gmd"
xmlns:srv="http://www.isotc211.org/2005/srv" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gfc="http://www.isotc211.org/2005/gfc" xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:gss="http://www.isotc211.org/2005/gss" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns="http://www.isotc211.org/2005/gmd" xmlns:geonet="http://www.fao.org/geonetwork" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/gmd/gmd.xsd http://www.isotc211.org/2005/srv http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/srv/srv.xsd http://www.geconnections.org/nap/napMetadataTools/napXsd/napm http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/napm/napm.xsd">
      <gmd:fileIdentifier>
        <gco:CharacterString>c87886cd-d37e-459c-945f-ca35f8055e85</gco:CharacterString>
      </gmd:fileIdentifier>
      <gmd:language>
        <gco:CharacterString>eng; CAN</gco:CharacterString>
      </gmd:language>
	…
    </gmd:MD_Metadata>
  </csw:Insert>
</csw:Transaction>
```

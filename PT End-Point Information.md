# P/T End-Point Information

## BC End-Points

[Data Catalogue](#data-catalogue)<br>
[ArcGIS Online Maps](#arcgis-online-maps)<br>
[FTP](#ftp)<br>
[Interactive Maps](#interactive-maps)<br>
[Map Services](#map-services)<br>
[Web Pages](#web-pages)<br>

---

### Data Catalogue

#### Description
The BC Data Catalogue is a search engine which allows users to locate datasets in DataBC. The Data Catalogue also includes an API for easy automatic searches. The BC Data Catalogue is powered by CKAN.

#### URLs
**Catalogue URL**: https://catalogue.data.gov.bc.ca/dataset<br>
**API URL**: https://catalogue.data.gov.bc.ca/api/3<br>

#### Catalogue Querying
Use the following parameters, along with the Catalogue URL, to search for datasets in the Data Catalogue:
* ***q***: Filter the results by key word search.
* ***type***: Filter the results by the dataset type.
* ***license_id***: Filter results by the license.
* ***sector***: Filter results by sector.
* ***res_format***: Filter the results by format.
* ***organization***: Filter results by organization.
* ***download_audience***: Filter results by download permission.

**Example**: To search for datasets with dataset type 'Geographic' using the word 'roads', use the following URL:
https://catalogue.data.gov.bc.ca/dataset?q=roads&type=Geographic

#### API Extraction
The search results and dataset pages in the Catalogue can be accessed using [CKAN's Action API](https://ckan.org/portfolio/api/).<br>
To get a list of search results in JSON format, use CKAN's Package Search (for BC's Catalogue: https://catalogue.data.gov.bc.ca/api/3/action/package_search).<br>
For a complete list of available parameters, see https://wiki.apache.org/solr/CommonQueryParameters.

**Example**: To get a list results in JSON format using the API with dataset type 'Geographic' using the word 'roads', use the following URL:
* https://catalogue.data.gov.bc.ca/api/3/action/package_search?q=roads&fq=type:Geographic&rows=1000000<br>
The "rows=1000000" returns all the results in the JSON.

The API can also be used to access individual datasets using the URL https://catalogue.data.gov.bc.ca/api/3/action/package_show and the parameter 'id' with the dataset's name.

**Example**: To view the dataset [Forest Road Segment Tenure](https://catalogue.data.gov.bc.ca/dataset/forest-road-segment-tenure) in JSON format, use https://catalogue.data.gov.bc.ca/api/3/action/package_show?id=forest-road-segment-tenure.

---

### ArcGIS Online Maps
An ArcGIS Online Map can be viewed online or can be accessed in JSON format. Every map has a unique ID which is used to view the map itself or access its metadata.

The URL for the viewer can vary depending on the type of map (for example, the webmaps on BC's site are located at https://governmentofbc.maps.arcgis.com/home/webmap/viewer.html while BC's MapSeries are located at https://governmentofbc.maps.arcgis.com/apps/MapSeries/index.html). However, the base URL for the JSON metadata, without the ID, is the same (in BC's case, https://governmentofbc.maps.arcgis.com/sharing/rest/content/items).

**Example**: The URL for the map of BC's Groundwater Level Data is https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=b53cb0bf3f6848e79d66ffd09b74f00d. Using the ID from this URL and the metadata URL, the JSON content can be accessed using https://governmentofbc.maps.arcgis.com/sharing/rest/content/items/<ID\>?f=pjson or https://governmentofbc.maps.arcgis.com/sharing/rest/content/items/b53cb0bf3f6848e79d66ffd09b74f00d?f=pjson

---

### FTP
BC's FTP site contains a large collection of geospatial datasets.
#### FTP URL
ftp://ftp.geobc.gov.bc.ca
#### Access
The FTP site can be accessed using any FTP application. Python's FTP protocol client package, ftplib, is used to access the site automatically.

---

### Interactive Maps
The interactive maps for BC use different mapping applications, such as Google Maps or Geocortex. Here are a few examples of BC's interactive maps:
* http://www.env.gov.bc.ca/bcparks/explore/map.html
* http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html
* http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/real-time-water-data-reporting
		
---

### Map Services
BC has two types of map services, ArcGIS REST and WMS.
#### ArcGIS REST Service
There are two ArcGIS REST Services for BC. They are located at:
* https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services
* http://maps.gov.bc.ca/arcserver/rest/services

The metadata for these services can be accessed in JSON format by appending "?f=pjson" to the end of their URL. So the JSON data URLs for both services are:
* https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services?f=pjson
* http://maps.gov.bc.ca/arcserver/rest/services?f=pjson

There are sub-folder links and layer links found throughout the service data. Adding "?f=pjson" to these links will return the JSON results.

#### WMS
There are three WMS sites for BC:
* http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?service=wms&request=getcapabilities&version=1.3.0
* http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?wms_landsat?service=wms&request=getcapabilities&version=1.3.0
* https://openmaps.gov.bc.ca/lzt/ows?service=wms&version=1.1.1&request=getcapabilities

The XML metadata is accessed using the 'getcapabilities' request.

---

### Web Pages
Web pages are any sites that contain links to geospatial datasets that are not found in any of the above end-point categories. The layout of each web page varies from site to site. Some of the metadata information can be taken from the page's metadata tags.

Some BC examples of web pages containing geospatial data are:
* https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/orthophotos/orthophoto-viewer
* https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/air-photos/air-photo-viewer
* https://www2.gov.bc.ca/gov/content/data/geographic-data-services/georeferencing/survey-control-operations
* https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder')
